# UI·UX 승인본 — Free Traveler

**Document ID:** UIUXA-TRAVEL-001
**기반 문서:** `docs/02_SRS_BASELINE.md`, `docs/PROJECT_SCOPE.md`, `docs/03_UI_COVERAGE_ANALYSIS.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, `docs/STITCH_VALIDATION_REPORT.md`
**연결 문서:** `docs/06_SRS_UIUX_REVISED.md`(SRS Route Inventory 개정), `docs/UIUX_TRACEABILITY.md`(Requirement 전수 추적)

---

## 1. 목적

SRS Baseline(`02_SRS_BASELINE.md`)이 정의한 다수의 공개 Route를, `03_UI_COVERAGE_ANALYSIS.md`에서 고정한 5개 디자인 Screen(SCR-001~005)으로 통합한 결과를 승인 기록으로 남긴다. REQ-FUNC-001~080, REQ-NF-001~034는 하나도 삭제하지 않으며, EXCLUDED로 분류된 항목은 계속 EXCLUDED로 유지한다.

---

## 2. 승인된 5개 Screen 현황

`docs/STITCH_VALIDATION_REPORT.md` 기준 실제 검증 결과를 그대로 인용한다. 구현되지 않은 부분을 구현된 것처럼 기록하지 않는다.

| Screen | Route | 분류 | Mobile 변형 | 현재 상태 |
|---|---|---|---|---|
| SCR-001 메인 | `/` | 핵심 | 승인(Desktop+Mobile 모두 PASS) | **PASS** |
| SCR-002 대표 소개 | `/about` | 보조 | 없음(Desktop만 승인) | **PASS** |
| SCR-003 통합 여행 준비 | `/travel-tools` | 핵심 | 승인(Desktop+Mobile) | **NEEDS_REVISION** — 실시간 가격 텍스트, 로그인 안내 Section 중복(Desktop) / 동행 탭 Section 누락(Mobile), 2회 수정 시도 후 미해결 |
| SCR-004 동행 조회 | `/mates` | 핵심 | 없음(Desktop만 승인) | **미검증(진행 중)** — Intro, Filter, 동행글 목록 일부 구축, 목록+상세 분할·신청 방법 3단계·안전 안내 Section 미완성 |
| SCR-005 계정·관리 | `/account` | 핵심 | 없음(Desktop만 승인) | **미생성** |

> 승인(Approved) 대상은 "5개 Screen 구조 자체"이며, 개별 Screen의 화면 완성도는 위 표와 `STITCH_VALIDATION_REPORT.md`를 그대로 따른다. SCR-003의 미해결 위반과 SCR-004/005의 미완성·미생성 상태는 §6 Release Acceptance Criteria에서 재확인한다.

---

## 3. 기존 Route → 신규 Screen 통합 매핑

SRS Baseline §3.5(Page and Route Inventory)의 16개 항목을 5개 Screen의 Section·탭·Drawer·Modal로 통합한다. 상세 개정 근거는 `docs/06_SRS_UIUX_REVISED.md` §2~§3 참조.

| 기존 Route | 기존 용도 | 통합 결과 |
|---|---|---|
| `/` | 홈 | SCR-001 `/` 유지 |
| `/destinations` | 전체 여행지 | SCR-001 Section 2·3(Card Grid)으로 통합, 별도 Route 없음 |
| `/destinations/domestic` | 국내 여행지 | SCR-001 Section 2(국내 Card Grid) |
| `/destinations/overseas` | 해외 여행지 | SCR-001 Section 3(해외 Card Grid) |
| `/destinations/[slug]` | 여행지 상세 | SCR-001 상세 **Drawer**(같은 화면 위에서 열림, 별도 Route 없음) |
| `/flights` | 비행기 찾기 | SCR-003 **항공편 찾기 탭** |
| `/hotels` | 호텔 찾기 | SCR-003 **숙소 찾기 탭** |
| `/mates` | 동행 모집글 목록 | SCR-004 `/mates` 유지 |
| `/mates/[id]` | 동행 모집글 상세 | SCR-004 상세 **패널**(Desktop)/**Drawer**(Mobile), 별도 페이지 Route 없음 |
| `/mates/new` | 동행 모집글 작성 | SCR-003 **동행 구하기 탭**(작성 Form) |
| `/safety` | 국가별 주의사항 목록 | SCR-001 Section 5(안전정보 Card) 진입점으로 통합 |
| `/safety/[countryCode]` | 국가별 주의사항 상세 | SCR-001 안전정보 **Modal/Drawer** |
| `/about` | 대표 소개 | SCR-002 `/about` 유지 |
| `/auth/*` | 가입·로그인·성인 확인 | SCR-005 **Guest 탭**(로그인/가입/재설정), 인증 콜백만 기술 Route로 잔존 |
| `/my/*` | 내 글·참가 요청·차단 | SCR-005 **Member 탭**(내 활동) |
| `/admin/*` | 콘텐츠·신고·설정 | SCR-005 **Admin 탭**(신고 상태·외부 URL 설정만, 콘텐츠 CRUD는 PROJECT_SCOPE EXCLUDED) |

---

## 4. UI Route Contract

`design-reference/SCREEN_ROUTE_CONTRACT.json`을 요약한다(전체는 원본 JSON 참조).

| Screen ID | Route | Page Entry | 분류 | Mobile 변형 |
|---|---|---|---|---|
| SCR-001 | `/` | `src/app/page.tsx` | 핵심 | O |
| SCR-002 | `/about` | `src/app/about/page.tsx` | 보조 | X |
| SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | 핵심 | O |
| SCR-004 | `/mates` | `src/app/mates/page.tsx` | 핵심 | X |
| SCR-005 | `/account` | `src/app/account/page.tsx` | 핵심 | X |

**기술 Route(Screen 수 미포함):**

| Type | Route | Page Entry |
|---|---|---|
| auth_callback | `/auth/callback` | `src/app/auth/callback/route.ts` |
| api_route | `/api/**` | `src/app/api/**/route.ts` |
| not_found | `*` | `src/app/not-found.tsx` |
| error_boundary | `*` | `src/app/error.tsx` |

Route 5개, Page Entry 5개 모두 중복 없음(`SCREEN_ROUTE_CONTRACT.json`의 `completion_checks` 확인).

---

## 5. PROJECT_SCOPE 연결 확인

`docs/PROJECT_SCOPE.md`의 IMPLEMENT/EXCLUDED 분류는 이번 Screen 통합 과정에서 변경하지 않았다.

- EXCLUDED 21개(REQ-FUNC-045, 055, 056, 071, 072, 073, 075, 076 / REQ-NF-007, 008, 009, 010, 011, 018, 020, 021, 022, 024, 029, 032, 033)는 이번에도 EXCLUDED를 유지하며, 5개 Screen 어디에도 복원하지 않았다.
- SCR-005 Admin 탭 범위는 PROJECT_SCOPE가 정한 "신고 상태와 외부 URL 설정만" 원칙을 그대로 따르며, 콘텐츠 CRUD·범용 감사 로그를 추가하지 않는다.
- 전 항목의 Requirement 단위 연결은 `docs/UIUX_TRACEABILITY.md`에서 확인한다.

---

## 6. Release Acceptance Criteria

| # | 기준 | 현재 상태 |
|---|---|---|
| 1 | 5개 Screen이 Stitch에서 생성되고 `STITCH_VALIDATION_REPORT.md` 기준 PASS 판정을 받는다 | **미충족** — SCR-003 NEEDS_REVISION, SCR-004 미검증, SCR-005 미생성 |
| 2 | REQ-FUNC-001~080, REQ-NF-001~034 114개 전항목이 Screen/Route에 매핑되어 누락 없이 추적된다 | **충족** — `docs/UIUX_TRACEABILITY.md` |
| 3 | EXCLUDED 21개 항목이 구현 범위에 포함되지 않는다 | **충족** |
| 4 | Do Not 금지 항목(별점, 실시간 가격, Airbnb 상표, 광고, Lorem ipsum/준비 중/정보 확인 필요, 빈 Card)이 승인된 화면에 없다 | **부분 충족** — SCR-001·SCR-002는 확인 완료, SCR-003은 실시간 가격·중복 Section 미해결, SCR-004·SCR-005는 미검증/미생성으로 확인 불가 |
| 5 | Next.js Page Entry 5개가 각각 정확히 1개 Route에 대응하고 중복이 없다 | **충족** — `SCREEN_ROUTE_CONTRACT.json` |
| 6 | 모든 Requirement Row에 실제 작업 단위(Task)가 생성된다 | **미충족** — 전항목 `PENDING_TASK_GENERATION` |
| 7 | 모든 Requirement Row의 Test가 작성되고 통과한다 | **미충족** — 전항목 미작성 |

**종합 판정: NOT READY FOR RELEASE.** 1·4·6·7번 기준이 아직 충족되지 않았으므로, 이 문서는 "5개 Screen 구조와 Requirement 매핑을 승인"하는 기록이지 "구현 완료"를 의미하지 않는다. 다음 단계는 SCR-003 재수정, SCR-004 완성, SCR-005 생성, 이후 Task 생성과 테스트 작성이다.

---

## 7. 참고 문서

- `docs/02_SRS_BASELINE.md` — Requirement 원본(AC 전문)
- `docs/PROJECT_SCOPE.md` — IMPLEMENT/EXCLUDED 분류 원본
- `docs/03_UI_COVERAGE_ANALYSIS.md` — UI 분류·Screen 배치 근거
- `docs/04_UIUX_PLAN.md` — Section 계약·디자인 시스템 초안
- `design-reference/D-001/DESIGN.md` — 디자인 정본(토큰·컴포넌트 규칙)
- `design-reference/UI_CONTRACT.md` — Screen별 구현 계약
- `design-reference/SCREEN_ROUTE_CONTRACT.json` — 기계 판독용 Route 계약
- `docs/STITCH_VALIDATION_REPORT.md` — Screen 검증 기록
- `docs/06_SRS_UIUX_REVISED.md` — SRS Route Inventory 개정본
- `docs/UIUX_TRACEABILITY.md` — Requirement 전수 추적 매트릭스
