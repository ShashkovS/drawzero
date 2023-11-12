"""
In this example we use Pt class for turtle-like coordinate manipulations.
Используем класс Pt, позволяющий менять координаты в "черепашьем" стиле
"""
from drawzero import *

screen_center = Pt(500, 500)

small_rect_size = Pt(50, 30)
small_rect_center = screen_center + Pt(300, 0)

big_rect_size = Pt(100, 80)
big_rect_center = screen_center.copy()
for i in range(720):
    # First we make all calculations for the next frame

    # Rotate the big rectangle left by 3 degrees
    big_rect_center.left(3)
    # Line from the center outside the canvas using big rect heading
    laser = big_rect_center.copy().forward(700)
    # Rotate the small rect around the screen center for 1 degree
    small_rect_center.rotate_around(1, screen_center)
    # Rotate the small rect by 5 degrees
    small_rect_center.right(5)

    # Sleep 1/30 second
    tick()
    # No we clear the canvas and draw the next frame
    clear()

    # We need to subtract size/2 to get left upper rect position
    filled_rect_rotated(C.green, big_rect_center - big_rect_size / 2, big_rect_size, angle=big_rect_center.heading)
    # Sometimes we draw laser
    if i % 37 <= 4:
        line(C.orange, screen_center, laser, line_width=10, alpha=140)
    # Transparent small rectangle orbit
    circle(C.yellow, screen_center, 300, line_width=1, alpha=50)
    filled_rect_rotated(C.red, small_rect_center - small_rect_size / 2, small_rect_size, angle=small_rect_center.heading)
    circle(C.violet, screen_center, 10)
