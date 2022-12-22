from drawzero import *

circles = []
tick()
while True:
    x, y = mouse_pos()
    circles.append([x, y, 100])
    clear()
    for i in range(len(circles) - 1, -1, -1):
        x, y, r = circles[i]
        if r > 1000:
            circles.pop(i)
        else:
            circle('grey', x, y, r, line_width=1)
            circles[i][2] += 10
    tick()
