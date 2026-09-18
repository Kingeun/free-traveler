import type { Config } from "tailwindcss";

// D-001 DESIGN.md 토큰은 이 프로젝트의 Tailwind v4 정본에서는 src/app/globals.css의
// `@theme` 블록에 CSS 커스텀 프로퍼티로 정의된다(v4는 CSS-first 테마를 우선한다).
// 이 파일은 소스 스캔 경로와 다크 모드 전략만 선언한다 — DESIGN.md는 다크 모드가
// 없다고 명시하므로(Visual Theme: "There is no dark mode") false로 고정한다.
const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  darkMode: false,
};

export default config;
