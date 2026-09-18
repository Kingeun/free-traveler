// COMP-TECH-POLICY-PAGES: 동행 안전수칙 정적 페이지(REQ-FUNC-080). 동행 모집글
// 작성 Form의 동의 체크박스가 이 페이지를 링크한다.

const SAFETY_RULES = [
  "처음 만나는 동행 상대와는 공개된 장소에서 만나고, 첫 만남 일정을 지인에게 미리 공유하세요.",
  "실명·주민등록번호·계좌번호 등 민감한 개인정보는 채팅으로 공유하지 마세요.",
  "출발 전 결제를 요구하거나 선입금을 유도하는 상대는 즉시 신고하세요.",
  "여행 일정 중 위치 공유 앱 등을 활용해 안전 상태를 주기적으로 확인하세요.",
  "불편하거나 위협적인 언행을 겪으면 즉시 대화를 종료하고 차단·신고 기능을 사용하세요.",
  "동행 상대의 신원(본인인증 완료 여부, 매너온도)을 신청 전에 확인하세요.",
];

export default function MateSafetyPage() {
  return (
    <article className="mx-auto max-w-(--breakpoint-md) px-6 py-16">
      <h1 className="mb-6 text-[length:var(--text-display-lg)] font-[number:var(--font-weight-display-lg)] text-[color:var(--color-ink)]">
        동행 안전수칙
      </h1>
      <p className="mb-6 text-[length:var(--text-body-md)] leading-[var(--text-body-md--line-height)] text-[color:var(--color-body)]">
        동행 모집글을 작성하거나 참가를 신청하기 전에 아래 안전수칙을 반드시
        읽고 동의해 주세요. free_traveler는 회원 간 만남을 중개할 뿐, 실제
        만남과 여행에서 발생하는 일에 대해 책임지지 않습니다.
      </p>
      <ol className="flex flex-col gap-4">
        {SAFETY_RULES.map((rule, index) => (
          <li
            key={rule}
            className="flex gap-3 text-[length:var(--text-body-md)] leading-[var(--text-body-md--line-height)] text-[color:var(--color-body)]"
          >
            <span className="font-[number:var(--font-weight-title-md)] text-[color:var(--color-primary)]">
              {index + 1}
            </span>
            <span>{rule}</span>
          </li>
        ))}
      </ol>
      <p className="mt-6 text-[length:var(--text-caption)] text-[color:var(--color-muted)]">
        시행일: 2026년 1월 5일
      </p>
    </article>
  );
}
