// COMP-TECH-POLICY-PAGES: 개인정보처리방침 정적 페이지(REQ-FUNC-080).

export default function PrivacyPage() {
  return (
    <article className="mx-auto max-w-(--breakpoint-md) px-6 py-16">
      <h1 className="mb-6 text-[length:var(--text-display-lg)] font-[number:var(--font-weight-display-lg)] text-[color:var(--color-ink)]">
        개인정보처리방침
      </h1>
      <div className="flex flex-col gap-6 text-[length:var(--text-body-md)] leading-[var(--text-body-md--line-height)] text-[color:var(--color-body)]">
        <section>
          <h2 className="mb-2 text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]">
            1. 수집하는 개인정보 항목
          </h2>
          <p>
            free_traveler는 회원가입 시 이메일과 비밀번호(암호화 저장)를, 프로필
            설정 시 닉네임과 성인 인증 여부를 수집합니다. 동행 모집글 작성·신청
            시 입력한 제목·기간·참가 메시지가 함께 저장됩니다. 항공/숙소 조건
            입력값(국가·지역·날짜)은 서버로 전송되거나 저장되지 않고 브라우저
            내에서만 사용됩니다.
          </p>
        </section>
        <section>
          <h2 className="mb-2 text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]">
            2. 개인정보의 이용 목적
          </h2>
          <p>
            수집된 정보는 회원 인증, 동행 모집글·참가 신청 처리, 신고·차단 기능
            운영, 서비스 부정이용 방지 목적으로만 사용됩니다.
          </p>
        </section>
        <section>
          <h2 className="mb-2 text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]">
            3. 개인정보의 보관 및 파기
          </h2>
          <p>
            회원 탈퇴 시 관련 개인정보는 지체 없이 파기합니다. 다만 신고 처리
            이력 등 법령상 보관이 필요한 정보는 관련 법령이 정한 기간 동안 보관
            후 파기합니다.
          </p>
        </section>
        <section>
          <h2 className="mb-2 text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]">
            4. 제3자 제공 및 위탁
          </h2>
          <p>
            free_traveler는 개인정보를 외부에 판매하거나 마케팅 목적으로
            제공하지 않습니다. 인증·데이터 저장을 위해 Supabase를 이용하며, 이는
            서비스 제공을 위한 필수 위탁 처리입니다.
          </p>
        </section>
        <section>
          <h2 className="mb-2 text-[length:var(--text-title-md)] font-[number:var(--font-weight-title-md)] text-[color:var(--color-ink)]">
            5. 이용자의 권리
          </h2>
          <p>
            이용자는 언제든지 자신의 개인정보를 열람·수정·삭제할 수 있으며, 계정
            설정 화면에서 직접 처리하거나 문의를 통해 요청할 수 있습니다.
          </p>
        </section>
        <p className="text-[length:var(--text-caption)] text-[color:var(--color-muted)]">
          시행일: 2026년 1월 5일
        </p>
      </div>
    </article>
  );
}
