from numbers import Real
from typing import Union, Optional, Tuple, List

from drawzero.utils.colors import ALL_COLORS
from drawzero.utils.screen_size import to_canvas_x, to_canvas_y
from drawzero.utils.errors import BadDrawParmsError
from drawzero.utils.i18n import I18N
from drawzero.utils.pt import Pt

_PT_LIKE = (tuple, list, Pt)
_NUM_LIKE = (int, float)
_DFT_LINE_WIDTH = 4


def _to_color(arg: Union[str, tuple, list], error: BadDrawParmsError) -> Optional[Tuple]:
    """Convert arg to color tuple

    Valid colors:
    - 'red', 'green', etc: ref ALL_COLORS
    - '#xxyyzz', where xx, yy and zz — are valid hex numbers between 0 and 255
    - '#xyz', where x, y and z — are valid hex digit
    - tuple of 3 (RGB) or 4 (RGBA) integers each between 0 and 255. Ex: (0, 0, 0), (255, 0, 0), (255, 0, 128, 100)
    """
    if isinstance(arg, str):
        if arg.startswith('#'):
            if len(arg) == 4:
                rgbs = tuple(arg[i] + arg[i] for i in range(1, 4, 1))
            elif len(arg) == 7:
                rgbs = tuple(arg[i:i + 2] for i in range(1, 7, 2))
            else:
                error.errors.append(I18N.bad_color.format(arg))
                error.errors.append(I18N.use_color_hex)
                return None
            try:
                return tuple(int(c, 16) for c in rgbs)
            except ValueError:
                error.errors.append(I18N.bad_color.format(arg))
                error.errors.append(I18N.use_color_hexdigits)
                return None
        elif arg in ALL_COLORS:
            return ALL_COLORS[arg]
        error.errors.append(I18N.bad_color.format(arg))
        error.errors.append(I18N.use_color_consts)
        return None

    if isinstance(arg, list):
        arg = tuple(arg)
    if isinstance(arg, tuple) and len(arg) != 3 and len(arg) != 4:
        error.errors.append(I18N.bad_color.format(arg))
        error.errors.append(I18N.use_color_tuple)
        return None
    elif isinstance(arg, tuple) and all(type(x) == int and 0 <= x <= 255 for x in arg):
        return arg
    elif isinstance(arg, tuple):
        error.errors.append(I18N.bad_color.format(arg))
        error.errors.append(I18N.use_color_ints)
        return None

    error.errors.append(I18N.bad_color.format(arg))
    error.errors.append(I18N.use_color_correct)
    return None


def _to_pos(pos, error: BadDrawParmsError):
    """Round a tuple position, so it can be used for drawing."""
    if not isinstance(pos, _PT_LIKE) or len(pos) != 2:
        error.errors.append(I18N.bad_coords.format(pos))
        error.errors.append(I18N.use_coords_pair)
        error.errors.append(I18N.use_coords_iterable)
        return None
    if not isinstance(pos[0], _NUM_LIKE) or not isinstance(pos[1], _NUM_LIKE):
        error.errors.append(I18N.bad_coords.format(pos))
        error.errors.append(I18N.use_coords_pair)
        error.errors.append(I18N.use_coords_ints)
        return None
    return to_canvas_x(pos[0]), to_canvas_y(pos[1])


def _to_scaled_int(num: Real, error: BadDrawParmsError) -> Optional[int]:
    try:
        return to_canvas_x(num)
    except:
        error.errors.append(I18N.bad_num.format(num))
        return None


def _to_line_width(num: Union[Real, None], error: BadDrawParmsError) -> Optional[int]:
    if num is None:
        return _DFT_LINE_WIDTH
    try:
        return to_canvas_x(num)
    except:
        error.errors.append(I18N.bad_width.format(num))
        error.errors.append(I18N.use_width_int)
        return None


def _to_alpha(num: Real, error: BadDrawParmsError) -> Optional[int]:
    if num is None:
        return 255
    try:
        use_num = int(num)
        assert 0 <= use_num <= 255
        return use_num
    except:
        error.errors.append(I18N.bad_alpha.format(num))
        error.errors.append(I18N.use_alpha_int)
        return None


def _to_flat(lst) -> list:
    flattened = []
    if not hasattr(lst, '__iter__') or isinstance(lst, (str, bytes)):
        return flattened
    for el in lst:
        if hasattr(el, '__iter__') and not isinstance(el, (str, bytes)):
            flattened.extend(_to_flat(el))
        else:
            flattened.append(el)
    return flattened


def _to_rect(rect: List, error: BadDrawParmsError) -> Optional[Tuple[int, int, int, int]]:
    """ Rect coordinates are four numbers: coordinates of top left corner, width and height.
    - (x, y), w, h
    - x, y, w, h
    - (x, y, w, h),
    """
    rect = _to_flat(rect)
    if not all(isinstance(el, _NUM_LIKE) for el in rect):
        error.errors.append(I18N.bad_rect.format(rect))
        error.errors.append(I18N.use_rect_ints)
        return None
    if len(rect) != 4:
        error.errors.append(I18N.bad_rect.format(rect))
        error.errors.append(I18N.use_rect_correct)
        return None
    x, y, w, h = rect
    cx = to_canvas_x(x)
    cy = to_canvas_y(y)
    cxw = to_canvas_x(x+w)
    cyh = to_canvas_y(y+h)
    cw = cxw - cx
    ch = cyh - cy
    return cx, cy, cw, ch


def _to_points_list(points: Union[list, tuple], error: BadDrawParmsError) -> Optional[List[Tuple[int, int]]]:
    if not points:
        error.errors.append(I18N.use_polygon_list)
        return None
    tot_cords = _to_flat(points)
    if not all(isinstance(el, _NUM_LIKE) for el in tot_cords):
        error.errors.append(I18N.bad_polygon.format(points))
        error.errors.append(I18N.use_polygon_ints)
        return None
    if len(tot_cords) % 2 != 0:
        error.errors.append(I18N.bad_polygon.format(points))
        error.errors.append(I18N.use_polygon_even)
        return None
    return [
        (to_canvas_x(tot_cords[i]), to_canvas_y(tot_cords[i + 1]))
        for i in range(0, len(tot_cords), 2)
    ]
