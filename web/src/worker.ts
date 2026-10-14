/**
 * drawzero's Python, in a module worker. Pyodide comes from the course's own
 * `s/pyrun/boot.js` (one pinned version for every worker in the course), the
 * library from its wheel beside flake8's.
 *
 * Drawing is fire-and-forget: Python collects operations and hands a frame
 * over at every `tick()`/`sleep()` (or when a long loop has drawn a lot). The
 * frame call posts the operations to the page, then blocks this worker for
 * the frame's time — on the shared mailbox, so Stop wakes it — and returns
 * the input events the page has left in shared memory meanwhile.
 *
 * main -> worker: {type:'init', mailbox, interrupt}
 *                 {type:'run', runId, source, stdin}
 * worker -> main: {type:'ready', version} | {type:'failed', error}
 *                 {type:'frame', runId, seq, ops}  (ops: JSON text)
 *                 {type:'out', runId, text}
 *                 {type:'done', runId, result}
 */
import { EVENT_BYTES, MAX_BACKLOG, MB } from "./types";

declare const __DRAWZERO_VERSION__: string;
const VERSION = __DRAWZERO_VERSION__;
const BOOT_URL = new URL("../pyrun/boot.js", import.meta.url).href;
const WHEEL_URL = new URL(`../pyodide/wheels/drawzero-${VERSION}-py3-none-any.whl`, import.meta.url).href;

const OUTPUT_LIMIT = 1_000_000;
const FLUSH_CHARS = 4096;

const GLUE = `
import json
import sys
import traceback

from drawzero import __version__
from drawzero.utils import renderer_browser, screen_size


def _frames_from_solution(tb):
    # A student's traceback starts in their code, not in this module.
    while tb is not None and tb.tb_frame.f_code.co_filename != "solution.py":
        tb = tb.tb_next
    return tb


def _error(error):
    line = None
    if isinstance(error, SyntaxError) and error.filename == "solution.py":
        line = error.lineno
        text = "".join(traceback.format_exception_only(type(error), error))
    else:
        tb = _frames_from_solution(error.__traceback__)
        for frame in traceback.extract_tb(tb):
            if frame.filename == "solution.py":
                line = frame.lineno
        text = "".join(traceback.format_exception(type(error), error, tb))
    return {"type": type(error).__name__, "message": str(error), "line": line, "traceback": text}


def run_solution(source, frame):
    renderer_browser.connect(frame)
    screen_size.set_virtual_size(1000, 1000)
    namespace = {"__name__": "__main__", "__builtins__": __builtins__}
    status, error = "ok", None
    try:
        exec(compile(source, "solution.py", "exec"), namespace)
    except KeyboardInterrupt:
        status = "stopped"
    except SystemExit as e:
        if e.code not in (None, 0):
            status, error = "error", {"type": "SystemExit", "message": str(e.code), "line": None,
                                      "traceback": f"SystemExit: {e.code}\\n"}
    except BaseException as e:
        status, error = "error", _error(e)
    if status != "stopped":
        # What was drawn before an error stays on the screen.
        try:
            renderer_browser.flush()
        except KeyboardInterrupt:
            status = "stopped"
    sys.stdout.flush()
    sys.stderr.flush()
    return json.dumps({"status": status, "error": error})
`;

let pyodide: any = null;
let mailbox: Int32Array;
let eventBytes: Uint8Array;
let interrupt: Int32Array | null = null;
let currentRun = 0;
let seq = 0;
let lastTick = 0;
let out = "";
let outTotal = 0;
let stdinText: string | null = null;
const decoder = new TextDecoder();

function flush(): void {
  if (out) {
    postMessage({ type: "out", runId: currentRun, text: out });
    out = "";
  }
}

function write(buf: Uint8Array): number {
  if (outTotal < OUTPUT_LIMIT) {
    const text = decoder.decode(buf, { stream: true });
    outTotal += text.length;
    out += outTotal < OUTPUT_LIMIT ? text : text + "\n… output truncated\n";
    if (out.length >= FLUSH_CHARS) flush();
  }
  return buf.length;
}

/** Take the events the page has written since the last frame. */
function takeEvents(): string {
  while (Atomics.compareExchange(mailbox, MB.EV_LOCK, 0, 1) !== 0) { /* the page holds it for microseconds */ }
  const n = Atomics.load(mailbox, MB.EV_LEN);
  const text = n ? decoder.decode(eventBytes.slice(0, n)) : "";
  Atomics.store(mailbox, MB.EV_LEN, 0);
  Atomics.store(mailbox, MB.EV_LOCK, 0);
  return "[" + text.split("\n").filter(Boolean).join(",") + "]";
}

const cancelled = () => Atomics.load(mailbox, MB.CANCEL) !== 0;

/** Python's frame function: show `ops`, keep them for `wait` seconds, return the input. */
(self as any).drawzeroFrame = (ops: string, wait: number): string | null => {
  flush();
  seq += 1;
  postMessage({ type: "frame", runId: currentRun, seq, ops });
  // pygame's Clock: the frame lasts `wait` since the previous one, so drawing
  // time is part of it, and a slow frame does not wait at all.
  const target = lastTick + wait * 1000;
  for (;;) {
    if (cancelled()) return null;
    const shown = Atomics.load(mailbox, MB.SHOWN);
    if (seq - shown > MAX_BACKLOG) {
      // The page is behind (or hidden): wait for it rather than pile up frames.
      Atomics.wait(mailbox, MB.SHOWN, shown, 100);
      continue;
    }
    const left = target - performance.now();
    if (left <= 0) break;
    Atomics.wait(mailbox, MB.CANCEL, 0, Math.min(left, 100));
  }
  lastTick = performance.now();
  return takeEvents();
};

async function init(msg: any): Promise<void> {
  mailbox = new Int32Array(msg.mailbox);
  eventBytes = new Uint8Array(msg.mailbox, MB.HEADER * 4, EVENT_BYTES);
  interrupt = msg.interrupt instanceof SharedArrayBuffer ? new Int32Array(msg.interrupt) : null;
  const { boot } = await import(/* @vite-ignore */ BOOT_URL);
  pyodide = await boot({ interrupt });
  await pyodide.loadPackage(WHEEL_URL);
  pyodide.setStdout({ write });
  pyodide.setStderr({ write });
  pyodide.setStdin({ stdin: () => { const t = stdinText; stdinText = null; return t || null; } });
  pyodide.runPython(GLUE);
  const version = pyodide.runPython("__version__");
  if (version !== VERSION) throw new Error(`drawzero wheel ${version} does not match the web build ${VERSION}`);
  postMessage({ type: "ready", version });
}

async function run(msg: any): Promise<void> {
  currentRun = msg.runId;
  seq = 0;
  lastTick = performance.now();
  out = "";
  outTotal = 0;
  stdinText = msg.stdin ?? "";
  if (interrupt) interrupt[0] = 0;
  const started = performance.now();
  const runSolution = pyodide.globals.get("run_solution");
  let result: any;
  try {
    result = JSON.parse(runSolution(msg.source, (self as any).drawzeroFrame));
  } catch (e: any) {
    const text = String(e?.message ?? e);
    result = text.includes("KeyboardInterrupt")
      ? { status: "stopped", error: null }
      : { status: "crashed", error: { type: "RuntimeError", message: text, line: null, traceback: text } };
  } finally {
    runSolution.destroy();
  }
  flush();
  postMessage({ type: "done", runId: msg.runId, result: { ...result, frames: seq, ms: Math.round(performance.now() - started) } });
}

self.onmessage = async (event: MessageEvent) => {
  const msg = event.data;
  try {
    if (msg.type === "init") await init(msg);
    else if (msg.type === "run") await run(msg);
  } catch (e: any) {
    if (msg.type === "init") postMessage({ type: "failed", error: String(e?.message ?? e) });
    else postMessage({ type: "done", runId: msg.runId, result: {
      status: "crashed", error: { type: "RuntimeError", message: String(e?.message ?? e), line: null, traceback: "" }, frames: seq, ms: 0 } });
  }
};
