# Just import everything | Импортируем всё
from drawzero import *

# Red rectangle with upper left corner at (50, 150) and width = 900, height = 700
# Красный прямоугольник с левым верхнем углом в точке(50, 150), шириной 900 и высотой 700
rect('red', (50, 150), 900, 700)

# Straight orange line from (100, 500) to (900, 500)
# Оранжевая прямая линия из точки (100, 500) в точку (900, 500)
line('orange', (100, 500), (900, 500))

# Centered text
# Центрированный текст
text('green', 'Hello world!', (500, 250), fontsize=72)
text('blue', 'Привет, мир!', (500, 750), fontsize=72)
