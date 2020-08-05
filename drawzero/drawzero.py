import renderer
import time

c_antiquewhite = (250, 235, 215)
c_aliceblue = (240, 248, 255)
c_aquamarine = (127, 255, 212)
c_azure = (240, 255, 255)
c_beige = (245, 245, 220)
c_bisque = (255, 228, 196)
c_black = (0, 0, 0)
c_blanchedalmond = (255, 235, 205)
c_blue = (0, 0, 255)
c_blueviolet = (138, 43, 226)
c_brown = (165, 42, 42)
c_burlywood = (222, 184, 135)
c_cadetblue = (95, 158, 160)
c_chartreuse = (127, 255, 0)
c_chocolate = (210, 105, 30)
c_coral = (255, 127, 80)
c_cornflowerblue = (100, 149, 237)
c_cornsilk = (255, 248, 220)
c_cyan = (0, 255, 255)
c_darkblue = (0, 0, 139)
c_darkcyan = (0, 139, 139)
c_darkgoldenrod = (184, 134, 11)
c_darkgray = (169, 169, 169)
c_darkgreen = (0, 100, 0)
c_darkgrey = (169, 169, 169)
c_darkkhaki = (189, 183, 107)
c_darkmagenta = (139, 0, 139)
c_darkolivegreen = (85, 107, 47)
c_darkorange = (255, 140, 0)
c_darkorchid = (153, 50, 204)
c_darkred = (139, 0, 0)
c_darksalmon = (233, 150, 122)
c_darkseagreen = (143, 188, 143)
c_darkslateblue = (72, 61, 139)
c_darkslategray = (47, 79, 79)
c_darkslategrey = (47, 79, 79)
c_darkturquoise = (0, 206, 209)
c_darkviolet = (148, 0, 211)
c_deeppink = (255, 20, 147)
c_deepskyblue = (0, 191, 255)
c_dimgray = (105, 105, 105)
c_dimgrey = (105, 105, 105)
c_dodgerblue = (30, 144, 255)
c_firebrick = (178, 34, 34)
c_floralwhite = (255, 250, 240)
c_forestgreen = (34, 139, 34)
c_gainsboro = (220, 220, 220)
c_ghostwhite = (248, 248, 255)
c_gold = (255, 215, 0)
c_goldenrod = (218, 165, 32)
c_gray = (190, 190, 190)
c_green = (0, 255, 0)
c_greenyellow = (173, 255, 47)
c_grey = (190, 190, 190)
c_honeydew = (240, 255, 240)
c_hotpink = (255, 105, 180)
c_indianred = (205, 92, 92)
c_ivory = (255, 255, 240)
c_khaki = (240, 230, 140)
c_lavender = (230, 230, 250)
c_lavenderblush = (255, 240, 245)
c_lawngreen = (124, 252, 0)
c_lemonchiffon = (255, 250, 205)
c_lightblue = (173, 216, 230)
c_lightcoral = (240, 128, 128)
c_lightcyan = (224, 255, 255)
c_lightgoldenrod = (238, 221, 130)
c_lightgoldenrodyellow = (250, 250, 210)
c_lightgray = (211, 211, 211)
c_lightgreen = (144, 238, 144)
c_lightgrey = (211, 211, 211)
c_lightpink = (255, 182, 193)
c_lightsalmon = (255, 160, 122)
c_lightseagreen = (32, 178, 170)
c_lightskyblue = (135, 206, 250)
c_lightslateblue = (132, 112, 255)
c_lightslategray = (119, 136, 153)
c_lightslategrey = (119, 136, 153)
c_lightsteelblue = (176, 196, 222)
c_lightyellow = (255, 255, 224)
c_limegreen = (50, 205, 50)
c_linen = (250, 240, 230)
c_magenta = (255, 0, 255)
c_maroon = (176, 48, 96)
c_mediumaquamarine = (102, 205, 170)
c_mediumblue = (0, 0, 205)
c_mediumorchid = (186, 85, 211)
c_mediumpurple = (147, 112, 219)
c_mediumseagreen = (60, 179, 113)
c_mediumslateblue = (123, 104, 238)
c_mediumspringgreen = (0, 250, 154)
c_mediumturquoise = (72, 209, 204)
c_mediumvioletred = (199, 21, 133)
c_midnightblue = (25, 25, 112)
c_mintcream = (245, 255, 250)
c_mistyrose = (255, 228, 225)
c_moccasin = (255, 228, 181)
c_navajowhite = (255, 222, 173)
c_navy = (0, 0, 128)
c_navyblue = (0, 0, 128)
c_oldlace = (253, 245, 230)
c_olivedrab = (107, 142, 35)
c_orange = (255, 165, 0)
c_orangered = (255, 69, 0)
c_orchid = (218, 112, 214)
c_palegoldenrod = (238, 232, 170)
c_palegreen = (152, 251, 152)
c_paleturquoise = (175, 238, 238)
c_palevioletred = (219, 112, 147)
c_papayawhip = (255, 239, 213)
c_peachpuff = (255, 218, 185)
c_peru = (205, 133, 63)
c_pink = (255, 192, 203)
c_plum = (221, 160, 221)
c_powderblue = (176, 224, 230)
c_purple = (160, 32, 240)
c_red = (255, 0, 0)
c_rosybrown = (188, 143, 143)
c_royalblue = (65, 105, 225)
c_saddlebrown = (139, 69, 19)
c_salmon = (250, 128, 114)
c_sandybrown = (244, 164, 96)
c_seagreen = (46, 139, 87)
c_seashell = (255, 245, 238)
c_sienna = (160, 82, 45)
c_skyblue = (135, 206, 235)
c_slateblue = (106, 90, 205)
c_slategray = (112, 128, 144)
c_slategrey = (112, 128, 144)
c_snow = (255, 250, 250)
c_springgreen = (0, 255, 127)
c_steelblue = (70, 130, 180)
c_tan = (210, 180, 140)
c_thistle = (216, 191, 216)
c_tomato = (255, 99, 71)
c_turquoise = (64, 224, 208)
c_violet = (238, 130, 238)
c_violetred = (208, 32, 144)
c_wheat = (245, 222, 179)
c_white = (255, 255, 255)
c_whitesmoke = (245, 245, 245)
c_yellow = (255, 255, 0)
c_yellowgreen = (154, 205, 50)

THECOLORS = {obj[2:]: globals()[obj] for obj in locals() if obj.startswith('c_')}

_ = lambda x: x  # That is for gettext localisation
_SECRET_PRINT = ''


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
    return int(renderer.surface_size / 1000 * pos[0] + 0.5), int(renderer.surface_size / 1000 * pos[1] + 0.5)


def _make_int(num):
    try:
        return int(renderer.surface_size / 1000 * num + 0.5)
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
    return int(renderer.surface_size / 1000 * x + 0.5), int(renderer.surface_size / 1000 * y + 0.5), \
           int(renderer.surface_size / 1000 * w + 0.5), int(renderer.surface_size / 1000 * h + 0.5)


def _make_points_list(points):
    if not points:
        raise TypeError(_('Укажите координаты вершин многоугольника в формате ((x1,y1), (x2, y2), ...)'))
    tot_cords = _make_flat(points)
    if not all(isinstance(el, (int, float)) for el in tot_cords):
        raise TypeError(_('Координаты многоугольника должны быть целыми или действительными (вида 100 или 100.25)'))
    cords_it = iter(map(lambda x: renderer.surface_size / 1000 * x, tot_cords))
    return list(zip(cords_it, cords_it))


def line(color='red', start=(100, 100), end=(200, 200), *args):
    """Draw a line from start to end."""
    parms = _make_pos(start), _make_pos(end), _make_color(color)
    print(_SECRET_PRINT, 'line', parms)
    renderer.draw_line(*parms)


def circle(color='red', pos=(100, 100), radius=10, *args):
    """Draw a circle."""
    parms = _make_pos(pos), _make_int(radius), _make_color(color)
    print(_SECRET_PRINT, 'circle', parms)
    renderer.draw_circle(*parms)


def filled_circle(color='red', pos=(100, 100), radius=10, *args):
    """Draw a filled circle."""
    parms = _make_pos(pos), _make_int(radius), _make_color(color)
    print(_SECRET_PRINT, 'filled_circle', parms)
    renderer.draw_filled_circle(*parms)


def rect(color='red', *rect):
    """Draw a rectangle."""
    parms = _make_rect(rect), _make_color(color)
    print(_SECRET_PRINT, 'rect', parms)
    renderer.draw_rect(*parms)


def filled_rect(color='red', *rect):
    """Draw a filled rectangle."""
    parms = _make_rect(rect), _make_color(color)
    print(_SECRET_PRINT, 'filled_rect', parms)
    renderer.draw_filled_rect(*parms)


def polygon(color='red', *points):
    """Draw a polygon."""
    parms = _make_color(color), _make_points_list(points)
    print(_SECRET_PRINT, 'polygon', parms)
    renderer.draw_polygon(*parms)


def filled_polygon(color='red', *points):
    """Draw a filled polygon."""
    parms = _make_color(color), _make_points_list(points)
    print(_SECRET_PRINT, 'filled_polygon', parms)
    renderer.draw_filled_polygon(*parms)


def text(color='red', text='', pos=(100, 100), fontsize=24, *args, **kwargs):
    """Draw text to the screen."""
    parms = text, _make_pos(pos), _make_int(fontsize), _make_color(color)
    print(_SECRET_PRINT, 'text', parms)
    renderer.draw_text(*parms)


def clear():
    """Reset the screen to black."""
    print(_SECRET_PRINT, 'clear')
    renderer.draw_clear()


def fill(color='red'):
    """Fill the screen with a solid color."""
    parms = _make_color(color),  # Запятая нужна!
    print(_SECRET_PRINT, 'fill', parms)
    renderer.draw_fill(*parms)


def blit(image, pos):
    """Draw the image to the screen at the given position."""
    parms = image, _make_pos(pos)
    print(_SECRET_PRINT, 'blit', parms)
    renderer.draw_blit(*parms)


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
sleep = time.sleep

FPS = 1 / 60


def tick(*, _prev=[0]):
    """Выждать такое время, чтобы частота обновления кадров была 60 FPS"""
    cur = time.time()
    dif = _prev[0] + FPS - cur
    _prev[0] = cur
    if dif > 0:
        time.sleep(dif)
