---
description: 하나의 Wave 안에 있는 Task들을 Depends On 순서로 하나씩 검사·구현한다. `/run-wave W03`, `/run-wave status`, `/run-wave resume`, `/run-wave dry-run W03`를 지원한다.
---

`traveler-project-pipeline` Skill과 `/prepare-task`·`/implement-task`의 규칙을 그대로 따른다. 이 Command 자신은 새로운 검사·구현 규칙을 추가하지 않는다 — 오직 두 Command를 Wave 단위로 순서대로 호출하는 오케스트레이션만 한다.

## 상태 파일

- `TASKS/WAVE_PLAN.md` — Wave별로 어떤 Task ID가 속하는지, 각 Wave 끝에 사람의 Preview Checkpoint가 있는지 정의한다(Markdown 표). **이 파일은 아직 만들어지지 않았을 수 있다** — DEC-010(`docs/DECISION_LOG.md`)에 따라 Wave 구성 자체가 아직 확정되지 않았다면 이 Command는 Wave를 진행할 수 없다.
- `TASKS/WAVE_STATE.md` — Task별 현재 상태(`PENDING`/`READY`/`IN_PROGRESS`/`DONE`/`BLOCKED_INPUT`/`BLOCKED_DEPENDENCY`/`BLOCKED_DIRTY_TREE`/`BLOCKED_SCOPE`)를 기록한다. 없으면 모든 Task를 `PENDING`으로 간주하고 이번 실행에서 새로 만든다.

두 파일 모두 실제로 읽는다 — 내용을 추정하거나 기억으로 대체하지 않는다.

## `/run-wave <WAVE_ID>` (예: `/run-wave W03`)

1. `TASKS/WAVE_PLAN.md`와 `TASKS/WAVE_STATE.md`를 읽는다. `WAVE_PLAN.md`가 없거나 `<WAVE_ID>`가 그 안에 없으면 즉시 중단하고 "Wave 계획 없음"을 보고한다(임의로 Wave 구성을 만들어내지 않는다).
2. 이 Wave에 속한 Task 중 Depends On이 모두 `DONE`인 Task를 Depends On 순서(의존이 적은 것 먼저)로 하나 고른다. 그런 Task가 없으면(전부 `DONE`이거나 전부 대기 중이면) 3~4단계로 가지 않고 종료 처리(§7~§8)로 넘어간다.
3. 선택한 Task에 `/prepare-task <WAVE_ID> <TASK_ID>`를 실행한다.
   - `READY_TO_IMPLEMENT`가 아니면 `TASKS/WAVE_STATE.md`에 해당 `BLOCKED_*` 상태를 기록하고, 그 Task는 건너뛴 뒤 같은 Wave의 다른 READY Task가 있으면 2번으로 돌아간다. 없으면 종료 처리(§7~§8)로 넘어간다.
4. `READY_TO_IMPLEMENT`면 `TASKS/WAVE_STATE.md`에 `IN_PROGRESS`로 기록하고 `/implement-task`로 그 Task 하나를 구현한다.
5. `/implement-task`가 보고한 검증(Unit Test/Playwright/AC)이 모두 PASS면 `TASKS/WAVE_STATE.md`에 `DONE`으로 갱신한다. 하나라도 FAIL이면 `BLOCKED_INPUT`(또는 실패 성격에 맞는 상태)으로 기록하고 이 Task를 완료로 처리하지 않는다.
6. 같은 Wave의 다음 READY Task로 2번을 반복한다.
7. 이 Wave의 모든 Task가 `DONE`이면 종료하고 `WAVE_COMPLETE`를 보고한다.
8. `WAVE_PLAN.md`에 이 Wave 끝에 사람 Preview Checkpoint가 정의되어 있으면(모든 Task가 `DONE`이더라도) `WAITING_FOR_PREVIEW`로 종료한다 — 사람이 실제로 Preview를 확인했다는 지시가 있어야 다음 Wave로 진행한다(CLAUDE.md 규칙 22).

세션 도중 언제든 `TASKS/00_TASK_LIST.md`나 각 `TASKS/TASK-*.md`의 실제 상태가 이 WAVE_STATE.md의 가정과 다르면(예: 사용자가 직접 코드를 수정함) 실제 파일을 다시 읽어 반영한다.

## `/run-wave status`

Task/구현을 진행하지 않는다. `TASKS/WAVE_STATE.md`(있으면)와 `TASKS/WAVE_PLAN.md`를 읽어 다음만 보고한다: 현재 Wave, 그 Wave의 Task별 상태, 전체 Wave 중 완료된 Wave 수. 파일이 없으면 "Wave 진행 기록 없음"을 그대로 보고한다.

## `/run-wave resume`

`TASKS/WAVE_STATE.md`에서 아직 `DONE`이 아닌 Task가 있는 가장 이전 Wave를 찾아 그 `WAVE_ID`로 `/run-wave <WAVE_ID>`를 이어서 실행한다. 상태 파일이 없으면 재개할 대상이 없다고 보고하고 중단한다.

## `/run-wave dry-run <WAVE_ID>`

1~2단계까지만 실제로 수행하고(다음에 선택될 Task 확인), 3단계의 `/prepare-task`까지는 실행해 판정을 보여주되 **4단계(`implement-task`)는 실행하지 않는다.** "이번에 진행됐다면 어떤 Task가 어떤 판정을 받았을지"를 보고하고 아무 파일도 바꾸지 않는다(`TASKS/WAVE_STATE.md`도 갱신하지 않음).

## 이 Command가 하지 않는 것

- Git Branch 생성, PR 생성, Merge — 어떤 경우에도 자동으로 수행하지 않는다(CLAUDE.md 규칙 21).
- `/implement-task`가 이미 지키는 Expected Files 경계·AC 범위를 이 Command가 다시 검사하거나 완화하지 않는다 — 그대로 위임한다.

## 출력 후 보고

- 이번 실행에서 시도한 Task ID 목록과 각각의 최종 상태
- Wave 전체 상태(`WAVE_COMPLETE` / `WAITING_FOR_PREVIEW` / 진행 중 / Wave 계획 없음)
- `docs/PROJECT_STATE.md`가 존재하면 Current Wave/Current Task/Completed Tasks/Blocked Tasks 필드를 이번 결과에 맞게 갱신한다(그 문서 자체의 필드 정의를 임의로 바꾸지 않는다)
