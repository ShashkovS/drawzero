import os
from math import sin, cos, pi

from drawzero.utils.examples import copy_examples
from drawzero.utils.colors import C, COLORS, THECOLORS, ALL_COLORS
from drawzero.utils.pt import Pt

if not bool(os.environ.get('EJUDGE_MODE', False)):
    from drawzero.utils import renderer
else:
    from drawzero.utils import renderer_ejudge as renderer

VIRTUAL_SIZE = 1000

_ = lambda x: x  # That is for gettext localization
PT_LIKE = (tuple, list, Pt)
NUM_LIKE = (int, float)


K = KEY = renderer.key_flags
get_keys_pressed = renderer.get_keys_pressed
keys_mods_pressed = renderer.keys_mods_pressed
get_mouse_pressed = renderer.get_mouse_pressed
keysdown = renderer.keysdown
keysup = renderer.keysup
mousemotions = renderer.mousemotions
mousebuttonsdown = renderer.mousebuttonsdown
mousebuttonsup = renderer.mousebuttonsup


def _to_color(arg):
    if isinstance(arg, tuple) and len(arg) in (3, 4):
        return arg
    elif isinstance(arg, list) and len(arg) in (3, 4):
        return tuple(arg)
    elif isinstance(arg, str):
        if arg.startswith('#'):
            if len(arg) == 4:
                rgbs = tuple(arg[i] + arg[i] for i in range(1, 4, 1))
            elif len(arg) == 7:
                rgbs = tuple(arg[i:i + 2] for i in range(1, 7, 2))
            else:
                raise TypeError('В качестве цвета укажите строку вида "#aabbcc"')
            try:
                return tuple(int(c, 16) for c in rgbs)
            except ValueError:
                raise TypeError('В коде цвета используйте только цифры 0-9 и буквы a-f')
        elif arg in ALL_COLORS:
            return ALL_COLORS[arg]
        raise TypeError('В качестве цвета укажите строку вида "#aabbcc" или название цвета ("red", "green" и т.п.)')
    raise TypeError('В качестве цвета тройку чисел вида (0, 128, 255): количество красного, зелёного и синего (0 до 255)')


def _to_pos(pos):
    """Round a tuple position, so it can be used for drawing."""
    if len(pos) != 2 or not isinstance(pos[0], NUM_LIKE) or not isinstance(pos[1], NUM_LIKE):
        raise TypeError('Координаты указывайте в виде (x, y), например, (100, 200)')
    return int(renderer.surface_size / VIRTUAL_SIZE * pos[0] + 0.5), int(renderer.surface_size / VIRTUAL_SIZE * pos[1] + 0.5)


def _to_scaled_int(num):
    try:
        return int(renderer.surface_size / VIRTUAL_SIZE * num + 0.5)
    except:
        raise TypeError('Здесь нужно целое число, например, 24. `{}` не подходит.'.format(num))


def _to_flat(lst):
    flattened = []
    for el in lst:
        if isinstance(el, PT_LIKE):
            flattened.extend(_to_flat(el))
        else:
            flattened.append(el)
    return flattened


def _to_rect(rect):
    # rect — one of
    # x, y, w, h
    # (x, y), (w, h)
    # (x, y, w, h),
    if not rect:
        raise TypeError('Укажите координаты прямоугольника в формате (x, y, w, h), '
                        'где x, y — координаты угла, и w, h — ширина и высота прямоугольника')
    rect = _to_flat(rect)
    if not all(isinstance(el, NUM_LIKE) for el in rect):
        raise TypeError('Координаты прямоугольника должны быть целыми или действительными (вида 100 или 100.25)')
    if len(rect) != 4:
        raise TypeError('Укажите координаты прямоугольника в формате (x, y, w, h), '
                        'где x, y — координаты угла, и w, h — ширина и высота прямоугольника')
    x, y, w, h = rect
    return int(renderer.surface_size / VIRTUAL_SIZE * x + 0.5), int(renderer.surface_size / VIRTUAL_SIZE * y + 0.5), \
        int(renderer.surface_size / VIRTUAL_SIZE * w + 0.5), int(renderer.surface_size / VIRTUAL_SIZE * h + 0.5)


def _to_points_list(points):
    if not points:
        raise TypeError('Укажите координаты вершин многоугольника в формате ((x1,y1), (x2, y2), ...)')
    tot_cords = _to_flat(points)
    if not all(isinstance(el, NUM_LIKE) for el in tot_cords):
        raise TypeError('Координаты многоугольника должны быть целыми или действительными (вида 100 или 100.25)')
    cords_it = iter(map(lambda x: int(renderer.surface_size / VIRTUAL_SIZE * x + 0.5), tot_cords))
    return list(zip(cords_it, cords_it))


def grid():
    """Draw a grid with coordinates"""
    for i in range(100, 901, 100):
        line('white', 0, i, 1000, i, alpha=64, line_width=1)
        line('white', i, 0, i, 1000, alpha=64, line_width=1)
        text('white', str(i), (0, i), 24, '<.')
        text('white', str(i), (i, 0), 24, '.^')
    text('white', '(0,0)', (0, 0), 24, align='<^')
    text('white', '(1000,0)', (1000, 0), 24, align='>^')
    text('white', '(0,1000)', (0, 1000), 24, align='<v')
    text('white', '(1000,1000)', (1000, 1000), 24, align='>v')


def line(color='red', start=(100, 100), end=(200, 200), *args, alpha: int = 255, line_width: int = None):
    """Draw a line from start to end."""
    coords = _to_flat([start, end, args])
    color = _to_color(color)
    start = _to_pos(coords[:2])
    end = _to_pos(coords[2:4])
    renderer.draw_line(color, start, end, alpha, line_width)


def circle(color='red', pos=(100, 100), radius=10, *args, alpha: int = 255, line_width: int = None):
    """Draw a circle."""
    coords = _to_flat([pos, radius, args])
    color = _to_color(color)
    pos = _to_pos(coords[:2])
    radius = _to_scaled_int(*coords[2:3])
    renderer.draw_circle(color, pos, radius, alpha, line_width)


def filled_circle(color='red', pos=(100, 100), radius=10, *args, alpha: int = 255):
    """Draw a filled circle."""
    circle(color, pos, radius, *args, alpha=alpha, line_width=0)


def rect(color='red', pos=(100, 100), width=500, height=200, *args, alpha: int = 255, line_width: int = None):
    """Draw a rectangle."""
    coords = _to_flat([pos, width, height, args])
    color = _to_color(color)
    rect = _to_rect(coords[:4])
    renderer.draw_rect(color, rect, alpha, line_width)


def filled_rect(color='red', pos=(100, 100), width=500, height=200, *args, alpha: int = 255):
    """Draw a filled rectangle."""
    rect(color, pos, width, height, *args, alpha=alpha, line_width=0)


def ellipse(color='red', pos=(100, 100), width=500, height=200, *args, alpha: int = 255, line_width: int = None):
    """Draw an ellipse."""
    coords = _to_flat([pos, width, height, args])
    color = _to_color(color)
    rect = _to_rect(coords[:4])
    renderer.draw_ellipse(color, rect, alpha, line_width)


def filled_ellipse(color='red', pos=(100, 100), width=500, height=200, *args, alpha: int = 255):
    """Draw a filled ellipse."""
    ellipse(color, pos, width, height, *args, alpha=alpha, line_width=0)


def arc(color='red', pos=(100, 100), width=500, height=200, start_angle=45, stop_angle=270, *args, alpha: int = 255, line_width: int = None):
    """Draw an arc."""
    coords = _to_flat([pos, width, height, args])
    color = _to_color(color)
    rect = _to_rect(coords[:4])
    renderer.draw_arc(color, rect, start_angle / 180 * pi, stop_angle / 180 * pi, alpha, line_width)


def rect_rotated(color='red', pos=(100, 100), width=500, height=200, angle=0, *args, alpha: int = 255, line_width: int = None):
    """Draw a rotated rectangle."""
    coords = _to_flat([pos, width, height, args])
    color = _to_color(color)
    x, y, w, h = coords[:4]
    mid_x = x + w / 2
    mid_y = y + h / 2
    angle_rad = angle / 180 * pi
    points = [
        _to_pos([mid_x + w / 2 * d1 * cos(angle_rad) + h / 2 * d2 * sin(angle_rad), mid_y - w / 2 * d1 * sin(angle_rad) + h / 2 * d2 * cos(angle_rad)])
        for d1, d2 in [(+1, +1), (-1, +1), (-1, -1), (+1, -1)]
    ]
    renderer.draw_polygon(color, points, alpha, line_width)


def filled_rect_rotated(color='red', pos=(100, 100), width=500, height=200, angle=0, *args, alpha: int = 255):
    """Draw a filled rotated rectangle."""
    rect_rotated(color, pos, width, height, alpha, *args, alpha=alpha, line_width=0)


def polygon(color='red', *points, alpha: int = 255, line_width: int = None):
    """Draw a polygon."""
    color = _to_color(color)
    points = _to_points_list(points)
    renderer.draw_polygon(color, points, alpha, line_width)


def filled_polygon(color='red', *points, alpha: int = 255):
    """Draw a filled polygon."""
    polygon(color, *points, alpha=alpha, line_width=0)


VALID_ALIGN = {x + y for x in '<.>' for y in '^.v'}


def text(color='red', text='Hello!', pos=(100, 100), fontsize=24, align='..'):
    """Draw text to the screen."""
    color = _to_color(color)
    pos = _to_pos(pos)
    fontsize = _to_scaled_int(fontsize)
    if align not in VALID_ALIGN:
        raise ValueError(f"align parm must be one of '<^', '.^', '>^', '<.', '..', '>.', '<v', '.v', '>v',\n"
                         f"(<=left, .=center, >=right), (^=top, .=middle, v=bottom)")
    renderer.draw_text(color, text, pos, fontsize, align)


def clear():
    """Reset the screen to black."""
    renderer.draw_clear()


def fill(color='red', alpha: int = 255):
    """Fill the screen with a solid color."""
    color = _to_color(color)
    renderer.draw_fill(color, alpha)


def image(image, pos, width: int = None, alpha: int = 255):
    """Draw the image to the screen at the given position."""
    pos = _to_pos(pos)
    renderer.draw_image(image, pos, width, alpha)


def mouse_pos() -> tuple:
    """Get current mouse coordinates on canvas"""
    x, y = renderer.mouse_pos()
    x = VIRTUAL_SIZE / renderer.surface_size * x
    y = VIRTUAL_SIZE / renderer.surface_size * y
    return x, y


def set_mouse_pos(x=500, y=500, *args):
    x, y = _to_flat([x, y, *args])[:2]
    renderer.set_mouse_pos((int(renderer.surface_size / VIRTUAL_SIZE * x + 0.5), int(renderer.surface_size / VIRTUAL_SIZE * y + 0.5)))


def _update_events_coordinates():
    for i, ev in enumerate(mousebuttonsdown):
        x, y = ev.pos
        x = VIRTUAL_SIZE / renderer.surface_size * x
        y = VIRTUAL_SIZE / renderer.surface_size * y
        ev.pos = (x, y)
    for i, ev in enumerate(mousebuttonsup):
        x, y = ev.pos
        x = VIRTUAL_SIZE / renderer.surface_size * x
        y = VIRTUAL_SIZE / renderer.surface_size * y
        ev.pos = (x, y)
    for i, ev in enumerate(mousemotions):
        x, y = ev.pos
        x = VIRTUAL_SIZE / renderer.surface_size * x
        y = VIRTUAL_SIZE / renderer.surface_size * y
        ev.pos = (x, y)
        x, y = ev.rel
        x = VIRTUAL_SIZE / renderer.surface_size * x
        y = VIRTUAL_SIZE / renderer.surface_size * y
        ev.rel = (x, y)


def tick(r=1):
    renderer.draw_tick(r)
    _update_events_coordinates()


def sleep(t=1):
    renderer.draw_sleep(t)
    _update_events_coordinates()


def quit():
    renderer.draw_quit()


################################################################################
# Pygamezero compatibility

class Obj:
    pass


screen = Obj()
screen.clear = clear
screen.fill = fill
screen.blit = image
screen.draw = Obj()
screen.draw.line = line
screen.draw.circle = circle
screen.draw.filled_circle = filled_circle
screen.draw.rect = rect
screen.draw.filled_rect = filled_rect
screen.draw.polygon = polygon
screen.draw.filled_polygon = filled_polygon
screen.draw.text = text
################################################################################
