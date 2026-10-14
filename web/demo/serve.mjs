// A cross-origin isolated dev server for the demo and the browser tests.
//   node web/demo/serve.mjs [port]
// /s/…  is the course's s/ (Pyodide, boot.js), with drawzero's own build and wheel laid over it.
import { createServer } from "node:http";
import { createReadStream, existsSync, statSync } from "node:fs";
import { dirname, extname, join, normalize, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, "../..");
const course = resolve(process.env.CSTLF_DIR || join(root, "../cstlf"));
const port = Number(process.argv[2] || process.env.PORT || 8775);
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".mjs": "text/javascript", ".map": "application/json",
  ".json": "application/json", ".wasm": "application/wasm", ".zip": "application/zip", ".whl": "application/zip",
  ".svg": "image/svg+xml", ".toml": "text/plain; charset=utf-8", ".py": "text/plain; charset=utf-8", ".css": "text/css" };

function resolvePath(url) {
  const path = decodeURIComponent(new URL(url, "http://x").pathname);
  const routes = [
    ["/s/drawzero/", join(root, "web/dist")],
    ["/s/pyodide/wheels/drawzero-", join(root, "dist"), "drawzero-"],
    ["/s/", join(course, "s")],
    ["/examples/", join(root, "src/drawzero/examples")],
    ["/", here],
  ];
  for (const [prefix, dir, keep = ""] of routes) {
    if (path.startsWith(prefix)) {
      const rest = keep + path.slice(prefix.length);
      const file = normalize(join(dir, rest || "index.html"));
      if (!file.startsWith(dir)) return null;
      return file;
    }
  }
  return null;
}

createServer((req, res) => {
  let file = resolvePath(req.url);
  if (file && existsSync(file) && statSync(file).isDirectory()) file = join(file, "index.html");
  const headers = { "Cross-Origin-Opener-Policy": "same-origin", "Cross-Origin-Embedder-Policy": "require-corp",
    "Cross-Origin-Resource-Policy": "same-origin", "Cache-Control": "no-store" };
  if (!file || !existsSync(file)) { res.writeHead(404, headers); res.end("not found"); return; }
  res.writeHead(200, { ...headers, "Content-Type": TYPES[extname(file)] || "application/octet-stream" });
  createReadStream(file).pipe(res);
}).listen(port, "127.0.0.1", () => console.log(`drawzero demo on http://127.0.0.1:${port}/`));
