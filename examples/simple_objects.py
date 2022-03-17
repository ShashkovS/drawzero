from random import randint

from drawzero import *

clear()
fill((50, 50, 50))

# Simple shapes
rect('red', (50, 50), 900, 900)
line('red', (400, 400), (800, 800))
line('blue', 200, 900, 900, 200)  # pairs or plain
circle('yellow', (500, 560), 200)
filled_circle('brown', (500, 500), 20)
text('red', 'Привет, мир!', (300, 200), 72)
rect('blue', (200, 600), 100, 100)
filled_rect('orange', (400, 600, 100, 100))  # tuple[x,y,w,h] is also OK
polygon('white', [(20, 200), (100, 240), (40, 160)])  # list of tuples
filled_polygon('burlywood', 200, 400, 130, 304, 20, 342, 20, 458, 130, 496, alpha=100)  # or just flattened

# Pygamezero compatibility
screen.draw.line('red', (240, 240), (440, 440))

# Alpha channel is straightforward
rect('yellow', (500, 100), 100, 700, line_width=30, alpha=255)  # via alpha
rect('#00FFFF', (520, 120), 100, 700, line_width=30, alpha=100)  # via alpha
filled_rect((0, 255, 0, 50), (100, 500), 700, 100)  # via rgba

# Dozens of shapes in cycles
for i in range(0, 1000, 8):
    line((randint(0, 90), 255 - randint(0, 90), randint(0, 90)), (i, 1000), (i, 900 - randint(0, 80)))

# Animations are straightforward
for i in range(60 * 5):
    circle((i % 255, (19 * i) % 255, (91 * i) % 255), (100 + 2 * i, 100 + i // 5), 20 + 4 * (i % 5))
    tick()
