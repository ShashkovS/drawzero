#!/usr/bin/env python3
"""Bounded production-example replay. Also captures actual SDL surfaces."""
import argparse
import os
from pathlib import Path
import random
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]


def replay(path, frames=12, capture=None, text_mode=False):
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    os.environ['SDL_AUDIODRIVER'] = 'dummy'
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    if text_mode:
        os.environ['EJUDGE_MODE'] = '1'
    else:
        os.environ.pop('EJUDGE_MODE', None)
    import drawzero as d
    from drawzero.utils.draw import renderer as r
    random.seed(5701)
    d.set_virtual_size(1000, 1000)
    if not text_mode:
        import pygame
        from drawzero.utils.screen_size import set_real_size
        r.surface_size = 640
        r._create_surface()
        set_real_size(640, 640)
        r._animation_not_detected = False
        pygame.event.clear()
    original_tick = r.draw_tick
    count = 0

    class Finished(BaseException):
        pass

    def bounded_tick(repetitions=1, **kwargs):
        nonlocal count
        count += 1
        if count >= frames:
            if capture and not text_mode:
                Path(capture).parent.mkdir(parents=True, exist_ok=True)
                pygame.image.save(r._surface, str(capture))
            raise Finished()
        if not text_mode:
            # Native queue replay, not a claim about hardware-held state.
            batch = []
            if count == 1:
                batch += [pygame.event.Event(pygame.KEYDOWN, key=d.K.RIGHT, scancode=79, mod=0, unicode=''),
                          pygame.event.Event(pygame.KEYDOWN, key=d.K.LSHIFT, scancode=225, mod=d.K.MOD_LSHIFT, unicode=''),
                          pygame.event.Event(pygame.KEYDOWN, key=d.K.SPACE, scancode=44, mod=d.K.MOD_LSHIFT, unicode=' '),
                          pygame.event.Event(pygame.TEXTINPUT, text='DrawZero')]
            if count == 2:
                batch += [pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(130, 300)),
                          pygame.event.Event(pygame.KEYUP, key=d.K.SPACE, scancode=44, mod=d.K.MOD_LSHIFT)]
            if 2 <= count <= 9:
                x = 130 + 40 * (count - 2)
                y = 300 + int(70 * __import__('math').sin((count - 2) * .6))
                prev_x = 130 + 40 * max(0, count - 3)
                prev_y = 300 + int(70 * __import__('math').sin(max(0, count - 3) * .6))
                batch.append(pygame.event.Event(pygame.MOUSEMOTION, pos=(x, y), rel=(x-prev_x, y-prev_y), buttons=(1, 0, 0)))
            if count == 5:
                batch += [pygame.event.Event(pygame.TEXTINPUT, text='!'),
                          pygame.event.Event(pygame.KEYDOWN, key=d.K.BACKSPACE, scancode=42, mod=d.K.MOD_LSHIFT, unicode=''),
                          pygame.event.Event(pygame.TEXTINPUT, text=': ready'),
                          pygame.event.Event(pygame.MOUSEWHEEL, x=2, y=3, precise_x=1.5, precise_y=2.5, flipped=False)]
            if count == 10:
                batch.append(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(410, 239)))
            for event in batch:
                if not pygame.event.post(event):
                    raise RuntimeError('SDL queue overflow')
            kwargs.update(fps=0, wait=False, display_update=False)
        original_tick(min(repetitions, 1), **kwargs)

    r.draw_tick = bounded_tick
    r.draw_sleep = lambda seconds=1: bounded_tick()
    try:
        runpy.run_path(str(path), run_name='__main__')
        if capture and not text_mode:
            pygame.image.save(r._surface, str(capture))
    except Finished:
        pass
    finally:
        r.draw_quit()
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('example', type=Path)
    parser.add_argument('--frames', type=int, default=12)
    parser.add_argument('--capture', type=Path)
    parser.add_argument('--text', action='store_true')
    args = parser.parse_args()
    replay(args.example, args.frames, args.capture, args.text)
