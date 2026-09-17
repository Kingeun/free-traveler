# COMP-SCR001-THEME-CHIPS - 여행 동기 6개 Chip

Category: Component | Implementation Status: IMPLEMENT | Priority: P1

## Context

여행 동기·테마 6개를 Chip으로 표시하고 선택 시 목록 필터와 URL query를 동기화한다.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-002, REQ-FUNC-010)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-002, REQ-FUNC-010

## Screen / Route / Page Entry

Screen: SCR-001  
Route: `/`  
Page Entry: `src/app/page.tsx`

## Design Ref

- `design-reference/UI_CONTRACT.md` - SCR-001 절
- `design-reference/D-001/DESIGN.md` - Color Token / Typography / Spacing / Radius / Shadow, Do / Do Not 목록

## Depends On

- COMP-SCR001-DOMESTIC-GRID
- COMP-SCR001-OVERSEAS-GRID

## Expected Files

- `src/components/home/ThemeChips.tsx`

## Functional AC

각 Component는 지정된 구현 방법을 따른다 — 여행지/안전/대표 콘텐츠는 `DATA-*` 정적 데이터만 읽고 DB를 호출하지 않는다(REQ-FUNC-008/046/052 데이터 계층 검증은 DATA-VALIDATION-SCRIPT 담당). 즐겨찾기는 localStorage(`favorites` key, JSON 배열)만 사용한다. API-MATE-POSTS를 호출하는 MATES-TEASER는 COMP-GLOBAL-LOADING-STATE/COMP-GLOBAL-ERROR-STATE로 로딩·오류 상태를 표시한다(나머지 Component는 정적 데이터만 사용하므로 해당 없음).

## Visual AC

Card는 사진 우선(`radius.md`), 국내/해외 Grid는 배경 톤 또는 배지로 시각적으로 구분한다(동일 레이아웃 반복 금지). 빈 Card·Lorem ipsum·준비 중 금지.

## Security/Privacy AC

전부 Public 컴포넌트, 인증 불필요. 안전정보 배지는 텍스트+아이콘 병기(색상 단독 금지).

## Test Cases

1. Chip 선택 시 국내/해외 Grid가 해당 테마로 필터링된다.
2. 필터 적용 후 새로고침해도 동일한 Chip이 선택된 상태로 복원된다.

## Verify

E2E-PUBLIC-SMOKE

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
