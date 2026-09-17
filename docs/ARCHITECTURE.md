# ARCHITECTURE — Free Traveler 구현 경계

이 문서는 Free Traveler MVP를 "무엇으로, 어디까지" 구현하는지에 대한 구현 경계를 정의한다. 화면·요구사항 자체의 상세는 `docs/06_SRS_UIUX_REVISED.md`·`docs/PROJECT_SCOPE.md`·`design-reference/UI_CONTRACT.md`가 다루고, 이 문서는 그 결정들을 실제로 코드로 옮길 때의 기술적 경계(무엇을 어떤 계층에 두는지, 무엇을 절대 만들지 않는지)만 다룬다.

## 1. 기술 스택

`package.json` 기준(2026-09 시점 실제 설치 버전):

| 영역 | 선택 | 비고 |
|---|---|---|
| 프레임워크 | Next.js `16.3.4`, App Router | Pages Router 사용 안 함. `src/app/**/page.tsx`만 Route 진입점 |
| 언어 | TypeScript `^5`, `strict: true` (`tsconfig.json`) | `any` 남용 금지, Requirement 검증 스크립트도 TypeScript로 작성 |
| UI 런타임 | React `19.2.8` | Server Component가 기본값(§2) |
| 스타일 | Tailwind CSS `^4` (`@tailwindcss/postcss`) | `design-reference/D-001/DESIGN.md` 토큰을 `tailwind.config.ts`/`globals.css`에 반영(`COMP-GLOBAL-DESIGN-TOKENS`) |
| 데이터/인증 | Supabase (Postgres + Auth) | §7 참고 — 전체 앱의 DB가 아니라 Auth·동행 기능 전용 |
| ORM | 사용 안 함 | §11 |
| 테스트 | Vitest(Unit) + Playwright(Chromium E2E) | §12 |
| CI/배포 | GitHub Actions + Vercel | §13 |

## 2. 화면 구성 — 핵심 4 · 보조 1

`docs/PROJECT_SCOPE.md` §2가 정의한 "핵심 화면 4개 + 보조 화면 1개" 분류는 이후 16개 개별 Route를 5개 Design Screen/Route로 통합하는 단계(`docs/06_SRS_UIUX_REVISED.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`)에서도 그대로 유지됐다 — 화면 수 분류는 유지되고 Route만 통합됐다.

| Screen | 분류 | Route | Page Entry | Mobile 변형 |
|---|---|---|---|---|
| SCR-001 | 핵심(홈) | `/` | `src/app/page.tsx` | 있음 |
| SCR-002 | **보조**(대표 소개) | `/about` | `src/app/about/page.tsx` | 없음 |
| SCR-003 | 핵심(여행 준비: 항공·숙소·동행 작성) | `/travel-tools` | `src/app/travel-tools/page.tsx` | 있음 |
| SCR-004 | 핵심(동행 조회) | `/mates` | `src/app/mates/page.tsx` | 없음(Desktop만 승인) |
| SCR-005 | 핵심(계정·관리) | `/account` | `src/app/account/page.tsx` | 없음(Desktop만 승인) |

Page Entry는 `design-reference/SCREEN_ROUTE_CONTRACT.json`의 `screens[].route`/`page_entry`와 정확히 일치해야 하며, Screen 수는 정확히 5개로 고정한다(추가 Screen 생성 금지).

### 기술 Route(Screen 수에 미포함)

`SCREEN_ROUTE_CONTRACT.json`의 `technical_routes`에 등록된 4개만 허용한다:

- `/auth/callback` → `src/app/auth/callback/route.ts` (Supabase Auth 리다이렉트 처리 Route Handler)
- `/api/**` → `src/app/api/**/route.ts` (예비 패턴 — 이번 범위에서는 실제로 사용하지 않음. 모든 쓰기는 §5·§9의 Server Action으로 처리하고, Auth 콜백을 제외한 Route Handler를 새로 만들지 않는다)
- `*` → `src/app/not-found.tsx` (404)
- `*` → `src/app/error.tsx` (500/런타임 오류)

## 3. Server Component / Client Component 경계

Next.js App Router 기본값을 그대로 따른다: **모든 컴포넌트는 기본이 Server Component**이며, 다음에 해당할 때만 파일 최상단에 `"use client"`를 선언한다.

- 사용자 입력을 받는 Form(항공·숙소 조건 입력, 동행글 작성/신고/차단, 프로필/Auth Form)
- 로컬 상호작용 상태가 필요한 UI(탭 전환, Drawer/Modal 열림·닫힘, Chip 필터, Toast)
- `localStorage` 접근이 필요한 UI(즐겨찾기)

Page Owner(`src/app/**/page.tsx`) 자체는 Server Component로 유지하고, 위 조건에 해당하는 하위 Component만 Client Component로 분리해서 조립한다(Page 전체를 `"use client"`로 선언하지 않음). `src/data`(§6) 정적 데이터는 Server Component에서 직접 import해서 읽고, Supabase 조회가 필요한 부분(동행글 목록/상세 등)만 Server Component에서 `src/lib/supabase/server.ts`(§9)를 통해 읽거나, 상호작용이 필요한 부분은 Client Component + Server Action으로 처리한다.

## 4. 항공·숙소 입력 폼의 상태 경계

`COMP-SCR003-FLIGHT-FORM`/`COMP-SCR003-HOTEL-FORM`은 Client Component이며, 입력값(국가/지역/출발일·귀국일 또는 체크인·체크아웃)은 **해당 컴포넌트의 `useState` 등 일시(ephemeral) React 상태에만** 존재한다. 탭을 벗어나거나 새로고침하면 값이 사라지는 것을 허용하며, 이를 복원하기 위한 서버 저장·URL 동기화를 추가하지 않는다.

## 5. 항공·숙소 입력값 비전송 원칙 (REQ-FUNC-017, REQ-FUNC-025, REQ-NF-017)

항공·숙소 입력값은 다음 어느 경로로도 내보내지 않는다:

- **API/Server Action** — 이 값을 받는 전용 서버 엔드포인트나 Server Action을 만들지 않는다.
- **DB** — Supabase 어떤 테이블에도 저장하지 않는다(§8의 6개 테이블 중 이 값을 위한 테이블 없음).
- **URL** — 외부 이동 링크(`COMP-SCR003-SUMMARY-ACTION`)의 쿼리 파라미터에 목적지·날짜를 포함하지 않는다. 외부 사이트로 이동만 시키고, 해당 사이트 안에서 사용자가 직접 조건을 다시 입력한다.
- **로그/분석** — `console.log` 이외의 분석·로깅 SDK로 전송하지 않으며, 이번 범위에는 클라이언트 분석 SDK 자체를 두지 않는다.

이 원칙은 `TASKS/TASK-COMP-SCR003-FLIGHT-FORM.md`·`TASK-COMP-SCR003-HOTEL-FORM.md`·`TASK-DB-ACCESS.md`·`TASK-E2E-TRAVEL-TOOLS.md`의 Security/Privacy AC로 이미 명문화되어 있다.

## 6. 정적 데이터 계층 (`src/data`)

여행지·국가 안전정보·대표 소개(`free_traveler`) 콘텐츠는 DB가 아니라 **`src/data`의 TypeScript 정적 데이터**로 관리한다(`docs/PROJECT_SCOPE.md` §4).

| 파일 | 내용 | 최소 기준 |
|---|---|---|
| `src/data/destinations.ts` | 여행지(국내/해외) | 국내 10개 이상, 해외 15개국 30개 도시 이상 |
| `src/data/safety.ts` | 국가별 안전정보 8개 카테고리 | 게시된 모든 해외 국가에 1:1 존재 |
| `src/data/representative.ts` | 대표 소개(지표/Timeline/방문국가/Gallery/추천 여행지) | Timeline 6+, 방문국가 30, Gallery 8+, 추천 여행지 4 |
| `scripts/validate-content.ts` | 위 3개 파일의 수량·필수 필드를 빌드 전 검사 | 기준 미달 시 실패(non-zero exit)로 배포 차단 |

콘텐츠 갱신은 코드 변경 + PR 리뷰로만 이루어진다. 인앱 작성·검수·게시 상태 전이 UI(CMS)는 만들지 않는다(§13).

## 7. Supabase의 사용 범위 — Auth와 동행 기능 중심

Supabase는 **전체 애플리케이션의 데이터베이스가 아니라**, 다음 두 영역에만 사용한다.

1. **Auth** — 이메일 인증, 로그인/로그아웃, 성인 확인 상태(`is_adult`/`adult_verified_at`만 저장, 생년월일 원본 미저장)
2. **동행(Travel Mate) 기능** — 동행 모집글, 참가 요청, 차단, 신고, 외부 URL 허용목록 설정(§8)

여행지·안전정보·대표 소개(§6)와 즐겨찾기(`localStorage`)는 Supabase를 전혀 호출하지 않는다.

## 8. DB 스키마 경계 — 정확히 6개 테이블

`supabase/migrations/0001_schema_base.sql`(`DB-SCHEMA-BASE`)이 만드는 테이블은 다음 6개로 고정하며, 이 범위를 넘는 새 테이블을 추가하지 않는다.

1. `profiles` — 회원 프로필, 역할(Member/Admin), 성인 확인 상태
2. `mate_posts` — 동행 모집글(자동 마감은 조회 시점 `end_date` 계산, 배치 없음), `safety_consent_at` 포함
3. `mate_applications` — 참가 요청(PENDING/ACCEPTED/REJECTED)
4. `user_blocks` — 사용자 차단
5. `reports` — 신고(OPEN/REVIEWING/RESOLVED/DISMISSED)
6. `outbound_url_settings` — 항공·숙소 외부 이동 URL 허용목록(Admin 설정)

범용 감사 로그(이전값/새값/사유/담당자 이력) 테이블은 만들지 않는다(§13).

## 9. Supabase Client 구조 — Browser · Server 분리

`src/lib/supabase/`에 목적이 다른 두 Client를 둔다(둘 다 anon key 기반이며, 서비스 롤 키로 RLS를 우회하는 별도 경로는 두지 않는다 — §10).

| 파일 | 실행 환경 | 용도 |
|---|---|---|
| `src/lib/supabase/client.ts` | 브라우저(Client Component) | 로그인 상태 구독, Client Component에서 직접 필요한 조회 |
| `src/lib/supabase/server.ts` | 서버(Server Component/Server Action/Route Handler) | 쿠키 기반 세션으로 RLS가 적용된 조회·쓰기 수행 |
| `src/lib/supabase/queries.ts` | 서버 | `server.ts` 위에서 동작하는 타입 안전 쿼리 헬퍼. 이메일·전화번호는 select 단계에서부터 응답에 포함하지 않음 |
| `src/lib/actions/*.ts` | 서버(Server Action) | `mate-posts`/`mate-applications`/`blocks-reports`/`auth-profile`/`admin-settings` — 모든 쓰기는 이 계층을 통해서만 수행하고 클라이언트에서 테이블에 직접 쓰지 않음 |

## 10. RLS 원칙 — 단순한 3단 규칙

`supabase/migrations/0002_rls_base.sql`(`DB-RLS-BASE`)은 6개 테이블 모두에 아래 3단 규칙만 적용한다(역할·조건을 더 세분화하지 않음).

1. **본인 행** — 자신이 작성/요청/신고/설정한 행은 본인만 조회·수정
2. **요청 대상 작성자** — 동행 모집글 작성자는 자신의 글에 걸린 참가 요청을 조회·승인·거절
3. **Moderator/Admin** — `profiles.role`이 Admin인 사용자만 신고 상태 변경, 외부 URL 설정, 신고 대상 데이터 열람

인증/역할 검증은 서버(RLS + Server Action)에서 수행하며, 클라이언트 조건부 렌더링은 UX 편의일 뿐 보안 경계로 취급하지 않는다(REQ-NF-013). 서비스 롤 키로 RLS를 건너뛰는 관리자 백도어나 별도 감사 로그 테이블은 두지 않는다.

## 11. ORM 미사용

Prisma 등 ORM을 사용하지 않는다. `src/lib/supabase/queries.ts`는 Supabase JS Client(`@supabase/supabase-js`, `@supabase/ssr`)의 쿼리 빌더를 직접 사용하고, 스키마 변경은 `supabase/migrations/*.sql`로만 관리한다.

## 12. 테스트 전략

| 계층 | 도구 | 대상 Task | 대상 |
|---|---|---|---|
| Unit | Vitest | `UNIT-TRAVEL-DATES`, `UNIT-CONTACT-DETECTION`, `UNIT-MATE-STATE` | 날짜 검증, 연락처 탐지 정규식, 동행 상태 전이 로직 |
| Integration | Vitest(+ 실제/로컬 Supabase) | `TEST-RLS-BASIC` | §10 3단 규칙이 실제 DB에서 허용/거부대로 동작하는지 |
| E2E | Playwright, **Chromium 프로젝트만** | `E2E-PUBLIC-SMOKE`, `E2E-TRAVEL-TOOLS`, `E2E-MATE-AUTH` | 공개 탐색, 항공·숙소 흐름, 로그인+동행 작성/참가 흐름 |

`playwright.config.ts`에 firefox/webkit 프로젝트를 추가하지 않는다. Playwright는 위 3개 Task로 5~7개 핵심 흐름만 커버하며, 화면별로 별도 Smoke Task를 늘리지 않는다.

## 13. CI/CD — GitHub Actions + Vercel

- **GitHub Actions**(`.github/workflows/ci.yml`, `CI-QUALITY-GATE`)가 PR마다 `tsc --noEmit`, `eslint`, `vitest`, `playwright test --project=chromium`을 실행한다. 실패 시 병합을 막는다.
- **Vercel**의 GitHub 연동이 PR마다 Preview 배포를 자동 생성한다(별도 배포 스크립트를 작성하지 않음).
- 병합은 사람이 리뷰 후 수동으로 수행한다.
- `RELEASE-CHECK-VERCEL-SUPABASE`(`TASKS/checks/release-vercel-supabase.md`)로 배포 URL의 HTTPS, 환경변수 노출 여부, Supabase 비용을 배포 후 수동 점검한다.

## 14. 명시적으로 만들지 않는 것

- **AWS·EC2** — 배포는 Vercel + Supabase로 한정한다. 별도 컴퓨트/네트워크 인프라를 두지 않는다.
- **자동 Merge** — 무인 자동 병합 봇/Runner를 두지 않는다. `CI-QUALITY-GATE`는 게이트일 뿐 병합을 자동 실행하지 않는다.
- **전체 콘텐츠 CMS** — §6의 정적 데이터는 코드 변경으로만 갱신하며, 인앱 작성·검수·게시 워크플로를 만들지 않는다.
- **외부 Email 공급자 연동** — 참가 요청/승인/거절/신고 처리 알림은 인앱 Toast/상태 배지로만 제공하고, 실제 이메일 발송 제공자(SendGrid 등)를 연동하지 않는다. Supabase Auth의 기본 인증 메일 발송만 사용한다.
- **범용 Monitoring/부하 테스트/자동 백업** — 가용성·에러율 모니터링 대시보드, DB 백업 SLA, 외부 링크 자동 점검, 부하 테스트 인프라를 구축하지 않는다(`docs/PROJECT_SCOPE.md` §5, REQ-NF-007~011/020/033 EXCLUDED).
- **범용 감사 로그** — 관리자 행위 이력 테이블을 두지 않는다(§8).
- **Prisma/ORM** — §11.

## 15. 착수 차단(Blocking) — 실제로 없는 파일/환경변수

아래는 2026-09-16 기준 저장소 실사(inspection)로 확인한, **실제로 존재하지 않아 구현을 시작하기 전에 준비해야 하는** 항목만 기록한다. CMS·외부 Email 공급자·Monitoring은 §14에 따라 프로젝트 범위에서 제외되므로 착수 차단 항목이 아니다.

| 구분 | 없는 것 | 필요한 조치 |
|---|---|---|
| 패키지 | `@supabase/supabase-js`, `@supabase/ssr` | `package.json`에 추가(§9 Client 구현 전 필수) |
| 패키지 | `vitest` (+ 관련 설정) | `package.json`에 추가, `vitest.config.ts` 작성(§12) |
| 패키지 | `@playwright/test` | `package.json`에 추가, `playwright.config.ts`에 `chromium` 프로젝트만 정의(§12) |
| 환경변수 | `NEXT_PUBLIC_SUPABASE_URL` | Supabase 프로젝트 생성 후 `.env.local`(로컬)·Vercel 프로젝트 환경변수(배포)에 설정 |
| 환경변수 | `NEXT_PUBLIC_SUPABASE_ANON_KEY` | 위와 동일 |
| 파일 | `.env.local`/`.env.example` | 저장소에 아직 없음. 위 두 환경변수를 담을 `.env.example`을 추가하고 `.env.local`은 `.gitignore`(`.env*`, 이미 적용됨)로 유지 |
| 디렉터리 | `supabase/` (`migrations/`, `seed.sql`) | `DB-SCHEMA-BASE`/`DB-RLS-BASE`/`DB-SEED-BASE` 착수 전 Supabase 프로젝트·CLI 연결 필요 |
| 디렉터리 | `.github/workflows/` | `CI-QUALITY-GATE` 착수 전 `ci.yml` 추가 필요 |
| Route | `src/app/about/`, `src/app/travel-tools/`, `src/app/mates/`, `src/app/account/` | 아직 create-next-app 기본 구조만 존재(`src/app/page.tsx`도 Starter 상태) — 각 Page Owner Task(`TASKS/TASK-PAGE-SCR00*.md`) 착수 전 디렉터리 생성 필요 |

위 항목은 모두 "실제로 없는 파일/설정"만 기록했으며, 화면·요구사항 설계(`docs/06_SRS_UIUX_REVISED.md`, `design-reference/*`)나 Task 정의(`TASKS/*`) 자체의 누락은 없다(`python scripts/audit_tasks.py` → `AUDIT_PASS`).

## 참고 문서

- `docs/PROJECT_SCOPE.md` — 구현/제외 범위, 화면 4+1 분류의 출처
- `docs/06_SRS_UIUX_REVISED.md` — 16→5 Route 통합, 114개 Requirement 최종 상태
- `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json` — Screen/Route/Page Entry 정본
- `design-reference/D-001/DESIGN.md` — 시각 디자인 토큰(이 문서가 다루는 구현 경계와는 별도 축)
- `TASKS/00_TASK_LIST.md`, `TASKS/TASK-*.md`, `TASKS/TASK_MANIFEST.csv` — Task 단위 실행 계획과 파일 경로 근거
