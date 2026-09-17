# DB-ACCESS - 타입 안전 쿼리/서버 액션 헬퍼

Category: Database | Implementation Status: IMPLEMENT | Priority: P0

## Context

타입 안전 Supabase 쿼리/서버 액션 헬퍼. 이메일·전화번호를 응답에서 제외한다. 항공·숙소 입력값(REQ-FUNC-017)은 이 모듈의 어떤 함수도 받지 않으며 DB에 저장하지 않는다 - 전송하지 않는다/저장하지 않는다.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-017, REQ-FUNC-033, REQ-NF-014, REQ-NF-015, REQ-NF-017)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-017, REQ-FUNC-033, REQ-NF-014, REQ-NF-015, REQ-NF-017

## Screen / Route / Page Entry

Screen: -  
Route: -  
Page Entry: -

## Design Ref

- `design-reference/D-001/DESIGN.md` - Do / Do Not 목록(금지 색상·금지 키워드 확인용). 이 Task는 화면을 직접 그리지 않는 비-UI Task다.

## Depends On

- DB-SCHEMA-BASE
- DB-RLS-BASE

## Expected Files

- `src/lib/supabase/queries.ts`
- `src/lib/supabase/client.ts`

## Functional AC

테이블은 정확히 6개로 제한한다(여행지·안전·대표 콘텐츠는 DB에 넣지 않고 정적 데이터로 처리). `mate_posts`에 `safety_consent_at`(REQ-FUNC-080 동의 시각) 컬럼을 포함한다.

## Visual AC

해당 없음.

## Security/Privacy AC

6개 테이블 모두 RLS 활성화, 본인/요청 대상 작성자/Moderator·Admin만 비공개 행 열람. `DB-ACCESS`는 이메일·전화번호를 클라이언트 응답에서 select 단계부터 제외한다(REQ-FUNC-033). CSRF/SameSite·입력 검증은 Server Action 기본 보호+명시적 zod 스키마 검증으로 처리.

## Test Cases

1. 동행글 목록 조회 응답에 이메일/전화번호 필드가 전혀 포함되지 않는다.
2. 항공/숙소 폼에서 호출되는 쿼리 함수가 없다(해당 폼은 이 모듈을 사용하지 않음).

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
