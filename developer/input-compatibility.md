# Input implementation and compatibility inventory

This contributor document is outside `docs/`, so it is not part of the student site
or its search index. Compatibility has no opt-in flag, warning, or removal schedule.

The working checkout was `b0109108a0851deb38cfb08eed1acfc74612523d`, preceding the specified
reference `da552b226a834acbff3afe6574929de65ade2340`. It was inspected in place; no reset was
performed. The reference archive was downloaded separately for measurement. The existing
staged `docs/.DS_Store` is unrelated and was preserved.

## Exact legacy surface

`drawzero.__all__` retains `get_keys_pressed`, `keys_mods_pressed`, `get_mouse_pressed`,
`mouse_pos`, `keysdown`, `keysup`, `mousemotions`, `mousebuttonsdown`, `mousebuttonsup`,
`K`, and `KEY`, alongside all previous drawing/utilities exports. Existing imports through
`drawzero.utils.draw`, `drawzero.utils.renderer`, and `drawzero.utils.key_flags` still work.
`K is KEY is key_flags` remains true. Statically declared key aliases and all `K.MOD_*`
numbers are unchanged. The authoritative constants table no longer attempts the broken
set-to-dict update from pygame; `str(K)` now returns text rather than printing and failing.

The five lists are permanently allocated **built-in lists**, cleared in place at each
renderer boundary. In GUI mode they contain the original mutable pygame events, with
native integer `.type`, `.dict`, extra fields, and native boolean motion `.buttons`.
There are no list proxies and no cloned pygame events. Wheel pseudo-buttons remain in
these lists but do not enter new button state or double-count modern scrolling.

The renderer retains native coordinates. `draw.tick()` and `draw.sleep()` subsequently
convert the legacy mouse lists using the final transform, preserving old resize timing.
New events capture the transform in queue order before that conversion. Thus the contracts
intentionally differ around resize: for example a native x=20 event at scale 5, followed
by a resize to scale 10, is x=100 in the new event and x=200 in the public legacy event.
New final pointer state is rescaled at publication, without rewriting historical events.

GUI helper functions still query pygame on demand. The `KeysPressed` wrapper keeps the
backend snapshot supplied at construction; saved wrappers do not become live manager
views. Numeric lookup and exact existing attribute-name string lookup, indexing and
membership, remain supported. Unsupported object lookup still returns false. The wrapper
can retain its former exceptions for invalid legacy strings/codes. Three-button helper
results remain three-element tuples; modifiers remain integer masks. New strict argument
validation is not retrofitted onto old helpers.

EJUDGE placeholders are repaired to neutral indexable key state, three false buttons,
integer zero modifiers, and `(0, 0)` pointer coordinates. Input reads print nothing and
import no pygame. Drawing JSON and tick/sleep record shapes are unchanged.

`tick(r=1, *, fps=30)` adds only a keyword-only parameter. Return value remains `None`,
presentation precedes waiting/polling, positional r still uses `range(r)`, and sleep still
rounds using `int(t * 30 + 0.5)`. Zero-count calls do not poll. Renderer callers retain
`display_update`; private `wait=False` supports deterministic verification. Explicit quit
marks the renderer closed; drawing cannot recreate it. The static atexit loop runs only
for an existing open surface and handles normal close without an ignored-exception log.

The original examples 16–20 were copied unmodified to `tests/fixtures/legacy_examples/`
before published examples were changed. Characterization tests were written and run with
stdlib `runpy` before implementation (pytest was initially absent). They recorded list
identity, event type/mutability, coordinates, key aliases, helper shapes, returns, poll
counts, `tick(0)`, `sleep(0)`, and sleep rounding.

## Ownership and cost

`utils/input.py` is GUI-independent. `_Input.begin/feed/reconcile/publish` is the private
injection seam used by tests. `input_pygame.py` translates the same production queue;
only the renderer drains it. `tick(r)` and `sleep()` open one accumulation frame and
publish once, not once per poll.

Held sets, physical-scancode associations, and logical reference counts are private.
Physical release resolves through the remembered logical identity, so layout changes and
two physical keys mapped to one logical key do not strand or prematurely release keys.
Grouped modifier edges derive from aggregate state at each transition. Repeat metadata
or an existing identity suppresses repeat edges. Reconciliation is explicit after focus
gain: pygame's final logical held state replaces final held sets without touching genuine
historical edges. Scancode associations rebuild afterward; pygame supplies no authoritative
per-scancode snapshot through this interface.

Compact records snapshot only required immutable payloads, with no retained backend event
or `.dict` reference. Public NamedTuple event/provenance instances are constructed lazily.
The common and device event tuples, text aggregate, coordinate tuples, and eight small
button-membership sets are cached. Old public tuples own immutable objects permanently;
no public object pool is reused. No events are coalesced or silently dropped.

Queries do bounded key resolution and direct set membership, never event-history scans,
OS polls, Pt construction, event wrapping, or snapshots. Successful string resolution has
a 256-entry LRU; fuzzy matching runs only on an error. All arguments are validated even
after a match. Published held sets are copied once per boundary; edge sets/record lists
are transferred and replaced for the next frame. These are small allocations, not a claim
of allocation-free ingestion. Complete history costs O(events in a frame or retained by
users), including long sleep calls. There is no history growing with elapsed frame count.

The font cache is a separate small repair: look up before constructing, then store the
font on a miss. Its benchmark is reported separately from input costs.

## Backend evidence and limits

Checked pygame-ce 2.5.6 `src_c/event.c`, SDL_MOUSEWHEEL conversion: x/y and precise values
are copied unchanged and `flipped` is copied separately. The reducer therefore applies
one sign correction. Positive normalized x is right; positive y is away/up. Missing
historical wheel position stays `None` (2.5.6 does not provide it).

References:

- [pygame event payloads and queue limits](https://pyga.me/docs/ref/event.html)
- [pygame key and text behavior](https://pyga.me/docs/ref/key.html)
- [pygame mouse behavior](https://pyga.me/docs/ref/mouse.html)
- [SDL wheel direction and precision](https://wiki.libsdl.org/SDL2/SDL_MouseWheelEvent)
- [SDL logical symbol versus scancode](https://wiki.libsdl.org/SDL2/SDL_Keysym)
- [Pinned pygame-ce 2.5.6 event conversion](https://github.com/pygame-community/pygame-ce/blob/2.5.6/src_c/event.c)

Current online pygame documentation describes newer releases too. Optional fields are
read defensively; no use is made of new backend edge getters, which would have the wrong
boundary for multi-poll DrawZero frames. No repeat or text-input lifecycle toggles were
introduced. Pygame generally cannot identify which releases were synthesized on focus
loss; an explicitly supplied `cancelled` marker is preserved, but unavailable provenance
is not inferred. No manual hardware, IME, alternate-layout, Windows, Linux, or macOS
native-window checks are claimed. SDL dummy queue tests and injected state tests are
separate from hardware verification.
