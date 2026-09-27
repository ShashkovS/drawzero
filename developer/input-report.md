# Unified input: engineering and verification report

## Delivered changes

The public API is documented completely in [English](../docs/keyboard_and_mouse_input.en.md)
and [Russian](../docs/keyboard_and_mouse_input.ru.md). The existing page URL and navigation
entry are retained. Animation, architecture, index, README, and example-gallery material
now teach the new API. Generated HTML and search indexes were checked for hidden legacy
names. No dependency minimum or lockfile change was required.

`utils/input.py` provides the backend-independent frame reducer, typed immutable events,
strict queries, grouped modifiers, text, motion, wheel, focus, scancode bookkeeping, and
lazy caches. `input_pygame.py` is the queue adapter. Renderer/draw integration preserves
public frame ordering and multi-poll accumulation. Examples 16–20 use the new interface;
21 and 22 add precise drawing and ordered text/scroll. Input remains an imperative loop.

See [the compatibility inventory](input-compatibility.md) for exact import paths,
list/event/helper contracts, snapshot ownership, focus policy, and backend references.
Original examples are preserved as regression fixtures, byte-for-byte identical to the
starting checkout. The staged unrelated `docs/.DS_Store` remains untouched.

## Verification commands and results

Commands below run from the repository root. `.venv` is the modern test environment.
Tests use fake clocks or bounded replay rather than wall-clock sleeps. GUI and EJUDGE
runs are isolated in subprocesses; no interactive example is imported unbounded into
the test runner. The requested example program is also a bounded fixture.

```sh
.venv/bin/python -m pytest -q
.venv/bin/python -m coverage erase
.venv/bin/python -m coverage run -m pytest -q
.venv/bin/python -m coverage combine
.venv/bin/python -m coverage report --include='*/utils/input.py,*/utils/input_pygame.py,*/utils/key_flags.py,*/utils/renderer.py,*/utils/renderer_ejudge.py' -m
PYTHONPATH=src /private/tmp/drawzero-py38/bin/python -m pytest -q
PYTHONPATH=src /private/tmp/drawzero-py39/bin/python -m pytest -q
.venv/bin/python -m mkdocs build --strict
.venv/bin/python tools/check_docs.py
git diff --check
```

- **116 tests passed** on all three interpreter/backend combinations below. The modern
  coverage run took 10.72 s; the final 3.8 and 3.9 runs took 5.26 s and 8.10 s. These are
  test-run durations, not benchmark measurements. A final targeted 22-test core run
  additionally exercised cached text access; its coverage was combined with `--append`.
- Both documentation languages built with `--strict`; 25 generated HTML pages, local
  links/anchors, image paths, and search indexes passed `tools/check_docs.py`.
- Six inline tutorial programs (both languages), included example programs, all five
  original input examples, and the exact requested composite program ran bounded.
- SDL dummy integration covers posted native pygame events and actual surfaces. Optional
  authoritative state reconciliation is tested separately using coherent fake snapshots;
  posted key events are not presented as evidence of physically held keys.
- Seeded independent reducers compare mixed device/focus histories and separately compare
  motion/transform histories. Lifetime, immutability, list operations, source mutation,
  multi-poll timing, exception shutdown, and static-window exit all have regressions.
- `git diff --check` passed. No manual operating-system input/layout/IME check is claimed.

| Python | pygame-ce | SDL | Environment | Result |
| --- | --- | --- | --- | --- |
| 3.8.20 | 2.1.3 | 2.0.22 | macOS arm64, dummy | 116 passed |
| 3.9.24 | 2.1.3 | 2.0.22 | macOS arm64, dummy | 116 passed |
| 3.14.7 | 2.5.6 | 2.32.10 | macOS arm64, dummy | 116 passed |

The exact declared minimum `pygame-ce==2.0.1` was attempted with uv and failed resolution:
that CE version is not published. The installable 2.1.3 combination was tested instead.
The metadata still declares Python >=3.8 and pygame-ce >=2.0.1, as requested. Python 3.8
was downloaded into a temporary directory, not substituted by a syntax-only claim.
The newer backend documentation includes optional fields absent from these versions;
missing scancodes/precision/wheel positions have explicit fallbacks. The test tooling
used pytest 9.1.1 / coverage 7.16.1 on 3.14, pytest 8.3.5 on 3.8 and 8.4.2 on 3.9.
Subprocess coverage uses the modern environment's coverage `patch = subprocess` support.

### Coverage

No broad source exclusions or omitted branch pragmas were used. Coverage is measured
on the modern interpreter; the older combinations execute the same tests without coverage.

| Module | Lines | Branches |
| --- | --- | --- |
| `input.py` | 336/336 (100.00%) | 116/116 (100.00%) |
| `input_pygame.py` | 31/31 (100.00%) | 17/18 (94.44%) |
| `key_flags.py` | 214/214 (100.00%) | 0/0 |
| `renderer.py` | 293/300 (97.67%) | 92/100 (92.00%) |
| `renderer_ejudge.py` | 58/60 (96.67%) | 1/2 (50.00%) |

Uncovered branches include optional missing pygame constants (both installed versions
supply them), Windows DPI setup, module-as-script diagnostics, low-level resize/warp
helpers, existing alpha-drawing variants, and invalid native resize guards. EJUDGE's
unrelated encoder fallback and line-width output helper are not covered by this run.
These are reported rather than excluded. New reducer lines and branches are fully covered;
the adapter has 100% line coverage and one optional-constant branch unexercised.

## Reproducible rendered example captures

```sh
.venv/bin/python tools/replay_input.py src/drawzero/examples/16_keyboard_and_mouse.py --capture docs/imgs/input-controls.png
.venv/bin/python tools/replay_input.py src/drawzero/examples/21_precise_drawing.py --capture docs/imgs/input-drawing.png
.venv/bin/python tools/replay_input.py src/drawzero/examples/22_text_and_scroll.py --capture docs/imgs/input-text-scroll.png
```

Each uses a 640×640 SDL dummy surface, 1000×1000 virtual coordinates, seed 5701, and a
fixed 12-boundary trace. The tool posts real pygame events and runs actual example code,
production normalization, and drawing. It saves the surface before orderly shutdown.
The PNGs total about 32 KiB and were visually inspected: readable labels, a visible path,
correct one-shot/axis state, and the ordered edited string with fractional scroll.
The on-canvas text is language-neutral English; captions/alt text are localized in both
guides. These are rendered outputs, not evidence of hardware input or IME behavior.
A second independent capture run produced byte-identical files:

| File | SHA-256 |
| --- | --- |
| `docs/imgs/input-controls.png` | `fe34cc8c2ebe8832f54af563697fa511a49701701cf7baf6e06e41e586d3b4c7` |
| `docs/imgs/input-drawing.png` | `4981bb73bd7aab340a18a4b7777c8fd9965fe5fbed8e99d5cc7059c746e3051c` |
| `docs/imgs/input-text-scroll.png` | `c611e1bf344df738512cd85872b311dcd467d188deede50cd8583e2d77b36b1a` |

## Performance methodology

Final baseline and current runs were sequential, without concurrent tests. Both used
CPython 3.14.7, pygame-ce 2.5.6, SDL 2.32.10, macOS 26.3.1 arm64, SDL dummy, and a 640×640
surface/virtual canvas. Timings use `perf_counter_ns`, 20 warmup calls per case, seven
samples of 300 iterations (30 for 1,000-motion batches). GC is collected before each
sample and disabled during its timed section. Queries use 20,000 iterations; legacy
queries use 10,000. A no-op clock disables waiting identically in baseline and current.

The reference source is commit `da552b226a834acbff3afe6574929de65ade2340`, unpacked separately;
no benchmark-only change is made to its source. Normalized reads are unavailable in the
reference and are marked accordingly, not compared to fictitious equivalent functions.
All modes use the normal star-import surface. The legacy mode queries live legacy key
and mouse helpers and lists; mixed-api additionally reads the new snapshot/stream.

- **provider** feeds preconstructed pygame events into the renderer, including coordinate
  conversion and legacy lists but no native queue, rendering, sleeping, or presentation.
- **reducer** isolates the new core state machine without pygame conversion or legacy lists.
- **queue-only** measures native post/get conversion round trips with no input reducer.
- **native** adds actual queue post/get to ingestion and verifies exact event counts each
  iteration. A false post result or dropped/injected event aborts instead of timing loss.
- **frame** adds a clear, a filled circle, and display presentation to native input. SDL
  dummy presentation is not a measurement of a physical display's latency.
- **font** is separate: warmed repeated rendering of `DrawZero`, size 24, without presentation.

Reproduction (the archive download requires network access):

```sh
curl -L --fail https://codeload.github.com/ShashkovS/drawzero/tar.gz/da552b226a834acbff3afe6574929de65ade2340 -o /private/tmp/drawzero-reference.tar.gz
tar -xzf /private/tmp/drawzero-reference.tar.gz -C /private/tmp
.venv/bin/python tools/benchmark_input.py --source /private/tmp/drawzero-da552b226a834acbff3afe6574929de65ade2340/src --output developer/benchmark-reference.json
.venv/bin/python tools/benchmark_input.py --output developer/benchmark-current.json
```

Both JSON files contain every sample, environment metadata, and all workloads/read modes.
Values below are microseconds per operation; brackets show the current run's minimum and
maximum sample averages, not per-event latency percentiles.

| Workload | Reference median µs | Current median µs [range] |
| --- | ---: | ---: |
| `provider/idle/none` | 0.391 | 0.941 [0.916, 0.974] |
| `provider/mixed/none` | 1.634 | 9.240 [8.982, 9.478] |
| `provider/motion-1/none` | 0.730 | 2.553 [2.513, 2.572] |
| `provider/motion-10/none` | 3.580 | 14.951 [14.482, 15.006] |
| `provider/motion-50/none` | 15.578 | 69.987 [69.620, 70.343] |
| `provider/motion-1000/none` | 307.208 | 1379.265 [1370.444, 1382.308] |
| `provider/mixed/legacy` | 3.268 | 11.075 [10.987, 11.137] |
| `provider/mixed/all` | unavailable | 12.057 [11.201, 12.105] |
| `provider/mixed/devices` | unavailable | 13.246 [12.637, 13.349] |
| `provider/mixed/cached` | unavailable | 14.588 [13.786, 14.643] |
| `provider/mixed/mixed-api` | unavailable | 14.067 [13.854, 14.161] |
| `queue-only/mixed` | 1.097 | 1.110 [1.094, 1.148] |
| `native/mixed/none` | 2.960 | 10.731 [10.687, 10.751] |
| `native/motion-1000/none` | 390.565 | 1486.450 [1483.029, 1501.156] |
| `frame/mixed/none` | 122.517 | 138.581 [136.088, 139.209] |
| `font/text` | 139.502 | 2.832 [2.788, 2.905] |

| New query | Median µs [range] |
| --- | ---: |
| `constant` | 0.136 [0.134, 0.139] |
| `string` | 0.157 [0.153, 0.158] |
| `any` | 0.257 [0.254, 0.260] |
| `modifier` | 0.157 [0.156, 0.157] |
| `axis` | 0.551 [0.550, 0.554] |

The richer default model has a measured cost: idle adds 0.551 µs and the seven-event
mixed provider case is 5.65× the reference. The 1,000-motion case remains linear in
trace size but costs substantially more because every event's historical data is retained.
Full stream reads add immutable wrapper construction; device filters add cached tuple
materialization. `cached` performs ten common/keyboard/mouse reads per frame and pays
materialization only on the first reads. These are regressions in input ingestion, not
claimed speedups. Input-free legacy-only programs still pay the new snapshot bookkeeping.

The separate font cache improves its repeated-text case from 139.502
to 2.832 µs by avoiding repeated font construction. That result
must not be attributed to input processing or extrapolated to arbitrary rendering.

### Allocations and retention

The structural test instruments all eight public event constructors plus `Provenance`.
Fifty frames of an eleven-event mixed trace, with polling-only reads, construct **zero**
public normalized objects. First common-stream access creates eleven events and eleven
provenance values; fifty subsequent accesses add zero. Device-filter identity/cache tests
separately ensure shared instances and no repeated filtering. No timing threshold is used
as a CI assertion.

The memory experiment warms 100 mixed frames, then uses tracemalloc with explicit GC after
1,000 and 11,000 frames (current run reads full events). Baseline retained bytes:
160 → 192; current:
3184 → 3248. Peaks were
590 and 7872 bytes respectively. The tiny
64-byte measured current growth does not indicate retained event
history. These are retained/peak measurements, **not counts of transient allocations**.
Private sets, record tuples, and coordinate pairs still allocate during ingestion.

Motion coalescing is deferred: preserving every delivered path point is the default,
and this implementation does not add an unmeasured optional mode or block mouse motion.
No Rust rewrite, renderer replacement, action-binding system, or hardware-specific claim
is included. Remaining platform work is real-device focus/layout/repeat/IME behavior on
macOS, Windows, and Linux; simulated and SDL dummy checks do not replace it.
