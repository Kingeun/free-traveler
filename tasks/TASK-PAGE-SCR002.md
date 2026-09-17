# PAGE-SCR002 - 대표 소개 페이지 조립

Category: Page Owner | Implementation Status: IMPLEMENT | Priority: P1

## Context

SCR-002(`/about`)의 Page Owner Task. `DATA-REPRESENTATIVE` 하나의 데이터 소스와 7개 Component를 순서대로 배치해 대표 소개 페이지를 완성한다.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030

## Screen / Route / Page Entry

Screen: SCR-002  
Route: `/about`  
Page Entry: `src/app/about/page.tsx`

## Design Ref

- `design-reference/UI_CONTRACT.md` - SCR-002 절
- `design-reference/D-001/DESIGN.md` - Color Token / Typography / Spacing / Radius / Shadow, Do / Do Not 목록
- `design-reference/SCREEN_ROUTE_CONTRACT.json` - 해당 Screen 객체(section_order/key_components/forbidden_features)

## Depends On

- COMP-SCR002-HERO
- COMP-SCR002-STATS
- COMP-SCR002-INTRO
- COMP-SCR002-TIMELINE
- COMP-SCR002-COUNTRY-CHIPS
- COMP-SCR002-GALLERY
- COMP-SCR002-MEMORABLE-CTA
- COMP-GLOBAL-HEADER-FOOTER
- DATA-REPRESENTATIVE

## Expected Files

- `src/app/about/page.tsx`(신규 생성)

## Functional AC

- Section 순서: ①Profile Hero ②여행 지표 ③소개·철학 ④Timeline ⑤방문 국가 ⑥Gallery ⑦기억에 남는 여행지+CTA.
- 최소 콘텐츠 수: Timeline 6개 이상, 방문 국가 30개(권역별), Gallery 8장 이상(실제 지명 alt), 추천 여행지 4개.
- 전 Section 데이터 출처: DATA-REPRESENTATIVE.
- Desktop 콘텐츠 최대폭 1200~1280px, Section 여백 64~96px.
- 이 Task는 Component를 새로 만들지 않고 Depends On의 Component/Data Task 결과물만 조립한다.

## Visual AC

- Hero 높이 제한, 다음 Section 폴드 내 노출.
- Lorem ipsum·준비 중·정보 확인 필요·빈 Card 금지.
- 정적 콘텐츠이므로 Empty State 없음 — 대신 최소 콘텐츠 수 미달 시 DATA-VALIDATION-SCRIPT가 게시를 차단.
- 전 Section이 빌드 타임 정적 데이터만 사용해 런타임 네트워크 호출이 없으므로 Loading/Error State도 해당 없음.

## Security/Privacy AC

- 전체 Public, 인증 불필요.

## Test Cases

1. Timeline이 6개 이상, 방문 국가가 30개, Gallery가 8장 이상 렌더링된다.
2. Gallery 이미지 각각에 실제 장소를 설명하는 alt 텍스트가 있다.
3. 기억에 남는 여행지 Card를 클릭하면 SCR-001의 상세 Drawer로 이동한다.

## Verify

E2E-PUBLIC-SMOKE, MANUAL-RESPONSIVE-DENSITY

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
