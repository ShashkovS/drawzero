"""Judge-side checking of drawing programs.

A program judged with ``EJUDGE_MODE=1`` prints its drawing instead of showing
it: one JSON object per shape (see ``utils/renderer_ejudge.py``). A problem's
checker reads that output back as shapes and decides about them with the
geometry here::

    #!/opt/ejudge/ej_py_venv_314/bin/python
    from drawzero.checking import main, Wrong, say

    def check(drawing, test_input, answer):
        lines = drawing.only('line')
        if len(lines) != 3:
            raise Wrong(say('Draw exactly three lines.', 'Нужно ровно три линии.'))
        return say('Right!', 'Верно!')

    raise SystemExit(main(check))

ejudge calls ``check <input> <output> [<answer>]``. Exit codes: 0 OK, 1 WA,
2 PE, 6 a check failure; the message goes to stdout, which ejudge shows as the
checker's comment.

Coordinates are canvas pixels of the 1000x1000 surface, integers, y down.
"""
from __future__ import annotations

import json
import math
import sys
import traceback
from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Optional, Sequence, Tuple

OK, WRONG_ANSWER, PRESENTATION_ERROR, CHECK_FAILED = 0, 1, 2, 6

Point = Tuple[float, float]
Polygon = Sequence[Point]


class Wrong(Exception):
    """The drawing is not what the problem asks for; the message says why."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def say(en: str, ru: str) -> str:
    """One message in both of the course's languages."""
    return f'{en} / {ru}'


# ---------------------------------------------------------------- shapes

@dataclass
class Shape:
    """One drawing call, in canvas pixels.

    ``kind`` is the renderer's figure: line, circle, rect, ellipse, arc,
    polygon, text, fill, clear or image (``filled_rect`` is a ``rect`` with
    ``filled``; ``rect_rotated`` is a ``polygon``). ``points`` are a line's
    ends, a polygon's vertices, or a rect's corners from the top left,
    clockwise. ``index`` is its place among the shapes, ``frame`` the number
    of ticks before it.
    """
    kind: str
    color: Tuple[int, int, int] = (0, 0, 0)
    alpha: int = 255
    width: Optional[int] = None
    index: int = 0
    frame: int = 0
    points: List[Point] = field(default_factory=list)
    center: Optional[Point] = None
    radius: Optional[float] = None
    box: Optional[Tuple[int, int, int, int]] = None
    text: str = ''
    size: int = 0
    raw: dict = field(default_factory=dict)

    @property
    def filled(self) -> bool:
        return self.kind in ('fill', 'clear', 'text', 'image') or self.width == 0

    @property
    def name(self) -> str:
        """What the student called, as near as the output can tell."""
        if self.kind in ('circle', 'rect', 'ellipse', 'polygon') and self.width == 0:
            return 'filled_' + self.kind
        return self.kind

    def rectangle(self) -> Optional['Rect']:
        """This shape as an axis-parallel rectangle, if it is one."""
        if self.kind == 'rect':
            x, y, w, h = self.box
            return Rect(min(x, x + w), min(y, y + h), max(x, x + w), max(y, y + h))
        if self.kind == 'polygon' and len(self.points) == 4 and is_rectangle(self.points):
            return axis_rect(self.points)
        return None

    def polygon(self) -> Optional[List[Point]]:
        """Vertices of a rect or a polygon."""
        if self.kind == 'rect':
            return list(self.rectangle().corners)
        if self.kind == 'polygon':
            return list(self.points)
        return None

    def __repr__(self) -> str:
        if self.kind == 'circle':
            geometry = f'{self.center}, r={self.radius}'
        elif self.kind in ('rect', 'ellipse', 'arc'):
            geometry = f'{self.box}'
        elif self.kind == 'text':
            geometry = repr(self.text)
        else:
            geometry = ', '.join(map(str, self.points))
        return f'{self.name}({color_name(self.color)}, {geometry})'


@dataclass(frozen=True)
class Rect:
    """An axis-parallel rectangle by its edges."""
    left: float
    top: float
    right: float
    bottom: float

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.bottom - self.top

    @property
    def center(self) -> Point:
        return ((self.left + self.right) / 2, (self.top + self.bottom) / 2)

    @property
    def corners(self) -> Tuple[Point, Point, Point, Point]:
        return ((self.left, self.top), (self.right, self.top), (self.right, self.bottom), (self.left, self.bottom))

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def orientation(self) -> str:
        if self.height > self.width:
            return 'vertical'
        if self.height < self.width:
            return 'horizontal'
        return 'square'

    def contains(self, other: 'Rect', strict: bool = False) -> bool:
        if strict:
            return self.left < other.left and other.right < self.right and self.top < other.top and other.bottom < self.bottom
        return self.left <= other.left and other.right <= self.right and self.top <= other.top and other.bottom <= self.bottom

    def overlaps(self, other: 'Rect') -> bool:
        """Do they share some area (touching edges do not count)?"""
        return self.left < other.right and other.left < self.right and self.top < other.bottom and other.top < self.bottom

    def touches(self, other: 'Rect') -> bool:
        """Do they share part of an edge without overlapping?"""
        if self.overlaps(other):
            return False
        side = (self.right == other.left or other.right == self.left) and self.top < other.bottom and other.top < self.bottom
        level = (self.bottom == other.top or other.bottom == self.top) and self.left < other.right and other.left < self.right
        return side or level

    def crosses(self, other: 'Rect') -> bool:
        """A plus sign: one is wider, the other taller, and each sticks out of the other."""
        return ((self.left < other.left and other.right < self.right and other.top < self.top and self.bottom < other.bottom)
                or (other.left < self.left and self.right < other.right and self.top < other.top and other.bottom < self.bottom))


@dataclass
class Drawing:
    """A program's drawing, read from its EJUDGE_MODE output."""
    shapes: List[Shape]
    ticks: int
    stray: List[str]

    def only(self, *names: str) -> List[Shape]:
        """Shapes by kind (``'rect'``) or by name (``'filled_rect'``)."""
        return [s for s in self.shapes if s.kind in names or s.name in names]

    def without(self, *names: str) -> List[Shape]:
        return [s for s in self.shapes if s.kind not in names and s.name not in names]

    def last_frame(self) -> List[Shape]:
        """What is on the screen at the end: shapes after the last clear() or opaque fill()."""
        start = 0
        for i, s in enumerate(self.shapes):
            if s.kind == 'clear' or (s.kind == 'fill' and s.alpha == 255):
                start = i
        return self.shapes[start:]


def _color(raw) -> Tuple[Tuple[int, int, int], Optional[int]]:
    if raw is None:
        return (0, 0, 0), None
    raw = list(raw)
    return (int(raw[0]), int(raw[1]), int(raw[2])), (int(raw[3]) if len(raw) > 3 else None)


def parse(text: str) -> Drawing:
    """The shapes a program printed. Lines that are not drawing are kept in ``stray``."""
    shapes: List[Shape] = []
    stray: List[str] = []
    ticks = 0
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except ValueError:
            stray.append(line)
            continue
        if not isinstance(data, dict):
            stray.append(line)
            continue
        if 'cmd' in data:
            if data['cmd'] in ('tick', 'sleep'):
                ticks += 1
            continue
        kind = data.get('figure')
        if not kind:
            stray.append(line)
            continue
        color, own_alpha = _color(data.get('color'))
        alpha = own_alpha if own_alpha is not None else int(data.get('alpha', 255))
        s = Shape(kind=kind, color=color, alpha=alpha, width=data.get('line_width'), index=len(shapes),
                  frame=ticks, raw=data)
        if kind == 'line':
            s.points = [tuple(data['start']), tuple(data['end'])]
        elif kind == 'circle':
            s.center = tuple(data['pos'])
            s.radius = data['radius']
        elif kind in ('rect', 'ellipse', 'arc'):
            s.box = tuple(data['rect'])
            if kind == 'rect':
                s.points = list(s.rectangle().corners)
        elif kind == 'polygon':
            s.points = [tuple(p) for p in data['points']]
        elif kind == 'text':
            s.text = data.get('text', '')
            s.center = tuple(data['pos'])
            s.size = data.get('fontsize', 0)
        shapes.append(s)
    return Drawing(shapes, ticks, stray)


# ---------------------------------------------------------------- colors

BLACK, WHITE, RED, GREEN, BLUE, YELLOW = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)

_NAMES = {
    (0, 0, 0): 'black', (255, 255, 255): 'white', (255, 0, 0): 'red', (0, 255, 0): 'green',
    (0, 0, 255): 'blue', (255, 255, 0): 'yellow', (165, 42, 42): 'brown',
}


def color_name(color) -> str:
    color = tuple(color[:3])
    return _NAMES.get(color, '(%d, %d, %d)' % color)


def same_color(a, b, tolerance: int = 100) -> bool:
    """Near enough to count as the colour asked for: each channel within ``tolerance``."""
    return all(abs(x - y) <= tolerance for x, y in zip(a[:3], b[:3]))


# ---------------------------------------------------------------- geometry

EPS = 1e-9


def sub(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1])


def cross(a: Point, b: Point) -> float:
    return a[0] * b[1] - a[1] * b[0]


def dot(a: Point, b: Point) -> float:
    return a[0] * b[0] + a[1] * b[1]


def dist(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def area(polygon: Polygon) -> float:
    """The polygon's area (vertices in either order)."""
    n = len(polygon)
    return abs(sum(cross(polygon[i], polygon[(i + 1) % n]) for i in range(n))) / 2


def is_triangle(points: Polygon) -> bool:
    return len(points) == 3 and abs(cross(sub(points[1], points[0]), sub(points[2], points[0]))) > EPS


def is_rectangle(points: Polygon) -> bool:
    """Four vertices, in order, with right angles (any rotation)."""
    if len(points) != 4:
        return False
    for i in range(4):
        a, b, c = points[i - 1], points[i], points[(i + 1) % 4]
        if dist(a, b) < EPS or abs(dot(sub(a, b), sub(c, b))) > EPS:
            return False
    return True


def is_square(points: Polygon) -> bool:
    return is_rectangle(points) and abs(dist(points[0], points[1]) - dist(points[1], points[2])) < EPS


def axis_rect(points: Polygon) -> Optional[Rect]:
    """The rectangle, if these four points are an axis-parallel one."""
    if not is_rectangle(points):
        return None
    xs = sorted({p[0] for p in points})
    ys = sorted({p[1] for p in points})
    if len(xs) != 2 or len(ys) != 2:
        return None
    return Rect(xs[0], ys[0], xs[1], ys[1])


def center_of(points: Polygon) -> Point:
    """The centre of a rectangle or square: where its diagonals meet."""
    return ((points[0][0] + points[2][0]) / 2, (points[0][1] + points[2][1]) / 2)


def on_segment(p: Point, a: Point, b: Point) -> bool:
    return (abs(cross(sub(b, a), sub(p, a))) <= EPS
            and min(a[0], b[0]) - EPS <= p[0] <= max(a[0], b[0]) + EPS
            and min(a[1], b[1]) - EPS <= p[1] <= max(a[1], b[1]) + EPS)


def segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    """Do the closed segments ab and cd share a point?"""
    d1, d2 = cross(sub(b, a), sub(c, a)), cross(sub(b, a), sub(d, a))
    d3, d4 = cross(sub(d, c), sub(a, c)), cross(sub(d, c), sub(b, c))
    if ((d1 > EPS and d2 < -EPS) or (d1 < -EPS and d2 > EPS)) and ((d3 > EPS and d4 < -EPS) or (d3 < -EPS and d4 > EPS)):
        return True
    return on_segment(c, a, b) or on_segment(d, a, b) or on_segment(a, c, d) or on_segment(b, c, d)


def segments_cross(a: Point, b: Point, c: Point, d: Point) -> bool:
    """Do ab and cd cross at a point inside both (not just touch)?"""
    d1, d2 = cross(sub(b, a), sub(c, a)), cross(sub(b, a), sub(d, a))
    d3, d4 = cross(sub(d, c), sub(a, c)), cross(sub(d, c), sub(b, c))
    return d1 * d2 < -EPS and d3 * d4 < -EPS


def parallel(a: Point, b: Point, c: Point, d: Point) -> bool:
    return abs(cross(sub(b, a), sub(d, c))) <= EPS


def edges(polygon: Polygon) -> Iterable[Tuple[Point, Point]]:
    n = len(polygon)
    for i in range(n):
        yield polygon[i], polygon[(i + 1) % n]


def point_in_polygon(p: Point, polygon: Polygon, boundary: bool = True) -> bool:
    """Is the point inside (or, with ``boundary``, on the border)?"""
    for a, b in edges(polygon):
        if on_segment(p, a, b):
            return boundary
    inside = False
    for a, b in edges(polygon):
        if (a[1] > p[1]) != (b[1] > p[1]):
            x = a[0] + (p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x > p[0]:
                inside = not inside
    return inside


def polygon_inside(inner: Polygon, outer: Polygon) -> bool:
    """Is ``inner`` within ``outer`` (borders may touch)?"""
    if not all(point_in_polygon(p, outer) for p in inner):
        return False
    return not any(segments_cross(a, b, c, d) for a, b in edges(inner) for c, d in edges(outer))


def polygons_overlap(p: Polygon, q: Polygon) -> bool:
    """Do they share some area or border?"""
    if any(segments_intersect(a, b, c, d) for a, b in edges(p) for c, d in edges(q)):
        return True
    return point_in_polygon(p[0], q) or point_in_polygon(q[0], p)


def segment_distance(p: Point, a: Point, b: Point) -> float:
    ab = sub(b, a)
    length = dot(ab, ab)
    if length < EPS:
        return dist(p, a)
    t = max(0.0, min(1.0, dot(sub(p, a), ab) / length))
    return dist(p, (a[0] + t * ab[0], a[1] + t * ab[1]))


def point_in_circle(p: Point, center: Point, radius: float) -> bool:
    return dist(p, center) <= radius + EPS


def polygon_in_circle(polygon: Polygon, center: Point, radius: float) -> bool:
    return all(point_in_circle(p, center, radius) for p in polygon)


def circle_in_polygon(center: Point, radius: float, polygon: Polygon) -> bool:
    return point_in_polygon(center, polygon) and all(segment_distance(center, a, b) >= radius - EPS for a, b in edges(polygon))


def polygon_circle_overlap(polygon: Polygon, center: Point, radius: float) -> bool:
    """Do a polygon and a disc share some area?"""
    return point_in_polygon(center, polygon) or any(segment_distance(center, a, b) < radius for a, b in edges(polygon))


def circles(a: Shape, b: Shape) -> str:
    """How two circles lie: ``inside``, ``touch_inside``, ``outside``, ``touch_outside`` or ``cross``."""
    d = dist(a.center, b.center)
    if d > a.radius + b.radius + EPS:
        return 'outside'
    if abs(d - (a.radius + b.radius)) <= EPS:
        return 'touch_outside'
    if d < abs(a.radius - b.radius) - EPS:
        return 'inside'
    if abs(d - abs(a.radius - b.radius)) <= EPS:
        return 'touch_inside'
    return 'cross'


def covers(shape: Shape, p: Point) -> bool:
    """Does a filled shape paint this point?"""
    if shape.kind == 'circle':
        return point_in_circle(p, shape.center, shape.radius)
    if shape.kind == 'ellipse':
        x, y, w, h = shape.box
        rx, ry = w / 2, h / 2
        return rx > 0 and ry > 0 and ((p[0] - x - rx) / rx) ** 2 + ((p[1] - y - ry) / ry) ** 2 <= 1 + EPS
    polygon = shape.polygon()
    return polygon is not None and point_in_polygon(p, polygon)


def samples(polygon: Polygon, step: float = 4) -> List[Point]:
    """Points that stand for a polygon's area: its vertices, edges and a grid inside."""
    points = list(polygon)
    for a, b in edges(polygon):
        n = max(1, int(dist(a, b) // step))
        points += [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n)]
    xs = [p[0] for p in polygon]
    ys = [p[1] for p in polygon]
    y = min(ys)
    while y <= max(ys):
        x = min(xs)
        while x <= max(xs):
            if point_in_polygon((x, y), polygon):
                points.append((x, y))
            x += step
        y += step
    return points


def paints(shape: Shape, p: Point) -> bool:
    """Does this shape put its colour on this point, outline shapes included?"""
    if shape.kind in ('fill', 'clear'):
        return True
    w = shape.width or 0
    if shape.kind == 'line':
        return w >= 1 and segment_distance(p, *shape.points) <= w / 2
    if shape.filled:
        return covers(shape, p)
    if shape.kind == 'circle':
        d = dist(p, shape.center)
        return shape.radius - w <= d <= shape.radius
    if shape.kind == 'rect':
        r = shape.rectangle()
        inside = r.left <= p[0] <= r.right and r.top <= p[1] <= r.bottom
        core = r.left + w < p[0] < r.right - w and r.top + w < p[1] < r.bottom - w
        return inside and not core
    if shape.kind == 'polygon':
        return any(segment_distance(p, a, b) <= w / 2 for a, b in edges(shape.points))
    return False


def color_at(shapes: Sequence[Shape], p: Point, background=(0, 0, 0)) -> Tuple[int, int, int]:
    """The colour the finished picture has at a point (shapes see-through below alpha 128)."""
    color = tuple(background)
    for shape in shapes:
        if shape.kind == 'clear':
            color = (0, 0, 0)
        elif shape.kind in ('text', 'image', 'arc', 'ellipse') and not shape.filled:
            continue
        elif shape.alpha >= 128 and paints(shape, p):
            color = shape.color
    return color


# ------------------------------------------------- what problems share

def fill_first(drawing: Drawing) -> List[Shape]:
    """The shapes without a background fill, which may only come first."""
    for s in drawing.shapes[1:]:
        if s.kind == 'fill':
            raise Wrong(say('Remove the extra fill(): only the background may be filled, at the start.',
                            'Удали лишнюю заливку fill!'))
    return [s for s in drawing.shapes if s.kind != 'fill']


def only(shapes: Sequence[Shape], *names: str) -> None:
    """Every shape is one of these (by kind or by name)."""
    for s in shapes:
        if s.kind not in names and s.name not in names:
            raise Wrong(say(f'There is an extra shape: {s.name}. Remove it.',
                            f'Вижу лишние фигуры ({s.name})! Их нужно удалить!'))


def count(items: Sequence, expected: int, what_en: str, what_ru: str) -> None:
    if len(items) < expected:
        raise Wrong(say(f'Too few {what_en}: {len(items)} instead of {expected}.',
                        f'{what_ru}: меньше, чем нужно ({len(items)} вместо {expected})!'))
    if len(items) > expected:
        raise Wrong(say(f'Too many {what_en}: {len(items)} instead of {expected}.',
                        f'{what_ru}: больше, чем нужно ({len(items)} вместо {expected})!'))


def as_rect(shape: Shape, upright: bool = True) -> Rect:
    """A filled_rect, or a four-point polygon that is a rectangle, as a Rect."""
    if shape.kind == 'rect':
        return shape.rectangle()
    if shape.kind != 'polygon':
        raise Wrong(say(f'Only rectangles are wanted here, not {shape.name}.',
                        f'Здесь нужны только прямоугольники, а не {shape.name}!'))
    if len(shape.points) != 4:
        raise Wrong(say('A rectangle needs four vertices.', 'Для прямоугольника нужно задать 4 вершины!'))
    if not is_rectangle(shape.points):
        raise Wrong(say('This polygon is not a rectangle.', 'Нарисован многоугольник, не являющийся прямоугольником!'))
    r = axis_rect(shape.points)
    if r is None:
        if upright:
            raise Wrong(say('Rectangles must be upright: horizontal or vertical.',
                            'Прямоугольник должен быть вертикальным либо горизонтальным!'))
        xs, ys = [p[0] for p in shape.points], [p[1] for p in shape.points]
        r = Rect(min(xs), min(ys), max(xs), max(ys))
    return r


def colour_wrong(shape: Shape, wanted) -> Wrong:
    return Wrong(say(f'Wrong colour: {shape.name} should be {color_name(wanted)}.',
                     f'Неверные цвета! {shape.name} должен быть цвета {color_name(wanted)}'))


def near(a: float, b: float, tolerance: float = 1) -> bool:
    return abs(a - b) <= tolerance


def pixel(value: float) -> int:
    """How drawzero rounds a coordinate onto the canvas."""
    return int(value + 0.5)


def has_segment(lines: Sequence[Shape], a: Point, b: Point, tolerance: float = 1) -> bool:
    """Is there a line from a to b (either way), each end within ``tolerance`` pixels?"""
    def close(p, q):
        return abs(p[0] - q[0]) <= tolerance and abs(p[1] - q[1]) <= tolerance
    return any((close(l.points[0], a) and close(l.points[1], b)) or (close(l.points[0], b) and close(l.points[1], a))
               for l in lines)


def numbers(text: str) -> List[int]:
    """The integers of a test's input."""
    return [int(x) for x in text.split()]


# ---------------------------------------------------------------- ejudge

def read(path: str) -> str:
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read()


def run(check: Callable[[Drawing, str, Optional[str]], Optional[str]], argv: Sequence[str],
        allow_print: bool = False) -> Tuple[int, str]:
    if len(argv) < 3:
        return CHECK_FAILED, 'usage: check INPUT OUTPUT [ANSWER]'
    test_input = read(argv[1])
    answer = read(argv[3]) if len(argv) > 3 else None
    drawing = parse(read(argv[2]))
    if drawing.stray and not allow_print:
        return WRONG_ANSWER, say('The program should only draw, not print: ' + drawing.stray[0][:80],
                                 'Программа должна только рисовать, а не печатать: ' + drawing.stray[0][:80])
    if not drawing.shapes:
        return WRONG_ANSWER, say('Nothing is drawn.', 'Ничего не нарисовано.')
    try:
        message = check(drawing, test_input, answer)
    except Wrong as e:
        return WRONG_ANSWER, e.message
    return OK, message or say('Right!', 'Верно!')


def main(check: Callable[[Drawing, str, Optional[str]], Optional[str]], argv: Optional[Sequence[str]] = None,
         allow_print: bool = False) -> int:
    """Run ``check`` as an ejudge checker; returns the exit code."""
    argv = sys.argv if argv is None else argv
    try:
        code, message = run(check, argv, allow_print)
    except Exception:  # noqa: BLE001 - a checker crash must be a check failure, never OK
        traceback.print_exc(file=sys.stdout)
        code, message = CHECK_FAILED, 'the checker crashed'
    print(message)
    sys.stdout.flush()
    return code
