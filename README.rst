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


.. |Hello world image| image:: ./doc/hello_world.png?raw=true

Animation
---------

Animations are also straightforward::

    from drawzero import *
    from math import sin, cos, pi
    earth_orbit = 400
    earth_radius = 30
    earth_rot_step = 2 * pi / 360
    moon_orbit = 100
    moon_radius = 10
    moon_rot_step = 2 * pi / 60

    filled_circle(c_red, (500, 500), 100)
    i = 0
    while True:
        i += 1
        e_x = 500 + earth_orbit * cos(earth_rot_step * i)
        e_y = 500 + earth_orbit * sin(earth_rot_step * i)
        m_x = e_x + moon_orbit * cos(moon_rot_step * i)
        m_y = e_y + moon_orbit * sin(moon_rot_step * i)

        filled_circle(c_blue, (e_x, e_y), earth_radius)
        filled_circle(c_yellow, (m_x, m_y), moon_radius)
        tick()
        filled_circle(c_black, (e_x, e_y), earth_radius)
        filled_circle(c_black, (m_x, m_y), moon_radius)

.. |Animation gif| image:: ./doc/planet_animation.gif?raw=true

Installation
------------

In a Terminal window, type::

    pip install drawzero

