# DECISION LOG — Free Traveler

이 문서는 Free Traveler MVP 진행 중 확정된 의사결정을 기록한다. 각 결정은 번호(DEC-NNN)로 고정하며, 이후 뒤집히더라도 기존 번호를 재사용하지 않고 새 결정으로 추가한다(이 버전에서는 14개 모두 최초 확정 상태).

## 요약

| ID | 결정 요약 | 상태 |
|---|---|---|
| DEC-001 | 실제 개발 루트는 `traveler/app` | 확정 |
| DEC-002 | 디자인 Screen은 핵심 4개·보조 1개 | 확정 |
| DEC-003 | `/travel-tools`에 항공·숙소·동행 작성을 통합 | 확정 |
| DEC-004 | 여행지·안전·대표는 정적 TypeScript Data | 확정 |
| DEC-005 | Supabase는 Auth와 동행 기능 중심 | 확정 |
| DEC-006 | DB는 6개 Table로 제한 | 확정 |
| DEC-007 | 항공·숙소 입력은 Browser Memory에만 유지 | 확정 |
| DEC-008 | Airbnb DESIGN.md는 vendor 참고본, D-001이 실제 정본 | 확정 |
| DEC-009 | Playwright는 Chromium Smoke만 필수 | 확정 |
| DEC-010 | 사용자의 개발 실행 단위는 Wave | 확정 |
| DEC-011 | Single Agent가 Wave 내부 Task를 순차 수행 | 확정 |
| DEC-012 | PR·Merge는 사용자가 수동 수행 | 확정 |
| DEC-013 | EC2·AWS는 사용하지 않음 | 확정 |
| DEC-014 | 제외 기능은 EXCLUDED로 관리 | 확정 |

---

## DEC-001. 실제 개발 루트는 `traveler/app`

- **결정**: 이 리포지토리 작업 트리에서 Free Traveler Next.js 프로젝트의 실제 개발 루트는 `C:\AI_SERVICE\traveler\app`이다. `package.json`, `src/app`, `docs/`, `design-reference/`, `TASKS/`, `scripts/`는 모두 이 경로 기준이다.
- **배경**: 작업 공간(`C:\AI_SERVICE`)에는 QABOARD 등 다른 프로젝트도 함께 존재한다(`C:\AI_SERVICE\CLAUDE.md` 참고). `traveler/app`이 Next.js 애플리케이션 자체가 위치한 유일한 디렉터리이며, 상위 `traveler/`나 `AI_SERVICE/` 루트에는 실행 가능한 코드가 없다.
- **영향**: 이후 모든 문서·Task·스크립트의 상대 경로는 `traveler/app`을 기준으로 기록한다. 다른 프로젝트(QABOARD 등)의 관례·설정을 Free Traveler에 끌어오지 않는다.
- **관련 문서/Task**: `AGENTS.md`, `CLAUDE.md`(`traveler/app`), `C:\AI_SERVICE\CLAUDE.md`(워크스페이스 개요)

## DEC-002. 디자인 Screen은 핵심 4개·보조 1개

- **결정**: 디자인 Screen 수를 정확히 5개(SCR-001~005)로 고정하고, 그중 4개(SCR-001 홈, SCR-003 여행 준비, SCR-004 동행, SCR-005 계정·관리)를 핵심, 1개(SCR-002 대표 소개)를 보조로 분류한다.
- **배경**: `docs/PROJECT_SCOPE.md` §2가 원래 16개 개별 Route를 핵심 4 + 보조 1로 분류했고, 이후 UI 통합 단계(`docs/03_UI_COVERAGE_ANALYSIS.md` → `docs/04_UIUX_PLAN.md` → Stitch 검증 → `design-reference/UI_CONTRACT.md`)에서도 이 분류를 그대로 계승했다.
- **영향**: 새로운 Screen을 추가로 만들지 않는다(`design-reference/SCREEN_ROUTE_CONTRACT.json`의 `completion_checks.screen_count == 5`로 기계적으로 강제). 인증/내 활동/관리자처럼 과거 독립 Route였던 것도 5개 Screen의 탭·패널로만 흡수한다.
- **관련 문서/Task**: `docs/PROJECT_SCOPE.md` §2, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, `docs/06_SRS_UIUX_REVISED.md`

## DEC-003. `/travel-tools`에 항공·숙소·동행 작성을 통합

- **결정**: 과거 별도 Route였던 항공(`/flights`)·숙소(`/hotels`)·동행 작성(`/mates/new`)을 하나의 Route `/travel-tools`(SCR-003) 안에 3개 탭(항공편 찾기/숙소 찾기/동행 구하기)으로 통합한다.
- **배경**: 세 기능 모두 "여행 준비" 단계에서 사용자가 연속적으로 오가는 흐름이라 판단해 UI 통합 단계에서 하나의 Screen으로 묶었다. 탭 전환 시 각 탭의 입력 상태는 독립적으로 보존한다(DEC-007과 별개로, 탭 자체의 전환 보존은 유지).
- **영향**: `src/app/travel-tools/page.tsx`(`PAGE-SCR003`) 하나가 세 영역을 조립하는 유일한 Page Owner이며, 세 기능을 위한 별도 Route를 만들지 않는다.
- **관련 문서/Task**: `design-reference/UI_CONTRACT.md`(SCR-003), `TASKS/TASK-PAGE-SCR003.md`, `TASKS/TASK-COMP-SCR003-INTRO-TABS-SHELL.md`

## DEC-004. 여행지·안전·대표는 정적 TypeScript Data

- **결정**: 여행지(destinations), 국가 안전정보(safety), 대표 소개(representative) 콘텐츠는 Supabase DB가 아니라 `src/data/*.ts` 정적 TypeScript 데이터로 관리한다.
- **배경**: 이 콘텐츠는 게시 상태 전이나 실시간 갱신이 필요 없고, 콘텐츠 변경은 코드 변경 + PR 리뷰로 충분하다고 판단했다(`docs/PROJECT_SCOPE.md` §4). CMS·인앱 작성/검수 워크플로를 만들지 않기로 한 결정(DEC-014의 EXCLUDED 목록 중 "전체 콘텐츠 CMS")과 직접 연결된다.
- **영향**: 필수 필드는 TypeScript 타입으로 강제하고, 수량·완전성은 `scripts/validate-content.ts`(`DATA-VALIDATION-SCRIPT`)가 빌드 전에 검증한다. 이 세 영역에 대해서는 DB 테이블을 만들지 않는다(DEC-006의 6개 테이블에 포함 안 됨).
- **관련 문서/Task**: `docs/ARCHITECTURE.md` §6, `TASKS/TASK-DATA-DESTINATIONS.md`, `TASKS/TASK-DATA-SAFETY.md`, `TASKS/TASK-DATA-REPRESENTATIVE.md`, `TASKS/TASK-DATA-VALIDATION-SCRIPT.md`

## DEC-005. Supabase는 Auth와 동행 기능 중심

- **결정**: Supabase는 애플리케이션 전체의 데이터베이스가 아니라 (1) Auth(이메일 인증/로그인/성인 확인)와 (2) 동행(Travel Mate) 기능(모집글/참가 요청/차단/신고/외부 URL 설정)에만 사용한다.
- **배경**: DEC-004에 따라 콘텐츠성 데이터는 이미 정적 데이터로 빠졌고, 즐겨찾기는 `localStorage`로 처리하기로 했으므로(`docs/PROJECT_SCOPE.md` §4) Supabase가 실제로 필요한 영역은 인증과 동행 기능뿐이다.
- **영향**: 여행지·안전·대표·즐겨찾기 화면은 Supabase Client를 전혀 호출하지 않는다. Supabase 관련 구현(스키마/RLS/쿼리 헬퍼/Server Action)은 동행·계정 화면(SCR-003 동행 작성 영역, SCR-004, SCR-005)에만 존재한다.
- **관련 문서/Task**: `docs/ARCHITECTURE.md` §7, `TASKS/TASK-DB-ACCESS.md`, `TASKS/TASK-API-*.md`

## DEC-006. DB는 6개 Table로 제한

- **결정**: Supabase Postgres 스키마는 정확히 6개 테이블(`profiles`, `mate_posts`, `mate_applications`, `user_blocks`, `reports`, `outbound_url_settings`)로 제한한다. 이 범위를 넘는 새 테이블(예: 범용 감사 로그, 알림 테이블)을 추가하지 않는다.
- **배경**: 동행 기능(DEC-005)에 필요한 최소 스키마만 남기고, 감사 로그·알림 큐 등 부가 테이블은 "제외 기능"(DEC-014)으로 분류했다.
- **영향**: `DB-SCHEMA-BASE`가 만드는 테이블 수를 `scripts/audit_tasks.py`의 "DB Table 범위" 검사(#12)로 기계적으로 확인한다. 새 기능이 추가되어도 이 6개 테이블 안에서 컬럼을 확장하는 것을 우선 검토한다.
- **관련 문서/Task**: `docs/ARCHITECTURE.md` §8, `TASKS/TASK-DB-SCHEMA-BASE.md`, `scripts/audit_tasks.py`(check 11·12)

## DEC-007. 항공·숙소 입력은 Browser Memory에만 유지

- **결정**: 항공·숙소 조건 입력 Form(`COMP-SCR003-FLIGHT-FORM`/`COMP-SCR003-HOTEL-FORM`)의 입력값은 Client Component의 일시적인 React 상태(Browser Memory)에만 존재하며, 서버 API·DB·URL 쿼리·로그·분석 SDK 어디에도 전송·저장하지 않는다.
- **배경**: 항공·숙소는 실제 예약/결제를 하지 않고 외부 사이트로 이동만 시키는 링크아웃 기능이므로, 사용자의 여행 계획(목적지·날짜)을 서버에 남길 이유가 없다고 판단했다(개인정보 최소화).
- **영향**: 이 값을 위한 전용 서버 엔드포인트를 만들지 않으며, 외부 이동 URL에도 목적지·날짜를 쿼리 파라미터로 넣지 않는다. 새로고침하거나 탭을 벗어나면 값이 사라지는 것을 허용한다.
- **관련 문서/Task**: `docs/ARCHITECTURE.md` §4·§5, `TASKS/TASK-COMP-SCR003-FLIGHT-FORM.md`, `TASKS/TASK-COMP-SCR003-HOTEL-FORM.md`, `TASKS/TASK-E2E-TRAVEL-TOOLS.md`

## DEC-008. Airbnb DESIGN.md는 vendor 참고본, D-001이 실제 정본

- **결정**: `design-reference/vendor/airbnb/DESIGN.md`는 레이아웃 패턴(Hero/Card Grid/Chip 등) 구조를 참고하기 위한 vendor 참고본일 뿐이며, Free Traveler가 실제로 따르는 디자인 정본은 `design-reference/D-001/DESIGN.md`다.
- **배경**: Airbnb 문서를 그대로 베끼면 Rausch 색상명, Cereal 폰트, "Guest favorite" 배지, 3-Product Nav 같은 Airbnb 고유 상표 요소가 섞여 들어갈 위험이 있어, 구조만 참고하고 색상·폰트·컴포넌트 명명은 D-001에서 독립적으로 새로 정의했다.
- **영향**: 코드·문서 어디에도 "Rausch", "Cereal", "Guest favorite" 등 Airbnb 상표 문자열이 나오면 위반으로 간주한다(`scripts/audit_tasks.py`의 금지 키워드 검사, `_traveler_common.py`의 `FORBIDDEN_KEYWORDS`). 색상 토큰(코랄 `#FF6F59` 등)·타이포·spacing은 전부 D-001 기준으로만 구현한다.
- **관련 문서/Task**: `design-reference/vendor/airbnb/DESIGN.md`, `design-reference/D-001/DESIGN.md`, `scripts/_traveler_common.py`(`FORBIDDEN_KEYWORDS`)

## DEC-009. Playwright는 Chromium Smoke만 필수

- **결정**: Playwright E2E 테스트는 Chromium 프로젝트만 정의하고(`playwright.config.ts`에 firefox/webkit 프로젝트를 추가하지 않음), 5~7개 핵심 흐름을 `E2E-PUBLIC-SMOKE`/`E2E-TRAVEL-TOOLS`/`E2E-MATE-AUTH` 3개 Task로만 커버한다.
- **배경**: 크로스 브라우저 회귀 테스트까지 이번 MVP 범위에 넣으면 유지 비용이 커지므로, "핵심 흐름이 최소 1개 브라우저에서 깨지지 않는다"를 확인하는 Smoke 수준으로 범위를 한정했다.
- **영향**: 화면별로 별도 E2E Task를 늘리지 않고, 새 흐름이 필요해도 기존 3개 Task 중 하나에 흐름을 추가하는 것을 우선 검토한다. `scripts/audit_tasks.py`가 E2E Test Task 개수(2~3개)와 chromium 전용 여부를 기계적으로 검사한다(check 15).
- **관련 문서/Task**: `docs/ARCHITECTURE.md` §12, `TASKS/TASK-E2E-PUBLIC-SMOKE.md`, `TASKS/TASK-E2E-TRAVEL-TOOLS.md`, `TASKS/TASK-E2E-MATE-AUTH.md`

## DEC-010. 사용자의 개발 실행 단위는 Wave

- **결정**: 사용자는 `TASKS/00_TASK_LIST.md`의 69개 구현 Task를 한 번에 전부 진행시키지 않고, "Wave"라는 실행 단위로 나누어 진행한다. Wave는 사용자가 한 번의 진행 지시로 처리하도록 묶는 Task 묶음이다.
- **배경**: Task 69개를 의존관계(Depends On) 없이 무작위로 진행하면 순서가 꼬이거나 미완성 의존성 위에서 작업하게 될 위험이 있어, 사용자가 스스로 진행 범위를 Wave 단위로 통제하기로 했다.
- **영향**: 이 결정 시점에는 어떤 Task가 어떤 Wave에 속하는지는 별도로 확정되지 않았다 — Wave 구성표(Wave별 Task 목록)는 이후 별도 계획 문서에서 정의되며, 확정되면 이 DEC-010에 연결한다.
- **관련 문서/Task**: `TASKS/00_TASK_LIST.md`(Wave 구성표는 추후 문서화 예정, 현재 없음)

## DEC-011. Single Agent가 Wave 내부 Task를 순차 수행

- **결정**: 하나의 Wave 안에 있는 여러 Task는 Single Agent(단일 실행 주체)가 순차적으로 하나씩 수행한다. 같은 Wave 내부 Task를 여러 Agent에 나누어 동시에(병렬로) 진행하지 않는다.
- **배경**: Task 간 Depends On 관계와 "Expected Files 밖 파일 수정 금지" 원칙(각 `TASKS/TASK-*.md`의 Forbidden 절)을 지키려면, 같은 Wave 안에서는 순서·완료 여부를 하나의 실행 흐름이 직접 추적하는 것이 충돌(같은 파일 동시 수정, 의존 Task 완료 전 착수)을 막는 가장 단순한 방법이라고 판단했다.
- **영향**: Wave 내부에서는 다중 Agent 병렬 실행(예: 여러 Agent를 동시에 fan-out)을 사용하지 않는다. Wave와 Wave 사이(서로 의존관계가 없는 경우)의 병렬화 여부는 이 결정의 범위 밖이다.
- **관련 문서/Task**: `TASKS/00_TASK_LIST.md`(Depends On 열), 각 `TASKS/TASK-*.md`의 Forbidden 절

## DEC-012. PR·Merge는 사용자가 수동 수행

- **결정**: Task 구현이 끝난 코드의 Pull Request 생성과 Merge는 항상 사용자가 직접, 수동으로 수행한다. Agent/파이프라인이 자동으로 PR을 병합하지 않는다.
- **배경**: DEC-013(자동 Merge 미사용) 및 `docs/PROJECT_SCOPE.md` §5 "무인 자동 Merge Runner" 제외 결정과 같은 맥락이며, 코드 병합은 사람의 리뷰를 거쳐야 한다는 운영 원칙을 명시적으로 재확인한다.
- **영향**: `CI-QUALITY-GATE`(GitHub Actions)는 병합 전 게이트(테스트 통과 여부 확인) 역할만 하고, 게이트 통과 시 자동으로 Merge하는 워크플로 단계를 추가하지 않는다.
- **관련 문서/Task**: `docs/ARCHITECTURE.md` §13·§14, `TASKS/TASK-CI-QUALITY-GATE.md`

## DEC-013. EC2·AWS는 사용하지 않음

- **결정**: 배포·인프라는 Vercel + Supabase로 한정하고, AWS EC2를 포함한 별도 AWS 인프라를 두지 않는다.
- **배경**: MVP 규모에서 별도 컴퓨트/네트워크 인프라를 운영할 필요가 없고, Vercel + Supabase 조합으로 요구되는 모든 기능(호스팅, DB, Auth)을 충족할 수 있다고 판단했다(`docs/PROJECT_SCOPE.md` §5).
- **영향**: `TASKS/00_TASK_LIST.md`·`TASKS/TASK-*.md`에 EC2/AWS 관련 Task를 만들지 않으며, `scripts/audit_tasks.py`가 Task 제목·본문에 EC2/AWS가 실제 구현 대상으로 언급되지 않는지 기계적으로 검사한다(check 16).
- **관련 문서/Task**: `docs/ARCHITECTURE.md` §14, `docs/PROJECT_SCOPE.md` §5, `scripts/audit_tasks.py`(check 16)

## DEC-014. 제외 기능은 EXCLUDED로 관리

- **결정**: MVP 범위에서 만들지 않기로 한 기능·요구사항은 삭제하지 않고, 상태를 `EXCLUDED`로 명시적으로 표시해 계속 추적한다(114개 Requirement 중 21개).
- **배경**: 요구사항을 지우면 나중에 "왜 없는지" 판단할 근거가 사라지므로, `docs/PROJECT_SCOPE.md`부터 시작해 모든 후속 문서(`docs/06_SRS_UIUX_REVISED.md`, `docs/UIUX_TRACEABILITY.md`, `TASKS/00_TASK_LIST.md`)에서 EXCLUDED 항목을 계속 표에 남기기로 했다.
- **영향**: EXCLUDED Requirement는 상세 구현 Task 파일(`TASKS/TASK-*.md`)을 만들지 않으며, `TASKS/00_TASK_LIST.md`의 "NON_IMPLEMENTATION" 표에 근거·후속 방향과 함께 남는다. `scripts/audit_tasks.py`가 114개 전체가 Task 또는 EXCLUDED 표 어느 한쪽에 반드시 존재하는지(check 17), EXCLUDED 항목에 구현 Task가 잘못 배정되지 않았는지(check 18)를 검사한다.
- **관련 문서/Task**: `docs/PROJECT_SCOPE.md` §5~7, `docs/UIUX_TRACEABILITY.md`, `TASKS/00_TASK_LIST.md`("1. NON_IMPLEMENTATION"), `scripts/audit_tasks.py`(check 17·18)
