import { defineConfig, devices } from "@playwright/test";

// CLAUDE.md 규칙 18 / PLAYWRIGHT_SCOPE=chromium-smoke: Chromium 프로젝트
// 하나만 정의한다. firefox/webkit 프로젝트는 추가하지 않는다.
//
// baseURL은 기본적으로 로컬 개발 서버(127.0.0.1:3000)를 가리키며,
// PLAYWRIGHT_BASE_URL이 설정되면 그 값(Preview URL 등)으로 덮어쓴다.
// 그 경우 이미 배포된 서버를 대상으로 하는 것이므로 webServer(npm run dev)는
// 띄우지 않는다.
const baseURL = process.env.PLAYWRIGHT_BASE_URL || "http://127.0.0.1:3000";
const usingRemoteBaseURL = Boolean(process.env.PLAYWRIGHT_BASE_URL);

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  retries: process.env.CI ? 1 : 0,
  reporter: [
    ["list"],
    ["html", { outputFolder: "playwright-report", open: "never" }],
  ],
  use: {
    baseURL,
    screenshot: "only-on-failure",
    trace: "on-first-retry",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  webServer: usingRemoteBaseURL
    ? undefined
    : {
        command: "npm run dev",
        url: baseURL,
        reuseExistingServer: !process.env.CI,
        timeout: 120_000,
      },
});
