import json
from pathlib import Path
from .input import _input, _validate_fps

from drawzero.utils.screen_size import set_real_size

set_real_size(1000, 1000)

class PathEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Path):
            return str(obj)
        return super().default(obj)

def draw_line(color, start, end, alpha, line_width):
    print(json.dumps({"figure": "line", "color": color, "start": start, "end": end, "alpha": alpha, "line_width": line_width}, cls=PathEncoder))

def draw_circle(color, pos, radius, alpha, line_width):
    print(json.dumps({"figure": "circle", "color": color, "pos": pos, "radius": radius, "alpha": alpha, "line_width": line_width}, cls=PathEncoder))

def draw_rect(color, rect, alpha, line_width):
    print(json.dumps({"figure": "rect", "color": color, "rect": rect, "alpha": alpha, "line_width": line_width}, cls=PathEncoder))

def draw_ellipse(color, rect, alpha, line_width):
    print(json.dumps({"figure": "ellipse", "color": color, "rect": rect, "alpha": alpha, "line_width": line_width}, cls=PathEncoder))

def draw_arc(color, rect, start_angle, stop_angle, alpha, line_width):
    print(json.dumps({"figure": "arc", "color": color, "rect": rect, "start_angle": start_angle, "stop_angle": stop_angle, "alpha": alpha, "line_width": line_width}, cls=PathEncoder))

def draw_polygon(color, points, alpha, line_width):
    print(json.dumps({"figure": "polygon", "color": color, "points": points, "alpha": alpha, "line_width": line_width}, cls=PathEncoder))

def draw_text(color, text, pos, fontsize, align):
    print(json.dumps({"figure": "text", "color": color, "text": text, "pos": pos, "fontsize": fontsize, "align": align}, cls=PathEncoder))

def draw_fill(color, alpha):
    print(json.dumps({"figure": "fill", "color": color, "alpha": alpha}, cls=PathEncoder))

def draw_clear():
    print(json.dumps({"figure": "clear"}))

def draw_image(path, pos, width, alpha):
    print(json.dumps({"figure": "image", "path": path, "pos": pos, "width": width, "alpha": alpha}, cls=PathEncoder))

def draw_tick(r=1, *, fps=30):
    _validate_fps(fps)
    _input.begin()
    _input.publish()
    print(json.dumps({"cmd": "tick", "r": r}))

def draw_sleep(t=1):
    _input.begin()
    _input.publish()
    print(json.dumps({"cmd": "sleep", "t": t}))

def draw_set_line_width(w):
    print(json.dumps({"cmd": "set_line_width", "w": w}))

def draw_quit():
    print(json.dumps({"cmd": "quit"}))

surface_size = 1000
key_flags = None

class _NeutralKeys:
    def __getitem__(self, key):
        return False

    def __contains__(self, key):
        return False


_neutral_keys = _NeutralKeys()
get_keys_pressed = lambda: _neutral_keys
keys_mods_pressed = lambda: 0
get_mouse_pressed = lambda: (False, False, False)
mouse_pos = lambda: (0, 0)
keysdown = []
keysup = []
mousemotions = []
mousebuttonsdown = []
mousebuttonsup = []