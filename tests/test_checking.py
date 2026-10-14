"""drawzero.checking: reading EJUDGE_MODE output back, the geometry, the ejudge entry."""
from pathlib import Path
import os
import subprocess
import sys
import textwrap

import pytest

from drawzero import checking as c

ROOT = Path(__file__).resolve().parents[1]


def drawing_of(source):
    env = {**os.environ, 'EJUDGE_MODE': '1', 'PYTHONPATH': str(ROOT / 'src')}
    out = subprocess.run([sys.executable, '-c', textwrap.dedent(source)], capture_output=True, text=True, env=env,
                         check=True, stdin=subprocess.DEVNULL).stdout
    return c.parse(out)


def test_parse_reads_every_shape_back():
    d = drawing_of('''
        from drawzero import *
        fill('white')
        line('red', (10, 20), (30, 40))
        filled_circle((0, 0, 255, 100), (500, 500), 50)
        rect('green', (10, 20), 30, 40, line_width=2)
        filled_rect_rotated('red', (500, 500), 100, 50, 0)
        tick()
        text('white', 'Hi', (5, 6), 30)
        print('stray')
    ''')
    assert [s.name for s in d.shapes] == ['fill', 'line', 'filled_circle', 'rect', 'filled_polygon', 'text']
    assert d.shapes[1].points == [(10, 20), (30, 40)]
    assert d.shapes[2].center == (500, 500) and d.shapes[2].radius == 50 and d.shapes[2].alpha == 100
    assert d.shapes[3].rectangle() == c.Rect(10, 20, 40, 60) and not d.shapes[3].filled
    assert d.shapes[4].rectangle() == c.Rect(500, 500, 600, 550)  # pos is a corner
    assert d.shapes[5].frame == 1 and d.ticks == 1
    assert d.stray == ['stray']


def test_rect_relations():
    big, small = c.Rect(0, 0, 100, 100), c.Rect(10, 10, 90, 90)
    assert big.contains(small, strict=True) and not small.contains(big)
    assert c.Rect(0, 0, 10, 10).touches(c.Rect(10, 0, 20, 10))
    assert not c.Rect(0, 0, 10, 10).touches(c.Rect(11, 0, 20, 10))
    assert c.Rect(0, 40, 100, 60).crosses(c.Rect(40, 0, 60, 100))
    assert c.Rect(0, 0, 100, 20).orientation == 'horizontal'


def test_polygons():
    square = [(0, 0), (10, 0), (10, 10), (0, 10)]
    assert c.area(square) == 100
    assert c.is_rectangle(square) and c.is_square(square)
    assert c.is_rectangle([(5, 0), (10, 5), (5, 10), (0, 5)]) and c.axis_rect([(5, 0), (10, 5), (5, 10), (0, 5)]) is None
    assert c.point_in_polygon((5, 5), square) and c.point_in_polygon((0, 5), square)
    assert not c.point_in_polygon((0, 5), square, boundary=False)
    assert c.polygon_inside([(2, 2), (8, 2), (5, 8)], square)
    assert not c.polygon_inside([(2, 2), (18, 2), (5, 8)], square)
    assert c.polygons_overlap(square, [(5, 5), (20, 5), (5, 20)])
    assert not c.polygons_overlap(square, [(50, 50), (60, 50), (50, 60)])
    assert not c.is_triangle([(0, 0), (5, 5), (10, 10)])


def test_circles_and_colours():
    a = c.Shape('circle', center=(0, 0), radius=10)
    assert c.circles(a, c.Shape('circle', center=(2, 0), radius=5)) == 'inside'
    assert c.circles(a, c.Shape('circle', center=(5, 0), radius=5)) == 'touch_inside'
    assert c.circles(a, c.Shape('circle', center=(30, 0), radius=5)) == 'outside'
    assert c.circles(a, c.Shape('circle', center=(12, 0), radius=5)) == 'cross'
    assert c.same_color((2, 255, 85), c.GREEN) and not c.same_color(c.RED, c.YELLOW)
    assert c.color_name((255, 0, 0)) == 'red' and c.color_name((1, 2, 3)) == '(1, 2, 3)'


def test_color_at_paints_in_order():
    d = drawing_of('''
        from drawzero import *
        fill('white')
        filled_rect('blue', (100, 100), 200, 200)
        circle('red', (200, 200), 50, line_width=10)
        filled_circle((0, 255, 0, 50), (200, 200), 20)
    ''')
    assert c.color_at(d.shapes, (10, 10)) == c.WHITE
    assert c.color_at(d.shapes, (150, 150)) == c.BLUE
    assert c.color_at(d.shapes, (245, 200)) == c.RED
    assert c.color_at(d.shapes, (200, 200)) == c.BLUE  # alpha 50 is see-through


def test_main_exit_codes(tmp_path):
    (tmp_path / 'in').write_text('')
    out = tmp_path / 'out'

    def three_lines(drawing, test_input, answer):
        if len(drawing.only('line')) != 3:
            raise c.Wrong(c.say('Three lines.', 'Три линии.'))

    out.write_text('{"figure": "line", "color": [1, 2, 3], "start": [0, 0], "end": [1, 1], "alpha": 255, "line_width": 4}\n' * 3)
    assert c.main(three_lines, ['check', str(tmp_path / 'in'), str(out)]) == c.OK
    out.write_text('{"figure": "line", "color": [1, 2, 3], "start": [0, 0], "end": [1, 1], "alpha": 255, "line_width": 4}\n')
    assert c.main(three_lines, ['check', str(tmp_path / 'in'), str(out)]) == c.WRONG_ANSWER
    out.write_text('')
    assert c.run(three_lines, ['check', str(tmp_path / 'in'), str(out)]) == (c.WRONG_ANSWER, c.say('Nothing is drawn.', 'Ничего не нарисовано.'))
    out.write_text('hello\n')
    assert c.run(three_lines, ['check', str(tmp_path / 'in'), str(out)])[0] == c.WRONG_ANSWER

    def crash(drawing, test_input, answer):
        raise ValueError('bug')

    out.write_text('{"figure": "clear"}\n')
    assert c.main(crash, ['check', str(tmp_path / 'in'), str(out)]) == c.CHECK_FAILED
