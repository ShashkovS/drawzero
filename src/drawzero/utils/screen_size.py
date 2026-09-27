VIRTUAL_WIDTH = 1000
VIRTUAL_HEIGHT = 1000

REAL_WIDTH = -1
REAL_HEIGHT = -1


def set_real_size(width, height):
    global REAL_WIDTH, REAL_HEIGHT
    REAL_WIDTH = width
    REAL_HEIGHT = height


def set_virtual_size(width, height):
    global VIRTUAL_WIDTH, VIRTUAL_HEIGHT
    VIRTUAL_WIDTH = width
    VIRTUAL_HEIGHT = height


def get_virtual_size():
    return VIRTUAL_WIDTH, VIRTUAL_HEIGHT


def get_real_size():
    return REAL_WIDTH, REAL_HEIGHT


def to_canvas_x(x):
    return int(REAL_WIDTH / VIRTUAL_WIDTH * x + 0.5)


def to_canvas_y(y):
    return int(REAL_HEIGHT / VIRTUAL_HEIGHT * y + 0.5)


def from_canvas_x(x):
    return VIRTUAL_WIDTH / REAL_WIDTH * x


def from_canvas_y(y):
    return VIRTUAL_HEIGHT / REAL_HEIGHT * y


_input_geometry = None
_input_factors = (1.0, 1.0)


def _input_scale():
    """Cached, safe input transform; does not change legacy conversions."""
    global _input_geometry, _input_factors
    geometry = (REAL_WIDTH, REAL_HEIGHT, VIRTUAL_WIDTH, VIRTUAL_HEIGHT)
    if geometry != _input_geometry:
        _input_geometry = geometry
        _input_factors = (VIRTUAL_WIDTH / REAL_WIDTH if REAL_WIDTH > 0 else 1.0,
                          VIRTUAL_HEIGHT / REAL_HEIGHT if REAL_HEIGHT > 0 else 1.0)
    return _input_factors
