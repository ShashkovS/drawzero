// Build the browser bundle: dist/drawzero-web.js (page) and dist/worker.js (Pyodide).
// node web/build.mjs [--dev] [--course ../cstlf]  also publishes them (and the wheel) into the course's s/.
import { build } from "esbuild";
import { copyFileSync, mkdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const web = dirname(fileURLToPath(import.meta.url));
const root = resolve(web, "..");
const version = /__version__ = '([^']+)'/.exec(readFileSync(join(root, "src/drawzero/__about__.py"), "utf8"))[1];

const common = {
  bundle: true, format: "esm", target: "es2022", minify: !process.argv.includes("--dev"), sourcemap: true,
  define: { __DRAWZERO_VERSION__: JSON.stringify(version) }, logLevel: "info",
};
await build({ ...common, entryPoints: [join(web, "src/index.ts")], outfile: join(web, "dist/drawzero-web.js") });
await build({ ...common, entryPoints: [join(web, "src/worker.ts")], outfile: join(web, "dist/worker.js") });
writeFileSync(join(web, "dist/VERSION"), version + "\n");

const i = process.argv.indexOf("--course");
if (i > 0) {
  const course = resolve(process.argv[i + 1]);
  const wheel = join(root, "dist", `drawzero-${version}-py3-none-any.whl`);
  if (!existsSync(wheel)) throw new Error(`build the wheel first: uv build --wheel (missing ${wheel})`);
  const out = join(course, "s/drawzero");
  mkdirSync(out, { recursive: true });
  for (const f of ["drawzero-web.js", "drawzero-web.js.map", "worker.js", "worker.js.map", "VERSION"]) copyFileSync(join(web, "dist", f), join(out, f));
  copyFileSync(wheel, join(course, "s/pyodide/wheels", `drawzero-${version}-py3-none-any.whl`));
  console.log(`published drawzero ${version} into ${course}/s`);
}
