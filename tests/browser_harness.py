"""Run a program on the browser backend with a fake page; print what the page saw.

    python tests/browser_harness.py PROGRAM [--frames N] [--events JSON]

The fake page answers every frame at once, hands out the scripted events one
frame at a time (``--events`` is a list of per-frame lists), and stops the
program after N frames. Prints one JSON object: the frames and how it ended.
"""
import json
import os
import runpy
import sys

os.environ.pop('EJUDGE_MODE', None)
os.environ['DRAWZERO_BACKEND'] = 'browser'

from drawzero.utils import renderer_browser  # noqa: E402


def main():
    args = sys.argv[1:]
    program = args[0]
    frames_limit = int(args[args.index('--frames') + 1]) if '--frames' in args else 10
    script = json.loads(args[args.index('--events') + 1]) if '--events' in args else []
    frames = []

    def frame(ops, wait):
        frames.append({'ops': json.loads(ops), 'wait': wait})
        if len(frames) > frames_limit:
            return None
        n = len(frames) - 1
        return json.dumps(script[n] if n < len(script) else [])

    renderer_browser.connect(frame)
    status = 'completed'
    error = None
    try:
        runpy.run_path(program, run_name='__main__')
        renderer_browser.flush()
    except KeyboardInterrupt:
        status = 'stopped'
    except SystemExit:
        renderer_browser.flush()
    except Exception as e:  # noqa: BLE001 - reported to the test
        status = 'error'
        error = f'{type(e).__name__}: {e}'
    sys.stdout = sys.__stdout__
    print(json.dumps({'status': status, 'error': error, 'frames': frames}))


if __name__ == '__main__':
    main()
