from drawzero import *

segments = []
previous = None
while True:
    for event in events():
        if event.type == E.FOCUS_LOST:
            previous = None
        elif event.type == E.MOUSE_DOWN and event.button == M.LEFT:
            previous = event.pos
        elif event.type == E.MOUSE_MOVE:
            if previous is not None and M.LEFT in event.buttons:
                segments.append((previous, event.pos))
                previous = event.pos
        elif event.type == E.MOUSE_UP and event.button == M.LEFT:
            if previous is not None and not event.source.cancelled:
                segments.append((previous, event.pos))
            previous = None
    if keyboard.just_pressed('space'):
        segments.clear()
    clear()
    text(C.white, 'PRECISE DRAWING', (500, 70), 48)
    text(C.white, 'Hold left mouse button to draw; Space clears', (500, 150), 32)
    for start, end in segments:
        line(C.cyan, start, end, line_width=6)
    filled_circle(C.yellow, mouse.pos, 8)
    text(C.gray, f'Path segments: {len(segments)}', (500, 900), 32)
    tick(fps=60)
