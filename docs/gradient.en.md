# Gradient helper reference

`Gradient` is a class that turns a number into a color.
It is available as soon as you write `from drawzero import *`.
Use it when you need smooth color transitions for temperature maps, progress bars, particle systems, or animated trails.

This guide also shows how to combine gradients with shapes from [Drawing primitives](primitives.md), transparency tips from
[Transparency and line width](transparency_and_line_width.md), and animated loops from [Animations](animation.md).

## Quick start

```python
from drawzero import *

heat = Gradient([C.blue, C.cyan, C.yellow, C.red])
print(heat(0.0))   # (0, 0, 255) - first color
print(heat(0.5))   # (0, 255, 255) - middle color
print(heat(1.0))   # (255, 0, 0) - last color
```

* The first argument is a list of colors. You can mix constants from `C`, named strings (`'gold'`), or RGB tuples like `(34, 139, 34)`.
* By default the valid input range (the **domain**) goes from `0` to `1`.
* Passing a value smaller than the start clamps to the first color; bigger values clamp to the last color.

## Why gradients are useful

* **Continuous shading** – draw rectangles that fade from cold to hot numbers.
* **Animated effects** – change particle colors as they age.
* **Status bars** – map progress (0–100) to a palette.

Open the example [`13_gradients.py`](https://github.com/ShashkovS/drawzero/blob/master/src/drawzero/examples/13_gradients.py) after reading this page. The file is also listed in the [Examples overview](examples_overview.md).

## Constructing a gradient

```
Gradient(color_list, start=0.0, end=1.0, *extra_domain_points)
```

* `color_list` must have at least two entries.
* If you pass only `start` and `end`, the helper spreads the colors evenly across that range.
* When you supply extra numbers, the helper sorts them automatically. The final domain always has the same length as `color_list`.

### Evenly spaced domain

```python
heat = Gradient([C.blue, C.white, C.red], 0, 100)
print(heat(0))     # blue
print(heat(50))    # white
print(heat(100))   # red
```

The colors sit at 0, 50, and 100 because the list has three entries.

### Custom positions for each color

```python
mist = Gradient([C.black, 'purple', C.white], 0, 30, 100)
print(mist(10))   # dark purple
print(mist(60))   # pale purple near white
```

Here the palette stays dark longer because the middle color is close to the start of the domain.

### Using raw RGB tuples

```python
sunrise = Gradient([(25, 25, 112), (255, 140, 0), (255, 215, 0)], -1, 1)
```

Any number outside `[-1, 1]` will clamp to the first or last tuple.

### Validation rules

If the domain points do not match the number of colors, `Gradient` raises `BadDrawParmsError`.  
The message suggests a fixed call such as `Gradient([C.red, C.green], 0, 100)`.

## Sampling colors inside drawings

`Gradient` objects are callable. You can pass the result straight into the drawing helpers.

```python
from drawzero import *

glow = Gradient([C.black, C.blue, C.cyan, C.white])

for index in range(10):
    color = glow(index / 9)   # 0.0 .. 1.0
    filled_circle(color, (500, 500), 40 + index * 15)
```

Combine this with alpha values from [Transparency and line width](transparency_and_line_width.md) to create soft halos.

### Heat map rectangle grid

```python
from drawzero import *

heat = Gradient([C.darkblue, C.lawngreen, C.yellow, C.orangered], 0, 30)
cell_size = 80

for row in range(5):
    for col in range(5):
        value = row * 5 + col  # pretend sensor reading
        color = heat(value)
        filled_rect(color, (100 + col * cell_size, 100 + row * cell_size), cell_size, cell_size)
        text('white', f"{value}", (110 + col * cell_size, 110 + row * cell_size))
```

The helper clamps any number above `30` to the last color (`C.orangered`).

## Mapping animation progress to colors

Gradients pair very well with the `tick()` loop from [Animations](animation.md).

```python
from drawzero import *

trail = Gradient([C.white, C.skyblue, C.blue, C.navy])
ball = Pt(200, 500, heading=0)

while tick():
    clear()
    for tail in range(20):
        color = trail(tail / 19)
        filled_circle(color, (ball.x - tail * 12, ball.y), 20 - tail)
    ball.forward(5)
    if ball.x > 1000:
        ball.goto(0, ball.y)
```

The gradient gives darker colors for older trail segments while the point keeps moving.

## Understanding interpolation

Between two domain values the helper blends color channels linearly:

```
channel = left_channel * (right_x - current_x) / diff + right_channel * (current_x - left_x) / diff
```

Each channel (`R`, `G`, `B`) is rounded to the nearest integer.  
You normally do not need to worry about this math, but it helps explain why gradients produce smooth steps even when the domain spacing is uneven.

## Tips and troubleshooting

* **Domain must be sorted.** The helper sorts your numbers automatically, but passing mixed strings and numbers triggers an error message.
* **Short palettes need matching domain length.** Two colors work with two domain points. Three colors need three points, and so on.
* **Re-use gradients.** Store the object once (e.g. `heat = Gradient(...)`) and call it many times per frame instead of creating new gradients inside loops.
* **Combine with alpha.** Use the `alpha` keyword from [Transparency and line width](transparency_and_line_width.md) to fade shapes even more.
* **Test in the shell.** Gradients have a readable `repr`, so printing them helps during debugging.

```python
heat = Gradient([C.blue, C.white, C.red], 0, 100)
print(heat)
# Gradient([(0, 0, 255), (255, 255, 255), (255, 0, 0)], 0, 50.0, 100)
```

## Where to read more

* [Drawing primitives](primitives.md) – shows every function that accepts colors.
* [Pt helper](pt.md) – use moving points together with gradients for animated trails.
* [Examples overview](examples_overview.md) – find `13_gradients.py` plus other scripts that mix gradients with motion.
* [Architecture notes](architecture.md) – quick summary of how utility helpers (including `Gradient`) fit into the project.

Try creating your own palette, then feed its colors into shapes, particle effects, or HUD elements. Small experiments make the gradient rules stick quickly.
