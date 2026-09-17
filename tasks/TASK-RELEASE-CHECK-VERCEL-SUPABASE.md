# RELEASE-CHECK-VERCEL-SUPABASE - Vercel 배포+Supabase 환경변수/TLS/비용 확인

Category: CI/Infra | Implementation Status: IMPLEMENT | Priority: P1

## Context

Vercel 배포와 Supabase 환경변수/TLS/비용 확인 체크리스트.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-NF-012, REQ-NF-016, REQ-NF-034)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-NF-012, REQ-NF-016, REQ-NF-034

## Screen / Route / Page Entry

Screen: 전역  
Route: 전체  
Page Entry: -

## Design Ref

- `design-reference/D-001/DESIGN.md` - Do / Do Not 목록(금지 색상·금지 키워드 확인용). 이 Task는 화면을 직접 그리지 않는 비-UI Task다.

## Depends On

- DB-SCHEMA-BASE
- DB-RLS-BASE

## Expected Files

- `TASKS/checks/release-vercel-supabase.md`

## Functional AC

CI는 `tsc --noEmit`, `eslint`, `playwright test --project=chromium`을 병합 전 필수로 실행한다. EC2·AWS 인프라, 자동 Merge Runner는 만들지 않는다.

## Visual AC

해당 없음.

## Security/Privacy AC

비밀키는 Vercel/GitHub Actions 환경변수로만 관리하고 클라이언트 번들에 포함되지 않는지 빌드 산출물로 확인. HTTPS(TLS 1.2+)는 Vercel 기본값 확인.

## Test Cases

1. 배포 URL이 HTTPS인지 확인.
2. 비밀키가 클라이언트 번들에 노출되지 않았는지 빌드 산출물에서 확인.
3. 월 예상 비용이 목표(10만원 이하) 범위인지 확인.

## Verify

CI 실행 로그

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
