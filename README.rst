Draw Zero
=========

A zero-boilerplate canvas drawing framework for Python 3, based on Pygame.


Some examples
-------------

Here's some of the neat stuff you can do::

    # import all
    from drawzero import *

    # simple shapes
    fill('#12bbae')
    line('red', (400, 400), (800, 800))
    circle('yellow', (500, 560), 200)
    filled_circle('brown', (500, 500), 20)
    text('red', 'Hello, world!', (300, 200), 72)
    rect('blue', (200, 600), 100, 100)
    filled_rect('orange', (400, 600), 100, 100)
    polygon('white', [(20, 200), (100, 240), (40, 160)])
    filled_polygon('burlywood', 200, 400, 130, 304, 20, 342, 20, 458, 130, 496, )
    # animation
    for i in range(60 * 5):
        tick()
        circle((i % 255, (19 * i) % 255, (91 * i) % 255), (100 + 2*i, 100 + i // 5), 20 + 4 * (i % 5))

Installation
------------

In a Terminal window, type::

    pip install drawzero

