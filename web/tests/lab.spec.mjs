// The live contract, in a real browser with the real Pyodide and wheel.
import { expect, test } from "@playwright/test";

async function open(page) {
  await page.goto("/");
  await page.evaluate(() => window.ready);
  expect(await page.evaluate(() => crossOriginIsolated)).toBe(true);
}

const run = (page, code, stdin = "") => page.evaluate(([c, s]) => lab.run(c, s), [code, stdin]);
/** Start a run without waiting for its end. */
const start = (page, code) => page.evaluate((c) => { window.running = lab.run(c); }, code);
const until = (page, fn, arg) => page.waitForFunction(fn, arg, { timeout: 20_000 });
const shapes = (page) => page.evaluate(() => [...lab.scene.svg.querySelectorAll("g:not([data-sprites]) > *")].map((e) => {
  const a = {};
  for (const at of e.attributes) a[at.name] = at.value;
  return { tag: e.tagName, text: e.textContent, ...a };
}));

test("a static picture is drawn with pygame's geometry", async ({ page }) => {
  await open(page);
  const r = await run(page, `from drawzero import *
line('red', (100, 100), (900, 900))
circle('yellow', (500, 500), 200, line_width=20)
filled_rect((0, 128, 255, 128), (300, 300), 400, 200)
rect('green', (10, 20), 100, 50)
arc('white', (100, 100), 200, 100, 0, 90, line_width=10)
text('white', 'Hello!', (500, 120), 64, '.^')
`);
  expect(r.status).toBe("ok");
  const s = await shapes(page);
  expect(s.map((e) => e.tag)).toEqual(["line", "circle", "rect", "rect", "path", "text"]);
  expect(s[0]).toMatchObject({ x1: "100", y1: "100", x2: "900", y2: "900", stroke: "rgb(255,0,0)", "stroke-width": "4" });
  // the border lies inside the circle: centre line at r - w/2
  expect(s[1]).toMatchObject({ r: "190", fill: "none", stroke: "rgb(255,255,0)", "stroke-width": "20" });
  expect(s[2]).toMatchObject({ x: "300", y: "300", width: "400", height: "200", fill: "rgb(0,128,255)", opacity: "0.502" });
  expect(s[3]).toMatchObject({ x: "12", y: "22", width: "96", height: "46", "stroke-width": "4" });
  expect(s[4].d).toBe("M295 150A95 45 0 0 0 200 105");
  expect(s[5]).toMatchObject({ text: "Hello!", "text-anchor": "middle", "dominant-baseline": "text-before-edge", "font-size": "44" });
});

test("input comes from stdin and print goes to the output", async ({ page }) => {
  await open(page);
  const out = [];
  await page.exposeFunction("collect", (t) => out.push(t));
  await page.evaluate(() => lab.on("output", (t) => window.collect(t)));
  const r = await run(page, "from drawzero import *\nn = int(input())\nprint(n * 2)\nfor i in range(n):\n    circle('red', (100 * i, 100), 10)\n", "3\n");
  expect(r.status).toBe("ok");
  expect(out.join("")).toBe("6\n");
  expect((await shapes(page)).length).toBe(3);
});

test("tick keeps pygame's pace", async ({ page }) => {
  await open(page);
  const r = await run(page, "from drawzero import *\nfor i in range(30):\n    clear()\n    circle('red', (i * 30, 500), 20)\n    tick()\n");
  expect(r.status).toBe("ok");
  expect(r.frames).toBeGreaterThanOrEqual(30);
  expect(r.ms).toBeGreaterThan(900);
  expect(r.ms).toBeLessThan(2500);
  const s = await shapes(page);
  expect(s.length).toBe(1);
  expect(s[0].cx).toBe("870");
});

test("Stop ends an endless animation and an endless computation", async ({ page }) => {
  await open(page);
  await start(page, "from drawzero import *\ni = 0\nwhile True:\n    clear()\n    circle('red', (i % 1000, 500), 20)\n    i += 7\n    tick()\n");
  await until(page, () => lab.frames > 5);
  await page.evaluate(() => lab.stop());
  expect((await page.evaluate(() => window.running)).status).toBe("stopped");
  await start(page, "while True:\n    pass\n");
  await page.waitForTimeout(300);
  await page.evaluate(() => lab.stop());
  expect((await page.evaluate(() => window.running)).status).toBe("stopped");
  // the worker is still usable
  expect((await run(page, "from drawzero import *\nline('red', (0, 0), (10, 10))\n")).status).toBe("ok");
});

test("the keyboard and the mouse reach the program", async ({ page }) => {
  await open(page);
  await start(page, `from drawzero import *
x, y, clicks = 500, 500, 0
while True:
    x += 10 * keyboard.axis('left', 'right')
    if mouse.just_pressed('left'):
        clicks += 1
        y = mouse.pos[1]
    clear()
    filled_circle('red', (x, y), 20)
    text('white', f'{clicks} {keyboard.typed!r}', (0, 0), 24, '<^')
    tick()
`);
  await until(page, () => lab.frames > 2);
  await page.locator("svg").focus();
  await page.keyboard.down("ArrowRight");
  await page.waitForTimeout(500);
  await page.keyboard.up("ArrowRight");
  await page.keyboard.type("hi");
  const box = await page.locator("svg").boundingBox();
  await page.mouse.click(box.x + box.width / 2, box.y + box.height * 0.25);
  await page.waitForTimeout(300);
  const s = await shapes(page);
  await page.evaluate(() => lab.stop());
  const circle = s.find((e) => e.tag === "circle");
  expect(Number(circle.cx)).toBeGreaterThan(560);
  expect(Math.abs(Number(circle.cy) - 250)).toBeLessThan(3);
  expect(s.find((e) => e.tag === "text").text).toMatch(/^1 /);
});

test("an error keeps what was drawn and names the line", async ({ page }) => {
  await open(page);
  const r = await run(page, "from drawzero import *\nline('red', (0, 0), (10, 10))\ncircle('reddish', (5, 5), 3)\n");
  expect(r.status).toBe("error");
  expect(r.error.line).toBe(3);
  expect(r.error.traceback).toContain("reddish");
  expect((await shapes(page)).map((e) => e.tag)).toEqual(["line"]);
});

test("a drawing that never clears stays quick", async ({ page }) => {
  await open(page);
  const r = await run(page, "from drawzero import *\nfor i in range(20000):\n    line((i % 256, 0, 0), (i % 1000, 0), (0, i % 1000), line_width=1)\n");
  expect(r.status).toBe("ok");
  await page.waitForTimeout(1500);
  expect(await page.evaluate(() => lab.scene.elementCount)).toBeLessThan(8000);
  expect(await page.evaluate(() => lab.scene.svg.querySelector("g > image") !== null)).toBe(true);
});

test("a new run starts on a black canvas", async ({ page }) => {
  await open(page);
  await run(page, "from drawzero import *\nfill('white')\ncircle('red', (5, 5), 3)\n");
  await run(page, "from drawzero import *\nline('red', (0, 0), (10, 10))\n");
  expect((await shapes(page)).map((e) => e.tag)).toEqual(["line"]);
  expect(await page.evaluate(() => lab.scene.svg.firstElementChild.getAttribute("fill"))).toBe("rgb(0,0,0)");
});

test("import turtle draws with the browser turtle", async ({ page }) => {
  await open(page);
  const r = await run(page, `import turtle
t = turtle.Turtle()
t.speed(0)
t.color('red', 'yellow')
t.begin_fill()
for _ in range(4):
    t.forward(200)
    t.left(90)
t.end_fill()
t.write('square', font=('Arial', 16, 'normal'))
turtle.done()
`);
  expect(r.status).toBe("ok");
  const s = await shapes(page);
  expect(s.filter((e) => e.tag === "polyline").length).toBe(8); // four sides, then again over the fill
  expect(s.find((e) => e.tag === "polygon")).toMatchObject({ fill: "rgb(255,255,0)" });
  expect(s.find((e) => e.tag === "polyline")).toMatchObject({ points: "500 500 750 500", "stroke-linecap": "round" });
  expect(s.find((e) => e.tag === "text")).toMatchObject({ text: "square", "font-weight": "normal" });
  expect(await page.evaluate(() => lab.scene.svg.querySelector("rect").getAttribute("fill"))).toBe("rgb(255,255,255)");
  // the turtle itself, over the picture
  expect(await page.evaluate(() => lab.scene.svg.querySelectorAll("[data-sprites] > *").length)).toBe(2);
});

test("a slow turtle animates and Stop ends it", async ({ page }) => {
  await open(page);
  await start(page, "import turtle\nturtle.speed(1)\nwhile True:\n    turtle.forward(300)\n    turtle.left(170)\n");
  await until(page, () => lab.frames > 20);
  const pieces = await page.evaluate(() => lab.scene.svg.querySelectorAll("polyline").length);
  expect(pieces).toBeGreaterThan(5);
  await page.evaluate(() => lab.stop());
  expect((await page.evaluate(() => window.running)).status).toBe("stopped");
});

test("a turtle fractal with tracer(0) is drawn at once", async ({ page }) => {
  await open(page);
  const t0 = Date.now();
  const r = await run(page, `import turtle
turtle.tracer(0)
turtle.hideturtle()
def dragon(n, size, sign=1):
    if n == 0:
        turtle.forward(size)
        return
    dragon(n - 1, size / 2 ** 0.5, 1)
    turtle.left(90 * sign)
    dragon(n - 1, size / 2 ** 0.5, -1)
dragon(12, 300)
turtle.update()
turtle.mainloop()
`);
  expect(r.status).toBe("ok");
  expect(Date.now() - t0).toBeLessThan(15_000);
  expect(await page.evaluate(() => lab.scene.elementCount)).toBeGreaterThan(0);
});
