"""Characterization of the pre-input-API public and renderer contracts."""
import os
import subprocess
import sys


def isolated(code, mode='gui'):
    env = dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy', PYGAME_HIDE_SUPPORT_PROMPT='1')
    env.pop('EJUDGE_MODE', None)
    if mode == 'ejudge':
        env['EJUDGE_MODE'] = '1'
    result = subprocess.run([sys.executable, '-c', code], env=env, text=True,
                          capture_output=True, timeout=30)
    assert result.returncode == 0, result.stderr
    return result


def test_legacy_characterization():
    isolated('''
import atexit
import drawzero as d
from drawzero.utils import renderer as r, draw, screen_size as s
import pygame
atexit.unregister(r._draw_go)
class Clock:
    def __init__(self): self.calls = []
    def tick(self, fps): self.calls.append(fps)
r._fps = Clock()
assert d.K is d.KEY
assert d.K.a == d.K.A == 97 and d.K.MOD_SHIFT == 3
names = ('keysdown', 'keysup', 'mousemotions', 'mousebuttonsdown', 'mousebuttonsup')
for n in names:
    assert n in d.__all__
    assert type(getattr(d, n)) is list
    assert getattr(d, n) is getattr(r, n) is getattr(draw, n)
s.set_virtual_size(1000, 500)
r._create_surface()
s.set_real_size(200, 100)
pygame.event.clear()
e = pygame.event.Event(pygame.MOUSEMOTION, pos=(20, 30), rel=(-2, 3), buttons=(1, 0, 0), custom='saved')
pygame.event.post(e)
assert d.tick(2) is None
assert r._fps.calls == [30, 30]
a = d.mousemotions
assert len(a) == 1 and type(a[0]) is pygame.event.EventType
assert a[0].type == pygame.MOUSEMOTION and a[0].buttons == (1, 0, 0)
assert a[0].pos == (100, 150) and a[0].rel == (-10, 15)
assert a[0].dict['custom'] == 'saved'
a[0].custom = 'changed'
a.append('x'); assert a.pop() == 'x'
a[:] = a.copy(); assert a == a[:]
assert d.tick(0) is None and a == [] and r._fps.calls == [30, 30]
assert d.sleep(0) is None and r._fps.calls == [30, 30]
d.sleep(.05); assert r._fps.calls == [30] * 4
assert len(d.get_mouse_pressed()) == 3 and isinstance(d.keys_mods_pressed(), int)
p = d.get_keys_pressed(); assert not p[d.K.a] and not p['a']
assert p[object()] is False
assert isinstance(d.mouse_pos(), tuple) and isinstance(r.mouse_pos(), tuple)
d.quit()
''')


def test_pygame_frames_and_lifecycle():
    isolated('''
import drawzero as d
from drawzero.utils import renderer as r, input as i, screen_size as s
import pygame
r._create_surface(); pygame.event.clear()
s.set_real_size(100, 100); s.set_virtual_size(1000, 500)
class Clock:
    def __init__(self): self.calls = []
    def tick(self, fps): self.calls.append(fps)
r._fps = Clock()
real_get = pygame.event.get
batches = [
 [pygame.event.Event(pygame.KEYDOWN, key=d.K.a, unicode='a', scancode=4, mod=0),
  pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(5, 6))],
 [pygame.event.Event(pygame.KEYUP, key=d.K.a, scancode=4),
  pygame.event.Event(pygame.TEXTINPUT, text='яλ'),
  pygame.event.Event(pygame.MOUSEMOTION, pos=(8, 9), rel=(3, 3), buttons=(1, 0, 0)),
  pygame.event.Event(pygame.MOUSEWHEEL, x=1, y=2, precise_x=0, precise_y=.5, flipped=True),
  pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=4, pos=(8, 9))]]
pygame.event.get = lambda: batches.pop(0)
d.tick(2, fps=60)
assert r._fps.calls == [60, 60]
assert d.keyboard.just_pressed('a') and d.keyboard.just_released('a') and not d.keyboard.pressed('a')
assert d.keyboard.typed == 'яλ' and d.mouse.wheel == (0, -.5)
assert d.mouse.pos == (80, 45) and d.mouse.rel == (30, 15)
assert len(d.mousebuttonsdown) == 2 and d.mousebuttonsdown[1].button == 4
assert d.mousemotions[0].buttons == (1, 0, 0)
d.mousemotions[0].pos = (999, 999); d.keysdown[0].key = d.K.b
d.mousemotions.clear()
assert d.events()[0].key == d.K.a and d.mouse.events[1].pos == (80, 45)
old = d.events(); assert old is d.events()
assert d.mouse.events[0] is old[1]
# Reads do not poll or create surfaces; legacy helpers remain live snapshots.
pygame.event.get = lambda: (_ for _ in ()).throw(AssertionError('getter polled'))
for n in range(100):
    assert d.keyboard.just_pressed('a') and d.mouse.pos == (80, 45)
    assert d.events() is old
raw1 = {d.K.a: True}; raw2 = {d.K.a: False}
pygame.key.get_pressed = lambda: raw1.copy()
saved = d.get_keys_pressed()
pygame.key.get_pressed = lambda: raw2.copy()
assert saved[d.K.a] and not d.get_keys_pressed()[d.K.a]
assert d.K.a in saved and 'a' in saved and object() not in saved
batches = [[pygame.event.Event(pygame.TEXTINPUT, text='x')], [pygame.event.Event(pygame.TEXTINPUT, text='y')]]
pygame.event.get = lambda: batches.pop(0)
d.sleep(.05); assert d.keyboard.typed == 'xy'
d.tick(0); assert d.events() == () and r._fps.calls == [60, 60, 30, 30]
pygame.event.get = lambda: []
d.tick(fps=0); assert r._fps.calls[-1] == 0
for bad in (-1, float('nan'), float('inf')):
    try: d.tick(fps=bad)
    except ValueError: pass
    else: raise AssertionError(bad)
pygame.event.get = real_get
pygame.event.clear(); pygame.event.post(pygame.event.Event(pygame.QUIT))
try: d.tick(fps=0)
except SystemExit: pass
else: raise AssertionError('quit did not exit')
assert r._closed
r._draw_go()
try: d.clear()
except RuntimeError: pass
else: raise AssertionError('window recreated')
''')


def test_ejudge_neutral():
    result = isolated('''
import sys
from drawzero import *
assert 'pygame' not in sys.modules
assert not keyboard.pressed('a') and keyboard.axis('a', 'b') == 0
assert keyboard.typed == '' and events() == ()
assert mouse.pos == mouse.rel == mouse.wheel == (0, 0)
assert not get_keys_pressed()[K.a] and K.a not in get_keys_pressed()
assert get_mouse_pressed() == (False, False, False)
assert keys_mods_pressed() & K.MOD_SHIFT == 0
assert mouse_pos() == (0, 0)
tick(fps=60); sleep(0); filled_circle('red', (10, 20), 5)
''', mode='ejudge')
    import json
    records = [json.loads(s) for s in result.stdout.splitlines()]
    assert records[0] == {'cmd': 'tick', 'r': 1}
    assert records[1] == {'cmd': 'sleep', 't': 0}
    assert records[2]['figure'] == 'circle'


def test_font_cache():
    isolated('''
import drawzero as d
from drawzero.utils import renderer as r
import pygame
original = pygame.font.Font
calls = []
def font(*args):
    calls.append(args)
    return original(*args)
pygame.font.Font = font
r.draw_text((255,255,255), 'First', (10,10), 20, '<^')
r.draw_text((255,255,255), 'Second', (10,40), 20, '<^')
assert len(calls) == 1 and 20 in r._fonts
d.quit()
''')


def test_adapter_focus_resize_and_hardware_snapshot():
    isolated('''
import drawzero as d
from drawzero.utils import renderer as r, input_pygame as adapter, input as core, screen_size as s
import pygame
r._create_surface(); pygame.event.clear()
s.set_real_size(200,200); s.set_virtual_size(1000,500)
real_resize = r._resize
r._resize = lambda w,h: s.set_real_size(min(w,h), min(w,h))
raw = pygame.key.get_pressed()
class Held:
    def __getitem__(self, key): return key in (d.K.a, d.K.LSHIFT)
pygame.key.get_pressed = lambda: Held()
pygame.mouse.get_pressed = lambda n: (False, False, True)
pygame.mouse.get_pos = lambda: (10,20)
pygame.key.get_mods = lambda: d.K.MOD_LSHIFT
batch = [pygame.event.Event(pygame.WINDOWLEAVE),
         pygame.event.Event(pygame.KEYDOWN, key=d.K.b, scancode=5, mod=0),
         pygame.event.Event(pygame.WINDOWFOCUSLOST),
         pygame.event.Event(pygame.WINDOWFOCUSGAINED),
         pygame.event.Event(pygame.TEXTEDITING, text='α', start=0, length=1),
         pygame.event.Event(pygame.VIDEORESIZE, size=(100,100), w=100,h=100),
         pygame.event.Event(pygame.MOUSEMOTION,pos=(20,30),rel=(1,2),buttons=(0,0,1)),
         pygame.event.Event(pygame.WINDOWRESIZED,x=50,y=50)]
pygame.event.get = lambda: batch
r.draw_tick(wait=False, display_update=False)
assert d.keyboard.just_pressed('b') and not d.keyboard.pressed('b')
assert d.keyboard.pressed('a') and not d.keyboard.just_pressed('a')
assert d.keyboard.pressed('shift') and d.mouse.pressed(3)
assert d.mouse.pos == (200,200)
assert d.mouse.events[0].pos == (200,150)
assert d.events()[-1].size == (50,50)
assert len(d.events()) == 7
core._input.begin()
adapter.ingest(pygame.event.Event(pygame.ACTIVEEVENT, gain=0, state=1))
assert core._input._focused
adapter.ingest(pygame.event.Event(pygame.ACTIVEEVENT, gain=0, state=2))
assert not core._input._focused
adapter.ingest(pygame.event.Event(pygame.ACTIVEEVENT, gain=1, state=2))
adapter.reconcile_focus(); core._input.publish()
assert d.keyboard.pressed('a')
r._resize = real_resize
d.quit()
''')


def test_static_lifetime_and_resize_history():
    result = isolated('''
import drawzero as d
from drawzero.utils import renderer as r, screen_size as s
import pygame
d.clear()
pygame.event.clear()
s.set_real_size(200,200); s.set_virtual_size(1000,500)
pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(20,30)))
pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(30,40)))
pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE,size=(100,100),w=100,h=100))
d.tick(fps=0)
assert d.mousebuttonsdown[0].pos == (200,150)
assert d.mousebuttonsup[0].pos == (300,200)
assert d.mouse.events[0].pos == (100,75)
assert d.mouse.pos == (300,200)
# The static atexit lifetime loop must close normally and silently.
pygame.event.post(pygame.event.Event(pygame.QUIT))
''')
    assert result.stderr == '' and result.stdout == ''


def test_no_window_from_new_getters():
    isolated('''
import drawzero as d
from drawzero.utils import renderer as r
assert r._surface is None
assert not d.keyboard.pressed('a') and not d.mouse.pressed('left')
assert d.events() == () and d.mouse.pos == (0,0)
assert r._surface is None
d.quit()
''')


def test_backend_failure_shutdown():
    # Each error path must leave stderr usable and stop the lifetime loop.
    for failure in ('clock', 'queue', 'display', 'static'):
        isolated('''
import sys
import drawzero as d
from drawzero.utils import renderer as r
import pygame
r._create_surface()
def fail(*args):
    raise pygame.error('test shutdown')
def interrupt(*args):
    raise KeyboardInterrupt()
mode = %r
if mode == 'clock':
    class Clock:
        tick = staticmethod(interrupt)
    r._fps = Clock()
elif mode == 'queue': pygame.event.get = fail
else: pygame.display.update = fail
try:
    if mode == 'static': r._display_update_if_no_animation()
    else: r.draw_tick(fps=0)
except SystemExit: pass
else: raise AssertionError('missing exit')
assert r._closed and sys.stderr is not None
r._draw_go()
''' % failure)
