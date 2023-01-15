from drawzero import *

# С — is an object with colors as attributes.
# С — специальный объект, у которого есть атрибуты — предопределённые цвета
# https://www.pygame.org/docs/ref/color_list.html
red_on = C.red
red_off = C.red4
yellow_on = C.yellow
yellow_off = C.yellow4
green_on = C.green
green_off = C.green4

fill(C.white)


def traf_light(red, yellow, green):
    """Function to draw signals with given colors
    """
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
