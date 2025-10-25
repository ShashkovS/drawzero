# Examples Overview

The `src/drawzero/examples` package contains runnable scripts that double as smoke tests and usage demonstrations. The table below highlights the intent of each script so you can pick a relevant starting point when troubleshooting or extending functionality.

| File | Focus | Key ideas |
| --- | --- | --- |
| `00_hello_world.py` | First canvas rendering | Draws a bordered canvas, splits text into two languages, and starts the `run()` loop. |
| `01_grid_and_coordinates.py` | Coordinate system tour | Renders the helper `grid()`, then annotates various primitives at known coordinates. |
| `02_loops_and_rgb_colors.py` | Loop-driven art | Uses a `for` loop and random RGB tuples to paint vertical bars with varying heights. |
| `03_simple_objects.py` | Primitive catalog | Demonstrates every drawing primitive (lines, circles, rotated rectangles, polygons, text alignment). |
| `04_loops_sin_plot.py` | Math plotting | Plots a sine wave by stitching short line segments along the X axis. |
| `05_points.py` | [`Pt` helper](pt.md) as vector/turtle | Shows how the `Pt` class supports arithmetic, motion, and turtle-style rotation in loops. |
| `06_turtle_style.py` | Polygon drawing with [`Pt`](pt.md) | Rotates a `Pt` instance to build regular polygons for sides 3–10 using turtle operations. |
| `07_animation_circles.py` | Minimal animation loop | Varies circle position, radius, and color over time while calling `tick()` each frame. |
| `08_animation_traffic_light.py` | State-based animation | Reuses a helper to draw a traffic light and uses `sleep()` to cycle colors. |
| `09_animation_rectangles.py` | Complex animation | Combines `Pt` math with rotation/orbit logic, transparency, and conditional effects. |
| `10_animation_planets.py` | Orbital motion | Calculates circular motion for a planet/moon pair and redraws every frame. |
| `11_transparency_and_line_width.py` | Alpha blending and stroke widths | Samples different alpha values and line widths across circles, rectangles, polygons, and ellipses. |
| `12_images.py` | Image rendering | Loads `cat.png` from the examples folder, demonstrates scaling and alpha when blitting images. |
| `13_gradients.py` | [Gradient helper](gradient.md) | Builds several `Gradient` scales and visualizes them through stacked rectangles. |
| `14_animation_close_vertex.py` | Proximity graph animation | Moves random `Pt` nodes with wrap-around motion, draws lines between nearby pairs, and uses FPS overlay. |
| `15_animation_firework.py` | Particle system | Implements `Particle` and `Firework` classes with physics updates, gradient-based glow, and clean-up logic. |
| `16_keyboard_and_mouse.py` | Input handling | Reads key state arrays and event queues to move a square, track typed characters, and follow the mouse. |
| `17_mouse_tube.py` | Mouse trail effect | Captures `mouse_pos()` each frame, grows concentric circles with a gradient as they age. |
| `18_game_stars.py` | 3D starfield mini-game | Uses dataclasses, random stars, and WASD/QE controls to navigate through a pseudo-3D field. |
| `19_game_colors.py` | Reaction game | Displays color words versus actual colors, handles mouse button choices with time penalties. |
| `20_game_racing.py` | Multiplayer mini-game | Assigns distinct key bindings per car, scrolls a precomputed road, and keeps per-player scores. |
| `99_errors.py` | Error reporting demo | Forces validation errors under `EJUDGE_MODE` to showcase localized diagnostics emitted by converters. |

When adding new examples, keep them import-safe (tests import modules directly) and prefer finite loops or guard infinite loops with a `if __name__ == "__main__"` block.
