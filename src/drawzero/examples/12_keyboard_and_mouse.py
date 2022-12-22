from drawzero import *

typed_letters = 'Typed: '
SIZE = 20
x = y = 500 - SIZE // 2

while True:
    # Mouse buttons events
    if mousebuttonsdown:
        x, y = mousebuttonsdown[0].pos
    # Keys which are still pressed
    keys = get_keys_pressed()
    dx = dy = 0
    if keys[K.LEFT] or keys[K.a]:
        dx = -5
    if keys[K.RIGHT] or keys[K.d]:
        dx = +5
    if keys[K.UP] or keys[K.w]:
        dy = -5
    if keys[K.DOWN] or keys[K.s]:
        dy = +5
    if keys[K.MOD_SHIFT] or keys[K.MOD_CTRL]:
        dx *= 4
        dy *= 4
    x += dx
    y += dy
    # Keyboard events
    for ev in keysdown:
        if ev.unicode:
            typed_letters += ev.unicode

    # Redraw everything
    clear()
    text(C.white, 'Press arrows to move square', (500, 70), 48)
    text(C.white, 'Press letters to type them', (500, 130), 48)
    text(C.white, 'Click mouse to move square', (500, 190), 48)
    text(C.green, typed_letters, (100, 250), 48, align='<.')
    filled_rect(C.red, x, y, SIZE, SIZE)
    filled_circle(C.yellow, mouse_pos(), 3)
    tick()
