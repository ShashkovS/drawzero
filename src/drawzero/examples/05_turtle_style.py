from drawzero import *

colors = [C.darkslategrey, C.dimgrey, C.slateblue, C.darkblue, C.yellowgreen, C.maroon,
          C.violetred, C.darkslategray, C.honeydew, C.mediumpurple, C.lightsalmon]

for n in range(3, 11):
    cur = Pt(500, 300 - 5*n)
    for i in range(n):
        prev = cur
        cur = cur.copy()
        cur.left(360 / n)
        cur.forward(200)
        line(colors[n], prev, cur)
