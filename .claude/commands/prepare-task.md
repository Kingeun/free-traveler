---
description: Task 하나를 구현 착수 전에 검사한다. WAVE_ID·TASK_ID를 받아 8개 항목을 검사하고 READY_TO_IMPLEMENT 또는 BLOCKED_* 상태 중 하나를 보고한다. 코드를 수정하지 않는다.
---

`traveler-project-pipeline` Skill을 로드하고 그 규칙(§2~§10, §12, §14~§17)을 기준으로 삼는다.

## 입력

- `WAVE_ID`(예: `W03`)
- `TASK_ID`(예: `PAGE-SCR003`, `COMP-SCR004-FILTER-BAR`)
- 선택된 상세 Task 파일: `TASKS/TASK-<TASK_ID>.md`(실제로 읽는다. 없으면 즉시 `BLOCKED_INPUT`)

이 Command는 **코드를 수정하지 않는다.** 검사와 판정만 한다.

## 검사 순서 (1번부터 순서대로, 실패하면 그 즉시 해당 상태로 중단)

1. **Working Tree 상태** — `git status`를 실제로 실행한다. `TASK_ID`의 Expected Files와 무관한 미커밋 변경이 남아 있거나, Working Tree가 이 Task를 시작하기에 지저분하면 `BLOCKED_DIRTY_TREE`. 깨끗하거나(또는 같은 Task를 재개하는 것이 명백한 변경만 있으면) 통과.
2. **Wave 소속 확인** — `TASKS/WAVE_PLAN.md`를 읽는다. 파일이 없거나 `WAVE_ID` 항목이 없으면 `BLOCKED_INPUT`. 있으면 그 Wave의 Task 목록에 `TASK_ID`가 포함되어 있는지 확인 — 포함되어 있지 않으면 `BLOCKED_INPUT`(다른 Wave의 Task를 잘못 지정한 것).
3. **Depends On 완료 여부** — `TASKS/TASK-<TASK_ID>.md`의 "Depends On" 절을 읽고, `TASKS/WAVE_STATE.json`을 읽어 각 의존 Task의 상태(각 Wave 객체의 `task_status` 맵, `/run-wave`가 관리)를 확인한다. `TASKS/WAVE_STATE.json`이 없으면 완료 여부를 확인할 수 없으므로 `BLOCKED_INPUT`. 파일은 있지만 하나 이상의 Depends On이 `done`이 아니면 `BLOCKED_DEPENDENCY`(어떤 Task가 미완료인지, 어떤 Wave에 속하는지 구체적으로 밝힌다). 의존 Task가 아직 `task_status`에 없으면 `pending`으로 간주해 동일하게 처리한다.
4. **Expected Files** — 상세 파일의 "Expected Files" 절을 읽고, 각 경로가 실제 `src/app`/`src/`/`supabase/`/`tests/` 트리 기준으로 말이 되는 위치인지(오탈자·존재하지 않는 상위 디렉터리 등) 실제로 `Glob`/`ls`로 확인한다. 목록이 비어 있거나 명백히 틀린 경로가 있으면 `BLOCKED_INPUT`.
5. **SRS·Scope·Design·Screen Ref 확인** — 상세 파일의 "Requirement Ref"에 있는 각 ID가 `docs/PROJECT_SCOPE.md`(=`PROJECT_SCOPE`)에 실제로 존재하고 EXCLUDED가 아닌지, "Screen / Route / Page Entry"가 `design-reference/SCREEN_ROUTE_CONTRACT.json`(=`SCREEN_CONTRACT`)과 일치하는지, "Design Ref"가 `design-reference/D-001/DESIGN.md`(=`DESIGN_PATH`)의 실제 절을 가리키는지 확인한다. 하나라도 실제 문서에서 확인되지 않으면 `BLOCKED_INPUT`.
6. **필요한 환경변수 이름** — Task가 Supabase를 사용하는 종류(`DB-*`, `API-*`, `COMP-SCR005-AUTH` 등)이면 `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`가 실제로 `.env.local`(또는 배포 환경)에 있는지 확인한다(`docs/ARCHITECTURE.md` §15 참고). Supabase가 필요 없는 Task는 이 검사를 통과로 간주한다. 필요한데 없으면 `BLOCKED_INPUT`이며, 없는 환경변수 이름을 정확히 나열한다.
7. **Secret 하드코딩 위험** — Task 범위 안에서 `SUPABASE_SERVICE_ROLE_KEY`나 다른 비밀값을 코드에 직접 쓰거나 Client Component에 노출시킬 계획/기존 코드가 있는지 확인한다(CLAUDE.md 규칙 14·15). 그런 위험이 감지되면 `BLOCKED_SCOPE`.
8. **EXCLUDED 범위 침범 여부** — Task의 Requirement Ref·Expected Files·Forbidden 절을 다시 확인해, `docs/PROJECT_SCOPE.md` §5의 제외 기능(전체 콘텐츠 CMS, 범용 감사 로그, 외부 Email 연동, EC2·AWS, 자동 Merge 등)이나 21개 EXCLUDED Requirement를 구현하려는 계획이 섞여 있지 않은지 확인한다. 섞여 있으면 `BLOCKED_SCOPE`.

모든 검사를 통과하면 **`READY_TO_IMPLEMENT`**를 출력한다.

## 출력

다음 5개 상태 중 정확히 하나를 최상단에 출력한다: `READY_TO_IMPLEMENT` | `BLOCKED_INPUT` | `BLOCKED_DEPENDENCY` | `BLOCKED_DIRTY_TREE` | `BLOCKED_SCOPE`

그 아래에:
- 어느 검사 번호(1~8)에서 그 상태가 나왔는지
- 구체적 근거(파일 경로, 누락된 Depends On ID, 누락된 환경변수 이름 등)
- `READY_TO_IMPLEMENT`인 경우: `TASK_ID`, Expected Files 목록, Functional/Visual/Security AC 요약을 다음 단계(`/implement-task`)가 바로 쓸 수 있게 함께 보고한다
