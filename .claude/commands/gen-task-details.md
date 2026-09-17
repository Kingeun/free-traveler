---
description: TASKS/00_TASK_LIST.md의 각 구현 Task에 대해 TASKS/TASK-<TASK_ID>.md 상세 파일을 1:1로 생성하고, 마지막에 scripts/audit_tasks.py를 실행한다.
---

`traveler-project-pipeline` Skill을 로드하고 그 규칙(§17~§23)을 그대로 따른다. 이 Command는 파이프라인 3~4단계이며, `TASKS/00_TASK_LIST.md`가 이미 존재해야 한다(없으면 먼저 `/gen-tasklist`를 안내하고 중단한다).

## 실행 순서

1. `TASKS/00_TASK_LIST.md`를 실제로 읽는다.
2. `python scripts/build_task_details.py`를 실행한다. 이 스크립트가 다음을 수행한다:
   - Task List의 사전 검사(중복 ID, 필수 열 공백, Depends On 참조 오류, EXCLUDED/Task ID 겹침, DB Task 6개 초과, Page Owner Page Entry 중복)를 통과해야 파일을 쓴다. 실패하면 오류 목록을 그대로 사용자에게 전달하고, `TASKS/00_TASK_LIST.md`를 임의로 고쳐서 통과시키지 않는다 — 무엇이 잘못됐는지 보고하고 사용자 지시를 기다린다.
   - Category별 구현 Task마다 `TASKS/TASK-<TASK_ID>.md`를 Skill §23 스키마(14개 절: Context/Project Scope/Requirement Ref/Screen·Route·Page Entry/Design Ref/Depends On/Expected Files/Functional AC/Visual AC/Security-Privacy AC/Test Cases/Verify/Definition of Done/Forbidden)로 작성한다.
   - **이미 존재하는 상세 파일은 건너뛴다**(덮어쓰지 않는다). 특정 Task의 상세 파일을 다시 만들어야 하면, 그 파일만 먼저 지우고 이 스크립트를 재실행한다 — 스크립트가 자동으로 갱신하지 않는다는 것을 사용자에게 알린다.
3. 스크립트가 생성한 각 상세 파일에서 다음을 실제로 확인한다(스크립트가 이미 반영하지만, 사람이 요청한 예외적 Task라면 다시 확인):
   - `PAGE-SCR001`: Starter 템플릿 제거 AC(Skill §7)
   - `PAGE-SCR003`: 항공·숙소·동행 3탭 실제 조립 AC(Skill §8)
   - `PAGE-SCR005`: Guest/Member/Admin 상태 실제 조립 AC, Dashboard 금지(Skill §9)
   - `COMP-SCR003-FLIGHT-FORM`/`COMP-SCR003-HOTEL-FORM`/`DB-ACCESS`/`E2E-TRAVEL-TOOLS`: 입력값 비전송 AC(Skill §12)
   - `E2E-*`: Playwright `chromium` 전용 AC(Skill §13)
   - `PAGE-SCR001`/`PAGE-SCR004`/`PAGE-SCR005`: 완성형 Empty State AC(Skill §20 — `PAGE-SCR002`/`PAGE-SCR003`은 대상 아님)
4. 상세 파일 작성을 모두 마친 뒤 **반드시** `python scripts/audit_tasks.py`를 실행한다(Skill §18). 이 스크립트는 `TASKS/TASK_MANIFEST.csv`와 `TASKS/TASK_AUDIT_REPORT.md`를 쓰고 18개 규칙(Skill §15 목록)을 검사한다.
5. `audit_tasks.py`가 `AUDIT_FAIL`을 보고하면 **위반 항목을 문서에서 지워서 통과시키지 않는다** — 원인(대개 `TASKS/00_TASK_LIST.md`의 실제 결함이거나 상세 파일 내용 결함)을 고치고 재실행한다. 두 스크립트 중 어느 쪽도 임의로 우회하지 않는다.

## 이 Command가 만들지 않는 것

- `src/**`, `supabase/**` 등 실제 구현 코드 — Task 상세 파일과 감사 산출물만 다룬다.

## 출력 후 보고

- `build_task_details.py`의 생성/건너뜀 개수, `TASKS/00_TASK_LIST.md` 구현 Task 개수와 1:1인지
- `audit_tasks.py` 최종 실행 결과(`AUDIT_PASS`/`AUDIT_FAIL`, 검사 수, 위반 목록)를 **있는 그대로** 보고한다 — FAIL을 요약에서 빼거나 "대체로 통과"처럼 완화해서 말하지 않는다
- FAIL이 남아있다면 그 이유와 다음에 고쳐야 할 파일/항목
- `TASKS/TASK_MANIFEST.csv`·`TASKS/TASK_AUDIT_REPORT.md` 경로
