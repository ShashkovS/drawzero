from drawzero import *
from math import sin, cos, pi

earth_orbit = 400
earth_radius = 30
earth_rot_step = 2 * pi / 360
moon_orbit = 100
moon_radius = 10
moon_rot_step = 2 * pi / 60

for i in range(360 * 2):
    e_x = 500 + earth_orbit * cos(earth_rot_step * i)
    e_y = 500 + earth_orbit * sin(earth_rot_step * i)
    m_x = e_x + moon_orbit * cos(moon_rot_step * i)
    m_y = e_y + moon_orbit * sin(moon_rot_step * i)

    clear()
    filled_circle(C.red, (500, 500), 100)
    filled_circle(C.blue, (e_x, e_y), earth_radius)
    filled_circle(C.yellow, (m_x, m_y), moon_radius)
    tick()
