# COMP-SCR001-MATES-TEASER - 최근 동행글 3개/Empty State

Category: Component | Implementation Status: IMPLEMENT | Priority: P1

## Context

SCR-001 하단에 최근 동행글 3개 또는 완성형 Empty State를 보여주는 티저. API-MATE-POSTS의 최신 3건을 재사용한다.

## Project Scope

이 Task는 개별 Requirement가 아니라 공통 인프라/전역 계층에 속하며, `docs/PROJECT_SCOPE.md`상 프로젝트 범위 내 **IMPLEMENT** 구현 방식을 지원한다.

## Requirement Ref

없음(이 Task는 특정 Requirement에 직접 매핑되지 않음)

## Screen / Route / Page Entry

Screen: SCR-001  
Route: `/`  
Page Entry: `src/app/page.tsx`

## Design Ref

- `design-reference/UI_CONTRACT.md` - SCR-001 절
- `design-reference/D-001/DESIGN.md` - Color Token / Typography / Spacing / Radius / Shadow, Do / Do Not 목록

## Depends On

- API-MATE-POSTS
- COMP-GLOBAL-EMPTY-STATE
- COMP-GLOBAL-LOADING-STATE
- COMP-GLOBAL-ERROR-STATE

## Expected Files

- `src/components/home/MatesTeaser.tsx`

## Functional AC

각 Component는 지정된 구현 방법을 따른다 — 여행지/안전/대표 콘텐츠는 `DATA-*` 정적 데이터만 읽고 DB를 호출하지 않는다(REQ-FUNC-008/046/052 데이터 계층 검증은 DATA-VALIDATION-SCRIPT 담당). 즐겨찾기는 localStorage(`favorites` key, JSON 배열)만 사용한다. API-MATE-POSTS를 호출하는 MATES-TEASER는 COMP-GLOBAL-LOADING-STATE/COMP-GLOBAL-ERROR-STATE로 로딩·오류 상태를 표시한다(나머지 Component는 정적 데이터만 사용하므로 해당 없음).

## Visual AC

Card는 사진 우선(`radius.md`), 국내/해외 Grid는 배경 톤 또는 배지로 시각적으로 구분한다(동일 레이아웃 반복 금지). 빈 Card·Lorem ipsum·준비 중 금지.

## Security/Privacy AC

전부 Public 컴포넌트, 인증 불필요. 안전정보 배지는 텍스트+아이콘 병기(색상 단독 금지).

## Test Cases

1. 동행글이 3건 이상이면 최신 3건만 표시된다.
2. 0건일 때 아이콘+설명+3단계 이용 방법+작성 CTA를 갖춘 Empty State가 표시된다.

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
