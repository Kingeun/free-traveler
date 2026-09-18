"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

// design-reference/D-001/DESIGN.md "Header · Footer": Desktop 72px/Mobile 56px,
// wordmark(→ /) · center nav 4개(현재 페이지는 코랄 밑줄/굵게) · 우측 로그인 영역.
// Supabase Auth는 아직 이 Wave에 없어 로그인 영역은 로그아웃 상태만 표시한다
// (COMP-SCR005-AUTH가 실제 인증 상태 연동을 담당).

const NAV_LINKS = [
  { label: "여행지", href: "/" },
  { label: "여행 도구", href: "/travel-tools" },
  { label: "동행", href: "/mates" },
  { label: "대표소개", href: "/about" },
] as const;

export function Header() {
  const pathname = usePathname();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="border-b border-[color:var(--color-hairline)] bg-[color:var(--color-canvas)]">
      <div className="mx-auto flex h-14 max-w-(--breakpoint-2xl) items-center justify-between px-6 md:h-[72px]">
        <Link
          href="/"
          className="text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]"
        >
          Free Traveler
        </Link>

        <nav
          aria-label="주요 내비게이션"
          className="hidden items-center gap-6 md:flex"
        >
          {NAV_LINKS.map((link) => {
            const isActive =
              link.href === "/"
                ? pathname === "/"
                : pathname.startsWith(link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                aria-current={isActive ? "page" : undefined}
                className={
                  isActive
                    ? "text-[length:var(--text-body-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)] underline decoration-[color:var(--color-primary)] decoration-2 underline-offset-8"
                    : "text-[length:var(--text-body-md)] text-[color:var(--color-body)] hover:text-[color:var(--color-ink)]"
                }
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        <div className="hidden md:block">
          <Link
            href="/account"
            className="text-[length:var(--text-body-md)] font-[number:var(--font-weight-button)] text-[color:var(--color-ink)]"
          >
            로그인
          </Link>
        </div>

        <button
          type="button"
          aria-label="메뉴 열기"
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((open) => !open)}
          className="flex h-11 w-11 items-center justify-center md:hidden"
        >
          <span aria-hidden>☰</span>
        </button>
      </div>

      {menuOpen && (
        <nav
          aria-label="모바일 내비게이션"
          className="flex flex-col gap-4 border-t border-[color:var(--color-hairline)] px-6 py-4 md:hidden"
        >
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMenuOpen(false)}
              className="text-[length:var(--text-body-md)] text-[color:var(--color-ink)]"
            >
              {link.label}
            </Link>
          ))}
          <Link
            href="/account"
            onClick={() => setMenuOpen(false)}
            className="text-[length:var(--text-body-md)] font-[number:var(--font-weight-button)] text-[color:var(--color-ink)]"
          >
            로그인
          </Link>
        </nav>
      )}
    </header>
  );
}

export default Header;
