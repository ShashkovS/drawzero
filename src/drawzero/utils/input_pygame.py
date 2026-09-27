"""Thin pygame adapter. Queue ownership remains with renderer.draw_tick."""
from .input import E, _input, _CODES
from . import screen_size
import pygame

_TYPES = {}
for name, kind in (
    ('KEYDOWN', E.KEY_DOWN), ('KEYUP', E.KEY_UP),
    ('TEXTINPUT', E.TEXT_INPUT), ('TEXTEDITING', E.TEXT_EDITING),
    ('MOUSEBUTTONDOWN', E.MOUSE_DOWN), ('MOUSEBUTTONUP', E.MOUSE_UP),
    ('MOUSEMOTION', E.MOUSE_MOVE), ('MOUSEWHEEL', E.MOUSE_WHEEL),
    ('WINDOWFOCUSLOST', E.FOCUS_LOST), ('WINDOWFOCUSGAINED', E.FOCUS_GAINED),
    ('VIDEORESIZE', E.WINDOW_RESIZED), ('WINDOWRESIZED', E.WINDOW_RESIZED)):
    value = getattr(pygame, name, None)
    if value is not None:
        _TYPES[value] = kind


def ingest(event):
    kind = _TYPES.get(event.type)
    if event.type == pygame.ACTIVEEVENT and event.state & 2:
        kind = E.FOCUS_GAINED if event.gain else E.FOCUS_LOST
    if kind is None:
        return
    if kind == E.WINDOW_RESIZED:
        size = getattr(event, 'size', None)
        if size is None:
            size = (event.x, event.y)
        _input.feed(kind, {'size': size})
    else:
        _input.feed(kind, event.dict, screen_size._input_scale())


def reconcile_focus():
    if _input.needs_reconcile:
        raw = pygame.key.get_pressed()
        keys = []
        for code in _CODES:
            if raw[code]:
                keys.append(code)
        buttons = [i + 1 for i, held in enumerate(pygame.mouse.get_pressed(3)) if held]
        x, y = pygame.mouse.get_pos()
        sx, sy = screen_size._input_scale()
        _input.reconcile(keys, buttons, (x * sx, y * sy), pygame.key.get_mods())
