from drawzero import *
from math import sin, cos, pi

filled_circle(c_red, (500, 500), 100)

r_e_o = 400
r_e_r = 30
phi_e = 2 * pi / 180

r_m_o = 100
r_m_r = 10
phi_m = 2 * pi / 15

for i in range(1000):
    e_x = 500 + r_e_o * cos(phi_e * i)
    e_y = 500 + r_e_o * sin(phi_e * i)
    m_x = e_x + r_m_o * cos(phi_m * i)
    m_y = e_y + r_m_o * sin(phi_m * i)

    filled_circle(c_blue, (e_x, e_y), r_e_r)
    filled_circle(c_yellow, (m_x, m_y), r_m_r)
    tick()
    filled_circle(c_black, (e_x, e_y), r_e_r)
    filled_circle(c_black, (m_x, m_y), r_m_r)
