# UI·UX Traceability Matrix — Free Traveler

**Document ID:** UIUXT-TRAVEL-001
**기반 문서:** `docs/02_SRS_BASELINE.md`, `docs/PROJECT_SCOPE.md`, `docs/03_UI_COVERAGE_ANALYSIS.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, `docs/STITCH_VALIDATION_REPORT.md`, `docs/06_SRS_UIUX_REVISED.md`
**대상:** REQ-FUNC-001~080, REQ-NF-001~034 (총 114개) 전수

---

## 열 정의 및 표기 규칙

| 열 | 정의 |
|---|---|
| **Requirement** | `02_SRS_BASELINE.md`의 Requirement ID |
| **Implementation Status** | `PROJECT_SCOPE.md`를 그대로 인용한 범위 결정. `IMPLEMENT` / `IMPLEMENT (축소·간소화·대체)` / `EXCLUDED` |
| **Screen** | 이 요구사항을 충족하는 디자인 Screen(SCR-001~005). UI로 나타나지 않는 요구사항은 `N/A`, 5개 Screen에 공통 적용되면 `전역`, 5개 Screen에 포함되지 않는 정책/오류 페이지는 `기술 Route` |
| **Route** | Screen에 대응하는 Next.js Route(`design-reference/SCREEN_ROUTE_CONTRACT.json` 기준) |
| **Page Entry** | Route에 대응하는 실제 파일 경로 |
| **Task** | 구현 작업 단위 ID. **Task가 아직 생성되지 않았으므로 전항목 `PENDING_TASK_GENERATION`으로 기록한다.** |
| **Test** | `02_SRS_BASELINE.md` §5.1 명명 규칙(`REQ-FUNC-XXX` ↔ `TC-FUNC-XXX`, `REQ-NF-XXX` ↔ `TC-NF-XXX`)에 따른 예정 테스트 ID. **어떤 테스트 코드도 아직 작성되지 않았다.** 이 열의 값은 "앞으로 사용할 식별자"이지 "이미 작성된 테스트"가 아니다. |
| **Status** | 현재 실제 진행 상태(아래 어휘 중 하나). 구현되지 않은 것을 구현된 것으로 기록하지 않는다. |

**Status 어휘:**

| 값 | 의미 |
|---|---|
| `EXCLUDED` | 이번 범위에서 제외(`PROJECT_SCOPE.md` 근거) |
| `UI_APPROVED` | 담당 Screen이 `STITCH_VALIDATION_REPORT.md` 기준 PASS |
| `UI_NEEDS_REVISION` | 담당 Screen이 NEEDS_REVISION(미해결 위반 존재) |
| `UI_IN_PROGRESS` | 담당 Screen이 일부 Section만 제작되고 검증되지 않음 |
| `NOT_STARTED` | 담당 Screen이 아직 생성되지 않았거나(SCR-005), UI가 아닌 항목(NON_UI/OPERATIONS)이라 코드·프로세스가 아직 시작되지 않음 |

여러 Screen에 걸친 행은 그중 가장 진행이 덜 된 Screen의 Status를 채택한다(과대 보고 방지).

---

## 1. REQ-FUNC-001~080

### 1.1 F1. Destination Guide (001~010)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-001 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-001 | UI_APPROVED |
| REQ-FUNC-002 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-002 | UI_APPROVED |
| REQ-FUNC-003 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-003 | UI_APPROVED |
| REQ-FUNC-004 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-004 | UI_APPROVED |
| REQ-FUNC-005 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-005 | UI_APPROVED |
| REQ-FUNC-006 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-006 | UI_APPROVED |
| REQ-FUNC-007 | IMPLEMENT (축소) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-007 | UI_APPROVED |
| REQ-FUNC-008 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-008 | NOT_STARTED |
| REQ-FUNC-009 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-009 | UI_APPROVED |
| REQ-FUNC-010 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-010 | UI_APPROVED |

### 1.2 F2. Flight Link-out (011~018)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-011 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-011 | UI_NEEDS_REVISION |
| REQ-FUNC-012 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-012 | UI_NEEDS_REVISION |
| REQ-FUNC-013 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-013 | UI_NEEDS_REVISION |
| REQ-FUNC-014 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-014 | UI_NEEDS_REVISION |
| REQ-FUNC-015 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-015 | UI_NEEDS_REVISION |
| REQ-FUNC-016 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-016 | UI_NEEDS_REVISION |
| REQ-FUNC-017 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-017 | NOT_STARTED |
| REQ-FUNC-018 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-018 | UI_NEEDS_REVISION |

### 1.3 F3. Hotel Link-out (019~026)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-019 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-019 | UI_NEEDS_REVISION |
| REQ-FUNC-020 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-020 | UI_NEEDS_REVISION |
| REQ-FUNC-021 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-021 | UI_NEEDS_REVISION |
| REQ-FUNC-022 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-022 | UI_NEEDS_REVISION |
| REQ-FUNC-023 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-023 | UI_NEEDS_REVISION |
| REQ-FUNC-024 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-024 | UI_NEEDS_REVISION |
| REQ-FUNC-025 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-025 | NOT_STARTED |
| REQ-FUNC-026 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-026 | UI_NEEDS_REVISION |

### 1.4 F4. Travel Mate (027~045)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-027 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-027 | NOT_STARTED |
| REQ-FUNC-028 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-028 | NOT_STARTED |
| REQ-FUNC-029 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-029 | NOT_STARTED |
| REQ-FUNC-030 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-030 | UI_IN_PROGRESS |
| REQ-FUNC-031 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-031 | UI_NEEDS_REVISION |
| REQ-FUNC-032 | IMPLEMENT (축소) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-032 | UI_NEEDS_REVISION |
| REQ-FUNC-033 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-033 | NOT_STARTED |
| REQ-FUNC-034 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-034 | UI_IN_PROGRESS |
| REQ-FUNC-035 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-035 | UI_IN_PROGRESS |
| REQ-FUNC-036 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-036 | UI_IN_PROGRESS |
| REQ-FUNC-037 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-037 | UI_IN_PROGRESS |
| REQ-FUNC-038 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-038 | UI_IN_PROGRESS |
| REQ-FUNC-039 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-039 | UI_IN_PROGRESS |
| REQ-FUNC-040 | IMPLEMENT | SCR-004, SCR-005 | `/mates`, `/account` | `src/app/mates/page.tsx`, `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-040 | NOT_STARTED |
| REQ-FUNC-041 | IMPLEMENT (간소화) | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-041 | NOT_STARTED |
| REQ-FUNC-042 | IMPLEMENT (축소) | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-042 | NOT_STARTED |
| REQ-FUNC-043 | IMPLEMENT (축소) | 전역(SCR-003·004·005) | `/travel-tools`, `/mates`, `/account` | 해당 3개 `page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-043 | NOT_STARTED |
| REQ-FUNC-044 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-044 | NOT_STARTED |
| REQ-FUNC-045 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-045 | EXCLUDED |

### 1.5 F5. Country Safety (046~056)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-046 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-046 | NOT_STARTED |
| REQ-FUNC-047 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-047 | UI_APPROVED |
| REQ-FUNC-048 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-048 | UI_APPROVED |
| REQ-FUNC-049 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-049 | UI_APPROVED |
| REQ-FUNC-050 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-050 | UI_APPROVED |
| REQ-FUNC-051 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-051 | UI_APPROVED |
| REQ-FUNC-052 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-052 | NOT_STARTED |
| REQ-FUNC-053 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-053 | UI_APPROVED |
| REQ-FUNC-054 | IMPLEMENT | SCR-001, SCR-003 | `/`, `/travel-tools` | `src/app/page.tsx`, `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-054 | UI_NEEDS_REVISION |
| REQ-FUNC-055 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-055 | EXCLUDED |
| REQ-FUNC-056 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-056 | EXCLUDED |

### 1.6 F6. About free_traveler (057~063)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-057 | IMPLEMENT | SCR-002, SCR-001 | `/about`, `/` | `src/app/about/page.tsx`, `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-057 | UI_APPROVED |
| REQ-FUNC-058 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-058 | UI_APPROVED |
| REQ-FUNC-059 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-059 | UI_APPROVED |
| REQ-FUNC-060 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-060 | UI_APPROVED |
| REQ-FUNC-061 | IMPLEMENT (축소) | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-061 | UI_APPROVED |
| REQ-FUNC-062 | IMPLEMENT (축소) | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-062 | UI_APPROVED |
| REQ-FUNC-063 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-063 | UI_APPROVED |

### 1.7 F7. Common, Admin, Governance (064~080)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-064 | IMPLEMENT | 전역(5개 Screen) | 전체 | `src/app/layout.tsx` | PENDING_TASK_GENERATION | TC-FUNC-064 | NOT_STARTED |
| REQ-FUNC-065 | IMPLEMENT | 전역(5개 Screen) | 전체 | `src/app/layout.tsx` | PENDING_TASK_GENERATION | TC-FUNC-065 | NOT_STARTED |
| REQ-FUNC-066 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-066 | NOT_STARTED |
| REQ-FUNC-067 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-067 | UI_APPROVED |
| REQ-FUNC-068 | IMPLEMENT | SCR-001, SCR-005 | `/`, `/account` | `src/app/page.tsx`, `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-068 | NOT_STARTED |
| REQ-FUNC-069 | IMPLEMENT | SCR-001, SCR-004 | `/`, `/mates` | `src/app/page.tsx`, `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-069 | UI_IN_PROGRESS |
| REQ-FUNC-070 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-070 | NOT_STARTED |
| REQ-FUNC-071 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-071 | EXCLUDED |
| REQ-FUNC-072 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-072 | EXCLUDED |
| REQ-FUNC-073 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-073 | EXCLUDED |
| REQ-FUNC-074 | IMPLEMENT (대체) | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-074 | NOT_STARTED |
| REQ-FUNC-075 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-075 | EXCLUDED |
| REQ-FUNC-076 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-076 | EXCLUDED |
| REQ-FUNC-077 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-077 | NOT_STARTED |
| REQ-FUNC-078 | IMPLEMENT | 기술 Route | `not-found`/`error` | `src/app/not-found.tsx`, `src/app/error.tsx` | PENDING_TASK_GENERATION | TC-FUNC-078 | NOT_STARTED |
| REQ-FUNC-079 | IMPLEMENT | 전역(5개 Screen) | 전체 | `src/app/layout.tsx` | PENDING_TASK_GENERATION | TC-FUNC-079 | NOT_STARTED |
| REQ-FUNC-080 | IMPLEMENT | SCR-003, 기술 Route | `/travel-tools`, 정책 페이지 | `src/app/travel-tools/page.tsx`, 정책 하위 경로 | PENDING_TASK_GENERATION | TC-FUNC-080 | NOT_STARTED |

---

## 2. REQ-NF-001~034

### 2.1 Performance (001~007)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-001 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-001 | NOT_STARTED |
| REQ-NF-002 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-002 | NOT_STARTED |
| REQ-NF-003 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-003 | NOT_STARTED |
| REQ-NF-004 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-004 | NOT_STARTED |
| REQ-NF-005 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-005 | NOT_STARTED |
| REQ-NF-006 | IMPLEMENT | SCR-001, SCR-002 | `/`, `/about` | `src/app/page.tsx`, `src/app/about/page.tsx` | PENDING_TASK_GENERATION | TC-NF-006 | UI_APPROVED |
| REQ-NF-007 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-007 | EXCLUDED |

### 2.2 Reliability and Recovery (008~011)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-008 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-008 | EXCLUDED |
| REQ-NF-009 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-009 | EXCLUDED |
| REQ-NF-010 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-010 | EXCLUDED |
| REQ-NF-011 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-011 | EXCLUDED |

### 2.3 Security and Privacy (012~018)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-012 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-012 | NOT_STARTED |
| REQ-NF-013 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-013 | NOT_STARTED |
| REQ-NF-014 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-014 | NOT_STARTED |
| REQ-NF-015 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-015 | NOT_STARTED |
| REQ-NF-016 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-016 | NOT_STARTED |
| REQ-NF-017 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-017 | NOT_STARTED |
| REQ-NF-018 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-018 | EXCLUDED |

### 2.4 Safety and Moderation (019~022)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-019 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-019 | NOT_STARTED |
| REQ-NF-020 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-020 | EXCLUDED |
| REQ-NF-021 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-021 | EXCLUDED |
| REQ-NF-022 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-022 | EXCLUDED |

### 2.5 Accessibility (023~025)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-023 | IMPLEMENT | 전역(5개 Screen) | 전체 | `src/app/layout.tsx` | PENDING_TASK_GENERATION | TC-NF-023 | NOT_STARTED |
| REQ-NF-024 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-024 | EXCLUDED |
| REQ-NF-025 | IMPLEMENT (축소) | 전역(5개 Screen) | 전체 | `src/app/layout.tsx` | PENDING_TASK_GENERATION | TC-NF-025 | NOT_STARTED |

### 2.6 Content, Freshness, SEO, Copyright (026~030)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-026 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-026 | NOT_STARTED |
| REQ-NF-027 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-027 | NOT_STARTED |
| REQ-NF-028 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-NF-028 | UI_APPROVED |
| REQ-NF-029 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-029 | EXCLUDED |
| REQ-NF-030 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-030 | NOT_STARTED |

### 2.7 Maintainability, Monitoring, Cost (031~034)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-031 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-031 | NOT_STARTED |
| REQ-NF-032 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-032 | EXCLUDED |
| REQ-NF-033 | **EXCLUDED** | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-033 | EXCLUDED |
| REQ-NF-034 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-034 | NOT_STARTED |

---

## 3. 요약 집계

| 구분 | 개수 |
|---|---:|
| REQ-FUNC-001~080 | 80 |
| REQ-NF-001~034 | 34 |
| **Requirement 합계** | **114** |

| Status | 개수 |
|---|---:|
| EXCLUDED | 21 |
| UI_APPROVED | 25 |
| UI_NEEDS_REVISION | 17 |
| UI_IN_PROGRESS | 8 |
| NOT_STARTED | 43 |
| **합계** | **114** |

(표 안의 각 값은 문서 내 모든 `REQ-FUNC-*`/`REQ-NF-*` 행을 직접 집계한 결과이며, 합계 114는 §3 상단의 Requirement 합계와 일치한다.)

- Task 열: 전항목 `PENDING_TASK_GENERATION` — Task가 아직 하나도 생성되지 않았음을 의미하며, Task 생성이 완료되면 이 문서를 갱신해 각 행에 실제 Task ID를 채운다.
- Test 열: 전항목이 `02_SRS_BASELINE.md` §5.1 명명 규칙에 따른 예정 ID이며, 실제 테스트 코드는 아직 작성되지 않았다.
- EXCLUDED 21개는 `docs/PROJECT_SCOPE.md`·`docs/06_SRS_UIUX_REVISED.md`와 동일한 목록이다: REQ-FUNC-045, 055, 056, 071, 072, 073, 075, 076 / REQ-NF-007, 008, 009, 010, 011, 018, 020, 021, 022, 024, 029, 032, 033.
- `UI_APPROVED` 25개는 모두 SCR-001·SCR-002(둘 다 `STITCH_VALIDATION_REPORT.md` 기준 PASS)에 속한 항목이다. SCR-003 관련 17개는 `UI_NEEDS_REVISION`, SCR-004 관련 8개는 `UI_IN_PROGRESS`, SCR-005 및 나머지 NON_UI/OPERATIONS/전역 항목 43개는 `NOT_STARTED`다.
