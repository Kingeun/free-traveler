"use client";

// COMP-TECH-ERROR-PAGES: 런타임/500 오류는 최소 1개의 복구 행동(다시 시도)을
// 제공한다(REQ-FUNC-078). Next.js App Router의 error.tsx는 반드시 Client
// Component여야 하며 reset()으로 해당 경로 세그먼트를 다시 렌더링한다.

export default function Error({ reset }: { error: Error; reset: () => void }) {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 px-6 text-center">
      <h1 className="text-[length:var(--text-display-md)] font-[number:var(--font-weight-display-md)] text-[color:var(--color-ink)]">
        문제가 발생했습니다
      </h1>
      <p className="text-[length:var(--text-body-md)] text-[color:var(--color-body)]">
        잠시 후 다시 시도해 주세요. 문제가 계속되면 홈으로 돌아가 다시 시작해
        주세요.
      </p>
      <button
        type="button"
        onClick={reset}
        className="inline-flex items-center justify-center rounded-[length:var(--radius-sm)] bg-[color:var(--color-primary)] px-6 py-2 text-[length:var(--text-button)] font-[number:var(--font-weight-button)] text-[color:var(--color-on-primary)] transition hover:bg-[color:var(--color-primary-active)]"
      >
        다시 시도
      </button>
    </div>
  );
}
