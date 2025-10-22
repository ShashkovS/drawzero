# DrawZero animations

## Introduction

This page explains how to build smooth animations in DrawZero. We use very
simple English and many examples, so even middle school students who are not
native speakers can follow along. By the end, you will know how to control the
animation loop, how to draw every frame, how to keep a stable frame rate, and
how to add extra visual effects like motion trails.

## The animation event loop

All DrawZero animations follow the same rhythm. A typical loop looks like this:

```python
while True:
    tick()
    clear()
    # draw something here
```

Let us look at each step in the loop.

1. `tick()` waits so that we keep a constant frame rate and collects new input
   events from the keyboard and the mouse.
2. `clear()` resets the screen before we draw the next frame. You can replace it
   with other tricks (for example, transparent fills) when you want a motion
   trail.
3. After that you draw shapes, text, or images for this frame.

When the loop reaches the end, it starts again. This repeats many times every
second, which creates the animation.

### Why the order matters

Always call `tick()` before drawing. The function updates the internal timer and
processes window events. If you skip it, the window can freeze and the close
button might stop working. Clearing the screen after `tick()` but before
drawing makes sure the new frame does not mix with the previous one (unless you
want that on purpose for a trail effect).

## A complete first example

Here is a tiny program that moves a circle from left to right:

```python
from drawzero import *

x = 50
speed = 5

while True:
    tick()            # keep 30 frames per second and read events
    clear()           # erase the previous frame

    circle('orange', (x, 300), 40, line_width=4)
    filled_circle('yellow', (x, 300), 32)

    x += speed        # change the position for the next frame
    if x > 1100:
        x = 50
```

Run it and you will see the circle travel across the screen. Try changing the
speed or the size to experiment.

## Function reference

### `clear()`

```python
def clear():
    """Reset the screen to black."""
```

`clear()` wipes the canvas to solid black. You usually call it once per frame to
start with a clean surface. This is the quickest way to remove everything drawn
in the previous frame.

*Tip:* if you prefer a different background color, you can draw a filled
rectangle that covers the full window right after `clear()`.

### `fill(color='red', alpha=255)`

`fill()` covers the screen with a color. The `alpha` parameter controls
transparency. When `alpha` is less than `255`, the new color is semi-transparent.
You can use this trick instead of `clear()` to keep motion trails:

```python
while True:
    tick()
    fill('black', alpha=30)  # almost clear, but keep a soft trail
    # draw moving objects here
```

A low alpha value (for example `30`) gives a long trail, because the old drawing
fades slowly. A higher alpha (for example `200`) erases the frame almost like a
full `clear()`.

### `tick(r=1)`

```python
def tick(r=1):
    """Sleep for 1/30 of a second.
    If tick functions is called in a loop, then sleep time is reduced so
    takes 1/30 second between calls. For example if calculations between tick() calls take 1/60s,
    then tick sleeps for 1/60s. So while calculations takes less then 1/30s tick()
    we get 30 frames per second."""
```

Calling `tick()` keeps the animation running at 30 frames per second (FPS). This
only works when your own drawing and calculations are fast enough. If one loop
iteration takes less than 1/30 of a second, `tick()` sleeps for the remaining
fraction so that the total time between frames is almost exactly 1/30 second. As
long as you stay under this limit, the animation is smooth and stable.

The optional parameter `r` lets you advance several ticks at once. DrawZero will
run the internal frame update `r` times back-to-back. This is helpful when you
want to fast-forward your simulation without redrawing in between. Most programs
keep the default value `1`.

Besides the timing, `tick()` empties the window event queue. It collects all new
mouse moves, button clicks, and key presses so you can read them from the global
lists in `drawzero.utils.events`. If you skip `tick()`, you will not see user
input and the window may stop responding.

### `sleep(t=1)`

```python
def sleep(t=1):
    """Sleep for t seconds

    :param t: Number of seconds to sleep
    """
```

`sleep()` pauses the program for a longer time. Internally it is just a loop of
`t * 30` calls to `tick()`, so the window continues to process events. Use this
when you need a break between animation phases. Example: show a text for two
seconds before you start moving objects.

```python
clear()
text('white', 'Ready...', (400, 320), fontsize=48)
sleep(2)
```

### `fps(fontsize=24)`

```python
def fps(fontsize=24, *, prev=[time()]):
    cur = time()
    diff = cur - prev[0]
    prev[0] = cur
    rate = int(1 / diff + 0.5)
    text('white', f'{rate} FPS', (1000, 000), fontsize, '>^')
```

Call `fps()` once per frame to draw a small counter in the upper-right corner.
It measures the time between the current call and the previous call, converts it
into frames per second, and writes the number on screen. Change `fontsize` if
you need bigger or smaller text.

If the number drops far below 30, your animation code is too slow. Try reducing
the amount of work you do each frame, or draw fewer very complex shapes.

## Working with frame-based motion

Because `tick()` keeps the loop at 30 FPS, you can describe motion in "pixels per
frame". For example, adding `5` to the x position each frame means the object
moves 150 pixels every second (`30 * 5`). If you want movement that stays the
same even when the frame rate changes, measure the actual time difference. You
can store the timestamp at the end of each loop using the `time()` function and
scale your motion by that delta.

```python
from time import time

x = 100
speed_per_second = 200  # pixels each second
prev_time = time()

while True:
    tick()
    now = time()
    dt = now - prev_time
    prev_time = now

    clear()
    x += speed_per_second * dt
    filled_circle('cyan', (x, 300), 30)
```

## Adding trails with transparent fills

To create comet-like trails, replace `clear()` with a dark transparent fill. The
old drawing will fade slowly, and the new drawing will appear on top.

```python
while True:
    tick()
    fill('black', alpha=20)      # low alpha = long trail
    filled_circle('lime', pos, 20)
```

You can also mix both methods: call `clear()` every few frames to reset the
screen, and use `fill()` with `alpha` in between to keep a shorter trail.

## Structuring larger animations

Here are some tips when your animation grows:

- Wrap your drawing code in functions to keep the `while True` loop small and
  easy to read.
- Keep calculations outside of the drawing commands. Update positions first,
  then draw everything.
- Use `tick()` only once per frame. If you call it several times, your animation
  will slow down because the function may wait after each call.
- Remember that `sleep()` also calls `tick()` internally. This means the window
  stays responsive even during pauses.
- Monitor the FPS counter during development. A steady value around 30 means
  your loop is healthy.

## More practice ideas

1. Make a bouncing ball that changes direction when it hits the window edge.
2. Draw a snake-like trail using `fill('black', alpha=10)` and a moving circle.
3. Create a night sky with moving stars. Use different speeds for each star and
   call `fps()` to make sure the loop stays fast.

Experiment with the examples above, combine the functions, and you will quickly
feel how the DrawZero animation loop works. Have fun creating your own animated
stories!
