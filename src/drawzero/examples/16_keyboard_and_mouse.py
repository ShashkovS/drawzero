from drawzero import *

x = y = 500
color = C.red
presses = 0
while True:
    speed = 12 if keyboard.pressed('shift') else 4
    dx = keyboard.axis(('left', 'a'), ('right', 'd'))
    dy = keyboard.axis(('up', 'w'), ('down', 's'))
    x += speed * dx
    y += speed * dy
    if keyboard.just_pressed('space'):
        presses += 1
        color = C.blue if color == C.red else C.red
    for event in events():
        if event.type == E.MOUSE_DOWN and event.button == M.LEFT:
            x, y = event.pos
    clear()
    text(C.white, 'CONTROLS / STATE', (500, 70), 48)
    text(C.white, 'Arrows or WASD move; Shift speeds up', (500, 150), 32)
    text(C.white, 'Space changes color once; click places the square', (500, 205), 30)
    text(C.cyan, f'Axis: ({dx}, {dy})   Shift: {keyboard.pressed("shift")}', (500, 300), 36)
    text(C.yellow, f'Space presses: {presses}', (500, 360), 36)
    filled_rect(color, (x, y), 35, 35)
    filled_circle(C.yellow, mouse.pos, 6)
    tick(fps=60)
