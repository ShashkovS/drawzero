"""
Draw Zero, a zero-boilerplate graphing library for education.

Functions:
line(color='red', start=(100, 100), end=(200, 200))
circle(color='red', pos=(100, 100), radius=10)
filled_circle(color='red', pos=(100, 100), radius=10)
rect(color='red', pos=(100, 100), width=500, height=200)
filled_rect(color='red', pos=(100, 100), width=500, height=200)
polygon(color='red', *points)
filled_polygon(color='red', *points)
text(color='red', text='', pos=(100, 100), fontsize=24)
clear()
fill(color='red')
blit(image, pos)
"""

__version__ = '0.1.10'

from .drawzero import *
