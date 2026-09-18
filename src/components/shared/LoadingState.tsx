// design-reference/D-001/DESIGN.md "Loading·Empty·Error 상태": 로딩은 실제
// 콘텐츠 모양을 닮은 Skeleton(카드 실루엣·텍스트 바)으로 표시하고, 그 콘텐츠가
// 대체할 시간보다 길게 남아있지 않는다 — 빈 화면·스피너 단독 화면을 남기지 않는다.

export interface LoadingStateProps {
  /** 렌더링할 Skeleton Card 개수 */
  count?: number;
  className?: string;
}

export function LoadingState({ count = 3, className }: LoadingStateProps) {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-label="콘텐츠를 불러오는 중"
      className={`grid grid-cols-1 gap-4 md:grid-cols-3 ${className ?? ""}`}
    >
      {Array.from({ length: count }).map((_, index) => (
        <div
          key={index}
          aria-hidden
          className="animate-pulse overflow-hidden rounded-[length:var(--radius-md)] bg-[color:var(--color-surface-strong)]"
        >
          <div className="aspect-[4/3] bg-[color:var(--color-hairline)]" />
          <div className="flex flex-col gap-2 p-4">
            <div className="h-4 w-3/4 rounded-[length:var(--radius-sm)] bg-[color:var(--color-hairline)]" />
            <div className="h-3 w-1/2 rounded-[length:var(--radius-sm)] bg-[color:var(--color-hairline)]" />
          </div>
        </div>
      ))}
      <span className="sr-only">콘텐츠를 불러오는 중입니다.</span>
    </div>
  );
}

export default LoadingState;
