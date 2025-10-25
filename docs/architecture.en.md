# DrawZero Architecture Overview

This document summarizes how DrawZero is put together without exposing low-level implementation details. It highlights the responsibilities of each part so that contributors know where to add new features while keeping the public API simple for learners.

## Public API surface

Everything in the library is re-exported, so one import is enough:

```python
from drawzero import *
```

The call exposes:

* Drawing helpers such as `line`, `circle`, `rect`, `polygon`, `text`, `image`, and their filled variants.
* Animation and timing helpers: `run`, `tick`, `sleep`, `fps`, and `quit`.
* Input helpers for reading the keyboard and mouse: `get_keys_pressed`, `keys_mods_pressed`, `get_mouse_pressed`, plus the shared lists `keysdown`, `keysup`, `mousemotions`, `mousebuttonsdown`, and `mousebuttonsup`.
* Utility objects: the `screen` shim used by Pygame Zero style scripts, the `Pt` vector/turtle hybrid, the `Gradient` color ramp builder, localization via `set_lang`, the color namespaces (`C`, `COLORS`, `THECOLORS`, `ALL_COLORS`), keyboard constants (`K`, `KEY`), and `copy_examples()` for scaffolding tutorials.
* Canvas configuration helpers such as `set_virtual_size()`.

All user guides in the documentation assume this import style.

## Rendering flow

Every drawing helper validates and normalizes its arguments (coordinates, angles, colors, and radii) before forwarding them to the active renderer. The renderer choice depends on the `EJUDGE_MODE` environment variable:

* When the variable is unset or false, DrawZero opens a graphical window backed by pygame and renders directly to the screen.
* When `EJUDGE_MODE` is true (used in automated graders and CI), DrawZero switches to a text-mode backend that prints serialized drawing commands instead of opening a window.

Regardless of the backend, calling `tick()` processes window events, updates the shared input lists, and keeps the animation running near 30 FPS. Skipping `tick()` prevents new events from reaching the program, so the documentation emphasizes placing it in every frame loop.

## Virtual canvas and coordinate scaling

The library works with a virtual 1000×1000 canvas. Drawing helpers accept integers or floats; values are converted to the current virtual size and then mapped to the actual window size. `set_virtual_size()` lets scripts change the logical resolution when they want to draw in a different coordinate space. Mouse helpers always return positions in the same virtual coordinate system, regardless of the real window dimensions.

## Utility helpers and constants

Several helpers ship with the public API and are heavily used by examples and tests:

* `Pt` stores a position and heading, supports turtle-style movement, and acts like a mutable 2D vector.
* `Gradient` converts numbers into colors by interpolating across a list of samples.
* Color namespaces (`C`, `COLORS`, `THECOLORS`, `ALL_COLORS`) make pygame's color table easy to access without typing RGB triples.
* Keyboard constants `K` and `KEY` mirror pygame's naming so programs can use `K.space`, `K.left`, and similar attributes in both GUI and headless environments.
* `copy_examples()` copies the bundled examples into the working directory to help newcomers start experimenting.

## Examples and documentation

The package includes bilingual example scripts that demonstrate primitives, animations, gradients, image loading, and keyboard/mouse interaction. The MkDocs documentation mirrors those scripts with detailed explanations. Tests import many of the examples directly, so new examples must avoid side effects at import time unless they are guarded by `if __name__ == "__main__":`.

## Test suite

Automated tests cover the drawing helpers, gradients, localization messages, point arithmetic, and example imports. Continuous integration runs them in both graphical mode and text mode (with `EJUDGE_MODE=true`) to ensure the public API behaves the same in either environment.
