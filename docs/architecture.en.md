# DrawZero Architecture Overview

This document summarizes the internal layout of the DrawZero project so that contributors can quickly orient themselves in the codebase.

## Package layout

```
src/drawzero/
├── __init__.py          # Re-exported public API
├── __main__.py          # CLI entry point (copies examples, draws demo frame)
├── examples/            # Tutorial-style scripts executed by tests
└── utils/               # Core rendering, math, and convenience helpers
```

Other notable top-level folders:

* `docs/` – MkDocs documentation shipped on PyPI; suitable place for additional guides.
* `tests/` – Pytest and unittest suites that import examples, validate converters, gradients, points, and internationalization helpers.

## Public API surface (`src/drawzero/__init__.py`)

The package exposes a “flat” API meant to mimic turtle/pygame zero ergonomics. All drawing helpers are imported from `utils.draw`, while math helpers come from sibling modules:

* Drawing primitives: `line`, `circle`, `rect`, `polygon`, `text`, `image`, etc.
* Filled variants share the same renderer entry points by passing `line_width=0`.
* Animation and timing helpers: `tick`, `sleep`, `run`, `fps`, `quit`.
* Input helpers proxy the renderer’s key/mouse state (`get_keys_pressed`, `keysdown`, `mousebuttonsdown`, ...).
* Utilities: `Pt` (vector/turtle hybrid), `Gradient`, `copy_examples`, color constants (`C`, `COLORS`, `ALL_COLORS`).

Every user-facing function ultimately routes through the renderer stack described below.

## Rendering pipeline (`utils.draw` → `utils.renderer`)

`utils.draw` performs argument validation and coercion before delegating to the actual drawing backend. Common steps for each primitive:

1. Convert user-supplied data through converter helpers (`utils.converters`). These functions normalize coordinates, radii, rectangles, and colors, while collecting rich error messages via `BadDrawParmsError` and localized strings in `utils.i18n`.
2. Choose the backend module depending on the `EJUDGE_MODE` environment variable. GUI builds import `utils.renderer` (pygame-based). Text-mode/CI builds fall back to `utils.renderer_ejudge`, which prints commands for automated judges.
3. After the renderer call, update cached input event lists so that consumers see mouse/key positions in logical (virtual) coordinates.

### `utils.renderer`

The pygame renderer lazily creates a resizable window and keeps an off-screen copy to survive resizes. Important responsibilities:

* Surface management: `_create_surface()` defers window creation until the first drawing call; `_resize()` rescales existing content when SDL emits a resize event.
* Primitive drawing: each `draw_*` function handles optional alpha blending by drawing into temporary `pygame.Surface` buffers when needed.
* Event pump: `draw_tick()` advances the clock (30 FPS target), flushes the event queue, and populates global lists (`keysdown`, `mousebuttonsdown`, etc.) consumed by `utils.draw`.
* Lifecycle hooks: `atexit.register(_draw_go)` keeps the pygame loop alive until the process exits; `_init()` configures DPI-awareness on Windows and centers the window.
* Coordinate scaling: setter functions from `utils.screen_size` maintain the mapping between “virtual” 1000×1000 coordinates (used by the API) and the actual window size.

### `utils.renderer_ejudge`

A lightweight stub used when `EJUDGE_MODE=true` (e.g., tests running without a GUI). It mirrors the renderer API but simply prints serialized drawing commands. Screen size is fixed to 1000×1000 so coordinate conversion remains consistent.

## Coordinate transforms (`utils.screen_size`)

DrawZero always exposes a 1000×1000 virtual canvas. `set_virtual_size()` can change that logical resolution, and `set_real_size()` is called by the renderer when it knows the real pixel size. The module exposes helpers to convert between coordinate spaces:

* `to_canvas_x` / `to_canvas_y` – convert virtual coordinates to actual pixels.
* `from_canvas_x` / `from_canvas_y` – convert back to logical coordinates (used when reporting mouse positions).

All converters and event wrappers rely on this module, so adjust it carefully if supporting non-square canvases.

## Math and utility helpers

* `utils.pt.Pt` implements a mutable 2D vector with turtle-style movement, arithmetic operators, and convenience methods (`forward`, `rotate_around`, `distance`, etc.). Examples rely on it for animation logic.
* `utils.gradient.Gradient` constructs color ramps over a numeric domain (default 0–1). It uses the same converter/error infrastructure to provide consistent validation.
* `utils.colors` exposes pygame’s color table both as attribute access (`C.red`) and dictionaries (`COLORS`, `ALL_COLORS`).
* `utils.key_flags` mirrors pygame key constants so code can use `K.<name>` even when pygame is absent (constants are loaded lazily when available).
* `utils.copy_examples.copy_examples()` copies `src/drawzero/examples` into the current working directory; the CLI entry point calls it to bootstrap learners.

## Examples (`src/drawzero/examples`)

Short, bilingual scripts demonstrate the API: drawing primitives, loops, animations, gradients, images, and simple interactive games. Tests import many of them to ensure they still execute, so keep side effects (e.g., infinite loops) behind guards if you add new ones.

## Tests (`tests/`)

* `test_examples_gui_mode.py` imports each example module to ensure it runs against the real renderer.
* `test_examples_text_mode.py` sets `EJUDGE_MODE` and asserts the text renderer paths work.
* The remaining pytest modules cover specific utilities: converter validation, localized error messages, gradient interpolation, the `Pt` vector API, and `copy_examples()` behavior.

Use these tests as references when extending validation logic or adding new primitives.
