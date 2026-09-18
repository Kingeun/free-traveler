// COMP-TECH-POLICY-PAGES: 이용약관 정적 페이지(REQ-FUNC-080). 실제 정책 문구를
// 채운다 — Lorem ipsum/준비 중 금지(design-reference/D-001/DESIGN.md Do Not).

export default function TermsPage() {
  return (
    <article className="mx-auto max-w-(--breakpoint-md) px-6 py-16">
      <h1 className="mb-6 text-[length:var(--text-display-lg)] font-[number:var(--font-weight-display-lg)] text-[color:var(--color-ink)]">
        이용약관
      </h1>
      <div className="flex flex-col gap-6 text-[length:var(--text-body-md)] leading-[var(--text-body-md--line-height)] text-[color:var(--color-body)]">
        <section>
          <h2 className="mb-2 text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]">
            제1조 (목적)
          </h2>
          <p>
            이 약관은 free_traveler(이하 &quot;서비스&quot;)가 제공하는
            여행지·안전정보 열람, 항공/숙소 외부 이동 안내, 동행 모집글
            게시·신청 기능의 이용과 관련하여 서비스와 이용자 간의 권리·의무 및
            책임 사항을 규정합니다.
          </p>
        </section>
        <section>
          <h2 className="mb-2 text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]">
            제2조 (서비스의 범위)
          </h2>
          <p>
            서비스는 정적으로 관리되는 여행지·대표 소개·안전정보 콘텐츠 열람,
            항공/숙소 조건 입력 후 외부 파트너 사이트로의 이동 안내, 회원 간
            동행 모집글 작성·조회·참가 신청 기능을 제공합니다. 서비스는 항공권·
            숙소 예약이나 결제를 직접 처리하지 않으며, 모든 예약은 이동한 외부
            사이트에서 이루어집니다.
          </p>
        </section>
        <section>
          <h2 className="mb-2 text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]">
            제3조 (회원의 의무)
          </h2>
          <p>
            회원은 동행 모집글 작성 시 실제와 다른 정보를 게시하지 않아야 하며,
            다른 이용자를 대상으로 한 사기·괴롭힘·차별적 언행을 금지합니다.
            서비스는 신고된 게시물에 대해 관리자 검토 후 숨김 처리할 수
            있습니다.
          </p>
        </section>
        <section>
          <h2 className="mb-2 text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]">
            제4조 (콘텐츠 면책)
          </h2>
          <p>
            안전정보·여행지 정보는 참고용이며, 실제 현지 상황과 다를 수
            있습니다. 출국 전 반드시 외교부 등 공식 출처를 통해 최신 정보를
            재확인해야 합니다. 자세한 내용은{" "}
            <a
              href="/policies/content-disclaimer"
              className="underline hover:text-[color:var(--color-ink)]"
            >
              콘텐츠 면책 안내
            </a>
            를 참고하십시오.
          </p>
        </section>
        <section>
          <h2 className="mb-2 text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]">
            제5조 (약관의 변경)
          </h2>
          <p>
            서비스는 필요한 경우 이 약관을 변경할 수 있으며, 변경된 약관은 이
            페이지에 게시함으로써 효력이 발생합니다.
          </p>
        </section>
        <p className="text-[length:var(--text-caption)] text-[color:var(--color-muted)]">
          시행일: 2026년 1월 5일
        </p>
      </div>
    </article>
  );
}
