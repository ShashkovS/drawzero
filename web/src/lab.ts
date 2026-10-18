/**
 * DrawLab: a canvas plus the Python that draws on it. The page owns the
 * controls; this owns the protocol — frames are drawn on the next animation
 * frame and acknowledged through the shared mailbox, keyboard and mouse on
 * the canvas go back into shared memory, and Stop always ends a run: by
 * waking a waiting frame, interrupting a computation, or as a last resort
 * replacing the worker.
 */
import { Scene } from "./scene";
import { type Color, EVENT_BYTES, type InputEvent, MAILBOX_BYTES, MB, type Op, type RunResult } from "./types";

const STOP_GRACE_MS = 1500;

export function support(): { ok: true } | { ok: false; reason: string } {
  if (typeof Worker !== "function") return { ok: false, reason: "this browser has no Web Workers" };
  if (typeof SharedArrayBuffer !== "function" || !(globalThis as any).crossOriginIsolated) {
    return { ok: false, reason: "this page is not cross-origin isolated, so drawings cannot run here" };
  }
  return { ok: true };
}

// ---------------------------------------------------------------------- host

type RunHandlers = { frame(seq: number, ops: string): void; out(text: string): void; done(result: RunResult): void };

/** One Pyodide worker per page, shared by every lab on it. */
class Host {
  private worker: Worker | null = null;
  private ready: Promise<void> | null = null;
  readonly memory = new SharedArrayBuffer(MAILBOX_BYTES);
  readonly mailbox = new Int32Array(this.memory, 0, MB.HEADER);
  private bytes = new Uint8Array(this.memory, MB.HEADER * 4, EVENT_BYTES);
  readonly interrupt = new Int32Array(new SharedArrayBuffer(4));
  private encoder = new TextEncoder();
  private nextId = 1;
  private runs = new Map<number, RunHandlers>();
  private lock: Promise<void> = Promise.resolve();
  version = "";

  constructor(private workerUrl: URL) {}

  start(): Promise<void> {
    if (this.ready) return this.ready;
    this.ready = new Promise((resolve, reject) => {
      const w = new Worker(this.workerUrl, { type: "module" });
      this.worker = w;
      w.onmessage = (e) => {
        const m = e.data;
        if (m.type === "ready") { this.version = m.version; resolve(); }
        else if (m.type === "failed") { this.ready = null; reject(new Error(m.error)); }
        else if (m.type === "frame") this.runs.get(m.runId)?.frame(m.seq, m.ops);
        else if (m.type === "out") this.runs.get(m.runId)?.out(m.text);
        else if (m.type === "done") { const h = this.runs.get(m.runId); this.runs.delete(m.runId); h?.done(m.result); }
      };
      w.onerror = (e) => { this.ready = null; reject(new Error(e.message || "the drawzero worker failed to start")); };
      w.postMessage({ type: "init", mailbox: this.memory, interrupt: this.interrupt.buffer });
    });
    return this.ready;
  }

  /** Serialise: a running program blocks the worker. */
  private exclusive<T>(fn: () => Promise<T>): Promise<T> {
    const result = this.lock.then(fn, fn);
    this.lock = result.then(() => undefined, () => undefined);
    return result;
  }

  run(source: string, stdin: string, handlers: RunHandlers): { runId: number; finished: Promise<RunResult> } {
    const runId = this.nextId++;
    const finished = this.exclusive(async () => {
      await this.start();
      Atomics.store(this.mailbox, MB.CANCEL, 0);
      Atomics.store(this.mailbox, MB.SHOWN, 0);
      Atomics.store(this.mailbox, MB.EV_LEN, 0);
      Atomics.store(this.mailbox, MB.RUN, runId);
      Atomics.store(this.interrupt, 0, 0);
      return new Promise<RunResult>((resolve) => {
        this.runs.set(runId, { ...handlers, done: (r) => { handlers.done(r); resolve(r); } });
        this.worker!.postMessage({ type: "run", runId, source, stdin });
      });
    });
    return { runId, finished };
  }

  current(runId: number): boolean {
    return Atomics.load(this.mailbox, MB.RUN) === runId && this.runs.has(runId);
  }

  shown(runId: number, seq: number): void {
    if (Atomics.load(this.mailbox, MB.RUN) !== runId) return;
    Atomics.store(this.mailbox, MB.SHOWN, seq);
    Atomics.notify(this.mailbox, MB.SHOWN);
  }

  /** Hand an input event to the running program; dropped when the buffer is full. */
  send(runId: number, event: InputEvent): void {
    if (!this.current(runId)) return;
    const data = this.encoder.encode(JSON.stringify(event) + "\n");
    while (Atomics.compareExchange(this.mailbox, MB.EV_LOCK, 0, 1) !== 0) { /* the worker holds it for microseconds */ }
    const n = Atomics.load(this.mailbox, MB.EV_LEN);
    if (n + data.length <= EVENT_BYTES) {
      this.bytes.set(data, n);
      Atomics.store(this.mailbox, MB.EV_LEN, n + data.length);
    }
    Atomics.store(this.mailbox, MB.EV_LOCK, 0);
  }

  cancel(runId: number): void {
    if (Atomics.load(this.mailbox, MB.RUN) !== runId) return;
    Atomics.store(this.mailbox, MB.CANCEL, 1);
    Atomics.notify(this.mailbox, MB.CANCEL);
    Atomics.notify(this.mailbox, MB.SHOWN);
    Atomics.store(this.interrupt, 0, 2); // SIGINT for a loop that never draws a frame
  }

  /** The worker did not stop in time: replace it and end the run as stopped. */
  kill(runId: number): void {
    const h = this.runs.get(runId);
    this.runs.delete(runId);
    this.worker?.terminate();
    this.worker = null;
    this.ready = null;
    h?.done({ status: "stopped", error: null, frames: 0, ms: 0 });
  }
}

let shared: Host | null = null;

export function host(workerUrl?: URL): Host {
  if (!shared) shared = new Host(workerUrl ?? new URL("./worker.js", import.meta.url));
  return shared;
}

// ---------------------------------------------------------------------- lab

export type LabState = "idle" | "loading" | "running" | "done";
type Events = {
  state: (s: LabState) => void;
  output: (text: string) => void;
  done: (r: RunResult) => void;
};

/** Keys whose browser action (scrolling, find, back) would fight a game. */
const OWN_KEYS = new Set(["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Space", "PageUp", "PageDown",
  "Home", "End", "Backspace", "Slash", "Quote", "Enter", "Escape"]);

export class DrawLab {
  readonly scene: Scene;
  private host: Host;
  private listeners: { [K in keyof Events]: Events[K][] } = { state: [], output: [], done: [] };
  private runId = 0;
  private pending: { seq: number; ops: Op[] }[] = [];
  private raf = 0;
  private stopping: ReturnType<typeof setTimeout> | null = null;
  private detach: () => void;
  state: LabState = "idle";
  frames = 0;
  /** The blank canvas: black for drawzero, white for a turtle (`background: [255, 255, 255, 255]`). */
  private background: Color;

  constructor(container: Element, options: { workerUrl?: URL; label?: string; background?: Color } = {}) {
    this.scene = new Scene(container, options);
    this.background = options.background ?? [0, 0, 0, 255];
    this.scene.reset(this.background);
    this.host = host(options.workerUrl);
    this.detach = this.listen();
  }

  on<K extends keyof Events>(event: K, fn: Events[K]): () => void {
    this.listeners[event].push(fn);
    return () => { this.listeners[event] = this.listeners[event].filter((f) => f !== fn) as any; };
  }

  private emit<K extends keyof Events>(event: K, ...args: Parameters<Events[K]>): void {
    for (const fn of this.listeners[event]) (fn as any)(...args);
  }

  private setState(s: LabState): void {
    this.state = s;
    this.emit("state", s);
  }

  get running(): boolean { return this.state === "loading" || this.state === "running"; }

  /** Start the worker early, so the first Run does not wait for Pyodide. */
  preload(): Promise<void> {
    return support().ok ? this.host.start() : Promise.resolve();
  }

  /** Run `source` with `stdin` on a fresh blank canvas. */
  async run(source: string, stdin = ""): Promise<RunResult> {
    if (this.running) this.stop();
    const why = support();
    if (!why.ok) {
      const r: RunResult = { status: "crashed", error: { type: "RuntimeError", message: why.reason, line: null, traceback: "" }, frames: 0, ms: 0 };
      this.emit("done", r);
      return r;
    }
    this.scene.reset(this.background);
    this.pending = [];
    this.frames = 0;
    this.setState("loading");
    const { runId, finished } = this.host.run(source, stdin, {
      frame: (seq, ops) => {
        if (runId !== this.runId) return;
        if (this.state === "loading") this.setState("running");
        this.pending.push({ seq, ops: JSON.parse(ops) });
        this.schedule();
      },
      out: (text) => { if (runId === this.runId) this.emit("output", text); },
      done: (r) => { if (runId === this.runId) this.finish(r); },
    });
    this.runId = runId;
    return finished;
  }

  private schedule(): void {
    if (!this.raf) this.raf = requestAnimationFrame(() => { this.raf = 0; this.draw(); });
  }

  /** Draw every frame that has arrived; only the result reaches the screen. */
  private draw(): void {
    if (!this.pending.length) return;
    const batch = this.pending;
    this.pending = [];
    const ops: Op[] = [];
    for (const f of batch) for (const op of f.ops) ops.push(op);
    this.scene.apply(ops);
    this.frames = batch[batch.length - 1].seq;
    this.host.shown(this.runId, this.frames);
  }

  stop(): void {
    if (!this.running) return;
    const runId = this.runId;
    this.host.cancel(runId);
    this.stopping = setTimeout(() => { if (this.runId === runId && this.running) this.host.kill(runId); }, STOP_GRACE_MS);
  }

  /** Stop, and a blank canvas. */
  reset(): void {
    this.stop();
    this.pending = [];
    this.scene.reset(this.background);
    if (!this.running) this.setState("idle");
  }

  private finish(r: RunResult): void {
    if (this.stopping) { clearTimeout(this.stopping); this.stopping = null; }
    if (this.raf) { cancelAnimationFrame(this.raf); this.raf = 0; }
    this.draw();
    this.setState("done");
    this.emit("done", r);
  }

  // -------------------------------------------------------------- input

  private send(event: InputEvent): void {
    if (this.running) this.host.send(this.runId, event);
  }

  private point(e: MouseEvent): { x: number; y: number; k: number } {
    const box = this.scene.svg.getBoundingClientRect();
    const k = 1000 / (box.width || 1);
    return { x: +((e.clientX - box.left) * k).toFixed(2), y: +((e.clientY - box.top) * 1000 / (box.height || 1)).toFixed(2), k };
  }

  private listen(): () => void {
    const svg = this.scene.svg;
    const on = <K extends keyof SVGElementEventMap>(type: K, fn: (e: SVGElementEventMap[K]) => void, opts?: AddEventListenerOptions) => {
      svg.addEventListener(type, fn as EventListener, opts);
      return () => svg.removeEventListener(type, fn as EventListener, opts);
    };
    const offs = [
      on("keydown", (e) => {
        if (!this.running || e.isComposing) return;
        if (!e.ctrlKey && !e.metaKey && !e.altKey && (OWN_KEYS.has(e.code) || e.key.length === 1)) e.preventDefault();
        this.send({ t: "kd", code: e.code, key: e.key, r: e.repeat || undefined, ctrl: e.ctrlKey || e.metaKey || undefined });
      }),
      on("keyup", (e) => { if (this.running) this.send({ t: "ku", code: e.code, key: e.key }); }),
      on("pointerdown", (e) => {
        if (!this.running) return;
        svg.focus({ preventScroll: true });
        e.preventDefault();
        if (e.button > 2) return;
        svg.setPointerCapture(e.pointerId);
        const p = this.point(e);
        this.send({ t: "md", b: [1, 2, 3][e.button], x: p.x, y: p.y });
      }),
      on("pointerup", (e) => {
        if (!this.running || e.button > 2) return;
        const p = this.point(e);
        this.send({ t: "mu", b: [1, 2, 3][e.button], x: p.x, y: p.y });
      }),
      on("pointermove", (e) => {
        if (!this.running) return;
        const p = this.point(e);
        this.send({ t: "mm", x: p.x, y: p.y, dx: +(e.movementX * p.k).toFixed(2), dy: +(e.movementY * p.k).toFixed(2),
          bs: [e.buttons & 1 ? 1 : 0, e.buttons & 4 ? 1 : 0, e.buttons & 2 ? 1 : 0] });
      }),
      on("wheel", (e) => {
        if (!this.running) return;
        e.preventDefault();
        const unit = e.deltaMode === 1 ? 1 : e.deltaMode === 2 ? 10 : 1 / 100;
        const p = this.point(e);
        // pygame: wheel up is positive y
        this.send({ t: "mw", dx: +(e.deltaX * unit).toFixed(3), dy: +(-e.deltaY * unit).toFixed(3), x: p.x, y: p.y });
      }, { passive: false }),
      on("contextmenu", (e) => { if (this.running) e.preventDefault(); }),
      on("focus", () => this.send({ t: "fg" })),
      on("blur", () => this.send({ t: "fl" })),
    ];
    return () => offs.forEach((off) => off());
  }

  destroy(): void {
    this.stop();
    this.detach();
    this.scene.destroy();
  }
}
