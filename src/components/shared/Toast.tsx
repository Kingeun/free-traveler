"use client";

import {
  createContext,
  useCallback,
  useContext,
  useRef,
  useState,
  type ReactNode,
} from "react";

// REQ-FUNC-043(축소): 참가 요청/승인/거절/신고 처리 결과는 인앱 Toast로만
// 알린다 — 서버 저장이나 실제 이메일 발송은 하지 않고 클라이언트 상태로만
// 동작한다(design-reference/D-001/DESIGN.md "Alert · Toast").

export type ToastVariant = "success" | "error" | "info";

interface ToastItem {
  id: number;
  message: string;
  variant: ToastVariant;
}

interface ToastContextValue {
  showToast: (message: string, variant?: ToastVariant) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

const AUTO_DISMISS_MS = 3000;

function variantClassName(variant: ToastVariant) {
  const base =
    "flex items-center gap-2 rounded-[length:var(--radius-sm)] px-4 py-2 text-[length:var(--text-body-sm)] text-[color:var(--color-on-primary)] shadow-[var(--shadow-card-hover)]";
  if (variant === "success") return `${base} bg-[color:var(--color-success)]`;
  if (variant === "error") return `${base} bg-[color:var(--color-danger)]`;
  return `${base} bg-[color:var(--color-ink)]`;
}

function variantIcon(variant: ToastVariant) {
  if (variant === "success") return "✓";
  if (variant === "error") return "!";
  return "ℹ";
}

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<ToastItem[]>([]);
  const nextId = useRef(0);

  const showToast = useCallback(
    (message: string, variant: ToastVariant = "info") => {
      const id = nextId.current++;
      setToasts((prev) => [...prev, { id, message, variant }]);
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
      }, AUTO_DISMISS_MS);
    },
    [],
  );

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <div
        aria-live="polite"
        className="fixed inset-x-0 bottom-6 z-50 flex flex-col items-center gap-2 px-4 md:inset-x-auto md:right-6 md:items-end"
      >
        {toasts.map((toast) => (
          <div
            key={toast.id}
            role="status"
            className={variantClassName(toast.variant)}
          >
            <span aria-hidden>{variantIcon(toast.variant)}</span>
            <span>{toast.message}</span>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) {
    throw new Error("useToast는 ToastProvider 내부에서만 사용할 수 있습니다.");
  }
  return ctx;
}

export default ToastProvider;
