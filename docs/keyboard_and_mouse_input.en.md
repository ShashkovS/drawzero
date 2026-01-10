# Keyboard and mouse input

This page explains how to read keyboard and mouse input when you build an
interactive drawing with DrawZero.

## Event loop and tick

Real-time programs must check input many times per second. DrawZero does this
inside `tick()`: it pumps the pygame event queue, refreshes key and mouse state,
and converts mouse coordinates into the 1000x1000 virtual canvas. Call `tick()`
once per frame (most examples put it at the end of the loop).

```python
from drawzero import *

while True:
    # read input collected by the last tick
    # update game state + draw
    tick()  # process events and keep ~30 FPS
```

If you stop calling `tick()`, the window freezes and input stops updating.

## State helpers

### `get_keys_pressed()`

Returns a `KeysPressed` object (a wrapper over `pygame.key.get_pressed()`). It
behaves like a list of booleans and accepts key codes or key names.

```python
from drawzero import *

keys = get_keys_pressed()
if keys[K.LEFT] or keys[K.a]:
    player_x -= 5
if keys["SPACE"]:
    player_jump()
```

Use `K`/`KEY` constants for reliable names (for example `K.LEFT`, `K.SPACE`,
`K.a`).

### `keys_mods_pressed()`

Returns an **integer bitmask** of active modifiers (same as
`pygame.key.get_mods()`). Check it with bitwise `&` and the `K.MOD_*` constants.

```python
from drawzero import *

mods = keys_mods_pressed()
if mods & K.MOD_CTRL and get_keys_pressed()[K.s]:
    save_project()
if mods & K.MOD_SHIFT:
    speed *= 2
```

### `get_mouse_pressed()`

Returns a tuple of booleans `(left, middle, right)` describing which mouse
buttons are held down.

```python
from drawzero import *

left, middle, right = get_mouse_pressed()
if left:
    draw_circle(mouse_pos(), radius=10)
```

### `mouse_pos()`

Returns the current mouse position in **virtual canvas coordinates**.

## Event queues

Event queues are **lists** cleared on every `tick()`. They contain `pygame`
event objects collected since the previous tick, in order.

### `keysdown` / `keysup`

Lists of key press and key release events. Use `event.key` to compare with
`K` constants and `event.unicode` to read typed characters.

```python
from drawzero import *

for event in keysdown:
    if event.key == K.SPACE:
        spawn_bullet()
    if event.unicode:
        typed_text += event.unicode
```

`event.mod` is a modifier bitmask if you need it.

If you only care about non-text keys (arrows, space, escape), check `event.key`
directly:

```python
from drawzero import *

for event in keysdown:
    if event.key == K.SPACE:
        print("space")
    elif event.key == K.LEFT:
        print("left")
```

### `mousemotions`

List of mouse motion events. Each event has:

- `event.pos` – current cursor position (virtual canvas coordinates)
- `event.rel` – movement delta since last motion
- `event.buttons` – tuple of held mouse buttons

```python
from drawzero import *

for event in mousemotions:
    trail.add_point(event.pos)
```

### `mousebuttonsdown` / `mousebuttonsup`

Lists of mouse button events. Each event has:

- `event.button` – button number (`1` left, `2` middle, `3` right, `4/5` wheel)
- `event.pos` – click position (virtual canvas coordinates)

```python
from drawzero import *

for event in mousebuttonsdown:
    if event.button == 1:
        start_drag(event.pos)
```

You can also read both the click position and the button number:

```python
from drawzero import *

for event in mousebuttonsdown:
    x, y = event.pos
    print(f"button={event.button} pos=({x:.1f}, {y:.1f})")
```

## Putting it all together

```python
from drawzero import *

while True:
    keys = get_keys_pressed()
    if keys[K.LEFT]:
        player.move(-5, 0)
    if keys[K.RIGHT]:
        player.move(5, 0)

    for event in keysdown:
        if event.key == K.SPACE:
            player.jump()

    for event in mousebuttonsdown:
        if event.button == 1:
            player.shoot(event.pos)

    # update the canvas here
    tick()
```

You can compare this pattern with the `16_keyboard_and_mouse.py` example listed
in [Examples](examples.md).

## Tips for smooth interaction

- Call `tick()` regularly to keep input fresh.
- Avoid long blocking code (like `time.sleep(5)`) inside the loop.
- Use `keys_mods_pressed()` with `K.MOD_*` for keyboard shortcuts.
- If you only need the latest mouse position, call `mouse_pos()`.
- Print events while developing to see the actual values on your hardware.

## Where to learn more

- [Animation basics](animation.md) explains how `tick()` fits inside the drawing
  pipeline.
- [Examples](examples.md) points to ready-made scripts you can
  run and modify.
