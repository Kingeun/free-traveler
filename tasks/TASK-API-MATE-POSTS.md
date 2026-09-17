# API-MATE-POSTS - 동행 모집글 CRUD+자동 마감

Category: API | Implementation Status: IMPLEMENT | Priority: P0

## Context

동행 모집글 CRUD와 조회 시점 자동 마감 계산.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-030, REQ-FUNC-031, REQ-FUNC-037, REQ-FUNC-038, REQ-NF-005)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-030, REQ-FUNC-031, REQ-FUNC-037, REQ-FUNC-038, REQ-NF-005

## Screen / Route / Page Entry

Screen: SCR-003, SCR-004  
Route: `/travel-tools`, `/mates`  
Page Entry: -

## Design Ref

- `design-reference/D-001/DESIGN.md` - Do / Do Not 목록(금지 색상·금지 키워드 확인용). 이 Task는 화면을 직접 그리지 않는 비-UI Task다.

## Depends On

- DB-ACCESS

## Expected Files

- `src/lib/actions/mate-posts.ts`

## Functional AC

모든 쓰기는 Supabase Server Action을 통해서만 수행하고 클라이언트에서 직접 테이블을 쓰지 않는다. `API-MATE-POSTS`의 자동 마감은 별도 배치 없이 조회 시점에 `end_date` 경과 여부를 계산해 표시한다(REQ-FUNC-037).

## Visual AC

해당 없음(서버 계층).

## Security/Privacy AC

`API-ADMIN-SETTINGS`는 HTTPS·허용목록 도메인만 저장하고 `http:`/`javascript:`/`data:` URL을 거부한다(REQ-FUNC-077). `API-AUTH-PROFILE`은 생년월일 원본을 저장하지 않는다(REQ-FUNC-028).

## Test Cases

1. 종료일이 지난 글을 조회하면 status가 CLOSED로 계산되어 반환된다.
2. 비인증 사용자의 작성 요청은 401/리다이렉트로 거부된다.

## Verify

TEST-RLS-BASIC, UNIT-MATE-STATE, E2E-MATE-AUTH

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
