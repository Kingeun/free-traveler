# E2E-TRAVEL-TOOLS - 항공·숙소 흐름 E2E

Category: E2E Test | Implementation Status: IMPLEMENT | Priority: P0

## Context

항공/숙소 조건 입력→요약→외부 이동 흐름 E2E. 입력값(REQ-FUNC-017, REQ-FUNC-025)은 어떤 단계에서도 서버로 전송하지 않는다/저장하지 않는다 - Network 탭에서 확인한다.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-011, REQ-FUNC-012, REQ-FUNC-013, REQ-FUNC-014, REQ-FUNC-015, REQ-FUNC-016, REQ-FUNC-017, REQ-FUNC-018, REQ-FUNC-019, REQ-FUNC-020, REQ-FUNC-021, REQ-FUNC-022, REQ-FUNC-023, REQ-FUNC-024, REQ-FUNC-025, REQ-FUNC-026, REQ-FUNC-054)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-011, REQ-FUNC-012, REQ-FUNC-013, REQ-FUNC-014, REQ-FUNC-015, REQ-FUNC-016, REQ-FUNC-017, REQ-FUNC-018, REQ-FUNC-019, REQ-FUNC-020, REQ-FUNC-021, REQ-FUNC-022, REQ-FUNC-023, REQ-FUNC-024, REQ-FUNC-025, REQ-FUNC-026, REQ-FUNC-054

## Screen / Route / Page Entry

Screen: SCR-003  
Route: `/travel-tools`  
Page Entry: -

## Design Ref

- `design-reference/D-001/DESIGN.md` - Do / Do Not 목록(금지 색상·금지 키워드 확인용). 이 Task는 화면을 직접 그리지 않는 비-UI Task다.

## Depends On

- PAGE-SCR003

## Expected Files

- `tests/e2e/travel-tools.spec.ts`

## Functional AC

`playwright.config.ts`는 `chromium` 프로젝트만 정의한다(firefox/webkit 프로젝트 없음). 3개 Task가 여행지 탐색, 안전정보 열람, 대표소개, 항공 이동, 숙소 이동, 동행 작성+로그인 유도, 참가 요청까지 핵심 5~7개 흐름을 커버한다.

## Visual AC

각 흐름에서 Lorem ipsum·준비 중·빈 Card가 렌더링되지 않는지 텍스트 스냅샷으로 확인.

## Security/Privacy AC

외부 이동 시 새 탭 URL에 목적지·날짜 쿼리가 없는지 확인(REQ-FUNC-016, REQ-FUNC-024).

## Test Cases

1. 항공 탭에서 조건 입력→요약 확인→외부 이동 새 탭 오픈 확인.
2. 숙소 탭에서 동일 흐름 확인.
3. 잘못된 날짜 입력 시 진행이 막히는지 확인.

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
