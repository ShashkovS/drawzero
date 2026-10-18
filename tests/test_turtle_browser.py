"""The browser turtle, driven by the fake page of ``browser_harness``."""
import math

import pytest

from .test_renderer_browser import all_ops, run


def paths(report):
    return [op for op in all_ops(report) if op[0] == 'path']


def last_sprites(report):
    sprites = [op for op in all_ops(report) if op[0] == 'sprites']
    return sprites[-1][1] if sprites else None


def test_a_square_on_a_white_window(tmp_path):
    report = run('''
        import turtle
        t = turtle.Turtle()
        t.speed(0)
        for _ in range(4):
            t.forward(100)
            t.left(90)
        turtle.done()
    ''', tmp_path, frames=1000)
    assert report['status'] == 'completed', report['error']
    ops = all_ops(report)
    assert ops[:2] == [['clear'], ['bg', [255, 255, 255, 255]]]
    # 800 x 800 window on the 1000 x 1000 canvas: a turtle pixel is 1.25 canvas pixels
    lines = [op[3] for op in paths(report)]
    assert lines == [[500, 500, 625, 500], [625, 500, 625, 375], [625, 375, 500, 375], [500, 375, 500, 500]]
    assert paths(report)[0][1:3] == [[0, 0, 0, 255], 1.25]
    # the turtle is shown at the end: the classic arrow, at home, heading east
    sprite = last_sprites(report)
    assert [op[0] for op in sprite] == ['polygon', 'path']
    assert sprite[0][3][:2] == [500, 500]


def test_speed_cuts_a_move_into_cpython_steps(tmp_path):
    report = run('''
        import turtle
        turtle.speed(1)
        turtle.forward(100)
    ''', tmp_path, frames=1000)
    # CPython: 1 + int(100 / (3 * 1.1 * 1)) = 31 steps of 10 ms each
    assert len(paths(report)) == 31
    assert sum(f['wait'] for f in report['frames']) == pytest.approx(0.31, abs=0.02)
    assert len(report['frames']) < 31  # joined into frames of at least 1/60 s


def test_tracer_zero_draws_in_one_frame(tmp_path):
    report = run('''
        import turtle
        turtle.tracer(0)
        for i in range(500):
            turtle.forward(5)
            turtle.left(1)
        turtle.update()
    ''', tmp_path, frames=1000)
    assert len(paths(report)) == 500
    assert len(report['frames']) <= 3


def test_circle_is_cpythons_polygon(tmp_path):
    report = run('''
        import turtle
        turtle.tracer(0)
        turtle.circle(60)
    ''', tmp_path)
    steps = 1 + int(min(11 + 60 / 6.0, 59.0))
    assert len(paths(report)) == steps
    side = 2 * 60 * math.sin(math.radians(180 / steps)) * 1.25
    for op in paths(report):
        x1, y1, x2, y2 = op[3]
        assert math.hypot(x2 - x1, y2 - y1) == pytest.approx(side, abs=0.01)


def test_fill_lies_under_its_lines(tmp_path):
    report = run('''
        import turtle
        turtle.tracer(0)
        turtle.color('red', 'yellow')
        turtle.begin_fill()
        for _ in range(3):
            turtle.forward(100)
            turtle.left(120)
        turtle.end_fill()
    ''', tmp_path)
    kinds = [op[0] for op in all_ops(report) if op[0] in ('path', 'polygon')]
    # three lines, then the fill, then the same lines again over it
    assert kinds[:7] == ['path'] * 3 + ['polygon'] + ['path'] * 3
    fill = [op for op in all_ops(report) if op[0] == 'polygon'][0]
    assert fill[1] == [255, 255, 0, 255]


def test_setup_scales_the_window_to_the_canvas(tmp_path):
    report = run('''
        import turtle
        turtle.setup(500, 500)
        turtle.tracer(0)
        print(turtle.window_width(), turtle.window_height())
        turtle.forward(250)
    ''', tmp_path)
    assert paths(report)[-1][3] == [500, 500, 1000, 500]


def test_colors_logo_mode_and_state(tmp_path):
    report = run('''
        import turtle
        turtle.tracer(0)
        turtle.mode('logo')
        assert turtle.heading() == 0
        turtle.forward(10)
        assert turtle.pos() == (0, 10), turtle.pos()
        turtle.right(90)
        assert turtle.heading() == 90
        turtle.colormode(255)
        turtle.pencolor(10, 20, 30)
        assert turtle.pencolor() == (10, 20, 30)
        turtle.pencolor('#ff8000')
        turtle.forward(10)
        turtle.pencolor('dark slate gray')
        turtle.forward(10)
        assert repr(turtle.pos()) == '(20.00,10.00)'
        try:
            turtle.pencolor('no such colour')
        except turtle.TurtleGraphicsError:
            pass
        else:
            raise AssertionError('a bad colour must fail')
    ''', tmp_path)
    assert report['status'] == 'completed', report['error']
    assert [op[1] for op in paths(report)] == [[0, 0, 0, 255], [255, 128, 0, 255], [47, 79, 79, 255]]


def test_keys_and_timers_run_in_mainloop(tmp_path):
    report = run('''
        import turtle
        turtle.tracer(0)
        def up():
            turtle.forward(10)
        def tick():
            turtle.left(90)
            turtle.ontimer(tick, 1000000)
        turtle.onkey(up, 'Up')
        turtle.onkeypress(lambda: turtle.bye(), 'q')
        turtle.ontimer(tick, 0)
        turtle.listen()
        turtle.mainloop()
    ''', tmp_path, frames=50, events=[[], [{'t': 'kd', 'code': 'ArrowUp', 'key': 'ArrowUp'}],
                                      [{'t': 'ku', 'code': 'ArrowUp', 'key': 'ArrowUp'}], [],
                                      [{'t': 'kd', 'code': 'KeyQ', 'key': 'q'}]])
    assert report['status'] == 'completed', report['error']
    # the timer turned the turtle north before the key release moved it
    assert paths(report)[0][3] == [500, 500, 500, 487.5]


def test_mainloop_without_handlers_returns(tmp_path):
    report = run('''
        import turtle
        turtle.forward(1)
        turtle.mainloop()
        print('after')
    ''', tmp_path)
    assert report['status'] == 'completed'


def test_screen_click_and_stamps(tmp_path):
    report = run('''
        import turtle
        turtle.tracer(0)
        screen = turtle.Screen()
        seen = []
        def click(x, y):
            seen.append((x, y))
            turtle.goto(x, y)
            turtle.stamp()
            if len(seen) == 2:
                assert seen == [(0, 0), (-400, 400)], seen
                turtle.clearstamps(1)
                turtle.bye()
        screen.onscreenclick(click)
        screen.mainloop()
    ''', tmp_path, frames=50, events=[[{'t': 'md', 'b': 1, 'x': 500, 'y': 500}], [],
                                      [{'t': 'md', 'b': 1, 'x': 0, 'y': 0}]])
    assert report['status'] == 'completed', report['error']
    assert ['clear'] in all_ops(report)[2:]  # clearstamps redrew the picture


def test_write_names_its_font(tmp_path):
    report = run('''
        import turtle
        turtle.hideturtle()
        turtle.write('Hello', align='center', font=('Courier', 12, 'bold italic'))
    ''', tmp_path)
    text = [op for op in all_ops(report) if op[0] == 'text'][0]
    assert text[2:5] == ['Hello', 500, 500]
    assert text[5] == pytest.approx(12 * 4 / 3 * 1.25)
    assert text[6:] == ['.v', ['Courier', 'bold', 'italic']]
    assert last_sprites(report) == []


def test_sleep_keeps_the_screen_live(tmp_path):
    report = run('''
        import time
        import turtle
        turtle.tracer(0)
        turtle.forward(10)
        time.sleep(0.25)
        turtle.forward(10)
    ''', tmp_path)
    assert sum(f['wait'] for f in report['frames']) >= 0.2
    assert report['frames'][0]['ops'][-2][0] == 'path'  # the first line was shown before the sleep


def test_an_endless_loop_stops(tmp_path):
    report = run('''
        import turtle
        turtle.speed(10)
        while True:
            turtle.forward(50)
            turtle.left(170)
    ''', tmp_path, frames=20)
    assert report['status'] == 'stopped'
