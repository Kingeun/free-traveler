# Free Traveler — Task List

**Document ID:** TASKLIST-TRAVEL-001
**기반 문서:** `docs/06_SRS_UIUX_REVISED.md`, `docs/PROJECT_SCOPE.md`, `docs/UIUX_TRACEABILITY.md`, `design-reference/D-001/DESIGN.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, 현재 `package.json`·`src/app` 파일 트리
**선행 검사:** `python scripts/validate_inputs.py` 실행 — **PASS** (schema_version=`traveler-screen-route-v1`, Screen 5개, Requirement 114개(IMPLEMENT 93 / EXCLUDED 21) 확인, `src/app` 실제 파일 4개: `layout.tsx`, `page.tsx`, `globals.css`, `favicon.ico`만 존재 — 다른 4개 Page Entry는 전부 신규 생성 대상).

이 문서는 Task List만 다룬다. 구현 코드, Git Branch, Commit, Issue는 만들지 않았다.

---

## 요약

| 구분 | 개수 |
|---|---:|
| Task 총개수 | **71** |
| Page Owner | 5 |
| Component | 33 |
| Global/Shared Component | 6 |
| Technical Route | 2 |
| Data | 4 |
| Database | 4 |
| API | 5 |
| Unit Test | 3 |
| Integration Test | 1 |
| E2E Test | 3 |
| Manual Check | 3 |
| CI/Infra | 2 |

| Requirement 커버리지 | 개수 |
|---|---:|
| REQ-FUNC-001~080 | 80 |
| REQ-NF-001~034 | 34 |
| **합계** | **114** |
| IMPLEMENT(Task List에 연결) | 93 |
| EXCLUDED(NON_IMPLEMENTATION 표에 기록) | 21 |

**빠진 Requirement ID: 없음.** §10 "Requirement 커버리지 자가 검증"에서 93개 IMPLEMENT 전항목이 최소 1개 Task에, 21개 EXCLUDED 전항목이 NON_IMPLEMENTATION 표에 있음을 직접 나열해 확인했다.

Task 개수(69)는 참고치이며 완료 조건으로 쓰지 않는다.

---

## 1. NON_IMPLEMENTATION — EXCLUDED Requirement (21개)

`docs/PROJECT_SCOPE.md` 제외 사유를 그대로 인용한다. 상세 구현 Task를 만들지 않는다.

| Requirement | 근거 | 후속 방향 |
|---|---|---|
| REQ-FUNC-045 | "반드시 직접 구현할 범위" 12개 항목에 회원 탈퇴 파이프라인이 없음. Supabase 콘솔에서 수동 처리 | 자동화 필요성이 생기면 별도 Task로 재평가 |
| REQ-FUNC-055 | "전체 콘텐츠 CMS" 제외 — 콘텐츠는 `src/data` 코드 배포/PR로 관리 | 콘텐츠 규모가 커지면 CMS 도입 검토 |
| REQ-FUNC-056 | 범용 감사 로그 제외 — 정적 데이터 변경 이력은 Git 커밋으로 대체 | 필요 시 Git log 기반 리포트 스크립트 검토 |
| REQ-FUNC-071 | 행동 분석 이벤트 파이프라인이 12개 핵심 범위에 없음 | 분석 요구 발생 시 GA4/PostHog 등 검토 |
| REQ-FUNC-072 | "전체 콘텐츠 CMS" 제외와 동일 | REQ-FUNC-055와 동일 |
| REQ-FUNC-073 | 미디어 업로드·라이선스 승인 워크플로 제외 — 이미지는 URL+alt만 사용 | Storage 업로드 필요성 재평가 시 검토 |
| REQ-FUNC-075 | 관리자 범위를 신고 상태·외부 URL 설정으로 한정 — stale 대시보드 제외 | 운영 규모 확대 시 별도 대시보드 검토 |
| REQ-FUNC-076 | 범용 감사 로그 제외 | REQ-FUNC-056과 동일 |
| REQ-NF-007 | 자동 Lighthouse CI 게이트 미구축 — `MANUAL-PERFORMANCE-LIGHTHOUSE`로 수동 대체 | CI 예산 확보 시 Lighthouse CI 도입 |
| REQ-NF-008 | Vercel/Supabase 표준 SLA에 의존 | 트래픽 증가 시 모니터링 도구 도입 |
| REQ-NF-009 | 위와 동일(내부 API 5xx 모니터링 미구축) | 위와 동일 |
| REQ-NF-010 | Supabase 기본 백업 정책에 의존 | 운영 단계 진입 시 백업 정책 재검토 |
| REQ-NF-011 | 외부 링크 자동 점검·알림 미구축 | cron 기반 링크 체커 도입 검토 |
| REQ-NF-018 | REQ-FUNC-045와 동일 사유, Supabase 콘솔 수동 처리 | 위와 동일 |
| REQ-NF-020 | 신고 1차 검토 SLA는 운영 인력이 필요한 프로세스, 자동화 미구축 | 운영 인력 확보 시 SLA 대시보드 검토 |
| REQ-NF-021 | Rate limiting 미구현 — 신고·차단 기능으로 악용 대응 | 악용 사례 발생 시 미들웨어 추가 검토 |
| REQ-NF-022 | 범용 감사 로그 제외와 동일 | REQ-FUNC-076과 동일 |
| REQ-NF-024 | 자동 접근성 스캔(axe) 대신 Playwright Smoke로 한정 | 접근성 이슈 누적 시 axe-core CI 통합 검토 |
| REQ-NF-029 | 미디어 업로드 워크플로 제외와 동일 | REQ-FUNC-073과 동일 |
| REQ-NF-032 | 구조화 로깅 미구축 — Vercel 기본 로그로 대체 | 운영 규모 확대 시 구조화 로깅 도입 검토 |
| REQ-NF-033 | 핵심 오류 알림 체계 미구축 | Sentry 등 알림 도구 도입 검토 |

---

## 2. Task List — Page Owner (5)

Screen마다 정확히 1개. 모두 App Router Page Entry를 실제로 조립한다.

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PAGE-SCR001 | 메인 페이지 조립 | Page Owner | IMPLEMENT | REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030 | SCR-001 | `/` | `src/app/page.tsx` | COMP-SCR001-HERO-SEARCH, COMP-SCR001-DOMESTIC-GRID, COMP-SCR001-OVERSEAS-GRID, COMP-SCR001-THEME-CHIPS, COMP-SCR001-SAFETY-PANEL, COMP-SCR001-MATES-TEASER, COMP-SCR001-FOUNDER-BAND, COMP-SCR001-DEST-DRAWER, COMP-GLOBAL-HEADER-FOOTER, COMP-GLOBAL-TOAST, COMP-GLOBAL-EMPTY-STATE, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE, DATA-DESTINATIONS, DATA-SAFETY, DATA-REPRESENTATIVE | `src/app/page.tsx`(기존 create-next-app 기본 코드 전체 교체) |
| 2 | PAGE-SCR002 | 대표 소개 페이지 조립 | Page Owner | IMPLEMENT | REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030 | SCR-002 | `/about` | `src/app/about/page.tsx` | COMP-SCR002-HERO, COMP-SCR002-STATS, COMP-SCR002-INTRO, COMP-SCR002-TIMELINE, COMP-SCR002-COUNTRY-CHIPS, COMP-SCR002-GALLERY, COMP-SCR002-MEMORABLE-CTA, COMP-GLOBAL-HEADER-FOOTER, DATA-REPRESENTATIVE | `src/app/about/page.tsx`(신규 생성) |
| 3 | PAGE-SCR003 | 통합 여행 준비 페이지 조립 | Page Owner | IMPLEMENT | REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030 | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | COMP-SCR003-INTRO-TABS-SHELL, COMP-SCR003-FLIGHT-FORM, COMP-SCR003-HOTEL-FORM, COMP-SCR003-SUMMARY-ACTION, COMP-SCR003-TIPS, COMP-SCR003-MATE-WRITE-FORM, COMP-SCR003-MATE-LOGIN-GATE, COMP-GLOBAL-HEADER-FOOTER, COMP-GLOBAL-TOAST, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE | `src/app/travel-tools/page.tsx`(신규 생성) |
| 4 | PAGE-SCR004 | 동행 조회 페이지 조립 | Page Owner | IMPLEMENT | REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030 | SCR-004 | `/mates` | `src/app/mates/page.tsx` | COMP-SCR004-FILTER-BAR, COMP-SCR004-POST-LIST, COMP-SCR004-DETAIL-PANEL, COMP-SCR004-APPLY-FORM, COMP-SCR004-REPORT-ACTION, COMP-SCR004-BLOCK-ACTION, COMP-GLOBAL-HEADER-FOOTER, COMP-GLOBAL-EMPTY-STATE, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE, API-MATE-POSTS | `src/app/mates/page.tsx`(신규 생성) |
| 5 | PAGE-SCR005 | 계정·관리 페이지 조립 | Page Owner | IMPLEMENT | REQ-FUNC-070, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-023, REQ-NF-025, REQ-NF-030 | SCR-005 | `/account` | `src/app/account/page.tsx` | COMP-SCR005-AUTH, COMP-SCR005-PROFILE, COMP-SCR005-MY-ACTIVITY, COMP-SCR005-ADMIN-REPORTS, COMP-SCR005-ADMIN-URL-SETTINGS, COMP-GLOBAL-HEADER-FOOTER, COMP-GLOBAL-EMPTY-STATE, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE, API-AUTH-PROFILE | `src/app/account/page.tsx`(신규 생성) |

### Page Owner — Functional / Visual / Security·Privacy AC / Verify / Priority

**PAGE-SCR001**
- Functional AC: create-next-app Starter(로고·"Get started"·Vercel 배포 링크) 완전 제거 후 교체 / Section 순서: ①검색 Hero ②국내 여행지 6개 Card ③해외 여행지 6개 Card ④여행 동기 6개 Chip ⑤국가별 주의사항 6개 Card ⑥최근 동행글 3개 또는 완성형 Empty State ⑦free_traveler 소개 / Section별 데이터 출처: ②③ DATA-DESTINATIONS, ⑤ DATA-SAFETY, ⑦ DATA-REPRESENTATIVE, ⑥ API-MATE-POSTS / Desktop(1440px) 콘텐츠 최대폭 1200~1280px·Section 여백 64~96px·Card 3열, Mobile(390px) 여백 40~64px·Card 1열
- Visual AC: Hero 높이 제한(1440px 기준 다음 Section 제목이 폴드 안에 보여야 함) / Lorem ipsum·"준비 중"·"정보 확인 필요"·내용 없는 빈 Card 금지 / ⑥ 동행글 0건 시 안내 문장+이용 방법 3단계+"동행 모집글 작성하기" CTA를 갖춘 완성형 Empty State / ⑥ 동행글 로딩 중 COMP-GLOBAL-LOADING-STATE, 조회 실패 시 COMP-GLOBAL-ERROR-STATE(재시도) 표시
- Security/Privacy AC: 전 Section Public 열람 가능 / 즐겨찾기는 localStorage만 사용하고 서버로 전송하지 않음
- Verify: E2E-PUBLIC-SMOKE, MANUAL-RESPONSIVE-DENSITY
- Priority: P0

**PAGE-SCR002**
- Functional AC: Section 순서: ①Profile Hero ②여행 지표 ③소개·철학 ④Timeline ⑤방문 국가 ⑥Gallery ⑦기억에 남는 여행지+CTA / 최소 콘텐츠 수: Timeline 6개 이상, 방문 국가 30개(권역별), Gallery 8장 이상(실제 지명 alt), 추천 여행지 4개 / 전 Section 데이터 출처: DATA-REPRESENTATIVE / Desktop 콘텐츠 최대폭 1200~1280px, Section 여백 64~96px
- Visual AC: Hero 높이 제한, 다음 Section 폴드 내 노출 / Lorem ipsum·준비 중·정보 확인 필요·빈 Card 금지 / 정적 콘텐츠이므로 Empty State 없음 — 대신 최소 콘텐츠 수 미달 시 DATA-VALIDATION-SCRIPT가 게시를 차단 / 전 Section이 빌드 타임 정적 데이터만 사용해 런타임 네트워크 호출이 없으므로 Loading/Error State도 해당 없음
- Security/Privacy AC: 전체 Public, 인증 불필요
- Verify: E2E-PUBLIC-SMOKE, MANUAL-RESPONSIVE-DENSITY
- Priority: P1

**PAGE-SCR003**
- Functional AC: Section 순서: ①Intro(3단계 안내) ②탭(항공편 찾기/숙소 찾기/동행 구하기) ③여행정보 Form ④입력 요약·외부 이동 ⑤찾기 Tip 3개 ⑥동행 작성 또는 로그인 안내·안전 안내 / 3탭을 하나의 탭 컨테이너에 실제로 조립하고 탭 전환 시 다른 탭 입력 상태를 유지 / 항공·숙소 입력값은 브라우저 상태로만 처리, 서버 API·DB·분석·외부 URL 쿼리 어디에도 전송하지 않음
- Visual AC: Lorem ipsum·준비 중·정보 확인 필요·빈 Card 금지 / 동행 탭 비로그인 시 완성형 로그인 안내(설명+CTA)를 표시(빈 화면 금지) / 로그인 상태 확인 중과 동행글 제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도)를 표시(항공·숙소 탭은 서버 호출이 없어 해당 없음)
- Security/Privacy AC: 동행 작성은 로그인+성인 인증 필요(COMP-SCR003-MATE-LOGIN-GATE) / 항공·호텔 입력값 비전송(REQ-FUNC-017, REQ-FUNC-025) / 외부 링크는 `noopener,noreferrer`로 새 탭
- Verify: E2E-TRAVEL-TOOLS, UNIT-TRAVEL-DATES, MANUAL-RESPONSIVE-DENSITY
- Priority: P0

**PAGE-SCR004**
- Functional AC: Section 순서: ①Intro+작성 CTA ②Filter·결과 요약 ③동행 목록(최대 8개 우선 노출) ④상세(Desktop 좌우 분할/Mobile 상세 Drawer, 작성자·게시글 대상 신고·차단 버튼 포함) ⑤신청 방법 3단계 ⑥동행 안전수칙 요약 안내 / 목록·필터·상세·참가·신고·차단을 각각 별도 Component Task로 조립(단일 컴포넌트로 합치지 않음), 신고·차단은 상세에서 열람 중인 특정 게시글·작성자를 대상으로 동작
- Visual AC: 검색 결과 0건 시 필터 초기화+작성 CTA+이용 방법을 갖춘 완성형 Empty State / Lorem ipsum·준비 중·정보 확인 필요·빈 Card 금지 / 목록·상세 조회 중과 참가·신고·차단 제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도)를 표시
- Security/Privacy AC: 참가 요청·신고·차단은 로그인 필요 / RLS로 본인 글/요청만 비공개 데이터 열람(DB-RLS-BASE)
- Verify: E2E-MATE-AUTH, TEST-RLS-BASIC, MANUAL-RESPONSIVE-DENSITY
- Priority: P0

**PAGE-SCR005**
- Functional AC: 현재 역할(Guest/Member/Admin)의 Intro→핵심 작업→도움말/다음 행동을 실제로 조건부 렌더링 / 역할에 없는 관리 영역(예: Member의 Admin 탭)은 렌더링 자체를 하지 않음 / Dashboard·통계형 화면을 만들지 않음
- Visual AC: 내 글/참가 요청/차단/즐겨찾기/신고 큐가 0건일 때 각각 완성형 Empty State(설명+다음 행동 CTA) / Lorem ipsum·준비 중·정보 확인 필요·빈 Card 금지 / 인증·프로필·활동 내역·관리자 데이터 조회·제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도)를 표시
- Security/Privacy AC: Guest는 Member/Admin 탭에 접근 불가(탭 자체 미노출) / Admin 범위는 신고 상태 변경·외부 URL 설정으로 한정(콘텐츠 CRUD·감사 로그 없음)
- Verify: E2E-MATE-AUTH, TEST-RLS-BASIC, MANUAL-RESPONSIVE-DENSITY
- Priority: P0

---

## 3. Task List — Component: SCR-001 (8)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 6 | COMP-SCR001-HERO-SEARCH | 검색 Hero | Component | IMPLEMENT | REQ-FUNC-003, REQ-FUNC-067, REQ-NF-004 | SCR-001 | `/` | `src/app/page.tsx` | COMP-GLOBAL-DESIGN-TOKENS | `src/components/home/HeroSearch.tsx` |
| 7 | COMP-SCR001-DOMESTIC-GRID | 국내 여행지 6개 Card | Component | IMPLEMENT | REQ-FUNC-001, REQ-FUNC-002, REQ-FUNC-005, REQ-FUNC-068 | SCR-001 | `/` | `src/app/page.tsx` | DATA-DESTINATIONS, COMP-SCR001-DEST-DRAWER | `src/components/home/DomesticGrid.tsx` |
| 8 | COMP-SCR001-OVERSEAS-GRID | 해외 여행지 6개 Card | Component | IMPLEMENT | REQ-FUNC-001, REQ-FUNC-002, REQ-FUNC-005, REQ-FUNC-006, REQ-FUNC-068 | SCR-001 | `/` | `src/app/page.tsx` | DATA-DESTINATIONS, COMP-SCR001-DEST-DRAWER, COMP-SCR001-SAFETY-PANEL | `src/components/home/OverseasGrid.tsx` |
| 9 | COMP-SCR001-DEST-DRAWER | 여행지 상세 Drawer | Component | IMPLEMENT | REQ-FUNC-004, REQ-FUNC-009, REQ-FUNC-069 | SCR-001 | `/` | `src/app/page.tsx` | DATA-DESTINATIONS | `src/components/home/DestinationDrawer.tsx` |
| 10 | COMP-SCR001-THEME-CHIPS | 여행 동기 6개 Chip | Component | IMPLEMENT | REQ-FUNC-002, REQ-FUNC-010 | SCR-001 | `/` | `src/app/page.tsx` | COMP-SCR001-DOMESTIC-GRID, COMP-SCR001-OVERSEAS-GRID | `src/components/home/ThemeChips.tsx` |
| 11 | COMP-SCR001-SAFETY-PANEL | 국가별 주의사항 6개 Card+Drawer | Component | IMPLEMENT | REQ-FUNC-047, REQ-FUNC-048, REQ-FUNC-049, REQ-FUNC-050, REQ-FUNC-051, REQ-FUNC-053, REQ-FUNC-054, REQ-NF-028 | SCR-001 | `/` | `src/app/page.tsx` | DATA-SAFETY | `src/components/home/SafetyPanel.tsx` |
| 12 | COMP-SCR001-MATES-TEASER | 최근 동행글 3개/Empty State | Component | IMPLEMENT | - | SCR-001 | `/` | `src/app/page.tsx` | API-MATE-POSTS, COMP-GLOBAL-EMPTY-STATE, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE | `src/components/home/MatesTeaser.tsx` |
| 13 | COMP-SCR001-FOUNDER-BAND | free_traveler 요약+CTA | Component | IMPLEMENT | REQ-FUNC-057, REQ-FUNC-063 | SCR-001 | `/` | `src/app/page.tsx` | DATA-REPRESENTATIVE | `src/components/home/FounderBand.tsx` |

- 공통 Functional AC: 각 Component는 지정된 구현 방법을 따른다 — 여행지/안전/대표 콘텐츠는 `DATA-*` 정적 데이터만 읽고 DB를 호출하지 않는다(REQ-FUNC-008/046/052 데이터 계층 검증은 DATA-VALIDATION-SCRIPT 담당). 즐겨찾기는 localStorage(`favorites` key, JSON 배열)만 사용한다. API-MATE-POSTS를 호출하는 MATES-TEASER는 COMP-GLOBAL-LOADING-STATE/COMP-GLOBAL-ERROR-STATE로 로딩·오류 상태를 표시한다(나머지 Component는 정적 데이터만 사용하므로 해당 없음).
- 공통 Visual AC: Card는 사진 우선(`radius.md`), 국내/해외 Grid는 배경 톤 또는 배지로 시각적으로 구분한다(동일 레이아웃 반복 금지). 빈 Card·Lorem ipsum·준비 중 금지.
- 공통 Security/Privacy AC: 전부 Public 컴포넌트, 인증 불필요. 안전정보 배지는 텍스트+아이콘 병기(색상 단독 금지).
- Verify: E2E-PUBLIC-SMOKE
- Priority: HERO-SEARCH/DOMESTIC-GRID/OVERSEAS-GRID/SAFETY-PANEL = P0, 나머지 = P1

---

## 4. Task List — Component: SCR-002 (7)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 14 | COMP-SCR002-HERO | Profile Hero | Component | IMPLEMENT | - | SCR-002 | `/about` | `src/app/about/page.tsx` | DATA-REPRESENTATIVE | `src/components/about/ProfileHero.tsx` |
| 15 | COMP-SCR002-STATS | 여행 지표 | Component | IMPLEMENT | REQ-FUNC-057 | SCR-002 | `/about` | `src/app/about/page.tsx` | DATA-REPRESENTATIVE | `src/components/about/Stats.tsx` |
| 16 | COMP-SCR002-INTRO | 소개·철학 | Component | IMPLEMENT | REQ-FUNC-058, REQ-FUNC-062 | SCR-002 | `/about` | `src/app/about/page.tsx` | DATA-REPRESENTATIVE | `src/components/about/Intro.tsx` |
| 17 | COMP-SCR002-TIMELINE | 여행 Timeline 6개 이상 | Component | IMPLEMENT | REQ-FUNC-060 | SCR-002 | `/about` | `src/app/about/page.tsx` | DATA-REPRESENTATIVE | `src/components/about/Timeline.tsx` |
| 18 | COMP-SCR002-COUNTRY-CHIPS | 방문 국가 30개 Chip | Component | IMPLEMENT | REQ-FUNC-059 | SCR-002 | `/about` | `src/app/about/page.tsx` | DATA-REPRESENTATIVE | `src/components/about/CountryChips.tsx` |
| 19 | COMP-SCR002-GALLERY | Gallery 8장 이상 | Component | IMPLEMENT | REQ-FUNC-061 | SCR-002 | `/about` | `src/app/about/page.tsx` | DATA-REPRESENTATIVE | `src/components/about/Gallery.tsx` |
| 20 | COMP-SCR002-MEMORABLE-CTA | 기억에 남는 여행지 4개+CTA | Component | IMPLEMENT | REQ-FUNC-063 | SCR-002 | `/about` | `src/app/about/page.tsx` | DATA-REPRESENTATIVE, COMP-SCR001-DEST-DRAWER | `src/components/about/MemorableCta.tsx` |

- 공통 Functional AC: 전부 `DATA-REPRESENTATIVE` 정적 데이터만 사용. Gallery 이미지는 실제 촬영 장소를 설명하는 alt 텍스트를 필수로 가진다(일반 URL 이미지, 업로드 워크플로 없음).
- 공통 Visual AC: Section마다 시각 패턴을 다르게 한다(Hero/Stat/좌우분할/Timeline/Chip/Gallery/CTA Banner가 서로 다른 레이아웃). Lorem ipsum·빈 Card 금지.
- 공통 Security/Privacy AC: 전부 Public.
- Verify: E2E-PUBLIC-SMOKE
- Priority: HERO/STATS/TIMELINE/GALLERY = P1, 나머지 = P2

---

## 5. Task List — Component: SCR-003 (7, 항공·숙소·동행 작성 분리)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 21 | COMP-SCR003-INTRO-TABS-SHELL | Intro 3단계 안내+탭 컨테이너 | Component | IMPLEMENT | - | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | COMP-GLOBAL-DESIGN-TOKENS | `src/components/travel-tools/IntroTabsShell.tsx` |
| 22 | COMP-SCR003-FLIGHT-FORM | 항공편 조건 입력(항공 영역) | Component | IMPLEMENT | REQ-FUNC-011, REQ-FUNC-012, REQ-FUNC-013, REQ-FUNC-015, REQ-FUNC-017, REQ-NF-017 | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | COMP-SCR003-INTRO-TABS-SHELL | `src/components/travel-tools/FlightForm.tsx` |
| 23 | COMP-SCR003-HOTEL-FORM | 숙소 조건 입력(숙소 영역) | Component | IMPLEMENT | REQ-FUNC-019, REQ-FUNC-020, REQ-FUNC-021, REQ-FUNC-023, REQ-FUNC-025, REQ-NF-017 | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | COMP-SCR003-INTRO-TABS-SHELL | `src/components/travel-tools/HotelForm.tsx` |
| 24 | COMP-SCR003-SUMMARY-ACTION | 입력 요약+외부 이동 Action Card | Component | IMPLEMENT | REQ-FUNC-014, REQ-FUNC-016, REQ-FUNC-018, REQ-FUNC-022, REQ-FUNC-024, REQ-FUNC-026, REQ-FUNC-054 | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | COMP-SCR003-FLIGHT-FORM, COMP-SCR003-HOTEL-FORM | `src/components/travel-tools/SummaryAction.tsx` |
| 25 | COMP-SCR003-TIPS | 찾기 Tip 3개 | Component | IMPLEMENT | - | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | - | `src/components/travel-tools/Tips.tsx` |
| 26 | COMP-SCR003-MATE-LOGIN-GATE | 동행 작성(동행 작성 영역) — 로그인/성인인증 게이트 | Component | IMPLEMENT | REQ-FUNC-027, REQ-FUNC-028 | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | API-AUTH-PROFILE, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE | `src/components/travel-tools/MateLoginGate.tsx` |
| 27 | COMP-SCR003-MATE-WRITE-FORM | 동행 작성(동행 작성 영역) — 작성 Form+안전 안내 | Component | IMPLEMENT | REQ-FUNC-031, REQ-FUNC-032, REQ-FUNC-080 | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | COMP-SCR003-MATE-LOGIN-GATE, API-MATE-POSTS, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE | `src/components/travel-tools/MateWriteForm.tsx` |

- 공통 Functional AC: 항공(22)·숙소(23)·동행 작성(26,27) 세 영역은 서로 다른 파일/컴포넌트로 분리하고, 세 영역의 입력·검증·완료 상태는 서로 독립적으로 유지한다(탭 전환 시 값 보존은 IntroTabsShell이 상위 상태로 관리).
- 공통 Visual AC: 각 Form은 라벨+도움말+오류 영역을 갖추고 Lorem ipsum·준비 중 금지. MATE-LOGIN-GATE(인증 상태 확인)와 MATE-WRITE-FORM(제출)은 COMP-GLOBAL-LOADING-STATE/COMP-GLOBAL-ERROR-STATE를 사용하고, FLIGHT-FORM/HOTEL-FORM/SUMMARY-ACTION/TIPS/INTRO-TABS-SHELL은 서버 호출이 없어 해당 없음.
- 공통 Security/Privacy AC: FLIGHT-FORM/HOTEL-FORM은 입력값을 `useState` 등 브라우저 상태로만 유지하고 서버 API·URL 쿼리로 전송하지 않는다(REQ-FUNC-017, REQ-FUNC-025). MATE-WRITE-FORM은 제출 전 정규식으로 전화번호·이메일·메신저 ID 패턴을 탐지해 차단한다(REQ-FUNC-032, UNIT-CONTACT-DETECTION 연동).
- Verify: E2E-TRAVEL-TOOLS(FLIGHT/HOTEL/SUMMARY/TIPS), E2E-MATE-AUTH(LOGIN-GATE/WRITE-FORM), UNIT-TRAVEL-DATES(FLIGHT/HOTEL)
- Priority: FLIGHT-FORM/HOTEL-FORM/SUMMARY-ACTION = P0, MATE-LOGIN-GATE/MATE-WRITE-FORM = P0, INTRO-TABS-SHELL = P1, TIPS = P2

---

## 6. Task List — Component: SCR-004 (6, 목록·필터·상세·참가·신고·차단 분리)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 28 | COMP-SCR004-FILTER-BAR | 필터(국가/지역/기간/연령대/성별/스타일/모집상태) | Component | IMPLEMENT | REQ-FUNC-030, REQ-NF-004 | SCR-004 | `/mates` | `src/app/mates/page.tsx` | API-MATE-POSTS | `src/components/mates/FilterBar.tsx` |
| 29 | COMP-SCR004-POST-LIST | 동행글 목록(최대 8개) | Component | IMPLEMENT | REQ-FUNC-033, REQ-FUNC-037 | SCR-004 | `/mates` | `src/app/mates/page.tsx` | COMP-SCR004-FILTER-BAR, API-MATE-POSTS, COMP-GLOBAL-EMPTY-STATE, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE | `src/components/mates/PostList.tsx` |
| 30 | COMP-SCR004-DETAIL-PANEL | 상세(Desktop 분할/Mobile Drawer) | Component | IMPLEMENT | REQ-FUNC-036, REQ-FUNC-038, REQ-FUNC-044, REQ-FUNC-069 | SCR-004 | `/mates` | `src/app/mates/page.tsx` | COMP-SCR004-POST-LIST, API-MATE-POSTS, DB-RLS-BASE, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE | `src/components/mates/DetailPanel.tsx` |
| 31 | COMP-SCR004-APPLY-FORM | 참가 요청 Form(500자 이내)+신청 방법 3단계 | Component | IMPLEMENT | REQ-FUNC-034, REQ-FUNC-035 | SCR-004 | `/mates` | `src/app/mates/page.tsx` | COMP-SCR004-DETAIL-PANEL, API-MATE-APPLICATIONS, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE | `src/components/mates/ApplyForm.tsx` |
| 32 | COMP-SCR004-REPORT-ACTION | 신고(사유 코드+설명) | Component | IMPLEMENT | REQ-FUNC-039, REQ-NF-019 | SCR-004 | `/mates` | `src/app/mates/page.tsx` | COMP-SCR004-DETAIL-PANEL, API-BLOCKS-REPORTS, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE | `src/components/mates/ReportAction.tsx` |
| 33 | COMP-SCR004-BLOCK-ACTION | 차단·해제+안전 안내 CTA | Component | IMPLEMENT | REQ-FUNC-040 | SCR-004 | `/mates` | `src/app/mates/page.tsx` | COMP-SCR004-DETAIL-PANEL, API-BLOCKS-REPORTS, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE | `src/components/mates/BlockAction.tsx` |

- 공통 Functional AC: 목록(29)·필터(28)·상세(30)·참가(31)·신고(32)·차단(33)을 각각 독립 컴포넌트/파일로 유지한다(단일 컴포넌트로 합치지 않음, rule 10). 신고(32)·차단(33)은 상세(30)에서 열람 중인 특정 게시글·작성자를 대상으로 동작하며(COMP-SCR004-DETAIL-PANEL 의존), 대상 없이 독립적으로 호출되지 않는다. 차단된 상대의 글은 목록·상세에서 제외한다.
- 공통 Visual AC: 검색 결과 0건은 COMP-GLOBAL-EMPTY-STATE(필터 초기화+작성 CTA+이용 방법)로 표시. Supabase 조회/제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도 포함)를 표시한다(POST-LIST/DETAIL-PANEL/APPLY-FORM/REPORT-ACTION/BLOCK-ACTION). Lorem ipsum·빈 Card 금지.
- 공통 Security/Privacy AC: 참가 요청 내용은 작성자·요청자만 열람(RLS). 신고·차단은 로그인 필요. 응답/렌더링에 이메일·전화번호 노출 금지(REQ-FUNC-033).
- Verify: E2E-MATE-AUTH, TEST-RLS-BASIC, UNIT-MATE-STATE(POST-LIST/DETAIL-PANEL/APPLY-FORM)
- Priority: FILTER-BAR/POST-LIST/DETAIL-PANEL/APPLY-FORM = P0, REPORT-ACTION/BLOCK-ACTION = P1

---

## 7. Task List — Component: SCR-005 (5, Auth·Profile·My Activity·Admin 분리)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 34 | COMP-SCR005-AUTH | Guest — 로그인/가입/비밀번호 재설정 | Component | IMPLEMENT | REQ-FUNC-027, REQ-FUNC-028, REQ-FUNC-066 | SCR-005 | `/account` | `src/app/account/page.tsx` | API-AUTH-PROFILE, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE | `src/components/account/Auth.tsx` |
| 35 | COMP-SCR005-PROFILE | Member — 프로필·성인 확인 요약 | Component | IMPLEMENT | REQ-FUNC-029 | SCR-005 | `/account` | `src/app/account/page.tsx` | COMP-SCR005-AUTH, API-AUTH-PROFILE, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE | `src/components/account/Profile.tsx` |
| 36 | COMP-SCR005-MY-ACTIVITY | Member — My Activity(내 글/참가요청/차단/즐겨찾기) | Component | IMPLEMENT | REQ-FUNC-040, REQ-FUNC-068 | SCR-005 | `/account` | `src/app/account/page.tsx` | API-MATE-POSTS, API-MATE-APPLICATIONS, API-BLOCKS-REPORTS, COMP-GLOBAL-EMPTY-STATE, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE | `src/components/account/MyActivity.tsx` |
| 37 | COMP-SCR005-ADMIN-REPORTS | Admin — 신고 상태 변경+글 숨김 | Component | IMPLEMENT | REQ-FUNC-041, REQ-FUNC-042 | SCR-005 | `/account` | `src/app/account/page.tsx` | API-BLOCKS-REPORTS, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE | `src/components/account/AdminReports.tsx` |
| 38 | COMP-SCR005-ADMIN-URL-SETTINGS | Admin — 항공·숙소 외부 URL 설정 | Component | IMPLEMENT | REQ-FUNC-077 | SCR-005 | `/account` | `src/app/account/page.tsx` | API-ADMIN-SETTINGS, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-ERROR-STATE | `src/components/account/AdminUrlSettings.tsx` |

- 공통 Functional AC: Guest/Member/Admin 4영역(Auth/Profile/My Activity/Admin)을 파일 단위로 분리한다. Admin 컴포넌트는 Admin 역할이 아니면 import된 채로도 렌더링되지 않는다(조건부 렌더링, 코드 존재 자체는 금지 아님).
- 공통 Visual AC: My Activity의 각 목록(내 글/참가요청/차단/즐겨찾기) 0건 시 완성형 Empty State. Supabase 조회/제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도 포함)를 표시한다(AUTH/PROFILE/MY-ACTIVITY/ADMIN-REPORTS/ADMIN-URL-SETTINGS 전부). Lorem ipsum·빈 Card 금지.
- 공통 Security/Privacy AC: 성인 인증은 `is_adult`/`adult_verified_at`만 저장하고 생년월일 원본은 저장하지 않는다(REQ-FUNC-028). Admin 컴포넌트는 서버 측 역할 검증과 함께 사용(클라이언트 조건부 렌더링만으로 신뢰하지 않음).
- Verify: E2E-MATE-AUTH, TEST-RLS-BASIC
- Priority: AUTH/PROFILE/MY-ACTIVITY = P0, ADMIN-REPORTS/ADMIN-URL-SETTINGS = P1

---

## 8. Task List — Global/Shared Component (6)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 39 | COMP-GLOBAL-HEADER-FOOTER | 전역 Header/Footer | Component | IMPLEMENT | REQ-FUNC-064, REQ-FUNC-079 | 전역(5개 Screen) | 전체 | `src/app/layout.tsx` | COMP-GLOBAL-DESIGN-TOKENS | `src/components/shared/Header.tsx`, `src/components/shared/Footer.tsx` |
| 40 | COMP-GLOBAL-TOAST | 인앱 Toast(접수/승인/거절/신고 알림) | Component | IMPLEMENT | REQ-FUNC-043 | 전역(SCR-003·004·005) | 전체 | `src/app/layout.tsx` | COMP-GLOBAL-DESIGN-TOKENS | `src/components/shared/Toast.tsx` |
| 41 | COMP-GLOBAL-EMPTY-STATE | 완성형 Empty State 재사용 블록 | Component | IMPLEMENT | - | 전역 | 전체 | `src/app/layout.tsx` | - | `src/components/shared/EmptyState.tsx` |
| 42 | COMP-GLOBAL-DESIGN-TOKENS | Tailwind 디자인 토큰(D-001 반영) | Component | IMPLEMENT | REQ-FUNC-065, REQ-NF-006 | 전역 | 전체 | `src/app/layout.tsx` | - | `tailwind.config.ts`, `src/app/globals.css`(수정) |
| 70 | COMP-GLOBAL-LOADING-STATE | 재사용 Loading State | Component | IMPLEMENT | - | 전역 | 전체 | `src/app/layout.tsx` | COMP-GLOBAL-DESIGN-TOKENS | `src/components/shared/LoadingState.tsx` |
| 71 | COMP-GLOBAL-ERROR-STATE | 재사용 Error State(재시도 포함) | Component | IMPLEMENT | - | 전역 | 전체 | `src/app/layout.tsx` | COMP-GLOBAL-DESIGN-TOKENS | `src/components/shared/ErrorState.tsx` |

- Functional AC: `design-reference/D-001/DESIGN.md`의 Color Token·Typography·Spacing·Radius·Shadow를 Tailwind 테마로 그대로 옮긴다. Toast는 서버 저장 없이 클라이언트 상태(예: `useToast` 훅)로만 동작한다. Supabase에서 데이터를 읽거나 쓰는 모든 Component(POST-LIST/DETAIL-PANEL/APPLY-FORM/REPORT-ACTION/BLOCK-ACTION/AUTH/PROFILE/MY-ACTIVITY/ADMIN-REPORTS/ADMIN-URL-SETTINGS/MATE-LOGIN-GATE/MATE-WRITE-FORM/MATES-TEASER)는 COMP-GLOBAL-LOADING-STATE(요청 진행 중)와 COMP-GLOBAL-ERROR-STATE(요청 실패+재시도 버튼)를 공용으로 사용한다 — 정적 데이터만 쓰는 Component(SCR-001/002의 나머지, SCR-003의 FLIGHT-FORM/HOTEL-FORM/SUMMARY-ACTION/TIPS/INTRO-TABS-SHELL)는 해당 없음.
- Visual AC: Header는 Desktop 72px/Mobile 56px 높이, nav 4개(여행지/여행 도구/동행/대표소개) + 로그인 영역. Footer는 서비스/정책/문의 3컬럼(Mobile 1컬럼). LoadingState는 Skeleton 또는 Spinner+안내 문구, ErrorState는 오류 메시지+재시도 버튼을 갖춘 완성형 블록으로 빈 화면·무한 스피너를 남기지 않는다.
- Security/Privacy AC: 해당 없음(순수 UI/스타일 계층).
- Verify: MANUAL-ACCESSIBILITY-KEYBOARD, MANUAL-RESPONSIVE-DENSITY
- Priority: P0

---

## 9. Task List — Technical Route (2)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 43 | COMP-TECH-ERROR-PAGES | 404/500 복구 화면 | Technical Route | IMPLEMENT | REQ-FUNC-078 | 기술 Route | `not-found` / `error` | `src/app/not-found.tsx`, `src/app/error.tsx` | COMP-GLOBAL-DESIGN-TOKENS | `src/app/not-found.tsx`, `src/app/error.tsx` |
| 44 | COMP-TECH-POLICY-PAGES | 이용약관·개인정보처리방침·동행 안전수칙·콘텐츠 면책 | Technical Route | IMPLEMENT | REQ-FUNC-080 | 기술 Route | `/policies/*` | `src/app/policies/terms/page.tsx` 등 | COMP-GLOBAL-DESIGN-TOKENS | `src/app/policies/terms/page.tsx`, `.../privacy/page.tsx`, `.../mate-safety/page.tsx`, `.../content-disclaimer/page.tsx` |

- Functional AC: 404/500 화면은 각각 홈으로 이동·다시 시도 중 최소 1개 복구 행동을 제공한다. 정책 페이지는 정적 콘텐츠이며 COMP-SCR003-MATE-WRITE-FORM의 동의 체크박스가 이 페이지를 링크한다.
- Visual AC: Lorem ipsum·준비 중 금지, 실제 정책 문구를 채운다.
- Security/Privacy AC: 해당 없음.
- Verify: E2E-PUBLIC-SMOKE
- Priority: P1(ERROR-PAGES), P2(POLICY-PAGES)

---

## 10. Task List — Data (4)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 45 | DATA-DESTINATIONS | 여행지 정적 데이터(국내 10+/해외 15개국 30도시+) | Data | IMPLEMENT | REQ-FUNC-001, REQ-FUNC-004, REQ-FUNC-007, REQ-FUNC-009, REQ-NF-026 | SCR-001 | `/` | - | - | `src/data/destinations.ts` |
| 46 | DATA-SAFETY | 국가 안전정보 정적 데이터(8개 카테고리) | Data | IMPLEMENT | REQ-FUNC-046, REQ-FUNC-047, REQ-FUNC-048, REQ-FUNC-053, REQ-NF-027 | SCR-001 | `/` | - | - | `src/data/safety.ts` |
| 47 | DATA-REPRESENTATIVE | 대표 소개 정적 데이터(지표/Timeline/방문국가/Gallery) | Data | IMPLEMENT | REQ-FUNC-057, REQ-FUNC-058, REQ-FUNC-059, REQ-FUNC-060, REQ-FUNC-061, REQ-FUNC-062, REQ-FUNC-063 | SCR-001, SCR-002 | `/`, `/about` | - | - | `src/data/representative.ts` |
| 48 | DATA-VALIDATION-SCRIPT | 게시 기준 수량·완전성 빌드 타임 검증 | Data | IMPLEMENT | REQ-FUNC-008, REQ-FUNC-046, REQ-FUNC-052, REQ-FUNC-074, REQ-NF-026, REQ-NF-027 | - | - | - | DATA-DESTINATIONS, DATA-SAFETY, DATA-REPRESENTATIVE | `scripts/validate-content.ts` |

- Functional AC: 지정된 구현 방법 = 정적 데이터(TypeScript 배열/객체, DB 미사용). `DATA-DESTINATIONS`는 국내 10개 이상·해외 15개국 30개 도시 이상을 포함하고 소개·명소 5개 이상·1일/3일 일정·예산·교통·음식 3개 이상·에티켓·출처·수정일 필드를 강제하는 TypeScript 타입을 가진다. `DATA-SAFETY`는 치안/사기/법규/교통/재난/보건/문화/긴급연락처 8개 카테고리와 출처·확인일·편집자 필드를 강제한다. `DATA-VALIDATION-SCRIPT`는 `npm run build` 전(또는 별도 `npm run validate:content`)에 수량·필수 필드 누락을 검사해 실패 시 빌드를 중단한다.
- Visual AC: 해당 없음(데이터 계층).
- Security/Privacy AC: 이미지 URL은 일반 인터넷 URL만 사용, 업로드 저장소 없음.
- Verify: DATA-VALIDATION-SCRIPT 자체 실행(CI-QUALITY-GATE에 포함)
- Priority: P0(DESTINATIONS/SAFETY), P1(REPRESENTATIVE), P0(VALIDATION-SCRIPT)

---

## 11. Task List — Database (4, Schema/RLS/Access 분리)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 49 | DB-SCHEMA-BASE | 6개 테이블 스키마(profiles/mate_posts/mate_applications/user_blocks/reports/outbound_url_settings) | Database | IMPLEMENT | REQ-FUNC-027, REQ-FUNC-028, REQ-FUNC-029, REQ-FUNC-031, REQ-FUNC-034, REQ-FUNC-037, REQ-FUNC-038, REQ-FUNC-039, REQ-FUNC-040, REQ-FUNC-041, REQ-FUNC-042, REQ-FUNC-077, REQ-FUNC-080 | - | - | - | - | `supabase/migrations/0001_schema_base.sql` |
| 50 | DB-RLS-BASE | 6개 테이블 RLS 정책 | Database | IMPLEMENT | REQ-FUNC-044, REQ-NF-013 | - | - | - | DB-SCHEMA-BASE | `supabase/migrations/0002_rls_base.sql` |
| 51 | DB-ACCESS | 타입 안전 쿼리/서버 액션 헬퍼 | Database | IMPLEMENT | REQ-FUNC-017, REQ-FUNC-033, REQ-NF-014, REQ-NF-015, REQ-NF-017 | - | - | - | DB-SCHEMA-BASE, DB-RLS-BASE | `src/lib/supabase/queries.ts`, `src/lib/supabase/client.ts` |
| 52 | DB-SEED-BASE | 로컬/개발용 시드 데이터 | Database | IMPLEMENT | - | - | - | - | DB-SCHEMA-BASE | `supabase/seed.sql` |

- Functional AC: 테이블은 정확히 6개로 제한한다(여행지·안전·대표 콘텐츠는 DB에 넣지 않고 §10 정적 데이터로 처리). `mate_posts`에 `safety_consent_at`(REQ-FUNC-080 동의 시각) 컬럼을 포함한다.
- Visual AC: 해당 없음.
- Security/Privacy AC: 6개 테이블 모두 RLS 활성화, 본인/요청 대상 작성자/Moderator·Admin만 비공개 행 열람. `DB-ACCESS`는 이메일·전화번호를 클라이언트 응답에서 select 단계부터 제외한다(REQ-FUNC-033). CSRF/SameSite·입력 검증은 Server Action 기본 보호+명시적 zod 스키마 검증으로 처리.
- Verify: TEST-RLS-BASIC
- Priority: P0(SCHEMA-BASE/RLS-BASE/ACCESS), P2(SEED-BASE)

---

## 12. Task List — API (5)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 53 | API-MATE-POSTS | 동행 모집글 CRUD+자동 마감 | API | IMPLEMENT | REQ-FUNC-030, REQ-FUNC-031, REQ-FUNC-037, REQ-FUNC-038, REQ-NF-005 | SCR-003, SCR-004 | `/travel-tools`, `/mates` | - | DB-ACCESS | `src/lib/actions/mate-posts.ts` |
| 54 | API-MATE-APPLICATIONS | 참가 요청 생성/승인/거절 | API | IMPLEMENT | REQ-FUNC-034, REQ-FUNC-035, REQ-FUNC-036, REQ-NF-005 | SCR-004 | `/mates` | - | DB-ACCESS, API-MATE-POSTS | `src/lib/actions/mate-applications.ts` |
| 55 | API-BLOCKS-REPORTS | 신고·차단 생성 및 Admin 처리 | API | IMPLEMENT | REQ-FUNC-039, REQ-FUNC-040, REQ-FUNC-041, REQ-FUNC-042, REQ-NF-019 | SCR-004, SCR-005 | `/mates`, `/account` | - | DB-ACCESS | `src/lib/actions/blocks-reports.ts` |
| 56 | API-AUTH-PROFILE | 이메일 인증/로그인/프로필/성인확인 | API | IMPLEMENT | REQ-FUNC-027, REQ-FUNC-028, REQ-FUNC-029, REQ-FUNC-033, REQ-FUNC-066 | SCR-003, SCR-005 | `/travel-tools`, `/account` | - | DB-ACCESS | `src/lib/actions/auth-profile.ts`, `src/app/auth/callback/route.ts` |
| 57 | API-ADMIN-SETTINGS | 외부 URL 허용목록 설정 | API | IMPLEMENT | REQ-FUNC-077 | SCR-005 | `/account` | - | DB-ACCESS | `src/lib/actions/admin-settings.ts` |

- Functional AC: 모든 쓰기는 Supabase Server Action을 통해서만 수행하고 클라이언트에서 직접 테이블을 쓰지 않는다. `API-MATE-POSTS`의 자동 마감은 별도 배치 없이 조회 시점에 `end_date` 경과 여부를 계산해 표시한다(REQ-FUNC-037).
- Visual AC: 해당 없음(서버 계층).
- Security/Privacy AC: `API-ADMIN-SETTINGS`는 HTTPS·허용목록 도메인만 저장하고 `http:`/`javascript:`/`data:` URL을 거부한다(REQ-FUNC-077). `API-AUTH-PROFILE`은 생년월일 원본을 저장하지 않는다(REQ-FUNC-028).
- Verify: TEST-RLS-BASIC, UNIT-MATE-STATE, E2E-MATE-AUTH
- Priority: P0

---

## 13. Task List — Unit Test (3)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 58 | UNIT-TRAVEL-DATES | 날짜 검증 유닛 테스트(출발/귀국, 체크인/체크아웃) | Unit Test | IMPLEMENT | REQ-FUNC-013, REQ-FUNC-021 | SCR-003 | `/travel-tools` | - | COMP-SCR003-FLIGHT-FORM, COMP-SCR003-HOTEL-FORM | `tests/unit/travel-dates.test.ts` |
| 59 | UNIT-CONTACT-DETECTION | 연락처 패턴 탐지 유닛 테스트 | Unit Test | IMPLEMENT | REQ-FUNC-032 | SCR-003 | `/travel-tools` | - | COMP-SCR003-MATE-WRITE-FORM | `tests/unit/contact-detection.test.ts` |
| 60 | UNIT-MATE-STATE | 동행 상태 전이 유닛 테스트(PENDING/ACCEPTED/REJECTED/CLOSED) | Unit Test | IMPLEMENT | REQ-FUNC-035, REQ-FUNC-036, REQ-FUNC-037, REQ-FUNC-038 | SCR-004 | `/mates` | - | API-MATE-POSTS, API-MATE-APPLICATIONS | `tests/unit/mate-state.test.ts` |

- Functional AC: 날짜 검증은 경계값(오늘, 당일 체크인/체크아웃, 역전 날짜)을 포함한다. 연락처 탐지는 기준 테스트셋에서 탐지율/오탐률을 기록만 하고(정량 KPI는 축소) 정규식 케이스를 유닛으로 고정한다. 상태 전이는 중복 요청 차단·비작성자 승인 거부·자동 마감 포함.
- Visual AC: 해당 없음.
- Security/Privacy AC: 해당 없음.
- Verify: CI-QUALITY-GATE
- Priority: P0

---

## 14. Task List — Integration Test (1)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 61 | TEST-RLS-BASIC | RLS 정책 기본 접근 테스트 | Integration Test | IMPLEMENT | REQ-FUNC-044, REQ-NF-013 | SCR-004, SCR-005 | `/mates`, `/account` | - | DB-RLS-BASE, DB-SEED-BASE | `tests/integration/rls-basic.test.ts` |

- Functional AC: 본인/타인/Moderator/Admin 4개 역할 조합으로 각 테이블 select/insert/update를 시도해 허용·거부가 설계대로 동작하는지 확인.
- Visual AC: 해당 없음.
- Security/Privacy AC: 비인가 접근이 전부 403 또는 빈 결과인지 확인.
- Verify: CI-QUALITY-GATE
- Priority: P0

---

## 15. Task List — E2E (3, Playwright Chromium 핵심 흐름 5~7개를 3개 Task로 묶음)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 62 | E2E-PUBLIC-SMOKE | 공개 흐름 Smoke(여행지 탐색·안전정보·대표소개) | E2E Test | IMPLEMENT | REQ-FUNC-001, REQ-FUNC-002, REQ-FUNC-003, REQ-FUNC-005, REQ-FUNC-006, REQ-FUNC-009, REQ-FUNC-047, REQ-FUNC-050, REQ-FUNC-051, REQ-FUNC-057, REQ-FUNC-059, REQ-FUNC-060, REQ-FUNC-063, REQ-NF-023, REQ-NF-025, REQ-NF-030 | SCR-001, SCR-002 | `/`, `/about` | - | PAGE-SCR001, PAGE-SCR002 | `tests/e2e/public-smoke.spec.ts` |
| 63 | E2E-TRAVEL-TOOLS | 항공·숙소 흐름 E2E | E2E Test | IMPLEMENT | REQ-FUNC-011, REQ-FUNC-012, REQ-FUNC-013, REQ-FUNC-014, REQ-FUNC-015, REQ-FUNC-016, REQ-FUNC-017, REQ-FUNC-018, REQ-FUNC-019, REQ-FUNC-020, REQ-FUNC-021, REQ-FUNC-022, REQ-FUNC-023, REQ-FUNC-024, REQ-FUNC-025, REQ-FUNC-026, REQ-FUNC-054 | SCR-003 | `/travel-tools` | - | PAGE-SCR003 | `tests/e2e/travel-tools.spec.ts` |
| 64 | E2E-MATE-AUTH | 로그인+동행 작성/참가 흐름 E2E | E2E Test | IMPLEMENT | REQ-FUNC-027, REQ-FUNC-028, REQ-FUNC-030, REQ-FUNC-031, REQ-FUNC-034, REQ-FUNC-035, REQ-FUNC-036, REQ-FUNC-039, REQ-FUNC-040, REQ-FUNC-066 | SCR-003, SCR-004, SCR-005 | `/travel-tools`, `/mates`, `/account` | - | PAGE-SCR003, PAGE-SCR004, PAGE-SCR005 | `tests/e2e/mate-auth.spec.ts` |

- Functional AC: `playwright.config.ts`는 `chromium` 프로젝트만 정의한다(firefox/webkit 프로젝트 없음). 3개 Task가 여행지 탐색, 안전정보 열람, 대표소개, 항공 이동, 숙소 이동, 동행 작성+로그인 유도, 참가 요청까지 핵심 5~7개 흐름을 커버한다.
- Visual AC: 각 흐름에서 Lorem ipsum·준비 중·빈 Card가 렌더링되지 않는지 텍스트 스냅샷으로 확인.
- Security/Privacy AC: 외부 이동 시 새 탭 URL에 목적지·날짜 쿼리가 없는지 확인(REQ-FUNC-016, REQ-FUNC-024).
- Verify: CI-QUALITY-GATE
- Priority: P0

---

## 16. Task List — Manual Check(브라우저 확인 필요) (3)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 65 | MANUAL-RESPONSIVE-DENSITY | Desktop 1440px/Mobile 390px 콘텐츠 밀도 육안 확인 | Manual Check | IMPLEMENT | REQ-FUNC-065 | SCR-001, SCR-003 | `/`, `/travel-tools` | - | PAGE-SCR001, PAGE-SCR003 | 없음(체크리스트만, `TASKS/checks/responsive-density.md`) |
| 66 | MANUAL-ACCESSIBILITY-KEYBOARD | 키보드 내비게이션·스크린리더 수동 점검 | Manual Check | IMPLEMENT | REQ-FUNC-079, REQ-NF-023, REQ-NF-025 | 전역 | 전체 | - | COMP-GLOBAL-HEADER-FOOTER | 없음(체크리스트만, `TASKS/checks/accessibility.md`) |
| 67 | MANUAL-PERFORMANCE-LIGHTHOUSE | Lighthouse 수동 측정(LCP/INP/CLS) | Manual Check | IMPLEMENT | REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-006 | 전역 | 전체 | - | PAGE-SCR001~005(배포 후) | 없음(측정 리포트만, `TASKS/checks/lighthouse.md`) |

- Functional AC: 자동 CI 게이트가 없는 항목(REQ-NF-007/024 EXCLUDED)을 사람이 배포 후 직접 확인하고 결과를 `TASKS/checks/*.md`에 기록한다.
- Visual AC: SCR-001/SCR-003 Card Grid가 Desktop 3열/Mobile 1열로 전환되는지, 빈 여백이 과도하지 않은지 스크린샷으로 확인.
- Security/Privacy AC: 해당 없음.
- Verify: 없음(Manual Check 자체가 검증 수단)
- Priority: P1

---

## 17. Task List — CI/Infra (2)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 68 | CI-QUALITY-GATE | TypeScript strict·ESLint·Playwright 병합 전 게이트 | CI/Infra | IMPLEMENT | REQ-NF-031 | 전역 | 전체 | - | UNIT-*, TEST-RLS-BASIC, E2E-* | `.github/workflows/ci.yml` 또는 동등 설정, `package.json`(scripts 추가) |
| 69 | RELEASE-CHECK-VERCEL-SUPABASE | Vercel 배포+Supabase 환경변수/TLS/비용 확인 | CI/Infra | IMPLEMENT | REQ-NF-012, REQ-NF-016, REQ-NF-034 | 전역 | 전체 | - | DB-SCHEMA-BASE, DB-RLS-BASE | `TASKS/checks/release-vercel-supabase.md` |

- Functional AC: CI는 `tsc --noEmit`, `eslint`, `playwright test --project=chromium`을 병합 전 필수로 실행한다. EC2·AWS 인프라, 자동 Merge Runner는 만들지 않는다.
- Visual AC: 해당 없음.
- Security/Privacy AC: 비밀키는 Vercel/GitHub Actions 환경변수로만 관리하고 클라이언트 번들에 포함되지 않는지 빌드 산출물로 확인. HTTPS(TLS 1.2+)는 Vercel 기본값 확인.
- Verify: CI 실행 로그
- Priority: P0(CI-QUALITY-GATE), P1(RELEASE-CHECK)

---

## 18. Requirement 커버리지 자가 검증

### 18.1 REQ-FUNC (IMPLEMENT 72개 — 001~044, 046~054, 057~070, 074, 077~080)

모두 위 표에 최소 1회 이상 등장한다. 대표적으로: 001→DATA-DESTINATIONS/COMP-SCR001-DOMESTIC-GRID·OVERSEAS-GRID, 017→COMP-SCR003-FLIGHT-FORM/DB-ACCESS, 033→COMP-SCR004-POST-LIST/DB-ACCESS, 044→DB-RLS-BASE/TEST-RLS-BASIC, 070→PAGE-SCR001~005, 077→COMP-SCR005-ADMIN-URL-SETTINGS/API-ADMIN-SETTINGS.

### 18.2 REQ-NF (IMPLEMENT 21개 — 001~006, 012~017, 019, 023, 025~028, 030, 031, 034)

모두 위 표에 최소 1회 이상 등장한다: 001~003→PAGE-SCR001~005/MANUAL-PERFORMANCE-LIGHTHOUSE, 004→COMP-SCR001-HERO-SEARCH·COMP-SCR004-FILTER-BAR, 005→API-*(3개), 006→COMP-GLOBAL-DESIGN-TOKENS/DATA-DESTINATIONS, 012→RELEASE-CHECK-VERCEL-SUPABASE, 013→DB-RLS-BASE/TEST-RLS-BASIC, 014·015→DB-ACCESS, 016→RELEASE-CHECK-VERCEL-SUPABASE, 017→COMP-SCR003-FLIGHT-FORM·HOTEL-FORM/DB-ACCESS, 019→API-BLOCKS-REPORTS, 023·025→MANUAL-ACCESSIBILITY-KEYBOARD, 026→DATA-DESTINATIONS/DATA-VALIDATION-SCRIPT, 027→DATA-SAFETY/DATA-VALIDATION-SCRIPT, 028→COMP-SCR001-SAFETY-PANEL/DATA-VALIDATION-SCRIPT, 030→PAGE-SCR001~005, 031→CI-QUALITY-GATE, 034→RELEASE-CHECK-VERCEL-SUPABASE.

### 18.3 EXCLUDED 21개

`§1 NON_IMPLEMENTATION` 표에 21개 전부 기록됨(REQ-FUNC-045, REQ-FUNC-055, REQ-FUNC-056, REQ-FUNC-071, REQ-FUNC-072, REQ-FUNC-073, REQ-FUNC-075, REQ-FUNC-076 / REQ-NF-007, REQ-NF-008, REQ-NF-009, REQ-NF-010, REQ-NF-011, REQ-NF-018, REQ-NF-020, REQ-NF-021, REQ-NF-022, REQ-NF-024, REQ-NF-029, REQ-NF-032, REQ-NF-033).

### 18.4 결론

93(IMPLEMENT) + 21(EXCLUDED) = **114**. `docs/UIUX_TRACEABILITY.md`의 114개와 정확히 일치하며, 빠진 Requirement ID는 없다. 이 문서를 완료로 보고한다.
