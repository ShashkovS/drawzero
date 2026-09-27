import random
import pytest
from drawzero import K, KEY, set_lang
from drawzero.utils.input import _Input, E, M, MOD, _key_name, _validate_fps
from drawzero.utils import screen_size as sizes


@pytest.fixture
def m():
    return _Input()


def frame(m, *records):
    m.begin()
    for kind, data in records:
        m.feed(kind, data)
    m.publish()


def kd(key=K.a, **kw):
    return E.KEY_DOWN, dict(key=key, **kw)


def ku(key=K.a, **kw):
    return E.KEY_UP, dict(key=key, **kw)


def test_neutral(m):
    assert not m.keyboard.pressed('a') and m.keyboard.axis('left', 'right') == 0
    assert not m.mouse.pressed('left')
    assert m.mouse.pos == m.mouse.rel == m.mouse.wheel == (0, 0)
    assert m.events() == m.keyboard.events == m.mouse.events == ()
    assert m.keyboard.typed == ''
    assert K is KEY and K.A == K.a and K.MOD_CTRL == 192
    assert 'K.LEFT' in str(K)


@pytest.mark.parametrize('key', [K.a, 'a', 'A'])
def test_arguments(m, key):
    frame(m, kd())
    assert m.keyboard.pressed(key, 'b')
    assert m.keyboard.just_pressed(key)
    assert not m.keyboard.just_released(key)
    for alias, canonical in [('enter', 'return'), ('esc', 'escape'), ('cmd', 'meta')]:
        assert _key_name(alias) == _key_name(canonical)
    assert m.keyboard.axis(('b', 'b'), ['A', 'a']) == 1
    assert m.keyboard.axis('a', 'a') == 0
    assert m.keyboard.axis(['a'], 'b') == -1
    for bad in [True, False, -9, 9.2, None, {}, [], 'ф', 'nonsense', MOD.CTRL]:
        with pytest.raises((ValueError, TypeError)):
            m.keyboard.pressed('a', bad)
        with pytest.raises((ValueError, TypeError)):
            m.mouse.pressed('left', bad)
    for bad in [(), [], [('a',)], [['a']], ['a', 'tyop']]:
        with pytest.raises(ValueError):
            m.keyboard.axis(bad, 'a')
        with pytest.raises(ValueError):
            m.keyboard.axis('a', bad)
    for method in (m.keyboard.pressed, m.keyboard.just_pressed, m.keyboard.just_released,
                   m.mouse.pressed, m.mouse.just_pressed, m.mouse.just_released):
        with pytest.raises(TypeError):
            method()
    for lang, text in [('en', 'Did you mean'), ('ru', 'Возможно')]:
        set_lang(lang)
        with pytest.raises(ValueError, match=text):
            m.keyboard.pressed('spaec')
    set_lang('en')
    assert _key_name.cache_info().maxsize == 256


def test_transitions(m):
    frame(m, kd(), ku(), kd(), ku())
    assert not m.keyboard.pressed('a')
    assert m.keyboard.just_pressed('a') and m.keyboard.just_released('a')
    assert len(m.events()) == 4
    frame(m, kd())
    assert m.keyboard.pressed('a')
    frame(m, kd(unicode='A'))
    assert not m.keyboard.just_pressed('a') and m.events()[0].repeat
    frame(m, ku(), kd())
    assert m.keyboard.just_pressed('a') and m.keyboard.just_released('a')
    frame(m)
    assert m.keyboard.pressed('a') and not m.keyboard.just_pressed('a')
    frame(m, ku())
    assert m.keyboard.just_released('a')
    frame(m, kd(repeat=True))
    assert not m.keyboard.just_pressed('a') and m.keyboard.pressed('a')
    # Getters cannot see the work-in-progress frame.
    m.begin(); m.feed(E.KEY_UP, {'key': K.a})
    assert m.keyboard.pressed('a')
    m.publish(); assert not m.keyboard.pressed('a')


@pytest.mark.parametrize('group,left,right', [('shift', K.LSHIFT, K.RSHIFT), ('ctrl', K.LCTRL, K.RCTRL),
                                             ('alt', K.LALT, K.RALT), ('meta', K.LMETA, K.RMETA)])
def test_groups(m, group, left, right):
    frame(m, kd(left)); assert m.keyboard.just_pressed(group)
    frame(m, kd(right)); assert not m.keyboard.just_pressed(group)
    frame(m, ku(left)); assert m.keyboard.just_released(left, right)
    assert not m.keyboard.just_released(group) and m.keyboard.pressed(group)
    frame(m, ku(right), kd(left))
    assert m.keyboard.just_released(group) and m.keyboard.just_pressed(group)
    frame(m, ku(left)); assert not m.keyboard.pressed(group)
    assert m.keyboard.just_released(group)


def test_physical(m):
    frame(m, kd(K.a, scancode=4), kd(K.a, scancode=5))
    frame(m, ku(K.b, scancode=4))
    assert m.keyboard.pressed('a') and not m.keyboard.just_released('a')
    frame(m, ku(K.c, scancode=5))
    assert not m.keyboard.pressed('a') and m.keyboard.just_released('a')
    assert m.events()[0].key == K.c
    frame(m, kd(K.a, scancode=4), kd(K.b, scancode=4))
    assert m.keyboard.pressed('a') and not m.keyboard.pressed('b')
    assert m.events()[1].repeat


def test_stream_text_lifetime(m):
    frame(m, kd(unicode='я'), (E.TEXT_INPUT, {'text': 'я'}),
          (E.TEXT_EDITING, {'text': 'αβ', 'start': 1, 'length': 2}),
          kd(K.BACKSPACE), (E.MOUSE_DOWN, {'button': 1, 'pos': [10, 20]}),
          (E.TEXT_INPUT, {'text': 'λ'}), (E.WINDOW_RESIZED, {'size': [800, 600]}))
    saved = m.events()
    assert saved is m.events()
    assert m.keyboard.events is m.keyboard.events and m.mouse.events is m.mouse.events
    assert m.keyboard.events[0] is saved[0] and m.mouse.events[0] is saved[4]
    assert m.keyboard.typed == 'яλ'
    cached_text = m.keyboard.typed
    assert m.keyboard.typed is cached_text
    assert saved[2].text == 'αβ' and saved[2].start == 1 and saved[2].length == 2
    assert saved[0].scancode is None and saved[0].unicode == 'я'
    assert 'KeyEvent' in repr(saved[0]) and saved[6].size == (800, 600)
    with pytest.raises(AttributeError):
        saved[4].pos = (0, 0)
    with pytest.raises(TypeError):
        saved[4].pos[0] = 99
    value = ''
    for event in saved:
        if event.type == E.TEXT_INPUT: value += event.text
        elif event.type == E.KEY_DOWN and event.key == K.BACKSPACE: value = value[:-1]
    assert value == 'λ'
    for _ in range(100): frame(m)
    assert saved[4].pos == (10, 20) and m.keyboard.typed == ''


def test_mouse(m):
    m.begin()
    m.feed(E.KEY_DOWN, {'key': K.LCTRL})
    for button in (1, 2, 3): m.feed(E.MOUSE_DOWN, {'button': button, 'pos': (1, 2)})
    m.feed(E.MOUSE_MOVE, {'pos': (-1, 2), 'rel': (-2, .5), 'buttons': (True, False, True)}, (2.5, 5))
    m.feed(E.KEY_UP, {'key': K.LCTRL})
    m.feed(E.MOUSE_UP, {'button': 1, 'pos': (7, 8)})
    m.publish()
    assert m.mouse.pressed('MIDDLE', M.RIGHT) and not m.mouse.pressed(M.LEFT)
    assert m.mouse.just_pressed('LEFT') and m.mouse.just_released(1)
    motion = m.mouse.events[3]
    assert motion.pos == (-2.5, 10) and motion.rel == (-5, 2.5)
    assert motion.buttons == frozenset((1, 3)) and M.LEFT in motion.buttons
    assert motion.mod & MOD.CTRL and not m.mouse.events[4].mod & MOD.CTRL
    assert m.mouse.pos == (7, 8) and m.mouse.rel == (-5, 2.5)
    for _ in range(10): assert m.mouse.rel == (-5, 2.5)
    frame(m, (E.MOUSE_UP, {'button': 2, 'pos': (0, 0)}), (E.MOUSE_DOWN, {'button': 2, 'pos': (0, 0)}))
    assert m.mouse.just_pressed(2) and m.mouse.just_released(2)


def test_geometry_and_copy(m):
    data = {'pos': [3, 4], 'rel': [-1, 2], 'buttons': [1, 0, 0]}
    m.begin(); m.feed(E.MOUSE_MOVE, data, (2, 4))
    m.feed(E.WINDOW_RESIZED, {'size': (100, 200)})
    m.feed(E.MOUSE_MOVE, data, (3, 5)); m.publish()
    data['pos'][0] = 999; data['buttons'][0] = 0
    saved = m.events()
    assert saved[0].pos == (6, 16) and saved[2].pos == (9, 20)
    assert m.mouse.rel == (-5, 18)
    frame(m, (E.MOUSE_MOVE, {'pos': (0, 0), 'rel': (2, -2)}),
          (E.MOUSE_MOVE, {'pos': (0, 0), 'rel': (-2, 2)}))
    assert m.mouse.rel == (0, 0)
    sizes.set_real_size(0, -1); assert sizes._input_scale() == (1, 1)
    sizes.set_real_size(200, 100); sizes.set_virtual_size(1000, 300)
    assert sizes._input_scale() == (5, 3)
    assert sizes._input_scale() is sizes._input_scale()
    sizes.set_real_size(1000, 1000); sizes.set_virtual_size(1000, 1000)


def test_wheel(m):
    frame(m, (E.MOUSE_WHEEL, {'x': 8, 'y': 8, 'precise_x': 0, 'precise_y': .25}),
          (E.MOUSE_WHEEL, {'x': 2, 'y': -3, 'flipped': True, 'pos': (1, 2)}),
          (E.MOUSE_DOWN, {'button': 4, 'pos': (0, 0)}),
          (E.MOUSE_UP, {'button': 5, 'pos': (0, 0)}))
    assert m.mouse.wheel == (-2, 3.25)
    assert len(m.events()) == 2 and m.events()[0].pos is None
    assert m.events()[1].pos == (1, 2)
    for button in (4, 5, 6):
        with pytest.raises(ValueError): m.mouse.pressed(button)


def test_focus_and_authority(m):
    frame(m, kd(), (E.MOUSE_DOWN, {'button': 1, 'pos': (2, 3)}),
          (E.MOUSE_MOVE, {'pos': (3, 4), 'rel': (1, 1)}), (E.FOCUS_LOST, {}))
    assert not m.keyboard.pressed('a') and not m.mouse.pressed(1)
    assert not m.keyboard.just_released('a') and not m.mouse.just_released(1)
    assert m.keyboard.just_pressed('a') and m.mouse.rel == (0, 0)
    m.begin(); m.feed(E.FOCUS_GAINED, {}); m.feed(E.KEY_DOWN, {'key': K.b})
    assert m.needs_reconcile
    m.reconcile([K.a, K.LSHIFT], [3, 5], (7, 8), MOD.SHIFT); m.publish()
    assert m.keyboard.pressed('shift', 'a') and not m.keyboard.just_pressed('a')
    assert m.keyboard.just_pressed('b') and not m.keyboard.pressed('b')
    assert m.mouse.pos == (7, 8) and m.mouse.pressed(3)
    frame(m, ku(K.LSHIFT, cancelled=True), (E.MOUSE_UP, {'button': 3, 'pos': (0, 0), 'cancelled': True}))
    assert not m.keyboard.just_released('shift') and not m.mouse.just_released(3)
    assert not m.keyboard.pressed('shift') and m.events()[0].source.cancelled


def test_native_mod_and_repeat_unknown(m):
    frame(m, kd(mod=int(MOD.CAPS), repeat=True))
    assert m.events()[0].mod == MOD.CAPS
    assert not m.keyboard.just_pressed('a')
    frame(m, ku()); assert m.keyboard.just_released('a')
    frame(m, (E.FOCUS_LOST, {}), kd(K.b), (E.MOUSE_DOWN, {'button': 1, 'pos': (0, 0)}))
    assert not m.keyboard.pressed('b') and not m.mouse.pressed(1)
    frame(m, ('unsupported', {})); assert m.events() == ()


def test_fps():
    for value in (-1, float('nan'), float('inf'), '30', True, None):
        with pytest.raises(ValueError): _validate_fps(value)
    for value in (0, 30, 60, 120, 29.97): _validate_fps(value)


def test_no_wrappers_and_cached_reads(m, monkeypatch):
    import drawzero.utils.input as module
    original = module.KeyEvent
    calls = []
    def constructor(*args):
        calls.append(args)
        return original(*args)
    monkeypatch.setattr(module, 'KeyEvent', constructor)
    for _ in range(50):
        frame(m, kd(), ku())
        for __ in range(10):
            m.keyboard.pressed(K.a); m.keyboard.just_pressed('a'); m.keyboard.axis('a', 'b')
        assert not calls
    first = m.events(); assert len(calls) == 2
    for _ in range(50): assert m.events() is first
    assert len(calls) == 2 and len(m._raw) == 2


def test_seeded_reference(m):
    rng = random.Random(5701)
    held = set()
    buttons = set()
    for _ in range(250):
        down, up, bd, bu = set(), set(), set(), set()
        text = ''; wheel = [0, 0]; expected = []
        m.begin()
        for __ in range(rng.randrange(25)):
            action = rng.randrange(8)
            key = rng.choice([K.a, K.b, K.c])
            if action < 2:
                kind = E.KEY_DOWN if action == 0 else E.KEY_UP
                if action == 0:
                    if key not in held: down.add(key)
                    held.add(key)
                else:
                    if key in held: up.add(key)
                    held.discard(key)
                data = {'key': key}
            elif action < 4:
                button = rng.randrange(1, 4)
                kind = E.MOUSE_DOWN if action == 2 else E.MOUSE_UP
                if action == 2:
                    if button not in buttons: bd.add(button)
                    buttons.add(button)
                else:
                    if button in buttons: bu.add(button)
                    buttons.discard(button)
                data = {'button': button, 'pos': (rng.randrange(-10, 10), 20)}
            elif action == 4:
                kind, data = E.TEXT_INPUT, {'text': rng.choice(['a', 'я', 'λ'])}
                text += data['text']
            elif action == 5:
                kind, data = E.MOUSE_WHEEL, {'x': .5, 'y': -1}
                wheel[0] += .5; wheel[1] -= 1
            elif action == 6:
                kind, data = E.WINDOW_RESIZED, {'size': (200, 400)}
            else:
                kind, data = E.FOCUS_LOST, {}
                held.clear(); buttons.clear()
            m.feed(kind, data)
            expected.append(kind)
            if action == 7:
                m.feed(E.FOCUS_GAINED, {})
                expected.append(E.FOCUS_GAINED)
        m.publish()
        assert m.keys == held and m.buttons == buttons
        assert (m.key_down, m.key_up, m.button_down, m.button_up) == (down, up, bd, bu)
        assert m.keyboard.typed == text and m.mouse.wheel == tuple(wheel)
        assert [e.type for e in m.events()] == expected


def test_provenance_and_final_scale(m):
    class Window:
        id = 42
    m.begin()
    m.feed(E.MOUSE_MOVE, {'pos': (5, 6), 'rel': (1, 1), 'window': Window(), 'which': 3, 'touch': True})
    m.rescale_position((2, 3)); m.publish()
    assert m.mouse.pos == (10, 18) and m.mouse.events[0].pos == (5, 6)
    source = m.events()[0].source
    assert (source.window, source.which, source.touch) == (42, 3, True)
    frame(m, kd(K.LSHIFT, repeat=True))
    assert m.keyboard.pressed('shift') and not m.keyboard.just_pressed('shift')
    frame(m, kd(K.RSHIFT))
    frame(m, ku(K.LSHIFT, cancelled=True))
    assert m.keyboard.pressed('shift') and not m.keyboard.just_released('shift')


def test_seeded_motion_reference(m):
    rng = random.Random(12981)
    retained = []
    for _ in range(100):
        m.begin(); expected = []; dx = dy = 0; sx = sy = 1
        pos = m.mouse.pos
        for __ in range(30):
            if rng.randrange(4) == 0:
                sx, sy = rng.choice((.5, 2, 3)), rng.choice((.25, 1, 4))
                m.feed(E.WINDOW_RESIZED, {'size': (100, 200)})
            else:
                x, y, rx, ry = [rng.uniform(-50, 50) for ___ in range(4)]
                buttons = tuple(rng.choice((0, 1)) for ___ in range(3))
                m.feed(E.MOUSE_MOVE, {'pos': (x, y), 'rel': (rx, ry), 'buttons': buttons}, (sx, sy))
                pos = (x*sx, y*sy); rel = (rx*sx, ry*sy)
                dx += rel[0]; dy += rel[1]
                expected.append((pos, rel, frozenset(i+1 for i,b in enumerate(buttons) if b)))
        m.publish()
        actual = [(e.pos, e.rel, e.buttons) for e in m.mouse.events]
        assert actual == expected and m.mouse.rel == (dx, dy) and m.mouse.pos == pos
        retained.append((m.mouse.events, expected))
    for saved, expected in retained:
        assert [(e.pos, e.rel, e.buttons) for e in saved] == expected


def test_all_event_constructors_are_lazy(m, monkeypatch):
    import drawzero.utils.input as module
    names = ('KeyEvent', 'TextEvent', 'EditingEvent', 'ButtonEvent', 'MotionEvent',
             'WheelEvent', 'FocusEvent', 'ResizeEvent', 'Provenance')
    counts = dict.fromkeys(names, 0)
    for name in names:
        original = getattr(module, name)
        def counted(*args, _original=original, _name=name):
            counts[_name] += 1
            return _original(*args)
        monkeypatch.setattr(module, name, counted)
    trace = [kd(), ku(), (E.TEXT_INPUT, {'text': 'a'}), (E.TEXT_EDITING, {'text': 'x'}),
             (E.MOUSE_DOWN, {'button': 1, 'pos': (0, 0)}),
             (E.MOUSE_MOVE, {'pos': (1, 2), 'rel': (1, 2), 'buttons': (1, 0, 0)}),
             (E.MOUSE_UP, {'button': 1, 'pos': (1, 2)}), (E.MOUSE_WHEEL, {'y': 1}),
             (E.FOCUS_LOST, {}), (E.FOCUS_GAINED, {}), (E.WINDOW_RESIZED, {'size': (50, 50)})]
    for _ in range(50):
        frame(m, *trace)
        m.keyboard.pressed('a'); m.mouse.pressed(1); m.keyboard.axis('left', 'right')
    assert not any(counts.values())
    first = m.events()
    assert sum(counts.values()) == 2 * len(trace)
    for _ in range(50): assert m.events() is first
    assert sum(counts.values()) == 2 * len(trace)
