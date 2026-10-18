/**
 * The canvas: an SVG of drawzero's 1000x1000 surface, drawn the way pygame
 * draws it. Drawing accumulates until `clear()` or an opaque `fill()`, as on
 * pygame's surface.
 *
 * pygame's rules kept here:
 * - circle, rect, ellipse and arc borders lie inside the shape; a width of 0,
 *   or one that reaches the middle, fills it; a negative width draws nothing;
 * - line and polygon borders are centred on the path, with square ends;
 * - an RGBA colour carries its own alpha (Python resolves it), and a shape is
 *   blended as a whole, never its overlapping strokes twice;
 * - text is FreeSans Bold at 0.6875 of the size, opaque, aligned by `align`
 *   (horizontal `<.>`, then vertical `^.v`).
 *
 * Two operations are a turtle's: `bg` changes the background under the
 * picture, and `sprites` replaces what lies over it (the turtles themselves).
 *
 * A program that never clears keeps adding elements; past a limit the oldest
 * ones are flattened into one picture so the page stays quick.
 */
import type { Color, Op } from "./types";

const NS = "http://www.w3.org/2000/svg";
export const SIZE = 1000;
const FLATTEN_AT = 6000;
const FONT = "FreeSans, 'Liberation Sans', Arial, Helvetica, sans-serif";

function el(name: string, attrs: Record<string, string | number>): SVGElement {
  const e = document.createElementNS(NS, name);
  for (const k in attrs) e.setAttribute(k, String(attrs[k]));
  return e;
}

const rgb = (c: Color) => `rgb(${c[0]},${c[1]},${c[2]})`;

function paint(e: SVGElement, c: Color, stroke: number): SVGElement {
  if (stroke > 0) {
    e.setAttribute("fill", "none");
    e.setAttribute("stroke", rgb(c));
    e.setAttribute("stroke-width", String(stroke));
  } else {
    e.setAttribute("fill", rgb(c));
  }
  if (c[3] < 255) e.setAttribute("opacity", String(+(c[3] / 255).toFixed(4)));
  return e;
}

/** A box border inside (x, y, w, h): the stroke's centre line, or null to fill. */
function inset(x: number, y: number, w: number, h: number, width: number) {
  if (w < 0) { x += w; w = -w; }
  if (h < 0) { y += h; h = -h; }
  if (width <= 0 || 2 * width >= Math.min(w, h)) return { x, y, w, h, stroke: 0 };
  const d = width / 2;
  return { x: x + d, y: y + d, w: w - width, h: h - width, stroke: width };
}

/** One SVG element for an operation, or null when pygame would draw nothing. */
export function shape(op: Op): SVGElement | null {
  switch (op[0]) {
    case "line": {
      const [, c, w, x1, y1, x2, y2] = op;
      if (w < 1) return null;
      return paint(el("line", { x1, y1, x2, y2 }), c, w);
    }
    case "circle": {
      const [, c, w, cx, cy, r] = op;
      if (w < 0 || r < 1) return null;
      if (w === 0 || w >= r) return paint(el("circle", { cx, cy, r }), c, 0);
      return paint(el("circle", { cx, cy, r: r - w / 2 }), c, w);
    }
    case "rect": {
      const [, c, w, x0, y0, w0, h0] = op;
      if (w < 0) return null;
      const b = inset(x0, y0, w0, h0, w);
      return paint(el("rect", { x: b.x, y: b.y, width: b.w, height: b.h }), c, b.stroke);
    }
    case "ellipse": {
      const [, c, w, x0, y0, w0, h0] = op;
      if (w < 0) return null;
      const b = inset(x0, y0, w0, h0, w);
      return paint(el("ellipse", { cx: b.x + b.w / 2, cy: b.y + b.h / 2, rx: b.w / 2, ry: b.h / 2 }), c, b.stroke);
    }
    case "arc": {
      const [, c, w, x0, y0, w0, h0, start, stop0] = op;
      if (w < 1) return null;
      const cx = x0 + w0 / 2, cy = y0 + h0 / 2;
      const width = Math.min(w, Math.abs(w0) / 2, Math.abs(h0) / 2);
      if (width <= 0) return null;
      const rx = Math.abs(w0) / 2 - width / 2, ry = Math.abs(h0) / 2 - width / 2;
      let stop = stop0;
      while (stop < start) stop += 2 * Math.PI;
      if (stop - start >= 2 * Math.PI - 1e-9) return paint(el("ellipse", { cx, cy, rx, ry }), c, width);
      // Angles go anticlockwise on the screen, from three o'clock.
      const px = (a: number) => +(cx + rx * Math.cos(a)).toFixed(3);
      const py = (a: number) => +(cy - ry * Math.sin(a)).toFixed(3);
      const large = stop - start > Math.PI ? 1 : 0;
      const d = `M${px(start)} ${py(start)}A${rx} ${ry} 0 ${large} 0 ${px(stop)} ${py(stop)}`;
      return paint(el("path", { d }), c, width);
    }
    case "polygon": {
      const [, c, w, flat] = op;
      if (w < 0 || flat.length < 4) return null;
      const e = paint(el("polygon", { points: flat.join(" ") }), c, w);
      if (w > 0) e.setAttribute("stroke-linejoin", "miter");
      return e;
    }
    case "text": {
      const [, c, text, x, y, size, align, font] = op;
      // drawzero's text is FreeSans Bold; a turtle's names its font, and its size is the pixel size.
      const e = el("text", {
        x, y, fill: rgb(c),
        "font-family": font ? `${JSON.stringify(font[0])}, ${FONT}` : FONT,
        "font-weight": font ? font[1] : "bold",
        "font-style": font ? font[2] : "normal",
        "font-size": font ? size : +(size * 0.6875).toFixed(2),
        "text-anchor": align[0] === "<" ? "start" : align[0] === ">" ? "end" : "middle",
        "dominant-baseline": align[1] === "^" ? "text-before-edge" : align[1] === "v" ? "text-after-edge" : "central",
      });
      e.setAttribute("style", "white-space:pre");
      e.textContent = text;
      return e;
    }
    case "path": {
      // A turtle's line: centred on the path, with round ends and joins, as in Tk.
      const [, c, w, flat] = op;
      if (w <= 0 || flat.length < 4) return null;
      const e = paint(el("polyline", { points: flat.join(" ") }), c, w);
      e.setAttribute("stroke-linecap", "round");
      e.setAttribute("stroke-linejoin", "round");
      return e;
    }
    case "fill": {
      const [, c] = op;
      return paint(el("rect", { x: 0, y: 0, width: SIZE, height: SIZE }), c, 0);
    }
    default:
      return null;
  }
}

/** Does this operation hide everything drawn before it? */
export function covers(op: Op): boolean {
  return op[0] === "clear" || (op[0] === "fill" && op[1][3] === 255);
}

export class Scene {
  readonly svg: SVGSVGElement;
  private background: SVGRectElement;
  private layer: SVGGElement;
  /** What moves over the picture without leaving copies: the turtles. */
  private sprites: SVGGElement;
  private count = 0;
  private generation = 0;
  private flattening = false;

  constructor(container: Element, options: { label?: string } = {}) {
    this.svg = el("svg", { viewBox: `0 0 ${SIZE} ${SIZE}`, xmlns: NS, tabindex: 0, role: "img" }) as SVGSVGElement;
    this.svg.setAttribute("aria-label", options.label ?? "drawzero canvas");
    this.svg.style.cssText = "display:block;width:100%;height:auto;aspect-ratio:1;background:#000;outline:none;touch-action:none;user-select:none";
    this.background = el("rect", { x: 0, y: 0, width: SIZE, height: SIZE, fill: "rgb(0,0,0)" }) as SVGRectElement;
    this.layer = el("g", {}) as SVGGElement;
    this.sprites = el("g", { "data-sprites": "" }) as SVGGElement;
    this.svg.append(this.background, this.layer, this.sprites);
    container.appendChild(this.svg);
  }

  /** A blank canvas, as at the start of a program: black, or `background` (a turtle's is white). */
  reset(background: Color = [0, 0, 0, 255]): void {
    this.cover(background);
  }

  private cover(c: Color): void {
    this.generation += 1;
    this.background.setAttribute("fill", rgb(c));
    this.layer.replaceChildren();
    this.sprites.replaceChildren();
    this.count = 0;
  }

  /** Draw operations in order. Everything before the last covering one is skipped. */
  apply(ops: Op[]): void {
    let from = 0;
    for (let i = ops.length - 1; i >= 0; i--) {
      if (covers(ops[i])) { from = i; break; }
    }
    const frag = document.createDocumentFragment();
    let added = 0;
    let sprites: Op[] | null = null;
    for (let i = from; i < ops.length; i++) {
      const op = ops[i];
      if (covers(op)) {
        this.cover(op[0] === "clear" ? [0, 0, 0, 255] : (op as ["fill", Color])[1]);
        continue;
      }
      if (op[0] === "bg") {
        // The background changes under what is drawn, unlike fill().
        this.background.setAttribute("fill", rgb(op[1]));
        continue;
      }
      if (op[0] === "sprites") {
        sprites = op[1];
        continue;
      }
      const e = shape(op);
      if (e) { frag.appendChild(e); added++; }
    }
    this.layer.appendChild(frag);
    this.count += added;
    if (sprites) {
      const top = document.createDocumentFragment();
      for (const op of sprites) { const e = shape(op); if (e) top.appendChild(e); }
      this.sprites.replaceChildren(top);
    }
    if (this.count > FLATTEN_AT && !this.flattening) void this.flatten();
  }

  get elementCount(): number { return this.count; }

  /** The picture as a standalone SVG document. */
  toSVG(): string {
    return new XMLSerializer().serializeToString(this.svg);
  }

  /** Replace the elements drawn so far by one bitmap of them. */
  private async flatten(): Promise<void> {
    this.flattening = true;
    const generation = this.generation;
    const nodes = Array.from(this.layer.childNodes);
    try {
      const doc = `<svg xmlns="${NS}" viewBox="0 0 ${SIZE} ${SIZE}" width="${SIZE}" height="${SIZE}">`
        + nodes.map((n) => new XMLSerializer().serializeToString(n)).join("") + "</svg>";
      const img = new Image();
      img.src = URL.createObjectURL(new Blob([doc], { type: "image/svg+xml" }));
      try { await img.decode(); } finally { URL.revokeObjectURL(img.src); }
      const scale = Math.min(2, Math.max(1, globalThis.devicePixelRatio || 1));
      const canvas = document.createElement("canvas");
      canvas.width = canvas.height = SIZE * scale;
      canvas.getContext("2d")!.drawImage(img, 0, 0, canvas.width, canvas.height);
      if (generation !== this.generation) return; // cleared meanwhile: nothing to flatten
      const bitmap = el("image", { x: 0, y: 0, width: SIZE, height: SIZE, href: canvas.toDataURL("image/png") });
      this.layer.insertBefore(bitmap, nodes[0] ?? null);
      for (const n of nodes) n.parentNode === this.layer && this.layer.removeChild(n);
      this.count -= nodes.length - 1;
    } catch {
      // A picture that cannot be flattened stays as it is.
    } finally {
      this.flattening = false;
    }
  }

  destroy(): void {
    this.svg.remove();
  }
}
