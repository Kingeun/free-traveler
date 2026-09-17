# UI Contract — Free Traveler (Next.js App Router)

**기반 문서:** `docs/03_UI_COVERAGE_ANALYSIS.md`, `docs/04_UIUX_PLAN.md`, `docs/STITCH_VALIDATION_REPORT.md`, `design-reference/D-001/DESIGN.md`
**대상:** 승인된 5개 Screen(SCR-001~005)을 Next.js App Router 구현 계약으로 변환
**현재 `src/app` 상태:** `layout.tsx`, `page.tsx`, `globals.css`, `favicon.ico`만 존재(create-next-app 기본 스캐폴드). 다른 4개 라우트 디렉터리는 아직 없음.

**화면 구분(핵심 4 · 보조 1):** `docs/PROJECT_SCOPE.md`가 대표소개를 원래 "보조 화면 1개"로 정의했던 것을 그대로 계승해 SCR-002(`/about`)를 **보조**로 분류한다. 나머지 4개(SCR-001, SCR-003, SCR-004, SCR-005)는 검색·여행 준비·동행·계정이라는 서비스의 필수 경로이므로 **핵심**으로 분류한다.

---

## SCR-001 — 메인 (핵심)

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-001 |
| **Route** | `/` |
| **Page Entry** | `src/app/page.tsx` |
| **영역 순서** | Header → ①검색 Hero → ②국내 인기 여행지(Card×6) → ③해외 인기 여행지(Card×6) → ④여행 동기·테마(Chip×6) → ⑤국가별 주의사항(Card×6) → ⑥최근 동행글(Card×3 또는 완성형 Empty State) → ⑦free_traveler 요약(좌우 분할+CTA) → Footer |
| **주요 Component** | Header/Footer(공통), 검색 Search bar(pill, 키워드 전용, 날짜·인원 필드 금지), Destination Card×12, Theme Chip 목록, 안전정보 Card(텍스트 배지), 여행지 상세 Drawer, 안전정보 상세 Drawer/Modal, Empty State block, 대표 소개 좌우 분할 밴드 |
| **상태** | Loading(카드 스켈레톤) · Success · Empty(필터 결과 없음 → 조건 완화 안내+초기화 / 동행글 없음 → 완성형 Empty State) · Error(여행지·안전정보 로드 실패 → 재시도) |
| **사용자 행동** | 키워드 검색, 국내/해외 필터 선택, 여행지 Card 선택→상세 Drawer 오픈, 즐겨찾기 등록/해제(localStorage), 테마 Chip 선택→필터 적용 스크롤, 국가 안전 Card 선택→안전 Drawer 오픈, 동행 CTA/대표소개 CTA 클릭 |
| **다른 화면으로의 이동** | `/travel-tools`(Hero CTA, 동행 Empty State CTA) · `/mates`(동행 섹션 "모두 보기") · `/about`(대표 소개 밴드 CTA) · `/account`(비로그인 상태에서 참가·작성류 액션 시 로그인 유도) |
| **Desktop·Mobile 규칙** | Desktop 1440px 기준(콘텐츠 최대 폭 1200–1280px, Section 여백 64–96px) + **Mobile 390px 변형 승인**(Card Grid 3열→1열, Section 여백 40–64px, Chip 가로 스크롤, Hero는 다음 Section 제목이 폴드 안에 보이도록 높이 제한) |
| **금지 기능** | 별점/리뷰 점수(Stitch 검증에서 실제 발견 후 제거된 위반), 실시간 가격, Airbnb 상표 요소, 날짜·인원이 결합된 예약형 검색 위젯, 광고 배너, Lorem ipsum/`준비 중`/`정보 확인 필요`, 의미 없는 빈 Card |

---

## SCR-002 — 대표 소개 (보조)

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-002 |
| **Route** | `/about` |
| **Page Entry** | `src/app/about/page.tsx` |
| **영역 순서** | Header → ①Hero(대표 사진+소개 문장) → ②여행 지표(50+ Trips/30+ Countries) → ③소개·철학(좌우 분할, 2~4 문단) → ④여행 Timeline(6개 이상 시점) → ⑤방문 국가(30개, 권역별 Chip/목록) → ⑥Gallery(사진 8장 이상, 실제 지명 캡션) → ⑦기억에 남는 여행지(Card×4)+CTA → Footer |
| **주요 Component** | Hero, Stat Pill×2, 좌우 분할 소개 블록, Step형 세로 Timeline, 권역별 Chip 그룹, Photo Gallery Grid, Destination Card×4, CTA Banner(2버튼: 항공·숙소 준비하기/동행 찾기) |
| **상태** | Loading(이미지 지연 로딩) · Success · Error(이미지 로드 실패 → 대체 이미지). Empty·Unauthorized 없음(정적 콘텐츠 상시 존재) |
| **사용자 행동** | Timeline·Gallery 열람, 방문국가 Chip 선택→SCR-001 관련 여행지 필터 이동, 추천 여행지 Card 선택→SCR-001 상세 Drawer, CTA 버튼 클릭 |
| **다른 화면으로의 이동** | `/`(추천 여행지 Card, 방문국가 Chip) · `/travel-tools`("항공·숙소 준비하기" CTA) · `/mates`("동행 찾기" CTA) |
| **Desktop·Mobile 규칙** | Desktop 1440px만 승인. Mobile 변형은 이번 범위에 포함되지 않음(반응형 최소 대응은 하되 별도 "Mobile 변형 Screen"으로 검증되지 않음) |
| **금지 기능** | 별점, 가격, Airbnb 상표 요소, 의미 없는 Gallery 캡션(실제 지명 alt 필수), 빈 Card, Lorem ipsum/`준비 중` |

---

## SCR-003 — 통합 여행 준비 (핵심)

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-003 |
| **Route** | `/travel-tools` |
| **Page Entry** | `src/app/travel-tools/page.tsx` |
| **영역 순서** | Header → ①Intro(3단계 안내) → ②탭(항공편 찾기/숙소 찾기/동행 구하기) → ③조건 입력 Form → ④요약+외부 이동 Action Card(좌우 분할) → ⑤비전달 고지+Tip(Chip×3) → ⑥동행 탭(로그인 안내 카드+안전 안내 박스, 또는 인증 회원의 작성 Form) → Footer |
| **주요 Component** | 3-Step Guide, Tab(세그먼트 컨트롤, 탭별 입력 상태 독립 유지), 조건 Form(국가/지역/출발일/귀국일), Summary+Action Card(2분할), Tip Chip×3, Login Gate Card+Safety Notice Box, 동행 모집글 작성 Form(인증 시) |
| **상태** | Success(요약 완료/외부 이동 성공) · Error(날짜·필수값 검증 실패, 연락처 패턴 탐지, 외부 URL 오류) · Unauthorized(동행 탭 비로그인/성인 미인증). Loading 없음(클라이언트 즉시 처리), Empty 없음 |
| **사용자 행동** | 탭 전환(다른 탭 입력값 유지), 조건 입력·검증, 요약 확인, 외부 사이트로 이동(새 탭, `noopener,noreferrer`, query 없음), 동행 모집글 작성(인증 시) 또는 로그인 유도 확인 |
| **다른 화면으로의 이동** | 외부 파트너 사이트(Google Flights/Booking류, 새 탭, Screen 아님) · `/account`(동행 탭 비로그인/미인증 시 로그인 유도) · `/mates`(모집글 작성 완료 후) |
| **Desktop·Mobile 규칙** | Desktop 1440px + **Mobile 390px 변형 승인**. Mobile은 탭이 가로 스크롤 세그먼트, Form 필드 전체 stacked, Summary+Action Card 세로 스택 |
| **금지 기능** | 실시간 항공권·호텔 가격 표시(Stitch 검증에서 "인기 비교 노선" 카드에 실가격 노출 발견 → 반드시 제거), 좌석 등급·인원수 등 과도한 예약형 UI 확장, 동행 로그인 안내 섹션 중복 배치(Stitch 검증에서 실제 발견), 입력값을 서버 API·DB·로그·분석에 저장, 목적지·날짜를 외부 URL 쿼리에 포함 |

---

## SCR-004 — 동행 조회 (핵심)

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-004 |
| **Route** | `/mates` |
| **Page Entry** | `src/app/mates/page.tsx` |
| **영역 순서** | Header → ①Intro+작성 CTA → ②Filter(국가/지역/기간/연령대/성별/스타일/모집상태)+결과 요약 → ③동행글 목록(최대 8 Card 우선 노출) → ④목록+상세(Desktop 좌우 분할/Mobile 상세 Drawer) → ⑤신청 방법 3단계 안내 → ⑥안전·신고·차단 안내+CTA → Footer |
| **주요 Component** | Filter Chip/Dropdown Bar+결과 카운트, Mate Post Card(최대 8), List+Detail Split(Desktop) / Detail Drawer(Mobile 대응 시), 참가 요청 Form(500자 이내 textarea), 3-Step Guide, Safety Notice Box+CTA, 검색 결과 없음 Empty State |
| **상태** | Loading(목록 스켈레톤) · Success · Empty(검색 결과 없음 → 필터 초기화+작성 CTA+이용 방법) · Error(참가 요청/신고/차단 처리 실패) · Unauthorized(비로그인 참가 요청·작성 시도) |
| **사용자 행동** | Filter 적용/초기화, 목록 Card 선택→상세 열람, 참가 요청 전송, (작성자) 요청 승인/거절, 모집글 수동 마감/수정/삭제, 신고·차단 |
| **다른 화면으로의 이동** | `/travel-tools`(작성 CTA → 동행 구하기 탭) · `/account`(비로그인 시 로그인 유도, 내 활동에서 재진입) |
| **Desktop·Mobile 규칙** | Desktop 1440px 목록+상세 2분할 중심으로 승인. **이번 범위에서 Mobile 변형 Screen은 승인 대상이 아님**(반응형 최소 대응은 하되 별도 Mobile Screen 검증 없음) |
| **금지 기능** | 별점, 가격, "매너온도"/"본인인증 완료" 외의 숫자 평점·리뷰 점수, 전화번호·이메일 등 공개 연락처 노출, Dashboard/통계성 레이아웃 |

---

## SCR-005 — 계정·관리 (핵심)

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-005 |
| **Route** | `/account` |
| **Page Entry** | `src/app/account/page.tsx` |
| **영역 순서(역할별, 없는 탭은 렌더링하지 않음)** | **Guest:** 계정 Intro → 로그인/가입/비밀번호 재설정 Card → 로그인 후 가능한 기능 안내 → 보안 안내. **Member:** 프로필·성인 확인 요약 → 내 글 → 참가 요청 → 차단 목록 → 즐겨찾기 목록 → 새 동행글 작성 CTA. **Admin:** 관리 Intro → 신고 상태 변경(+대상 글 숨김) → 항공·숙소 외부 URL 설정 |
| **주요 Component** | Auth Form(로그인/가입/재설정), 성인 확인 체크박스, 프로필 Form, 목록형 Card(내 글/참가요청/차단/즐겨찾기), 목록별 Empty State, 관리자 신고 큐 Filter+목록, 외부 URL 설정 Form |
| **상태** | Loading · Success · Empty(내 글·참가요청·차단·즐겨찾기·신고 큐 없음 → 설명+다음 행동 CTA) · Error(로그인 실패, 외부 URL 허용목록 위반) · Unauthorized(Guest가 Member/Admin 전용 탭에 접근 시 해당 탭 자체를 렌더링하지 않음) |
| **사용자 행동** | 로그인/가입/비밀번호 재설정, 성인 인증, 프로필 수정, 내 글/참가 요청 관리, 즐겨찾기 목록에서 여행지로 이동, 차단 해제, (Admin) 신고 상태 변경·외부 URL 저장 |
| **다른 화면으로의 이동** | `/mates`(내 글/참가 요청 Card 선택 시 상세) · `/`(즐겨찾기 Card 선택 시 상세 Drawer) · `/travel-tools`(새 동행글 작성 CTA) |
| **Desktop·Mobile 규칙** | Desktop 1440px만 승인. Mobile 변형은 이번 범위에 포함되지 않음 |
| **금지 기능** | Dashboard/통계 화면(명시적 금지, `04_UIUX_PLAN.md` §7), 역할에 없는 탭 렌더링, 관리자 범위를 신고 상태·외부 URL 설정 이외(콘텐츠 CRUD, 범용 감사 로그 등 `PROJECT_SCOPE.md` EXCLUDED 항목)로 확장 |

---

## 기술 Route (Screen 수에 미포함)

`04_UIUX_PLAN.md` §3.1 기준, 디자인 Screen으로 세지 않는 경로:

| 기술 Route | 성격 | 비고 |
|---|---|---|
| 인증 콜백 | Supabase Auth 리다이렉트 처리 전용 | Route Handler, 화면 없음 |
| API Route(`/api/**`) | 서버 응답 전용 | 화면 없음 |
| `not-found`(404) | 오류 처리 전용 | 복구 행동(홈/이전/재시도) 최소 1개 필요 |
| 이용약관/개인정보처리방침/동행 안전수칙/콘텐츠 면책 | 정적 정책 콘텐츠 | 동의 UI 자체는 SCR-003 동행 작성 Form 안에 위치 |

세부 매핑은 `design-reference/SCREEN_ROUTE_CONTRACT.json`의 `technical_routes`를 참조한다.
