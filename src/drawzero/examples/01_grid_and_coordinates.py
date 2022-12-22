from drawzero import *

# Canvas is always 1000×1000
# Размер холста всегда 1000×1000

# Coordinate grid
# Координатная сетка для упрощения рисования
grid()

line('red', (100, 200), (600, 800))

filled_rect('blue', (600, 100), 200, 300)

circle('green', (300, 800), 50)

text('yellow', '(800, 600)', (800, 600))
