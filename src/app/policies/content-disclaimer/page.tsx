// COMP-TECH-POLICY-PAGES: 콘텐츠 면책 안내 정적 페이지(REQ-FUNC-080).

export default function ContentDisclaimerPage() {
  return (
    <article className="mx-auto max-w-(--breakpoint-md) px-6 py-16">
      <h1 className="mb-6 text-[length:var(--text-display-lg)] font-[number:var(--font-weight-display-lg)] text-[color:var(--color-ink)]">
        콘텐츠 면책 안내
      </h1>
      <div className="flex flex-col gap-6 text-[length:var(--text-body-md)] leading-[var(--text-body-md--line-height)] text-[color:var(--color-body)]">
        <section>
          <h2 className="mb-2 text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]">
            여행지·안전정보의 성격
          </h2>
          <p>
            free_traveler가 제공하는 여행지 소개, 일정·예산 예시, 국가별
            안전정보는 작성 시점에 확인한 참고 정보이며, 실제 현지 상황·법규·
            치안 상태와 다를 수 있습니다. 각 안전정보 항목에는 출처와 최종
            확인일이 함께 표기되어 있으니 반드시 확인하세요.
          </p>
        </section>
        <section>
          <h2 className="mb-2 text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]">
            출국 전 재확인 의무
          </h2>
          <p>
            여행 계획을 확정하기 전에는 외교부 해외안전여행(0404.go.kr) 등 공식
            출처를 통해 최신 안전정보와 입국 요건을 반드시 재확인해야 합니다.
            free_traveler는 이 재확인 절차를 대체하지 않습니다.
          </p>
        </section>
        <section>
          <h2 className="mb-2 text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]">
            외부 파트너 사이트 이동
          </h2>
          <p>
            항공/숙소 조건 요약 후 이동하는 외부 사이트(Google Flights,
            Booking.com 등)는 free_traveler와 독립적으로 운영되며, 해당
            사이트에서 발생하는 가격·예약·결제 관련 사항은 각 사이트의 정책이
            적용됩니다.
          </p>
        </section>
        <section>
          <h2 className="mb-2 text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]">
            동행 모집글의 성격
          </h2>
          <p>
            동행 모집글은 회원이 직접 작성한 게시물이며, free_traveler는 그
            내용의 정확성을 보증하지 않습니다. 참가 전 상대방과 충분히 소통하고{" "}
            <a
              href="/policies/mate-safety"
              className="underline hover:text-[color:var(--color-ink)]"
            >
              동행 안전수칙
            </a>
            을 따라주세요.
          </p>
        </section>
        <p className="text-[length:var(--text-caption)] text-[color:var(--color-muted)]">
          시행일: 2026년 1월 5일
        </p>
      </div>
    </article>
  );
}
