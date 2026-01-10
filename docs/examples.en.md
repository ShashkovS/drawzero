# DrawZero Examples

This page contains a gallery of examples demonstrating the capabilities of the DrawZero library.

Use the index below to jump to a specific script.

| File | Focus | Key ideas |
| --- | --- | --- |
| [`00_hello_world.py`](#00_hello_worldpy) | First canvas rendering | Draws a bordered canvas, splits text into two languages, and starts the `run()` loop. |
| [`01_grid_and_coordinates.py`](#01_grid_and_coordinatespy) | Coordinate system tour | Renders the helper `grid()`, then annotates various primitives at known coordinates. |
| [`02_loops_and_rgb_colors.py`](#02_loops_and_rgb_colorspy) | Loop-driven art | Uses a `for` loop and random RGB tuples to paint vertical bars with varying heights. |
| [`03_simple_objects.py`](#03_simple_objectspy) | Primitive catalog | Demonstrates every drawing primitive (lines, circles, rotated rectangles, polygons, text alignment). |
| [`04_loops_sin_plot.py`](#04_loops_sin_plotpy) | Math plotting | Plots a sine wave by stitching short line segments along the X axis. |
| [`05_points.py`](#05_pointspy) | [`Pt` helper](pt.md) as vector/turtle | Shows how the `Pt` class supports arithmetic, motion, and turtle-style rotation in loops. |
| [`06_turtle_style.py`](#06_turtle_stylepy) | Polygon drawing with [`Pt`](pt.md) | Rotates a `Pt` instance to build regular polygons for sides 3–10 using turtle operations. |
| [`07_animation_circles.py`](#07_animation_circlespy) | Minimal animation loop | Varies circle position, radius, and color over time while calling `tick()` each frame. |
| [`08_animation_traffic_light.py`](#08_animation_traffic_lightpy) | State-based animation | Reuses a helper to draw a traffic light and uses `sleep()` to cycle colors. |
| [`09_animation_rectangles.py`](#09_animation_rectanglespy) | Complex animation | Combines `Pt` math with rotation/orbit logic, transparency, and conditional effects. |
| [`10_animation_planets.py`](#10_animation_planetspy) | Orbital motion | Calculates circular motion for a planet/moon pair and redraws every frame. |
| [`11_transparency_and_line_width.py`](#11_transparency_and_line_widthpy) | Alpha blending and stroke widths | Samples different alpha values and line widths across circles, rectangles, polygons, and ellipses. |
| [`12_images.py`](#12_imagespy) | Image rendering | Loads `cat.png` from the examples folder, demonstrates scaling and alpha when blitting images. |
| [`13_gradients.py`](#13_gradientspy) | [Gradient helper](gradient.md) | Builds several `Gradient` scales and visualizes them through stacked rectangles. |
| [`14_animation_close_vertex.py`](#14_animation_close_vertexpy) | Proximity graph animation | Moves random `Pt` nodes with wrap-around motion, draws lines between nearby pairs, and uses FPS overlay. |
| [`15_animation_firework.py`](#15_animation_fireworkpy) | Particle system | Implements `Particle` and `Firework` classes with physics updates, gradient-based glow, and clean-up logic. |
| [`16_keyboard_and_mouse.py`](#16_keyboard_and_mousepy) | Input handling | Reads key state arrays and event queues to move a square, track typed characters, and follow the mouse. |
| [`17_mouse_tube.py`](#17_mouse_tubepy) | Mouse trail effect | Captures `mouse_pos()` each frame, grows concentric circles with a gradient as they age. |
| [`18_game_stars.py`](#18_game_starspy) | 3D starfield mini-game | Uses dataclasses, random stars, and WASD/QE controls to navigate through a pseudo-3D field. |
| [`19_game_colors.py`](#19_game_colorspy) | Reaction game | Displays color words versus actual colors, handles mouse button choices with time penalties. |
| [`20_game_racing.py`](#20_game_racingpy) | Multiplayer mini-game | Assigns distinct key bindings per car, scrolls a precomputed road, and keeps per-player scores. |
| [`99_errors.py`](#99_errorspy) | Error reporting demo | Forces validation errors under `EJUDGE_MODE` to showcase localized diagnostics emitted by converters. |

## Getting Started

These examples show the very basics of getting an image on the screen.

### 00_hello_world.py

![00_hello_world](imgs/ex_00.png)
``` title="00_hello_world.py"
--8<-- "src/drawzero/examples/00_hello_world.py"
```

### 01_grid_and_coordinates.py

![01_grid_and_coordinates](imgs/ex_01.png)
``` title="01_grid_and_coordinates.py"
--8<-- "src/drawzero/examples/01_grid_and_coordinates.py"
```

## Using Loops and Colors

Learn how to use loops to create more complex patterns and how to work with different colors.

### 02_loops_and_rgb_colors.py

![02_loops_and_rgb_colors](imgs/ex_02.png)
``` title="02_loops_and_rgb_colors.py"
--8<-- "src/drawzero/examples/02_loops_and_rgb_colors.py"
```

### 03_simple_objects.py

![03_simple_objects](imgs/ex_03.png)
``` title="03_simple_objects.py"
--8<-- "src/drawzero/examples/03_simple_objects.py"
```

### 04_loops_sin_plot.py

![04_loops_sin_plot](imgs/ex_04.png)
``` title="04_loops_sin_plot.py"
--8<-- "src/drawzero/examples/04_loops_sin_plot.py"
```

## Points and Turtle-style Graphics

The `Pt` class allows for vector math and turtle-like drawing commands.

### 05_points.py

![05_points](imgs/ex_05.png)
``` title="05_points.py"
--8<-- "src/drawzero/examples/05_points.py"
```

### 06_turtle_style.py

![06_turtle_style](imgs/ex_06.png)
``` title="06_turtle_style.py"
--8<-- "src/drawzero/examples/06_turtle_style.py"
```

## Animation

Bring your drawings to life with animations.

### 07_animation_circles.py

![07_animation_circles](imgs/ex_07.webp)
``` title="07_animation_circles.py"
--8<-- "src/drawzero/examples/07_animation_circles.py"
```

### 08_animation_traffic_light.py

![08_animation_traffic_light](imgs/ex_08.webp)
``` title="08_animation_traffic_light.py"
--8<-- "src/drawzero/examples/08_animation_traffic_light.py"
```

### 09_animation_rectangles.py

![09_animation_rectangles](imgs/ex_09.webp)
``` title="09_animation_rectangles.py"
--8<-- "src/drawzero/examples/09_animation_rectangles.py"
```

### 10_animation_planets.py

![10_animation_planets](imgs/ex_10.webp)
``` title="10_animation_planets.py"
--8<-- "src/drawzero/examples/10_animation_planets.py"
```

## Advanced Drawing

Explore more advanced features like transparency, image rendering, and color gradients.

### 11_transparency_and_line_width.py

![11_transparency_and_line_width](imgs/ex_11.png)
``` title="11_transparency_and_line_width.py"
--8<-- "src/drawzero/examples/11_transparency_and_line_width.py"
```

### 12_images.py

![12_images](imgs/ex_12.png)
``` title="12_images.py"
--8<-- "src/drawzero/examples/12_images.py"
```

### 13_gradients.py

![13_gradients](imgs/ex_13.png)
``` title="13_gradients.py"
--8<-- "src/drawzero/examples/13_gradients.py"
```

## Interactive Examples

Make your creations interactive by responding to keyboard and mouse input.

### 14_animation_close_vertex.py

![14_animation_close_vertex](imgs/ex_14.webp)
``` title="14_animation_close_vertex.py"
--8<-- "src/drawzero/examples/14_animation_close_vertex.py"
```

### 15_animation_firework.py

![15_animation_firework](imgs/ex_15.webp)
``` title="15_animation_firework.py"
--8<-- "src/drawzero/examples/15_animation_firework.py"
```

### 16_keyboard_and_mouse.py

![16_keyboard_and_mouse](imgs/ex_16.webp)
``` title="16_keyboard_and_mouse.py"
--8<-- "src/drawzero/examples/16_keyboard_and_mouse.py"
```

### 17_mouse_tube.py

![17_mouse_tube](imgs/ex_17.webp)
``` title="17_mouse_tube.py"
--8<-- "src/drawzero/examples/17_mouse_tube.py"
```

## Games

Build simple games using the DrawZero library.

### 18_game_stars.py

![18_game_stars](imgs/ex_18.webp)
``` title="18_game_stars.py"
--8<-- "src/drawzero/examples/18_game_stars.py"
```

### 19_game_colors.py

![19_game_colors](imgs/ex_19.webp)
``` title="19_game_colors.py"
--8<-- "src/drawzero/examples/19_game_colors.py"
```

### 20_game_racing.py

![20_game_racing](imgs/ex_20.webp)
``` title="20_game_racing.py"
--8<-- "src/drawzero/examples/20_game_racing.py"
```
