/**
 * <drawzero-canvas>: marks a problem as a drawing problem.
 *
 *   <section class="problem">
 *     <h3 class="prob_name" data-problem="0020_Three_Lines">B: Three Lines</h3>
 *     <drawzero-canvas></drawzero-canvas>
 *     …
 *
 * The portal reads it and runs the problem's program on a canvas instead of
 * comparing its output. On a course page it draws nothing: the statement's own
 * pictures show what is wanted.
 */
export class DrawzeroCanvas extends HTMLElement {
  connectedCallback(): void {
    this.hidden = true;
  }
}

/**
 * <turtle-canvas>: the same for a problem whose program uses Python's `turtle`.
 * The portal runs it on a white canvas, where `import turtle` is drawzero's
 * browser turtle.
 */
export class TurtleCanvas extends HTMLElement {
  connectedCallback(): void {
    this.hidden = true;
  }
}

export function define(): void {
  if (!customElements.get("drawzero-canvas")) customElements.define("drawzero-canvas", DrawzeroCanvas);
  if (!customElements.get("turtle-canvas")) customElements.define("turtle-canvas", TurtleCanvas);
}
