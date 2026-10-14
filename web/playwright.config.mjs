import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  timeout: 90_000,
  workers: 1,
  use: { baseURL: "http://127.0.0.1:8776", headless: true },
  webServer: { command: "node demo/serve.mjs 8776", url: "http://127.0.0.1:8776/", reuseExistingServer: true },
});
