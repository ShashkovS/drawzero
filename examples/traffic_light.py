from drawzero import *

#  colors
red_on = c_red
red_off = (150, 43, 21)
yellow_on = c_yellow
yellow_off = (195, 199, 90)
green_on = c_green
green_off = (59, 115, 74)

fill(c_white)


def traf_light(red, yellow, green):
    filled_rect(c_black, (200, 150, 100, 240))
    filled_circle((250, 340), 30, green)
    filled_circle((250, 270), 30, yellow)
    filled_circle((250, 200), 30, red)


for i in range(5):
    traf_light(red_on, yellow_off, green_off)
    sleep(1)
    traf_light(red_off, yellow_on, green_off)
    sleep(1)
    traf_light(red_off, yellow_off, green_on)
    sleep(1)
    traf_light(red_off, yellow_on, green_off)
    sleep(1)
