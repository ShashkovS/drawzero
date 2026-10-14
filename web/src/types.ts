/** A drawing operation, exactly as `renderer_browser.py` writes it. */
export type Color = [number, number, number, number];
export type Op =
  | ["line", Color, number, number, number, number, number]
  | ["circle", Color, number, number, number, number]
  | ["rect", Color, number, number, number, number, number]
  | ["ellipse", Color, number, number, number, number, number]
  | ["arc", Color, number, number, number, number, number, number, number]
  | ["polygon", Color, number, number[]]
  | ["text", Color, string, number, number, number, string]
  | ["fill", Color]
  | ["clear"];

/** An input event for Python's `_ingest`. Coordinates are canvas pixels (0..1000). */
export type InputEvent =
  | { t: "kd" | "ku"; code: string; key: string; r?: boolean; ctrl?: boolean }
  | { t: "md" | "mu"; b: number; x: number; y: number }
  | { t: "mm"; x: number; y: number; dx: number; dy: number; bs: [number, number, number] }
  | { t: "mw"; dx: number; dy: number; x: number; y: number }
  | { t: "fg" | "fl" };

export type RunError = { type: string; message: string; line: number | null; traceback: string };

export type RunResult = {
  /** ok: the program ended; error: it raised; stopped: Stop; crashed: the runtime itself failed. */
  status: "ok" | "error" | "stopped" | "crashed";
  error: RunError | null;
  frames: number;
  ms: number;
};

/**
 * Shared memory (Int32 slots, then the event bytes). The page writes input
 * events under EV_LOCK; the worker takes them at every frame. The worker
 * paces itself on CANCEL and waits on SHOWN when the page falls behind.
 */
export const MB = { CANCEL: 0, RUN: 1, SHOWN: 2, EV_LOCK: 3, EV_LEN: 4, HEADER: 8 } as const;
export const EVENT_BYTES = 64 * 1024;
export const MAILBOX_BYTES = MB.HEADER * 4 + EVENT_BYTES;
/** Frames the worker may run ahead of the screen. */
export const MAX_BACKLOG = 2;
