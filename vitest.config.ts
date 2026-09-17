import { defineConfig } from "vitest/config";

// Traveler 검증 규칙: Unit Test는 src 내부와 tests/unit만 대상으로 하고
// tests/e2e(Playwright 전용)는 절대 검색하지 않는다. Unit Test가 아직
// 없는 단계에서는 passWithNoTests로 성공 종료한다.
export default defineConfig({
  test: {
    environment: "node",
    include: [
      "src/**/*.{test,spec}.{ts,tsx}",
      "tests/unit/**/*.{test,spec}.{ts,tsx}",
    ],
    exclude: ["tests/e2e/**", "node_modules/**", ".next/**"],
    passWithNoTests: true,
  },
});
