import os
from math import sin, cos, pi
from time import time

from drawzero.utils.screen_size import from_canvas_x, from_canvas_y
from drawzero.utils.errors import BadDrawParmsError
from drawzero.utils.i18n import I18N
from drawzero.utils.converters import _to_color, _to_pos, _to_scaled_int, _to_line_width, _to_alpha, _to_flat, _to_rect, _to_points_list

# TODO Check if GUI is possible
if not bool(os.environ.get('EJUDGE_MODE', False)):
    from drawzero.utils import renderer
else:
    from drawzero.utils import renderer_ejudge as renderer


# TODO Refactor keyboard and mouse interface
get_keys_pressed = renderer.get_keys_pressed
keys_mods_pressed = renderer.keys_mods_pressed
get_mouse_pressed = renderer.get_mouse_pressed
keysdown = renderer.keysdown
keysup = renderer.keysup
mousemotions = renderer.mousemotions
mousebuttonsdown = renderer.mousebuttonsdown
mousebuttonsup = renderer.mousebuttonsup


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


def line(color='red', start=(100, 100), end=(200, 200), *args, alpha=255, line_width: int = None):
    """Draw a line from start to end."""
    error = BadDrawParmsError()
    use_color = _to_color(color, error)
    coords = _to_flat([start, end, args])
    use_start = _to_pos(coords[:2], error)
    use_end = _to_pos(coords[2:4], error)
    use_alpha = _to_alpha(alpha, error)
    use_line_width = _to_line_width(line_width, error)
    if error.errors:
        use_args = ', ' + ', '.join(map(repr, args)) if args else ''
        use_alpha = f', {alpha=}' if alpha != 255 else ''
        use_line_width = f', {line_width=}' if line_width is not None else ''
        error.call_string = f'line({color!r}, {start!r}, {end!r}{use_args}{use_alpha}{use_line_width})'
        error.example = f"line({color if use_color else 'red'!r}, {use_start if use_start else (100, 100)!r}, {use_end if use_end else (200, 200)!r}{use_alpha}{use_line_width})"
        error.finish()
        raise error
    renderer.draw_line(use_color, use_start, use_end, use_alpha, use_line_width)


def circle(color='red', pos=(100, 100), radius=10, *args, alpha=255, line_width: int = None):
    """Draw a circle."""
    error = BadDrawParmsError()
    use_color = _to_color(color, error)
    coords = _to_flat([pos, radius, args])
    use_pos = _to_pos(coords[:2], error)
    use_radius = _to_scaled_int(*coords[2:3], error)
    use_alpha = _to_alpha(alpha, error)
    use_line_width = _to_line_width(line_width, error)
    if error.errors:
        use_args = ', ' + ', '.join(map(repr, args)) if args else ''
        use_alpha = f', {alpha=}' if alpha != 255 else ''
        use_line_width = f', {line_width=}' if line_width is not None else ''
        error.call_string = f'circle({color!r}, {pos!r}, {radius!r}{use_args}{use_alpha}{use_line_width})'
        error.example = f"circle({color if use_color else 'red'!r}, {use_pos if use_pos else (100, 100)!r}, {use_radius if use_radius else 50!r}{use_alpha}{use_line_width})"
        raise error
    renderer.draw_circle(use_color, use_pos, use_radius, use_alpha, use_line_width)


def filled_circle(color='red', pos=(100, 100), radius=10, *args, alpha=255):
    """Draw a filled circle.
    Example:
    >>> filled_circle('red', (200, 300), 50)
    """
    try:
        circle(color, pos, radius, *args, alpha=alpha, line_width=0)
    except BadDrawParmsError as error:
        error.call_string = error.call_string.replace(', line_width=0', '').replace('circle', 'filled_circle')
        error.example = error.example.replace(', line_width=0', '').replace('circle', 'filled_circle')


def rect(color='red', pos=(100, 100), width=500, height=200, *args, alpha=255, line_width: int = None):
    """Draw a rectangle."""
    error = BadDrawParmsError()
    use_color = _to_color(color, error)
    coords = _to_flat([pos, width, height, args])
    use_rect = _to_rect(coords[:4], error)
    use_alpha = _to_alpha(alpha, error)
    use_line_width = _to_line_width(line_width, error)
    renderer.draw_rect(use_color, use_rect, use_alpha, use_line_width)


def filled_rect(color='red', pos=(100, 100), width=500, height=200, *args, alpha=255):
    """Draw a filled rectangle."""
    rect(color, pos, width, height, *args, alpha=alpha, line_width=0)


def ellipse(color='red', pos=(100, 100), width=500, height=200, *args, alpha=255, line_width: int = None):
    """Draw an ellipse."""
    error = BadDrawParmsError()
    use_color = _to_color(color, error)
    coords = _to_flat([pos, width, height, args])
    use_rect = _to_rect(coords[:4], error)
    use_alpha = _to_alpha(alpha, error)
    use_line_width = _to_line_width(line_width, error)
    renderer.draw_ellipse(use_color, use_rect, use_alpha, use_line_width)


def filled_ellipse(color='red', pos=(100, 100), width=500, height=200, *args, alpha=255):
    """Draw a filled ellipse."""
    ellipse(color, pos, width, height, *args, alpha=alpha, line_width=0)


def arc(color='red', pos=(100, 100), width=500, height=200, start_angle=45, stop_angle=270, alpha=255, line_width: int = None):
    """Draw an arc."""
    error = BadDrawParmsError()
    use_color = _to_color(color, error)
    coords = _to_flat([pos, width, height])
    use_rect = _to_rect(coords[:4], error)
    use_alpha = _to_alpha(alpha, error)
    use_line_width = _to_line_width(line_width, error)
    renderer.draw_arc(use_color, use_rect, start_angle / 180 * pi, stop_angle / 180 * pi, use_alpha, use_line_width)


def rect_rotated(color='red', pos=(100, 100), width=500, height=200, angle=0, *args, alpha=255, line_width: int = None):
    """Draw a rotated rectangle."""
    error = BadDrawParmsError()
    use_color = _to_color(color, error)
    coords = _to_flat([pos, width, height, args])
    x, y, w, h = coords[:4]
    mid_x = x + w / 2
    mid_y = y + h / 2
    angle_rad = angle / 180 * pi
    points = [
        _to_pos([mid_x + w / 2 * d1 * cos(angle_rad) - h / 2 * d2 * sin(angle_rad), mid_y + w / 2 * d1 * sin(angle_rad) + h / 2 * d2 * cos(angle_rad)], error)
        for d1, d2 in [(+1, +1), (-1, +1), (-1, -1), (+1, -1)]
    ]
    renderer.draw_polygon(use_color, points, alpha, line_width)


def filled_rect_rotated(color='red', pos=(100, 100), width=500, height=200, angle=0, *args, alpha=255):
    """Draw a filled rotated rectangle."""
    rect_rotated(color, pos, width, height, angle, *args, alpha=alpha, line_width=0)


def polygon(color='red', *points, alpha=255, line_width: int = None):
    """Draw a polygon."""
    error = BadDrawParmsError()
    use_color = _to_color(color, error)
    use_points = _to_points_list(points, error)
    use_alpha = _to_alpha(alpha, error)
    use_line_width = _to_line_width(line_width, error)
    renderer.draw_polygon(use_color, use_points, use_alpha, use_line_width)


def filled_polygon(color='red', *points, alpha=255):
    """Draw a filled polygon."""
    polygon(color, *points, alpha=alpha, line_width=0)


_VALID_ALIGN = {x + y for x in '<.>' for y in '^.v'}


def text(color='red', text='Hello!', pos=(100, 100), fontsize=24, align='..'):
    """Draw text to the screen."""
    error = BadDrawParmsError()
    use_color = _to_color(color, error)
    use_pos = _to_pos(pos, error)
    use_fontsize = _to_scaled_int(fontsize, error)
    if align not in _VALID_ALIGN:
        error.errors.append(I18N.bad_text_align.format(align))
        error.errors.append(I18N.use_text_align)
    renderer.draw_text(use_color, str(text), use_pos, use_fontsize, align)


def clear():
    """Reset the screen to black."""
    renderer.draw_clear()


def fill(color='red', alpha=255):
    """Fill the screen with a solid color."""
    error = BadDrawParmsError()
    use_color = _to_color(color, error)
    use_alpha = _to_alpha(alpha, error)
    renderer.draw_fill(use_color, use_alpha)


def image(image, pos, width: int = None, alpha=255):
    """Draw the image to the screen at the given position.

    :param image: name of the image file
    :param pos: a tuple, list or Pt of the left upper corner. For example (100, 200)
    :param width: width of an image to draw on canvas
    :param alpha: opacity of the image (if needed)
    """
    error = BadDrawParmsError()
    use_pos = _to_pos(pos, error)
    use_width = _to_scaled_int(width, error) if width is not None else None
    use_alpha = _to_alpha(alpha, error)
    renderer.draw_image(image, use_pos, use_width, use_alpha)


def mouse_pos() -> tuple:
    """Get current mouse coordinates on canvas"""
    x, y = renderer.mouse_pos()
    return from_canvas_x(x), from_canvas_y(y)


def _update_events_coordinates():
    """Update mouse events coordinates so that they correspond to canvas coordinates"""
    for i, ev in enumerate(mousebuttonsdown):
        x, y = ev.pos
        ev.pos = (from_canvas_x(x), from_canvas_y(y))
    for i, ev in enumerate(mousebuttonsup):
        x, y = ev.pos
        ev.pos = (from_canvas_x(x), from_canvas_y(y))
    for i, ev in enumerate(mousemotions):
        x, y = ev.pos
        ev.pos = (from_canvas_x(x), from_canvas_y(y))
        x, y = ev.rel
        ev.rel = (from_canvas_x(x), from_canvas_y(y))


def tick(r=1):
    """Sleep for 1/30 of a second.
    If tick functions is called in a loop, then sleep time is reduced so
    takes 1/30 second between calls. For example if calculations between tick() calls take 1/60s,
    then tick sleeps for 1/60s. So while calculations takes less then 1/30s tick()
    we get 30 frames per second."""
    renderer.draw_tick(r)
    _update_events_coordinates()


def sleep(t=1):
    """Sleep for t seconds

    :param t: Number of seconds to sleep
    """
    renderer.draw_sleep(t)
    _update_events_coordinates()


def quit():
    """Close canvas window"""
    renderer.draw_quit()


def fps(fontsize=24, *, prev=[time()]):
    cur = time()
    diff = cur - prev[0]
    prev[0] = cur
    rate = int(1 / diff + 0.5)
    text('white', f'{rate} FPS', (1000, 000), fontsize, '>^')


################################################################################
# Pygamezero compatibility

class _Obj:
    pass


screen = _Obj()
screen.clear = clear
screen.fill = fill
screen.blit = image
screen.draw = _Obj()
screen.draw.line = line
screen.draw.circle = circle
screen.draw.filled_circle = filled_circle
screen.draw.rect = rect
screen.draw.filled_rect = filled_rect
screen.draw.polygon = polygon
screen.draw.filled_polygon = filled_polygon
screen.draw.text = text
################################################################################
