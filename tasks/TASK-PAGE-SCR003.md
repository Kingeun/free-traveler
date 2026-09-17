# PAGE-SCR003 - 통합 여행 준비 페이지 조립

Category: Page Owner | Implementation Status: IMPLEMENT | Priority: P0

## Context

SCR-003(`/travel-tools`)의 Page Owner Task. 항공/숙소/동행 구하기 3탭을 실제로 하나의 화면에 조립하고, 탭 전환 시 각 탭의 입력 상태가 독립적으로 보존되도록 상위 상태를 관리한다.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030

## Screen / Route / Page Entry

Screen: SCR-003  
Route: `/travel-tools`  
Page Entry: `src/app/travel-tools/page.tsx`

## Design Ref

- `design-reference/UI_CONTRACT.md` - SCR-003 절
- `design-reference/D-001/DESIGN.md` - Color Token / Typography / Spacing / Radius / Shadow, Do / Do Not 목록
- `design-reference/SCREEN_ROUTE_CONTRACT.json` - 해당 Screen 객체(section_order/key_components/forbidden_features)

## Depends On

- COMP-SCR003-INTRO-TABS-SHELL
- COMP-SCR003-FLIGHT-FORM
- COMP-SCR003-HOTEL-FORM
- COMP-SCR003-SUMMARY-ACTION
- COMP-SCR003-TIPS
- COMP-SCR003-MATE-WRITE-FORM
- COMP-SCR003-MATE-LOGIN-GATE
- COMP-GLOBAL-HEADER-FOOTER
- COMP-GLOBAL-TOAST
- COMP-GLOBAL-LOADING-STATE
- COMP-GLOBAL-ERROR-STATE

## Expected Files

- `src/app/travel-tools/page.tsx`(신규 생성)

## Functional AC

- Section 순서: ①Intro(3단계 안내) ②탭(항공편 찾기/숙소 찾기/동행 구하기) ③여행정보 Form ④입력 요약·외부 이동 ⑤찾기 Tip 3개 ⑥동행 작성 또는 로그인 안내·안전 안내.
- 3탭을 하나의 탭 컨테이너에 실제로 조립하고 탭 전환 시 다른 탭 입력 상태를 유지.
- 항공·숙소 입력값은 브라우저 상태로만 처리, 서버 API·DB·분석·외부 URL 쿼리 어디에도 전송하지 않음.
- 이 Task는 FlightForm/HotelForm/MateWriteForm 등 하위 Component를 새로 만들지 않고 Depends On의 결과물만 탭 컨테이너에 조립한다.

## Visual AC

- Lorem ipsum·준비 중·정보 확인 필요·빈 Card 금지.
- 동행 탭 비로그인 시 완성형 로그인 안내(설명+CTA)를 표시(빈 화면 금지).
- 로그인 상태 확인 중과 동행글 제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도)를 표시(항공·숙소 탭은 서버 호출이 없어 해당 없음).

## Security/Privacy AC

- 동행 작성은 로그인+성인 인증 필요(COMP-SCR003-MATE-LOGIN-GATE).
- 항공·호텔 입력값 비전송(REQ-FUNC-017, REQ-FUNC-025).
- 외부 링크는 `noopener,noreferrer`로 새 탭.

## Test Cases

1. 항공 탭에 값을 입력한 뒤 숙소 탭으로 전환하고 다시 항공 탭으로 돌아오면 입력값이 그대로 남아 있다.
2. 네트워크 탭을 확인했을 때 항공/숙소 폼 제출로 인한 서버 요청이 발생하지 않는다.
3. 비로그인 상태에서 동행 구하기 탭을 열면 작성 Form 대신 로그인 안내 카드가 보인다.

## Verify

E2E-TRAVEL-TOOLS, UNIT-TRAVEL-DATES, MANUAL-RESPONSIVE-DENSITY

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
- Depends On에 없는 하위 Component를 이 Task 안에서 직접 새로 만드는 것(조립만 허용).
