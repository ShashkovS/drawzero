"""
A Pt class — is a 2 dimensional vector class with point-like interface.
Can be used as coordinates for all drawing functions
"""

from math import sin, cos, atan2, pi, hypot


class Pt:
    """A point which acts as 2-d vector and as a Turtle

    Provides (for a, b — points, k number):
      * arithmetic
        a+b — vector addition
        a-b — vector subtraction
        k*a and a*k — multiplication with scalar
        |a| — absolute value of a
        +a, -a
      * turtle-style movement
        forward — Move the point forward by the specified distance.
        backward — Move the point backward by distance.
        right — Turn point right by angle degrees.
        left — Turn point left by angle degrees.
        goto — Move point to an absolute position.
        rotate_around — Rotate around given point by angle degrees.
        move_towards — Move towards the given point by the specified distance.
        reset, home — Move point to the origin - coordinates (0,0), set heading=0
        setx — Set the point's first coordinate to x
        sety — Set the point's second coordinate to y
        setheading — Set the point's heading
      * information
        position — Return the point's current location (x,y), as a tuple.
        x, xcor — Return the point's x coordinate.
        y, ycor — Return the point's y coordinate
        heading — Return the point's heading
        distance — Return the distance between points
        towards — Return the angle towards point
      * deep copy
        copy — a clone of point
    """
    __slots__ = ['x', 'y', 'heading', '_heading_rad']

    def __init__(self, x=0.0, y=0.0, *, heading=0.0):
        """
        Creates a point with given coordinates and heading angle (given in degrees)
        :param x: x coordinate
        :param y: y coordinate
        :param heading: hading angle in degrees
        """
        self.x = x
        self.y = y
        self.heading = heading
        self._heading_rad = heading / 180.0 * pi

    def __add__(self, other):
        """ Add two points
        Example:
        >>> p1 = Pt(1, 2)
        >>> p2 = Pt(3, 4)
        >>> p1 + p2
        Pt(4,6,heading=0.0)
        """
        return Pt(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        """ Add two points
        Example:
        >>> p1 = Pt(1, 2)
        >>> p2 = Pt(3, 4)
        >>> p1 += p2
        >>> p1
        Pt(4,6,heading=0.0)
        """
        self.x += other.x
        self.y += other.y
        return self

    def __mul__(self, other):
        """ Multiply by number
        Example:
        >>> p = Pt(1, 2)
        >>> p * 3
        Pt(3,6,heading=0.0)
        >>> -2 * p
        Pt(-2,-4,heading=0.0)
        """
        if isinstance(other, _NUMERIC):
            return Pt(self.x * other, self.y * other)
        return NotImplemented

    def __rmul__(self, other):
        """ Multiply by number
        Example:
        >>> p = Pt(1, 2)
        >>> p * 3
        Pt(3,6,heading=0.0)
        >>> -2 * p
        Pt(-2,-4,heading=0.0)
        """
        if isinstance(other, _NUMERIC):
            return Pt(self.x * other, self.y * other)
        return NotImplemented

    def __truediv__(self, other):
        """ Multiply by number
        Example:
        >>> p = Pt(4, 6)
        >>> p / 2
        Pt(2.0,3.0,heading=0.0)
        """
        if isinstance(other, _NUMERIC):
            return Pt(self.x / other, self.y / other)
        return NotImplemented

    def __sub__(self, other):
        """ Substract two points
        Example:
        >>> p1 = Pt(1, 2)
        >>> p2 = Pt(3, 4)
        >>> p1 - p2
        Pt(-2,-2,heading=0.0)
        """
        return Pt(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        """ Add two points
        Example:
        >>> p1 = Pt(1, 2)
        >>> p2 = Pt(3, 4)
        >>> p1 -= p2
        >>> p1
        Pt(-2,-2,heading=0.0)
        """
        self.x -= other.x
        self.y -= other.y
        return self

    def __neg__(self):
        """
        Example:
        >>> p1 = Pt(1, 2)
        >>> -p1
        Pt(-1,-2,heading=0.0)
        """
        return Pt(-self.x, -self.y, heading=self.heading)

    def __pos__(self):
        """
        Example:
        >>> p1 = Pt(1, 2)
        >>> +p1
        Pt(1,2,heading=0.0)
        """
        return Pt(self.x, self.y, heading=self.heading)

    def copy(self):
        """
        Example:
        >>> p1 = Pt(1, 2)
        >>> p2 = p1.copy()
        >>> p1.forward(10)
        >>> p1
        Pt(11.0,2.0,heading=0.0)
        >>> p2
        Pt(1,2,heading=0.0)
        """
        return Pt(self.x, self.y, heading=self.heading)

    def __abs__(self):
        """
        Example:
        >>> p1 = Pt(3, 4)
        >>> abs(p1)
        5.0
        """
        return hypot(self.x, self.y)

    def __str__(self):
        """ Human readeable
        Example:
        >>> p1 = Pt(100/3, 200/9)
        >>> print(str(p1))
        (33.33,22.22)
        """
        return f"({self.x:.2f},{self.y:.2f})"

    def __repr__(self):
        """ Exact representation
        Example:
        >>> p1 = Pt(100/3, 200/9, heading=30)
        >>> print(repr(p1))
        Pt(33.333333333333336,22.22222222222222,heading=30)
        """
        return f"Pt({self.x},{self.y},heading={self.heading})"

    def __iter__(self):
        """
        Example:
        >>> p1 = Pt(1, 2)
        >>> [*p1]
        [1, 2]
        """
        yield self.x
        yield self.y

    def __getitem__(self, item):
        """
        Example:
        >>> p = Pt(1, 2)
        >>> p[0]
        1
        >>> p[1]
        2
        >>> p[:2]
        [1, 2]
        """
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == slice(None, 2, None) or item == slice(0, 2, None):
            return [self.x, self.y]
        else:
            raise IndexError('Point index out of range')

    def __len__(self):
        """
        Example:
        >>> p1 = Pt(1, 2)
        >>> len(p1)
        2
        """
        return 2

    def reset(self):
        """Move point to the origin - coordinates (0,0).

        No arguments.

        Move point to the origin - coordinates (0,0) and set its
        heading to its start-orientation (which depends on mode).

        Example (for a Point instance named point):
        >>> point = Pt(1, 2)
        >>> point.reset()
        >>> point
        Pt(0,0,heading=0)
        """
        self.x = 0
        self.y = 0
        self.heading = 0
        self._heading_rad = 0

    def forward(self, distance):
        """Move the point forward by the specified distance.

        Aliases: forward | fd

        Argument:
        distance -- a number (integer or float)

        Move the point forward by the specified distance, in the direction
        the point is headed.

        Example (for a Point instance named point):
        >>> point = Pt(0, 0)
        >>> point.position()
        (0, 0)
        >>> point.forward(25)
        >>> point.position()
        (25.0, 0.0)
        >>> point.forward(-75)
        >>> point.position()
        (-50.0, 0.0)
        """
        self.x += distance * cos(self._heading_rad)
        self.y += distance * sin(self._heading_rad)

    fd = forward

    def back(self, distance):
        """Move the point backward by distance.

        Aliases: back | backward | bk

        Argument:
        distance -- a number

        Move the point backward by distance, opposite to the direction the
        point is headed. Do not change the point's heading.

        Example (for a Point instance named point):
        >>> point = Pt(0, 0)
        >>> point.position()
        (0, 0)
        >>> point.backward(30)
        >>> point.position()
        (-30.0, 0.0)
        """
        self.x -= distance * cos(self._heading_rad)
        self.y -= distance * sin(self._heading_rad)

    backward = bk = back

    def right(self, angle):
        """Turn point right by angle degrees.

        Aliases: right | rt

        Argument:
        angle -- a number (integer or float)

        Turn point right by angle degrees.

        Example (for a Point instance named point):
        >>> point = Pt(0, 0, heading=22)
        >>> point.heading
        22
        >>> point.right(45)
        >>> point.heading
        337.0
        """
        self.heading = (self.heading - angle) % 360.0
        self._heading_rad = self.heading / 180.0 * pi

    rt = right

    def left(self, angle):
        """Turn point left by angle degrees.

        Aliases: left | lt

        Argument:
        angle -- a number (integer or float)

        Turn point left by angle degrees.

        Example (for a Point instance named point):
        >>> point = Pt(0, 0, heading=22)
        >>> point.heading
        22
        >>> point.left(45)
        >>> point.heading
        67.0
        """
        self.heading = (self.heading + angle) % 360.0
        self._heading_rad = self.heading / 180.0 * pi

    lt = left

    def pos(self) -> tuple:
        """Return the point's current location (x,y), as a Pt-vector.

        Aliases: pos | position

        No arguments.

        Example (for a Point instance named point):
        >>> point = Pt(0, 240)
        >>> point.position()
        (0, 240)
        """
        return round(self.x, 10), round(self.y, 10)

    position = pos

    def xcor(self):
        """Return the point's x coordinate.

        No arguments.

        Example (for a Point instance named point):
        >>> point = Pt()
        >>> point.left(60)
        >>> point.forward(100)
        >>> print(point.xcor())
        50.0
        """
        return round(self.x, 10)

    def ycor(self):
        """Return the point's y coordinate
        ---
        No arguments.

        Example (for a Point instance named point):
        >>> point = Pt()
        >>> point.left(60)
        >>> point.forward(100)
        >>> print(point.ycor())
        86.6025403784
        """
        return round(self.y, 10)

    def goto(self, x=None, y=None):
        """Move point to an absolute position.

        Aliases: setpos | setposition | goto:

        Arguments:
        x -- a number      or     a pair/vector of numbers
        y -- a number             None

        call: goto(x, y)         # two coordinates
        --or: goto((x, y))       # a pair (tuple) of coordinates
        --or: goto(pt)          # e.g. as returned by pos()

        Move point to an absolute position.
        The point's orientation does not change.

        Example (for a Point instance named point):
        >>> tp = Pt(0, 0)
        >>> tp
        Pt(0,0,heading=0.0)
        >>> point = Pt()
        >>> point.setpos(60,30)
        >>> point.position()
        (60, 30)
        >>> point.setpos((20,80))
        >>> point.position()
        (20, 80)
        >>> point.setpos(tp)
        >>> point.position()
        (0, 0)
        """
        if isinstance(x, Pt):
            self.x = x.x
            self.y = x.y
        elif isinstance(x, _PT_LIKE):
            self.x = x[0]
            self.y = x[1]
        elif x is not None:
            self.x = x
        if y is not None:
            self.y = y

    setpos = goto
    setposition = goto

    def rotate_around(self, angle, x, y=None):
        """rotate self counterclockwise by angle around point (x, y) (or x if x is Pt, tuple, or list)
        Example (for a Point instance named point):
        >>> tp = Pt(1, 0)
        >>> tp.rotate_around(90, (0, 0))
        >>> tp.position()
        (0.0, 1.0)
        >>> tp.rotate_around(90, Pt(0, 0))
        >>> tp.position()
        (-1.0, 0.0)
        >>> tp.rotate_around(90, 0, 0)
        >>> tp.position()
        (-0.0, -1.0)
        >>> tp.rotate_around(180, [2, 3])
        >>> tp.position()
        (4.0, 7.0)
        """
        if isinstance(x, Pt):
            px = x.x
            py = x.y
        elif isinstance(x, _PT_LIKE):
            px = x[0]
            py = x[1]
        else:
            px = x
            py = y
        dx = self.x - px
        dy = self.y - py
        angle_rad = angle * pi / 180.0
        c, s = cos(angle_rad), sin(angle_rad)
        ndx = dx * c + -dy * s
        ndy = dx * s + dy * c
        self.x, self.y = px + ndx, py + ndy

    def home(self):
        """Move point to the origin - coordinates (0,0).

        No arguments.

        Move point to the origin - coordinates (0,0) and set its
        heading to its start-orientation (which depends on mode).

        Example (for a Point instance named point):
        >>> point = Pt(1, 2)
        >>> point.home()
        >>> point
        Pt(0,0,heading=0)
        """
        self.x = 0
        self.y = 0
        self.heading = 0
        self._heading_rad = 0

    def setx(self, x):
        """Set the point's first coordinate to x

        Argument:
        x -- a number (integer or float)

        Set the point's first coordinate to x, leave second coordinate
        unchanged.

        Example (for a Point instance named point):
        >>> point = Pt(0, 240)
        >>> point.position()
        (0, 240)
        >>> point.setx(10)
        >>> point.position()
        (10, 240)
        """
        self.x = x

    def sety(self, y):
        """Set the point's second coordinate to y

        Argument:
        y -- a number (integer or float)

        Set the point's first coordinate to x, second coordinate remains
        unchanged.

        Example (for a Point instance named point):
        >>> point = Pt(0, 40)
        >>> point.position()
        (0, 40)
        >>> point.sety(-10)
        >>> point.position()
        (0, -10)
        """
        self.y = y

    def distance(self, x, y=None):
        """Return the distance from the point to (x,y) in point step degrees.

        Arguments:
        x -- a number   or  a pair/vector of numbers   or   a point instance
        y -- a number       None                            None

        call: distance(x, y)         # two coordinates
        --or: distance((x, y))       # a pair (tuple) of coordinates
        --or: distance(pt)           # e.g. as returned by pos()

        Example (for a Point instance named point):
        >>> point = Pt(0, 0)
        >>> point.position()
        (0, 0)
        >>> point.distance(30,40)
        50.0
        >>> pen = Pt()
        >>> pen.forward(77)
        >>> point.distance(pen)
        77.0
        """
        if isinstance(x, Pt):
            return hypot(self.x - x.x, self.y - x.y)
        elif isinstance(x, _PT_LIKE):
            return hypot(self.x - x[0], self.y - x[1])
        else:
            return hypot(self.x - x, self.y - y)

    def towards(self, x, y=None):
        """Return the angle of the line from the point's position to (x, y).

        Arguments:
        x -- a number   or  a pair/vector of numbers   or   a point instance
        y -- a number       None                            None

        call: distance(x, y)         # two coordinates
        --or: distance((x, y))       # a pair (tuple) of coordinates
        --or: distance(pt)          # e.g. as returned by pos()

        Return the angle in degrees, between the line from point-position to position
        specified by x, y and the point's start orientation.

        Example (for a Point instance named point):
        >>> point = Pt(10, 10)
        >>> point.position()
        (10, 10)
        >>> point.towards(0, 0)
        225.0
        >>> point.towards((20, 10))
        0.0
        >>> point.towards([10, 20])
        90.0
        >>> point.towards(Pt(0, 20))
        135.0
        >>> point.towards((10, 0))
        270.0
        """
        if isinstance(x, Pt):
            angle_rad = atan2(x.y - self.y, x.x - self.x)
        elif isinstance(x, _PT_LIKE):
            angle_rad = atan2(x[1] - self.y, x[0] - self.x)
        else:
            angle_rad = atan2(y - self.y, x - self.x)
        return round(angle_rad * 180.0 / pi, 10) % 360.0

    def move_towards(self, distance, x, y=None):
        """Move towards the given point by the specified distance.

        Arguments:
        distance -- a number (integer or float)
        x -- a number   or  a pair/vector of numbers   or   a point instance
        y -- a number       None                            None

        call: move_towards(100, x, y)         # two coordinates
        --or: move_towards(100, (x, y))       # a pair (tuple) of coordinates
        --or: move_towards(100, pt)          # e.g. as returned by pos()

        Return the angle in degrees, between the line from point-position to position
        specified by x, y and the point's start orientation.

        Example (for a Point instance named point):
        >>> point = Pt(10, 10)
        >>> point.position()
        (10, 10)
        >>> point.move_towards(20, 100, 10)
        >>> point.position()
        (30.0, 10.0)
        >>> point.move_towards(20, (30, 0))
        >>> point.position()
        (30.0, -10.0)
        """
        if isinstance(x, Pt):
            px = x.x
            py = x.y
        elif isinstance(x, _PT_LIKE):
            px = x[0]
            py = x[1]
        else:
            px = x
            py = y
        dx = px - self.x
        dy = py - self.y
        dist = hypot(dx, dy)
        if dist != 0:
            coef = distance / hypot(dx, dy)
            self.x += dx * coef
            self.y += dy * coef

    def setheading(self, to_angle):
        """Set the orientation of the point to to_angle.

        Aliases:  setheading | seth

        Argument:
        to_angle -- a number (integer or float)

        Set the orientation of the point to to_angle.

         standard - mode:
        -----------------
           0 - east
          90 - north
         180 - west
         270 - south

        Example (for a Point instance named point):
        >>> point = Pt(0, 0)
        >>> point.setheading(90)
        >>> point.heading
        90.0
        """
        self.heading = to_angle % 360.0
        self._heading_rad = self.heading / 180.0 * pi

    seth = setheading


_PT_LIKE = (list, tuple)
_NUMERIC = (int, float)
