from drawzero import *
from random import randint, uniform
from itertools import combinations

NUM_POINTS = 100
MIN_DIST = 150
MAX_SPEED = 4
"""
Here we use Pt class for coordinates. It looks like a tuple with .x and .y methods (and many other).
Здесь мы используем класс Pt для работы с координатами. Почти кортеж, только изменяемый с атрибутами .x и .y
"""
points = [
    (Pt(randint(0, 1000), randint(0, 1000)), Pt(uniform(-MAX_SPEED, MAX_SPEED), uniform(-MAX_SPEED, MAX_SPEED)))
    for __ in range(NUM_POINTS)
]
scale = Gradient(['#5cc3e6', C.black], 0, MIN_DIST)

for i in range(30 * 30):
    # First we make all calculations for the next frame
    for pt, v in points:
        pt.x = (pt.x + v.x) % 1000
        pt.y = (pt.y + v.y) % 1000

    # Sleep 1/30 second
    tick()
    # No we clear the canvas and draw the next frame
    clear()

    for (pt1, v1), (pt2, v2) in combinations(points, r=2):
        dist = pt1.distance(pt2)
        if dist < MIN_DIST:
            color = scale(dist)
            line(color, pt1, pt2, line_width=1)
    for pt, v in points:
        filled_circle('blue', pt, 5)
    fps()
