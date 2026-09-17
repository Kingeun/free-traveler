# COMP-SCR005-PROFILE - Member — 프로필·성인 확인 요약

Category: Component | Implementation Status: IMPLEMENT | Priority: P0

## Context

Member 프로필(닉네임/연령대/여행 스타일/자기소개)과 성인 확인 상태 요약.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-029)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-029

## Screen / Route / Page Entry

Screen: SCR-005  
Route: `/account`  
Page Entry: `src/app/account/page.tsx`

## Design Ref

- `design-reference/UI_CONTRACT.md` - SCR-005 절
- `design-reference/D-001/DESIGN.md` - Color Token / Typography / Spacing / Radius / Shadow, Do / Do Not 목록

## Depends On

- COMP-SCR005-AUTH
- API-AUTH-PROFILE
- COMP-GLOBAL-LOADING-STATE
- COMP-GLOBAL-ERROR-STATE

## Expected Files

- `src/components/account/Profile.tsx`

## Functional AC

Guest/Member/Admin 4영역(Auth/Profile/My Activity/Admin)을 파일 단위로 분리한다. Admin 컴포넌트는 Admin 역할이 아니면 import된 채로도 렌더링되지 않는다(조건부 렌더링, 코드 존재 자체는 금지 아님).

## Visual AC

My Activity의 각 목록(내 글/참가요청/차단/즐겨찾기) 0건 시 완성형 Empty State. Supabase 조회/제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도 포함)를 표시한다(AUTH/PROFILE/MY-ACTIVITY/ADMIN-REPORTS/ADMIN-URL-SETTINGS 전부). Lorem ipsum·빈 Card 금지.

## Security/Privacy AC

성인 인증은 `is_adult`/`adult_verified_at`만 저장하고 생년월일 원본은 저장하지 않는다(REQ-FUNC-028). Admin 컴포넌트는 서버 측 역할 검증과 함께 사용(클라이언트 조건부 렌더링만으로 신뢰하지 않음).

## Test Cases

1. 닉네임/연령대/여행 스타일은 필수, 성별은 선택 입력이다.
2. 성인 확인 상태가 배지로 표시된다.

## Verify

E2E-MATE-AUTH, TEST-RLS-BASIC

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
