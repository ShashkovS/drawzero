from drawzero import *

# just coordinates
A = Pt(100, 100)
B = Pt(300, 150)
line(C.red, A, B)

# A point which acts as 2-d vector and as a Turtle
# Pt(x=0.0, y=0.0, *, heading=0.0)
#
# Provides (for a, b — points, k number):
#   * arithmetic
#     a+b — vector addition
#     a-b — vector subtraction
#     k*a and a*k — multiplication with scalar
#     abs  — absolute value of a
#     +a, -a

# arithmetic
A = Pt(100, 200)
dx = Pt(50, 5)
for i in range(10):
    filled_circle(C.blue, A + dx * i, radius=10)

#   * turtle-style movement
#     forward — Move the point forward by the specified distance.
#     backward — Move the point backward by distance.
#     right — Turn point right by angle degrees.
#     left — Turn point left by angle degrees.
#     goto — Move point to an absolute position.
#     rotate_around — Rotate around given point by angle degrees.
#     move_towards — Move towards the given point by the specified distance.
#     reset, home — Move point to the origin - coordinates (0,0), set heading=0
#     setx — Set the point's first coordinate to x
#     sety — Set the point's second coordinate to y
#     setheading — Set the point's heading

A = Pt(100, 300)
B = Pt(1000, 400)
for i in range(10):
    filled_circle(C.green2, A, radius=10)
    A.move_towards(50, B)

A = Pt(100, 400)
for i in range(10):
    filled_circle(C.magenta, A, radius=10)
    A.left(10).forward(30)

#   * information
#     position — Return the point's current location (x,y), as a tuple.
#     x, xcor — Return the point's x coordinate.
#     y, ycor — Return the point's y coordinate
#     heading — Return the point's heading
#     distance — Return the distance between points
#     towards — Return the angle towards point
#   * deep copy
#     copy — a clone of point
