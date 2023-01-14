from drawzero import *

# All simple shapes

# Fill with color rgb=(50, 50, 50)
fill((50, 50, 50))

# Grid
grid()
text('white', "grid()", (500, 50), 32, '<.')

# Straight line
line('red', (100, 50), (300, 150))
text('white', "line('red', (100, 50), (300, 150))", (500, 100), 32, '<.')

# Circles
circle('yellow', (300, 200), 100)
filled_circle('brown', (100, 200), 50)
text('white', "circle('yellow', (300, 200), 100)", (500, 200 - 20), 32, '<.')
text('white', "filled_circle('brown', (100, 200), 50)", (500, 200 + 20), 32, '<.')

# Rectangles
rect('violet', (100, 300), 100, 200)
filled_rect('yellow', (250, 350, 50, 100))  # tuple[x,y,w,h] is also OK
filled_rect_rotated('red', (350, 350), 50, 100, 135)
rect_rotated('green', (350, 350), 50, 100, 45)
text('white', "rect('violette', (100, 300), 100, 200)", (500, 400 - 40 - 20), 32, '<.')
text('white', "filled_rect('yellow', (250, 350, 50, 100))", (500, 400 - 20), 32, '<.')
text('white', "filled_rect_rotated('red',(350,350),50,100,135)", (500, 400 + 20), 32, '<.')
text('white', "rect_rotated('green', (350, 350), 50, 100, 45)", (500, 400 + 40 + 20), 32, '<.')

# Polygons
filled_polygon('white', [(100, 600), (200, 640), (140, 560)])  # list oftuples
polygon('white', 430, 550, 374, 626, 285, 597, 285, 502, 374, 473)  # or just flattened
text('white', "filled_polygon('white', [(100, 600),(200,640),(140,560)])", (500, 600 - 40), 24, '<.')
text('white', "polygon('white', 430,550,374,626,285,597,285,502,374,473)", (500, 600), 24, '<.')

# Ellipsis and arcs
ellipse('grey', (100, 650), 200, 100)
arc('grey', (300, 650), 200, 100, start_angle=45, stop_angle=270)
arc('red', (350, 650), 100, 100, start_angle=45, stop_angle=270)
text('white', "ellipse('grey', (100, 650), 200, 100)", (500, 700 - 40), 32, '<.')
text('white', "arc('grey', (300, 650), 200, 100, 45, 270)", (500, 700), 32, '<.')
text('white', "arc('red', (350, 650), 100, 100, 45, 270)", (500, 700 + 40), 32, '<.')

# Text
text('red', 'Hello, world!', (100, 800), 48, '<.')
text('white', "text('red', 'Hello, world!', (100, 800), 48, '<.')", (500, 800), 32, '<.')

text(C.magenta, 'text', (200, 900), 48, '>v')
text(C.red, '×', (200, 900), 72, '..')
text(C.magenta, 'align', (200, 900), 48, '<^')
text('white', "text(C.magenta, 'text', (200, 900), 48, '>v')", (500, 860), 32, '<.')
text('white', "text(C.red, '×', (200, 900), 72, '..')", (500, 900), 32, '<.')
text('white', "text(C.magenta, 'align', (200, 900), 48, '<^')", (500, 940), 32, '<.')
