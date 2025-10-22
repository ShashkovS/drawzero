# Drawing primitives

This page shows how to use the most common drawing helpers in DrawZero.
The goal is to help you make nice sketches even if you are new to programming.
We will focus on color names, points, and shapes. Read [Transparency (`alpha`) and line thickness (`line_width`)](transparency_and_line_width.md) when you want to control see-through effects or stroke sizes.

Once you feel comfortable drawing static shapes, jump to the [Animations guide](animation.md).
It explains how to put your drawings inside the frame loop, control the speed with `tick()`, and even make motion trails.

Each example starts with the same import:

```python
from drawzero import *
```

After the import you can call the functions one by one. The virtual canvas is 1000 by 1000 units. Coordinates are always written as `(x, y)`.

## Named colors for quick sketches

You can pass the color as a short text such as `'red'`, `'white'`, `'black'`, `'gold'`, `'skyblue'`, and many other names. The library understands hundreds of names and converts them to the right RGB values for you.

### `line(color='red', start=(100, 100), end=(200, 200), *args)`

Draws a straight segment from the start point to the end point.

**Tips**

* `start` and `end` are coordinate pairs. `(0, 0)` is the top-left corner, `(1000, 1000)` is the bottom-right corner.
* The default line is red from `(100, 100)` to `(200, 200)`.

**Example – diagonal line in white**

```python
from drawzero import *

line('white', (0, 0), (1000, 1000))
```

This draws a thin white line from the top-left corner to the bottom-right corner.

**Example – crosshair in cyan**

```python
from drawzero import *

line('cyan', (500, 0), (500, 1000))
line('cyan', (0, 500), (1000, 500))
```

The two calls create a vertical and a horizontal line that meet at the center.

### `circle(color='red', pos=(100, 100), radius=10, *args)`

Draws the outline of a circle.

**Tips**

* `pos` is the center point of the circle.
* `radius` is how far the circle extends from the center in canvas units.

**Example – blue ring around a point**

```python
from drawzero import *

circle('blue', (300, 300), 80)
```

**Example – three concentric circles**

```python
from drawzero import *

center = (750, 200)
circle('orange', center, 40)
circle('white', center, 80)
circle('green', center, 120)
```

### `filled_circle(color='red', pos=(100, 100), radius=10, *args)`

Draws a circle filled with the chosen color.

**Example – traffic light dots**

```python
from drawzero import *

x = 200
filled_circle('red', (x, 200), 60)
filled_circle('yellow', (x, 400), 60)
filled_circle('green', (x, 600), 60)
```

**Example – sun with a face**

```python
from drawzero import *

filled_circle('gold', (800, 200), 100)
filled_circle('black', (760, 170), 10)
filled_circle('black', (840, 170), 10)
line('black', (760, 240), (840, 240))
```

The last `line` reuses the knowledge from the previous section to draw a simple smile.

## Colors as RGB triples

Sometimes you want a very specific shade that does not have a name. In that case you can pass a tuple `(R, G, B)` where each value goes from `0` to `255`. `(255, 0, 0)` is pure red, `(0, 255, 0)` is pure green, `(0, 0, 255)` is pure blue. Mixing values gives new colors.

### `rect(color='red', pos=(100, 100), width=500, height=200, *args)`

Draws only the border of a rectangle.

* `pos` is the top-left corner of the rectangle.
* `width` stretches the rectangle to the right.
* `height` stretches it downward.

**Example – teal frame using RGB**

```python
from drawzero import *

rect((0, 128, 128), (100, 100), 300, 200)
```

**Example – picture frame around a filled area**

```python
from drawzero import *

filled_rect((240, 230, 140), (200, 200), 400, 300)
rect((139, 69, 19), (200, 200), 400, 300)
```

The first call paints the background. The second call, using `rect`, keeps only the outline.

### `filled_rect(color='red', pos=(100, 100), width=500, height=200, *args)`

Draws a solid rectangle.

**Example – basic HUD panel**

```python
from drawzero import *

filled_rect((30, 30, 30), (50, 50), 300, 150)
text('white', 'Score: 1200', (70, 90))
```

**Example – checkerboard tile**

```python
from drawzero import *

for row in range(4):
    for col in range(4):
        color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
        filled_rect(color, (100 + col * 60, 100 + row * 60), 60, 60)
```

This loops over 16 squares and chooses white or black using the RGB tuples.

## Color helper constant `C`

You can also import the special object `C` that contains every named color as an attribute.  
This works great in modern IDEs: typing `C.` shows a dropdown list of color names, and the IDE can warn you when the name is wrong.

```python
from drawzero import C, line

line(C.lightskyblue, (100, 500), (900, 500))
```

If you prefer, you can import both styles together:

```python
from drawzero import *, C
filled_circle(C.magenta, (500, 500), 120)
```

<details>
<summary>Full list of named colors available through <code>C</code> (665 items)</summary>

--8<-- "docs/_color_table.md"

</details>

## More drawing tools

The following helpers build on the same ideas. You can mix text colors, RGB tuples, or values from `C` with all of them.

### `grid()`

Draws a helpful coordinate grid. Lines appear every 100 units with light labels. Use it when you are planning positions.

**Example – show the grid for planning**

```python
from drawzero import *

grid()
```

You can draw other shapes on top of the grid and then remove the `grid()` call once you finish planning.

### `polygon(color='red', *points)`

Draws the outline of a polygon. Pass each corner as its own `(x, y)` pair. The function joins the last point back to the first point automatically.

**Example – simple triangle**

```python
from drawzero import *

polygon('orange', (200, 800), (500, 400), (800, 800))
```

**Example – star outline**

```python
from drawzero import *

points = [
    (500, 200),
    (560, 380),
    (740, 380),
    (600, 500),
    (660, 680),
    (500, 580),
    (340, 680),
    (400, 500),
    (260, 380),
    (440, 380),
]
polygon('gold', *points)
```

### `filled_polygon(color='red', *points)`

Fills the inside of the polygon using the same point format.

**Example – kite shape with shadow**

```python
from drawzero import *

shape = [(500, 200), (700, 400), (500, 800), (300, 400)]
filled_polygon('lightblue', *shape)
polygon('navy', *shape)
```

**Example – mountain silhouettes**

```python
from drawzero import *

mountain1 = [(0, 800), (200, 400), (400, 800)]
mountain2 = [(300, 800), (550, 300), (800, 800)]
filled_polygon((70, 90, 110), *mountain1)
filled_polygon((50, 70, 90), *mountain2)
```

The second polygon uses RGB tuples for a darker shade.

### `text(color='red', text='Hello!', pos=(100, 100), fontsize=24, align='..')`

Draws text on the canvas.

* `text` is the string that you want to show.
* `pos` marks the anchor point.
* `fontsize` controls the size in pixels.
* `align` decides how the anchor sticks to the text. The first symbol handles horizontal alignment (`'<'` for left, `'.'` for center, `'>'` for right). The second symbol handles vertical alignment (`'^'` for top, `'.'` for middle, `'v'` for bottom).

**Example – centered scoreboard**

```python
from drawzero import *

text('white', 'Level Complete!', (500, 120), 48, '.^')
```

**Example – labels near shapes**

```python
from drawzero import *

rect('white', (150, 700), 200, 120)
text('white', 'Player base', (150, 700), 24, '<^')
text('yellow', 'Danger zone', (250, 760), 24, '..')
```

### `fill(color='red')`

Fills the whole canvas with a solid color. This is very useful for the background before you draw other objects.

**Example – night sky background**

```python
from drawzero import *

fill((10, 10, 35))
filled_circle('white', (200, 150), 5)
filled_circle('white', (600, 220), 4)
```

**Example – quick color reset**

```python
from drawzero import *

fill('white')
line('black', (100, 100), (900, 900))
```

Calling `fill('white')` removes old drawings by painting the entire canvas white before you start again.

## Ellipses, arcs, and rotated rectangles

These helpers let you create stretched circles and tilted rectangles. They follow the same color rules you saw before: you can
use color names, RGB triples, or values from `C`. For transparency and stroke size tips, read [Transparency (`alpha`) and line thickness (`line_width`)](transparency_and_line_width.md).

### `ellipse(color='red', pos=(100, 100), width=500, height=200, *args, alpha=255, line_width: int = None)`

Draws the outline of an ellipse. The ellipse fits inside an invisible rectangle whose top-left corner is `pos`, whose `width`
extends to the right, and whose `height` extends downward.

**Tips**

* Think of the ellipse as a squashed circle. When `width` equals `height` you get a perfect circle outline.
* Placing the ellipse in the middle of the canvas is easy when you combine it with `grid()` from the previous section.

**Example – planet orbit guide**

```python
from drawzero import *

grid()
ellipse('white', (200, 300), 600, 200)
filled_circle('yellow', (500, 400), 40)
filled_circle('dodgerblue', (750, 400), 20)
```

The ellipse marks the orbit, while the filled circles show the star and the planet.

**Example – stage spotlight border**

```python
from drawzero import *

fill((10, 10, 25))
ellipse('gold', (250, 150), 500, 700)
text('white', 'Talent Show', (500, 220), 48, '.^')
```

The tall ellipse surrounds the title like a glowing frame.

### `filled_ellipse(color='red', pos=(100, 100), width=500, height=200, *args, alpha=255)`

Fills the entire ellipse with color, using the same bounding box idea as `ellipse`.

**Tips**

* Layer multiple filled ellipses to build gradients or shadows.
* Use them to fake soft shapes such as clouds, ponds, or stadium tracks.

**Example – calm pond with reflection**

```python
from drawzero import *

fill((120, 180, 255))
filled_ellipse((70, 120, 200), (200, 650), 600, 220)
filled_ellipse((150, 200, 255), (260, 690), 480, 140)
```

The second, smaller ellipse sits on top to suggest a highlight on the water.

**Example – running track lanes**

```python
from drawzero import *

fill((30, 120, 30))
for offset in range(0, 80, 20):
    filled_ellipse('sienna', (150 + offset, 200 + offset), 700 - 2 * offset, 400 - 2 * offset)
```

The loop paints four nested ellipses to imitate the rounded corners of a stadium track.

### `arc(color='red', pos=(100, 100), width=500, height=200, start_angle=45, stop_angle=270, alpha=255, line_width: int = None)`

Draws part of an ellipse outline between two angles. The angles are measured in degrees, where `0` points to the right and the
values grow counterclockwise.

**Tips**

* Use a difference between `start_angle` and `stop_angle` smaller than `360` to create a curved slice.
* Try combining `arc` with `filled_circle` eyes or gauges to add expressive details to your drawings.

**Example – smiling mouth on a face**

```python
from drawzero import *

fill((255, 224, 189))
filled_circle('black', (420, 360), 15)
filled_circle('black', (580, 360), 15)
arc('brown', (360, 420), 280, 160, 200, 340)
```

Here the arc starts on the left side (near `200` degrees) and ends on the right side (near `340` degrees), leaving a curved smile
on the bottom.

**Example – progress gauge**

```python
from drawzero import *

fill((20, 20, 30))
ellipse('gray', (250, 250), 500, 500)
arc('lime', (250, 250), 500, 500, 180, 360)
text('white', '50%', (500, 520), 64, '.^')
```

The green arc begins on the left (`180` degrees) and ends on the right (`360` degrees), covering the lower half of the circle li
ke a progress meter.

### `rect_rotated(color='red', pos=(100, 100), width=500, height=200, angle=0, *args, alpha=255, line_width: int = None)`

Draws the outline of a rectangle that has been rotated around its center. The unrotated rectangle would start at `pos` and
would measure `width` by `height`. Positive angles turn the shape counterclockwise.

**Tips**

* Sketch the rectangle with `rect` first, then switch to `rect_rotated` when you know the right angle.
* Small angles (like `15` or `20` degrees) are great for giving objects a sense of motion.

**Example – tilted photo frame**

```python
from drawzero import *

fill((240, 235, 220))
rect_rotated('saddlebrown', (250, 200), 500, 350, -12)
filled_rect('white', (270, 220), 460, 310)
text('black', 'Family Trip', (500, 350), 36, '.^')
```

The thin negative angle makes the frame lean to the right.

**Example – warning sign**

```python
from drawzero import *

fill((40, 40, 40))
rect_rotated('yellow', (350, 300), 300, 300, 45)
text('black', '!', (500, 450), 180, '.^')
```

Rotating a square by `45` degrees turns it into a diamond-shaped outline.

### `filled_rect_rotated(color='red', pos=(100, 100), width=500, height=200, angle=0, *args, alpha=255)`

Fills the rotated rectangle using the same center and angle rules as `rect_rotated`.

**Tips**

* Combine `filled_rect_rotated` with `rect_rotated` of a different color to get borders.
* Use several rotated rectangles together to build windmill blades or paper pinwheels.

**Example – rotating propeller art**

```python
from drawzero import *

fill((15, 15, 35))
for blade in range(4):
    filled_rect_rotated('deepskyblue', (460, 360), 80, 280, blade * 45)
filled_circle('white', (500, 500), 60)
```

Each iteration draws one blade by rotating the same rectangle.

**Example – cozy rug on the floor**

```python
from drawzero import *

fill((120, 85, 60))
filled_rect_rotated((200, 120, 70), (250, 250), 500, 320, 8)
rect_rotated((120, 60, 30), (250, 250), 500, 320, 8)
```

The filled rectangle creates the fabric, and the outline adds a stitched border.
