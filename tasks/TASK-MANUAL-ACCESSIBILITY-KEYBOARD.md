# MANUAL-ACCESSIBILITY-KEYBOARD - 키보드 내비게이션·스크린리더 수동 점검

Category: Manual Check | Implementation Status: IMPLEMENT | Priority: P1

## Context

키보드 전용 내비게이션과 스크린리더 수동 점검.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-079, REQ-NF-023, REQ-NF-025)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-079, REQ-NF-023, REQ-NF-025

## Screen / Route / Page Entry

Screen: 전역  
Route: 전체  
Page Entry: -

## Design Ref

- `design-reference/D-001/DESIGN.md` - Do / Do Not 목록(금지 색상·금지 키워드 확인용). 이 Task는 화면을 직접 그리지 않는 비-UI Task다.

## Depends On

- COMP-GLOBAL-HEADER-FOOTER

## Expected Files

- 없음(체크리스트만
- `TASKS/checks/accessibility.md`)

## Functional AC

자동 CI 게이트가 없는 항목(REQ-NF-007/024 EXCLUDED)을 사람이 배포 후 직접 확인하고 결과를 `TASKS/checks/*.md`에 기록한다.

## Visual AC

SCR-001/SCR-003 Card Grid가 Desktop 3열/Mobile 1열로 전환되는지, 빈 여백이 과도하지 않은지 스크린샷으로 확인.

## Security/Privacy AC

해당 없음.

## Test Cases

1. Tab 키만으로 5개 Screen의 핵심 흐름을 완료할 수 있는지 확인.
2. 모든 인터랙티브 요소에서 포커스 표시가 보이는지 확인.

## Verify

없음(Manual Check 자체가 검증 수단)

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
