# COMP-GLOBAL-EMPTY-STATE - 완성형 Empty State 재사용 블록

Category: Component | Implementation Status: IMPLEMENT | Priority: P0

## Context

여러 화면에서 재사용하는 완성형 Empty State 블록(아이콘+설명+이용 방법+CTA).

## Project Scope

이 Task는 개별 Requirement가 아니라 공통 인프라/전역 계층에 속하며, `docs/PROJECT_SCOPE.md`상 프로젝트 범위 내 **IMPLEMENT** 구현 방식을 지원한다.

## Requirement Ref

없음(이 Task는 특정 Requirement에 직접 매핑되지 않음)

## Screen / Route / Page Entry

Screen: 전역  
Route: 전체  
Page Entry: `src/app/layout.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` - Color Token / Typography / Spacing / Radius / Shadow, Do / Do Not 목록

## Depends On

- 없음

## Expected Files

- `src/components/shared/EmptyState.tsx`

## Functional AC

`design-reference/D-001/DESIGN.md`의 Color Token·Typography·Spacing·Radius·Shadow를 Tailwind 테마로 그대로 옮긴다. Toast는 서버 저장 없이 클라이언트 상태(예: `useToast` 훅)로만 동작한다. Supabase에서 데이터를 읽거나 쓰는 모든 Component(POST-LIST/DETAIL-PANEL/APPLY-FORM/REPORT-ACTION/BLOCK-ACTION/AUTH/PROFILE/MY-ACTIVITY/ADMIN-REPORTS/ADMIN-URL-SETTINGS/MATE-LOGIN-GATE/MATE-WRITE-FORM/MATES-TEASER)는 COMP-GLOBAL-LOADING-STATE(요청 진행 중)와 COMP-GLOBAL-ERROR-STATE(요청 실패+재시도 버튼)를 공용으로 사용한다 — 정적 데이터만 쓰는 Component(SCR-001/002의 나머지, SCR-003의 FLIGHT-FORM/HOTEL-FORM/SUMMARY-ACTION/TIPS/INTRO-TABS-SHELL)는 해당 없음.

## Visual AC

Header는 Desktop 72px/Mobile 56px 높이, nav 4개(여행지/여행 도구/동행/대표소개) + 로그인 영역. Footer는 서비스/정책/문의 3컬럼(Mobile 1컬럼). LoadingState는 Skeleton 또는 Spinner+안내 문구, ErrorState는 오류 메시지+재시도 버튼을 갖춘 완성형 블록으로 빈 화면·무한 스피너를 남기지 않는다.

## Security/Privacy AC

해당 없음(순수 UI/스타일 계층).

## Test Cases

1. 아이콘·설명·이용 방법·CTA 네 props가 모두 없으면 개발 중 경고를 낸다.

## Verify

MANUAL-ACCESSIBILITY-KEYBOARD, MANUAL-RESPONSIVE-DENSITY

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
