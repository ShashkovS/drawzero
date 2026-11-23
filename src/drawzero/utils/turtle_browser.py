"""Python's ``turtle``, drawn by the browser backend.

In the browser there is no Tk, so ``import turtle`` there loads this module
instead (the worker installs it under that name). It keeps the standard
module's interface and its behaviour where a student can see it:

- the window: ``setup()`` sets its size (800 x 800 by default), and the page
  shows it scaled to the canvas; ``setworldcoordinates()`` works;
- the animation: ``speed()``, ``tracer()``, ``delay()`` and ``update()``
  pace the drawing as in CPython — a move is cut into the same number of
  steps, every screen update waits ``delay`` ms — so a slow turtle is slow and
  ``tracer(0)`` is instant;
- what is drawn: lines with round ends, fills under the lines that made them,
  ``circle`` as the same polygon, ``dot``, ``write``, ``stamp`` and the
  turtle shapes (classic, arrow, turtle, circle, square, triangle);
- events: ``onkey``/``onkeypress``/``onkeyrelease``, ``onscreenclick``,
  ``onclick``/``onrelease``/``ondrag`` on a turtle, ``ontimer``; ``mainloop``
  runs while any of them can still fire and returns when none can.

Not here: ``undo``, images (``bgpic``, gif shapes), the Tk canvas itself.

The picture goes to the page as drawzero operations (see
``renderer_browser``), in canvas pixels of the 1000 x 1000 surface; the
turtles themselves are one ``sprites`` operation that replaces the previous
one, so they move without leaving copies.
"""
import math
import time as _time

from . import renderer_browser as _rb
from .colors import THECOLORS

__all__ = [
    # classes
    'ScrolledCanvas', 'TurtleScreen', 'Screen', 'RawTurtle', 'Turtle', 'RawPen', 'Pen', 'Shape', 'Vec2D',
    'TurtleGraphicsError', 'Terminator',
    # screen functions
    'addshape', 'bgcolor', 'bgpic', 'bye', 'clearscreen', 'colormode', 'delay', 'exitonclick', 'getcanvas',
    'getshapes', 'listen', 'mainloop', 'mode', 'numinput', 'onkey', 'onkeypress', 'onkeyrelease',
    'onscreenclick', 'ontimer', 'register_shape', 'resetscreen', 'screensize', 'setup', 'setworldcoordinates',
    'textinput', 'title', 'tracer', 'turtles', 'update', 'window_height', 'window_width',
    # turtle functions
    'back', 'backward', 'begin_fill', 'begin_poly', 'bk', 'circle', 'clear', 'clearstamp', 'clearstamps',
    'clone', 'color', 'degrees', 'distance', 'dot', 'down', 'end_fill', 'end_poly', 'fd', 'fillcolor',
    'filling', 'forward', 'get_poly', 'getpen', 'getscreen', 'get_shapepoly', 'getturtle', 'goto', 'heading',
    'hideturtle', 'home', 'ht', 'isdown', 'isvisible', 'left', 'lt', 'onclick', 'ondrag', 'onrelease', 'pd',
    'pen', 'pencolor', 'pendown', 'pensize', 'penup', 'pos', 'position', 'pu', 'radians', 'right', 'reset',
    'resizemode', 'rt', 'seth', 'setheading', 'setpos', 'setposition', 'settiltangle', 'setundobuffer', 'setx',
    'sety', 'shape', 'shapesize', 'shapetransform', 'shearfactor', 'showturtle', 'speed', 'st', 'stamp',
    'teleport', 'tilt', 'tiltangle', 'towards', 'turtlesize', 'undo', 'undobufferentries', 'up', 'width',
    'write', 'xcor', 'ycor',
    'done',
]

SIZE = 1000                 # the canvas, in drawzero pixels
DEFAULT_WINDOW = (800, 800)
FRAME = 1 / 60              # the page shows at most this many frames a second
FLUSH_OPS = 4000


class TurtleGraphicsError(Exception):
    """Some TurtleGraphics error."""


class Terminator(Exception):
    """Raised by a turtle after ``bye()`` closed its window."""


class _Bye(SystemExit):
    """``bye()``: the program ends, and that is not an error."""

    def __init__(self):
        super().__init__(None)


class Vec2D(tuple):
    """A 2-D vector, as ``turtle.Vec2D``: a tuple with arithmetic."""

    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))

    def __add__(self, other):
        return Vec2D(self[0] + other[0], self[1] + other[1])

    def __mul__(self, other):
        if isinstance(other, Vec2D):
            return self[0] * other[0] + self[1] * other[1]
        return Vec2D(self[0] * other, self[1] * other)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2D(self[0] * other, self[1] * other)
        return NotImplemented

    def __sub__(self, other):
        return Vec2D(self[0] - other[0], self[1] - other[1])

    def __neg__(self):
        return Vec2D(-self[0], -self[1])

    def __abs__(self):
        return math.hypot(*self)

    def rotate(self, angle):
        """Rotate by ``angle`` degrees, counterclockwise."""
        perp = Vec2D(-self[1], self[0])
        angle = math.radians(angle)
        c, s = math.cos(angle), math.sin(angle)
        return Vec2D(self[0] * c + perp[0] * s, self[1] * c + perp[1] * s)

    def __getnewargs__(self):
        return (self[0], self[1])

    def __repr__(self):
        return "(%.2f,%.2f)" % self


# ------------------------------------------------------------------ colours

def _color_name_rgb(name):
    key = name.lower().replace(' ', '')
    if key in THECOLORS:
        return tuple(THECOLORS[key][:3])
    if key.startswith('#') and len(key) in (4, 7, 13):
        digits = key[1:]
        try:
            n = len(digits) // 3
            parts = [int(digits[i * n:(i + 1) * n], 16) for i in range(3)]
        except ValueError:
            return None
        if n == 1:
            return tuple(p * 17 for p in parts)
        if n == 4:
            return tuple(p >> 8 for p in parts)
        return tuple(parts)
    return None


def _shape_points(points):
    return tuple((float(x), float(y)) for x, y in points)


_SHAPES = {
    'arrow': _shape_points(((-10, 0), (10, 0), (0, 10))),
    'turtle': _shape_points(((0, 16), (-2, 14), (-1, 10), (-4, 7), (-7, 9), (-9, 8), (-6, 5), (-7, 1), (-5, -3),
                             (-8, -6), (-6, -8), (-4, -5), (0, -7), (4, -5), (6, -8), (8, -6), (5, -3), (7, 1),
                             (6, 5), (9, 8), (7, 9), (4, 7), (1, 10), (2, 14))),
    'circle': tuple((10 * math.sin(math.radians(a)), 10 * math.cos(math.radians(a))) for a in range(0, 360, 18)),
    'square': _shape_points(((10, -10), (10, 10), (-10, 10), (-10, -10))),
    'triangle': _shape_points(((10, -5.77), (0, 11.55), (-10, -5.77))),
    'classic': _shape_points(((0, 0), (-5, -9), (0, -7), (5, -9))),
    'blank': (),
}


class Shape:
    """A turtle shape: ``Shape("polygon", points)`` or ``Shape("compound")`` with components."""

    def __init__(self, type_, data=None):
        self._type = type_
        if type_ == 'polygon':
            if isinstance(data, list):
                data = tuple(data)
            data = _shape_points(data)
        elif type_ == 'compound':
            data = []
        elif type_ == 'image':
            raise TurtleGraphicsError('image shapes are not available in the browser')
        else:
            raise TurtleGraphicsError('There is no shape type %s' % type_)
        self._data = data

    def addcomponent(self, poly, fill, outline=None):
        if self._type != 'compound':
            raise TurtleGraphicsError('Cannot add component to %s Shape' % self._type)
        if outline is None:
            outline = fill
        self._data.append([_shape_points(poly), fill, outline])


# ------------------------------------------------------------------ the screen

class _Screen:
    """What every turtle draws on: one window, its items and its events."""

    def __init__(self):
        self._turtles = []
        self._shapes = {name: Shape('polygon', pts) for name, pts in _SHAPES.items()}
        self._items = []           # [owner, kind, data] in drawing order
        self._stamps = 0
        self._bg = 'white'
        self._bg_rgb = (255, 255, 255)
        self._colormode = 1.0
        self._mode = 'standard'
        self._tracing = 1
        self._update_counter = 0
        self._delayvalue = 10
        self._window = DEFAULT_WINDOW
        self._world = None         # (llx, lly, urx, ury) after setworldcoordinates
        self._debt = 0.0
        self._last_frame = _time.perf_counter()
        self._frames = 0
        self._dirty = True         # the turtles moved since the last sprites
        self._keys_press = {}
        self._keys_release = {}
        self._any_press = None
        self._any_release = None
        self._clicks = {}
        self._timers = []
        self._timer_seq = 0
        self._dispatching = False
        self._queue = []
        self._drag = None
        self._held = set()
        self._closed = False
        self._fresh = True

    # -------------------------------------------------- geometry

    def _scale(self):
        return SIZE / max(self._window)

    def _to_px(self, x, y):
        """World coordinates to window pixels (y up, origin in the middle)."""
        if self._world is None:
            return x, y
        llx, lly, urx, ury = self._world
        w, h = self._window
        return (x - (llx + urx) / 2) * w / (urx - llx), (y - (lly + ury) / 2) * h / (ury - lly)

    def _from_px(self, px, py):
        if self._world is None:
            return px, py
        llx, lly, urx, ury = self._world
        w, h = self._window
        return px * (urx - llx) / w + (llx + urx) / 2, py * (ury - lly) / h + (lly + ury) / 2

    def _canvas(self, px, py):
        s = self._scale()
        return round(SIZE / 2 + px * s, 3), round(SIZE / 2 - py * s, 3)

    def _world_from_canvas(self, cx, cy):
        s = self._scale()
        return self._from_px((cx - SIZE / 2) / s, (SIZE / 2 - cy) / s)

    # -------------------------------------------------- colours

    def _rgb(self, color):
        """A colour as turtle accepts it, to (r, g, b) 0..255; TurtleGraphicsError if it is not one."""
        if isinstance(color, str):
            rgb = _color_name_rgb(color)
            if rgb is None:
                raise TurtleGraphicsError('bad color string: %s' % (color,))
            return rgb
        try:
            r, g, b = color
        except (TypeError, ValueError):
            raise TurtleGraphicsError('bad color arguments: %s' % (color,)) from None
        if self._colormode == 1.0:
            r, g, b = [round(255.0 * x) for x in (r, g, b)]
        if not all(0 <= x <= 255 for x in (r, g, b)):
            raise TurtleGraphicsError('bad color sequence: %s' % (color,))
        return int(r), int(g), int(b)

    def _colorstr(self, args):
        """A colour argument as given (name, tuple or r, g, b) to what is stored: a name or an rgb tuple."""
        if len(args) == 1:
            args = args[0]
        if isinstance(args, str):
            self._rgb(args)
            return args
        rgb = self._rgb(args)
        return rgb

    def _color_out(self, stored):
        """What ``pencolor()`` returns for a stored colour."""
        if isinstance(stored, str):
            return stored
        if self._colormode == 1.0:
            return tuple(round(c / 255.0, 8) for c in stored)
        return tuple(stored)

    def _rgb_stored(self, stored):
        return stored if isinstance(stored, tuple) else self._rgb(stored)

    # -------------------------------------------------- drawing

    def _push(self, op):
        _rb._ops.append(op)
        if len(_rb._ops) >= FLUSH_OPS:
            self._frame(0, force=True)

    def _add(self, owner, kind, data, emit=True):
        item = [owner, kind, data]
        self._items.append(item)
        if emit:
            for op in self._ops_of(item):
                self._push(op)
        return item

    def _ops_of(self, item):
        _, kind, data = item[:3]
        s = self._scale()
        if kind == 'line':
            rgb, width, pts = data
            flat = []
            for x, y in pts:
                flat.extend(self._canvas(*self._to_px(x, y)))
            return [['path', [*rgb, 255], round(max(width, 1) * s, 3), flat]]
        if kind == 'poly':
            rgb, pts = data
            flat = []
            for x, y in pts:
                flat.extend(self._canvas(*self._to_px(x, y)))
            return [['polygon', [*rgb, 255], 0, flat]] if len(flat) >= 6 else []
        if kind == 'dot':
            rgb, x, y, size = data
            cx, cy = self._canvas(*self._to_px(x, y))
            return [['circle', [*rgb, 255], 0, cx, cy, round(size / 2 * s, 3)]]
        if kind == 'text':
            rgb, text, x, y, font, align = data
            cx, cy = self._canvas(*self._to_px(x, y))
            family, size, style = font
            weight = 'bold' if 'bold' in style else 'normal'
            slant = 'italic' if 'italic' in style else 'normal'
            px = abs(size) * 4 / 3 if size >= 0 else -size
            anchor = {'left': '<', 'center': '.', 'right': '>'}[align]
            return [['text', [*rgb, 255], str(text), cx, cy, round(px * s, 3), anchor + 'v',
                     [family, weight, slant]]]
        if kind == 'stamp':
            return self._shape_ops(data)
        return []

    def _shape_ops(self, look):
        """The operations that draw a turtle as ``look`` (``_Turtle._look()``) describes it."""
        x, y, angle, shape_name, pen_rgb, fill_rgb, stretch, outline = look
        shape = self._shapes.get(shape_name)
        if shape is None:
            return []
        px0, py0 = self._to_px(x, y)
        ex, ey = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        sw, sl = stretch
        s = self._scale()

        def place(points):
            flat = []
            for sx, sy in points:
                fwd, left = sy * sl, -sx * sw
                flat.extend(self._canvas(px0 + fwd * ex - left * ey, py0 + fwd * ey + left * ex))
            return flat

        ops = []
        if shape._type == 'polygon':
            parts = [(shape._data, fill_rgb, pen_rgb)]
        else:
            parts = [(poly, self._rgb(fill), self._rgb(line)) for poly, fill, line in shape._data]
        for poly, fill, line in parts:
            if len(poly) < 2:
                continue
            flat = place(poly)
            if len(poly) >= 3:
                ops.append(['polygon', [*fill, 255], 0, flat])
            if outline > 0:
                ops.append(['path', [*line, 255], round(outline * s, 3), flat + flat[:2]])
        return ops

    def _redraw(self):
        """Draw everything again: after a turtle's clear(), a new window, or new world coordinates."""
        self._push(['clear'])
        self._push(['bg', [*self._bg_rgb, 255]])
        for item in self._items:
            for op in self._ops_of(item):
                self._push(op)
        self._dirty = True

    def _sprites(self):
        ops = []
        for t in self._turtles:
            if t._shown:
                ops.extend(self._shape_ops(t._look()))
        return ['sprites', ops]

    # -------------------------------------------------- time

    def _frame(self, wait, force=False):
        """One screen update that should last ``wait`` seconds.

        Updates shorter than a frame of the page are joined: their waits add
        up and one frame carries them, so a turtle with ``delay(10)`` keeps its
        pace without asking the page for a hundred frames a second.
        """
        if self._closed:
            raise Terminator()
        self._debt += wait
        if not force and self._debt < FRAME and not self._fresh:
            return
        if self._dirty or self._fresh:
            _rb._ops.append(self._sprites())
            self._dirty = False
        self._fresh = False
        debt, self._debt = self._debt, 0.0
        self._frames += 1
        for event in _rb._send(debt):
            self._queue.append(event)
        self._last_frame = _time.perf_counter()
        self._dispatch()

    def _turtle_update(self):
        """A turtle moved one step: CPython's ``RawTurtle._update``."""
        self._dirty = True
        if self._tracing == 0:
            return
        if self._tracing == 1:
            self._frame(self._delayvalue / 1000)
        else:
            self._update_counter += 1
            if self._update_counter >= self._tracing:
                self._update_counter = 0
                self._frame(self._delayvalue / 1000)

    def _sleep(self, seconds):
        """``time.sleep`` while turtle is in use: the screen stays live."""
        seconds = float(seconds)
        if seconds < 0:
            raise ValueError('sleep length must be non-negative')
        end = _time.perf_counter() + seconds
        self._frame(0, force=True)
        while True:
            left = end - _time.perf_counter()
            if left <= 0:
                break
            self._frame(min(left, 0.1), force=True)

    def _finish(self):
        """The program has ended: show the turtles where they stopped."""
        if not self._closed:
            _rb._ops.append(self._sprites())

    # -------------------------------------------------- events

    def _has_handlers(self):
        if self._timers or self._keys_press or self._keys_release or self._any_press or self._any_release:
            return True
        if self._clicks:
            return True
        return any(t._handlers for t in self._turtles)

    def _call(self, fun, *args):
        if fun is not None:
            fun(*args)

    def _dispatch(self):
        if self._dispatching:
            return
        self._dispatching = True
        try:
            while True:
                now = _time.perf_counter()
                due = [t for t in self._timers if t[0] <= now]
                if due:
                    due.sort()
                    first = due[0]
                    self._timers.remove(first)
                    first[2]()
                    continue
                if not self._queue:
                    break
                self._event(self._queue.pop(0))
        finally:
            self._dispatching = False

    def _event(self, ev):
        t = ev.get('t')
        if t == 'kd':
            names = _key_names(ev)
            if not ev.get('r'):
                self._held.update(names)
            for name in names:
                if name in self._keys_press:
                    self._call(self._keys_press[name])
                    break
            else:
                if self._any_press is not None:
                    self._any_press()
        elif t == 'ku':
            names = _key_names(ev)
            self._held.difference_update(names)
            for name in names:
                if name in self._keys_release:
                    self._call(self._keys_release[name])
                    break
            else:
                if self._any_release is not None:
                    self._any_release()
        elif t in ('md', 'mu'):
            x, y = self._world_from_canvas(ev['x'], ev['y'])
            button = ev.get('b', 1)
            if t == 'md':
                for turtle in reversed(self._turtles):
                    if turtle._hit(x, y):
                        handler = turtle._handlers.get(('click', button))
                        if ('drag', button) in turtle._handlers:
                            self._drag = (turtle, button)
                        if handler:
                            handler(x, y)
                            return
                        break
                for fun in self._clicks.get(button, ()):
                    fun(x, y)
            else:
                drag, self._drag = self._drag, None
                for turtle in reversed(self._turtles):
                    if (drag and drag[0] is turtle) or turtle._hit(x, y):
                        handler = turtle._handlers.get(('release', button))
                        if handler:
                            handler(x, y)
                        break
        elif t == 'mm':
            if self._drag is not None:
                turtle, button = self._drag
                handler = turtle._handlers.get(('drag', button))
                if handler:
                    handler(*self._world_from_canvas(ev['x'], ev['y']))

    # -------------------------------------------------- the public screen methods

    def bgcolor(self, *args):
        if not args:
            return self._color_out(self._bg) if not isinstance(self._bg, str) else self._bg
        self._bg = self._colorstr(args)
        self._bg_rgb = self._rgb_stored(self._bg)
        self._push(['bg', [*self._bg_rgb, 255]])
        self._frame(0, force=True)

    def bgpic(self, picname=None):
        if picname is None or picname == 'nopic':
            return 'nopic'
        raise TurtleGraphicsError('bgpic: pictures are not available in the browser')

    def colormode(self, cmode=None):
        if cmode is None:
            return self._colormode
        if cmode == 1.0:
            self._colormode = float(cmode)
        elif cmode == 255:
            self._colormode = int(cmode)

    def mode(self, mode=None):
        if mode is None:
            return self._mode
        mode = mode.lower()
        if mode not in ('standard', 'logo', 'world'):
            raise TurtleGraphicsError('No turtle-graphics-mode %s' % mode)
        self._mode = mode
        if mode in ('standard', 'logo'):
            self._world = None
        self.reset()

    def setworldcoordinates(self, llx, lly, urx, ury):
        if urx == llx or ury == lly:
            raise TurtleGraphicsError('world coordinates need a non-empty rectangle')
        if self._mode != 'world':
            self._mode = 'world'
        self._world = (llx, lly, urx, ury)
        self._redraw()
        self._frame(0, force=True)

    def setup(self, width=None, height=None, startx=None, starty=None):
        w0, h0 = self._window
        if width is None:
            width = w0
        if height is None:
            height = h0
        # A fraction is a share of the screen; this "screen" is 1000 pixels each way.
        if isinstance(width, float) and 0 <= width <= 1:
            width = width * SIZE
        if isinstance(height, float) and 0 <= height <= 1:
            height = height * SIZE
        width, height = int(width), int(height)
        if width <= 0 or height <= 0:
            raise TurtleGraphicsError('the window needs a positive size')
        self._window = (width, height)
        self._redraw()
        self._frame(0, force=True)

    def screensize(self, canvwidth=None, canvheight=None, bg=None):
        if canvwidth is None and canvheight is None and bg is None:
            return self._window
        if bg is not None:
            self.bgcolor(bg)

    def window_width(self):
        return self._window[0]

    def window_height(self):
        return self._window[1]

    def title(self, titlestring):
        pass

    def tracer(self, n=None, delay=None):
        if n is None:
            return self._tracing
        self._tracing = int(n)
        self._update_counter = 0
        if delay is not None:
            self._delayvalue = int(delay)
        if self._tracing:
            self.update()

    def delay(self, delay=None):
        if delay is None:
            return self._delayvalue
        self._delayvalue = int(delay)

    def update(self):
        self._dirty = True
        self._frame(0, force=True)

    def turtles(self):
        return list(self._turtles)

    def register_shape(self, name, shape=None):
        if shape is None:
            if isinstance(name, str) and name.lower().endswith('.gif'):
                raise TurtleGraphicsError('gif shapes are not available in the browser')
            raise TurtleGraphicsError('register_shape needs a shape: a tuple of points or a Shape')
        if not isinstance(shape, Shape):
            shape = Shape('polygon', shape)
        self._shapes[name] = shape

    addshape = register_shape

    def getshapes(self):
        return sorted(self._shapes)

    def clear(self):
        """``clearscreen()``: delete all drawings and all turtles."""
        self._items.clear()
        self._turtles.clear()
        self._bg, self._bg_rgb = 'white', (255, 255, 255)
        self._keys_press.clear()
        self._keys_release.clear()
        self._any_press = self._any_release = None
        self._clicks.clear()
        self._timers.clear()
        self._tracing, self._delayvalue = 1, 10
        self._redraw()
        self._frame(0, force=True)

    clearscreen = clear

    def reset(self):
        for t in self._turtles:
            t.reset()

    resetscreen = reset

    def listen(self, xdummy=None, ydummy=None):
        pass

    def onkeyrelease(self, fun, key):
        if fun is None:
            self._keys_release.pop(key, None)
        elif key is None:
            self._any_release = fun
        else:
            self._keys_release[key] = fun

    onkey = onkeyrelease

    def onkeypress(self, fun, key=None):
        if key is None:
            self._any_press = fun
        elif fun is None:
            self._keys_press.pop(key, None)
        else:
            self._keys_press[key] = fun

    def onscreenclick(self, fun, btn=1, add=None):
        if fun is None:
            self._clicks.pop(btn, None)
        elif add:
            self._clicks.setdefault(btn, []).append(fun)
        else:
            self._clicks[btn] = [fun]

    onclick = onscreenclick

    def ontimer(self, fun, t=0):
        self._timer_seq += 1
        self._timers.append((_time.perf_counter() + max(t, 0) / 1000, self._timer_seq, fun))

    def mainloop(self):
        """Run the event loop while a handler or a timer can still do something."""
        self._frame(0, force=True)
        while self._has_handlers() and not self._closed:
            self._frame(FRAME, force=True)

    done = mainloop

    def exitonclick(self):
        self.onscreenclick(lambda x, y: self.bye())
        self.mainloop()

    def bye(self):
        self._finish()
        self._closed = True
        raise _Bye()

    def textinput(self, title, prompt):
        self._frame(0, force=True)
        try:
            return input()
        except EOFError:
            return None

    def numinput(self, title, prompt, default=None, minval=None, maxval=None):
        text = self.textinput(title, prompt)
        if text is None:
            return None
        try:
            return float(text)
        except ValueError:
            return default

    def getcanvas(self):
        raise TurtleGraphicsError('there is no Tk canvas in the browser')


_KEYSYMS = {
    'ArrowUp': 'Up', 'ArrowDown': 'Down', 'ArrowLeft': 'Left', 'ArrowRight': 'Right',
    'Space': 'space', 'Enter': 'Return', 'NumpadEnter': 'KP_Enter', 'Escape': 'Escape', 'Tab': 'Tab',
    'Backspace': 'BackSpace', 'Delete': 'Delete', 'Insert': 'Insert', 'Home': 'Home', 'End': 'End',
    'PageUp': 'Prior', 'PageDown': 'Next', 'ShiftLeft': 'Shift_L', 'ShiftRight': 'Shift_R',
    'ControlLeft': 'Control_L', 'ControlRight': 'Control_R', 'AltLeft': 'Alt_L', 'AltRight': 'Alt_R',
    'CapsLock': 'Caps_Lock',
}
_CHAR_NAMES = {
    ' ': 'space', '+': 'plus', '-': 'minus', '=': 'equal', ',': 'comma', '.': 'period', '/': 'slash',
    ';': 'semicolon', "'": 'apostrophe', '[': 'bracketleft', ']': 'bracketright', '\\': 'backslash',
    '*': 'asterisk', '!': 'exclam', '?': 'question', '<': 'less', '>': 'greater', '_': 'underscore',
}
for _f in range(1, 13):
    _KEYSYMS[f'F{_f}'] = f'F{_f}'


def _key_names(ev):
    """Tk's names for a key event: the keysym, then the character it types."""
    names = []
    code, key = ev.get('code', ''), ev.get('key', '')
    if code in _KEYSYMS:
        names.append(_KEYSYMS[code])
    if len(key) == 1:
        names.append(key)
        if key in _CHAR_NAMES:
            names.append(_CHAR_NAMES[key])
    return names


# ------------------------------------------------------------------ turtles

class RawTurtle:
    """A turtle; ``Turtle`` is the same on the one screen there is."""

    def __init__(self, canvas=None, shape='classic', undobuffersize=1000, visible=True):
        screen = _getscreen()
        self.screen = screen
        self._handlers = {}
        self._shape = shape
        self._shown = bool(visible)
        self._reset_state()
        screen._turtles.append(self)
        screen._dirty = True
        if self._shown:
            screen._turtle_update()

    def _reset_state(self):
        self._x = self._y = 0.0
        # The heading is a unit vector, turned by Vec2D.rotate, as in CPython: a
        # turtle that has only gone along the axes stays on whole numbers.
        self._orient = Vec2D(0.0, 1.0) if self.screen._mode == 'logo' else Vec2D(1.0, 0.0)
        self._tilt = 0.0
        self._fullcircle = 360.0
        self._down = True
        self._pensize = 1
        self._speed = 3
        self._pencolor = 'black'
        self._fillcolor = 'black'
        self._stretch = (1.0, 1.0)
        self._outline = 1
        self._fill_path = None
        self._fill_index = 0
        self._poly = None

    # -------------------------------------------------- helpers

    @property
    def _angle(self):
        return math.degrees(math.atan2(self._orient[1], self._orient[0]))

    @property
    def _dpau(self):
        return 360.0 / self._fullcircle

    def _pen_rgb(self):
        return self.screen._rgb_stored(self._pencolor)

    def _fill_rgb(self):
        return self.screen._rgb_stored(self._fillcolor)

    def _look(self):
        return (self._x, self._y, self._screen_angle() + self._tilt, self._shape,
                self._pen_rgb(), self._fill_rgb(), self._stretch, self._outline)

    def _screen_angle(self):
        """The heading on the window, after world coordinates' stretching."""
        if self.screen._world is None:
            return self._angle
        ex, ey = math.cos(math.radians(self._angle)), math.sin(math.radians(self._angle))
        x0, y0 = self.screen._to_px(0, 0)
        x1, y1 = self.screen._to_px(ex, ey)
        return math.degrees(math.atan2(y1 - y0, x1 - x0))

    def _hit(self, x, y):
        px, py = self.screen._to_px(x, y)
        tx, ty = self.screen._to_px(self._x, self._y)
        return self._shown and math.hypot(px - tx, py - ty) <= 10 * max(self._stretch) + 2

    def _line(self, start, end):
        if self._down:
            self.screen._add(self, 'line', (self._pen_rgb(), self._pensize, [start, end]))

    def _goto(self, x, y, draw=True):
        screen = self.screen
        start = (self._x, self._y)
        end = (float(x), float(y))
        if self._speed and screen._tracing == 1:
            sx, sy = screen._to_px(*start)
            ex, ey = screen._to_px(*end)
            dist = math.hypot(ex - sx, ey - sy)
            nhops = 1 + int(dist / (3 * (1.1 ** self._speed) * self._speed))
            prev = start
            for n in range(1, nhops):
                k = n / nhops
                point = (start[0] + (end[0] - start[0]) * k, start[1] + (end[1] - start[1]) * k)
                if draw and self._down:
                    for op in screen._ops_of([self, 'line', (self._pen_rgb(), self._pensize, [prev, point])]):
                        screen._push(op)
                prev = point
                self._x, self._y = point
                screen._turtle_update()
            if draw and self._down:
                for op in screen._ops_of([self, 'line', (self._pen_rgb(), self._pensize, [prev, end])]):
                    screen._push(op)
                self.screen._add(self, 'line', (self._pen_rgb(), self._pensize, [start, end]), emit=False)
        elif draw:
            self._line(start, end)
        self._x, self._y = end
        if self._fill_path is not None:
            self._fill_path.append(end)
        if self._poly is not None:
            self._poly.append(end)
        screen._turtle_update()

    def _rotate(self, angle):
        """Turn by ``angle`` (degrees, counterclockwise), in steps when animated."""
        screen = self.screen
        if self._speed and screen._tracing == 1:
            anglevel = 3.0 * self._speed
            steps = 1 + int(abs(angle) / anglevel)
            delta = angle / steps
            for _ in range(steps):
                self._orient = self._orient.rotate(delta)
                screen._turtle_update()
        else:
            self._orient = self._orient.rotate(angle)
            screen._turtle_update()

    # -------------------------------------------------- motion

    def forward(self, distance):
        end = Vec2D(self._x, self._y) + self._orient * distance
        self._goto(end[0], end[1])

    fd = forward

    def back(self, distance):
        self.forward(-distance)

    bk = backward = back

    def left(self, angle):
        self._rotate(angle * self._dpau)

    lt = left

    def right(self, angle):
        self._rotate(-angle * self._dpau)

    rt = right

    def goto(self, x, y=None):
        if y is None:
            x, y = x
        self._goto(x, y)

    setpos = setposition = goto

    def teleport(self, x=None, y=None, *, fill_gap=False):
        x = self._x if x is None else x
        y = self._y if y is None else y
        if fill_gap:
            self._goto(x, y, draw=False)
        else:
            self._x, self._y = float(x), float(y)
            if self._fill_path is not None:
                self._fill_path.append((self._x, self._y))
            self.screen._turtle_update()

    def setx(self, x):
        self._goto(x, self._y)

    def sety(self, y):
        self._goto(self._x, y)

    def setheading(self, to_angle):
        angle = to_angle - self.heading()
        if self.screen._mode == 'logo':
            angle = -angle
        full = self._fullcircle
        angle = (angle + full / 2.0) % full - full / 2.0
        self._rotate(angle * self._dpau)

    seth = setheading

    def home(self):
        self.goto(0, 0)
        self.setheading(0)

    def circle(self, radius, extent=None, steps=None):
        speed = self.speed()
        fullcircle = self._fullcircle
        if extent is None:
            extent = fullcircle
        if steps is None:
            frac = abs(extent) / fullcircle
            steps = 1 + int(min(11 + abs(radius) / 6.0, 59.0) * frac)
        w = 1.0 * extent / steps
        w2 = 0.5 * w
        length = 2.0 * radius * math.sin(math.radians(w2 * self._dpau))
        if radius < 0:
            length, w, w2 = -length, -w, -w2
        screen = self.screen
        tracing, delay = screen._tracing, screen._delayvalue
        if speed == 0:
            screen._tracing = 0
        else:
            self._speed = 0
        self._rotate(w2 * self._dpau)
        for _ in range(steps):
            self._speed = speed
            self.forward(length)
            self._speed = 0
            self._rotate(w * self._dpau)
        self._rotate(-w2 * self._dpau)
        if speed == 0:
            screen._tracing, screen._delayvalue = tracing, delay
            screen._turtle_update()
        self._speed = speed

    def speed(self, speed=None):
        speeds = {'fastest': 0, 'fast': 10, 'normal': 6, 'slow': 3, 'slowest': 1}
        if speed is None:
            return self._speed
        if speed in speeds:
            speed = speeds[speed]
        elif 0.5 < speed < 10.5:
            speed = int(round(speed))
        else:
            speed = 0
        self._speed = speed

    # -------------------------------------------------- state

    def position(self):
        return Vec2D(self._x, self._y)

    pos = position

    def xcor(self):
        return self._x

    def ycor(self):
        return self._y

    def heading(self):
        x, y = self._orient
        result = round(math.atan2(y, x) * 180.0 / math.pi, 10) % 360.0
        result /= self._dpau
        if self.screen._mode == 'logo':
            return (self._fullcircle / 4 - result) % self._fullcircle
        return result % self._fullcircle

    def towards(self, x, y=None):
        if y is None:
            if isinstance(x, RawTurtle):
                x, y = x._x, x._y
            else:
                x, y = x
        angle = math.degrees(math.atan2(y - self._y, x - self._x)) % 360.0
        if self.screen._mode == 'logo':
            angle = (90.0 - angle) % 360.0
        return round(angle / self._dpau, 10) % self._fullcircle

    def distance(self, x, y=None):
        if y is None:
            if isinstance(x, RawTurtle):
                x, y = x._x, x._y
            else:
                x, y = x
        return math.hypot(x - self._x, y - self._y)

    def degrees(self, fullcircle=360.0):
        self._fullcircle = fullcircle

    def radians(self):
        self.degrees(2 * math.pi)

    # -------------------------------------------------- pen

    def pendown(self):
        self._down = True

    pd = down = pendown

    def penup(self):
        self._down = False

    pu = up = penup

    def isdown(self):
        return self._down

    def pensize(self, width=None):
        if width is None:
            return self._pensize
        self._pensize = width

    width = pensize

    def pencolor(self, *args):
        if not args:
            return self.screen._color_out(self._pencolor)
        self._pencolor = self.screen._colorstr(args)
        self.screen._dirty = True

    def fillcolor(self, *args):
        if not args:
            return self.screen._color_out(self._fillcolor)
        self._fillcolor = self.screen._colorstr(args)
        self.screen._dirty = True

    def color(self, *args):
        if not args:
            return self.pencolor(), self.fillcolor()
        if len(args) == 1:
            self.pencolor(args[0])
            self.fillcolor(args[0])
        elif len(args) == 2:
            self.pencolor(args[0])
            self.fillcolor(args[1])
        elif len(args) == 3:
            self.pencolor(args)
            self.fillcolor(args)
        else:
            raise TurtleGraphicsError('color() takes at most 3 arguments')

    def pen(self, pen=None, **pendict):
        current = {
            'shown': self._shown, 'pendown': self._down, 'pencolor': self.pencolor(),
            'fillcolor': self.fillcolor(), 'pensize': self._pensize, 'speed': self._speed,
            'resizemode': 'noresize', 'stretchfactor': self._stretch, 'shearfactor': 0.0,
            'outline': self._outline, 'tilt': self._tilt,
        }
        if pen is None and not pendict:
            return current
        settings = dict(pen or {}, **pendict)
        if 'shown' in settings:
            (self.showturtle if settings['shown'] else self.hideturtle)()
        if 'pendown' in settings:
            self._down = bool(settings['pendown'])
        if 'pencolor' in settings:
            self.pencolor(settings['pencolor'])
        if 'fillcolor' in settings:
            self.fillcolor(settings['fillcolor'])
        if 'pensize' in settings:
            self._pensize = settings['pensize']
        if 'speed' in settings:
            self.speed(settings['speed'])
        if 'stretchfactor' in settings:
            self._stretch = tuple(settings['stretchfactor'])
        if 'outline' in settings:
            self._outline = settings['outline']
        if 'tilt' in settings:
            self._tilt = settings['tilt']

    # -------------------------------------------------- filling

    def filling(self):
        return self._fill_path is not None

    def begin_fill(self):
        self._fill_path = [(self._x, self._y)]
        self._fill_index = len(self.screen._items)

    def end_fill(self):
        if self._fill_path is None:
            return
        path, self._fill_path = self._fill_path, None
        screen = self.screen
        if len(path) > 2:
            # The fill lies under the lines drawn since begin_fill, as in Tk.
            item = [self, 'poly', (self._fill_rgb(), path)]
            index = min(self._fill_index, len(screen._items))
            screen._items.insert(index, item)
            for op in screen._ops_of(item):
                screen._push(op)
            for later in screen._items[index + 1:]:
                for op in screen._ops_of(later):
                    screen._push(op)
        screen._turtle_update()

    def begin_poly(self):
        self._poly = [(self._x, self._y)]

    def end_poly(self):
        pass

    def get_poly(self):
        return tuple(self._poly) if self._poly is not None else None

    # -------------------------------------------------- more drawing

    def dot(self, size=None, *color):
        if not color:
            if isinstance(size, (str, tuple)):
                color, size = self.screen._colorstr((size,)), None
            else:
                color = self._pencolor
        else:
            color = self.screen._colorstr(color)
        if size is None:
            size = max(self._pensize + 4, 2 * self._pensize)
        self.screen._add(self, 'dot', (self.screen._rgb_stored(color), self._x, self._y, size))
        self.screen._turtle_update()

    def write(self, arg, move=False, align='left', font=('Arial', 8, 'normal')):
        align = align.lower()
        if align not in ('left', 'center', 'right'):
            raise TurtleGraphicsError('align must be "left", "center" or "right"')
        family = font[0] if len(font) > 0 else 'Arial'
        size = font[1] if len(font) > 1 else 8
        style = font[2] if len(font) > 2 else 'normal'
        text = str(arg)
        self.screen._add(self, 'text', (self._pen_rgb(), text, self._x, self._y, (family, size, style), align))
        if move:
            px = abs(size) * 4 / 3 if size >= 0 else -size
            width = 0.55 * px * max((len(line) for line in text.split('\n')), default=0)
            if align == 'left':
                self._goto(self._x + width, self._y, draw=True)
            elif align == 'center':
                self._goto(self._x + width / 2, self._y, draw=True)
        self.screen._turtle_update()

    def stamp(self):
        screen = self.screen
        screen._stamps += 1
        stamp_id = screen._stamps
        item = screen._add(self, 'stamp', self._look())
        item.append(stamp_id)
        screen._turtle_update()
        return stamp_id

    def clearstamp(self, stampid):
        before = len(self.screen._items)
        self.screen._items[:] = [it for it in self.screen._items
                                 if not (it[1] == 'stamp' and it[0] is self and it[3] == stampid)]
        if len(self.screen._items) != before:
            self.screen._redraw()
            self.screen._turtle_update()

    def clearstamps(self, n=None):
        mine = [it for it in self.screen._items if it[1] == 'stamp' and it[0] is self]
        if n is None:
            drop = mine
        elif n >= 0:
            drop = mine[:n]
        else:
            drop = mine[n:]
        if drop:
            ids = {id(it) for it in drop}
            self.screen._items[:] = [it for it in self.screen._items if id(it) not in ids]
            self.screen._redraw()
            self.screen._turtle_update()

    def clear(self):
        self.screen._items[:] = [it for it in self.screen._items if it[0] is not self]
        self._fill_path = None
        self.screen._redraw()
        self.screen._turtle_update()

    def reset(self):
        self.screen._items[:] = [it for it in self.screen._items if it[0] is not self]
        shown, shape = self._shown, self._shape
        self._reset_state()
        self._shown, self._shape = shown, shape
        self.screen._redraw()
        self.screen._turtle_update()

    # -------------------------------------------------- appearance

    def hideturtle(self):
        self._shown = False
        self.screen._turtle_update()

    ht = hideturtle

    def showturtle(self):
        self._shown = True
        self.screen._turtle_update()

    st = showturtle

    def isvisible(self):
        return self._shown

    def shape(self, name=None):
        if name is None:
            return self._shape
        if name not in self.screen._shapes:
            raise TurtleGraphicsError('There is no shape named %s' % name)
        self._shape = name
        self.screen._turtle_update()

    def shapesize(self, stretch_wid=None, stretch_len=None, outline=None):
        if stretch_wid is None and stretch_len is None and outline is None:
            return self._stretch[0], self._stretch[1], self._outline
        if stretch_wid == 0 or stretch_len == 0:
            raise TurtleGraphicsError('stretch_wid/stretch_len must not be zero')
        if stretch_wid is not None:
            if stretch_len is None:
                self._stretch = (stretch_wid, stretch_wid)
            else:
                self._stretch = (stretch_wid, stretch_len)
        elif stretch_len is not None:
            self._stretch = (self._stretch[0], stretch_len)
        if outline is not None:
            self._outline = outline
        self.screen._turtle_update()

    turtlesize = shapesize

    def resizemode(self, rmode=None):
        if rmode is None:
            return 'noresize'

    def shearfactor(self, shear=None):
        if shear is None:
            return 0.0

    def shapetransform(self, t11=None, t12=None, t21=None, t22=None):
        if t11 is None:
            return (self._stretch[1], 0.0, 0.0, self._stretch[0])

    def tilt(self, angle):
        self._tilt += angle * self._dpau
        self.screen._turtle_update()

    def settiltangle(self, angle):
        self._tilt = angle * self._dpau
        self.screen._turtle_update()

    def tiltangle(self, angle=None):
        if angle is None:
            return (self._tilt / self._dpau) % self._fullcircle
        self.settiltangle(angle)

    def get_shapepoly(self):
        shape = self.screen._shapes.get(self._shape)
        if shape is None or shape._type != 'polygon':
            return None
        sw, sl = self._stretch
        return tuple((x * sw, y * sl) for x, y in shape._data)

    # -------------------------------------------------- events

    def onclick(self, fun, btn=1, add=None):
        self._set_handler('click', fun, btn)

    def onrelease(self, fun, btn=1, add=None):
        self._set_handler('release', fun, btn)

    def ondrag(self, fun, btn=1, add=None):
        self._set_handler('drag', fun, btn)

    def _set_handler(self, kind, fun, btn):
        if fun is None:
            self._handlers.pop((kind, btn), None)
        else:
            self._handlers[(kind, btn)] = fun

    # -------------------------------------------------- the rest

    def clone(self):
        twin = RawTurtle.__new__(type(self))
        twin.__dict__.update(self.__dict__)
        twin._handlers = {}
        twin._fill_path = None
        twin._poly = None
        self.screen._turtles.append(twin)
        self.screen._turtle_update()
        return twin

    def getscreen(self):
        return self.screen

    def getturtle(self):
        return self

    getpen = getturtle

    def setundobuffer(self, size):
        pass

    def undobufferentries(self):
        return 0

    def undo(self):
        raise TurtleGraphicsError('undo() is not available in the browser')

    def _screen_method(name):
        def method(self, *args, **kwargs):
            return getattr(self.screen, name)(*args, **kwargs)
        method.__name__ = name
        return method

    # A turtle passes these to its screen, as CPython's RawTurtle does.
    onkey = _screen_method('onkey')
    onkeypress = _screen_method('onkeypress')
    onkeyrelease = _screen_method('onkeyrelease')
    ontimer = _screen_method('ontimer')
    listen = _screen_method('listen')
    del _screen_method


Turtle = Pen = RawPen = RawTurtle


class TurtleScreen(_Screen):
    """The screen class; there is one screen, ``Screen()``."""


class ScrolledCanvas:
    def __init__(self, *args, **kwargs):
        raise TurtleGraphicsError('there is no Tk canvas in the browser')


_screen = None
_pen = None


def _getscreen():
    global _screen
    if _screen is None:
        _screen = TurtleScreen()
        _rb._ops.append(['clear'])
        _rb._ops.append(['bg', [255, 255, 255, 255]])
    return _screen


def Screen():
    """The screen: one per program."""
    return _getscreen()


def _getpen():
    global _pen
    if _pen is None:
        _pen = Turtle()
    return _pen


def _reset():
    """Forget the previous run's screen and turtles (the worker calls this before a run)."""
    global _screen, _pen
    _screen = None
    _pen = None


def _finish():
    """The program ended: show the turtles (the worker calls this after a run)."""
    if _screen is not None:
        _screen._finish()


def _sleep(seconds):
    if _screen is None:
        _real_sleep(seconds)
    else:
        _screen._sleep(seconds)


_real_sleep = _time.sleep


# Module functions: the screen's on the screen, the turtle's on the anonymous turtle.
_SCREEN_FUNCTIONS = [
    'addshape', 'bgcolor', 'bgpic', 'bye', 'clearscreen', 'colormode', 'delay', 'exitonclick',
    'getcanvas', 'getshapes', 'listen', 'mainloop', 'mode', 'numinput', 'onkey', 'onkeypress',
    'onkeyrelease', 'onscreenclick', 'ontimer', 'register_shape', 'resetscreen', 'screensize', 'setup',
    'setworldcoordinates', 'textinput', 'title', 'tracer', 'turtles', 'update', 'window_height',
    'window_width', 'done',
]
_TURTLE_FUNCTIONS = [
    'back', 'backward', 'begin_fill', 'begin_poly', 'bk', 'circle', 'clear', 'clearstamp', 'clearstamps',
    'clone', 'color', 'degrees', 'distance', 'dot', 'down', 'end_fill', 'end_poly', 'fd', 'fillcolor',
    'filling', 'forward', 'get_poly', 'getpen', 'getscreen', 'get_shapepoly', 'getturtle', 'goto',
    'heading', 'hideturtle', 'home', 'ht', 'isdown', 'isvisible', 'left', 'lt', 'onclick', 'ondrag',
    'onrelease', 'pd', 'pen', 'pencolor', 'pendown', 'pensize', 'penup', 'pos', 'position', 'pu', 'radians',
    'right', 'reset', 'resizemode', 'rt', 'seth', 'setheading', 'setpos', 'setposition', 'settiltangle',
    'setundobuffer', 'setx', 'sety', 'shape', 'shapesize', 'shapetransform', 'shearfactor', 'showturtle',
    'speed', 'st', 'stamp', 'teleport', 'tilt', 'tiltangle', 'towards', 'turtlesize', 'undo',
    'undobufferentries', 'up', 'width', 'write', 'xcor', 'ycor',
]


def _screen_function(name):
    def function(*args, **kwargs):
        return getattr(_getscreen(), name)(*args, **kwargs)
    function.__name__ = name
    function.__doc__ = getattr(_Screen, name).__doc__
    return function


def _turtle_function(name):
    def function(*args, **kwargs):
        return getattr(_getpen(), name)(*args, **kwargs)
    function.__name__ = name
    function.__doc__ = getattr(RawTurtle, name).__doc__
    return function


for _name in _SCREEN_FUNCTIONS:
    globals()[_name] = _screen_function(_name)
for _name in _TURTLE_FUNCTIONS:
    globals()[_name] = _turtle_function(_name)
del _name
