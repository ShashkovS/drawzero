from drawzero import *

# Animations are straightforward
for i in range(0, 60 * 5, 3):
    # Take color at "random"
    # Выбираем цвет псевдослучайно
    color = (i % 255, (19 * i) % 255, (91 * i) % 255)
    x = 100 + 2 * i
    y = 100 + i // 5
    r = 20 + 4 * (i % 5)
    circle(color, (x, y), r)
    # Sleep for 1/30 second
    # Самое главное для анимации — ждём 1/30 секунды
    tick()
