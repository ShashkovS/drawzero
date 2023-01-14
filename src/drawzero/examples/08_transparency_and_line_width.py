from drawzero import *

filled_circle('red', (100, 100), 20)
filled_circle('blue', (100, 110), 22, alpha=100)
circle('red', (100, 100), 50, line_width=10)
circle((0, 255, 0, 50), (100, 110), 50, line_width=10)

filled_rect(C.aquamarine, (200, 100), 100, 40)
filled_rect(C.darkmagenta, (210, 110), 100, 40, alpha=80)
rect(C.darkgoldenrod, (180, 90), 200, 80, line_width=10)
rect(C.hotpink, (190, 90), 200, 90, alpha=180, line_width=10)

line('red', 600, 400, 600, 990)

polygon('yellow', [(20, 300), (100, 340), (40, 260)], line_width=20)
polygon((0, 0, 255, 200), [(20, 300), (100, 340), (40, 260)], line_width=15)
polygon('red', [(20, 300), (100, 340), (40, 260)])

filled_polygon('burlywood', 200, 600, 130, 504, 20, 542, 20, 658, 130, 696)
filled_polygon(C.hotpink, 200, 700, 130, 604, 20, 642, 20, 758, 130, 796, alpha=100)

line(C.green, (700, 100), (800, 200))
line(C.green, (710, 100), (810, 200), line_width=5)
line(C.red, (820, 100), (720, 200), line_width=10, alpha=50)
line(C.blue, (830, 100), (730, 200), line_width=10, alpha=128)

# Alpha channel is straightforward
rect('yellow', (500, 100), 100, 700, line_width=30, alpha=255)  # via alpha
rect('#00FFFF', (520, 120), 100, 700, line_width=30, alpha=100)  # via alpha
filled_rect((0, 255, 0, 50), (100, 500), 700, 100)  # via rgba

ellipse('grey', (100, 850), 200, 100, alpha=100)
filled_ellipse('red', (100 + 50, 850 + 25), 100, 50, alpha=100)
arc('blue', (200, 850), 200, 100, start_angle=45, stop_angle=270, alpha=100, line_width=10)

fill(C.magenta, alpha=30)
