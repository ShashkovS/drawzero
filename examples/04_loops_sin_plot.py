from drawzero import *
from math import sin

line('blue', 0, 500, 1000, 500)
line('blue', 500, 0, 500, 1000)

STEP = 4
SCALE = 100
for x1 in range(0, 1000, STEP):
    y1 = 500 + SCALE * sin(x1 / SCALE)
    x2 = x1 + STEP
    y2 = 500 + SCALE * sin(x2 / SCALE)
    line('red', (x1, y1), (x2, y2))
