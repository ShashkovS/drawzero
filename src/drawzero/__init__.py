"""
drawzero
========
A zero-boilerplate canvas drawing framework for Python 3, based on Pygame.
"""

from .utils.draw import *
from .utils.pt import Pt
from .utils.gradient import Gradient
from .utils.copy_examples import copy_examples
from .utils.screen_size import set_virtual_size
from .utils.i18n import set_lang
from .utils.key_flags import K, KEY
from .utils.colors import C, COLORS, THECOLORS, ALL_COLORS
from .__about__ import __author__, __copyright__, __version__

__all__ = [
    # spec
    '__author__', '__copyright__', '__version__',
    # simple shapes
    'line', 'arc', 'circle', 'rect', 'ellipse', 'rect_rotated', 'polygon',
    # filled shapes
    'filled_circle', 'filled_rect', 'filled_ellipse', 'filled_rect_rotated', 'filled_polygon',
    # other
    'grid', 'text', 'clear', 'fill', 'image', 'fps', 'set_lang',
    # animation control
    'tick', 'sleep', 'quit',
    # keyboard and mouse
    'mouse_pos',
    # examples
    'copy_examples',
    # Point class
    'Pt',
    # Color consts (all are the same)
    'C', 'COLORS', 'THECOLORS', 'ALL_COLORS',
    # Keyboard key names
    'K', 'KEY',
    # Gradient tools
    'Gradient',
    # pygamezero compatibility
    'screen', 'set_virtual_size',
    # Mouse and keyboard events
    'get_keys_pressed', 'keys_mods_pressed', 'get_mouse_pressed', 'keysdown', 'keysup', 'mousemotions', 'mousebuttonsdown', 'mousebuttonsup',
]
