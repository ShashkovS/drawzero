from drawzero import *

#  colors
red_on = C.red
red_off = (150, 43, 21)
yellow_on = C.yellow
yellow_off = (195, 199, 90)
green_on = C.green
green_off = (59, 115, 74)

fill(C.white)


def traf_light(red, yellow, green):
    filled_rect(C.black, (400, 300, 200, 480))
    filled_circle(green, (500, 680), 60)
    filled_circle(yellow, (500, 540), 60)
    filled_circle(red, (500, 400), 60)


for i in range(3):
    traf_light(red_on, yellow_off, green_off)
    sleep(1)
    traf_light(red_off, yellow_on, green_off)
    sleep(1)
    traf_light(red_off, yellow_off, green_on)
    sleep(1)
    traf_light(red_off, yellow_on, green_off)
    sleep(1)
