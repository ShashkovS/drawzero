#!/usr/bin/env python3
"""Same-interpreter input benchmark; --source selects an unpacked source checkout."""
import argparse
import atexit
import gc
import json
import os
from pathlib import Path
import platform
import statistics
import sys
import time
import tracemalloc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1] / 'src')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--repeats', type=int, default=7)
    parser.add_argument('--iterations', type=int, default=300)
    args = parser.parse_args()
    sys.path.insert(0, str(args.source.resolve()))
    os.environ.pop('EJUDGE_MODE', None)
    os.environ.update(SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy', PYGAME_HIDE_SUPPORT_PROMPT='1')
    import drawzero as d
    from drawzero.utils import renderer as r, draw
    from drawzero.utils.screen_size import set_real_size
    import pygame
    atexit.unregister(r._draw_go)
    r.surface_size = 640
    r._create_surface()
    set_real_size(640, 640)
    d.set_virtual_size(640, 640)
    r._animation_not_detected = False
    # The baseline has no waiting switch. A no-op clock is applied equally to both.
    class Clock:
        def tick(self, fps):
            pass
    r._fps = Clock()
    native_get = pygame.event.get
    new = hasattr(d, 'keyboard')
    star = {}; exec('from drawzero import *', star)
    motion = lambda: pygame.event.Event(pygame.MOUSEMOTION, pos=(20, 30), rel=(1, -1), buttons=(0, 0, 0))
    mixed = [pygame.event.Event(pygame.KEYDOWN, key=d.K.a, scancode=4, unicode='a', mod=0),
             pygame.event.Event(pygame.TEXTINPUT, text='яλ'),
             pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(10, 20)), motion(),
             pygame.event.Event(pygame.MOUSEWHEEL, x=1, y=-1, precise_x=.25, precise_y=-.5, flipped=False),
             pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(20, 30)),
             pygame.event.Event(pygame.KEYUP, key=d.K.a, scancode=4, unicode='', mod=0)]
    traces = {'idle': [], 'mixed': mixed}
    traces.update({'motion-' + str(n): [motion() for _ in range(n)] for n in (1, 10, 50, 1000)})
    result = {'environment': {'python': sys.version, 'pygame_ce': pygame.version.ver,
               'sdl': pygame.get_sdl_version(), 'os': platform.platform(), 'machine': platform.machine(),
               'driver': pygame.display.get_driver(), 'canvas': [640, 640], 'source': str(args.source.resolve()),
               'clock': 'perf_counter_ns', 'gc': 'disabled during timing; collected before samples',
               'warmup_calls': 20, 'repeats': args.repeats, 'iterations': args.iterations,
               'waiting': False, 'presentation': 'only frame layer', 'font': 'only separate font case'},
              'cases': {}}

    def measure(name, fn, iterations=None):
        n = iterations or args.iterations
        for _ in range(20): fn()
        samples = []
        for _ in range(args.repeats):
            gc.collect(); gc.disable()
            start = time.perf_counter_ns()
            for __ in range(n): fn()
            samples.append((time.perf_counter_ns() - start) / n / 1000)
            gc.enable()
        result['cases'][name] = {'median_us': statistics.median(samples), 'min_us': min(samples),
                                 'max_us': max(samples), 'samples_us': samples, 'iterations': n}

    def read(mode):
        if mode in ('legacy', 'mixed-api'):
            star['get_keys_pressed']()[d.K.a]
            star['get_mouse_pressed']()
            len(star['keysdown']); len(star['mousemotions'])
        if mode == 'all':
            d.events()
        elif mode == 'devices':
            d.keyboard.events; d.mouse.events
        elif mode == 'cached':
            for _ in range(10): d.events(); d.keyboard.events; d.mouse.events
        elif mode == 'mixed-api':
            d.keyboard.pressed(d.K.a); d.events()

    # Native event creation/conversion round-trip alone, without the reducer.
    for name, batch in traces.items():
        native_get()
        def queue_only():
            for event in batch:
                if not pygame.event.post(event): raise RuntimeError('queue overflow')
            if len(native_get()) != len(batch): raise RuntimeError('queue count mismatch')
        measure('queue-only/' + name, queue_only,
                max(20, args.iterations // 10) if len(batch) >= 1000 else None)

    consumed = [0]
    def counted_get():
        batch = native_get()
        consumed[0] += len(batch)
        return batch

    for layer in ('provider', 'native', 'frame'):
        for name, batch in traces.items():
            for mode in (('none', 'legacy', 'all', 'devices', 'cached', 'mixed-api') if new else ('none', 'legacy')):
                if layer == 'provider':
                    pygame.event.get = lambda: batch
                else:
                    pygame.event.get = counted_get
                native_get()
                def operation():
                    if layer != 'provider':
                        before = consumed[0]
                        for event in batch:
                            if not pygame.event.post(event): raise RuntimeError('queue overflow')
                    if layer == 'frame':
                        d.clear(); d.filled_circle('red', (320, 320), 20)
                    r.draw_tick(display_update=layer == 'frame')
                    draw._update_events_coordinates()
                    if layer != 'provider' and consumed[0] - before != len(batch):
                        raise RuntimeError('queue dropped or injected events')
                    read(mode)
                measure(layer + '/' + name + '/' + mode, operation,
                        max(20, args.iterations // 10) if len(batch) >= 1000 else None)
    pygame.event.get = lambda: []
    if new:
        for name, fn in {
            'constant': lambda: d.keyboard.pressed(d.K.a),
            'string': lambda: d.keyboard.pressed('a'),
            'any': lambda: d.keyboard.pressed('left', 'a'),
            'modifier': lambda: d.keyboard.pressed('shift'),
            'axis': lambda: d.keyboard.axis(('left', 'a'), ('right', 'd')),
        }.items(): measure('query/' + name, fn, 20000)
        # Pure reducer, with neither pygame translation nor legacy buckets.
        from drawzero.utils.input import _Input, E
        manager = _Input()
        payload = {'pos': (20, 30), 'rel': (1, -1), 'buttons': (0, 0, 0)}
        for count in (0, 1, 10, 50, 1000):
            def reduce():
                manager.begin()
                for _ in range(count): manager.feed(E.MOUSE_MOVE, payload)
                manager.publish()
            measure('reducer/motion-' + str(count), reduce, max(20, args.iterations // 10))
    measure('legacy-query/constant', lambda: star['get_keys_pressed']()[d.K.a], 10000)
    measure('legacy-query/string', lambda: star['get_keys_pressed']()['a'], 10000)
    measure('font/text', lambda: r.draw_text((255,255,255), 'DrawZero', (10,10), 24, '<^'))
    pygame.event.get = lambda: mixed
    def memory_run(n):
        for _ in range(n):
            r.draw_tick(display_update=False)
            if new: d.events()
    memory_run(100)
    gc.collect(); tracemalloc.start()
    memory_run(1000); gc.collect()
    first, peak1 = tracemalloc.get_traced_memory()
    memory_run(10000); gc.collect()
    last, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    result['memory'] = {'after_1000_bytes': first, 'after_11000_bytes': last, 'peak_bytes': peak2,
                        'retained_growth_bytes': last-first, 'note': 'retained/peak, NOT transient allocation counts'}
    r.draw_quit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
