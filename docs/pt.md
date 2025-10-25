# Pt helper reference

The `Pt` class is a small helper that acts both like a 2D point and like a very light turtle.  
It lives in [`drawzero.utils.pt`](../src/drawzero/utils/pt.py) and is imported for you when you write `from drawzero import *`.
Use `Pt` whenever you want to store a position, move it around, and pass it into the drawing helpers from
[Drawing primitives](primitives.md) or [Animations](animation.md).

This page explains the full `Pt` API in simple language, with many short examples that you can copy into
an interactive shell or one of the example scripts.

## Quick import and first steps

```python
from drawzero import *

point = Pt()          # (0, 0) facing east (heading = 0°)
other = Pt(200, 150)  # x=200, y=150
```

`Pt` stores three values:

* `x` – horizontal coordinate (0 is the left edge of the canvas).
* `y` – vertical coordinate (0 is the top edge).
* `heading` – direction in degrees. `0` means “pointing right”, `90` means “pointing up”.

All drawing helpers accept a `Pt` object anywhere they expect a coordinate pair. For example:

```python
from drawzero import *

center = Pt(500, 400)
point = Pt(200, 200)

filled_circle('gold', center, 80)
line('black', point, center)  # `line` reads the `(x, y)` from each Pt
```

## Creating and reading points

### Constructors

```python
Pt()
Pt(x_value, y_value)
Pt(x_value, y_value, heading=degrees)
```

* All numbers can be integers or floats.
* If you leave `heading` out, DrawZero assumes `0` degrees.

### Getting the stored values

```python
point = Pt(120, 345, heading=30)

point.x        # 120
point.y        # 345
point.heading  # 30

point.pos()       # (120.0, 345.0)
point.position()  # same as pos()
point.xcor()      # 120.0
point.ycor()      # 345.0
```

The `xcor`/`ycor` helpers round the values to 10 decimal places so the output stays tidy in the console.

## Vector-style arithmetic

`Pt` behaves like a mutable 2D vector. You can add, subtract, and scale points without writing your own loops.
Each operation creates a new `Pt` unless it ends with `=` (like `+=`).

```python
start = Pt(50, 20)
offset = Pt(10, -5)

result = start + offset   # Pt(60, 15, heading=0.0)
start += offset           # start is now Pt(60, 15, heading=0.0)
mirror = -offset          # Pt(-10, 5, heading=0.0)
```

Scaling works with plain numbers:

```python
point = Pt(5, 8)
print(point * 3)     # Pt(15, 24, heading=0.0)
print(2 * point)     # Pt(10, 16, heading=0.0)
print(point / 2)     # Pt(2.5, 4.0, heading=0.0)
```

When you need only the length of the vector, call `abs(point)`.

```python
hyp = Pt(3, 4)
print(abs(hyp))  # 5.0
```

### Copying and unpacking

Use `.copy()` to duplicate the point while keeping the original intact.

```python
head = Pt(100, 100)
shadow = head.copy()
head.forward(50)
# `shadow` still remembers the old coordinates
```

`Pt` also supports unpacking and indexing:

```python
p = Pt(7, 9)

x, y = p        # iterates over x then y
p[0]            # 7
p[1]            # 9
p[:2]           # [7, 9]
len(p)          # always 2
```

## Turtle-style movement

`Pt` keeps a heading angle and can move in that direction. This is perfect for drawing polygons or animation paths.

```python
walker = Pt()
walker.forward(100)   # moves along heading (initially east)
walker.right(90)
walker.forward(50)
print(walker.pos())   # (100.0, 50.0)
```

Key methods and their aliases:

| Action | Preferred name | Aliases |
| --- | --- | --- |
| Move forward | `forward(distance)` | `fd(distance)` |
| Move backward | `backward(distance)` | `back(distance)`, `bk(distance)` |
| Turn right | `right(angle)` | `rt(angle)` |
| Turn left | `left(angle)` | `lt(angle)` |
| Set heading directly | `setheading(angle)` | `seth(angle)` |
| Reset to origin | `reset()` or `home()` | — |

Headings always wrap to the range `[0, 360)`.

### Example – regular polygon helper

```python
from drawzero import *
from math import sin, pi

def regular_polygon(center, sides, radius):
    corner = Pt(center.x, center.y - radius)
    corner.setheading(0)
    angle = 360 / sides
    vertices = []
    for _ in range(sides):
        vertices.append(corner.pos())
        corner.right(angle)
        corner.forward(2 * radius * sin(pi / sides))
    polygon('white', vertices)

regular_polygon(Pt(300, 300), sides=6, radius=120)
```

`polygon` comes from [Drawing primitives](primitives.md). `Pt` supplies the vertex coordinates.

## Absolute moves and rotations

Sometimes you need to jump to a location or rotate around another point.

* `goto(x, y)` / `setpos(...)` / `setposition(...)` – move to exact coordinates without changing heading.
* `rotate_around(angle, pivot)` – spin around another `Pt`, tuple, or list.
* `move_towards(distance, target)` – move a fixed distance in the direction of another point.

```python
p = Pt(100, 100)
p.goto(400, 200)           # -> Pt(400, 200, heading=0.0)
p.rotate_around(90, (200, 200))  # pivot around absolute point
p.move_towards(50, Pt(200, 500))
```

`rotate_around` rotates counter-clockwise when the angle is positive. If you need the shortest path towards a target, `move_towards`
combines the direction and step size for you.

## Distance and angle helpers

```python
p = Pt(0, 0)
q = Pt(30, 40)

p.distance(q)      # 50.0
p.towards(q)       # 53.1301023542 degrees
p.is_left_of(10)   # True because 0 < 10
p.is_right_of(-5)  # True because 0 > -5
```

Comparison helpers use the canvas axes:

* `is_above(y_value)` returns `True` if the point is higher on the screen (smaller `y`).
* `is_below(y_value)` returns `True` if the point is lower on the screen (larger `y`).
* `is_left_of(x_value)` returns `True` if `x` is smaller.
* `is_right_of(x_value)` returns `True` if `x` is larger.

Use them to keep sprites within bounds:

```python
ball = Pt(500, -10, heading=90)
if ball.is_above(0):
    ball.flip_vertically()  # bounce from the top edge
```

`flip_vertically()` and `flip_horizontally()` mirror the heading without changing the position. This is handy for collision logic in small games.

## Working with drawing helpers

Most drawing helpers accept `Pt` objects directly. You can mix plain tuples and points in the same call.

```python
from drawzero import *

start = Pt(150, 150)
end = Pt(600, 300)

line('cyan', start, end)
rect('orange', start, 200, 120)
filled_circle('white', end, 40)
```

For shapes that expect a list of vertices (like `polygon` or `filled_polygon`), call `.pos()` on each `Pt`.

```python
triangle = [Pt(400, 200), Pt(300, 450), Pt(500, 450)]
polygon('white', [p.pos() for p in triangle])
```

To connect the dots with animation, combine this page with [Animations](animation.md) and the
`tick()` call shown there.

## Using Pt inside loops and animations

`Pt` shines when you update positions every frame. The example below creates a simple orbit.

```python
from drawzero import *

center = Pt(500, 500)
planet = Pt(650, 500)
planet.setheading(90)

while tick():
    clear()
    filled_circle('navy', center, 40)
    filled_circle('orange', planet, 20)
    planet.rotate_around(3, center)
```

Read [Examples overview](examples_overview.md) and open `05_points.py` or `09_animation_rectangles.py` to see longer scripts that use these methods together.

## Troubleshooting tips

* **Movement looks wrong?** Remember that the screen origin `(0, 0)` is the top-left corner. Moving “up” means decreasing `y`.
* **Heading jumps unexpectedly?** Check if you used `backward()` or `forward()` with negative numbers. Both change the point but keep the heading.
* **`distance` returns a float with many decimals.** That is normal. Use `round(value, 2)` when printing if you want fewer digits.
* **Need to reset everything?** Call `reset()` or `home()` to set `(x, y)` to `(0, 0)` and `heading` to `0`.

## Where to go next

* [Drawing primitives](primitives.md) – shapes and text helpers that happily accept `Pt` objects.
* [Animations](animation.md) – how to redraw every frame and schedule updates with `tick()`.
* [Gradient helper](gradient.md) – smooth color transitions that go well with moving points.
* [Examples overview](examples_overview.md) – table of scripts, including the ones that focus on `Pt`.

Experiment with the snippets above, then mix `Pt` with the other utilities to build your own scenes.
