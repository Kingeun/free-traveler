# SRS UI·UX 개정본 — Free Traveler

**Document ID:** SRS-UIUX-REV-001
**개정 대상:** `docs/02_SRS_BASELINE.md`(SRS-TRAVEL-001 v1.0) §3.5 Page and Route Inventory
**개정 범위:** Route 구조만 개정한다. REQ-FUNC-001~080, REQ-NF-001~034의 요구사항 본문·Acceptance Criteria는 `02_SRS_BASELINE.md`가 계속 원본(authoritative)이며, 이 문서는 그 내용을 삭제하거나 대체하지 않는다.
**연결 문서:** `docs/05_UIUX_APPROVED.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, `docs/UIUX_TRACEABILITY.md`

---

## 1. 개정 목적과 원칙

`02_SRS_BASELINE.md` §3.5는 16개의 공개 Route(`/`, `/destinations`, `/destinations/domestic` 등)를 정의했다. `03_UI_COVERAGE_ANALYSIS.md`와 `04_UIUX_PLAN.md`를 거치며 이 Route들은 정확히 5개의 디자인 Screen(SCR-001~005)으로 통합되었다. 이 문서는 그 통합을 SRS 관점에서 공식화한다.

- **삭제 없음:** REQ-FUNC-001~080, REQ-NF-001~034 114개 전항목을 §4에서 전수 재확인한다.
- **Route만 통합:** 기존에 별도 페이지였던 기능은 5개 Screen의 탭·패널·Drawer·Modal로 재배치되었을 뿐, 요구사항이 요구하는 동작 자체는 변경되지 않았다.
- **범위 불변:** `PROJECT_SCOPE.md`의 IMPLEMENT/EXCLUDED 분류는 그대로 유지한다.

---

## 2. 개정된 §3.5 Page and Route Inventory

| Route | Screen | Page Entry | Access |
|---|---|---|---|
| `/` | SCR-001 메인 | `src/app/page.tsx` | Public |
| `/about` | SCR-002 대표 소개 | `src/app/about/page.tsx` | Public |
| `/travel-tools` | SCR-003 통합 여행 준비(항공/숙소/동행 구하기 3탭) | `src/app/travel-tools/page.tsx` | Public(동행 작성은 Adult Member) |
| `/mates` | SCR-004 동행 조회(목록+상세 패널) | `src/app/mates/page.tsx` | Public(참가 요청은 Adult Member) |
| `/account` | SCR-005 계정·관리(Guest/Member/Admin 역할별 탭) | `src/app/account/page.tsx` | Public/Member/Role Restricted(탭별 상이) |

**기술 Route(위 5개에 포함되지 않음):** `/auth/callback`(인증 콜백), `/api/**`(API Route), `not-found`/`error`(404·500 오류 화면). 상세는 `design-reference/SCREEN_ROUTE_CONTRACT.json`의 `technical_routes` 참조.

---

## 3. Route 통합 근거

기존 16개 Route 중 `/`, `/about`, `/mates`를 제외한 13개는 아래와 같이 5개 Screen 내부의 탭·패널·Drawer·Modal로 통합되었다(전체 매핑표는 `docs/05_UIUX_APPROVED.md` §3).

- **여행지 탐색 계열**(`/destinations`, `/destinations/domestic`, `/destinations/overseas`, `/destinations/[slug]`) → SCR-001의 Card Grid Section과 상세 **Drawer**로 통합. 사용자는 별도 페이지 이동 없이 같은 화면에서 탐색을 완료한다.
- **항공·호텔 계열**(`/flights`, `/hotels`, `/mates/new`) → SCR-003 `/travel-tools`의 **3탭**(항공편 찾기/숙소 찾기/동행 구하기)으로 통합. 세 탭은 입력·검증·완료 상태를 서로 독립적으로 유지한다.
- **동행 상세**(`/mates/[id]`) → SCR-004의 상세 **패널**(Desktop)/**Drawer**(Mobile)로 통합.
- **안전정보 계열**(`/safety`, `/safety/[countryCode]`) → SCR-001의 안전정보 **Modal/Drawer**로 통합.
- **인증·내 활동·관리 계열**(`/auth/*`, `/my/*`, `/admin/*`) → SCR-005 `/account`의 역할별 탭(Guest/Member/Admin)으로 통합.

이 통합은 REQ-FUNC-064(전역 내비게이션 2회 이내 도달)를 더 쉽게 만족시키는 방향이며, 어떤 요구사항의 승인 기준(Acceptance Criteria)도 변경하지 않는다.

---

## 4. REQ-FUNC-001~080 / REQ-NF-001~034 보존 확인

전항목을 요약·분류·Screen 배치와 함께 재확인한다. AC 전문은 `02_SRS_BASELINE.md`를 따른다. Implementation Status는 `PROJECT_SCOPE.md`를 그대로 인용한다.

### 4.1 F1. Destination Guide (001~010)

| ID | 요약 | Implementation Status | Screen |
|---|---|---|---|
| REQ-FUNC-001 | 국내·해외 여행지 목록 구분 제공 | IMPLEMENT | SCR-001 |
| REQ-FUNC-002 | 국가·도시·계절·테마·기간 필터 | IMPLEMENT | SCR-001 |
| REQ-FUNC-003 | 키워드 검색 | IMPLEMENT | SCR-001 |
| REQ-FUNC-004 | 상세 필수 필드 | IMPLEMENT | SCR-001 |
| REQ-FUNC-005 | 빈 결과 안내 + 전체 초기화 | IMPLEMENT | SCR-001 |
| REQ-FUNC-006 | 해외 여행지 상세→국가 안전 연결 | IMPLEMENT | SCR-001 |
| REQ-FUNC-007 | 이미지 alt·출처·작가·라이선스 | IMPLEMENT (축소) | SCR-001 |
| REQ-FUNC-008 | 게시 기준 수량 검증 | IMPLEMENT | N/A(데이터 검증 스크립트) |
| REQ-FUNC-009 | 관련 여행지 추천 최대 6개 | IMPLEMENT | SCR-001 |
| REQ-FUNC-010 | 필터 상태 URL query 동기화 | IMPLEMENT | SCR-001 |

### 4.2 F2. Flight Link-out (011~018)

| ID | 요약 | Implementation Status | Screen |
|---|---|---|---|
| REQ-FUNC-011 | 국가·지역·출발일·귀국일 필수 입력 | IMPLEMENT | SCR-003(항공 탭) |
| REQ-FUNC-012 | 국가별 지역 종속 선택 | IMPLEMENT | SCR-003(항공 탭) |
| REQ-FUNC-013 | 날짜 역전/과거 출발일 차단 | IMPLEMENT | SCR-003(항공 탭) |
| REQ-FUNC-014 | 입력→요약 단계 표시 | IMPLEMENT | SCR-003(항공 탭) |
| REQ-FUNC-015 | 입력값 비전달 고지 | IMPLEMENT | SCR-003(항공 탭) |
| REQ-FUNC-016 | 외부 URL 새 탭 이동 | IMPLEMENT | SCR-003(항공 탭) |
| REQ-FUNC-017 | 서버 DB·로그·분석 미저장 | IMPLEMENT | N/A(아키텍처 제약) |
| REQ-FUNC-018 | URL 오류 시 이동 차단+재시도 | IMPLEMENT | SCR-003(항공 탭) |

### 4.3 F3. Hotel Link-out (019~026)

| ID | 요약 | Implementation Status | Screen |
|---|---|---|---|
| REQ-FUNC-019 | 국가·지역·체크인·체크아웃 필수 입력 | IMPLEMENT | SCR-003(숙소 탭) |
| REQ-FUNC-020 | 국가별 지역 종속 선택 | IMPLEMENT | SCR-003(숙소 탭) |
| REQ-FUNC-021 | 체크인/체크아웃 검증 | IMPLEMENT | SCR-003(숙소 탭) |
| REQ-FUNC-022 | 입력→요약 단계 표시 | IMPLEMENT | SCR-003(숙소 탭) |
| REQ-FUNC-023 | 입력값 비전달 고지 | IMPLEMENT | SCR-003(숙소 탭) |
| REQ-FUNC-024 | 외부 URL 새 탭 이동 | IMPLEMENT | SCR-003(숙소 탭) |
| REQ-FUNC-025 | 서버 DB·로그·분석 미저장 | IMPLEMENT | N/A(아키텍처 제약) |
| REQ-FUNC-026 | URL 오류 시 이동 차단+재시도 | IMPLEMENT | SCR-003(숙소 탭) |

### 4.4 F4. Travel Mate (027~045)

| ID | 요약 | Implementation Status | Screen |
|---|---|---|---|
| REQ-FUNC-027 | 동행 쓰기에 인증 세션 요구 | IMPLEMENT | SCR-005 |
| REQ-FUNC-028 | 성인확인 상태 요구, 생년월일 미저장 | IMPLEMENT | SCR-005 |
| REQ-FUNC-029 | 프로필 입력 | IMPLEMENT | SCR-005 |
| REQ-FUNC-030 | 동행글 다중 필터 | IMPLEMENT | SCR-004 |
| REQ-FUNC-031 | 모집글 작성 입력 | IMPLEMENT | SCR-003(동행 작성 탭) |
| REQ-FUNC-032 | 연락처 패턴 탐지 후 차단 | IMPLEMENT (축소) | SCR-003(동행 작성 탭) |
| REQ-FUNC-033 | 응답에서 연락처 노출 제외 | IMPLEMENT | N/A(데이터 필터링) |
| REQ-FUNC-034 | 참가 메시지 비공개 제출 | IMPLEMENT | SCR-004(상세 패널) |
| REQ-FUNC-035 | 중복 요청 차단 | IMPLEMENT | SCR-004(상세 패널) |
| REQ-FUNC-036 | 작성자의 요청 승인/거절 | IMPLEMENT | SCR-004(상세 패널) |
| REQ-FUNC-037 | 종료일 다음날 자동 마감 | IMPLEMENT | SCR-004 |
| REQ-FUNC-038 | 작성자 수동 마감/수정/삭제 | IMPLEMENT | SCR-004(상세 패널) |
| REQ-FUNC-039 | 사유 코드+설명 신고 | IMPLEMENT | SCR-004(상세 패널) |
| REQ-FUNC-040 | 사용자 차단·해제 | IMPLEMENT | SCR-004, SCR-005 |
| REQ-FUNC-041 | Moderator 신고 큐 | IMPLEMENT (간소화) | SCR-005(관리자 탭) |
| REQ-FUNC-042 | 신고 상태 변경+글 숨김 | IMPLEMENT (축소) | SCR-005(관리자 탭) |
| REQ-FUNC-043 | 인앱 알림(이메일 선택) | IMPLEMENT (축소) | 전역(SCR-003·004·005) |
| REQ-FUNC-044 | RLS 비공개 데이터 제한 | IMPLEMENT | N/A(백엔드 정책) |
| REQ-FUNC-045 | 탈퇴 시 비식별화+삭제 | **EXCLUDED** | N/A |

### 4.5 F5. Country Safety (046~056)

| ID | 요약 | Implementation Status | Screen |
|---|---|---|---|
| REQ-FUNC-046 | 게시 해외국가 전체 안전 페이지 요구 | IMPLEMENT | N/A(데이터 검증) |
| REQ-FUNC-047 | 8개 필수 카테고리 | IMPLEMENT | SCR-001 |
| REQ-FUNC-048 | 출처·확인일·편집자 표기 | IMPLEMENT | SCR-001 |
| REQ-FUNC-049 | 외교부 원문 링크 | IMPLEMENT | SCR-001 |
| REQ-FUNC-050 | stale 7일 경고 | IMPLEMENT | SCR-001 |
| REQ-FUNC-051 | 중대 경보 텍스트 상단 표시 | IMPLEMENT | SCR-001 |
| REQ-FUNC-052 | 경보 범위 필수 필드화 | IMPLEMENT | N/A(데이터 검증) |
| REQ-FUNC-053 | 긴급전화·영사콜센터 정보 | IMPLEMENT | SCR-001 |
| REQ-FUNC-054 | 공식 판단 대체 불가 고지 | IMPLEMENT | SCR-001, SCR-003 |
| REQ-FUNC-055 | 콘텐츠 작성·검수·게시 워크플로 | **EXCLUDED** | N/A |
| REQ-FUNC-056 | 변경 이력 보존 | **EXCLUDED** | N/A |

### 4.6 F6. About free_traveler (057~063)

| ID | 요약 | Implementation Status | Screen |
|---|---|---|---|
| REQ-FUNC-057 | 대표명·지표 표시 | IMPLEMENT | SCR-002, SCR-001 |
| REQ-FUNC-058 | 소개문·철학·편집 원칙 | IMPLEMENT | SCR-002 |
| REQ-FUNC-059 | 방문 권역/30개국 목록 | IMPLEMENT | SCR-002 |
| REQ-FUNC-060 | 여행 타임라인 | IMPLEMENT | SCR-002 |
| REQ-FUNC-061 | 대표 이미지 메타데이터 | IMPLEMENT (축소) | SCR-002 |
| REQ-FUNC-062 | 문의·SNS 링크 | IMPLEMENT (축소) | SCR-002 |
| REQ-FUNC-063 | 추천 여행지 6개 연결 | IMPLEMENT | SCR-002 |

### 4.7 F7. Common, Admin, Governance (064~080)

| ID | 요약 | Implementation Status | Screen |
|---|---|---|---|
| REQ-FUNC-064 | 전역 내비게이션·푸터 | IMPLEMENT | 전역(5개 Screen 공통) |
| REQ-FUNC-065 | 320px~데스크톱 반응형 | IMPLEMENT | 전역 |
| REQ-FUNC-066 | 이메일 가입·인증·로그인 | IMPLEMENT | SCR-005 |
| REQ-FUNC-067 | 통합 검색 | IMPLEMENT | SCR-001 |
| REQ-FUNC-068 | 즐겨찾기(localStorage) | IMPLEMENT | SCR-001, SCR-005 |
| REQ-FUNC-069 | URL 공유 | IMPLEMENT | SCR-001, SCR-004 |
| REQ-FUNC-070 | SEO 메타데이터 | IMPLEMENT | N/A(head 메타) |
| REQ-FUNC-071 | 행동 이벤트 기록 | **EXCLUDED** | N/A |
| REQ-FUNC-072 | 콘텐츠 CRUD | **EXCLUDED** | N/A |
| REQ-FUNC-073 | 미디어 업로드 메타데이터 필수 | **EXCLUDED** | N/A |
| REQ-FUNC-074 | 게시 전 완전성 게이트 | IMPLEMENT (대체) | N/A(검증 스크립트) |
| REQ-FUNC-075 | 안전정보 stale 대시보드 | **EXCLUDED** | N/A |
| REQ-FUNC-076 | 감사 로그 | **EXCLUDED** | N/A |
| REQ-FUNC-077 | 외부 URL 허용목록 설정 | IMPLEMENT | SCR-005(관리자 탭) |
| REQ-FUNC-078 | 404/500 복구 행동 | IMPLEMENT | 기술 Route |
| REQ-FUNC-079 | 시맨틱·ARIA | IMPLEMENT | 전역 |
| REQ-FUNC-080 | 정책 페이지+동의 기록 | IMPLEMENT | SCR-003(동행 작성 탭)/기술 Route(정책 본문) |

---

## 5. REQ-NF-001~034 보존 확인

### 5.1 Performance (001~007)

| ID | 요약 | Implementation Status | Screen |
|---|---|---|---|
| REQ-NF-001 | LCP p75 ≤2.5s | IMPLEMENT | N/A |
| REQ-NF-002 | INP p75 ≤200ms | IMPLEMENT | N/A |
| REQ-NF-003 | CLS p75 ≤0.1 | IMPLEMENT | N/A |
| REQ-NF-004 | 필터 응답 p95 ≤1s | IMPLEMENT | N/A |
| REQ-NF-005 | 쓰기 API 응답 p95 ≤3s | IMPLEMENT | N/A |
| REQ-NF-006 | 이미지 반응형·lazy load | IMPLEMENT | SCR-001, SCR-002 |
| REQ-NF-007 | Lighthouse 성능 예산 검사 | **EXCLUDED** | N/A |

### 5.2 Reliability (008~011)

| ID | 요약 | Implementation Status | Screen |
|---|---|---|---|
| REQ-NF-008 | 월간 가용성 ≥99.5% | **EXCLUDED** | N/A |
| REQ-NF-009 | 내부 API 5xx ≤0.5% | **EXCLUDED** | N/A |
| REQ-NF-010 | DB 백업 RPO/RTO | **EXCLUDED** | N/A |
| REQ-NF-011 | 외부 링크 자동 검사+알림 | **EXCLUDED** | N/A |

### 5.3 Security/Privacy (012~018)

| ID | 요약 | Implementation Status | Screen |
|---|---|---|---|
| REQ-NF-012 | TLS 1.2 이상 | IMPLEMENT | N/A |
| REQ-NF-013 | 인증·역할·RLS 서버 검증 | IMPLEMENT | N/A |
| REQ-NF-014 | CSRF 방어·SameSite | IMPLEMENT | N/A |
| REQ-NF-015 | 입력 검증·XSS 차단 | IMPLEMENT | N/A |
| REQ-NF-016 | 비밀키 환경변수 관리 | IMPLEMENT | N/A |
| REQ-NF-017 | 원시 입력값 미보존 | IMPLEMENT | N/A |
| REQ-NF-018 | 개인정보 내보내기·탈퇴 | **EXCLUDED** | N/A |

### 5.4 Safety/Moderation (019~022)

| ID | 요약 | Implementation Status | Screen |
|---|---|---|---|
| REQ-NF-019 | 신고 접수 응답 p95 ≤3s | IMPLEMENT | N/A |
| REQ-NF-020 | 신고 1차 검토 SLA | **EXCLUDED** | N/A |
| REQ-NF-021 | 속도 제한 | **EXCLUDED** | N/A |
| REQ-NF-022 | Moderator 조치 추적성 | **EXCLUDED** | N/A |

### 5.5 Accessibility (023~025)

| ID | 요약 | Implementation Status | Screen |
|---|---|---|---|
| REQ-NF-023 | WCAG 2.2 AA 목표 | IMPLEMENT | 전역 |
| REQ-NF-024 | 자동 접근성 검사 | **EXCLUDED** | N/A |
| REQ-NF-025 | 키보드·스크린리더 수동 검사 | IMPLEMENT (축소) | 전역 |

### 5.6 Content/SEO/Copyright (026~030)

| ID | 요약 | Implementation Status | Screen |
|---|---|---|---|
| REQ-NF-026 | 여행지 콘텐츠 완전성 100% | IMPLEMENT | N/A |
| REQ-NF-027 | 안전정보 커버리지 100% | IMPLEMENT | N/A |
| REQ-NF-028 | 안전정보 최신 확인 95%+ | IMPLEMENT | SCR-001 |
| REQ-NF-029 | 미디어 라이선스 메타데이터 | **EXCLUDED** | N/A |
| REQ-NF-030 | SEO 메타데이터 누락 0건 | IMPLEMENT | N/A |

### 5.7 Maintainability/Monitoring/Cost (031~034)

| ID | 요약 | Implementation Status | Screen |
|---|---|---|---|
| REQ-NF-031 | TS strict·lint·Playwright | IMPLEMENT | N/A |
| REQ-NF-032 | 구조화 로그 | **EXCLUDED** | N/A |
| REQ-NF-033 | 핵심 오류 알림 | **EXCLUDED** | N/A |
| REQ-NF-034 | 월 인프라 비용 목표 | IMPLEMENT | N/A |

---

## 6. 보존 검증

| 구분 | 개수 |
|---|---:|
| REQ-FUNC-001~080 | 80 |
| REQ-NF-001~034 | 34 |
| **합계** | **114** |

§4~§5에 정확히 114개 행이 존재하며, `02_SRS_BASELINE.md`에서 삭제된 항목은 없다. EXCLUDED 21개 목록은 `PROJECT_SCOPE.md`·`03_UI_COVERAGE_ANALYSIS.md`와 동일하다: REQ-FUNC-045, 055, 056, 071, 072, 073, 075, 076 / REQ-NF-007, 008, 009, 010, 011, 018, 020, 021, 022, 024, 029, 032, 033.

컬럼별 상세(Route, Page Entry, Task, Test, Status)는 `docs/UIUX_TRACEABILITY.md`에서 관리한다.
