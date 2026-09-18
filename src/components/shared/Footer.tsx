import Link from "next/link";

// design-reference/D-001/DESIGN.md "Header · Footer": Desktop 3컬럼(서비스/정책/
// 문의), Mobile 1컬럼. 하단에 저작권 표시 + 표준 면책 문구.

const SERVICE_LINKS = [
  { label: "여행지", href: "/" },
  { label: "여행 도구", href: "/travel-tools" },
  { label: "동행", href: "/mates" },
  { label: "대표소개", href: "/about" },
] as const;

const POLICY_LINKS = [
  { label: "이용약관", href: "/policies/terms" },
  { label: "개인정보처리방침", href: "/policies/privacy" },
  { label: "동행 안전수칙", href: "/policies/mate-safety" },
  { label: "콘텐츠 면책 안내", href: "/policies/content-disclaimer" },
] as const;

export function Footer() {
  return (
    <footer className="border-t border-[color:var(--color-hairline)] bg-[color:var(--color-canvas)]">
      <div className="mx-auto grid max-w-(--breakpoint-2xl) grid-cols-1 gap-8 px-6 py-12 md:grid-cols-3">
        <div>
          <h2 className="mb-4 text-[length:var(--text-caption)] font-[number:var(--font-weight-caption)] text-[color:var(--color-muted)]">
            서비스
          </h2>
          <ul className="flex flex-col gap-2">
            {SERVICE_LINKS.map((link) => (
              <li key={link.href}>
                <Link
                  href={link.href}
                  className="text-[length:var(--text-body-sm)] text-[color:var(--color-body)] hover:text-[color:var(--color-ink)]"
                >
                  {link.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h2 className="mb-4 text-[length:var(--text-caption)] font-[number:var(--font-weight-caption)] text-[color:var(--color-muted)]">
            정책
          </h2>
          <ul className="flex flex-col gap-2">
            {POLICY_LINKS.map((link) => (
              <li key={link.href}>
                <Link
                  href={link.href}
                  className="text-[length:var(--text-body-sm)] text-[color:var(--color-body)] hover:text-[color:var(--color-ink)]"
                >
                  {link.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h2 className="mb-4 text-[length:var(--text-caption)] font-[number:var(--font-weight-caption)] text-[color:var(--color-muted)]">
            문의
          </h2>
          <p className="text-[length:var(--text-body-sm)] text-[color:var(--color-body)]">
            이메일:{" "}
            <a
              href="mailto:contact@free-traveler.example.com"
              className="hover:text-[color:var(--color-ink)]"
            >
              contact@free-traveler.example.com
            </a>
          </p>
          <p className="text-[length:var(--text-body-sm)] text-[color:var(--color-body)]">
            인스타그램:{" "}
            <a
              href="https://instagram.com/free_traveler.example"
              className="hover:text-[color:var(--color-ink)]"
            >
              @free_traveler.example
            </a>
          </p>
        </div>
      </div>

      <div className="border-t border-[color:var(--color-hairline)] px-6 py-6">
        <p className="text-[length:var(--text-caption)] text-[color:var(--color-muted)]">
          © {new Date().getFullYear()} free_traveler. 안전정보 등 콘텐츠는
          참고용이며 출국 전 공식 출처 재확인이 필요합니다.
        </p>
      </div>
    </footer>
  );
}

export default Footer;
