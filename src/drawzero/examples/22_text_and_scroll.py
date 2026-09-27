from drawzero import *

value = ''
scroll_x = scroll_y = 0
composition = ''
while True:
    for event in events():
        if event.type == E.TEXT_INPUT:
            value += event.text
            composition = ''
        elif event.type == E.TEXT_EDITING:
            composition = event.text
        elif event.type == E.KEY_DOWN and event.key == K.BACKSPACE:
            value = value[:-1]
        elif event.type == E.FOCUS_LOST:
            composition = ''
    dx, dy = mouse.wheel
    scroll_x += dx
    scroll_y += dy
    clear()
    text(C.white, 'TEXT / TWO-DIMENSIONAL SCROLL', (500, 70), 40)
    text(C.white, 'Type text; Backspace deletes; scroll moves the marker', (500, 150), 28)
    text(C.cyan, value, (80, 300), 48, '<.')
    text(C.gray, composition, (80, 370), 36, '<.')
    text(C.yellow, f'Scroll: ({scroll_x:.1f}, {scroll_y:.1f})', (500, 480), 36)
    line(C.gray, (200, 720), (800, 720))
    line(C.gray, (500, 570), (500, 870))
    filled_circle(C.orange, (500 + 30 * scroll_x, 720 - 30 * scroll_y), 22)
    tick(fps=60)
