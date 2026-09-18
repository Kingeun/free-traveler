// design-reference/D-001/DESIGN.md "Loading·Empty·Error 상태": 오류는 인라인,
// 사람이 읽을 수 있는 한국어 메시지 + 재시도 버튼(의미 있을 때만)을 갖춘 완성형
// 블록으로 표시한다. 원시 에러 코드나 영어 스택 트레이스는 노출하지 않는다.

export interface ErrorStateProps {
  message: string;
  onRetry?: () => void;
  retryLabel?: string;
  className?: string;
}

export function ErrorState({
  message,
  onRetry,
  retryLabel = "다시 시도",
  className,
}: ErrorStateProps) {
  return (
    <div
      role="alert"
      className={`flex flex-col items-center gap-4 rounded-[length:var(--radius-md)] bg-[color:var(--color-surface-soft)] px-6 py-8 text-center ${className ?? ""}`}
    >
      <p className="text-[length:var(--text-body-md)] leading-[var(--text-body-md--line-height)] text-[color:var(--color-danger)]">
        {message}
      </p>

      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="inline-flex items-center justify-center rounded-[length:var(--radius-sm)] bg-[color:var(--color-primary)] px-6 py-2 text-[length:var(--text-button)] leading-[var(--text-button--line-height)] font-[number:var(--font-weight-button)] text-[color:var(--color-on-primary)] transition hover:bg-[color:var(--color-primary-active)]"
        >
          {retryLabel}
        </button>
      )}
    </div>
  );
}

export default ErrorState;
