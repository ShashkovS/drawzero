# Transparency (`alpha`) and line thickness (`line_width`)

Many DrawZero helpers accept two optional parameters: `alpha` for transparency and `line_width` for stroke thickness. This page explains what they do, when to use them, and how to avoid common mistakes. The tone stays simple so that learners with basic English can still follow the ideas.

## Why these parameters matter

* `alpha` controls how much the background shows through your drawing. Lower values make the object look lighter or ghost-like. Higher values make it solid.
* `line_width` controls how thick the outline of a shape or line appears. Thin lines are great for details. Thick lines help emphasize borders or UI panels.

Together, these parameters let you build depth, focus, and style in your sketches.

## Quick reference

| Parameter | Works with | Default value | Allowed values |
|-----------|------------|----------------|----------------|
| `alpha` | `line`, `circle`, `filled_circle`, `rect`, `filled_rect`, `ellipse`, `filled_ellipse`, `arc`, `polygon`, `filled_polygon`, `rect_rotated`, `filled_rect_rotated`, `fill`, `image` | `255` | Any integer from `0` to `255` |
| `line_width` | Outline helpers such as `line`, `circle`, `rect`, `ellipse`, `arc`, `polygon`, `rect_rotated` | `4` (virtual units, roughly 4 pixels on the default 1000×1000 canvas) | Non-negative integers. Use `0` to fill shapes through the outline helper. |

> 💡 Filled helpers (`filled_circle`, `filled_rect`, and so on) already set `line_width=0` internally, so you usually do not need to pass it yourself.

## Understanding `alpha` {#understanding-alpha}

`alpha` measures opacity on a scale from `0` (fully transparent) to `255` (fully opaque). DrawZero rounds the value to an integer, so pass whole numbers.

| Value | Visual result |
|-------|----------------|
| `0` | The object becomes invisible. Good for hiding elements without deleting code. |
| `64` | Very light ghost of the original color. Useful for shadows and planning guides. |
| `128` | Half-transparent. Background is clearly visible through the object. |
| `192` | Mostly solid with a soft edge. Great for highlights. |
| `255` | Fully solid. Default setting. |

### Layered example – glowing button

```python
from drawzero import *

fill((20, 20, 35))
base = (500, 500)
filled_circle('#4caf50', base, 120, alpha=220)
filled_circle('#81c784', base, 90, alpha=160)
filled_circle('white', base, 60, alpha=90)
text('white', 'PLAY', base, 48, '.^')
```

Each circle uses a different alpha value. The background shines through the outer rings, creating a glow effect.

### Example – glass window using shapes

```python
from drawzero import *

fill('#202840')
rect('white', (150, 200), 700, 500, line_width=12)
filled_rect('#90caf9', (150, 200), 700, 500, alpha=120)
line('white', (150, 450), (850, 450), alpha=160, line_width=6)
line('white', (500, 200), (500, 700), alpha=160, line_width=6)
```

The rectangle outline stays solid, while the inner filled rectangle uses a medium alpha to look like glass.

### Example – fading image copies

```python
from drawzero import *

fill('black')
for layer, opacity in enumerate(range(200, 40, -40)):
    image('runner.png', (200 + layer * 60, 420), width=220, alpha=opacity)
```

This snippet combines `image()` with different alpha values to show a runner leaving a trail. For more details about the `image()` helper, read [Working with images](images.md).

### Tips for using `alpha`

* Keep alpha values between `30` and `80` for soft shadows and between `120` and `200` for glow or UI overlays.
* When stacking several transparent layers, start drawing from the darkest background to the lightest foreground.
* `alpha` multiplies any transparency already stored in a PNG image. A semi-transparent pixel with per-pixel alpha `128` becomes even lighter if you call `image(..., alpha=128)`.
* Passing `None` or leaving the argument out uses the default value `255`.
* Values outside the range raise a `BadDrawParmsError`. Double-check that your code produces integers.

## Understanding `line_width`

`line_width` describes how thick the outline of a primitive should be. The value is measured in virtual canvas units. On the default 1000×1000 canvas, one unit is roughly one pixel.

| `line_width` | Visual style |
|--------------|--------------|
| `1`–`2` | Very thin lines for delicate details or sketch guides. |
| `3`–`6` | Standard outlines. The default `4` lives here. |
| `8`–`12` | Heavy borders for panels, speech bubbles, or map outlines. |
| `20` and above | Bold graphic style. Useful for cartoon shadows or timelines. |
| `0` | Special case. The shape becomes filled because the outline has no width. |

### Example – using different line widths on circles

```python
from drawzero import *

fill('black')
for step, width in enumerate([2, 4, 8, 16]):
    circle('cyan', (200 + step * 150, 500), 60, line_width=width)
    text('white', f'line_width={width}', (200 + step * 150, 620), 24, '.^')
```

The four circles let you compare how the outline grows as `line_width` increases.

### Example – drawing a filled shape through the outline helper

```python
from drawzero import *

fill('#263238')
rect('orange', (250, 250), 500, 300, line_width=0, alpha=220)
```

Setting `line_width=0` tells the renderer to fill the rectangle. This is how the convenience helper `filled_rect()` works internally.

### Example – precise outlines with polygons

```python
from drawzero import *

fill('#0d1b2a')
points = [(200, 800), (500, 200), (800, 800)]
polygon('#e0e1dd', *points, line_width=6)
polygon('#778da9', *points, line_width=2, alpha=160)
```

The first polygon creates a thick border, and the second one on top adds a thin highlight with partial transparency.

### Tips for using `line_width`

* Use the same `line_width` across related elements (for example, all buttons) to keep a consistent style.
* When drawing animations, cache the chosen value in a variable so it stays constant frame to frame.
* Large `line_width` values need extra space around the shape. Make sure your coordinates leave padding so the stroke is not cut off by the canvas edge.
* Negative values are not allowed. If you calculate the width, wrap it in `max(0, value)` to avoid mistakes.

## Mixing `alpha` and `line_width`

These parameters can work together for polished designs.

```python
from drawzero import *

fill('#1a1a1a')
outer = (150, 150)
inner = (250, 250)
rect('#ff9800', outer, 700, 700, line_width=14, alpha=220)
rect('#ffc107', inner, 500, 500, line_width=6, alpha=140)
filled_rect('#ffffff', (320, 420), 360, 200, alpha=30)
text('white', 'Mission Briefing', (500, 360), 42, '.^')
```

The outer rectangle has a thick, almost solid stroke. The inner rectangle uses a thinner, more transparent line to add depth. The semi-transparent filled rectangle creates a readable panel.

## Troubleshooting checklist

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Shape looks the same after changing `alpha`. | The helper you used does not accept `alpha` (for example, `text()`). | Check the documentation of that helper. If it lacks `alpha`, draw the text on top of a semi-transparent shape instead. |
| Stroke looks blurry. | The line width is very large for a small shape. | Reduce `line_width` or increase the shape size. |
| `BadDrawParmsError: bad alpha`. | The value was outside `0`–`255` or not a number. | Clamp the number or convert it with `int()`. |
| `BadDrawParmsError: bad width`. | `line_width` was negative or not numeric. | Ensure you pass a non-negative integer. |
| Transparent layers disappear in random order. | You draw the brightest elements first. Later opaque shapes cover them. | Draw the darkest background first, then lighter transparent layers, then solid highlights. |

With these guidelines you can choose `alpha` and `line_width` values confidently and make your drawings look professional.
