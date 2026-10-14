/** drawzero in the browser: the lab (canvas + Python) and the statement marker. */
import { define } from "./element";

declare const __DRAWZERO_VERSION__: string;
export const VERSION = __DRAWZERO_VERSION__;

export { DrawLab, support, host, type LabState } from "./lab";
export { Scene, shape, covers, SIZE } from "./scene";
export { DrawzeroCanvas, define } from "./element";
export type { Op, Color, InputEvent, RunResult, RunError } from "./types";

if (typeof customElements !== "undefined") define();
