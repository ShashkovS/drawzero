from drawzero import *
from math import sin

line('blue', 0, 500, 1000, 500)
line('blue', 500, 0, 500, 1000)

for x1 in range(0, 1000, 3):
    x2 = x1 + 3
    line('red', x1, 500 + 100 * sin(x1 / 100), x2, 500 + 100 * sin(x2 / 100))
