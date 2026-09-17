---
description: 하나의 Wave 안에 있는 Task를 Task ID 순으로 하나씩 prepare·implement한다. `/run-wave W08`, `/run-wave W08 --status`, `/run-wave W08 --dry-run`, `/run-wave W08 --resume`를 지원한다.
---

`traveler-project-pipeline` Skill과 `/prepare-task`·`/implement-task`의 규칙을 그대로 따른다. 이 Command 자신은 새로운 검사·구현 규칙을 추가하지 않는다 — 오직 두 Command를 Wave 단위로 순서대로 호출하는 오케스트레이션과, 그 결과를 `TASKS/WAVE_STATE.json`에 기록하는 책임만 가진다.

## 상태 파일 (실제로 존재한다 — 추정하지 않고 매번 다시 읽는다)

- **`TASKS/WAVE_PLAN.md`** — `scripts/build_waves.py`가 생성한 정본. Wave ID(`W01`~`W29`)별 그룹·Task ID 목록·Checkpoint 필요 여부가 표로 들어 있다.
- **`TASKS/WAVE_STATE.json`** — 이 Command가 실행마다 갱신하는 살아있는 상태 파일. 각 Wave 객체는 최소 `wave_id`/`title`/`task_ids`/`status`(`pending`|`in_progress`|`blocked`|`completed`)/`checkpoint_required`/`checkpoint_result`를 가진다.
  - **Task별 상태 확장**: `build_waves.py`는 Wave 단위 상태만 만든다. 이 Command는 각 Wave 객체에 `task_status`(Task ID → `pending`|`in_progress`|`done`|`blocked`) 필드를 추가로 관리한다 — 처음 그 Wave를 건드릴 때 없으면 `task_ids` 전체를 `pending`으로 채워 넣는다. 기존 `wave_id`/`title`/`task_ids`/`status`/`checkpoint_required`/`checkpoint_result` 필드는 그대로 유지한다(값만 갱신).

두 파일 모두 실제로 읽는다 — 내용을 추정하거나 기억으로 대체하지 않는다. `TASKS/00_TASK_LIST.md`나 `TASKS/TASK-*.md`의 실제 상태가 이 파일들의 가정과 다르면(예: 사용자가 직접 코드를 수정함) 실제 파일을 다시 읽어 반영한다.

## 호출 형식

```
/run-wave <WAVE_ID>              기본: 이 Wave의 pending Task를 하나씩 prepare·implement한다.
/run-wave <WAVE_ID> --status     실행하지 않는다. 이 Wave와 Task별 상태만 보여준다.
/run-wave <WAVE_ID> --dry-run    실행하지 않는다. 실행될 Task·파일·검증·Checkpoint만 미리 보여준다.
/run-wave <WAVE_ID> --resume     이 Wave의 첫 pending 또는 blocked Task부터 다시 시작한다.
```

`WAVE_ID`는 항상 필요하다. `TASKS/WAVE_PLAN.md`에 없는 `WAVE_ID`면 즉시 중단하고 "Wave 계획 없음(`<WAVE_ID>`)"을 보고한다(임의로 Wave 구성을 만들어내지 않는다).

## Wave 상태 계산 규칙 (모든 모드가 공유)

`task_status`를 갱신한 뒤, 그 Wave의 `status`는 항상 아래 순서로 다시 계산한다(임의로 다른 값을 쓰지 않는다):

1. `task_status` 중 하나라도 `blocked`면 → `status = blocked`.
2. 전부 `done`이면 → `checkpoint_required`가 `true`이고 `checkpoint_result`가 아직 PASS로 채워지지 않았으면 `status = in_progress`(Checkpoint 대기, 규칙 5). `checkpoint_required`가 `false`거나 `checkpoint_result`가 PASS면 `status = completed`.
3. 하나 이상이 `done` 또는 `in_progress`이지만 전부는 아니면 → `status = in_progress`.
4. 전부 `pending`이면 → `status = pending`.

## 규칙 1: 이전 Wave가 completed가 아니면 시작하지 않는다

`--status`를 제외한 모든 모드에서: `TASKS/WAVE_STATE.json`의 `waves` 배열에서 `WAVE_ID` 바로 앞에 있는 Wave를 찾는다(첫 Wave면 이 검사를 건너뛴다). 그 Wave의 `status`가 `completed`가 아니면 즉시 중단하고 `WAVE_NOT_STARTED(이전 Wave <ID> 미완료)`를 보고한다 — Task를 하나도 건드리지 않는다. (`in_progress`로 멈춘 이전 Wave는 대개 규칙 5의 Checkpoint 대기 상태이므로, 힌트에 "사람 Preview 확인 필요"를 함께 적는다.)

## 기본 모드: `/run-wave <WAVE_ID>`

1. 규칙 1을 검사한다.
2. `task_status`가 없으면 그 Wave의 모든 Task를 `pending`으로 초기화한다.
3. `task_status`가 `pending`인 Task를 **Task ID 사전순**으로 하나 고른다(Wave 안에는 서로 의존하는 Task가 없도록 이미 나뉘어 있으므로 Depends On 순서를 다시 따질 필요가 없다 — `TASKS/WAVE_PLAN.md` 규칙 6).
4. 그런 Task가 없으면(전부 `done`/`blocked`) 5단계로 간다.
5. 골라낸 Task에 `/prepare-task <WAVE_ID> <TASK_ID>`를 실행한다.
   - `READY_TO_IMPLEMENT`가 아니면: 이 Task의 `task_status`를 `blocked`로 기록하고, Wave 상태를 위 계산 규칙대로 갱신한 뒤 **그 자리에서 멈춘다**(규칙 2 — 다른 Task로 건너뛰어 계속하지 않는다).
   - `READY_TO_IMPLEMENT`면 이 Task의 `task_status`를 `in_progress`로 기록하고 `/implement-task`로 구현한다.
6. `/implement-task`가 보고한 검증(그 Task 상세 파일의 "Verify" 절에 명시된 최소 검증 — 규칙 3)이 모두 PASS면 `task_status`를 `done`으로 갱신한다. 하나라도 FAIL이면 `blocked`로 기록하고 멈춘다(규칙 2).
7. Wave의 모든 Task가 `done`이 될 때까지 3번으로 반복한다.
8. 전부 `done`이 되면:
   - Wave에 **Page Owner Task가 있으면**(`TASKS/00_TASK_LIST.md` 기준 Category가 Page Owner인 Task, 즉 이 Wave가 그 Screen의 마지막 통합 Wave라면 — 규칙 4) `checkpoint_required`가 이미 `true`로 표시되어 있어야 한다. 사람이 실제로 Preview를 확인했다는 지시를 받기 전까지는 `checkpoint_result`를 채우지 않는다(규칙 5) — "## Browser Checkpoint 확인" 절차를 따른다.
   - Checkpoint가 필요 없으면(`checkpoint_required=false`) Wave 상태가 자동으로 `completed`가 된다.

## `--status`

Task/구현을 진행하지 않는다. `TASKS/WAVE_STATE.json`에서 `WAVE_ID`의 `status`·`checkpoint_required`·`checkpoint_result`와 각 Task의 `task_status`를 그대로 나열한다. `task_status`가 아직 없으면 전부 `pending`으로 간주해 보여준다(파일을 수정하지는 않는다).

## `--dry-run`

아무 파일도 수정하지 않는다(`TASKS/WAVE_STATE.json` 포함). 규칙 1을 먼저 확인해 이미 시작할 수 없는 상태면 그 사실만 보고한다. 시작할 수 있으면, 기본 모드의 3~5단계를 "만약 지금 실행한다면"의 시뮬레이션으로 수행한다 — 즉 `task_status=pending`인 Task를 Task ID 순으로 훑으며 각각 `/prepare-task`까지는 실제로 실행해 판정을 보되, **`/implement-task`는 절대 호출하지 않는다.** 첫 `BLOCKED_*` 판정이 나오면 그 이후 Task는 보지 않고 멈춘다(실제 실행 시 규칙 2로 멈출 지점과 동일하게 보여준다). 각 Task마다 Expected Files, Verify에 필요한 최소 검증, 그리고 이 Wave에 Browser Checkpoint가 걸려 있는지를 함께 보여준다.

## `--resume`

`TASKS/WAVE_STATE.json`에서 이 Wave의 `task_status`를 읽어 **Task ID 사전순으로 처음 나오는 `pending` 또는 `blocked` Task**부터 기본 모드의 3~8단계를 이어서 실행한다(이미 `done`인 Task는 다시 건드리지 않는다). `blocked`였던 Task를 다시 시도하는 것이므로, 그 Task가 왜 `blocked`였는지(직전 `/prepare-task`/`/implement-task` 결과)를 먼저 요약해 보여준 뒤 같은 절차를 반복한다. Wave 자체가 이미 `completed`면 재개할 것이 없다고 보고하고 멈춘다.

## Browser Checkpoint 확인

Page Owner Task가 `done`이 되어 Wave의 나머지가 전부 끝났는데 `checkpoint_required=true`인 경우:

1. 이 Command는 스스로 브라우저를 열어 확인하지 않는다 — **사람이 실제로 배포본/로컬 미리보기를 눈으로 확인**하고 그 결과를 알려줘야 한다(CLAUDE.md 규칙 22).
2. 사람이 "SCR-00N Preview 확인함, PASS" 또는 그에 준하는 명확한 확인을 알려주면: 해당 Screen의 `docs/preview-checks/SCR-00N.md`에 확인 시각·확인자·PASS 여부를 기록하고(파일이 없으면 새로 만든다 — `scripts/check_screen_contract.py --mode=release`가 이 파일을 확인한다), `TASKS/WAVE_STATE.json`의 이 Wave `checkpoint_result`를 `"PASS"`로, `status`를 `completed`로 갱신한다.
3. 사람이 문제를 지적하면(NEEDS_REVISION 등) `checkpoint_result`에 그 내용을 기록하고 Wave는 `completed`로 바꾸지 않는다 — 다음 Wave로 진행하지 않는다.
4. 확인 지시가 아직 없으면 이 Wave는 `in_progress`로 남고, 다음 Wave(`/run-wave <다음 WAVE_ID>`)는 규칙 1에 의해 시작되지 않는다.

## 이 Command가 하지 않는 것

- Git Branch 생성, Commit, Push, PR 생성, Merge — 어떤 모드에서도 자동으로 수행하지 않는다(규칙 6, CLAUDE.md 규칙 21).
- `/implement-task`가 이미 지키는 Expected Files 경계·AC 범위를 이 Command가 다시 검사하거나 완화하지 않는다 — 그대로 위임한다.
- Wave 순서·그룹 구성을 임의로 바꾸지 않는다 — `TASKS/WAVE_PLAN.md`가 정본이며, 구성을 바꿔야 하면 `scripts/build_waves.py`를 다시 실행하는 별도 작업으로 처리한다.

## 종료 보고

- **완료 Task**: 이번 실행에서 `done`이 된 Task ID 목록
- **변경 파일**: 완료된 각 Task의 Expected Files(실제 `git diff --stat` 결과와 대조)
- **통과한 검사**: Task별로 실행되어 PASS한 검증(Unit Test/Playwright/포맷 등, `/implement-task` 보고를 그대로 취합)
- **남은 수동 Browser 확인**: `checkpoint_required=true`인데 `checkpoint_result`가 아직 없는 Wave/Screen 목록(없으면 "없음")
- **다음에 입력할 명령**: 다음으로 사람이 실행하면 되는 정확한 명령 한 줄
  - Wave가 `blocked`로 멈췄으면 → `/run-wave <WAVE_ID> --resume`(먼저 그 Task를 막은 원인 해결)
  - Wave가 Checkpoint 대기(`in_progress`+`checkpoint_required`)면 → "SCR-00N Preview를 확인한 뒤 결과를 알려주세요"
  - Wave가 `completed`이고 다음 Wave가 있으면 → `/run-wave <다음 WAVE_ID>`
  - 마지막 Wave까지 `completed`면 → `/release-check`
