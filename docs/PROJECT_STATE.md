# PROJECT STATE — Free Traveler

이 문서는 Free Traveler 구현 진행 상태를 담는 살아있는 스냅샷이다. `/run-wave`·`/release-check`가 실행될 때마다 아래 필드를 실제 상태에 맞게 갱신한다. 사람이 직접 갱신해도 된다 — 항상 "지금 실제로 무엇이 맞는지"를 반영해야 하며, 낙관적으로 앞서가서 기록하지 않는다.

이 문서 자체는 정본이 아니다. 각 필드의 실제 정본은 아래 표의 "출처"에 있으며, 이 문서는 그 출처들을 한 곳에서 보기 위한 요약일 뿐이다. 값이 의심되면 출처 파일을 다시 읽는다.

## 필드

| 필드 | 현재 값 | 출처 |
|---|---|---|
| Harness Schema | `traveler-screen-route-v1` | `CLAUDE.md`(Harness Marker), `design-reference/SCREEN_ROUTE_CONTRACT.json`(`schema_version`) |
| Design Version | `D-001` | `design-reference/D-001/DESIGN.md` |
| Scope Mode | MVP — `docs/PROJECT_SCOPE.md` 기준 114개 Requirement 중 93 IMPLEMENT / 21 EXCLUDED | `docs/PROJECT_SCOPE.md` |
| Current Wave | 없음(`TASKS/WAVE_PLAN.md` 아직 없음 — Wave 구성 미확정, `docs/DECISION_LOG.md` DEC-010) | `TASKS/WAVE_PLAN.md` |
| Current Task | 없음(미착수) | `TASKS/WAVE_STATE.md` |
| Completed Tasks | 0 / 71 | `TASKS/WAVE_STATE.md`, `TASKS/00_TASK_LIST.md` |
| Blocked Tasks | 없음(아직 어떤 Task도 `/prepare-task`로 평가되지 않음). 다만 `docs/ARCHITECTURE.md` §15의 착수 차단 항목(Supabase 패키지·env·`supabase/`·`.github/workflows/` 미존재)이 해결되기 전에는 `DB-*`/`API-*`/`CI-*` 등 다수 Task가 `BLOCKED_INPUT`으로 판정될 가능성이 높다 | `docs/ARCHITECTURE.md` §15, `/prepare-task` 실행 결과 |
| Latest CI | 없음(`.github/workflows/ci.yml` 아직 없음) | `.github/workflows/ci.yml` |
| Supabase State | 미구성(`supabase/` 디렉터리·Supabase 프로젝트·env 변수 없음) | `docs/ARCHITECTURE.md` §15, `.env.local` |
| Vercel Preview URL | 없음 | Vercel 프로젝트 연결 후 배포 기록 |
| Playwright State | 미구성(`@playwright/test` 미설치, `playwright.config.ts` 없음) | `package.json`, `playwright.config.ts` |
| Deferred Items | 1) `TASKS/WAVE_PLAN.md` 작성 필요(Wave 구성 미확정). 2) Stitch SCR-003 Desktop/Mobile NEEDS_REVISION 2건(가격 문구·중복 로그인 섹션, 동행 섹션 누락) 미해결 — `docs/STITCH_VALIDATION_REPORT.md` 참고. 이 항목은 시각 디자인 목업 단계의 잔여 이슈이며 `TASKS/TASK-PAGE-SCR003.md` 구현 자체를 막지 않는다. 3) EXCLUDED 21개는 "제외"이며 "지연"이 아니다 — `docs/PROJECT_SCOPE.md` §5~7 참고, 이 필드에 포함하지 않는다 | `docs/STITCH_VALIDATION_REPORT.md`, `docs/DECISION_LOG.md` |
| Next Action | 1) `docs/ARCHITECTURE.md` §15 착수 차단 항목 해소(Supabase 프로젝트 생성, 패키지 설치, `.env.local` 작성) → 2) `TASKS/WAVE_PLAN.md` 작성(Task를 Wave로 묶기) → 3) `/run-wave W01` 시작 | 이 문서 자체 |

## Screen Checkpoint

각 Screen의 Page Owner Task(`PAGE-SCR00N`)가 실제로 배포·확인된 시점의 상태를 기록한다. 값은 `PENDING`(착수 전) → `IN_PROGRESS` → `DONE`(사람 Preview 확인 완료, CLAUDE.md 규칙 22) 중 하나다.

| Screen | Route | 상태 |
|---|---|---|
| SCR-001 | `/` | PENDING |
| SCR-002 | `/about` | PENDING |
| SCR-003 | `/travel-tools` | PENDING |
| SCR-004 | `/mates` | PENDING |
| SCR-005 | `/account` | PENDING |
| FINAL | (`/release-check`의 `RELEASE_READY` 판정) | PENDING |
