# E2E-PUBLIC-SMOKE - 공개 흐름 Smoke(여행지 탐색·안전정보·대표소개)

Category: E2E Test | Implementation Status: IMPLEMENT | Priority: P0

## Context

여행지 탐색, 안전정보 열람, 대표소개 등 비로그인 공개 흐름 Smoke Test.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-001, REQ-FUNC-002, REQ-FUNC-003, REQ-FUNC-005, REQ-FUNC-006, REQ-FUNC-009, REQ-FUNC-047, REQ-FUNC-050, REQ-FUNC-051, REQ-FUNC-057, REQ-FUNC-059, REQ-FUNC-060, REQ-FUNC-063, REQ-NF-023, REQ-NF-025, REQ-NF-030)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-001, REQ-FUNC-002, REQ-FUNC-003, REQ-FUNC-005, REQ-FUNC-006, REQ-FUNC-009, REQ-FUNC-047, REQ-FUNC-050, REQ-FUNC-051, REQ-FUNC-057, REQ-FUNC-059, REQ-FUNC-060, REQ-FUNC-063, REQ-NF-023, REQ-NF-025, REQ-NF-030

## Screen / Route / Page Entry

Screen: SCR-001, SCR-002  
Route: `/`, `/about`  
Page Entry: -

## Design Ref

- `design-reference/D-001/DESIGN.md` - Do / Do Not 목록(금지 색상·금지 키워드 확인용). 이 Task는 화면을 직접 그리지 않는 비-UI Task다.

## Depends On

- PAGE-SCR001
- PAGE-SCR002

## Expected Files

- `tests/e2e/public-smoke.spec.ts`

## Functional AC

`playwright.config.ts`는 `chromium` 프로젝트만 정의한다(firefox/webkit 프로젝트 없음). 3개 Task가 여행지 탐색, 안전정보 열람, 대표소개, 항공 이동, 숙소 이동, 동행 작성+로그인 유도, 참가 요청까지 핵심 5~7개 흐름을 커버한다.

## Visual AC

각 흐름에서 Lorem ipsum·준비 중·빈 Card가 렌더링되지 않는지 텍스트 스냅샷으로 확인.

## Security/Privacy AC

외부 이동 시 새 탭 URL에 목적지·날짜 쿼리가 없는지 확인(REQ-FUNC-016, REQ-FUNC-024).

## Test Cases

1. `/` 접속 → 국내/해외 Card 클릭 → 상세 Drawer 열림.
2. 안전정보 Card 클릭 → Drawer 열림 → 외교부 링크 새 탭.
3. `/about` 접속 → 7개 Section 모두 렌더링 확인.

## Verify

CI-QUALITY-GATE

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
- `playwright.config.ts`에 chromium 이외의 브라우저 프로젝트(firefox/webkit)를 추가하는 것.
