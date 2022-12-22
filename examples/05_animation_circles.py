from drawzero import *

# Animations are straightforward
for i in range(60 * 5, 3):
    color = (i % 255, (19 * i) % 255, (91 * i) % 255)
    x = 100 + 2 * i
    y = 100 + i // 5
    r = 20 + 4 * (i % 5)
    circle(color, (x, y), r)
    tick()  # Sleep for 1/30 second
