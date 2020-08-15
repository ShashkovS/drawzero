from drawzero import *
from math import sin, cos


line('blue', 0, 500, 1000, 500)
line('blue', 500, 0, 500, 1000)

for i in range(0, 1000, 3):
    j = i + 3
    line('red', i, 500+100*sin(i/100), j, 500+100*sin(j/100))
