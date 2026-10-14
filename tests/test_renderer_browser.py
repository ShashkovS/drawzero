"""The browser backend, driven by a fake page in a fresh subprocess."""
from pathlib import Path
import json
import os
import subprocess
import sys
import textwrap

import pytest

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / 'tests/browser_harness.py'
EXAMPLES = sorted((ROOT / 'src/drawzero/examples').glob('[0-9][0-9]_*.py'))


def run(source, tmp_path, frames=10, events=None):
    program = tmp_path / 'program.py'
    program.write_text(textwrap.dedent(source), encoding='utf-8')
    command = [sys.executable, str(HARNESS), str(program), '--frames', str(frames)]
    if events is not None:
        command += ['--events', json.dumps(events)]
    env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src')}
    result = subprocess.run(command, capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL, env=env)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout.strip().splitlines()[-1])


def all_ops(report):
    return [op for frame in report['frames'] for op in frame['ops']]


def test_static_picture_is_one_frame(tmp_path):
    report = run('''
        from drawzero import *
        line('red', (10, 20), (30, 40))
        filled_circle((0, 0, 255, 100), (500, 500), 50)
        rect('green', (10, 20), 30, 40, alpha=128, line_width=2)
        text('white', 'Hi', (500, 70), 48, '.^')
    ''', tmp_path)
    assert report['status'] == 'completed'
    assert len(report['frames']) == 1
    assert report['frames'][0]['wait'] == 0
    assert all_ops(report) == [
        ['line', [255, 0, 0, 255], 4, 10, 20, 30, 40],
        ['circle', [0, 0, 255, 100], 0, 500, 500, 50],
        ['rect', [0, 255, 0, 128], 2, 10, 20, 30, 40],
        ['text', [255, 255, 255, 255], 'Hi', 500, 70, 48, '.^'],
    ]


def test_shapes_and_virtual_size(tmp_path):
    report = run('''
        from drawzero import *
        set_virtual_size(500, 500)
        filled_polygon('red', (0, 0), (100, 0), (0, 100))
        arc('red', (100, 100), 200, 100, 0, 90)
        fill('black', alpha=10)
        clear()
    ''', tmp_path)
    ops = all_ops(report)
    assert ops[0] == ['polygon', [255, 0, 0, 255], 0, [0, 0, 200, 0, 0, 200]]
    assert ops[1][:7] == ['arc', [255, 0, 0, 255], 4, 200, 200, 400, 200]
    assert ops[1][7] == 0 and abs(ops[1][8] - 3.14159 / 2) < 1e-3
    assert ops[2] == ['fill', [0, 0, 0, 10]]
    assert ops[3] == ['clear']


def test_tick_paces_frames(tmp_path):
    report = run('''
        from drawzero import *
        for i in range(3):
            clear()
            circle('red', (i, i), 5)
            tick()
        tick(2, fps=60)
        sleep(0.5)
        tick(fps=0)
    ''', tmp_path)
    waits = [f['wait'] for f in report['frames']]
    assert waits[:3] == [pytest.approx(1 / 30)] * 3
    assert waits[3] == pytest.approx(2 / 60)
    assert waits[4] == pytest.approx(0.5)
    assert waits[5] == 0
    assert report['frames'][0]['ops'] == [['clear'], ['circle', [255, 0, 0, 255], 4, 0, 0, 5]]
    assert report['frames'][5]['ops'] == []


def test_long_loop_without_tick_is_flushed(tmp_path):
    report = run('''
        from drawzero import *
        for i in range(10000):
            line('red', (i % 1000, 0), (0, i % 1000))
    ''', tmp_path, frames=100)
    sizes = [len(f['ops']) for f in report['frames']]
    assert sum(sizes) == 10000
    assert max(sizes) <= 4000


def test_stop_ends_an_endless_animation(tmp_path):
    report = run('''
        from drawzero import *
        while True:
            tick()
    ''', tmp_path, frames=3)
    assert report['status'] == 'stopped'
    assert len(report['frames']) == 4


def test_keyboard_and_mouse(tmp_path):
    events = [
        [{'t': 'kd', 'code': 'ArrowLeft', 'key': 'ArrowLeft'}, {'t': 'kd', 'code': 'KeyW', 'key': 'ц'}],
        [{'t': 'kd', 'code': 'KeyW', 'key': 'ц', 'r': True}, {'t': 'md', 'b': 1, 'x': 250, 'y': 750},
         {'t': 'mm', 'x': 260, 'y': 760, 'dx': 10, 'dy': 10, 'bs': [1, 0, 0]}],
        [{'t': 'ku', 'code': 'ArrowLeft', 'key': 'ArrowLeft'}, {'t': 'mu', 'b': 1, 'x': 260, 'y': 760},
         {'t': 'mw', 'dx': 0, 'dy': 1, 'x': 260, 'y': 760}],
        [{'t': 'fl'}],
    ]
    report = run('''
        from drawzero import *
        log = []
        for frame in range(4):
            tick()
            log.append([
                keyboard.pressed('left'), keyboard.just_pressed('w'), keyboard.pressed('w'), keyboard.typed,
                mouse.just_pressed('left'), mouse.pressed('left'), mouse.just_released('left'),
                list(mouse.pos), list(mouse.rel), list(mouse.wheel), keyboard.axis('left', 'right'),
                [e.type.value for e in events()],
            ])
        text('white', repr(log), (0, 0))
    ''', tmp_path, events=events)
    assert report['status'] == 'completed', report['error']
    log = eval(all_ops(report)[-1][2])
    assert log[0][:4] == [True, True, True, 'ц']
    assert log[0][10] == -1
    assert log[1][1:4] == [False, True, 'ц']  # an auto-repeat is held, not pressed again; it types, as in SDL
    assert log[1][4:9] == [True, True, False, [260, 760], [10, 10]]
    assert log[1][11] == ['key_down', 'text_input', 'mouse_down', 'mouse_move']
    assert log[2][0] is False and log[2][6] is True and log[2][9] == [0, 1]
    assert log[3][2] is False  # focus lost releases everything


def test_virtual_size_scales_mouse(tmp_path):
    report = run('''
        from drawzero import *
        set_virtual_size(100, 200)
        tick()
        text('white', repr((tuple(mouse.pos), mouse_pos())), (0, 0))
    ''', tmp_path, events=[[{'t': 'mm', 'x': 500, 'y': 500, 'dx': 0, 'dy': 0, 'bs': [0, 0, 0]}]])
    pos, legacy = eval(all_ops(report)[-1][2])
    assert pos == (50, 100)
    assert legacy == (50, 100)


def test_legacy_input_lists(tmp_path):
    report = run('''
        from drawzero import *
        tick()
        keys = get_keys_pressed()
        text('white', repr((keys[K.SPACE], [e.key for e in keysdown], [e.pos for e in mousebuttonsdown])), (0, 0))
    ''', tmp_path, events=[[{'t': 'kd', 'code': 'Space', 'key': ' '}, {'t': 'md', 'b': 1, 'x': 500, 'y': 250}]])
    assert eval(all_ops(report)[-1][2]) == (True, [32], [(500, 250)])


def test_image_explains_itself(tmp_path):
    report = run('''
        from drawzero import *
        image('cat.png', (0, 0))
    ''', tmp_path)
    assert report['status'] == 'error'
    assert 'not available in the browser' in report['error']


@pytest.mark.parametrize('example', EXAMPLES, ids=lambda p: p.stem)
def test_examples_run(example, tmp_path):
    report = run(example.read_text(encoding='utf-8'), tmp_path, frames=20)
    if example.stem == '12_images':
        assert report['status'] == 'error'
    else:
        assert report['status'] in ('completed', 'stopped'), report['error']
        if example.stem != '99_errors':  # it only prints error messages
            assert all_ops(report), 'drew nothing'
