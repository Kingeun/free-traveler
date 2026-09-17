# TEST-RLS-BASIC - RLS 정책 기본 접근 테스트

Category: Integration Test | Implementation Status: IMPLEMENT | Priority: P0

## Context

6개 테이블에 대한 RLS 통합 테스트. 실제 Supabase(로컬 또는 테스트 프로젝트)에 대해 실행한다.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-044, REQ-NF-013)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-044, REQ-NF-013

## Screen / Route / Page Entry

Screen: SCR-004, SCR-005  
Route: `/mates`, `/account`  
Page Entry: -

## Design Ref

- `design-reference/D-001/DESIGN.md` - Do / Do Not 목록(금지 색상·금지 키워드 확인용). 이 Task는 화면을 직접 그리지 않는 비-UI Task다.

## Depends On

- DB-RLS-BASE
- DB-SEED-BASE

## Expected Files

- `tests/integration/rls-basic.test.ts`

## Functional AC

본인/타인/Moderator/Admin 4개 역할 조합으로 각 테이블 select/insert/update를 시도해 허용·거부가 설계대로 동작하는지 확인.

## Visual AC

해당 없음.

## Security/Privacy AC

비인가 접근이 전부 403 또는 빈 결과인지 확인.

## Test Cases

1. 본인 데이터 조회 → 성공.
2. 타인 비공개 데이터 조회 → 빈 결과/403.
3. Admin 계정의 신고 테이블 조회 → 성공.

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
