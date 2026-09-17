# WAVE_PLAN — Free Traveler 실행 Wave 계획

`scripts/build_waves.py`가 `TASKS/TASK_MANIFEST.csv`의 Depends On을 바탕으로 생성했다.
여기 적힌 Wave ID가 `/run-wave`·`TASKS/WAVE_STATE.json`이 사용하는 정본이다 — W00~W10으로
미리 고정하지 않고, 실제 Task 수·의존관계·파일 충돌에 따라 그룹당 1개 이상의 Wave로 나뉜다.

## Wave 배치 규칙 요약

1. 순환 의존성은 0이어야 하며, 있으면 이 문서 자체가 생성되지 않는다.
2. 선행 Task는 항상 그 Task보다 앞선 Wave에만 배치된다(같은 Wave에도 배치하지 않는다 — rule 6이 한 Wave 안에서도 Task ID 순으로 하나씩 실행하도록 정했기 때문에, 의존 관계가 있는 두 Task를 같은 Wave에 두면 Task ID 정렬이 우연히 의존 순서와 어긋날 때 실행 순서가 깨질 수 있다).
3. Wave당 기본 4~7개를 목표로 하되, 실제 의존 사슬이 그보다 좁으면(예: DB Schema→RLS→Access처럼 한 단계씩 순차 의존) 규칙 2를 지키기 위해 더 작은 Wave가 된다 — 이는 결함이 아니라 의존 구조를 정직하게 반영한 결과다.
4. Page Owner는 해당 Screen 그룹의 마지막 Wave에 단독으로 배치되고, 사람 Preview Checkpoint가 걸린다.
5. 같은 Wave 안에서 Expected Files가 겹치는 Task가 있으면 자동으로 다음 Wave로 분리한다.
6. 한 Wave 안에서도 Task ID 순으로 한 Task씩 실행한다.
7. 자동 Branch·PR·Merge 기능은 포함하지 않는다(생성 스크립트도, 이 계획서도 그런 기능을 정의하지 않는다).

## Wave 그룹 순서(10개)

| 그룹 | 제목 | 매칭된 Task 수 |
|---|---|---|
| 1 | Scaffold, 문서, Harness 확인 | 0 (현재 Task List에 매칭되는 Task 없음 — Task 목록 밖의 사전 점검 단계) |
| 2 | Airbnb 스타일 공통 UI, 정적 데이터, Layout | 12 |
| 3 | Supabase Auth, 6개 Table, 기본 RLS | 9 |
| 4 | SCR-001 메인 Component와 Page Owner | 9 |
| 5 | SCR-002 대표 소개 Component와 Page Owner | 8 |
| 6 | SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner | 8 |
| 7 | SCR-004 동행 목록·상세·신청 Component와 Page Owner | 7 |
| 8 | SCR-005 계정·내 활동·간단 관리자 Component와 Page Owner | 6 |
| 9 | Unit·Playwright·접근성·CI | 11 |
| 10 | Vercel Preview와 Release 확인 | 1 |

## Wave 목록

| Wave ID | 그룹 | Task 수 | Checkpoint 필요 | Task ID 목록 |
|---|---|---|---|---|
| W01 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | 5 | 아니오 | COMP-GLOBAL-DESIGN-TOKENS, COMP-GLOBAL-EMPTY-STATE, DATA-DESTINATIONS, DATA-REPRESENTATIVE, DATA-SAFETY |
| W02 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | 7 | 아니오 | COMP-GLOBAL-ERROR-STATE, COMP-GLOBAL-HEADER-FOOTER, COMP-GLOBAL-LOADING-STATE, COMP-GLOBAL-TOAST, COMP-TECH-ERROR-PAGES, COMP-TECH-POLICY-PAGES, DATA-VALIDATION-SCRIPT |
| W03 | 3. Supabase Auth, 6개 Table, 기본 RLS | 1 | 아니오 | DB-SCHEMA-BASE |
| W04 | 3. Supabase Auth, 6개 Table, 기본 RLS | 2 | 아니오 | DB-RLS-BASE, DB-SEED-BASE |
| W05 | 3. Supabase Auth, 6개 Table, 기본 RLS | 1 | 아니오 | DB-ACCESS |
| W06 | 3. Supabase Auth, 6개 Table, 기본 RLS | 4 | 아니오 | API-ADMIN-SETTINGS, API-AUTH-PROFILE, API-BLOCKS-REPORTS, API-MATE-POSTS |
| W07 | 3. Supabase Auth, 6개 Table, 기본 RLS | 1 | 아니오 | API-MATE-APPLICATIONS |
| W08 | 4. SCR-001 메인 Component와 Page Owner | 5 | 아니오 | COMP-SCR001-DEST-DRAWER, COMP-SCR001-FOUNDER-BAND, COMP-SCR001-HERO-SEARCH, COMP-SCR001-MATES-TEASER, COMP-SCR001-SAFETY-PANEL |
| W09 | 4. SCR-001 메인 Component와 Page Owner | 2 | 아니오 | COMP-SCR001-DOMESTIC-GRID, COMP-SCR001-OVERSEAS-GRID |
| W10 | 4. SCR-001 메인 Component와 Page Owner | 1 | 아니오 | COMP-SCR001-THEME-CHIPS |
| W11 | 4. SCR-001 메인 Component와 Page Owner | 1 | 예 | PAGE-SCR001 |
| W12 | 5. SCR-002 대표 소개 Component와 Page Owner | 7 | 아니오 | COMP-SCR002-COUNTRY-CHIPS, COMP-SCR002-GALLERY, COMP-SCR002-HERO, COMP-SCR002-INTRO, COMP-SCR002-MEMORABLE-CTA, COMP-SCR002-STATS, COMP-SCR002-TIMELINE |
| W13 | 5. SCR-002 대표 소개 Component와 Page Owner | 1 | 예 | PAGE-SCR002 |
| W14 | 6. SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner | 3 | 아니오 | COMP-SCR003-INTRO-TABS-SHELL, COMP-SCR003-MATE-LOGIN-GATE, COMP-SCR003-TIPS |
| W15 | 6. SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner | 3 | 아니오 | COMP-SCR003-FLIGHT-FORM, COMP-SCR003-HOTEL-FORM, COMP-SCR003-MATE-WRITE-FORM |
| W16 | 6. SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner | 1 | 아니오 | COMP-SCR003-SUMMARY-ACTION |
| W17 | 6. SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner | 1 | 예 | PAGE-SCR003 |
| W18 | 7. SCR-004 동행 목록·상세·신청 Component와 Page Owner | 1 | 아니오 | COMP-SCR004-FILTER-BAR |
| W19 | 7. SCR-004 동행 목록·상세·신청 Component와 Page Owner | 1 | 아니오 | COMP-SCR004-POST-LIST |
| W20 | 7. SCR-004 동행 목록·상세·신청 Component와 Page Owner | 1 | 아니오 | COMP-SCR004-DETAIL-PANEL |
| W21 | 7. SCR-004 동행 목록·상세·신청 Component와 Page Owner | 3 | 아니오 | COMP-SCR004-APPLY-FORM, COMP-SCR004-BLOCK-ACTION, COMP-SCR004-REPORT-ACTION |
| W22 | 7. SCR-004 동행 목록·상세·신청 Component와 Page Owner | 1 | 예 | PAGE-SCR004 |
| W23 | 8. SCR-005 계정·내 활동·간단 관리자 Component와 Page Owner | 4 | 아니오 | COMP-SCR005-ADMIN-REPORTS, COMP-SCR005-ADMIN-URL-SETTINGS, COMP-SCR005-AUTH, COMP-SCR005-MY-ACTIVITY |
| W24 | 8. SCR-005 계정·내 활동·간단 관리자 Component와 Page Owner | 1 | 아니오 | COMP-SCR005-PROFILE |
| W25 | 8. SCR-005 계정·내 활동·간단 관리자 Component와 Page Owner | 1 | 예 | PAGE-SCR005 |
| W26 | 9. Unit·Playwright·접근성·CI | 5 | 아니오 | E2E-MATE-AUTH, E2E-PUBLIC-SMOKE, E2E-TRAVEL-TOOLS, MANUAL-ACCESSIBILITY-KEYBOARD, MANUAL-PERFORMANCE-LIGHTHOUSE |
| W27 | 9. Unit·Playwright·접근성·CI | 5 | 아니오 | MANUAL-RESPONSIVE-DENSITY, TEST-RLS-BASIC, UNIT-CONTACT-DETECTION, UNIT-MATE-STATE, UNIT-TRAVEL-DATES |
| W28 | 9. Unit·Playwright·접근성·CI | 1 | 아니오 | CI-QUALITY-GATE |
| W29 | 10. Vercel Preview와 Release 확인 | 1 | 예 | RELEASE-CHECK-VERCEL-SUPABASE |

## Checkpoint 안내

`checkpoint_required=예`인 Wave는 CLAUDE.md 규칙 22에 따라 사람이 Preview를 확인해야 다음 Wave로 진행한다(`/run-wave`가 해당 Wave 완료 후 `WAITING_FOR_PREVIEW`로 멈춘다). SCR-001~005 Page Owner Wave 5개와 최종 `RELEASE-CHECK-VERCEL-SUPABASE` Wave가 여기 해당한다.
