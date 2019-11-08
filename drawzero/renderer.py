import atexit
import sys
from typing import Tuple, List

import pygame

Pt = Tuple[int, int]
Clr = Tuple[int, int, int]
Rect = Tuple[int, int, int, int]

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


def draw_blit(image, pos):
    """Draw the image to the screen at the given position."""
    EXTNS = ['png', 'gif', 'jpg', 'jpeg', 'bmp']
    TYPE = 'image'
    path = image
    _surface.blit(pygame.image.load(path).convert_alpha(), pos)
    pygame.display.update()


def draw_tick():
    _fps.tick(60)
    try:
        events = pygame.event.get()
    except pygame.error:
        pygame.quit()
        sys.exit()
    if any(event.type == pygame.QUIT for event in events):
        pygame.quit()
        sys.exit()


def draw_set_line_width(w):
    global _dft_wid
    _dft_wid = w


def _draw_go():
    while True:
        draw_tick()


def _init_surface():
    SCREEN_SIZE = (500, 500)
    pygame.init()
    _pygame_surface = pygame.display.set_mode(SCREEN_SIZE)
    _pygame_surface.fill((0, 0, 0))
    pygame.display.set_caption('Draw Zero')
    return _pygame_surface


_surface = _init_surface()
_fps = pygame.time.Clock()
_fonts = {}
_dft_wid = 2
atexit.register(_draw_go)
