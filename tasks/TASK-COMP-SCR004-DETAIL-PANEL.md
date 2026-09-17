# COMP-SCR004-DETAIL-PANEL - 상세(Desktop 분할/Mobile Drawer)

Category: Component | Implementation Status: IMPLEMENT | Priority: P0

## Context

선택한 동행글의 상세 정보. Desktop은 목록 옆 패널, Mobile은 Drawer로 표시한다.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-036, REQ-FUNC-038, REQ-FUNC-044, REQ-FUNC-069)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-036, REQ-FUNC-038, REQ-FUNC-044, REQ-FUNC-069

## Screen / Route / Page Entry

Screen: SCR-004  
Route: `/mates`  
Page Entry: `src/app/mates/page.tsx`

## Design Ref

- `design-reference/UI_CONTRACT.md` - SCR-004 절
- `design-reference/D-001/DESIGN.md` - Color Token / Typography / Spacing / Radius / Shadow, Do / Do Not 목록

## Depends On

- COMP-SCR004-POST-LIST
- API-MATE-POSTS
- DB-RLS-BASE
- COMP-GLOBAL-LOADING-STATE
- COMP-GLOBAL-ERROR-STATE

## Expected Files

- `src/components/mates/DetailPanel.tsx`

## Functional AC

목록·필터·상세·참가·신고·차단을 각각 독립 컴포넌트/파일로 유지한다(단일 컴포넌트로 합치지 않음). 신고·차단은 상세에서 열람 중인 특정 게시글·작성자를 대상으로 동작하며(COMP-SCR004-DETAIL-PANEL 의존), 대상 없이 독립적으로 호출되지 않는다. 차단된 상대의 글은 목록·상세에서 제외한다.

## Visual AC

검색 결과 0건은 COMP-GLOBAL-EMPTY-STATE(필터 초기화+작성 CTA+이용 방법)로 표시. Supabase 조회/제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도 포함)를 표시한다(POST-LIST/DETAIL-PANEL/APPLY-FORM/REPORT-ACTION/BLOCK-ACTION). Lorem ipsum·빈 Card 금지.

## Security/Privacy AC

참가 요청 내용은 작성자·요청자만 열람(RLS). 신고·차단은 로그인 필요. 응답/렌더링에 이메일·전화번호 노출 금지(REQ-FUNC-033).

## Test Cases

1. 작성자 본인에게만 수정/마감/삭제 버튼이 보인다.
2. 비공개 데이터는 RLS로 본인/작성자만 조회된다.

## Verify

E2E-MATE-AUTH, TEST-RLS-BASIC, UNIT-MATE-STATE

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
