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


def draw_resize(width: int, height: int):
    global _surface
    _surface = pygame.display.set_mode([width, height])
    pygame.display.update()


def draw_line(start: Pt, end: Pt, color: Clr):
    """Draw a line from start to end."""
    pygame.draw.line(_surface, color, start, end, _dft_wid)
    pygame.display.update()


def draw_circle(pos: Pt, radius: int, color: Clr):
    """Draw a circle."""
    pygame.draw.circle(_surface, color, pos, radius, _dft_wid)
    pygame.display.update()


def draw_filled_circle(pos: Pt, radius: int, color: Clr):
    """Draw a filled circle."""
    pygame.draw.circle(_surface, color, pos, radius, 0)
    pygame.display.update()


def draw_rect(rect: Rect, color: Clr):
    """Draw a rectangle."""
    pygame.draw.rect(_surface, color, pygame.rect.Rect(rect), _dft_wid)
    pygame.display.update()


def draw_filled_rect(rect: Rect, color: Clr):
    """Draw a filled rectangle."""
    pygame.draw.rect(_surface, color, rect, 0)
    pygame.display.update()


def draw_polygon(color: Clr, points: List[Pt]):
    """Draw a polygon."""
    pygame.draw.polygon(_surface, color, points, _dft_wid)
    pygame.display.update()


def draw_filled_polygon(color: Clr, points: List[Pt]):
    """Draw a filled polygon."""
    pygame.draw.polygon(_surface, color, points, 0)
    pygame.display.update()


def draw_text(text: str, pos: Pt, fontsize: int, color: Clr):
    """Draw text."""
    use_font = _fonts.get(fontsize, pygame.font.Font(None, fontsize))
    temp_surf = use_font.render(text, True, color)
    _surface.blit(temp_surf, pos)
    pygame.display.update()


def draw_fill(color: Clr):
    """Fill the screen with a solid color."""
    _surface.fill(color)  # Заливаем всё чёрным
    pygame.display.update()


def draw_clear(color: Clr = (0, 0, 0)):
    """Fill the screen with a solid color."""
    _surface.fill(color)  # Заливаем всё чёрным
    pygame.display.update()


def draw_blit(image: str, pos: Pt):
    """Draw the image to the screen at the given position."""
    EXTNS = ['png', 'gif', 'jpg', 'jpeg', 'bmp']
    TYPE = 'image'
    path = image
    _surface.blit(pygame.image.load(path).convert_alpha(), pos)
    pygame.display.update()


def _resize(nw: int, nh: int):
    global _surface, surface_size
    surface_size = min(nw, nh)
    scaled = pygame.transform.smoothscale(_surface, (surface_size, surface_size))
    _surface = pygame.display.set_mode((surface_size, surface_size), pygame.locals.RESIZABLE)
    _surface.blit(scaled, (0, 0))
    pygame.display.update()


def draw_tick():
    _fps.tick(60)
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
    ticks = int(t * 60 + 0.5)
    for __ in range(ticks):
        draw_tick()


def draw_set_line_width(w):
    global _dft_wid
    _dft_wid = w


def _draw_go():
    while True:
        draw_tick()


def _init_surface():
    if os.name == 'nt':
        # need to get screen size with scale factor for HDPI
        ctypes.windll.user32.SetProcessDPIAware()
    pygame.init()
    info = pygame.display.Info()
    w, h = info.current_w, info.current_h
    surface_size = 4 * min(w, h) // 5
    # set window position
    os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format((w - surface_size) // 2, (h - surface_size) // 2)
    _surface = pygame.display.set_mode((surface_size, surface_size), pygame.locals.RESIZABLE)
    _surface.fill((0, 0, 0))
    pygame.display.set_caption('Draw Zero')
    return surface_size, _surface


surface_size, _surface = _init_surface()

atexit.register(_draw_go)
