# COMP-SCR003-SUMMARY-ACTION - 입력 요약+외부 이동 Action Card

Category: Component | Implementation Status: IMPLEMENT | Priority: P0

## Context

항공/숙소 입력 요약과 외부 사이트 이동 Action Card. 비전달 고지 문구를 포함한다.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-014, REQ-FUNC-016, REQ-FUNC-018, REQ-FUNC-022, REQ-FUNC-024, REQ-FUNC-026, REQ-FUNC-054)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-014, REQ-FUNC-016, REQ-FUNC-018, REQ-FUNC-022, REQ-FUNC-024, REQ-FUNC-026, REQ-FUNC-054

## Screen / Route / Page Entry

Screen: SCR-003  
Route: `/travel-tools`  
Page Entry: `src/app/travel-tools/page.tsx`

## Design Ref

- `design-reference/UI_CONTRACT.md` - SCR-003 절
- `design-reference/D-001/DESIGN.md` - Color Token / Typography / Spacing / Radius / Shadow, Do / Do Not 목록

## Depends On

- COMP-SCR003-FLIGHT-FORM
- COMP-SCR003-HOTEL-FORM

## Expected Files

- `src/components/travel-tools/SummaryAction.tsx`

## Functional AC

항공·숙소·동행 작성 세 영역은 서로 다른 파일/컴포넌트로 분리하고, 세 영역의 입력·검증·완료 상태는 서로 독립적으로 유지한다(탭 전환 시 값 보존은 IntroTabsShell이 상위 상태로 관리).

## Visual AC

각 Form은 라벨+도움말+오류 영역을 갖추고 Lorem ipsum·준비 중 금지. MATE-LOGIN-GATE(인증 상태 확인)와 MATE-WRITE-FORM(제출)은 COMP-GLOBAL-LOADING-STATE/COMP-GLOBAL-ERROR-STATE를 사용하고, FLIGHT-FORM/HOTEL-FORM/SUMMARY-ACTION/TIPS/INTRO-TABS-SHELL은 서버 호출이 없어 해당 없음.

## Security/Privacy AC

FLIGHT-FORM/HOTEL-FORM은 입력값을 `useState` 등 브라우저 상태로만 유지하고 서버 API·URL 쿼리로 전송하지 않는다(REQ-FUNC-017, REQ-FUNC-025). MATE-WRITE-FORM은 제출 전 정규식으로 전화번호·이메일·메신저 ID 패턴을 탐지해 차단한다(REQ-FUNC-032, UNIT-CONTACT-DETECTION 연동).

## Test Cases

1. 요약 값이 입력 Form의 값과 정확히 일치한다.
2. 이동 버튼 클릭 시 새 탭이 `noopener,noreferrer`로 열리고 URL에 목적지/날짜 쿼리가 없다.
3. 외부 URL이 설정되지 않았거나 허용목록 밖이면 이동이 차단되고 재시도 안내가 보인다.

## Verify

E2E-TRAVEL-TOOLS, E2E-MATE-AUTH, UNIT-TRAVEL-DATES

## Definition of Done

- 위 Functional AC / Visual AC / Security-Privacy AC 항목을 모두 만족한다.
- Verify에 명시된 Task/Check가 통과한다.
- Expected Files 목록에 있는 파일만 생성·수정했다(그 외 파일 변경 없음).
- Forbidden 목록에 해당하는 요소가 결과물에 없다.
- Requirement Ref가 있는 경우 `docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적 가능하다.

## Forbidden

- Expected Files 목록 밖의 파일을 생성·수정·삭제하는 것.
- Lorem ipsum, "준비 중", "정보 확인 필요" 등 placeholder 문구, 또는 내용 없는 빈 Card를 남기는 것.
- 별점(★)·리뷰 점수 UI, 실시간 항공/숙소 가격, 광고 배너를 추가하는 것.
- Airbnb 상표 요소(Rausch 색상명, Cereal 폰트, "Guest favorite" 배지, 3-Product Nav 등)를 재현하는 것.
- 자동 Merge Runner, EC2/AWS 인프라 Task로 이 Task의 범위를 확장하는 것.
- 이 문서에 명시되지 않은 새 DB 테이블·새 Screen·새 Route를 추가하는 것.
- 외부 이동 URL에 목적지·날짜 등 사용자 입력값을 쿼리 파라미터로 포함하는 것.
