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
