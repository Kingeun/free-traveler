# PAGE-SCR001 - 메인 페이지 조립

Category: Page Owner | Implementation Status: IMPLEMENT | Priority: P0

## Context

SCR-001(`/`)의 Page Owner Task. create-next-app 기본 스캐폴드를 완전히 교체하고, 이미 만들어진 8개 Component와 3개 Data Task의 결과물을 7개 Section 순서로 조립하는 것이 유일한 책임이다.

## Project Scope

이 Task가 다루는 모든 Requirement(REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030)는 `docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다.

## Requirement Ref

REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030

## Screen / Route / Page Entry

Screen: SCR-001  
Route: `/`  
Page Entry: `src/app/page.tsx`

## Design Ref

- `design-reference/UI_CONTRACT.md` - SCR-001 절
- `design-reference/D-001/DESIGN.md` - Color Token / Typography / Spacing / Radius / Shadow, Do / Do Not 목록
- `design-reference/SCREEN_ROUTE_CONTRACT.json` - 해당 Screen 객체(section_order/key_components/forbidden_features)

## Depends On

- COMP-SCR001-HERO-SEARCH
- COMP-SCR001-DOMESTIC-GRID
- COMP-SCR001-OVERSEAS-GRID
- COMP-SCR001-THEME-CHIPS
- COMP-SCR001-SAFETY-PANEL
- COMP-SCR001-MATES-TEASER
- COMP-SCR001-FOUNDER-BAND
- COMP-SCR001-DEST-DRAWER
- COMP-GLOBAL-HEADER-FOOTER
- COMP-GLOBAL-TOAST
- COMP-GLOBAL-EMPTY-STATE
- COMP-GLOBAL-LOADING-STATE
- COMP-GLOBAL-ERROR-STATE
- DATA-DESTINATIONS
- DATA-SAFETY
- DATA-REPRESENTATIVE

## Expected Files

- `src/app/page.tsx`(기존 create-next-app 기본 코드 전체 교체)

## Functional AC

- create-next-app Starter(로고·"Get started"·Vercel 배포 링크) 완전 제거 후 교체.
- Section 순서: ①검색 Hero ②국내 여행지 6개 Card ③해외 여행지 6개 Card ④여행 동기 6개 Chip ⑤국가별 주의사항 6개 Card ⑥최근 동행글 3개 또는 완성형 Empty State ⑦free_traveler 소개.
- Section별 데이터 출처: ②③ DATA-DESTINATIONS, ⑤ DATA-SAFETY, ⑦ DATA-REPRESENTATIVE, ⑥ API-MATE-POSTS.
- Desktop(1440px) 콘텐츠 최대폭 1200~1280px·Section 여백 64~96px·Card 3열, Mobile(390px) 여백 40~64px·Card 1열.
- 이 Task는 Component를 새로 만들지 않고 Depends On에 있는 Component/Data/API Task의 결과물만 import해 조립한다.

## Visual AC

- Hero 높이 제한 — 1440px 기준 다음 Section 제목이 폴드 안에 보여야 함.
- Lorem ipsum·"준비 중"·"정보 확인 필요"·내용 없는 빈 Card 금지.
- ⑥ 동행글 0건 시 안내 문장+이용 방법 3단계+"동행 모집글 작성하기" CTA를 갖춘 완성형 Empty State.
- ⑥ 동행글 로딩 중 COMP-GLOBAL-LOADING-STATE, 조회 실패 시 COMP-GLOBAL-ERROR-STATE(재시도) 표시.

## Security/Privacy AC

- 전 Section Public 열람 가능.
- 즐겨찾기는 localStorage만 사용하고 서버로 전송하지 않음.

## Test Cases

1. 빌드 후 `/`에 접속하면 create-next-app 기본 로고/문구가 전혀 남아있지 않다.
2. 1440px 뷰포트에서 Hero 아래로 스크롤 없이 Section ②의 제목이 보인다.
3. 동행글이 0건인 계정으로 접속했을 때 Section ⑥이 완성형 Empty State로 렌더링된다(빈 화면 아님).

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
