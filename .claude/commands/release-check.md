---
description: 배포 준비 상태를 종합 판정한다. Task/Wave 상태, Page Owner 완료, CI, Playwright Smoke, Supabase 6개 Table·RLS, Vercel Preview, EXCLUDED 목록을 검사해 RELEASE_READY 또는 RELEASE_BLOCKED를 보고한다.
---

`traveler-project-pipeline` Skill과 `docs/PROJECT_SCOPE.md`·`docs/ARCHITECTURE.md`를 기준으로 삼는다. 이 Command는 판정만 한다 — 코드나 Task 문서를 수정하지 않는다.

## 검사 (전부 실제 파일을 읽고 확인한다)

1. **Task·Wave 상태** — `TASKS/WAVE_PLAN.md`·`TASKS/WAVE_STATE.md`를 읽는다. 하나라도 없으면 그 자체로 `RELEASE_BLOCKED`(Wave 진행 기록이 없어 배포 판단 근거가 없음). 있으면 `BLOCKED_*` 상태로 남아있는 Task가 있는지 확인한다.
2. **5개 Page Owner DONE** — `TASKS/WAVE_STATE.md`에서 `PAGE-SCR001`~`PAGE-SCR005` 5개가 모두 `DONE`인지 확인한다. 하나라도 아니면 `RELEASE_BLOCKED`.
3. **CI PASS** — `docs/PROJECT_STATE.md`의 "Latest CI" 필드(있으면)와 `.github/workflows/ci.yml` 실행 이력을 확인한다. 최신 실행이 PASS로 기록되어 있지 않으면 `RELEASE_BLOCKED`.
4. **Playwright Smoke PASS** — `docs/PROJECT_STATE.md`의 "Playwright State" 필드를 확인한다. `E2E-PUBLIC-SMOKE`/`E2E-TRAVEL-TOOLS`/`E2E-MATE-AUTH` 3개 모두 최신 실행이 PASS로 기록되어 있어야 한다.
5. **Supabase 6개 Table·기본 RLS 확인 기록** — `TASKS/TASK_AUDIT_REPORT.md`의 check 11(DB Schema·RLS·Access·Seed Task 존재)·12(Table 범위)가 PASS인지, 그리고 `TEST-RLS-BASIC`의 실제 실행 결과가 `docs/PROJECT_STATE.md`의 "Supabase State" 필드나 `TASKS/WAVE_STATE.md`에 `DONE`으로 기록되어 있는지 확인한다. 문서상 계획만 있고 실제 실행 기록이 없으면 `RELEASE_BLOCKED`.
6. **Vercel Preview Checkpoint** — `docs/PROJECT_STATE.md`의 "Vercel Preview URL" 필드가 실제 URL로 채워져 있고, `TASKS/checks/release-vercel-supabase.md`(`RELEASE-CHECK-VERCEL-SUPABASE`)에 사람이 직접 확인한 기록이 있는지 확인한다. 둘 중 하나라도 비어 있으면 `RELEASE_BLOCKED`.
7. **EXCLUDED 목록** — `TASKS/TASK_AUDIT_REPORT.md`의 check 17(114개 전항목 커버리지)·18(EXCLUDED 상세 구현 파일 미생성)이 PASS인지 확인한다. 즉 21개 EXCLUDED Requirement가 여전히 `docs/PROJECT_SCOPE.md`·`TASKS/00_TASK_LIST.md`의 "1. NON_IMPLEMENTATION" 표와 일치하고, 그중 어느 것도 실제로 구현되지 않았는지 확인한다.

## 판정

위 7개 검사를 모두 통과해야 **`RELEASE_READY`**다. 하나라도 실패하면 **`RELEASE_BLOCKED`**이며, 실패한 검사 번호와 구체적 근거(부족한 파일, 미완료 Task ID, FAIL로 기록된 검사 등)를 전부 나열한다 — 일부만 보고하고 나머지를 생략하지 않는다.

## 출력 후 보고

- 전체 판정: `RELEASE_READY` 또는 `RELEASE_BLOCKED`
- 검사 1~7 각각의 PASS/FAIL과 근거
- `RELEASE_BLOCKED`인 경우 무엇을 먼저 해결해야 하는지(예: "`/run-wave` 재실행으로 미완료 Task 처리", "`TASKS/checks/release-vercel-supabase.md` 작성 필요")
