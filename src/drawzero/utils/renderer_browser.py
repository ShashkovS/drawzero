"""Browser backend: drawing goes to a web page, input comes back from it.

Python runs in a Pyodide web worker; the page draws an SVG. The worker hands
this module one function with ``connect(frame)``:

    frame(ops_json: str, wait: float) -> str | None

``ops_json`` is the list of drawing operations since the previous frame,
``wait`` the seconds this frame should stay on screen before the program goes
on (``tick`` and ``sleep``; 0 for a flush). The call blocks for that long and
returns the input events that arrived meanwhile as a JSON list, or None when
the page has stopped the program.

An operation is a short list: its kind, then its colour as [r, g, b, a] with
the alpha already resolved the way pygame resolves it, then its geometry.

    ['line', c, w, x1, y1, x2, y2]
    ['circle', c, w, x, y, r]
    ['rect', c, w, x, y, width, height]
    ['ellipse', c, w, x, y, width, height]
    ['arc', c, w, x, y, width, height, start, stop]      (radians)
    ['polygon', c, w, [x1, y1, x2, y2, ...]]
    ['text', c, text, x, y, fontsize, align]
    ['fill', c]
    ['clear']

``w`` is the line width in canvas pixels; 0 fills the shape. Coordinates are
canvas pixels of a 1000x1000 surface.

An input event is a dict with ``t``: ``kd``/``ku`` (``code``, ``key``, ``r``
for an auto-repeat), ``md``/``mu`` (``b`` 1..3, ``x``, ``y``), ``mm`` (``x``,
``y``, ``dx``, ``dy``, ``bs``), ``mw`` (``dx``, ``dy``, ``x``, ``y``),
``fg``/``fl`` for focus. Wheel steps follow pygame (up is positive);
``ctrl`` on a key press marks a shortcut, which types no text. Keys are physical (``KeyboardEvent.code``), so WASD
work in any keyboard layout.
"""
import json
from types import SimpleNamespace

from .input import _input, _validate_fps, E
from .key_flags import _pygame_constants
from .screen_size import set_real_size, _input_scale
from .errors import BadDrawParmsError

set_real_size(1000, 1000)

# Flush a long drawing loop that never ticks, so the page shows progress and
# no frame grows without bound.
FLUSH_OPS = 4000

_frame = None
_ops = []
_dft_wid = 4
_pos = (0, 0)


class StopRequested(KeyboardInterrupt):
    """The page stopped the program while it waited for a frame."""


def connect(frame):
    """Install the page's frame function and start a fresh canvas."""
    global _frame
    _frame = frame
    reset()


def reset():
    """Forget the previous run: pending drawing, input state, legacy lists."""
    global _dft_wid, _pos
    _ops.clear()
    _dft_wid = 4
    _pos = (0, 0)
    _input.__init__()
    for lst in (keysdown, keysup, mousemotions, mousebuttonsdown, mousebuttonsup):
        lst.clear()


def _send(wait):
    if _frame is None:
        raise RuntimeError('drawzero: the browser backend is not connected to a page')
    ops = json.dumps(_ops, separators=(',', ':'))
    _ops.clear()
    reply = _frame(ops, float(wait))
    if reply is None:
        raise StopRequested()
    return json.loads(reply) if reply else []


def flush():
    """Send whatever is drawn but not yet shown (the end of a program)."""
    if _ops:
        _send(0)


def _push(op):
    _ops.append(op)
    if len(_ops) >= FLUSH_OPS:
        _send(0)


def _rgba(color, alpha):
    # pygame: an RGBA colour carries its own alpha, and the alpha argument is
    # ignored; an RGB colour takes the alpha argument.
    if len(color) == 4:
        return list(color)
    return [color[0], color[1], color[2], alpha]


def _wid(line_width):
    return line_width if line_width is not None else _dft_wid


def draw_line(color, start, end, alpha=255, line_width=None):
    _push(['line', _rgba(color, alpha), _wid(line_width), start[0], start[1], end[0], end[1]])


def draw_circle(color, pos, radius, alpha=255, line_width=None):
    _push(['circle', _rgba(color, alpha), _wid(line_width), pos[0], pos[1], radius])


def draw_rect(color, rect, alpha=255, line_width=None):
    _push(['rect', _rgba(color, alpha), _wid(line_width), *rect])


def draw_ellipse(color, rect, alpha=255, line_width=None):
    _push(['ellipse', _rgba(color, alpha), _wid(line_width), *rect])


def draw_arc(color, rect, start_angle, stop_angle, alpha=255, line_width=None):
    _push(['arc', _rgba(color, alpha), _wid(line_width), *rect, start_angle, stop_angle])


def draw_polygon(color, points, alpha=255, line_width=None):
    flat = []
    for x, y in points:
        flat.append(x)
        flat.append(y)
    _push(['polygon', _rgba(color, alpha), _wid(line_width), flat])


def draw_text(color, text, pos, fontsize, align):
    # pygame renders text opaque whatever the colour's alpha.
    _push(['text', [color[0], color[1], color[2], 255], text, pos[0], pos[1], fontsize, align])


def draw_fill(color, alpha=255):
    _push(['fill', _rgba(color, alpha)])


def draw_clear():
    _push(['clear'])


def draw_image(path, pos, width=None, alpha=255):
    error = BadDrawParmsError()
    error.errors.append('image() is not available in the browser: there are no image files here.')
    error.call_string = f'image({path!r}, {pos!r})'
    error.example = 'filled_rect(...) or polygon(...) instead'
    error.finish()
    raise error


def draw_set_line_width(w):
    global _dft_wid
    _dft_wid = w


def draw_tick(r=1, *, fps=30):
    _validate_fps(fps)
    _input.begin()
    for lst in (keysdown, keysup, mousemotions, mousebuttonsdown, mousebuttonsup):
        lst.clear()
    wait = r / fps if fps and r > 0 else 0
    for event in _send(wait):
        _ingest(event)
    # The page cannot report what is held when focus returns; keys pressed
    # then arrive as ordinary events.
    _input.needs_reconcile = False
    _input.rescale_position(_input_scale())
    _input.publish()


def draw_sleep(t=1):
    draw_tick(int(t * 30 + 0.5))


def draw_quit():
    flush()
    raise SystemExit


# ---------------------------------------------------------------- input

_K = _pygame_constants
_CODE_KEYS = {
    'Space': _K['K_SPACE'], 'Enter': _K['K_RETURN'], 'Escape': _K['K_ESCAPE'], 'Tab': _K['K_TAB'],
    'Backspace': _K['K_BACKSPACE'], 'Delete': _K['K_DELETE'], 'Insert': _K['K_INSERT'],
    'Home': _K['K_HOME'], 'End': _K['K_END'], 'PageUp': _K['K_PAGEUP'], 'PageDown': _K['K_PAGEDOWN'],
    'ArrowLeft': _K['K_LEFT'], 'ArrowRight': _K['K_RIGHT'], 'ArrowUp': _K['K_UP'], 'ArrowDown': _K['K_DOWN'],
    'ShiftLeft': _K['K_LSHIFT'], 'ShiftRight': _K['K_RSHIFT'],
    'ControlLeft': _K['K_LCTRL'], 'ControlRight': _K['K_RCTRL'],
    'AltLeft': _K['K_LALT'], 'AltRight': _K['K_RALT'],
    'MetaLeft': _K['K_LMETA'], 'MetaRight': _K['K_RMETA'], 'OSLeft': _K['K_LMETA'], 'OSRight': _K['K_RMETA'],
    'CapsLock': _K['K_CAPSLOCK'], 'NumLock': _K['K_NUMLOCK'], 'ScrollLock': _K['K_SCROLLLOCK'],
    'Pause': _K['K_PAUSE'], 'PrintScreen': _K['K_PRINT'], 'ContextMenu': _K['K_MENU'],
    'Minus': _K['K_MINUS'], 'Equal': _K['K_EQUALS'], 'BracketLeft': _K['K_LEFTBRACKET'],
    'BracketRight': _K['K_RIGHTBRACKET'], 'Backslash': _K['K_BACKSLASH'], 'Semicolon': _K['K_SEMICOLON'],
    'Quote': _K['K_QUOTE'], 'Backquote': _K['K_BACKQUOTE'], 'Comma': _K['K_COMMA'],
    'Period': _K['K_PERIOD'], 'Slash': _K['K_SLASH'], 'IntlBackslash': _K['K_BACKSLASH'],
    'NumpadEnter': _K['K_KP_ENTER'], 'NumpadAdd': _K['K_KP_PLUS'], 'NumpadSubtract': _K['K_KP_MINUS'],
    'NumpadMultiply': _K['K_KP_MULTIPLY'], 'NumpadDivide': _K['K_KP_DIVIDE'],
    'NumpadDecimal': _K['K_KP_PERIOD'], 'NumpadEqual': _K['K_KP_EQUALS'],
}
for _c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    _CODE_KEYS['Key' + _c] = ord(_c.lower())
for _d in range(10):
    _CODE_KEYS[f'Digit{_d}'] = ord(str(_d))
    _CODE_KEYS[f'Numpad{_d}'] = _K[f'K_KP_{_d}']
for _f in range(1, 16):
    _CODE_KEYS[f'F{_f}'] = _K[f'K_F{_f}']


def key_code(code):
    """The pygame key for a browser ``KeyboardEvent.code``; 0 if unknown."""
    return _CODE_KEYS.get(code, 0)


def _ingest(ev):
    global _pos
    t = ev.get('t')
    scale = _input_scale()
    if t in ('kd', 'ku'):
        key = key_code(ev.get('code', ''))
        if not key:
            return
        char = ev.get('key', '')
        unicode = char if len(char) == 1 else ''
        down = t == 'kd'
        _input.feed(E.KEY_DOWN if down else E.KEY_UP, {'key': key, 'unicode': unicode, 'repeat': bool(ev.get('r'))})
        if not ev.get('r'):
            legacy = SimpleNamespace(type=t, key=key, unicode=unicode, mod=int(_input._mod))
            (keysdown if down else keysup).append(legacy)
        if down and unicode and not ev.get('ctrl'):
            _input.feed(E.TEXT_INPUT, {'text': unicode})
    elif t in ('md', 'mu'):
        _pos = (ev['x'], ev['y'])
        down = t == 'md'
        _input.feed(E.MOUSE_DOWN if down else E.MOUSE_UP, {'button': ev['b'], 'pos': _pos}, scale)
        (mousebuttonsdown if down else mousebuttonsup).append(SimpleNamespace(type=t, button=ev['b'], pos=_pos))
    elif t == 'mm':
        _pos = (ev['x'], ev['y'])
        rel = (ev.get('dx', 0), ev.get('dy', 0))
        buttons = tuple(ev.get('bs', (0, 0, 0)))
        _input.feed(E.MOUSE_MOVE, {'pos': _pos, 'rel': rel, 'buttons': buttons}, scale)
        mousemotions.append(SimpleNamespace(type=t, pos=_pos, rel=rel, buttons=buttons))
    elif t == 'mw':
        pos = (ev['x'], ev['y']) if 'x' in ev else None
        _input.feed(E.MOUSE_WHEEL, {'precise_x': ev.get('dx', 0), 'precise_y': ev.get('dy', 0), 'pos': pos}, scale)
    elif t == 'fl':
        _input.feed(E.FOCUS_LOST, {})
    elif t == 'fg':
        _input.feed(E.FOCUS_GAINED, {})


# Legacy (pre-0.7) input, kept working for old programs.
keysdown = []
keysup = []
mousemotions = []
mousebuttonsdown = []
mousebuttonsup = []


class _Pressed:
    def __init__(self, held):
        self._held = held

    def __getitem__(self, key):
        return key in self._held

    def __contains__(self, key):
        return key in self._held


def get_keys_pressed():
    return _Pressed(_input.keys)


def keys_mods_pressed():
    return int(_input._mod)


def get_mouse_pressed():
    return tuple(b in _input.buttons for b in (1, 2, 3))


def mouse_pos():
    return _pos
