# UI·UX Plan — Free Traveler MVP

**Document ID:** UIUX-TRAVEL-001
**기반 문서:** `docs/01_PRD.md`(현재 비어 있음, 참고 불가), `docs/02_SRS_BASELINE.md`, `docs/PROJECT_SCOPE.md`, `docs/03_UI_COVERAGE_ANALYSIS.md`, `design-reference/vendor/airbnb/DESIGN.md`(참고용, 상표 요소 미사용)
**대상 Screen:** SCR-001 `/`, SCR-002 `/about`, SCR-003 `/travel-tools`, SCR-004 `/mates`, SCR-005 `/account`

---

## 1. 목적

`docs/03_UI_COVERAGE_ANALYSIS.md`에서 확정한 5개 디자인 Screen과 요구사항 배치를 기반으로, Free Traveler의 공통 디자인 시스템과 화면별 Section 구성·상태·콘텐츠 원칙을 정의한다. Airbnb 참고본(`DESIGN.md`)은 레이아웃 밀도·카드 구조 등 구조적 아이디어를 참고하는 용도로만 사용하며, Rausch 컬러명·Cereal 서체·3-Product 내비게이션·"NEW" 배지 같은 Airbnb 고유 상표 요소는 그대로 가져오지 않는다.

---

## 2. 공통 디자인 시스템

### 2.1 브랜드와 참고 범위

| 항목 | 내용 |
|---|---|
| 브랜드명 | Free Traveler |
| Airbnb 참고 범위 | 사진 중심 카드, 넓은 여백의 섹션 리듬, 카드 hover 시 1단계 그림자, pill 형태 필터 Chip 등 **구조적 패턴만** 참고 |
| Airbnb 상표 요소 배제 | Rausch(#ff385c) 컬러명·Cereal 서체·Homes/Experiences/Services 3-Product 내비게이션·"NEW" 배지·Luxe/Plus 서브브랜드는 사용하지 않음 |

### 2.2 컬러

| 토큰 | 값 | 용도 |
|---|---|---|
| `color.canvas` | `#FFFFFF` | 전체 배경(흰 배경) |
| `color.surface-soft` | `#F7F6F4` | 섹션 배경 구분(연속된 Card Grid 톤 분리용) |
| `color.surface-strong` | `#EFEDEA` | 비활성 필드, Chip 기본 배경 |
| `color.ink` | `#2B2E33` | 짙은 회색 본문·제목 텍스트(순검정 미사용) |
| `color.body` | `#4A4E54` | 본문 보조 텍스트 |
| `color.muted` | `#6B7078` | 캡션, 부가 정보 |
| `color.hairline` | `#E2E0DD` | 1px 구분선 |
| `color.border-strong` | `#C7C4C0` | 포커스 아닌 입력 아웃라인 강조 |
| `color.primary` (코랄) | `#FF6F59` | 주요 CTA, 강조 포인트, 선택된 Chip |
| `color.primary-active` | `#E6543F` | CTA press 상태 |
| `color.primary-disabled` | `#FFD9CE` | 비활성 CTA |
| `color.on-primary` | `#FFFFFF` | 코랄 위 텍스트 |
| `color.success` | `#2E8B57` | 안전정보 최신 배지, 성공 메시지 |
| `color.warning` | `#B25E00` | 재확인 필요(stale), 일반 경고 — 코랄과 명확히 구분되는 호박색 계열 |
| `color.danger` | `#C6362E` | 폼 오류, 여행금지/출국권고 등 중대 경보 텍스트 |
| `color.focus-ring` | `#1F6FEB` | 키보드 포커스 링(본문 코랄·경고색과 겹치지 않는 파란색 계열) |

> 오류(danger)·경고(warning)·안전정보 배지는 코랄(primary)과 색상 자체가 다르며, 색상만으로 의미를 전달하지 않고 아이콘과 텍스트 라벨을 항상 함께 표기한다(REQ-FUNC-051 대응).

### 2.3 타이포그래피

- 폰트 스택: `'Inter', 'Apple SD Gothic Neo', 'Malgun Gothic', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- 한글 본문은 Inter가 커버하지 못하므로 시스템 한글 폰트(Apple SD Gothic Neo / Malgun Gothic)로 즉시 대체된다.

| 토큰 | 크기 | 굵기 | 줄간격 | 용도 |
|---|---:|---:|---:|---|
| `type.display-xl` | 36px | 700 | 1.3 | SCR-001/002 Hero 제목 |
| `type.display-lg` | 28px | 700 | 1.35 | Section 제목 |
| `type.display-md` | 22px | 600 | 1.4 | 카드 그룹 부제, 상세 Drawer 제목 |
| `type.title-md` | 18px | 600 | 1.45 | 카드 제목, 폼 라벨 그룹 제목 |
| `type.body-md` | 16px | 400 | 1.6 | 본문, 설명 문단 |
| `type.body-sm` | 14px | 400 | 1.55 | 카드 메타, 캡션 |
| `type.caption` | 13px | 500 | 1.4 | 배지, 상태 라벨 |
| `type.button` | 16px | 600 | 1.3 | 버튼 라벨 |

### 2.4 Spacing·Radius·Elevation

| 토큰 | 값 |
|---|---|
| `space.xs` / `sm` / `md` / `base` / `lg` / `xl` | 4 / 8 / 12 / 16 / 24 / 32px |
| `space.section-desktop` | 64~96px (Section 상하 여백, Desktop) |
| `space.section-mobile` | 40~64px (Section 상하 여백, Mobile) |
| `radius.sm` / `md` / `lg` / `full` | 8 / 12 / 16px / 9999px(Chip·아바타) |
| `elevation.card-hover` | `0 1px 2px rgba(0,0,0,.04), 0 4px 10px rgba(0,0,0,.08)` — 카드 hover/상세 Drawer 1단계만 사용 |

### 2.5 Breakpoint 기준

| 기준 | 폭 | 비고 |
|---|---:|---|
| **Desktop 기준** | **1440px** | 콘텐츠 최대 폭 1200~1280px, 좌우 여백은 나머지를 흡수 |
| Tablet | 744~1023px | Card Grid 열 수만 축소(4→2), 좌우 분할은 유지하되 비율 조정 |
| **Mobile 기준** | **390px** | Card 1열, Section 상하 여백 축소(40~64px), 좌우 분할은 세로 스택으로 전환 |

### 2.6 접근성

- 모든 인터랙티브 요소는 키보드 포커스 시 `color.focus-ring`으로 2px 아웃라인 표시(별도 outline-offset 2px).
- 버튼·Chip·아이콘 버튼의 최소 터치 영역은 44×44px 이상(시각적 크기가 작아도 히트 영역으로 확보).
- 색상 대비 AA 이상, 경보·오류는 아이콘+텍스트 병기.

### 2.7 공통 컴포넌트 — Header / Footer (5개 Screen 공통)

**Header**
- Desktop(1440px): 좌측 "Free Traveler" 워드마크(SCR-001로 이동) · 중앙 내비게이션(여행지, 여행 도구, 동행, 대표소개) · 우측 계정 영역(비로그인: 로그인 버튼 / 로그인: 아바타+닉네임, 클릭 시 SCR-005 이동)
- Mobile(390px): 좌측 워드마크 · 우측 햄버거 버튼(전체화면 내비게이션 시트로 전환), 계정 영역은 시트 하단에 노출
- 높이: Desktop 72px, Mobile 56px. 하단 1px hairline.

**Footer**
- 3컬럼(Desktop) → 1컬럼 누적(Mobile): ①서비스(여행지, 여행 도구, 동행, 대표소개) ②정책(이용약관, 개인정보 처리방침, 동행 안전수칙, 콘텐츠 면책 안내) ③문의(대표 연락처/SNS — REQ-FUNC-062 데이터 재사용)
- 하단 레거시 밴드: 저작권 문구, "안전정보 등 콘텐츠는 참고용이며 출국 전 공식 출처 재확인이 필요합니다" 공통 고지(REQ-FUNC-054 관련)

### 2.8 Section 배치 공통 규칙

- 모든 화면은 Header–Footer 사이에 목적이 분명한 Section을 순서대로 배치하고, 각 Section은 제목·1~3문장 설명·실제 콘텐츠 또는 CTA를 포함한다.
- 같은 화면 안에서 Hero, Card Grid, 좌우 분할, Chip 목록, 3단계 안내, CTA Banner를 교차 사용해 시각적 리듬을 만든다. 인접한 Card Grid가 불가피한 경우(예: 국내/해외 여행지) 사진 비중·배지 종류·배경 톤을 달리해 반복감을 줄인다.
- Lorem ipsum, "준비 중", "정보 확인 필요" 같은 모호한 문구를 쓰지 않는다. 데이터가 없는 상태에도 안내 문장 + 이용 방법 + 다음 행동 CTA를 함께 표시한다(EmptyState 원칙).
- 아래 화면별 표의 "제목(안)"과 "설명(안)"은 실제 게시 가능한 완성된 한국어 문장으로 작성했다.

---

## 3. SCR-001 `/` 메인 (7 Section)

| # | Section | 패턴 | 제목(안) | 설명(안) | 핵심 콘텐츠 | 상태 | 이동/CTA | 관련 REQ |
|---|---|---|---|---|---|---|---|---|
| 1 | 검색 Hero | Hero | 다음 여행지를 자유롭게 찾아보세요 | 국내외 인기 여행지를 검색하고, 항공·숙소 준비부터 동행까지 한 곳에서 시작하세요. | 여행지·국가·테마 검색창, 인기 검색어 Chip 3~4개, "여행 준비 시작하기" 버튼 | Success / Loading(검색창은 즉시 노출, 목록만 스켈레톤) | `/travel-tools` | FUNC-003, 064, 067 |
| 2 | 국내 인기 여행지 | Card Grid | 국내에서 지금 가장 인기 있는 여행지 | 제주, 부산, 강릉 등 국내 대표 여행지를 모았습니다. 카드를 선택하면 상세 정보를 바로 확인할 수 있습니다. | 6개 Card(사진, 지역명, 테마 Chip 1~2개, 추천 계절) | Success / Loading(스켈레톤) / Error(재시도 버튼) | 카드 선택 → 같은 화면 상세 Drawer | FUNC-001, 002, 007, 009 |
| 3 | 해외 인기 여행지 | Card Grid(사진 비중↑, 배경 톤 구분) | 해외에서 지금 가장 인기 있는 여행지 | 15개국 이상의 대표 도시를 모았습니다. 국가 배지를 선택하면 안전정보도 함께 확인할 수 있습니다. | 6개 Card(사진, 도시·국가명, 국가 안전 배지) | Success / Loading / Error | 카드 선택 → 상세 Drawer, 국가 배지 → 안전정보 Drawer | FUNC-001, 002, 006, 007 |
| 4 | 여행 동기·테마 | Chip 목록 | 어떤 여행을 떠나고 싶으신가요 | 휴양, 미식, 액티비티 등 테마별로 여행지를 빠르게 좁혀보세요. | 테마 Chip 6개(휴양/도심 탐방/자연·트레킹/미식/액티비티/문화유산) | Success | Chip 선택 → 필터 적용된 목록으로 스크롤 | FUNC-002, 010 |
| 5 | 국가별 주의사항 | Card Grid(안전정보 Drawer 연결) | 떠나기 전 꼭 확인할 국가별 안전정보 | 외교부 공식 정보를 기준으로 치안, 사기, 재난 등 주요 안전 항목을 정리했습니다. 최종 확인일도 함께 표시됩니다. | 6개 국가 Card(국가명, 경보 단계 배지, 최종 확인일/재확인 필요 배지) | Success / Warning(stale 배지) / Error | 카드 선택 → 안전정보 Drawer | FUNC-006, 046~054(대표 047·048·050·051) |
| 6 | 최근 동행글 | Card Grid / Empty State | 지금 함께 떠날 동행을 찾고 있어요 | 최근 등록된 동행 모집글입니다. 원하는 여행 스타일의 동행을 찾아보세요. | Success: 최대 3개 Card(제목, 국가/기간, 모집 인원, 모집중 배지) · Empty: "아직 등록된 동행글이 없어요" + 이용 방법 3줄(조건 입력→모집글 작성→참가자 승인) + "동행 모집글 작성하기" CTA | Success / Empty | `/mates` (모두 보기), Empty 시 `/travel-tools` 동행 탭 | FUNC-030, 031, 037 |
| 7 | free_traveler 요약 | 좌우 분할 + CTA Banner | 50번의 여행, 30개국의 기록을 나눠드립니다 | 여행 대표 free_traveler가 직접 경험한 여행 이야기를 만나보세요. | 좌: 대표 사진+한 줄 소개, 우: "50+ Trips"·"30+ Countries" 지표 + "대표 소개 보기" CTA | Success | `/about` | FUNC-057, 063 |

- Drawer 상세(REQ-FUNC-004, 007, 009, 047~054)는 Section 2·3·5 카드 클릭 시 동일 화면 위에 열리며, 여행지 상세 Drawer에는 관련 여행지 최대 6개와 안전정보 진입 링크가 포함된다.
- 필터·검색 상태는 URL query로 동기화되어 새로고침·공유 시 복원된다(FUNC-010).

---

## 4. SCR-002 `/about` 대표 소개 (7 Section)

| # | Section | 패턴 | 제목(안) | 설명(안) | 핵심 콘텐츠 | 상태 | 이동/CTA | 관련 REQ |
|---|---|---|---|---|---|---|---|---|
| 1 | 대표 Hero | Hero | 50번의 여행 끝에 만난, 진짜 여행 이야기 | free_traveler는 지난 여행에서 30개국 이상을 다니며 얻은 경험을 이 사이트에 담았습니다. | 대표 사진(실제 여행지 촬영), 한 줄 소개 문장 | Success / Error(이미지 로드 실패 시 대체 이미지) | - | FUNC-057, 058 |
| 2 | 여행 지표 | 좌우 분할(지표 2~3단) | 숫자로 보는 free_traveler의 여행 | 지금까지의 여행 기록을 숫자로 정리했습니다. | "50+ Trips", "30+ Countries" 지표 카드 | Success | - | FUNC-057 |
| 3 | 소개 | 좌우 분할(텍스트+사진) | 여행을 시작한 이유 | 자기소개, 여행을 시작한 계기, 여행 철학, 콘텐츠 편집 원칙을 담은 2~4개 문단 | 문단형 텍스트 + 보조 사진 | Success | - | FUNC-058 |
| 4 | 여행 Timeline | 3단계 안내(확장형 세로 타임라인) | 연도별로 보는 여행 발자취 | 2018년부터 지금까지의 주요 여행 기록입니다. | 6개 이상 시점(연도·장소·한 줄 요약) | Success | - | FUNC-060 |
| 5 | 방문 국가 | Chip 목록(권역별 그룹) | 지금까지 다녀온 30개국 | 권역별로 정리했습니다. 국가명을 누르면 관련 여행지를 확인할 수 있어요. | 권역(아시아/유럽/아메리카/오세아니아 등)별 국가 Chip | Success | Chip 선택 → SCR-001 관련 여행지 필터 | FUNC-059 |
| 6 | 여행 Gallery | Card Grid(Photo Gallery) | 카메라에 담은 여행의 순간들 | 서로 다른 나라에서 찍은 사진 8장을 모았습니다. | 8장 이상 사진 Grid, 각 사진에 촬영 장소를 설명하는 alt(예: "페루 마추픽추 전망대에서 바라본 유적지 전경") | Success | - | FUNC-061 |
| 7 | 기억에 남는 여행지 | Card Grid + CTA Banner | 가장 기억에 남는 여행지 4곳 | free_traveler가 직접 추천하는 여행지입니다. 지금 바로 준비를 시작해보세요. | 4개 Card(→SCR-001 상세 Drawer), "항공·숙소 준비하기"/"동행 찾기" CTA | Success | `/travel-tools`, `/mates` | FUNC-063 |

---

## 5. SCR-003 `/travel-tools` 통합 여행 준비 (6 Section, 3탭)

3탭(항공편 찾기 / 숙소 찾기 / 동행 구하기)은 입력·검증·완료 상태를 서로 완전히 분리해 관리하며, 탭 전환 시 다른 탭에 입력한 값은 유지된다.

| # | Section | 패턴 | 제목(안) | 설명(안) | 핵심 콘텐츠 | 상태 | 관련 REQ |
|---|---|---|---|---|---|---|---|
| 1 | Intro | 3단계 안내 | 여행 준비, 이 페이지에서 한 번에 | 항공권과 숙소 조건을 입력해 요약을 확인한 뒤 외부 사이트로 이동하고, 함께 갈 동행도 구할 수 있습니다. | 이용 순서: ①조건 입력 ②요약 확인 ③외부 이동 또는 모집글 등록 | Success | FUNC-015, 017, 023, 025 |
| 2 | 탭 | 탭(세그먼트 컨트롤) | - | - | "항공편 찾기" · "숙소 찾기" · "동행 구하기" | Success | (구조 요소) |
| 3 | 조건 입력 Form | Form | 조건을 입력해주세요 | 국가와 지역, 일정을 입력하면 바로 요약을 확인할 수 있습니다. | 항공: 국가/지역/출발일/귀국일 · 숙소: 국가/지역/체크인/체크아웃 · 동행: 제목/국가/지역/기간/인원/스타일/설명/안전수칙 동의 | Success / Error(날짜 역전·필수값 누락 시 인라인 오류) | FUNC-011~013, 019~021, 031~032 |
| 4 | 요약 + 외부 이동 Action Card (항공/숙소 탭) | 좌우 분할 | 입력하신 조건을 확인해주세요 | 국가·지역·기간을 다시 확인한 뒤 외부 사이트로 이동합니다. | 좌: 요약 카드, 우: "Google Flights에서 항공권 보기" / "Booking.com에서 숙소 보기" Action Card | Success / Error(외부 URL 오류 시 재시도 안내) | FUNC-014, 016, 018, 022, 024, 026 |
| 5 | 비전달 고지 + Tip | Chip 목록 | 입력값은 외부로 전달되지 않아요 | 브라우저에서만 처리되며 서버에 저장하지 않습니다. 아래 팁으로 더 좋은 조건을 찾아보세요. | 고지 문구 + Tip 3개(예: "출발 3~4주 전 예약이 비교적 저렴해요", "평일 출발이 저렴한 편이에요", "성수기는 미리 일정을 확인하세요") | Success | FUNC-015, 017, 023, 025 |
| 6 | 동행 탭 하단 — 로그인 안내 또는 작성 폼 + 안전 안내 | CTA Banner(Unauthorized) / Form(작성 완료) | 동행을 모집하려면 로그인이 필요해요 | 성인 인증을 완료한 회원만 동행 모집글을 작성할 수 있습니다. | 비로그인: 로그인 유도 CTA · 로그인 후: Section 3 작성 폼 활성화 + "안전한 동행을 위한 안내"(공개 연락처 금지, 신고·차단 안내) | Unauthorized / Success | FUNC-027, 028, 032, 080 |

---

## 6. SCR-004 `/mates` 동행 조회 (6 Section)

| # | Section | 패턴 | 제목(안) | 설명(안) | 핵심 콘텐츠 | 상태 | 관련 REQ |
|---|---|---|---|---|---|---|---|
| 1 | Intro | CTA Banner | 함께 떠날 동행을 찾아보세요 | 여행 스타일이 맞는 동행을 찾고, 원하는 조건의 모집글이 없다면 직접 등록해보세요. | "동행 모집글 작성하기" CTA | Success | FUNC-031 (진입) |
| 2 | 검색 Filter | Chip 목록(Filter) | - | 국가, 지역, 기간, 연령대, 성별, 여행 스타일, 모집 상태로 좁혀보세요. | Filter Chip/드롭다운 + 결과 요약("총 12개의 모집글") | Success | FUNC-030 |
| 3 | 동행글 목록 | Card Grid | - | - | 최대 8개 우선 노출 Card(제목, 국가/기간, 모집 인원, 모집중/마감 배지) | Success / Empty | FUNC-030, 037 |
| 4 | 목록+상세 | 좌우 분할(Desktop) / Drawer(Mobile) | - | - | 좌: 목록, 우: 상세 패널(작성자 정보, 설명, 참가 요청 폼, 승인/거절, 신고·차단 버튼, 수동 마감/수정/삭제) | Success / Unauthorized(참가 요청 시 로그인 필요) / Error | FUNC-033~036, 038~040, 044 |
| 5 | 참가 신청 방법 | 3단계 안내 | 참가 요청은 이렇게 진행돼요 | 아래 순서로 참가 요청을 보낼 수 있습니다. | ①모집글 확인 ②참가 메시지 작성(500자 이내) ③작성자 승인 대기 | Success | FUNC-034 |
| 6 | 안전 안내 | CTA Banner | 안전한 동행을 위해 지켜주세요 | 공개 연락처 공유는 금지되어 있으며, 문제가 있으면 신고·차단 기능을 이용할 수 있습니다. | 안전 수칙 요약 + "여행 조건 준비하기" CTA | Success | FUNC-032, 039, 040, 080 |

- Empty 상태(검색 결과 없음): "조건에 맞는 동행글이 없어요" + 필터 전체 초기화 버튼 + "먼저 모집글을 등록해보세요" CTA + 이용 방법 요약을 함께 표시한다.
- `/travel-tools` CTA는 Section 1과 6에 문맥에 맞게 배치되어 반복이 아닌 입구/출구 역할을 한다.

---

## 7. SCR-005 `/account` 계정·관리 (역할별 탭)

역할에 없는 탭은 렌더링하지 않는다. 계정 탭은 인증 상태에 따라 "로그인"(Guest) 또는 "프로필"(Member 이상)로 내용이 전환된다.

| 역할 | 노출 탭 | Section 구성 |
|---|---|---|
| **Guest** | 계정(로그인) | ①"로그인하고 Free Traveler를 더 편하게 이용하세요" Intro ②로그인/가입/비밀번호 재설정 Card 3종(Form) ③로그인 후 가능한 기능 체크리스트(동행 글 작성, 참가 요청, 내 활동 관리) ④보안·성인 확인 절차 안내 |
| **Member** | 프로필, 내 활동 | **프로필**: 닉네임·연령대·여행 스타일·자기소개 Form, 성인 확인 상태 배지. **내 활동**: 내 글 목록 / 참가 요청 목록(보낸·받은) / 차단 목록 / 즐겨찾기 목록(각 Empty 시 안내+CTA) + "새 동행글 작성" CTA |
| **Admin** | 프로필, 내 활동, 관리자 | **관리자**: ①"신고 처리와 외부 이동 링크만 관리할 수 있어요" Intro ②신고 상태 큐(OPEN/REVIEWING/RESOLVED/DISMISSED 필터, 상태 변경+대상 글 숨김) ③항공·숙소 외부 URL 설정 Form(HTTPS 허용목록 검증) |

| Section | 패턴 | 상태 | 관련 REQ |
|---|---|---|---|
| 로그인/가입/재설정 | Form | Success / Error(자격 증명 오류) / Unauthorized(전체 화면 기본 상태) | FUNC-066 |
| 성인 확인 | Form(체크박스) | Success / Error | FUNC-028 |
| 프로필 | Form | Success / Error | FUNC-029 |
| 내 글 / 참가 요청 / 차단 / 즐겨찾기 목록 | Card Grid(목록형) | Success / Empty(설명+CTA) | FUNC-030, 034, 036, 038, 040, 068 |
| 관리자 — 신고 큐 | Chip 목록(Filter)+Card | Success / Empty | FUNC-041, 042 |
| 관리자 — 외부 URL 설정 | Form | Success / Error(허용목록 위반) | FUNC-077 |

- Dashboard형 통계 위젯이나 그래프는 만들지 않는다. 모든 목록은 Card 또는 표 형태의 단순 목록으로 제공한다.
- Admin이 아닌 사용자가 `/account`의 관리자 탭 경로로 직접 접근하면 탭 자체가 존재하지 않으므로 Unauthorized 화면 대신 프로필 탭으로 대체 노출한다.

---

## 8. 상태(State) 정의 요약

Loading / Success / Empty / Error / Unauthorized 중 화면별로 필요한 상태만 정의한다.

| Screen | Loading | Success | Empty | Error | Unauthorized |
|---|---|---|---|---|---|
| SCR-001 | 카드 스켈레톤 | 여행지·안전·동행 콘텐츠 정상 노출 | 필터 결과 없음(조건 완화 안내+초기화), 최근 동행글 없음(안내+CTA) | 여행지/안전정보 로드 실패(재시도) | 해당 없음(전체 공개) |
| SCR-002 | 이미지 지연 로딩 placeholder | 전체 콘텐츠 정상 노출 | 해당 없음(정적 콘텐츠 상시 존재) | 이미지 로드 실패(대체 이미지) | 해당 없음(전체 공개) |
| SCR-003 | 해당 없음(클라이언트 즉시 처리) | 요약 완료·외부 이동 성공 | 해당 없음 | 날짜/필수값 검증 실패, 연락처 패턴 탐지, 외부 URL 오류 | 동행 탭 비로그인/성인 미확인 |
| SCR-004 | 목록 스켈레톤 | 목록·상세 정상 노출 | 검색 결과 없음(초기화+작성 CTA+이용 방법) | 신고/차단/참가 요청 처리 실패 | 참가 요청·신고·차단 시도 시 비로그인 |
| SCR-005 | 목록 스켈레톤 | 프로필/내 활동/관리자 정상 노출 | 내 글·참가 요청·차단·즐겨찾기 없음(안내+CTA), 신고 큐 없음 | 로그인 실패, 외부 URL 허용목록 위반 | Guest가 내 활동·관리자 탭에 접근(탭 미노출로 대체) |

---

## 9. 검증

| 항목 | 확인 결과 |
|---|---|
| 핵심 디자인 Screen 수 | 정확히 5개(SCR-001~005), 초과 생성 없음 |
| SCR-001 / SCR-002 Section 수 | 각 7개 |
| SCR-003 / SCR-004 Section 수 | 각 6개 |
| SCR-005 구성 | 역할별(Guest/Member/Admin) 탭+Section, 역할에 없는 탭 미노출 |
| Header/Footer 공통 사용 | 5개 Screen 모두 동일 컴포넌트 재사용 |
| Desktop/Mobile 기준 | 1440px / 390px 명시, Section 여백 범위(64~96px / 40~64px) 기록 |
| Hero 높이 | 첫 화면 전체를 차지하지 않도록 설계, 1440px에서 다음 Section 시작부가 보이는 높이로 제한 |
| 콘텐츠 패턴 다양성 | Hero, Card Grid, 좌우 분할, Chip 목록, 3단계 안내, CTA Banner를 화면별로 교차 사용 |
| 빈 상태 처리 | 모든 Empty Section에 안내 문장+이용 방법+CTA 포함, Lorem ipsum·"준비 중"·"정보 확인 필요" 미사용 |
| 오류·경고·안전정보 색상 | 코랄(`color.primary`)과 분리된 `color.warning`/`color.danger`/`color.success` 사용 |
| 접근성 | 키보드 포커스 링, 44px 이상 터치 영역 규칙 명시 |
| Dashboard/통계 화면 | 생성하지 않음(SCR-005는 목록·폼 중심) |
| PROJECT_SCOPE/UI Coverage 정합성 | 각 Section에 표기한 관련 REQ는 `docs/03_UI_COVERAGE_ANALYSIS.md`의 Screen 배치와 동일하며, EXCLUDED 항목(REQ-FUNC-045/055/056/071~073/075/076 등)은 본 화면 설계에 포함하지 않음 |
