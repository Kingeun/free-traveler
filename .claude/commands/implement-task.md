---
description: /prepare-task가 READY_TO_IMPLEMENT로 판정한 Task 하나를 실제로 구현한다. Expected Files 밖은 건드리지 않는다.
---

`traveler-project-pipeline` Skill과 CLAUDE.md의 "Task 완료 순서"(Task 읽기 → 입력 확인 → 구현 → 관련 포맷·Unit Test → 필요 시 Playwright → Diff 확인 → 완료 보고)를 그대로 따른다.

## 전제 조건

이 Command는 **`/prepare-task`가 해당 Task를 `READY_TO_IMPLEMENT`로 판정했을 때만** 실행한다. `READY_TO_IMPLEMENT` 판정을 받지 않았다면 먼저 `/prepare-task <WAVE_ID> <TASK_ID>`를 실행하고, 그 결과가 `READY_TO_IMPLEMENT`가 아니면 이 Command를 진행하지 않고 그 상태(`BLOCKED_*`)를 그대로 보고한다.

## 규칙

1. 한 번의 실행에서 **`READY_TO_IMPLEMENT`인 Task 하나만** 구현한다. 여러 Task를 한 번에 묶어서 구현하지 않는다.
2. `TASKS/TASK-<TASK_ID>.md`의 "Expected Files" 절에 실제로 나열된 파일만 생성·수정한다. 그 밖의 파일(다른 Task의 Expected Files, 설정 파일 등)은 건드리지 않는다 — 필요하다고 판단되면 먼저 사용자에게 알리고 지시를 받는다.
3. 상세 파일의 Functional AC·Visual AC·Security/Privacy AC를 모두 실제로 만족시킨다. AC에 없는 기능을 추가하지 않는다(범위 확장 금지).
4. Task가 Page Owner(`PAGE-SCR00N`)이면 Depends On에 있는 Component/Data/API Task의 결과물을 실제로 import해서 Page Entry(`src/app/**/page.tsx`)에 조립한다 — 새 하위 Component를 이 Task 안에서 만들지 않는다.
5. `TASKS/TASK-<TASK_ID>.md`의 "Verify" 절에 Unit Test(`UNIT-*`, `TEST-RLS-BASIC`)가 있으면 실제로 실행한다(`npm test` 또는 해당 Vitest 명령). 실패하면 구현을 완료로 보고하지 않는다.
6. Playwright Smoke(`E2E-*`)는 이 Task가 **Page Owner이거나 E2E Test 자신일 때만** 실행한다. Component/Data/DB/API/Unit Test 등 그 외 Category는 Playwright를 실행하지 않는다(불필요한 브라우저 구동 금지).
7. AWS·EC2 인프라, Prisma 등 ORM, 자동 Merge/자동 PR 기능을 추가하지 않는다(CLAUDE.md 규칙 12·13·15·17·21과 동일).
8. 작업 중 Task 범위를 넘는 결함을 발견해도 그 자리에서 고치지 않는다 — Expected Files 밖이면 발견 사실만 보고하고 다른 Task/사용자 지시로 넘긴다.

## Git — 기본적으로 Commit·Push·PR을 하지 않는다

- 기본 동작: 코드만 수정하고 **Commit, Push, PR 생성을 하지 않는다.** 변경사항은 Working Tree에 그대로 남긴다.
- 사용자가 명시적으로 요청하면 **이 Task 하나에 대한 Commit까지만** 수행할 수 있다(Task ID를 커밋 메시지에 포함). Push나 PR 생성은 사용자가 별도로 명시적으로 요청하지 않는 한 하지 않는다.
- destructive Git 명령(`reset --hard`, `checkout --`, `clean -f`, force push 등)은 사용자가 명시적으로 요청하지 않는 한 사용하지 않는다.

## 완료 순서

1. `TASKS/TASK-<TASK_ID>.md` 읽기
2. Depends On 결과물·Expected Files·환경변수 등 입력 확인
3. Expected Files 안에서 구현
4. 관련 포맷(ESLint/TypeScript) 확인 + 관련 Unit Test 실행(규칙 5)
5. 필요 시(규칙 6) Playwright Smoke 실행
6. `git diff`로 변경 범위가 Expected Files와 정확히 일치하는지 확인
7. 완료 보고

## 출력 후 보고

- 변경한 파일 목록(Expected Files와 1:1 대조)
- 실행한 검증(Unit Test/Playwright/포맷)과 결과(PASS/FAIL)
- AC 중 충족하지 못한 항목이 있다면 명시(완료로 보고하지 않음)
- 남은 제약: 이 Task가 의존하는 다른 미완료 Task, Playwright/Unit Test를 실행하지 못한 이유(환경 미구성 등), Commit/Push 여부
