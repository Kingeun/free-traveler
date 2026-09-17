# UI Coverage Analysis — Free Traveler MVP

**Document ID:** UICOV-TRAVEL-001
**기반 문서:** `docs/02_SRS_BASELINE.md` (SRS-TRAVEL-001 v1.0), `docs/PROJECT_SCOPE.md` (SCOPE-TRAVEL-001)
**대상:** REQ-FUNC-001~080, REQ-NF-001~034 (총 114개), 고정 디자인 Screen 5개

---

## 1. 목적 및 범위

본 문서는 SRS Baseline의 요구사항 114개(REQ-FUNC-001~080, REQ-NF-001~034)를 하나도 삭제하지 않고 전수 유지한 상태에서, 각 요구사항이 UI에서 어떤 성격으로 나타나는지 분류하고 정확히 5개로 고정된 디자인 Screen에 배치한다. `PROJECT_SCOPE.md`의 IMPLEMENT/EXCLUDED 분류는 그대로 유지하며, EXCLUDED 항목을 구현 범위로 되돌리지 않는다. Screen 수는 5개를 넘지 않는다.

---

## 2. 분류 정의

| 분류 | 정의 | 예시 |
|---|---|---|
| **UI_DIRECT** | 사용자가 직접 보고 조작하는 렌더링된 화면 요소(패널, 폼, 버튼, 목록, 텍스트)로 요구사항이 충족되는 경우 | 여행지 필터 UI, 항공 입력 폼, 참가 요청 버튼 |
| **UI_STATE** | 화면 동작에 영향을 주는 클라이언트 상태·검증·계산 로직(오류 차단, 자동 전환, URL 동기화 등)으로, 별도의 독립된 렌더링 요소가 아니라 기존 UI_DIRECT 요소의 동작 방식인 경우 | 날짜 역전 검증 차단, stale 7일 경과 계산, 반응형 레이아웃 동작 |
| **NON_UI** | 화면에 나타나지 않는 백엔드·보안·성능·데이터 제약·빌드타임 검증 스크립트 | RLS 정책, TLS 적용, 데이터 완전성 검증 스크립트 |
| **OPERATIONS** | 코드가 아니라 사람이 지속적으로 수행하는 운영·거버넌스·모니터링·편집·CI 프로세스(구현 여부와 무관하게 프로세스 성격이면 이 분류) | 감사 로그 거버넌스, 콘텐츠 편집 워크플로, 신고 1차검토 SLA, 회원탈퇴 수동 처리 |

> 자동화된 데이터/코드 검증 스크립트(빌드 타임, 사람의 반복 개입 없음)는 NON_UI로, 사람이 반복적으로 관여해야 하는 절차(모니터링 대응, SLA, 수동 처리, 편집 검수, CI 병합 게이트)는 OPERATIONS로 구분한다.

---

## 3. Design Screen 인벤토리 (정확히 5개, 고정)

| Screen | Route | 사용자 목표 | 주요 영역 | 상태(State) | 이동 목적지 |
|---|---|---|---|---|---|
| **SCR-001** | `/` 메인 | 여행지를 탐색하고 국가 안전정보를 확인하며 핵심 기능으로 진입 | 히어로/진입 배너, 국내·해외 탭, 필터·검색 바, 여행지 카드 목록, **여행지 상세 Drawer**(관련 여행지 포함), **안전정보 Modal/Drawer**(8개 카테고리, 경보 단계, stale 배지, 외교부 링크) | 필터 결과 있음/없음, 로딩, stale/최신, 즐겨찾기 등록 여부, 검색어 없음 | SCR-003(항공/숙소/동행 CTA), SCR-002(대표소개), SCR-004(동행 CTA), SCR-005(로그인 필요 시) |
| **SCR-002** | `/about` 대표 소개 | `free_traveler` 대표를 신뢰하고 추천 여행지를 탐색 | 대표 프로필 헤더(50+ Trips/30+ Countries), 소개문·철학, 방문국가 목록/지도, 여행 타임라인, 추천 여행지 카드(6), 문의/SNS 링크 | 이미지 로드 실패 대체, 추천 여행지 없음(비공개 자동 제외) | SCR-001(추천 여행지 클릭 시 상세 Drawer) |
| **SCR-003** | `/travel-tools` 통합 여행 준비 | 항공/숙소 조건 입력 후 요약 확인·외부 이동, 동행 모집글 작성 | 3탭: **항공**(국가/지역/출발/귀국 폼+요약), **숙소**(국가/지역/체크인/아웃 폼+요약), **동행 작성**(제목/국가/지역/기간/인원/스타일/설명/안전수칙 동의), 비전달 고지, 외부이동 버튼, Toast 오류 | 미검증/검증실패/요약완료/외부이동성공·실패, 비로그인(동행 작성 탭 진입 시 SCR-005 유도) | 외부 사이트(새 탭, 항공/숙소), SCR-005(비로그인 유도), SCR-004(작성 완료 후 이동) |
| **SCR-004** | `/mates` 동행 조회 | 동행 모집글을 탐색하고 참가 요청·승인/거절·신고·차단을 처리 | 필터 바(국가/지역/기간/연령대/성별/스타일/모집상태), 모집글 목록, **상세 패널**(작성자 정보, 설명, 참가 요청 폼, 승인/거절 컨트롤, 신고·차단 버튼, 수동 마감/수정/삭제) | 모집중/마감(자동·수동), PENDING/ACCEPTED/REJECTED, 비로그인 시 SCR-005 유도, 차단 관계로 미노출 | SCR-005(비로그인 유도), SCR-003(새 글 작성 CTA) |
| **SCR-005** | `/account` 계정·관리 | 인증·성인확인, 프로필 관리, 내 활동 관리, (Admin) 신고 처리·외부 URL 설정 | 4탭: **로그인**(가입/로그인/로그아웃/비밀번호 재설정/성인확인), **프로필**(닉네임/연령대/스타일/자기소개), **내 활동**(내 글, 참가 요청, 즐겨찾기, 차단 목록), **관리자**(Admin 권한에서만 노출 — 신고 상태 큐, 외부 URL 설정) | 미인증/인증됨, 성인확인 전/후, 관리자 권한 유무(탭 노출 여부) | SCR-004(내 글/요청 클릭 시 상세 패널), SCR-001(즐겨찾기 클릭 시 상세 Drawer) |

### 3.1 디자인 Screen에 포함되지 않는 기술 Route

다음은 화면 이동의 대상이 될 수 있으나 사용자가 별도로 "탐색"하는 디자인 화면이 아니므로 5개 집계에서 제외한다.

| 기술 Route | 성격 |
|---|---|
| `/auth/callback` 등 인증 콜백 | Supabase Auth 리다이렉트 처리 전용 |
| `/api/*` API Route | 서버 응답 전용, 화면 없음 |
| 404 / 500 / 권한 없음 / 외부 연결 실패 | 오류 처리 전용 화면(REQ-FUNC-078) |
| 이용약관 / 개인정보 처리방침 / 동행 안전수칙 / 콘텐츠 면책 | 정적 정책 콘텐츠 페이지, 동의 UI 자체는 SCR-003에 위치 |

### 3.2 배치 원칙 확인

| # | 배치 원칙 | 적용 결과 |
|---|---|---|
| 5 | 여행지·안전 상세는 SCR-001 Drawer/Modal | REQ-FUNC-004, 006, 007, 047~054가 SCR-001 Drawer/Modal에 배치됨 |
| 6 | 항공·숙소·동행 작성은 SCR-003의 3탭 | REQ-FUNC-011~026(항공/숙소), 031~032(동행 작성)이 SCR-003 탭에 배치됨 |
| 7 | 동행 상세는 SCR-004 상세 패널 | REQ-FUNC-034~036, 038~040이 SCR-004 상세 패널에 배치됨 |
| 8 | 로그인·프로필·내 활동·간단 관리자는 SCR-005 탭 | REQ-FUNC-027~029, 066, 041~042, 068, 077이 SCR-005 탭에 배치됨 |
| 9 | API Route·인증 콜백·오류 처리는 기술 Route | REQ-FUNC-078 및 인증 콜백은 디자인 Screen으로 세지 않음(§3.1) |

---

## 4. Requirement 매핑 — 기능 요구사항 (REQ-FUNC-001~080)

범례 — PROJECT_SCOPE 분류는 `docs/PROJECT_SCOPE.md` 원문 그대로 인용(변경 없음).

### 4.1 F1. Destination Guide (001~010)

| ID | 요구사항 요약 | PROJECT_SCOPE 분류 | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-FUNC-001 | 국내·해외 여행지 목록 구분 제공 | IMPLEMENT | UI_DIRECT | SCR-001 | 탭 UI |
| REQ-FUNC-002 | 국가·도시·계절·테마·기간 필터 | IMPLEMENT | UI_DIRECT | SCR-001 | |
| REQ-FUNC-003 | 키워드 검색 | IMPLEMENT | UI_DIRECT | SCR-001 | |
| REQ-FUNC-004 | 상세 필수 필드(소개/명소/일정/예산/교통/음식/에티켓/출처/수정일) | IMPLEMENT | UI_DIRECT | SCR-001 (상세 Drawer) | |
| REQ-FUNC-005 | 빈 결과 안내 + 전체 초기화 | IMPLEMENT | UI_DIRECT | SCR-001 | |
| REQ-FUNC-006 | 해외 여행지 상세→국가 안전 페이지 연결 | IMPLEMENT | UI_DIRECT | SCR-001 (상세 Drawer→안전 Modal) | |
| REQ-FUNC-007 | 이미지 alt·출처·작가·라이선스 연결 | IMPLEMENT (축소) | UI_DIRECT | SCR-001 | 출처/작가/라이선스는 선택 캡션 |
| REQ-FUNC-008 | 게시 기준 수량(국내10+/해외15개국30도시+) 검증 | IMPLEMENT | NON_UI | - | 데이터 검증 스크립트 |
| REQ-FUNC-009 | 관련 여행지 추천 최대 6개 | IMPLEMENT | UI_DIRECT | SCR-001 (상세 Drawer) | |
| REQ-FUNC-010 | 필터 상태 URL query 동기화 | IMPLEMENT | UI_STATE | SCR-001 | URL 직렬화/복원 로직 |

### 4.2 F2. Flight Link-out (011~018)

| ID | 요구사항 요약 | PROJECT_SCOPE 분류 | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-FUNC-011 | 국가·지역·출발일·귀국일 필수 입력 | IMPLEMENT | UI_DIRECT | SCR-003 (항공 탭) | |
| REQ-FUNC-012 | 국가별 지역 종속 선택 | IMPLEMENT | UI_DIRECT | SCR-003 (항공 탭) | |
| REQ-FUNC-013 | 날짜 역전/과거 출발일 차단 | IMPLEMENT | UI_STATE | SCR-003 (항공 탭) | 검증 로직 |
| REQ-FUNC-014 | 입력→요약 단계 표시 | IMPLEMENT | UI_DIRECT | SCR-003 (항공 탭) | |
| REQ-FUNC-015 | 입력값 비전달 고지 문구 | IMPLEMENT | UI_DIRECT | SCR-003 (항공 탭) | |
| REQ-FUNC-016 | 외부 URL 새 탭 이동(noopener,noreferrer, query 없음) | IMPLEMENT | UI_STATE | SCR-003 (항공 탭) | 이동 동작 |
| REQ-FUNC-017 | 서버 DB·로그·분석 미저장 | IMPLEMENT | NON_UI | - | 아키텍처 제약 |
| REQ-FUNC-018 | URL 오류 시 이동 차단+재시도 | IMPLEMENT | UI_DIRECT | SCR-003 (항공 탭) | 오류 UI |

### 4.3 F3. Hotel Link-out (019~026)

| ID | 요구사항 요약 | PROJECT_SCOPE 분류 | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-FUNC-019 | 국가·지역·체크인·체크아웃 필수 입력 | IMPLEMENT | UI_DIRECT | SCR-003 (숙소 탭) | |
| REQ-FUNC-020 | 국가별 지역 종속 선택 | IMPLEMENT | UI_DIRECT | SCR-003 (숙소 탭) | |
| REQ-FUNC-021 | 체크인 과거/체크아웃≤체크인 차단 | IMPLEMENT | UI_STATE | SCR-003 (숙소 탭) | 검증 로직 |
| REQ-FUNC-022 | 입력→요약 단계 표시 | IMPLEMENT | UI_DIRECT | SCR-003 (숙소 탭) | |
| REQ-FUNC-023 | 입력값 비전달 고지 문구 | IMPLEMENT | UI_DIRECT | SCR-003 (숙소 탭) | |
| REQ-FUNC-024 | 외부 URL 새 탭 이동(noopener,noreferrer) | IMPLEMENT | UI_STATE | SCR-003 (숙소 탭) | 이동 동작 |
| REQ-FUNC-025 | 서버 DB·로그·분석 미저장 | IMPLEMENT | NON_UI | - | 아키텍처 제약 |
| REQ-FUNC-026 | URL 오류 시 이동 차단+재시도 | IMPLEMENT | UI_DIRECT | SCR-003 (숙소 탭) | 오류 UI |

### 4.4 F4. Travel Mate (027~045)

| ID | 요구사항 요약 | PROJECT_SCOPE 분류 | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-FUNC-027 | 동행 쓰기에 인증 세션 요구 | IMPLEMENT | UI_STATE | SCR-005 (가드→로그인 탭 유도) | 가드 동작 |
| REQ-FUNC-028 | 성인확인 상태 요구, 생년월일 미저장 | IMPLEMENT | UI_STATE | SCR-005 (로그인/프로필 탭) | 확인 게이트+저장 제약 |
| REQ-FUNC-029 | 프로필(닉네임/연령대/스타일/자기소개) | IMPLEMENT | UI_DIRECT | SCR-005 (프로필 탭) | |
| REQ-FUNC-030 | 국가/지역/기간/연령대/성별/스타일/모집상태 필터 | IMPLEMENT | UI_DIRECT | SCR-004 | |
| REQ-FUNC-031 | 모집글 작성 입력(제목/국가/지역/기간/인원/조건/스타일/설명/동의) | IMPLEMENT | UI_DIRECT | SCR-003 (동행 작성 탭) | |
| REQ-FUNC-032 | 연락처 패턴 탐지 후 제출 차단 | IMPLEMENT (축소) | UI_STATE | SCR-003 (동행 작성 탭) | 검증 로직 |
| REQ-FUNC-033 | 응답에서 이메일·연락처 노출 제외 | IMPLEMENT | NON_UI | - | 데이터 필터링 |
| REQ-FUNC-034 | 참가 메시지(≤500자) 비공개 제출 | IMPLEMENT | UI_DIRECT | SCR-004 (상세 패널) | |
| REQ-FUNC-035 | 동일 사용자 중복 PENDING/ACCEPTED 차단 | IMPLEMENT | UI_STATE | SCR-004 (상세 패널) | 검증 로직 |
| REQ-FUNC-036 | 작성자의 요청 승인/거절 | IMPLEMENT | UI_DIRECT | SCR-004 (상세 패널) | |
| REQ-FUNC-037 | 종료일 다음날 자동 CLOSED 전환 | IMPLEMENT | UI_STATE | SCR-004 | 조회 시 계산 |
| REQ-FUNC-038 | 작성자 수동 마감/수정/삭제+경고 | IMPLEMENT | UI_DIRECT | SCR-004 (상세 패널) | |
| REQ-FUNC-039 | 사유 코드+설명 신고 | IMPLEMENT | UI_DIRECT | SCR-004 (상세 패널) | |
| REQ-FUNC-040 | 사용자 차단·해제 | IMPLEMENT | UI_DIRECT | SCR-004 (트리거) / SCR-005 (내 활동 - 차단 관리) | |
| REQ-FUNC-041 | Moderator 신고 큐(상태 필터) | IMPLEMENT (간소화) | UI_DIRECT | SCR-005 (관리자 탭) | 우선순위·담당자 배정 없음 |
| REQ-FUNC-042 | 신고 상태 변경+대상 글 숨김 | IMPLEMENT (축소) | UI_DIRECT | SCR-005 (관리자 탭) | 경고/계정제한 기능 없음 |
| REQ-FUNC-043 | 접수/승인/거절/신고 결과 인앱 알림(이메일 선택) | IMPLEMENT (축소) | UI_DIRECT | 전역 Toast(SCR-003·004·005에서 트리거) | 실제 이메일 발송 없음 |
| REQ-FUNC-044 | RLS로 비공개 데이터 열람 제한 | IMPLEMENT | NON_UI | - | 백엔드 정책 |
| REQ-FUNC-045 | 탈퇴 시 비식별화+30일 내 삭제 | **EXCLUDED** | OPERATIONS | - | Supabase 콘솔 수동 처리로 대체(구현 범위 미포함) |

### 4.5 F5. Country Safety (046~056)

| ID | 요구사항 요약 | PROJECT_SCOPE 분류 | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-FUNC-046 | 게시 해외국가 전체에 안전 페이지 요구 | IMPLEMENT | NON_UI | - | 데이터 검증 스크립트 |
| REQ-FUNC-047 | 8개 필수 카테고리(치안/사기/법규/교통/재난/보건/문화/긴급연락처) | IMPLEMENT | UI_DIRECT | SCR-001 (안전 Modal/Drawer) | |
| REQ-FUNC-048 | 출처명·URL·최종 확인일·편집자 표기 | IMPLEMENT | UI_DIRECT | SCR-001 (안전 Modal/Drawer) | |
| REQ-FUNC-049 | 외교부 원문 링크(새 탭) | IMPLEMENT | UI_DIRECT | SCR-001 (안전 Modal/Drawer) | |
| REQ-FUNC-050 | 확인 7일 경과 시 stale 경고 | IMPLEMENT | UI_STATE | SCR-001 (안전 Modal/Drawer) | 렌더링 시 날짜 계산 |
| REQ-FUNC-051 | 중대 경보 텍스트로 상단 표시 | IMPLEMENT | UI_DIRECT | SCR-001 (안전 Modal/Drawer) | 색상 단독 사용 금지 |
| REQ-FUNC-052 | 국가/지역 경보 범위 필수 필드화 | IMPLEMENT | NON_UI | - | 데이터 검증 스크립트 |
| REQ-FUNC-053 | 긴급전화·영사콜센터 정보 표시 | IMPLEMENT | UI_DIRECT | SCR-001 (안전 Modal/Drawer) | |
| REQ-FUNC-054 | 공식 판단 대체 불가 고지 | IMPLEMENT | UI_DIRECT | SCR-001 (안전 Modal/Drawer), SCR-003 (항공 요약) | |
| REQ-FUNC-055 | Editor/Admin 콘텐츠 작성·검수·게시·보관 워크플로 | **EXCLUDED** | OPERATIONS | - | `src/data` 코드 배포/PR 프로세스로 대체 |
| REQ-FUNC-056 | 변경 이력(이전값/새값/사유/담당자/시각) 보존 | **EXCLUDED** | OPERATIONS | - | Git 커밋 이력으로 대체 |

### 4.6 F6. About free_traveler (057~063)

| ID | 요구사항 요약 | PROJECT_SCOPE 분류 | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-FUNC-057 | 대표명·`50+ Trips`·`30+ Countries` 표시 | IMPLEMENT | UI_DIRECT | SCR-002, SCR-001 (홈 소개 카드) | |
| REQ-FUNC-058 | 소개문·여행 철학·편집 원칙 | IMPLEMENT | UI_DIRECT | SCR-002 | |
| REQ-FUNC-059 | 방문 권역 지도/30개국 이상 목록 | IMPLEMENT | UI_DIRECT | SCR-002 | |
| REQ-FUNC-060 | 여행 타임라인 | IMPLEMENT | UI_DIRECT | SCR-002 | |
| REQ-FUNC-061 | 대표 이미지 alt·출처·작가·라이선스 | IMPLEMENT (축소) | UI_DIRECT | SCR-002 | |
| REQ-FUNC-062 | 문의·SNS 링크 | IMPLEMENT (축소) | UI_DIRECT | SCR-002 | |
| REQ-FUNC-063 | 대표 추천 여행지 6개 연결 | IMPLEMENT | UI_DIRECT | SCR-002 (→SCR-001 상세 Drawer 이동) | |

### 4.7 F7. Common, Admin, Governance (064~080)

| ID | 요구사항 요약 | PROJECT_SCOPE 분류 | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-FUNC-064 | 전역 내비게이션·푸터 | IMPLEMENT | UI_DIRECT | 전역(Layout, 5개 Screen 공통) | |
| REQ-FUNC-065 | 320px~데스크톱 반응형 | IMPLEMENT | UI_STATE | 전역(5개 Screen 공통) | 레이아웃 동작 |
| REQ-FUNC-066 | 이메일 가입/인증/로그인/로그아웃/비번재설정 | IMPLEMENT | UI_DIRECT | SCR-005 (로그인 탭) | |
| REQ-FUNC-067 | 여행지·안전정보 통합 검색 | IMPLEMENT | UI_DIRECT | SCR-001 | |
| REQ-FUNC-068 | 여행지 즐겨찾기(localStorage) | IMPLEMENT | UI_DIRECT | SCR-001 (등록), SCR-005 (내 활동 - 목록) | |
| REQ-FUNC-069 | URL 공유(Web Share/클립보드 폴백) | IMPLEMENT | UI_DIRECT | SCR-001, SCR-004 | |
| REQ-FUNC-070 | 공개 페이지 SEO 메타데이터 | IMPLEMENT | NON_UI | - | head 메타, 비가시 |
| REQ-FUNC-071 | 폼/외부클릭/안전조회/동행요청 이벤트 기록 | **EXCLUDED** | NON_UI | - | 이벤트 수집 파이프라인 미구현 |
| REQ-FUNC-072 | Editor/Admin 여행지 콘텐츠 CRUD | **EXCLUDED** | OPERATIONS | - | `src/data` 코드 배포로 대체(전체 콘텐츠 CMS 제외) |
| REQ-FUNC-073 | 미디어 업로드 시 출처/작가/라이선스/alt 필수 | **EXCLUDED** | OPERATIONS | - | 업로드·라이선스 승인 워크플로 미구현, URL+alt만 사용 |
| REQ-FUNC-074 | 게시 전 완전성 게이트 | IMPLEMENT (대체) | NON_UI | - | 데이터 검증 스크립트로 대체 |
| REQ-FUNC-075 | 안전정보 stale 현황·담당자 대시보드 | **EXCLUDED** | OPERATIONS | - | 관리자 탭 범위 축소(신고/외부URL만), stale 표시는 050으로 충족 |
| REQ-FUNC-076 | 관리자 변경·신고 처리·권한 변경 감사 로그 | **EXCLUDED** | OPERATIONS | - | 범용 감사 로그 미구현 |
| REQ-FUNC-077 | 항공·숙소 외부 URL 허용목록 설정 | IMPLEMENT | UI_DIRECT | SCR-005 (관리자 탭) | |
| REQ-FUNC-078 | 404/500/권한없음/외부연결실패 복구 행동 | IMPLEMENT | UI_DIRECT | 기술 Route(§3.1), 디자인 Screen 미포함 | |
| REQ-FUNC-079 | 폼/모달/탭/알림 시맨틱·ARIA | IMPLEMENT | UI_STATE | 전역(5개 Screen 공통) | 구현 관행 |
| REQ-FUNC-080 | 정책 페이지 제공+동행 안전수칙 동의 기록 | IMPLEMENT | UI_DIRECT | SCR-003 (동행 작성 탭, 동의 체크박스) / 정책 본문은 기술 Route(§3.1) | |

---

## 5. Requirement 매핑 — 비기능 요구사항 (REQ-NF-001~034)

### 5.1 Performance (001~007)

| ID | 요구사항 요약 | PROJECT_SCOPE 분류 | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-NF-001 | LCP p75 ≤2.5s | IMPLEMENT | NON_UI | - | 성능 지표 |
| REQ-NF-002 | INP p75 ≤200ms | IMPLEMENT | NON_UI | - | 성능 지표 |
| REQ-NF-003 | CLS p75 ≤0.1 | IMPLEMENT | NON_UI | - | 성능 지표 |
| REQ-NF-004 | 필터 응답 p95 ≤1s | IMPLEMENT | NON_UI | - | 성능 지표(SCR-001/004 필터 기반) |
| REQ-NF-005 | 쓰기 API 응답 p95 ≤3s | IMPLEMENT | NON_UI | - | 성능 지표 |
| REQ-NF-006 | 이미지 반응형·lazy load·priority | IMPLEMENT | UI_STATE | SCR-001, SCR-002 | 이미지 렌더링 동작 |
| REQ-NF-007 | 배포 전 Lighthouse 성능 예산 검사 | **EXCLUDED** | OPERATIONS | - | 자동 CI 게이트 미구축, 수동 점검 대체 |

### 5.2 Reliability and Recovery (008~011)

| ID | 요구사항 요약 | PROJECT_SCOPE 분류 | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-NF-008 | 월간 가용성 ≥99.5% | **EXCLUDED** | OPERATIONS | - | Vercel/Supabase 표준 SLA 의존 |
| REQ-NF-009 | 내부 API 5xx ≤0.5% | **EXCLUDED** | OPERATIONS | - | 모니터링 대시보드 미구축 |
| REQ-NF-010 | DB 백업 RPO≤24h/RTO≤8h | **EXCLUDED** | OPERATIONS | - | Supabase 기본 백업 정책 의존 |
| REQ-NF-011 | 외부 링크 주1회 자동 검사+Admin 알림 | **EXCLUDED** | OPERATIONS | - | 자동 점검·알림 미구축 |

### 5.3 Security and Privacy (012~018)

| ID | 요구사항 요약 | PROJECT_SCOPE 분류 | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-NF-012 | TLS 1.2 이상 | IMPLEMENT | NON_UI | - | |
| REQ-NF-013 | 인증·역할·RLS 서버 검증 | IMPLEMENT | NON_UI | - | |
| REQ-NF-014 | CSRF 방어·SameSite 쿠키 | IMPLEMENT | NON_UI | - | |
| REQ-NF-015 | 입력 검증·이스케이프, 저장 XSS 차단 | IMPLEMENT | NON_UI | - | |
| REQ-NF-016 | 비밀키 환경변수 관리 | IMPLEMENT | NON_UI | - | |
| REQ-NF-017 | 항공·호텔 원시 입력값 서버·분석 미보존 | IMPLEMENT | NON_UI | - | |
| REQ-NF-018 | 개인정보 내보내기·탈퇴·삭제 요청 제공 | **EXCLUDED** | OPERATIONS | - | Supabase 콘솔 수동 처리로 대체 |

### 5.4 Safety and Moderation (019~022)

| ID | 요구사항 요약 | PROJECT_SCOPE 분류 | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-NF-019 | 신고 접수 응답 p95 ≤3s | IMPLEMENT | NON_UI | - | 성능 지표(SCR-004 신고 UI 기반) |
| REQ-NF-020 | 신고 1차 검토 24h 이내 90%+ | **EXCLUDED** | OPERATIONS | - | 운영 SLA, 자동 모니터링 미구축 |
| REQ-NF-021 | 사용자별 글/요청/신고 속도 제한 | **EXCLUDED** | NON_UI | - | Rate limiting 미구현, 신고·차단으로 대응 |
| REQ-NF-022 | Moderator 조치 추적 가능성 | **EXCLUDED** | OPERATIONS | - | 범용 감사 로그 미구현 |

### 5.5 Accessibility (023~025)

| ID | 요구사항 요약 | PROJECT_SCOPE 분류 | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-NF-023 | WCAG 2.2 Level AA 목표 | IMPLEMENT | UI_STATE | 전역(5개 Screen 공통) | 설계 원칙 |
| REQ-NF-024 | 자동 접근성 검사(axe 등) | **EXCLUDED** | OPERATIONS | - | 자동 스캔 도구 미도입, Playwright Smoke로 한정 |
| REQ-NF-025 | 키보드·스크린리더 수동 검사 | IMPLEMENT (축소) | UI_STATE | 전역(핵심 흐름) | 수동 점검, 전수 인증 아님 |

### 5.6 Content, Freshness, SEO, Copyright (026~030)

| ID | 요구사항 요약 | PROJECT_SCOPE 분류 | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-NF-026 | 여행지 콘텐츠 완전성 100% | IMPLEMENT | NON_UI | - | 데이터 검증 스크립트 |
| REQ-NF-027 | 해외 국가 안전정보 커버리지 100% | IMPLEMENT | NON_UI | - | 데이터 검증 스크립트 |
| REQ-NF-028 | 안전정보 7일 이내 최신 확인 95%+ | IMPLEMENT | UI_STATE | SCR-001 | REQ-FUNC-050 stale 로직 재사용 |
| REQ-NF-029 | 공개 미디어 라이선스 메타데이터 100% | **EXCLUDED** | OPERATIONS | - | 업로드·라이선스 워크플로 미구현 |
| REQ-NF-030 | 공개 페이지 SEO 메타데이터 누락 0건 | IMPLEMENT | NON_UI | - | REQ-FUNC-070과 동일 구현 |

### 5.7 Maintainability, Monitoring, Cost (031~034)

| ID | 요구사항 요약 | PROJECT_SCOPE 분류 | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-NF-031 | TypeScript strict·lint·Playwright 병합 전 통과 | IMPLEMENT | OPERATIONS | - | 개발/CI 절차 |
| REQ-NF-032 | 구조화 로그(request_id 등) | **EXCLUDED** | NON_UI | - | Vercel 기본 로그로 대체 |
| REQ-NF-033 | 핵심 오류 5분 이내 알림 | **EXCLUDED** | OPERATIONS | - | 장애 알림 체계 미구축 |
| REQ-NF-034 | MVP 월 인프라 비용 목표 | IMPLEMENT | OPERATIONS | - | 요금제 선택·확인(비용 관리) |

---

## 6. 검증 요약

### 6.1 Requirement 총수 확인

| 구분 | 개수 |
|---|---:|
| REQ-FUNC-001~080 | 80 |
| REQ-NF-001~034 | 34 |
| **합계** | **114** |

REQ-FUNC-001~080, REQ-NF-001~034 전 항목이 4~5장 표에 정확히 1회씩 기록되었으며, 삭제되거나 누락된 ID는 없다.

### 6.2 UI 분류별 집계

| UI 분류 | FUNC | NF | 합계 |
|---|---:|---:|---:|
| UI_DIRECT | 50 | 0 | 50 |
| UI_STATE | 13 | 4 | 17 |
| NON_UI | 10 | 17 | 27 |
| OPERATIONS | 7 | 13 | 20 |
| **합계** | **80** | **34** | **114** |

### 6.3 PROJECT_SCOPE 분류 유지 확인

| PROJECT_SCOPE 분류 | FUNC | NF | 합계 | 비고 |
|---|---:|---:|---:|---|
| IMPLEMENT | 72 | 21 | 93 | `docs/PROJECT_SCOPE.md` §8과 동일 |
| EXCLUDED | 8 | 13 | 21 | `docs/PROJECT_SCOPE.md` §8과 동일, 본 문서에서 구현 범위로 되돌린 항목 없음 |

EXCLUDED 21개 목록(변경 없음): REQ-FUNC-045, 055, 056, 071, 072, 073, 075, 076 / REQ-NF-007, 008, 009, 010, 011, 018, 020, 021, 022, 024, 029, 032, 033

### 6.4 Design Screen 수 확인

핵심 디자인 Screen은 SCR-001~SCR-005 정확히 5개이며, 인증 콜백·API Route·오류 페이지·정책 콘텐츠 페이지는 기술 Route로 별도 집계하지 않는다(§3.1).
