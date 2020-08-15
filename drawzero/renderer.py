import atexit
import sys
import ctypes
import os
from typing import Tuple, List, Union

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.locals

Pt = Tuple[int, int]
Clr = Tuple[int, int, int]
Rect = Tuple[int, int, int, int]

_fps = pygame.time.Clock()
_fonts = {}
_dft_wid = 4

if __name__ == '__main__':
    print("You shouldn't need run this module directly")
    sys.exit(0)


def _create_surface():
    global _surface
    if not _surface:
        _surface = pygame.display.set_mode((surface_size, surface_size), pygame.locals.RESIZABLE)
        _surface.fill((0, 0, 0))
        pygame.display.set_caption('Draw Zero')


def draw_resize(width: int, height: int):
    global _surface
    _surface = pygame.display.set_mode([width, height])
    # pygame.display.update()


def draw_line(color: Clr, start: Pt, end: Pt):
    """Draw a line from start to end."""
    _create_surface()
    pygame.draw.line(_surface, color, start, end, _dft_wid)
    # pygame.display.update()


def draw_circle(color: Clr, pos: Pt, radius: int):
    """Draw a circle."""
    _create_surface()
    pygame.draw.circle(_surface, color, pos, radius, _dft_wid)
    # pygame.display.update()


def draw_filled_circle(color: Clr, pos: Pt, radius: int):
    """Draw a filled circle."""
    _create_surface()
    pygame.draw.circle(_surface, color, pos, radius, 0)
    # pygame.display.update()


def draw_rect(color: Clr, rect: Rect):
    """Draw a rectangle."""
    _create_surface()
    pygame.draw.rect(_surface, color, pygame.rect.Rect(rect), _dft_wid)
    # pygame.display.update()


def draw_filled_rect(color: Clr, rect: Rect):
    """Draw a filled rectangle."""
    _create_surface()
    pygame.draw.rect(_surface, color, rect, 0)
    # pygame.display.update()


def draw_polygon(color: Clr, points: List[Pt]):
    """Draw a polygon."""
    _create_surface()
    pygame.draw.polygon(_surface, color, points, _dft_wid)
    # pygame.display.update()


def draw_filled_polygon(color: Clr, points: List[Pt]):
    """Draw a filled polygon."""
    _create_surface()
    pygame.draw.polygon(_surface, color, points, 0)
    # pygame.display.update()


def draw_text(color: Clr, text: str, pos: Pt, fontsize: int):
    """Draw text."""
    _create_surface()
    use_font = _fonts.get(fontsize, pygame.font.Font(None, fontsize))
    temp_surf = use_font.render(text, True, color)
    _surface.blit(temp_surf, pos)
    # pygame.display.update()


def draw_fill(color: Clr):
    """Fill the screen with a solid color."""
    _create_surface()
    _surface.fill(color)  # Заливаем всё чёрным
    # pygame.display.update()


def draw_clear(color: Clr = (0, 0, 0)):
    """Fill the screen with a solid color."""
    _create_surface()
    _surface.fill(color)  # Заливаем всё чёрным
    # pygame.display.update()


def draw_blit(image: str, pos: Pt):
    """Draw the image to the screen at the given position."""
    _create_surface()
    EXTNS = ['png', 'gif', 'jpg', 'jpeg', 'bmp']
    TYPE = 'image'
    path = image
    _surface.blit(pygame.image.load(path).convert_alpha(), pos)
    # pygame.display.update()


def _resize(nw: int, nh: int):
    global _surface, surface_size
    surface_size = min(nw, nh)
    scaled = pygame.transform.smoothscale(_surface, (surface_size, surface_size))
    _surface = pygame.display.set_mode((surface_size, surface_size), pygame.locals.RESIZABLE)
    _surface.blit(scaled, (0, 0))
    # pygame.display.update()


def _display_update():
    try:
        pygame.display.update()
    except pygame.error:
        pygame.quit()
        sys.exit()


def draw_tick(r=1, *, display_update=True):
    _create_surface()
    if display_update:
        _display_update()
    for __ in range(r):
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


def draw_sleep(t: Union[int, float]):
    _create_surface()
    ticks = int(t * 30 + 0.5)
    draw_tick(ticks)


def draw_set_line_width(w):
    _create_surface()
    global _dft_wid
    _dft_wid = w


def _draw_go():
    _display_update()
    while True:
        draw_tick(display_update=False)


def _init():
    if os.name == 'nt':
        # need to get screen size with scale factor for HDPI
        ctypes.windll.user32.SetProcessDPIAware()
    pygame.init()
    info = pygame.display.Info()
    w, h = info.current_w, info.current_h
    surface_size = 4 * min(w, h) // 5
    # set window position
    os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format((w - surface_size) // 2, (h - surface_size) // 2)
    return surface_size


_surface = None
surface_size = _init()

atexit.register(_draw_go)
