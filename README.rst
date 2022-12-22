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


.. image:: https://raw.githubusercontent.com/ShashkovS/drawzero/master/docs/hello_world.png
    :width: 75%

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

    i = 0
    while True:
        i += 1
        e_x = 500 + earth_orbit * cos(earth_rot_step * i)
        e_y = 500 + earth_orbit * sin(earth_rot_step * i)
        m_x = e_x + moon_orbit * cos(moon_rot_step * i)
        m_y = e_y + moon_orbit * sin(moon_rot_step * i)

        clear()
        filled_circle(C.red, (500, 500), 100)
        filled_circle(C.blue, (e_x, e_y), earth_radius)
        filled_circle(C.yellow, (m_x, m_y), moon_radius)
        tick()


.. image:: https://raw.githubusercontent.com/ShashkovS/drawzero/master/docs/planet_animation.gif
    :width: 50%


Transparency
------------

Transparency is also straightforward via alpha or RGBA::

    from drawzero import *

    clear()
    fill(C.black)

    filled_circle('red', (100, 100), 20)
    filled_circle('blue', (100, 110), 22, alpha=100)
    circle('red', (100, 100), 50, line_width=10)
    circle((0, 255, 0, 50), (100, 110), 50, line_width=10)

    filled_rect(C.aquamarine, (200, 100), 100, 40)
    filled_rect(C.darkmagenta, (210, 110), 100, 40, alpha=80)
    rect(C.darkgoldenrod, (180, 90), 200, 80, line_width=10)
    rect(C.hotpink, (190, 90), 200, 90, alpha=180, line_width=10)

    line('red', 600, 400, 600, 990)
    image('cat.png', (500, 500))
    image('cat.png', (500, 800), width=200, alpha=128)
    image('cat.png', (550, 850), width=200, alpha=128)

    polygon('yellow', [(20, 300), (100, 340), (40, 260)], line_width=20)
    polygon((0, 0, 255, 200), [(20, 300), (100, 340), (40, 260)], line_width=15)
    polygon('red', [(20, 300), (100, 340), (40, 260)])

    filled_polygon('burlywood', 200, 600, 130, 504, 20, 542, 20, 658, 130, 696)
    filled_polygon(C.hotpink, 200, 700, 130, 604, 20, 642, 20, 758, 130, 796, alpha=100)

    line(C.green, (700, 100), (800, 200))
    line(C.green, (710, 100), (810, 200), line_width=5)
    line(C.red, (820, 100), (720, 200), line_width=10, alpha=50)
    line(C.blue, (830, 100), (730, 200), line_width=10, alpha=128)


.. image:: https://raw.githubusercontent.com/ShashkovS/drawzero/master/docs/transparent.png
    :width: 50%


Keyboard and mouse events
-------------------------

Process keyboard events in two ways: check if key is pressed via `get_keys_pressed()` or run throw `keysdown` or `keysup` events::


    from drawzero import *

    upper_text = 'Typed: '
    SIZE = 20
    x = y = 500 - SIZE // 2

    while True:
        # Mouse buttons events
        if mousebuttonsdown:
            x, y = mousebuttonsdown[0].pos
        # Keys which are still pressed
        keys = get_keys_pressed()
        if keys[K.UP] or keys[K.w]:
            y -= 5
        if keys[K.DOWN] or keys[K.s]:
            y += 5
        if keys[K.LEFT] or keys[K.a]:
            x -= 5
        if keys[K.RIGHT] or keys[K.d]:
            x += 5
        # Keyboard events
        for ev in keysdown:
            if ev.unicode:
                upper_text += ev.unicode

        # Redraw everything
        clear()
        filled_rect(C.red, x, y, SIZE, SIZE)
        text(C.white, upper_text, (100, 5))
        filled_circle(C.yellow, mouse_pos(), 3)
        tick()



.. image:: https://raw.githubusercontent.com/ShashkovS/drawzero/master/docs/keyboard_and_mouse_events.gif
    :width: 50%



Installation
------------

In a Terminal window, type::

    pip install drawzero --upgrade --user


Or run the following program::

    import os, sys
    python = sys.executable
    user = '--user' if 'venv' not in python else ''
    cmd = f'"{python}" -m pip install drawzero --upgrade {user}'
    print(cmd)
    os.system(cmd)
