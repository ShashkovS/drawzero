from drawzero import *
from random import randint, seed

# Fill with color #003366 (Dark midnight blue)
# Заливка цветом #003366 (Dark midnight blue)
fill('#003366')

# Draw a vertical line every 8 "pixels"
# Будем рисовать линию через каждые 8 пунктов
for x in range(0, 1000, 8):
    # Color is defined by 3 components: red, greed and blue. Take them at random
    # Каждый цвет состоит из трёх компонент: красной, зелёной и синей. Выбираем их случайно
    red = randint(0, 90)
    green = 255 - randint(0, 90)
    blue = randint(0, 90)
    random_green_color = (red, green, blue)

    # Take line height at random too.
    # Высота тоже случайная
    height = 200 + randint(0, 80)

    # 1000 — is the bottom of the canvas
    # 1000 самый низ экрана
    line(random_green_color, (x, 1000 - height), (x, 1000))
