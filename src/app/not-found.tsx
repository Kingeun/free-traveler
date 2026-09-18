import Link from "next/link";

// COMP-TECH-ERROR-PAGES: 404는 최소 1개의 복구 행동(홈 이동)을 제공한다
// (REQ-FUNC-078, design-reference/SCREEN_ROUTE_CONTRACT.json technical_routes).

export default function NotFound() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 px-6 text-center">
      <h1 className="text-[length:var(--text-display-md)] font-[number:var(--font-weight-display-md)] text-[color:var(--color-ink)]">
        페이지를 찾을 수 없습니다
      </h1>
      <p className="text-[length:var(--text-body-md)] text-[color:var(--color-body)]">
        요청하신 주소가 삭제되었거나 잘못 입력되었을 수 있습니다.
      </p>
      <Link
        href="/"
        className="inline-flex items-center justify-center rounded-[length:var(--radius-sm)] bg-[color:var(--color-primary)] px-6 py-2 text-[length:var(--text-button)] font-[number:var(--font-weight-button)] text-[color:var(--color-on-primary)] transition hover:bg-[color:var(--color-primary-active)]"
      >
        홈으로 이동
      </Link>
    </div>
  );
}
