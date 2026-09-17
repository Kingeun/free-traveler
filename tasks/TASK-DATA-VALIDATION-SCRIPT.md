# DATA-VALIDATION-SCRIPT - 게시 기준 수량·완전성 빌드 타임 검증

Category: Data | Implementation Status: IMPLEMENT | Priority: P0

## Context

빌드 전 콘텐츠 수량·완전성을 검사하는 스크립트. DATA-DESTINATIONS/SAFETY/REPRESENTATIVE 3개 데이터 소스를 모두 검사한다.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-008, REQ-FUNC-046, REQ-FUNC-052, REQ-FUNC-074, REQ-NF-026, REQ-NF-027)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-008, REQ-FUNC-046, REQ-FUNC-052, REQ-FUNC-074, REQ-NF-026, REQ-NF-027

## Screen / Route / Page Entry

Screen: -  
Route: -  
Page Entry: -

## Design Ref

- `design-reference/D-001/DESIGN.md` - Do / Do Not 목록(금지 색상·금지 키워드 확인용). 이 Task는 화면을 직접 그리지 않는 비-UI Task다.

## Depends On

- DATA-DESTINATIONS
- DATA-SAFETY
- DATA-REPRESENTATIVE

## Expected Files

- `scripts/validate-content.ts`

## Functional AC

지정된 구현 방법 = 정적 데이터(TypeScript 배열/객체, DB 미사용). `DATA-DESTINATIONS`는 국내 10개 이상·해외 15개국 30개 도시 이상을 포함하고 소개·명소 5개 이상·1일/3일 일정·예산·교통·음식 3개 이상·에티켓·출처·수정일 필드를 강제하는 TypeScript 타입을 가진다. `DATA-SAFETY`는 치안/사기/법규/교통/재난/보건/문화/긴급연락처 8개 카테고리와 출처·확인일·편집자 필드를 강제한다. `DATA-VALIDATION-SCRIPT`는 `npm run build` 전(또는 별도 `npm run validate:content`)에 수량·필수 필드 누락을 검사해 실패 시 빌드를 중단한다.

## Visual AC

해당 없음(데이터 계층).

## Security/Privacy AC

이미지 URL은 일반 인터넷 URL만 사용, 업로드 저장소 없음.

## Test Cases

1. 기준 미달(예: 국내 9개) 데이터로 실행하면 스크립트가 실패(non-zero exit)한다.
2. 기준을 만족하는 데이터로 실행하면 성공한다.

## Verify

DATA-VALIDATION-SCRIPT 자체 실행(CI-QUALITY-GATE에 포함)

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
- 정적 데이터를 DB 테이블로 옮기거나, DATA-VALIDATION-SCRIPT의 최소 수량 기준을 낮추는 것.
