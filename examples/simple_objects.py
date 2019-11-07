from drawzero import *

window(700, 700)

line((100, 100), (200, 200), 'red')
line((100, 100), (200, 300), 'green')
circle((250, 50), 10, 'yellow')
filled_circle((250, 250), 10, 'brown')
text('Привет, мир!', (300, 300), 36, 'red')
rect('blue', (100, 300, 50, 50))
filled_rect('orange', (200, 300, 50, 50))
polygon('white', [(400, 400), (450, 400), (450, 350), (475, 475), (400, 400)])

screen.draw.line((120, 120), (220, 220), 'red')

for i in range(60 * 10):
    tick()
    circle((250 + i, 250 + i // 3), 10, 'yellow')
