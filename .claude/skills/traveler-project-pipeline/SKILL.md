---
name: traveler-project-pipeline
description: Free Traveler Next.js 구현을 위한 Task 생성 파이프라인. SCREEN_ROUTE_CONTRACT.json을 정본으로 5개 승인 Screen과 REQ-FUNC-001~080/REQ-NF-001~034 114개 요구사항을 Page Owner·Component·Data·DB·API·Test·Manual·CI Task로 분해하고, 생성 전 입력을 검증하고 생성 후 결과를 감사한다. TASKS/00_TASK_LIST.md(Markdown)와 TASKS/TASK-<ID>.md 1:1 상세 파일 체계를 사용한다. "task list 만들어줘", "task 생성 파이프라인", "/gen-tasklist", "/gen-task-details", "/audit-tasks" 요청 시 사용.
---

# Traveler Project Pipeline

Free Traveler(Next.js App Router) 구현을 위한 Task를 생성·상세화·감사하는 4단계 파이프라인이다. 이 Skill은 `/gen-tasklist`, `/gen-task-details`, `/audit-tasks` 세 Command와 `scripts/validate_inputs.py`, `scripts/build_task_details.py`, `scripts/audit_tasks.py` 세 Script의 공통 규칙 원본이다. 세 Command는 모두 이 문서를 먼저 따른다.

**실제 산출물은 Markdown이다.** `tasks/TASK_LIST.json`·`tasks/details/*.md` 같은 JSON 기반 산출물은 이 프로젝트에서 실제로 만들어진 적이 없다 — 실제 정본은 `TASKS/00_TASK_LIST.md`(사람이 읽는 Markdown Task List)와 `TASKS/TASK-<TASK_ID>.md`(Task별 상세 파일) 1:1 체계다.

## 0. Pipeline 단계

1. **입력 검증**: `python scripts/validate_inputs.py` 실행. 실패(non-zero exit)하면 여기서 멈추고 검증 리포트를 그대로 사용자에게 보고한다.
2. **Task List**: `TASKS/00_TASK_LIST.md`를 실제 SRS·Scope·Design·Screen Contract 문서와 `src/app` 실제 파일 트리를 읽어 작성/갱신한다(이 단계를 자동 생성하는 Script는 없다 — `/gen-tasklist`가 직접 읽고 쓴다).
3. **Task 상세**: `python scripts/build_task_details.py` 실행 → `TASKS/00_TASK_LIST.md`의 구현 Task마다 `TASKS/TASK-<TASK_ID>.md`를 1:1로 생성한다(이미 있는 파일은 건너뛴다 — 갱신하려면 먼저 지우고 재실행).
4. **감사**: `python scripts/audit_tasks.py` 실행 → `TASKS/TASK_MANIFEST.csv`·`TASKS/TASK_AUDIT_REPORT.md`를 쓰고, 18개 규칙(§15 참고) 중 하나라도 위반하면 `AUDIT_FAIL`로 종료(exit 1)한다. `/gen-task-details`는 3단계 뒤에 **반드시** 이 4단계를 실행한다. `/audit-tasks`는 이 4단계만 독립적으로 다시 실행한다.

이 Skill 자체는 Task나 구현 코드를 생성하지 않는다. `TASKS/`는 이미 채워져 있을 수도, 비어 있을 수도 있다 — 매번 실제 상태를 다시 읽는다.

---

## 1. HARNESS_SCHEMA

`HARNESS_SCHEMA = "traveler-screen-route-v1"`

`design-reference/SCREEN_ROUTE_CONTRACT.json`의 `schema_version` 값과 정확히 일치해야 한다. 불일치하면 `validate_inputs.py`가 실패로 보고한다.

## 2. Screen 목록의 정본

**Screen 목록·Route·Page Entry의 유일한 정본은 `design-reference/SCREEN_ROUTE_CONTRACT.json`이다.** `docs/UIUX_TRACEABILITY.md`, `design-reference/UI_CONTRACT.md`, 이 문서의 표는 모두 참고용 요약이며, 실제 생성/감사 시점에는 반드시 JSON을 다시 읽어 Screen 개수·Route·Page Entry를 확정한다. JSON과 다른 문서가 상충하면 JSON이 우선한다.

현재(참고용) 5개 Screen:

| Screen ID | Route | Page Entry | 분류 | Mobile 변형 |
|---|---|---|---|---|
| SCR-001 | `/` | `src/app/page.tsx` | 핵심 | O |
| SCR-002 | `/about` | `src/app/about/page.tsx` | 보조 | X |
| SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | 핵심 | O |
| SCR-004 | `/mates` | `src/app/mates/page.tsx` | 핵심 | X |
| SCR-005 | `/account` | `src/app/account/page.tsx` | 핵심 | X |

## 3. Page Owner Task — 정확히 5개

Screen마다 **정확히 하나**의 Page Owner Task(`PAGE-SCR001`~`PAGE-SCR005`)를 만든다. Page Owner Task는 해당 Route의 Page Entry(`page.tsx`)를 실제로 조립·완성하는 책임을 진다. Screen이 몇 개든 JSON에서 읽은 개수만큼만 만들고, 5가 아니면 `audit_tasks.py`가 실패로 보고한다(check 5).

## 4. Expected Files는 실제 파일 트리를 본 뒤에 쓴다

Task 생성 시 매번 `src/app` 아래를 실제로 스캔(`Glob`/`ls` 또는 `validate_inputs.py`의 스캔 결과)해서 이미 존재하는 파일과 새로 만들어야 하는 파일을 구분한다. 존재 여부를 확인하지 않고 Expected Files를 추정해서 쓰지 않는다. 이 Skill 갱신 시점 기준 `src/app`에는 create-next-app 기본 `layout.tsx`/`page.tsx`/`globals.css`/`favicon.ico`만 있고 `about/`, `travel-tools/`, `mates/`, `account/` 디렉터리는 없다 — 이 스냅샷은 시간이 지나면 바뀌므로 매번 재확인한다(`docs/ARCHITECTURE.md` §15도 동일 스냅샷을 기록).

## 5. Task 종류와 ID 접두사

| 종류 | ID 접두사(예시) | 역할 |
|---|---|---|
| Page Owner | `PAGE-SCR00N` | 하나의 Route에 정확히 하나. Page Entry를 조립하고 Section 순서·상태 연결까지 책임진다. 개별 Section의 마크업/로직을 직접 새로 만들지 않는다(이미 있는 Component Task 결과물만 조립) |
| Component | `COMP-SCR00N-*`, `COMP-GLOBAL-*`, `COMP-TECH-*` | Screen 하나의 Section/재사용 UI 단위 하나. `COMP-GLOBAL-*`(Header/Footer/Toast/Empty State/Design Tokens)와 `COMP-TECH-*`(404/500/정책 페이지)는 특정 Screen에 종속되지 않는 전역/기술 Component다 |
| Data | `DATA-*` | `src/data` 정적 데이터 + 검증 스크립트 |
| Database | `DB-*` | Supabase 스키마/RLS/쿼리 헬퍼/시드(§10) |
| API | `API-*` | Server Action / Auth 콜백 Route Handler |
| Unit Test | `UNIT-*` | Vitest 단위 테스트 |
| Integration Test | `TEST-RLS-BASIC` | RLS 통합 테스트 |
| E2E Test | `E2E-*` | Playwright Chromium Smoke(§13) |
| Manual Check | `MANUAL-*` | 자동화되지 않는 수동 점검(체크리스트 문서만 산출) |
| CI/Infra | `CI-*`, `RELEASE-CHECK-*` | GitHub Actions 게이트, Vercel/Supabase 배포 점검 |

## 6. 의존 관계 — Page Owner는 같은 Screen의 Component Task에 의존한다

`PAGE-SCR00N`의 Depends On은 **같은 Screen(SCR-00N)에 속한 모든 `COMP-SCR00N-*` Task ID를 포함해야 한다.** 다른 Screen의 Component Task를 의존 대상에 넣지 않는다. `COMP-GLOBAL-*`는 예외로, 직접적인 Depends On 없이도 모든 Page Owner가 암묵적으로 혜택을 받는 기반 계층으로 취급한다(예: `COMP-GLOBAL-DESIGN-TOKENS`는 Tailwind 설정 단계에서 전역 적용되며 어떤 Page Owner의 Depends On에도 직접 나열되지 않는다). `audit_tasks.py`는 Screen 태그 기준으로 이 규칙을 검증하되, `COMP-GLOBAL-*`/`COMP-TECH-*`는 이 검사에서 제외한다(check 7).

## 7. `src/app/page.tsx` Owner — Starter 제거 AC

`PAGE-SCR001`의 Acceptance Criteria에는 반드시 "create-next-app 기본 Starter 템플릿(로고, `Get started by editing`, Vercel 배포 링크 등)을 완전히 제거하고 SCR-001 실제 콘텐츠로 교체한다"는 항목을 포함한다. `SCREEN_ROUTE_CONTRACT.json`의 `starter_template_forbidden: true`가 이 Screen에 설정되어 있다. `audit_tasks.py`는 `PAGE-SCR001` 상세 파일에 "Starter" 또는 "스타터" 문구가 있는지 검사한다(check 8).

## 8. `/travel-tools` Owner — 3탭 실제 조립

`PAGE-SCR003`은 항공편 찾기(`COMP-SCR003-FLIGHT-FORM`) / 숙소 찾기(`COMP-SCR003-HOTEL-FORM`) / 동행 구하기(`COMP-SCR003-MATE-WRITE-FORM`, `COMP-SCR003-MATE-LOGIN-GATE`) 3개 영역을 `COMP-SCR003-INTRO-TABS-SHELL` 위에서 **실제로 하나의 탭 컨테이너에 조립**하는 AC를 가진다. 탭 전환 시 다른 탭의 입력 상태가 유지되어야 한다는 조건도 AC에 포함한다. `audit_tasks.py`는 상세 파일에 "항공"·"숙소"·"동행" 세 단어가 모두 있는지 검사한다(check 9).

## 9. `/account` Owner — Guest·Member·Admin 상태 실제 조립

`PAGE-SCR005`는 Guest/Member/Admin 역할별 Component(`COMP-SCR005-AUTH`/`COMP-SCR005-PROFILE`/`COMP-SCR005-MY-ACTIVITY`/`COMP-SCR005-ADMIN-REPORTS`/`COMP-SCR005-ADMIN-URL-SETTINGS`)를 **실제로 조건부 렌더링으로 조립**하는 AC를 가진다. 역할에 없는 탭은 렌더링 자체를 하지 않는다는 조건과 Dashboard·통계 화면 금지를 함께 명시한다. `audit_tasks.py`는 상세 파일에 Guest/Member/Admin(또는 게스트/회원/관리자) 언급이 모두 있는지 검사한다(check 10).

## 10. DB는 6개 테이블로 제한하고, DB Task는 4개다

`docs/PROJECT_SCOPE.md`의 결정에 따라 여행지·안전·대표 콘텐츠는 DB가 아닌 정적 데이터(§11)이므로, DB 테이블은 아래 **정확히 6개**로 고정한다. 이 6개 테이블을 다루는 DB Task는 4개(`DB-SCHEMA-BASE`, `DB-RLS-BASE`, `DB-ACCESS`, `DB-SEED-BASE`)이며, 테이블마다 별도 Task를 만들지 않는다.

| 테이블 | 근거 Requirement |
|---|---|
| `profiles` | REQ-FUNC-027, 028, 029, 066 |
| `mate_posts` | REQ-FUNC-030, 031, 037, 038, 080(동의 시각 컬럼 포함) |
| `mate_applications` | REQ-FUNC-034, 035, 036 |
| `user_blocks` | REQ-FUNC-040 |
| `reports` | REQ-FUNC-039, 041, 042 |
| `outbound_url_settings` | REQ-FUNC-077 |

각 DB Task의 AC에는 RLS 원칙(§10 요약, `docs/ARCHITECTURE.md` §10)과 관련 REQ-FUNC ID를 명시한다. `audit_tasks.py`는 `DB-SCHEMA-BASE`·`DB-RLS-BASE`·`DB-ACCESS`·`DB-SEED-BASE` 4개가 모두 있는지(check 11), 테이블이 6개를 넘지 않는지(check 12)를 검사한다.

## 11. 여행지·안전·대표는 정적 데이터 Task

REQ-FUNC-001~010(여행지), 046~054(안전정보), 057~063(대표소개) 관련 콘텐츠는 DB Task가 아니라 `src/data`의 정적 TypeScript Task로 만든다.

| Data Task ID | 산출물 | 근거 |
|---|---|---|
| `DATA-DESTINATIONS` | `src/data/destinations.ts`(국내 10+, 해외 15개국 30도시+) | REQ-FUNC-001~010 |
| `DATA-SAFETY` | `src/data/safety.ts`(8개 카테고리, 출처·확인일) | REQ-FUNC-046~054 |
| `DATA-REPRESENTATIVE` | `src/data/representative.ts`(지표·소개·Timeline·방문국가·Gallery·추천 여행지) | REQ-FUNC-057~063 |
| `DATA-VALIDATION-SCRIPT` | `scripts/validate-content.ts` — 게시 기준 수량·완전성 빌드 타임 검증 | REQ-FUNC-008, 046, 052, 074 / REQ-NF-026, 027 |

## 12. 항공·숙소 입력값 — 서버·DB·URL·로그 전송 금지

`COMP-SCR003-FLIGHT-FORM`, `COMP-SCR003-HOTEL-FORM`, 이들과 연결된 `DB-ACCESS`·`E2E-TRAVEL-TOOLS`, 그리고 `PAGE-SCR003`의 AC에는 다음을 명시한다: 입력값(국가/지역/출발일/귀국일 등)은 브라우저 Client 상태로만 처리하고, 서버 API·DB·분석 이벤트·외부 이동 URL 쿼리·로그 어디에도 전송하지 않는다(REQ-FUNC-017, 025 / REQ-NF-017). `audit_tasks.py`는 REQ-FUNC-017/025가 배정된 Task 상세 파일에 이 취지의 문구("전송하지 않는다"/"저장하지 않는다" 등)가 있는지 검사한다(check 13).

## 13. Playwright는 Chromium Smoke Task 2~3개만

Screen마다 별도 Test Task를 만들지 않는다 — `E2E-PUBLIC-SMOKE`(공개 흐름), `E2E-TRAVEL-TOOLS`(항공·숙소), `E2E-MATE-AUTH`(로그인+동행) 3개 Task에 5~7개 핵심 흐름을 묶는다. 각 Task의 AC는 "Playwright `chromium` 프로젝트만 사용하고 firefox/webkit 프로젝트는 설정하지 않는다"를 명시한다. 시각적 회귀, 성능, 부하 테스트 Task는 만들지 않는다(REQ-NF-007/008/009/010/011/024가 EXCLUDED인 것과 일치). `audit_tasks.py`는 E2E Test Task 개수가 2~3개인지, firefox/webkit이 (부재를 명시하지 않은 채) 언급되지 않는지를 검사한다(check 15).

## 14. 자동 Merge·EC2·AWS Task 금지

`docs/PROJECT_SCOPE.md`가 명시적으로 제외한 "EC2·AWS 인프라", "무인 자동 Merge Runner"에 해당하는 Task를 만들지 않는다. 배포/CI Task는 Vercel·Supabase·GitHub Actions 범위 안에서만 만든다(`CI-QUALITY-GATE`, `RELEASE-CHECK-VERCEL-SUPABASE`). `audit_tasks.py`는 모든 Task 제목·상세 파일에서 `EC2`, `AWS`, `자동 Merge`, `자동 병합`, `auto-merge`가 (부재를 명시하지 않은 채) 실제 구현 대상으로 언급되는지 검사한다(check 16). Command 실행 중 destructive Git 명령(force push, reset --hard 등)을 임의로 쓰지 않는다.

## 15. 114개 Requirement 전항목 상태 기록 — `docs/PROJECT_SCOPE.md`가 정본

`docs/PROJECT_SCOPE.md`에 있는 REQ-FUNC-001~080, REQ-NF-001~034 **114개 전항목**이 Task List 결과에서 다음 중 하나로 반드시 기록되어야 한다:

- **IMPLEMENT(계열)**: `TASKS/00_TASK_LIST.md`의 어느 한 Task 행의 Requirement Ref 열에 포함된다.
- **EXCLUDED**: Task를 만들지 않고 `TASKS/00_TASK_LIST.md`의 "1. NON_IMPLEMENTATION" 표에 근거·후속 방향과 함께 기록된다.

어느 쪽에도 없는 Requirement가 하나라도 있으면 `audit_tasks.py`가 실패로 보고한다(check 17). `docs/UIUX_TRACEABILITY.md`도 같은 매핑을 화면 단위로 보여주지만, 감사 시점의 IMPLEMENT/EXCLUDED 판정 자체는 `docs/PROJECT_SCOPE.md`를 정본으로 삼는다.

`scripts/audit_tasks.py`가 실제로 검사하는 18개 규칙 전체 목록(요약)은 다음과 같다 — 정확한 로직은 스크립트 자체와 `TASKS/TASK_AUDIT_REPORT.md`를 참조한다.

1. Task List 구현 ID와 상세 Task 파일 1:1
2. 중복 Task ID 0
3. Depends On 누락 0
4. Dependency Cycle 0
5. Screen 5개 모두 Page Owner 정확히 1개
6. Route·Page Entry·Expected Files 일치
7. Component-only Screen 0
8. SCR-001 Starter 제거 AC 존재
9. SCR-003 세 탭 조립 AC 존재
10. SCR-005 역할별 상태 조립 AC 존재
11. DB Schema·RLS·Access·Seed Task 존재
12. DB Table 범위가 6개 기본 테이블을 크게 넘지 않음
13. 외부 입력 비저장 AC 존재
14. Auth·성인·기본 RLS AC 존재
15. Playwright Chromium Smoke Task 존재
16. AWS·EC2·자동 Merge 구현 Task 0
17. REQ-FUNC 80개와 REQ-NF 34개가 Task 또는 EXCLUDED 표에 존재
18. EXCLUDED 상세 구현 파일이 생성되지 않음

## 16. EXCLUDED는 Task를 만들지 않되 추적에서 지우지 않는다

EXCLUDED 21개는 상세 구현 Task를 만들지 않는다: `REQ-FUNC-045, 055, 056, 071, 072, 073, 075, 076` / `REQ-NF-007, 008, 009, 010, 011, 018, 020, 021, 022, 024, 029, 032, 033`. 대신 `TASKS/00_TASK_LIST.md`의 "1. NON_IMPLEMENTATION" 표에 `docs/PROJECT_SCOPE.md`의 제외 사유를 그대로 인용해 남긴다. `audit_tasks.py`는 이 21개가 어떤 Task의 Requirement Ref에도 배정되지 않았는지, `TASKS/TASK-<REQ_ID>.md` 같은 상세 파일이 만들어지지 않았는지를 검사한다(check 18).

## 17. Task List와 상세 파일은 1:1

`TASKS/00_TASK_LIST.md`의 모든 구현 Task 행은 `TASKS/TASK-<TASK_ID>.md` 파일을 정확히 하나 가져야 하고, 반대로 목록에 없는 상세 파일이 있어서도 안 된다. `audit_tasks.py`가 양방향으로 검사한다(check 1·2).

## 18. 상세 생성 후 audit_tasks.py 실행

`/gen-task-details`는 `scripts/build_task_details.py`로 상세 파일을 다 쓴 뒤 마지막 단계로 `python scripts/audit_tasks.py`를 실행하고, 그 결과(AUDIT_PASS/AUDIT_FAIL과 위반 목록)를 사용자에게 그대로 보고한다. 실패했다고 임의로 위반 항목을 문서에서 지워서 통과시키지 않는다 — 원인을 고쳐 재실행한다.

## 19. Page Owner AC — Section 순서와 최소 콘텐츠 수

모든 Page Owner Task의 Acceptance Criteria는 `design-reference/UI_CONTRACT.md`에 정의된 **Section 순서**와 `docs/04_UIUX_PLAN.md`/`design-reference/D-001/DESIGN.md`의 **최소 콘텐츠 수**를 그대로 옮겨 적는다(예: SCR-001은 국내 6·해외 6·테마 6·안전정보 6, SCR-002는 Timeline 6개 이상·방문국가 30개·Gallery 8장 이상·추천 여행지 4개, SCR-003은 3탭 전부와 Tip 3개, SCR-004는 목록 최대 8·신청 3단계). 숫자를 생략하거나 "충분히"처럼 모호하게 쓰지 않는다.

## 20. Empty State 규칙 — 빈 영역·Placeholder 금지 (SCR-001/004/005 한정)

`docs/04_UIUX_PLAN.md`의 화면별 상태 정의에 따라, 실제로 "0건" 런타임 상황이 있는 Page Owner(`PAGE-SCR001`의 동행글 티저, `PAGE-SCR004`의 검색 결과, `PAGE-SCR005`의 내 활동/신고 큐)만 다음을 AC에 포함한다:

- 큰 빈 영역이나 장식만 있는 빈 Card를 만들지 않는다.
- Lorem ipsum, "준비 중", "정보 확인 필요" 같은 Placeholder 문구를 쓰지 않는다.
- 데이터가 없는 상태에도 **안내 문장 + 이용 방법 + CTA**를 갖춘 완성형 Empty State를 표시한다.

`PAGE-SCR002`(정적 콘텐츠, 0건 상황 자체가 없음)와 `PAGE-SCR003`(0건 대신 로그인/성인 인증 Unauthorized 상태)은 이 Empty State 요구사항 대상이 아니다 — 대신 각각 `DATA-VALIDATION-SCRIPT`(최소 콘텐츠 수 미달 시 빌드 차단)와 로그인 안내 UI로 같은 취지를 구현한다. `audit_tasks.py`의 check 10은 이 구분을 반영해 `PAGE-SCR001`/`004`/`005`에만 Empty State 문구를 강제한다.

---

## 21. Task 분해 참고표 — 실제 71개 (2026-09-16 Task Audit 보완 기준)

| 종류 | 개수 | ID 예 |
|---|---|---|
| Page Owner | 5 | `PAGE-SCR001`~`PAGE-SCR005` |
| Component — SCR-001 | 8 | `COMP-SCR001-HERO-SEARCH` 등 |
| Component — SCR-002 | 7 | `COMP-SCR002-HERO` 등 |
| Component — SCR-003 | 7 | `COMP-SCR003-FLIGHT-FORM` 등 |
| Component — SCR-004 | 6 | `COMP-SCR004-FILTER-BAR` 등 |
| Component — SCR-005 | 5 | `COMP-SCR005-AUTH` 등 |
| Component — 전역 | 6 | `COMP-GLOBAL-HEADER-FOOTER`, `COMP-GLOBAL-LOADING-STATE`, `COMP-GLOBAL-ERROR-STATE` 등 |
| Component — 기술 Route | 2 | `COMP-TECH-ERROR-PAGES`, `COMP-TECH-POLICY-PAGES` |
| Data | 4 | `DATA-DESTINATIONS` 등 |
| Database | 4 | `DB-SCHEMA-BASE` 등 |
| API | 5 | `API-MATE-POSTS` 등 |
| Unit Test | 3 | `UNIT-TRAVEL-DATES` 등 |
| Integration Test | 1 | `TEST-RLS-BASIC` |
| E2E Test | 3 | `E2E-PUBLIC-SMOKE` 등 |
| Manual Check | 3 | `MANUAL-RESPONSIVE-DENSITY` 등 |
| CI/Infra | 2 | `CI-QUALITY-GATE`, `RELEASE-CHECK-VERCEL-SUPABASE` |

**합계: 69** — 이 총계는 이미 실제로 생성된 `TASKS/00_TASK_LIST.md`/`TASKS/TASK-*.md`의 현재 상태이며, 새 Requirement나 Screen이 추가되지 않는 한 이 표가 곧 정본이다. 개수 자체를 완료 조건으로 쓰지 않는다 — Requirement 커버리지(§15)와 `audit_tasks.py` 결과가 완료 조건이다.

---

## 22. Task List Markdown 스키마 (`TASKS/00_TASK_LIST.md`)

이 파일은 JSON이 아니라 Markdown이다. 구조:

1. 헤더 + 사전 검사(`validate_inputs.py`) 통과 기록, Task 총계·Category별 개수 요약표
2. "1. NON_IMPLEMENTATION" — EXCLUDED 21개 Requirement 표(`| Requirement | 분류 | 근거 | 후속 방향 |`)
3. "2."~"N." — Category별 Task 표, 열은 정확히 다음 순서다:

   `| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |`

   각 표 뒤에는 그 Category(또는 Page Owner는 Task별)의 Functional/Visual/Security AC, Verify, Priority를 프로즈로 덧붙인다.
4. 마지막 절 — 114개 Requirement 커버리지 자가 검증 요약

## 23. Task 상세 Markdown 스키마 (`TASKS/TASK-<TASK_ID>.md`)

`scripts/build_task_details.py`가 실제로 생성하는 형식이며, 정확히 아래 14개 절을 이 순서로 포함한다(예시: `TASKS/TASK-PAGE-SCR003.md`).

```markdown
# <TASK_ID> - <제목>

Category: ... | Implementation Status: ... | Priority: ...

## Context
## Project Scope
## Requirement Ref
## Screen / Route / Page Entry
## Design Ref
## Depends On
## Expected Files
## Functional AC
## Visual AC
## Security/Privacy AC
## Test Cases
## Verify
## Definition of Done
## Forbidden
```

`Forbidden` 절에는 공통 항목(Expected Files 밖 수정 금지 등, §24)과 Task별 추가 항목을 함께 적는다. `Forbidden` 절 안에서 금지 키워드를 "이름 붙여 금지"하는 것은 §24 위반이 아니다(§24는 실제로 만들라는 의미로 쓰인 경우만 위반).

## 24. 금지 키워드(전 Task 상세 공통 검사 대상)

`EC2`, `AWS`, `자동 병합`, `자동 Merge`, `auto-merge`, `별점`, `★`, `Lorem ipsum`, `준비 중`, `정보 확인 필요`, Airbnb 상표 관련 고유명사(`Rausch`, `Guest favorite` 등). `audit_tasks.py`는 "## Forbidden" 절을 제외한 본문에서, "금지"/"없음"/"제거"/"거부"/"~않(는다)" 같은 부정 표현과 같은 줄에 없는 경우만 위반으로 판정한다(§14/§13 참고 — 금지 항목을 이름 붙여 금지하는 서술 자체는 위반이 아니다).
