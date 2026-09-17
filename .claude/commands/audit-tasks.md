---
description: scripts/audit_tasks.py를 실행해 현재 TASKS/ 상태(Task List·상세 파일·18개 규칙 준수)를 재검사한다.
---

`traveler-project-pipeline` Skill(§15, §17~§18)을 기준으로 `TASKS/00_TASK_LIST.md`와 `TASKS/TASK-*.md`의 현재 상태를 감사한다. Task를 새로 만들거나 고치지 않고 **감사만** 한다.

## 실행 순서

1. `python scripts/audit_tasks.py`를 실제로 실행한다.
2. `TASKS/00_TASK_LIST.md`가 없으면 스크립트가 `NOT_GENERATED`(exit 2) 상태를 보고한다 — 이 경우 `/gen-tasklist`부터 실행하라고 안내하고 끝낸다.
3. 스크립트가 쓴 `TASKS/TASK_MANIFEST.csv`와 `TASKS/TASK_AUDIT_REPORT.md`를 실제로 읽고, 콘솔 출력과 함께 그 내용을 사용자에게 전달한다.
4. 위반이 있어도 이 Command에서 임의로 문서를 수정하지 않는다 — 수정은 `/gen-task-details` 재실행 또는 사용자의 직접 지시가 있을 때만 한다. **위반을 축소해서 보고하거나 "대체로 문제 없음"처럼 무시하지 않는다.**

## 보고 형식

- 전체 판정: `AUDIT_PASS` 또는 `AUDIT_FAIL`(+ `NOT_GENERATED`인 경우 그 사실)
- 18개 검사 각각의 PASS/FAIL(Skill §15 목록 순서와 동일)
- FAIL인 항목의 구체적 Task ID·Requirement ID와 사유
- `TASKS/TASK_MANIFEST.csv`·`TASKS/TASK_AUDIT_REPORT.md` 경로
