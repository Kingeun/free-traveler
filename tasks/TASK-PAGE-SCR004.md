# PAGE-SCR004 - 동행 조회 페이지 조립

Category: Page Owner | Implementation Status: IMPLEMENT | Priority: P0

## Context

SCR-004(`/mates`)의 Page Owner Task. Filter/목록/상세/참가/신고/차단 6개 Component를 조립해 목록形+상세 분할(Desktop) 또는 목록→Drawer(Mobile) 레이아웃을 완성한다.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030

## Screen / Route / Page Entry

Screen: SCR-004  
Route: `/mates`  
Page Entry: `src/app/mates/page.tsx`

## Design Ref

- `design-reference/UI_CONTRACT.md` - SCR-004 절
- `design-reference/D-001/DESIGN.md` - Color Token / Typography / Spacing / Radius / Shadow, Do / Do Not 목록
- `design-reference/SCREEN_ROUTE_CONTRACT.json` - 해당 Screen 객체(section_order/key_components/forbidden_features)

## Depends On

- COMP-SCR004-FILTER-BAR
- COMP-SCR004-POST-LIST
- COMP-SCR004-DETAIL-PANEL
- COMP-SCR004-APPLY-FORM
- COMP-SCR004-REPORT-ACTION
- COMP-SCR004-BLOCK-ACTION
- COMP-GLOBAL-HEADER-FOOTER
- COMP-GLOBAL-EMPTY-STATE
- COMP-GLOBAL-LOADING-STATE
- COMP-GLOBAL-ERROR-STATE
- API-MATE-POSTS

## Expected Files

- `src/app/mates/page.tsx`(신규 생성)

## Functional AC

- Section 순서: ①Intro+작성 CTA ②Filter·결과 요약 ③동행 목록(최대 8개 우선 노출) ④상세(Desktop 좌우 분할/Mobile 상세 Drawer, 작성자·게시글 대상 신고·차단 버튼 포함) ⑤신청 방법 3단계 ⑥동행 안전수칙 요약 안내.
- 목록·필터·상세·참가·신고·차단을 각각 별도 Component Task로 조립(단일 컴포넌트로 합치지 않음), 신고·차단은 상세에서 열람 중인 특정 게시글·작성자를 대상으로 동작한다.
- 이 Task는 하위 Component를 새로 만들지 않고 Depends On의 결과물만 페이지에 배치한다.

## Visual AC

- 검색 결과 0건 시 필터 초기화+작성 CTA+이용 방법을 갖춘 완성형 Empty State.
- Lorem ipsum·준비 중·정보 확인 필요·빈 Card 금지.
- 목록·상세 조회 중과 참가·신고·차단 제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도)를 표시.

## Security/Privacy AC

- 참가 요청·신고·차단은 로그인 필요.
- RLS로 본인 글/요청만 비공개 데이터 열람(DB-RLS-BASE).

## Test Cases

1. 조건에 맞는 글이 없을 때 필터 초기화 버튼과 작성 CTA가 있는 Empty State가 보인다.
2. Desktop 1440px에서는 좌측 목록+우측 상세 패널이 동시에 보이고, Mobile 390px에서는 상세가 Drawer로 열린다.
3. 차단한 사용자의 글이 목록에 나타나지 않는다.

## Verify

E2E-MATE-AUTH, TEST-RLS-BASIC, MANUAL-RESPONSIVE-DENSITY

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
