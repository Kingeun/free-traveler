# PAGE-SCR005 - 계정·관리 페이지 조립

Category: Page Owner | Implementation Status: IMPLEMENT | Priority: P0

## Context

SCR-005(`/account`)의 Page Owner Task. 로그인 상태와 역할(Guest/Member/Admin)에 따라 5개 Component 중 해당하는 것만 조건부로 렌더링한다.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030

## Screen / Route / Page Entry

Screen: SCR-005  
Route: `/account`  
Page Entry: `src/app/account/page.tsx`

## Design Ref

- `design-reference/UI_CONTRACT.md` - SCR-005 절
- `design-reference/D-001/DESIGN.md` - Color Token / Typography / Spacing / Radius / Shadow, Do / Do Not 목록
- `design-reference/SCREEN_ROUTE_CONTRACT.json` - 해당 Screen 객체(section_order/key_components/forbidden_features)

## Depends On

- COMP-SCR005-AUTH
- COMP-SCR005-PROFILE
- COMP-SCR005-MY-ACTIVITY
- COMP-SCR005-ADMIN-REPORTS
- COMP-SCR005-ADMIN-URL-SETTINGS
- COMP-GLOBAL-HEADER-FOOTER
- COMP-GLOBAL-EMPTY-STATE
- COMP-GLOBAL-LOADING-STATE
- COMP-GLOBAL-ERROR-STATE
- API-AUTH-PROFILE

## Expected Files

- `src/app/account/page.tsx`(신규 생성)

## Functional AC

- Section(역할별 영역) 순서 - Guest: 계정 Intro → 로그인/가입/비밀번호 재설정 Card → 로그인 후 가능한 기능 안내 → 보안 안내. Member: 프로필·성인 확인 요약 → 내 글 → 참가 요청 → 차단 목록 → 즐겨찾기 목록 → 새 동행글 작성 CTA. Admin: 관리 Intro → 신고 상태 변경(+대상 글 숨김) → 항공·숙소 외부 URL 설정.
- 현재 역할(Guest/Member/Admin)의 Intro→핵심 작업→도움말/다음 행동을 실제로 조건부 렌더링.
- 역할에 없는 관리 영역(예: Member의 Admin 탭)은 렌더링 자체를 하지 않음.
- Dashboard·통계형 화면을 만들지 않음.
- 이 Task는 Auth/Profile/MyActivity/AdminReports/AdminUrlSettings Component를 새로 만들지 않고 역할별 조건부 조립만 한다.

## Visual AC

- 내 글/참가 요청/차단/즐겨찾기/신고 큐가 0건일 때 각각 완성형 Empty State(설명+이용 방법+다음 행동 CTA).
- Lorem ipsum·준비 중·정보 확인 필요·빈 Card 금지.
- 인증·프로필·활동 내역·관리자 데이터 조회·제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도)를 표시.

## Security/Privacy AC

- Guest는 Member/Admin 탭에 접근 불가(탭 자체 미노출).
- Admin 범위는 신고 상태 변경·외부 URL 설정으로 한정(콘텐츠 CRUD·감사 로그 없음).

## Test Cases

1. Guest로 접속하면 로그인/가입 폼만 보이고 Profile·My Activity·Admin 탭은 DOM에 존재하지 않는다.
2. Member로 로그인하면 Admin 탭이 보이지 않는다.
3. Admin으로 로그인하면 신고 큐와 외부 URL 설정만 보이고 콘텐츠 CRUD·통계 화면은 없다.

## Verify

E2E-MATE-AUTH, TEST-RLS-BASIC, MANUAL-RESPONSIVE-DENSITY

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
- Depends On에 없는 하위 Component를 이 Task 안에서 직접 새로 만드는 것(조립만 허용).
