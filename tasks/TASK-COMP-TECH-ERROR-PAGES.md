# COMP-TECH-ERROR-PAGES - 404/500 복구 화면

Category: Technical Route | Implementation Status: IMPLEMENT | Priority: P1

## Context

404/500 오류 화면.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-078)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-078

## Screen / Route / Page Entry

Screen: 기술 Route  
Route: `not-found` / `error`  
Page Entry: `src/app/not-found.tsx`, `src/app/error.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` - Color Token / Typography / Spacing / Radius / Shadow, Do / Do Not 목록

## Depends On

- COMP-GLOBAL-DESIGN-TOKENS

## Expected Files

- `src/app/not-found.tsx`
- `src/app/error.tsx`

## Functional AC

404/500 화면은 각각 홈으로 이동·다시 시도 중 최소 1개 복구 행동을 제공한다. 정책 페이지는 정적 콘텐츠이며 COMP-SCR003-MATE-WRITE-FORM의 동의 체크박스가 이 페이지를 링크한다.

## Visual AC

Lorem ipsum·준비 중 금지, 실제 정책 문구를 채운다.

## Security/Privacy AC

해당 없음.

## Test Cases

1. 존재하지 않는 경로 접속 시 404 화면과 홈 이동 버튼이 보인다.
2. 런타임 오류 발생 시 500 화면과 다시 시도 버튼이 보인다.

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
