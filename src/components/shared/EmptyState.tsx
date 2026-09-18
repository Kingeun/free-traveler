import type { ReactNode } from "react";

// design-reference/D-001/DESIGN.md "완성형 Empty State와 Placeholder 문구 금지 규칙":
// 아이콘 + 한 문장 설명 + 짧은 이용 방법(2~3단계) + 명확한 CTA 버튼 1개, 이 4요소가
// 모두 있어야 "완성형"으로 인정한다. 이 4요소 중 하나라도 비어 있으면 개발 중에만
// console.warn으로 알리고, 화면에는 placeholder 문구를 절대 노출하지 않는다.

export interface EmptyStateStep {
  label: string;
}

export interface EmptyStateCta {
  label: string;
  href?: string;
  onClick?: () => void;
}

export interface EmptyStateProps {
  icon: ReactNode;
  description: string;
  steps: EmptyStateStep[];
  cta: EmptyStateCta;
  className?: string;
}

export function EmptyState({
  icon,
  description,
  steps,
  cta,
  className,
}: EmptyStateProps) {
  if (
    process.env.NODE_ENV !== "production" &&
    (!icon || !description || steps.length === 0 || !cta?.label)
  ) {
    console.warn(
      "EmptyState: icon/description/steps/cta 네 요소가 모두 있어야 완성형 Empty State로 인정됩니다 (D-001 참고).",
    );
  }

  const ctaClassName =
    "inline-flex items-center justify-center rounded-[length:var(--radius-sm)] bg-[color:var(--color-primary)] px-6 py-2 text-[length:var(--text-button)] leading-[var(--text-button--line-height)] font-[number:var(--font-weight-button)] text-[color:var(--color-on-primary)] transition hover:bg-[color:var(--color-primary-active)]";

  return (
    <div
      className={`flex flex-col items-center gap-4 rounded-[length:var(--radius-md)] bg-[color:var(--color-surface-soft)] px-6 py-8 text-center ${className ?? ""}`}
    >
      <div aria-hidden className="text-[color:var(--color-muted)]">
        {icon}
      </div>

      <p className="text-[length:var(--text-body-md)] leading-[var(--text-body-md--line-height)] font-[number:var(--font-weight-body-md)] text-[color:var(--color-ink)]">
        {description}
      </p>

      {steps.length > 0 && (
        <ol className="flex flex-col gap-1 text-left">
          {steps.map((step, index) => (
            <li
              key={step.label}
              className="text-[length:var(--text-body-sm)] leading-[var(--text-body-sm--line-height)] text-[color:var(--color-body)]"
            >
              {index + 1}. {step.label}
            </li>
          ))}
        </ol>
      )}

      {cta.href ? (
        <a href={cta.href} className={ctaClassName}>
          {cta.label}
        </a>
      ) : (
        <button type="button" onClick={cta.onClick} className={ctaClassName}>
          {cta.label}
        </button>
      )}
    </div>
  );
}

export default EmptyState;
