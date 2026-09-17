# UNIT-TRAVEL-DATES - 날짜 검증 유닛 테스트(출발/귀국, 체크인/체크아웃)

Category: Unit Test | Implementation Status: IMPLEMENT | Priority: P0

## Context

항공/숙소 날짜 검증 로직 유닛 테스트.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-013, REQ-FUNC-021)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-013, REQ-FUNC-021

## Screen / Route / Page Entry

Screen: SCR-003  
Route: `/travel-tools`  
Page Entry: -

## Design Ref

- `design-reference/D-001/DESIGN.md` - Do / Do Not 목록(금지 색상·금지 키워드 확인용). 이 Task는 화면을 직접 그리지 않는 비-UI Task다.

## Depends On

- COMP-SCR003-FLIGHT-FORM
- COMP-SCR003-HOTEL-FORM

## Expected Files

- `tests/unit/travel-dates.test.ts`

## Functional AC

날짜 검증은 경계값(오늘, 당일 체크인/체크아웃, 역전 날짜)을 포함한다. 연락처 탐지는 기준 테스트셋에서 탐지율/오탐률을 기록만 하고(정량 KPI는 축소) 정규식 케이스를 유닛으로 고정한다. 상태 전이는 중복 요청 차단·비작성자 승인 거부·자동 마감 포함.

## Visual AC

해당 없음.

## Security/Privacy AC

해당 없음.

## Test Cases

1. 출발일=오늘-1일 → 실패.
2. 체크아웃=체크인 → 실패.
3. 정상 범위 날짜 → 성공.

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
