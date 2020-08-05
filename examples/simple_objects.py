from random import randint

from drawzero import *

clear()

rect('red', 50, 50, 900, 900)

fill((50, 50, 50))

line('red', (400, 400), (800, 800))
line('blue', 200, 900, 900, 200)
line('green', (200, 200), (400, 600))
circle('yellow', (500, 560), 200)
filled_circle('brown', (500, 500), 20)
text('red', 'Привет, мир!', (300, 200), 72)
rect('blue', (200, 600, 100, 100))
filled_rect('orange', (400, 600, 100, 100))
polygon('white', [(20, 200), (100, 240), (40, 160)])
filled_polygon('burlywood', 200, 400, 130, 304, 20, 342, 20, 458, 130, 496, )
screen.draw.line('red', (240, 240), (440, 440))

for i in range(0, 1000, 8):
    line((randint(0, 90), 255 - randint(0, 90), randint(0, 90)), (i, 1000), (i, 900 - randint(0, 80)))

for i in range(60 * 5):
    tick()
    circle((i % 255, (19 * i) % 255, (91 * i) % 255), (100 + 2*i, 100 + i // 5), 20 + 4 * (i % 5))
