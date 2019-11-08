from random import randint

from drawzero import *

clear()

fill((50, 50, 50))
# blit('test1', (0,0))

line((100, 100), (200, 200), 'red')
line((100, 100), (200, 300), 'green')
circle((250, 280), 100, 'yellow')
filled_circle((250, 250), 10, 'brown')
text('Привет, мир!', (150, 100), 36, 'red')
rect('blue', (100, 300, 50, 50))
filled_rect('orange', (200, 300, 50, 50))
polygon('white', [(10, 100), (50, 120), (20, 80)])
filled_polygon('burlywood', 100, 200, 65, 152, 10, 171, 10, 229, 65, 248, )

screen.draw.line((120, 120), (220, 220), 'red')

for i in range(0, 500, 4):
    line((i, 500), (i, 450 - randint(0, 40)), (randint(0, 90), 255 - randint(0, 90), randint(0, 90)))

for i in range(60 * 5):
    tick()
    circle(
        (50 + i, 50 + i // 10),
        10 + 2 * (i % 5),
        (i % 255, (19 * i) % 255, (91 * i) % 255)
    )
