from colordict import THECOLORS
from renderer import *

_ = lambda x: x  # That is for gettext localisation


def _make_color(arg):
    if isinstance(arg, tuple) and len(arg) == 3:
        return arg
    elif isinstance(arg, list) and len(arg) == 3:
        return tuple(arg)
    elif isinstance(arg, str):
        if arg.startswith('#'):
            if len(arg) == 4:
                rgbs = tuple(arg[i] + arg[i] for i in range(1, 4, 1))
            elif len(arg) == 7:
                rgbs = tuple(arg[i:i + 2] for i in range(1, 7, 2))
            else:
                raise TypeError(_('В качестве цвета укажите строку вида "#aabbcc"'))
            try:
                return tuple(int(c, 16) for c in rgbs)
            except ValueError:
                raise TypeError(_('В коде цвета используйте только цифры 0-9 и буквы a-f'))
        elif arg in THECOLORS:
            return THECOLORS[arg]
        raise TypeError(_('В качестве цвета укажите строку вида "#aabbcc" или название цвета ("red", "green" и т.п.)'))
    raise TypeError(_('В качестве цвета тройку чисел вида (0, 128, 255): количество красного, зелёного и синего (0 до 255)'))


def _make_pos(pos):
    """Round a tuple position so it can be used for drawing."""
    if len(pos) != 2 or not isinstance(pos[0], (int, float)) or not isinstance(pos[1], (int, float)):
        raise TypeError(_('Координаты указывайте в виде (x, y), например, (100, 200)'))
    return int(pos[0] + 0.5), int(pos[1] + 0.5)


def _make_int(num):
    try:
        return int(num)
    except:
        raise TypeError(_('Здесь нужно целое число, например, 24. `{}` не подходит.'.format(num)))


def _make_flat(lst):
    flattened = []
    for el in lst:
        if isinstance(el, (tuple, list)):
            flattened.extend(_make_flat(el))
        else:
            flattened.append(el)
    return flattened


def _make_rect(rect):
    # rect — one of
    # x, y, w, h
    # (x, y), (w, h)
    # (x, y, w, h),
    if not rect:
        raise TypeError(_('Укажите координаты прямоугольника в формате (x, y, w, h), '
                          'где x, y — координаты угла, и w, h — ширина и высота прямоугольника'))
    rect = _make_flat(rect)
    if not all(isinstance(el, (int, float)) for el in rect):
        raise TypeError(_('Координаты прямоугольника должны быть целыми или действительными (вида 100 или 100.25)'))
    if len(rect) != 4:
        raise TypeError(_('Укажите координаты прямоугольника в формате (x, y, w, h), '
                          'где x, y — координаты угла, и w, h — ширина и высота прямоугольника'))
    x, y, w, h = rect
    return int(x + 0.5), int(y + 0.5), int(w + 0.5), int(h + 0.5)


def _make_points_list(points):
    if not points:
        raise TypeError(_('Укажите координаты вершин многоугольника в формате ((x1,y1), (x2, y2), ...)'))
    tot_cords = _make_flat(points)
    if not all(isinstance(el, (int, float)) for el in tot_cords):
        raise TypeError(_('Координаты многоугольника должны быть целыми или действительными (вида 100 или 100.25)'))
    cords_it = iter(tot_cords)
    return list(zip(cords_it, cords_it))


def line(start=(100, 100), end=(200, 200), color='white', *args):
    """Draw a line from start to end."""
    draw_line(_make_pos(start), _make_pos(end), _make_color(color), )


def circle(pos=(100, 100), radius=10, color='white', *args):
    """Draw a circle."""
    draw_circle(_make_pos(pos), _make_int(radius), _make_color(color))


def filled_circle(pos=(100, 100), radius=10, color='white', *args):
    """Draw a filled circle."""
    draw_filled_circle(_make_pos(pos), _make_int(radius), _make_color(color))


def rect(color='white', *rect):
    """Draw a rectangle."""
    draw_rect(_make_rect(rect), _make_color(color))


def filled_rect(color='white', *rect):
    """Draw a filled rectangle."""
    draw_filled_rect(_make_rect(rect), _make_color(color))


def polygon(color='white', *points):
    """Draw a polygon."""
    draw_polygon(_make_color(color), _make_points_list(points))


def filled_polygon(color='white', *points):
    """Draw a filled polygon."""
    draw_filled_polygon(_make_color(color), _make_points_list(points))


def text(text='', pos=(100, 100), fontsize=24, color='black', *args, **kwargs):
    """Draw text to the screen."""
    draw_text(text, _make_pos(pos), _make_int(fontsize), _make_color(color))


def clear():
    """Reset the screen to black."""
    draw_fill((0, 0, 0))


def fill(color='white'):
    """Fill the screen with a solid color."""
    draw_fill(_make_color(color))
    pass


def blit(image, pos):
    """Draw the image to the screen at the given position."""
    draw_blit(image, _make_pos(pos))


def window(width=500, height=500):
    """Resize window."""
    draw_resize(_make_int(width), _make_int(height))


################################################################################

class Obj:
    pass


screen = Obj()
screen.clear = clear
screen.fill = fill
screen.blit = blit
screen.draw = Obj()
screen.draw.line = line
screen.draw.circle = circle
screen.draw.filled_circle = filled_circle
screen.draw.rect = rect
screen.draw.filled_rect = filled_rect
screen.draw.polygon = polygon
screen.draw.filled_polygon = filled_polygon
screen.draw.text = text
tick = draw_tick
