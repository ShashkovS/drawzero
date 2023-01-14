from drawzero import *
from random import randint, seed

# Fill with color #003366 (Dark midnight blue)
# Заливка цветом #003366 (Dark midnight blue)
fill('#003366')

# Dozens of shapes
for x in range(0, 1000, 8):
    red = randint(0, 90)
    green = 255 - randint(0, 90)
    blue = randint(0, 90)
    random_green_color = (red, green, blue)
    height = 200 + randint(0, 80)
    line(random_green_color, (x, 1000 - height), (x, 1000))
