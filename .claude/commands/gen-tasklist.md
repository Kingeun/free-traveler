---
description: Free Traveler 5개 Screen과 114개 Requirement를 읽어 TASKS/00_TASK_LIST.md(Markdown Task List)를 작성/갱신한다.
---

`traveler-project-pipeline` Skill을 로드하고 그 규칙을 그대로 따른다(특히 §1~§11, §15~§16, §19~§22). 이 Command는 파이프라인 2단계다. 실제 산출물은 `TASKS/00_TASK_LIST.md`(Markdown)이며, `tasks/TASK_LIST.json` 같은 JSON 파일은 만들지 않는다.

## 실행 순서

1. **입력 검증**: `python scripts/validate_inputs.py`를 실제로 실행한다. non-zero exit이면 여기서 멈추고 검증 리포트를 그대로 사용자에게 보여준다. Task List를 만들거나 고치지 않는다.
2. **Screen 정본 재확인**: `design-reference/SCREEN_ROUTE_CONTRACT.json`을 실제로 다시 읽어 `schema_version == "traveler-screen-route-v1"`, `screens` 배열 정확히 5개, `route`·`page_entry` 각각 중복 없음을 확인한다(Skill §1~§2).
3. **Requirement 상태 재확인**: `docs/PROJECT_SCOPE.md`를 실제로 읽어 REQ-FUNC-001~080, REQ-NF-001~034 114개 각각의 IMPLEMENT/EXCLUDED 분류를 가져온다. `docs/UIUX_TRACEABILITY.md`는 화면 매핑 참고용으로만 함께 읽는다.
4. **실제 파일 트리 확인**: `src/app`(및 필요 시 `supabase/`, `tests/`, `scripts/`)를 실제로 스캔해 이미 존재하는 파일과 없는 파일을 구분한다. 확인하지 않고 추정해서 Expected Files를 쓰지 않는다(Skill §4).
5. **기존 Task List 확인**: `TASKS/00_TASK_LIST.md`가 이미 있으면 먼저 전체를 읽는다. 이번 요청이 전체 재작성인지 일부 갱신인지에 따라, 기존에 이미 옳게 기록된 Task 행(Seq, Depends On 등)을 임의로 흔들지 않는다.
6. **Task 분해**: Skill §5·§10~§13, §21 규칙에 따라 Page Owner(정확히 5개, `PAGE-SCR00N`), Component(`COMP-SCR00N-*`/`COMP-GLOBAL-*`/`COMP-TECH-*`), Data(`DATA-*`), Database(4개, `DB-*`), API(`API-*`), Unit/Integration/E2E Test, Manual Check, CI/Infra Task로 분해한다. EC2·AWS·자동 Merge Task는 만들지 않는다(Skill §14).
7. **Requirement 매핑**: IMPLEMENT 93개 각각을 최소 하나의 Task의 Requirement Ref에 배정한다. EXCLUDED 21개는 Task를 만들지 않고 "1. NON_IMPLEMENTATION" 표에 `docs/PROJECT_SCOPE.md`의 제외 사유를 인용해 기록한다(Skill §15~§16). 어느 쪽에도 빠지는 Requirement가 없어야 한다.
8. **의존 관계**: 각 `PAGE-SCR00N`의 Depends On에 같은 Screen의 모든 `COMP-SCR00N-*` Task ID(+필요 시 `COMP-GLOBAL-*`)를 포함한다(Skill §6).
9. **작성**: Skill §22의 Markdown 표 스키마(열 순서: `Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files`)에 맞춰 `TASKS/00_TASK_LIST.md`를 쓴다. Page Owner AC에는 §19~§20 규칙(Section 순서, 최소 콘텐츠 수, Empty State)을 프로즈로 포함한다.

## 이 Command가 만들지 않는 것

- `TASKS/TASK-<TASK_ID>.md` 상세 파일 — `/gen-task-details`의 책임이다.
- `src/**`, `supabase/**` 등 실제 구현 코드 — 이 파이프라인의 어떤 단계도 구현 코드를 만들지 않는다.

## 출력 후 보고

- 생성/갱신된 Task 총개수와 Category별 개수(참고치일 뿐 완료 조건 아님)
- Page Owner 5개 목록과 각 Route/Page Entry
- DB Task 4개, Database 테이블 6개 확인
- EXCLUDED Requirement 개수(21개와 일치하는지)
- 이번 갱신으로 기존 `TASKS/TASK-*.md` 상세 파일 중 내용이 달라져야 하는 Task ID가 있다면 명시하고, `/gen-task-details` 재실행이 필요함을 안내한다
- `python scripts/audit_tasks.py`를 실행해 현재 상태를 확인하고, 결과(AUDIT_PASS/AUDIT_FAIL)를 그대로 보고한다 — FAIL이 나와도 임의로 숨기거나 무시하지 않는다. FAIL의 원인이 아직 만들지 않은 상세 파일(1:1 불일치)뿐이라면 그 사실을 명시하고 `/gen-task-details`로 이어가라고 안내한다
