from drawzero import *

upper_text = 'Typed: '
SIZE = 20
x = y = 500 - SIZE // 2

while True:
    # Mouse buttons events
    if mousebuttonsdown:
        x, y = mousebuttonsdown[0].pos
    # Keys which are still pressed
    keys = get_keys_pressed()
    if keys[K.UP] or keys[K.w]:
        y -= 5
    if keys[K.DOWN] or keys[K.s]:
        y += 5
    if keys[K.LEFT] or keys[K.a]:
        x -= 5
    if keys[K.RIGHT] or keys[K.d]:
        x += 5
    # Keyboard events
    for ev in keysdown:
        if ev.unicode:
            upper_text += ev.unicode

    # Redraw everything
    clear()
    filled_rect(C.red, x, y, SIZE, SIZE)
    text(C.white, upper_text, (100, 5))
    filled_circle(C.yellow, mouse_pos(), 3)
    tick()
