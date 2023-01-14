from drawzero import *

# Canvas is always 1000×1000
# Размер холста всегда 1000×1000

# Coordinate grid
# Координатная сетка для упрощения рисования
grid()

# (100, 200) -> (600, 800)
line('red', (100, 200), (600, 800))

# ┌─ at (600, 100), width=200, height=300
filled_rect('blue', (600, 100), 200, 300)

# Center at (300, 800), radius = 50
circle('green', (300, 800), 50)

# Center of text at (800, 600)
text('yellow', '(800, 600)', (800, 600))
