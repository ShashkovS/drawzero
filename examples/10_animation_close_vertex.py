from drawzero import *
from random import randint, uniform
from math import hypot

NUM_POINTS = 100
MIN_DIST = 150
MAX_SPEED = 4
points = [[randint(0, 1000), randint(0, 1000), uniform(-MAX_SPEED, MAX_SPEED), uniform(-MAX_SPEED, MAX_SPEED)] for __ in range(NUM_POINTS)]
pallet = ['#88dfe7', '#70d2e6', '#5cc3e6', '#43afe5', '#2a97e5', '#177ade', '#1160d0', '#0c46bb', '#082fa6', '#051d94', '#020c7e', '#000066']
for i in range(30*30):
    clear()
    for i in range(len(points) - 1):
        x1, y1, vx1, vy1 = points[i]
        for j in range(i+1, len(points)):
            x2, y2, vx2, vy2 = points[j]
            dist = hypot(x2-x1, y2-y1)
            if dist < MIN_DIST:
                color = pallet[int(dist / MIN_DIST * (len(pallet)-1) + 0.4999)]
                line(color, x1, y1, x2, y2, line_width=1)
    for i, (x, y, vx, vy) in enumerate(points):
        filled_circle('blue', (x, y), 5)
        points[i][0] = (x + vx) % 1000
        points[i][1] = (y + vy) % 1000
    tick()
