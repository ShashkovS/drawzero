from drawzero import *


scale1 = Gradient([C.black, C.white], 0, 1000)
for x in range(0, 1000, 10):
    filled_rect(scale1(x), (x, 0), 10, 100)
text(C.white, 'scale1 = Gradient([C.black, C.white], 0, 1000)', (50, 100), 48, '<^')

scale2 = Gradient([C.green, C.yellow, C.magenta, C.red], 0, 1000)
for x in range(0, 1000, 10):
    filled_rect(scale2(x), (x, 200), 10, 100)
text(C.white, 'scale2 = Gradient([C.green, C.yellow, C.magenta, C.red], 0, 1000)', (50, 300), 32, '<^')

scale3 = Gradient([C.white, C.black, C.red, C.black, C.white], 200, 800)
for x in range(0, 1000, 10):
    filled_rect(scale3(x), (x, 400), 10, 100)
text(C.white, 'scale3 = Gradient([C.white, C.black, C.red, C.black, C.white], 200, 800)', (50, 500), 32, '<^')
