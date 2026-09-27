"""Frame input reducer. No GUI imports; raw records own all lazy-event data."""
from enum import IntFlag, Enum
from functools import lru_cache
from difflib import get_close_matches
from math import isfinite
from typing import NamedTuple, Tuple, Optional, FrozenSet, Union

from .key_flags import K, _pygame_constants
from .i18n import I18N


class M:
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3


class MOD(IntFlag):
    NONE = 0
    LSHIFT = K.MOD_LSHIFT
    RSHIFT = K.MOD_RSHIFT
    SHIFT = K.MOD_SHIFT
    LCTRL = K.MOD_LCTRL
    RCTRL = K.MOD_RCTRL
    CTRL = K.MOD_CTRL
    LALT = K.MOD_LALT
    RALT = K.MOD_RALT
    ALT = K.MOD_ALT
    LMETA = LGUI = K.MOD_LGUI
    RMETA = RGUI = K.MOD_RGUI
    META = GUI = K.MOD_GUI
    NUM = K.MOD_NUM
    CAPS = K.MOD_CAPS
    MODE = K.MOD_MODE


class E(Enum):
    KEY_DOWN = 'key_down'
    KEY_UP = 'key_up'
    TEXT_INPUT = 'text_input'
    TEXT_EDITING = 'text_editing'
    MOUSE_DOWN = 'mouse_down'
    MOUSE_UP = 'mouse_up'
    MOUSE_MOVE = 'mouse_move'
    MOUSE_WHEEL = 'mouse_wheel'
    FOCUS_LOST = 'focus_lost'
    FOCUS_GAINED = 'focus_gained'
    WINDOW_RESIZED = 'window_resized'


Position = Tuple[float, float]


class Provenance(NamedTuple):
    window: Optional[int] = None
    which: Optional[int] = None
    touch: Optional[bool] = None
    cancelled: bool = False


class KeyEvent(NamedTuple):
    type: E
    key: int
    mod: MOD
    scancode: Optional[int]
    unicode: str
    repeat: bool
    source: Provenance


class TextEvent(NamedTuple):
    type: E
    text: str
    source: Provenance


class EditingEvent(NamedTuple):
    type: E
    text: str
    start: int
    length: int
    source: Provenance


class ButtonEvent(NamedTuple):
    type: E
    button: int
    pos: Position
    mod: MOD
    source: Provenance


class MotionEvent(NamedTuple):
    type: E
    pos: Position
    rel: Position
    buttons: FrozenSet[int]
    mod: MOD
    source: Provenance


class WheelEvent(NamedTuple):
    type: E
    x: float
    y: float
    pos: Optional[Position]
    source: Provenance


class FocusEvent(NamedTuple):
    type: E
    source: Provenance


class ResizeEvent(NamedTuple):
    type: E
    size: Tuple[int, int]
    source: Provenance


InputEvent = Union[KeyEvent, TextEvent, EditingEvent, ButtonEvent, MotionEvent,
                   WheelEvent, FocusEvent, ResizeEvent]
_GROUPS = {'shift': (K.LSHIFT, K.RSHIFT), 'ctrl': (K.LCTRL, K.RCTRL),
           'alt': (K.LALT, K.RALT), 'meta': (K.LMETA, K.RMETA)}
_KEY_NAMES = {n[2:].lower(): v for n, v in _pygame_constants.items() if n.startswith('K_')}
_KEY_NAMES.update(enter=K.RETURN, esc=K.ESCAPE, cmd='meta')
_KEY_NAMES.update({n: n for n in _GROUPS})
_CODES = frozenset(v for n, v in _pygame_constants.items() if n.startswith('K_'))
_MOUSE_NAMES = {'left': 1, 'middle': 2, 'right': 3}
_MOD_KEYS = {K.LSHIFT: MOD.LSHIFT, K.RSHIFT: MOD.RSHIFT, K.LCTRL: MOD.LCTRL,
             K.RCTRL: MOD.RCTRL, K.LALT: MOD.LALT, K.RALT: MOD.RALT,
             K.LMETA: MOD.LMETA, K.RMETA: MOD.RMETA}
_GROUP_FOR = {k: n for n, pair in _GROUPS.items() for k in pair}
_BUTTON_SETS = tuple(frozenset(i + 1 for i in range(3) if mask & (1 << i)) for mask in range(8))
_ZERO = (0.0, 0.0)


def _invalid(value, names):
    hint = ''
    if isinstance(value, str):
        matches = get_close_matches(value.lower(), names, n=1)
        if matches:
            hint = I18N.input_suggestion.format(matches[0])
    raise ValueError(I18N.input_invalid.format(value) + hint)


@lru_cache(maxsize=256)
def _key_name(name):
    try:
        return _KEY_NAMES[name.lower()]
    except KeyError:
        _invalid(name, _KEY_NAMES)


def _key(value):
    if isinstance(value, MOD):
        raise TypeError(I18N.input_mask)
    if type(value) is int and value in _CODES:
        return value
    if isinstance(value, str):
        return _key_name(value)
    _invalid(value, _KEY_NAMES)


def _button(value):
    if type(value) is int and 1 <= value <= 3:
        return value
    if isinstance(value, str):
        result = _MOUSE_NAMES.get(value.lower())
        if result is not None:
            return result
    _invalid(value, _MOUSE_NAMES)


def _query(state, resolve, first, rest):
    result = resolve(first) in state
    for arg in rest:
        if resolve(arg) in state:
            result = True
    return result


def _side(state, value):
    if isinstance(value, (tuple, list)):
        if not value:
            raise ValueError(I18N.input_group)
        result = False
        for arg in value:
            if _key(arg) in state:
                result = True
        return result
    return _key(value) in state


def _validate_fps(fps):
    if isinstance(fps, bool) or not isinstance(fps, (int, float)) or not isfinite(fps) or fps < 0:
        raise ValueError(I18N.input_fps)


class Keyboard:
    __slots__ = ('_manager',)

    def __init__(self, manager):
        self._manager = manager

    def pressed(self, key, *other_keys) -> bool:
        return _query(self._manager.keys, _key, key, other_keys)

    def just_pressed(self, key, *other_keys) -> bool:
        return _query(self._manager.key_down, _key, key, other_keys)

    def just_released(self, key, *other_keys) -> bool:
        return _query(self._manager.key_up, _key, key, other_keys)

    def axis(self, negative, positive) -> int:
        state = self._manager.keys
        neg = _side(state, negative)
        pos = _side(state, positive)
        return int(pos) - int(neg)

    @property
    def typed(self) -> str:
        m = self._manager
        if m._typed is None:
            m._typed = ''.join(m._text)
        return m._typed

    @property
    def events(self) -> Tuple[InputEvent, ...]:
        return self._manager.device_events(True)


class Mouse:
    __slots__ = ('_manager',)

    def __init__(self, manager):
        self._manager = manager

    def pressed(self, button, *other_buttons) -> bool:
        return _query(self._manager.buttons, _button, button, other_buttons)

    def just_pressed(self, button, *other_buttons) -> bool:
        return _query(self._manager.button_down, _button, button, other_buttons)

    def just_released(self, button, *other_buttons) -> bool:
        return _query(self._manager.button_up, _button, button, other_buttons)

    @property
    def pos(self) -> Position:
        return self._manager.pos

    @property
    def rel(self) -> Position:
        return self._manager.rel

    @property
    def wheel(self) -> Position:
        return self._manager.wheel

    @property
    def events(self) -> Tuple[InputEvent, ...]:
        return self._manager.device_events(False)


class _Input:
    """Private injection seam: begin(), feed(E, payload, scale), publish().

    Optional reconcile() consumes authoritative logical keys/buttons after a
    focus-gain batch. It updates final state without changing historical edges.
    """
    def __init__(self):
        self._keys = set()
        self._buttons = set()
        self._physical = {}
        self._counts = {}
        self._mod = MOD.NONE
        self._pos = _ZERO
        self._native_pos = None
        self._focused = True
        self.keyboard = Keyboard(self)
        self.mouse = Mouse(self)
        self.begin()
        self.publish()

    def begin(self):
        self._kd = set()
        self._ku = set()
        self._bd = set()
        self._bu = set()
        self._records = []
        self._texts = []
        self._rel = _ZERO
        self._wheel = _ZERO
        self.needs_reconcile = False

    def _edge(self, key, down, repeat=False):
        group = _GROUP_FOR.get(key)
        before = group in self._keys if group else False
        if down:
            if key not in self._keys and not repeat:
                self._kd.add(key)
            self._keys.add(key)
        else:
            if key in self._keys:
                self._ku.add(key)
            self._keys.discard(key)
        if group:
            after = any(k in self._keys for k in _GROUPS[group])
            if after:
                self._keys.add(group)
            else:
                self._keys.discard(group)
            if before != after:
                if after and not repeat:
                    self._kd.add(group)
                elif not after:
                    self._ku.add(group)

    def reconcile(self, keys=(), buttons=(), pos=None, mod=0):
        self._keys = set(keys)
        for group, pair in _GROUPS.items():
            if any(k in self._keys for k in pair):
                self._keys.add(group)
        self._buttons = set(buttons).intersection((1, 2, 3))
        self._physical.clear()
        self._counts.clear()
        self._mod = MOD(mod)
        if pos is not None:
            self._pos = tuple(pos)
            self._native_pos = None
        self.needs_reconcile = False

    def feed(self, kind, data, scale=(1.0, 1.0)):
        # Only immutable primitive fields enter records; no backend dictionaries escape.
        sx, sy = scale
        window = data.get('window')
        if window is not None and not isinstance(window, int):
            window = getattr(window, 'id', None)
        source = (window, data.get('which'), data.get('touch'), bool(data.get('cancelled', False)))
        def point(p):
            return (p[0] * sx, p[1] * sy)
        if kind in (E.KEY_DOWN, E.KEY_UP):
            key = data.get('key', 0)
            scan = data.get('scancode')
            repeat = bool(data.get('repeat', False))
            down = kind == E.KEY_DOWN
            identity = ('scan', scan) if scan is not None and scan > 0 else ('key', key)
            if down:
                repeat = repeat or identity in self._physical
                if identity not in self._physical:
                    self._physical[identity] = key
                    self._counts[key] = self._counts.get(key, 0) + 1
                logical = self._physical[identity]
                if self._focused and not source[3]:
                    self._edge(logical, True, repeat)
            else:
                logical = self._physical.pop(identity, key)
                count = self._counts.get(logical, 1) - 1
                if count > 0:
                    self._counts[logical] = count
                else:
                    self._counts.pop(logical, None)
                    if not source[3]:
                        self._edge(logical, False)
                    else:
                        self._keys.discard(logical)
                        group = _GROUP_FOR.get(logical)
                        if group and not any(k in self._keys for k in _GROUPS[group]):
                            self._keys.discard(group)
            if 'mod' in data:
                self._mod = MOD(data['mod'])
            flag = _MOD_KEYS.get(logical)
            if flag and 'mod' not in data:
                if logical in self._keys:
                    self._mod |= flag
                else:
                    self._mod &= ~flag
            payload = (kind, key, self._mod, scan, data.get('unicode', ''), repeat if down else False, source)
            cls = KeyEvent
        elif kind == E.TEXT_INPUT:
            value = data.get('text', '')
            self._texts.append(value)
            cls, payload = TextEvent, (kind, value, source)
        elif kind == E.TEXT_EDITING:
            cls, payload = EditingEvent, (kind, data.get('text', ''), data.get('start', 0), data.get('length', 0), source)
        elif kind in (E.MOUSE_DOWN, E.MOUSE_UP):
            button = data['button']
            if button not in (1, 2, 3):
                return
            self._native_pos = tuple(data['pos'])
            self._pos = point(self._native_pos)
            if kind == E.MOUSE_DOWN:
                if self._focused and not source[3]:
                    if button not in self._buttons:
                        self._bd.add(button)
                    self._buttons.add(button)
            else:
                if button in self._buttons and not source[3]:
                    self._bu.add(button)
                self._buttons.discard(button)
            cls, payload = ButtonEvent, (kind, button, self._pos, MOD(data.get('mod', self._mod)), source)
        elif kind == E.MOUSE_MOVE:
            self._native_pos = tuple(data['pos'])
            self._pos = point(self._native_pos)
            rel = point(data.get('rel', _ZERO))
            self._rel = (self._rel[0] + rel[0], self._rel[1] + rel[1])
            mask = 0
            for i, value in enumerate(data.get('buttons', ())[:3]):
                if value:
                    mask |= 1 << i
            buttons = _BUTTON_SETS[mask]
            cls, payload = MotionEvent, (kind, self._pos, rel, buttons, MOD(data.get('mod', self._mod)), source)
        elif kind == E.MOUSE_WHEEL:
            sign = -1 if data.get('flipped', False) else 1
            x = float(data.get('precise_x', data.get('x', 0))) * sign
            y = float(data.get('precise_y', data.get('y', 0))) * sign
            self._wheel = (self._wheel[0] + x, self._wheel[1] + y)
            pos = data.get('pos')
            cls, payload = WheelEvent, (kind, x, y, point(pos) if pos is not None else None, source)
        elif kind in (E.FOCUS_LOST, E.FOCUS_GAINED):
            self._focused = kind == E.FOCUS_GAINED
            if not self._focused:
                self.reconcile()
                self._rel = _ZERO
            else:
                self.needs_reconcile = True
            cls, payload = FocusEvent, (kind, source)
        elif kind == E.WINDOW_RESIZED:
            cls, payload = ResizeEvent, (kind, tuple(data['size']), source)
        else:
            return
        self._records.append((cls, payload))

    def rescale_position(self, scale):
        if self._native_pos is not None:
            self._pos = (self._native_pos[0] * scale[0], self._native_pos[1] * scale[1])

    def publish(self):
        self.keys = self._keys.copy()
        self.buttons = self._buttons.copy()
        self.key_down, self.key_up = self._kd, self._ku
        self.button_down, self.button_up = self._bd, self._bu
        self.pos, self.rel, self.wheel = self._pos, self._rel, self._wheel
        self._raw, self._text = self._records, self._texts
        self._events = self._keyboard_events = self._mouse_events = None
        self._typed = None

    def events(self) -> Tuple[InputEvent, ...]:
        if self._events is None:
            self._events = tuple(cls(*args[:-1], Provenance(*args[-1])) for cls, args in self._raw)
        return self._events

    def device_events(self, keyboard):
        if keyboard:
            if self._keyboard_events is None:
                self._keyboard_events = tuple(e for e in self.events() if isinstance(e, (KeyEvent, TextEvent, EditingEvent)))
            return self._keyboard_events
        if self._mouse_events is None:
            self._mouse_events = tuple(e for e in self.events() if isinstance(e, (ButtonEvent, MotionEvent, WheelEvent)))
        return self._mouse_events


_input = _Input()
keyboard = _input.keyboard
mouse = _input.mouse
events = _input.events
