# DB-SCHEMA-BASE - 6개 테이블 스키마(profiles/mate_posts/mate_applications/user_blocks/reports/outbound_url_settings)

Category: Database | Implementation Status: IMPLEMENT | Priority: P0

## Context

6개 테이블(profiles, mate_posts, mate_applications, user_blocks, reports, outbound_url_settings) 스키마 마이그레이션.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-027, REQ-FUNC-028, REQ-FUNC-029, REQ-FUNC-031, REQ-FUNC-034, REQ-FUNC-037, REQ-FUNC-038, REQ-FUNC-039, REQ-FUNC-040, REQ-FUNC-041, REQ-FUNC-042, REQ-FUNC-077, REQ-FUNC-080)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-027, REQ-FUNC-028, REQ-FUNC-029, REQ-FUNC-031, REQ-FUNC-034, REQ-FUNC-037, REQ-FUNC-038, REQ-FUNC-039, REQ-FUNC-040, REQ-FUNC-041, REQ-FUNC-042, REQ-FUNC-077, REQ-FUNC-080

## Screen / Route / Page Entry

Screen: -  
Route: -  
Page Entry: -

## Design Ref

- `design-reference/D-001/DESIGN.md` - Do / Do Not 목록(금지 색상·금지 키워드 확인용). 이 Task는 화면을 직접 그리지 않는 비-UI Task다.

## Depends On

- 없음

## Expected Files

- `supabase/migrations/0001_schema_base.sql`

## Functional AC

테이블은 정확히 6개로 제한한다(여행지·안전·대표 콘텐츠는 DB에 넣지 않고 정적 데이터로 처리). `mate_posts`에 `safety_consent_at`(REQ-FUNC-080 동의 시각) 컬럼을 포함한다.

## Visual AC

해당 없음.

## Security/Privacy AC

6개 테이블 모두 RLS 활성화, 본인/요청 대상 작성자/Moderator·Admin만 비공개 행 열람. `DB-ACCESS`는 이메일·전화번호를 클라이언트 응답에서 select 단계부터 제외한다(REQ-FUNC-033). CSRF/SameSite·입력 검증은 Server Action 기본 보호+명시적 zod 스키마 검증으로 처리.

## Test Cases

1. 마이그레이션 적용 후 테이블이 정확히 6개다(추가 테이블 없음).
2. `mate_posts`에 `safety_consent_at` 컬럼이 있다.

## Verify

TEST-RLS-BASIC

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
- 정의된 6개 테이블(profiles/mate_posts/mate_applications/user_blocks/reports/outbound_url_settings) 외의 테이블을 추가하거나, RLS를 비활성화한 채 테이블을 남기는 것.
