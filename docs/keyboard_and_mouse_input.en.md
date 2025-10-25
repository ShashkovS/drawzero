# Keyboard and mouse input

This page explains how to read keyboard and mouse input when you build an
interactive drawing with DrawZero. It uses simple English and many examples so
that you can follow every step.

## Why we need an event loop

Real-time programs must check for new events many times per second. You can see
this pattern in almost every game or animation. The main loop looks like this:

```python
while True:
    tick()          # update animations, timers, physics
    # process events # read keyboard and mouse state here
```

`tick()` comes from DrawZero helpers (see the [Animation basics](animation.md)
page). It advances time and asks the renderer to collect new input events. After
each `tick()` you can safely read the keyboard and mouse lists described on this
page.

If you stop calling `tick()`, the window freezes and no fresh input arrives.
This is why you must keep the loop running even when nothing happens yet.

## Understanding input helpers

The renderer records two kinds of information:

1. **Current state** – which keys or mouse buttons are held down right now.
2. **Event queues** – a history of what changed during the last frame.

State helpers are good for continuous actions (for example, holding the left
arrow to move a sprite). Event queues are better when you need one-time actions
(for example, detecting that a key was pressed once to open a menu).

All helpers live on the global `renderer` object. Import them from
`drawzero.renderer` or access them through `utils.draw` depending on the script
style you picked (see [Architecture overview](architecture.md)).

### Snapshot helpers

#### `get_keys_pressed = renderer.get_keys_pressed`

Returns a **set of strings** with the names of all keys that are currently held
down. Use it when you only care whether a key is down, not how many times it was
pressed.

```python
from drawzero.renderer import get_keys_pressed

pressed = get_keys_pressed()
if "LEFT" in pressed:
    player_x -= 5
if "SPACE" in pressed:
    player_jump()
```

`get_keys_pressed()` is re-evaluated on each call, so ask for it **after**
`tick()`. It uses the same key names that appear in the event queues described
below.

#### `keys_mods_pressed = renderer.keys_mods_pressed`

Returns a **set of modifier names** like `"SHIFT"`, `"CTRL"`, or `"ALT"`. This
is useful when you want to support shortcuts such as `Ctrl+S`.

```python
if "CTRL" in keys_mods_pressed() and "S" in get_keys_pressed():
    save_project()
```

Modifiers are separated from regular keys so you can check them quickly without
searching inside the full key set.

#### `get_mouse_pressed = renderer.get_mouse_pressed`

Returns a **set of mouse button names** such as `"LEFT"`, `"MIDDLE"`, and
`"RIGHT"`. Combine it with the current mouse position from your canvas helpers
(see [Drawing primitives](primitives.md) for coordinate utilities).

```python
if "LEFT" in get_mouse_pressed():
    draw_circle(mouse_pos(), radius=10)
```

Remember: this only reports buttons that are held during the latest frame. You
still need the event queues to detect the exact click moment.

### Event queues

Event queues are lists that reset on every `tick()`. They keep the order of
incoming events so you can replay what happened during the last frame.

Each item inside the queue is a small object (usually a `namedtuple` or a
simple class) with fields like `key`, `mod`, `button`, `pos`, or `rel`. You can
inspect them with `print(event)` to learn the exact structure.

#### `keysdown = renderer.keysdown`

Contains a **list of key-down events**. Each event fires when a key changes from
"up" to "down". Use it for single presses.

```python
for event in keysdown:
    if event.key == "SPACE":
        spawn_bullet()
```

This queue is empty when no new key press happened in the current frame.

#### `keysup = renderer.keysup`

Contains a **list of key-up events**. These events fire when a key is released.
They are useful for toggles or for stopping an action exactly when the player
lets go.

```python
for event in keysup:
    if event.key == "LEFT":
        stop_moving()
```

#### `mousemotions = renderer.mousemotions`

Contains a **list of mouse motion events**. Every event has at least a `pos`
attribute with the current cursor position in logical (virtual) coordinates, and
usually a `rel` attribute with the movement delta.

```python
for event in mousemotions:
    trail.add_point(event.pos)
```

Read [Images and coordinate systems](images.md) to learn how logical positions
map to your canvas.

#### `mousebuttonsdown = renderer.mousebuttonsdown`

Contains a **list of mouse button down events**. They fire when the user presses
any mouse button. Events include the button name and the mouse position.

```python
for event in mousebuttonsdown:
    if event.button == "LEFT":
        start_drag(event.pos)
```

#### `mousebuttonsup = renderer.mousebuttonsup`

Contains a **list of mouse button up events**. They fire when the user releases
any mouse button. Use them to finish actions like drawing a line or confirming a
selection.

```python
for event in mousebuttonsup:
    if event.button == "LEFT":
        end_drag(event.pos)
```

## Putting it all together

Here is a full loop that uses both state and event helpers.

```python
from drawzero import renderer
from drawzero import utils

while True:
    utils.tick()

    # continuous movement
    pressed = renderer.get_keys_pressed()
    if "LEFT" in pressed:
        player.move(-5, 0)
    if "RIGHT" in pressed:
        player.move(5, 0)

    # one-time actions
    for event in renderer.keysdown:
        if event.key == "SPACE":
            player.jump()

    for event in renderer.mousebuttonsdown:
        if event.button == "LEFT":
            player.shoot(event.pos)

    # update the canvas here (see Animation basics for draw calls)
```

You can compare this pattern with the `16_keyboard_and_mouse.py` example listed
in the [Examples overview](examples_overview.md). That script also demonstrates
how to combine keyboard input with on-screen feedback.

## Tips for smooth interaction

- Call `tick()` regularly. A typical DrawZero animation runs 30 times per
  second, but the helpers work at any speed.
- Avoid long blocking code (like `time.sleep(5)`) inside the loop. Put heavy
  work into small slices or background threads if needed.
- If you only need the latest mouse position, keep the last item from
  `mousemotions` or use utility functions such as `utils.draw.mouse_pos()`.
- Always test on real hardware. Touchpads, gaming mice, and keyboards with
  non-English layouts can send different button names. Print events while
  developing to see the actual data.
- Combine modifier checks (`keys_mods_pressed`) with regular keys to create
  shortcuts that feel natural to users.

## Where to learn more

- [Animation basics](animation.md) explains how `tick()` fits inside the drawing
  pipeline.
- [Architecture overview](architecture.md) shows how input helpers connect to
  the renderer internals.
- [Examples overview](examples_overview.md) points to ready-made scripts you can
  run and modify.
- The `keyboard_and_mouse_events.gif` image in the docs folder gives a quick
  visual preview of what you can build.

With these tools you can capture keyboard and mouse events reliably and build
responsive, interactive scenes in DrawZero.
