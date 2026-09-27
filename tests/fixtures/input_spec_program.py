from drawzero import *

x = y = 500
radius = 20
color = C.red

while True:
    speed = 12 if keyboard.pressed("shift") else 4
    x += speed * keyboard.axis(("left", "a"), ("right", "d"))
    y += speed * keyboard.axis(("up", "w"), ("down", "s"))
    if keyboard.just_pressed("space"):
        color = C.blue if color == C.red else C.red
    for event in events():
        if event.type == E.MOUSE_DOWN and event.button == M.LEFT:
            x, y = event.pos
    wheel_x, wheel_y = mouse.wheel
    radius = max(5, min(100, radius + 2 * wheel_y))
    clear()
    filled_circle(color, (x, y), radius)
    filled_circle(C.yellow, mouse.pos, 3)
    tick(fps=60)
