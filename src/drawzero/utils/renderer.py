import atexit
import sys
import ctypes
import os
from typing import Tuple, List, Union

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.locals

from drawzero.utils.key_flags import key_flags

# Types
Pt = Tuple[int, int]
Clr = Union[Tuple[int, int, int], Tuple[int, int, int, int]]  # RGB or RGBA
Rect = Tuple[int, int, int, int]

_fps = pygame.time.Clock()
_fonts = {}
_dft_wid = 4
_animation_not_detected = True

if __name__ == '__main__':
    print("You shouldn't need run this module directly")
    sys.exit(0)


def _create_surface():
    """
    We create surface only on first drawing call
    So without any drawing command new windows is not created nor opened
    """
    global _surface
    if not _surface:
        _surface = pygame.display.set_mode((surface_size, surface_size), pygame.locals.RESIZABLE)
        _surface.fill((0, 0, 0))
        pygame.display.set_caption('Draw Zero')


def draw_resize(width: int, height: int):
    global _surface
    _surface = pygame.display.set_mode([width, height])


def draw_line(color: Clr, start: Pt, end: Pt, alpha: int = 255, line_width: int = None):
    """Draw a line from start to end."""
    _create_surface()
    wid = line_width if line_width is not None else _dft_wid
    if alpha == 255 and len(color) == 3:
        pygame.draw.line(_surface, color, start, end, wid)
    else:
        # create a surface with alpha channel
        # We need some extra space for line width
        points = [start, end]
        minx, maxx, miny, maxy = _get_bounding_box(points)
        transparent = pygame.Surface((maxx - minx + 2 * wid, maxy - miny + 2 * wid), pygame.SRCALPHA, 32)
        transparent.fill((0, 0, 0, 0))
        if len(color) == 3:
            color = [*color, alpha]
        points = [(x - minx + wid, y - miny + wid) for x, y in points]
        pygame.draw.line(transparent, color, points[0], points[1], wid)
        _surface.blit(transparent, (minx - wid, miny - wid))
    _display_update_if_no_animation()


def draw_circle(color: Clr, pos: Pt, radius: int, alpha: int = 255, line_width: int = None):
    """
    Draw a circle.
    Set line_width to zero to make it filled
    """
    _create_surface()
    wid = line_width if line_width is not None else _dft_wid
    if alpha == 255 and len(color) == 3:
        pygame.draw.circle(_surface, color, pos, radius, wid)
    else:
        # create a surface with alpha channel
        transparent = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        transparent.fill((0, 0, 0, 0))
        if len(color) == 3:
            color = [*color, alpha]
        pygame.draw.circle(transparent, color, (radius, radius), radius, wid)
        _surface.blit(transparent, (pos[0] - radius, pos[1] - radius))
    _display_update_if_no_animation()


def draw_ellipse(color: Clr, rect: Rect, alpha: int = 255, line_width: int = None):
    """
    Draw an ellipse.
    Set line_width to zero to make it filled
    """
    _create_surface()
    wid = line_width if line_width is not None else _dft_wid
    if alpha == 255 and len(color) == 3:
        pygame.draw.ellipse(_surface, color, pygame.rect.Rect(rect), wid)
    else:
        # create a surface with alpha channel
        # We need some extra space for line width
        transparent = pygame.Surface((rect[2] + 2 * wid, rect[3] + 2 * wid), pygame.SRCALPHA, 32)
        transparent.fill((0, 0, 0, 0))
        if len(color) == 3:
            color = [*color, alpha]
        pygame.draw.ellipse(transparent, color, pygame.rect.Rect((wid, wid, rect[2], rect[3])), wid)
        _surface.blit(transparent, (rect[0] - wid, rect[1] - wid))
    _display_update_if_no_animation()


def draw_arc(color: Clr, rect: Rect, start_angle: float, stop_angle: float, alpha: int = 255, line_width: int = None):
    """
    Draw an arc.
    """
    _create_surface()
    wid = line_width if line_width is not None else _dft_wid
    if alpha == 255 and len(color) == 3:
        pygame.draw.arc(_surface, color, pygame.rect.Rect(rect), start_angle, stop_angle, wid)
    else:
        # create a surface with alpha channel
        # We need some extra space for line width
        transparent = pygame.Surface((rect[2] + 2 * wid, rect[3] + 2 * wid), pygame.SRCALPHA, 32)
        transparent.fill((0, 0, 0, 0))
        if len(color) == 3:
            color = [*color, alpha]
        pygame.draw.arc(transparent, color, pygame.rect.Rect((wid, wid, rect[2], rect[3])), start_angle, stop_angle, wid)
        _surface.blit(transparent, (rect[0] - wid, rect[1] - wid))
    _display_update_if_no_animation()


def draw_rect(color: Clr, rect: Rect, alpha: int = 255, line_width: int = None):
    """
    Draw a rectangle.
    Set line_width to zero to make it filled
    """
    _create_surface()
    wid = line_width if line_width is not None else _dft_wid
    if alpha == 255 and len(color) == 3:
        pygame.draw.rect(_surface, color, pygame.rect.Rect(rect), wid)
    else:
        # create a surface with alpha channel
        # We need some extra space for line width
        transparent = pygame.Surface((rect[2] + 2 * wid, rect[3] + 2 * wid), pygame.SRCALPHA, 32)
        transparent.fill((0, 0, 0, 0))
        if len(color) == 3:
            color = [*color, alpha]
        pygame.draw.rect(transparent, color, pygame.rect.Rect((wid, wid, rect[2], rect[3])), wid)
        _surface.blit(transparent, (rect[0] - wid, rect[1] - wid))
    _display_update_if_no_animation()


def _get_bounding_box(points: List[Pt]) -> tuple:
    minx = miny = float('inf')
    maxx = maxy = float('-inf')
    for x, y in points:
        if x < minx:
            minx = x
        if x > maxx:
            maxx = x
        if y < miny:
            miny = y
        if y > maxy:
            maxy = y
    return minx, maxx, miny, maxy


def draw_polygon(color: Clr, points: List[Pt], alpha: int = 255, line_width: int = None):
    """Draw a polygon."""
    _create_surface()
    wid = line_width if line_width is not None else _dft_wid
    if alpha == 255 and len(color) == 3:
        pygame.draw.polygon(_surface, color, points, wid)
    else:
        # create a surface with alpha channel
        # We need some extra space for line width
        minx, maxx, miny, maxy = _get_bounding_box(points)
        transparent = pygame.Surface((maxx - minx + 2 * wid, maxy - miny + 2 * wid), pygame.SRCALPHA, 32)
        transparent.fill((0, 0, 0, 0))
        if len(color) == 3:
            color = [*color, alpha]
        points = [(x - minx + wid, y - miny + wid) for x, y in points]
        pygame.draw.polygon(transparent, color, points, wid)
        _surface.blit(transparent, (minx - wid, miny - wid))
    _display_update_if_no_animation()


def draw_text(color: Clr, text: str, pos: Pt, fontsize: int, align: str):
    """Draw text."""
    _create_surface()
    use_font = _fonts.get(fontsize, pygame.font.Font(None, fontsize))
    temp_surf = use_font.render(text, True, color)
    t_width, t_height = temp_surf.get_size()
    x, y = pos
    if align[0] == '.':
        x -= t_width // 2
    elif align[0] == '>':
        x -= t_width
    if align[1] == '.':
        y -= t_height // 2
    elif align[1] == 'v':
        y -= t_height
    _surface.blit(temp_surf, [x, y])
    _display_update_if_no_animation()


def draw_fill(color: Clr, alpha: int = 255):
    """Fill the screen with a solid color."""
    _create_surface()
    if alpha == 255 and len(color) == 3:
        _surface.fill(color)  # Заливаем всё нужным цветом
    else:
        transparent = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA, 32)
        if len(color) == 3:
            color = [*color, alpha]
        transparent.fill(color)
        _surface.blit(transparent, (0, 0))
    _display_update_if_no_animation()


def draw_clear(color: Clr = (0, 0, 0)):
    """Fill the screen with a solid color."""
    _create_surface()
    _surface.fill(color)  # Заливаем всё чёрным
    _display_update_if_no_animation()


def draw_image(path: str, pos: Pt, width: int = None, alpha: int = 255):
    """Draw the image to the screen at the given position."""
    _create_surface()
    image = pygame.image.load(path).convert_alpha()
    # Scale image if needed
    if width:
        w, h = image.get_size()
        height = int(h * width / w + 0.5)
        image = pygame.transform.smoothscale(image, (width, height))
    if alpha != 255:
        temp = pygame.Surface((image.get_width(), image.get_height())).convert()  # Create a temporary image OPAQUE the size of the image
        temp.blit(_surface, (-pos[0], -pos[1]))  # Blit the OPAQUE BACKGROUND onto this temporary image.
        temp.blit(image, (0, 0))  # Blit the per-pixel transparency image onto the temporary image.
        # The temporary image is completely opaque and has the transparent image on it above the background.
        temp.set_alpha(alpha)
        image = temp
    _surface.blit(image, pos)
    _display_update_if_no_animation()


def _resize(nw: int, nh: int):
    global _surface, surface_size
    surface_size = min(nw, nh)
    scaled = pygame.transform.smoothscale(_surface, (surface_size, surface_size))
    _surface = pygame.display.set_mode((surface_size, surface_size), pygame.locals.RESIZABLE)
    _surface.blit(scaled, (0, 0))


def _display_update():
    try:
        pygame.display.update()
    except pygame.error:
        pygame.quit()
        sys.exit()


def _display_update_if_no_animation():
    if _animation_not_detected:
        try:
            pygame.display.update()
        except pygame.error:
            pygame.quit()
            sys.exit()


def draw_tick(r=1, *, display_update=True):
    global keysdown, keysup, mousemotions, mousebuttonsdown, mousebuttonsup, _animation_not_detected
    _create_surface()
    _animation_not_detected = False
    keysdown.clear()
    keysup.clear()
    mousemotions.clear()
    mousebuttonsdown.clear()
    mousebuttonsup.clear()
    if display_update:
        _display_update()
    for __ in range(r):
        # We need this hack to process close button clicks
        _fps.tick(30)
        try:
            events = pygame.event.get()
        except pygame.error:
            pygame.quit()
            sys.exit()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                _resize(event.w, event.h)
            elif event.type == pygame.KEYDOWN:
                keysdown.append(event)
            elif event.type == pygame.KEYUP:
                keysup.append(event)
            elif event.type == pygame.MOUSEMOTION:
                mousemotions.append(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousebuttonsdown.append(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                mousebuttonsup.append(event)


def draw_sleep(t: Union[int, float]):
    _create_surface()
    ticks = int(t * 30 + 0.5)
    draw_tick(ticks)


def draw_set_line_width(w):
    global _dft_wid
    _dft_wid = w


def _draw_go():
    _display_update()
    while True:
        # We need this hack to process close button clicks
        draw_tick(display_update=False)


def draw_quit():
    try:
        pygame.quit()
    except:
        pass


def mouse_pos():
    return pygame.mouse.get_pos()


def set_mouse_pos(pos: Pt):
    pygame.mouse.set_pos(pos)


def get_mouse_pressed():
    return pygame.mouse.get_pressed(3)


def get_keys_pressed():
    return pygame.key.get_pressed()


def keys_mods_pressed():
    return pygame.key.get_mods()


def _init():
    global surface_size
    if os.name == 'nt':
        # need to get screen size with scale factor for HDPI
        ctypes.windll.user32.SetProcessDPIAware()
    pygame.init()
    info = pygame.display.Info()
    w, h = info.current_w, info.current_h
    surface_size = 4 * min(w, h) // 5
    # set window position
    os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format((w - surface_size) // 2, (h - surface_size) // 2)


_surface = None
surface_size = 0
keysdown = []
keysup = []
mousemotions = []
mousebuttonsdown = []
mousebuttonsup = []

_init()
atexit.register(_draw_go)
