# PROJECT_SCOPE — Free Traveler MVP

**Document ID:** SCOPE-TRAVEL-001
**기반 문서:** `docs/02_SRS_BASELINE.md` (SRS-TRAVEL-001 v1.0), `docs/01_PRD.md`
**비고:** `docs/01_PRD.md`는 현재 내용이 비어 있어 본 문서는 SRS Baseline과 프로젝트 지시 범위를 기준으로 작성한다. PRD가 채워지면 본 문서를 재검토한다.
**대상:** `package.json` 기준 Next.js App Router 프로젝트 (`src/app`, `src/data`)

---

## 1. 목적

이 문서는 SRS Baseline에 정의된 REQ-FUNC-001~080, REQ-NF-001~034 각각에 대해 이번 MVP에서 **직접 구현(IMPLEMENT)** 할지 **제외(EXCLUDED)** 할지를 확정하고, 구현 시 방식과 확인 방법을 기록한다. 요구사항은 하나도 삭제하지 않고 전수 기록한다.

---

## 2. 화면 구성

### 2.1 핵심 화면 (4)

| # | 화면 | 대응 라우트 | 포함 기능 |
|---|---|---|---|
| 1 | 홈 | `/` | 전역 진입, 4대 핵심 기능·대표 소개 진입점 |
| 2 | 여행지 탐색 | `/destinations`, `/destinations/domestic`, `/destinations/overseas`, `/destinations/[slug]` | 검색·필터·상세, 상세 내 국가 안전정보 패널 연결 |
| 3 | 항공·숙소 조건 입력 | `/flights`, `/hotels` | 입력·검증·요약·외부 이동 |
| 4 | 동행 모집 | `/mates`, `/mates/[id]`, `/mates/new` | 작성·조회·수정·마감, 참가 요청·승인·거절, 신고·차단 진입점 |

### 2.2 보조 화면 (1)

| # | 화면 | 대응 라우트 | 포함 기능 |
|---|---|---|---|
| 5 | 대표 소개 | `/about` | `free_traveler` 대표 소개, 방문 국가, 타임라인 |

### 2.3 지원 화면 (핵심/보조 화면 수 집계 외, 기능 요구사항 충족을 위해 필요)

| 화면 | 대응 라우트 | 비고 |
|---|---|---|
| 인증 | `/auth/*` | Supabase 이메일 인증, 로그인/로그아웃, 성인 확인 |
| 국가 안전정보 상세 | `/safety/[countryCode]` | 여행지 상세의 안전정보 패널에서 연결되는 서브 페이지 |
| 내 활동 + 관리자 탭 | `/my/*` | 내 글/참가 요청/차단 목록 + (Admin 권한에서만 노출되는) 관리자 탭 — 신고 상태 변경, 외부 URL 설정만 처리하는 간소화된 단일 탭 |

> 국가 안전정보는 요구사항 3에 따라 "패널"로 취급한다. 독립 목록(`/safety`)은 최소 구현으로 유지하고, 주 진입 경로는 여행지 상세의 안전정보 패널이다. 관리자 기능은 별도 `/admin/*` 섹션을 만들지 않고 `/my` 하위의 탭 하나로 축소한다.

---

## 3. 반드시 직접 구현할 범위 ↔ 요구사항 매핑

| # | 범위 | 관련 REQ |
|---|---|---|
| 1 | 핵심 화면 4개 + 보조 화면 1개 | REQ-FUNC-064, 065 (공통 셸) |
| 2 | 여행지 검색·필터·상세 패널 | REQ-FUNC-001~010 |
| 3 | 국가 안전정보 패널 | REQ-FUNC-046~054 |
| 4 | `free_traveler` 대표 소개 | REQ-FUNC-057~063 |
| 5 | 항공·숙소 입력·검증·요약·외부 이동 | REQ-FUNC-011~026, 077 |
| 6 | Supabase 이메일 인증과 성인 확인 | REQ-FUNC-027~028, 066 |
| 7 | 동행글 작성·조회·수정·마감 | REQ-FUNC-029~033, 037~038, 080 |
| 8 | 참가 요청·승인·거절 | REQ-FUNC-034~036, 043~044 |
| 9 | 간단한 차단·신고 | REQ-FUNC-039~040 |
| 10 | 내 활동과 간단한 관리자 탭 | REQ-FUNC-041~042, 077 |
| 11 | Playwright 핵심 Smoke Test | REQ-NF-031, REQ-FUNC-078~079 검증 수단 |
| 12 | Vercel 배포 | REQ-NF-012, 016, 034 |

---

## 4. 구현 방식

| 구현 방식 | 설명 | 적용 REQ |
|---|---|---|
| 여행지·안전·대표 콘텐츠는 `src/data` 정적 데이터 | DB CRUD·게시 상태 전이 없이 코드 배포로 콘텐츠 갱신. 필수 필드는 TypeScript 타입 + 데이터 검증 스크립트로 강제 | REQ-FUNC-004, 007~008, 046~048, 052, 057~061, 074, REQ-NF-026~027 |
| 즐겨찾기는 localStorage | 서버 저장 없이 브라우저별 즐겨찾기 목록 유지, 중복 방지는 클라이언트에서 처리 | REQ-FUNC-068 |
| 실제 이메일 알림은 Toast 또는 화면 상태 | 참가 요청/승인/거절/신고 처리 결과는 인앱 상태 배지·Toast로만 안내, 이메일 발송 연동 없음 | REQ-FUNC-043 |
| 자동 마감은 조회 시 종료일 계산 | 배치/트리거 없이 목록·상세 조회 시점에 `end_date` 경과 여부를 계산해 CLOSED로 표시 | REQ-FUNC-037 |
| 안전정보 stale은 렌더링 시 날짜 계산 | 별도 배치 없이 `verified_at` 대비 현재 시각을 렌더링 시 계산해 경고 표시 | REQ-FUNC-050, REQ-NF-028 |
| 이미지는 일반 인터넷 URL과 alt 텍스트만 사용 | Storage 업로드·라이선스 승인 없이 URL 필드 + 필수 alt, 출처/작가/라이선스는 선택 캡션으로 최소 표기 | REQ-FUNC-007, 061, REQ-NF-029 |
| 관리자는 신고 상태와 외부 URL 설정만 다룸 | `/my` 관리자 탭은 신고 상태 변경(+대상 글 숨김)과 항공/숙소 외부 URL 설정으로 한정, 그 외 콘텐츠 CRUD·감사 로그·SNS 링크 편집 UI 없음 | REQ-FUNC-041~042, 077 |

---

## 5. 제외 기능

| 제외 기능 | 제외 이유 | 관련 REQ (전부 EXCLUDED로 아래 5장/6장에 기록) |
|---|---|---|
| 전체 콘텐츠 CMS | 콘텐츠는 `src/data` 정적 파일로 코드 변경/PR로 관리, 인앱 작성·검수·게시 워크플로는 만들지 않음 | REQ-FUNC-055, 072 |
| 미디어 업로드·라이선스 승인 워크플로 | 이미지는 일반 URL + alt 텍스트만 사용, Storage 업로드·라이선스 검증 절차 없음 | REQ-FUNC-073, REQ-NF-029 |
| 범용 감사 로그 | 모든 관리자 행위에 대한 이전값/새값/사유/담당자 이력 테이블을 만들지 않음. 정적 콘텐츠 변경은 Git 이력으로 대체 | REQ-FUNC-056, 076, REQ-NF-022, 032 |
| 자동 백업·장애 알림·부하 테스트 | 가용성/에러율 모니터링, DB 백업 SLA, 외부 링크 자동 점검·알림, 부하 테스트 인프라를 구축하지 않음 | REQ-NF-007~011, 020, 033 |
| 외부 이메일 사업자 연동 | 알림은 Toast/화면 상태로 대체, 실제 이메일 발송 제공자 연동 없음 | REQ-FUNC-043(이메일 발송 부분) |
| EC2·AWS 인프라 | 배포는 Vercel + Supabase로 한정, 별도 AWS 인프라를 두지 않음 | 인프라 결정 사항 (특정 REQ 없음) |
| 무인 자동 Merge Runner | 코드 병합은 사람이 검토 후 수행, 자동 병합 봇을 두지 않음 | 운영 정책 사항 (특정 REQ 없음) |

그 외에 위 7개 범주에 직접 속하지 않지만, "반드시 직접 구현할 범위"(3장) 12개 항목에 포함되지 않아 이번 MVP에서 별도로 제외하는 항목은 REQ-FUNC-045, 071, 075, REQ-NF-018, 021, 024이며 사유는 6~7장의 해당 행에 개별 기록한다.

---

## 6. 기능 요구사항 상태 (REQ-FUNC-001~080)

범례 — IMPLEMENT: 구현하고 테스트 / EXCLUDED: 만들지 않으며 이유를 기록

### 6.1 F1. Destination Guide (001~010)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-001 | IMPLEMENT | 국내·해외 탭에서 `src/data`의 `scope` 필드로 목록 필터 | Playwright smoke: 탭 전환 시 해당 구분만 표시 |
| REQ-FUNC-002 | IMPLEMENT | 국가·도시·계절·테마·기간 다중 필터를 클라이언트 배열 필터 함수로 AND 결합 | 복수 필터 조합 결과를 Playwright로 확인, 정적 데이터라 응답은 즉시 |
| REQ-FUNC-003 | IMPLEMENT | 여행지명·국가명·테마 문자열에 대한 클라이언트 부분 일치 검색 | Playwright: 검색어 입력 후 결과/결과 없음 상태 확인 |
| REQ-FUNC-004 | IMPLEMENT | 상세 필수 필드(소개/명소 5+/추천 시기/1·3일 일정/예산/교통/음식 3+/에티켓/출처/수정일)를 TypeScript 타입으로 강제. 게시 상태 전이 UI는 없고 코드에 존재하는 데이터가 곧 게시본 | 데이터 검증 스크립트로 필드 누락 시 실패 처리 |
| REQ-FUNC-005 | IMPLEMENT | 필터 결과 0건 시 안내 문구 + 전체 초기화 버튼 컴포넌트 | Playwright: 조건 조합으로 빈 결과 유도 후 초기화 동작 확인 |
| REQ-FUNC-006 | IMPLEMENT | 여행지의 `countryCode`로 안전정보 데이터를 조회해 상세 하단 패널에 연결 | 데이터 검증 스크립트로 country_code 일치 확인 + Playwright 이동 확인 |
| REQ-FUNC-007 | IMPLEMENT (축소) | 이미지 URL + alt 텍스트를 필수로 하고, 출처·작가·라이선스는 선택 캡션으로만 최소 표기(강제 검증 없음) | 코드 리뷰로 alt 속성 존재 확인 |
| REQ-FUNC-008 | IMPLEMENT | 데이터 검증 스크립트로 `src/data`의 국내 10개 이상, 해외 15개국 30개 도시 이상 여부를 집계 | 스크립트 실행 결과(기준 미달 시 실패) |
| REQ-FUNC-009 | IMPLEMENT | 같은 국가·테마 조건으로 필터 후 최대 6개 slice, 비공개/현재 여행지 제외 | 수동 확인 |
| REQ-FUNC-010 | IMPLEMENT | 허용된 필터 키만 `useSearchParams`/router로 직렬화, 잘못된 값은 무시 | 수동 확인: 새로고침·URL 공유 시 필터 상태 복원 |

### 6.2 F2. Flight Link-out (011~018)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-011 | IMPLEMENT | 국가·지역·출발일·귀국일 4개 필수 입력 필드(라벨/도움말/오류 영역 포함) 폼 구현 | Playwright smoke |
| REQ-FUNC-012 | IMPLEMENT | `src/data` 국가-지역 매핑, 국가 변경 시 기존 지역값 초기화 | Playwright |
| REQ-FUNC-013 | IMPLEMENT | 클라이언트 검증 함수로 과거 출발일·역전 날짜 제출 차단 | Playwright 경계값 테스트 |
| REQ-FUNC-014 | IMPLEMENT | `useState` 기반 폼→요약 단계 전환, 브라우저 세션 동안 값 유지 | Playwright: 수정 버튼 왕복 시 값 유지 확인 |
| REQ-FUNC-015 | IMPLEMENT | 폼·요약 화면에 "입력값은 외부 사이트로 전달되지 않습니다" 고정 안내 | 코드 리뷰 + Playwright 문구 노출 확인 |
| REQ-FUNC-016 | IMPLEMENT | 환경변수 `FLIGHT_OUTBOUND_URL`을 `window.open`으로 새 탭 오픈, `noopener,noreferrer` 적용, query 미부착 | Playwright: 새 탭에 목적지/날짜 query 없음, opener 접근 불가 확인 |
| REQ-FUNC-017 | IMPLEMENT | 항공 폼 전용 서버 API/DB를 만들지 않고 전량 클라이언트 상태로만 처리 | 코드 리뷰(서버 라우트 없음) + 네트워크 탭 점검 |
| REQ-FUNC-018 | IMPLEMENT | 외부 URL 미설정/허용목록 밖이면 이동을 차단하고 Toast 오류 + 재시도 버튼 제공(별도 운영 로그 시스템은 미구축) | Playwright: URL 미설정 케이스 |

### 6.3 F3. Hotel Link-out (019~026)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-019 | IMPLEMENT | 국가·지역·체크인·체크아웃 4개 필수 입력 필드 폼 구현 | Playwright smoke |
| REQ-FUNC-020 | IMPLEMENT | 국가별 지역 매핑, 국가 변경 시 지역값 초기화 | Playwright |
| REQ-FUNC-021 | IMPLEMENT | 체크인 과거/체크아웃≤체크인 제출 차단 | Playwright 경계값 테스트 |
| REQ-FUNC-022 | IMPLEMENT | 폼→요약 단계에서 값이 입력과 정확히 일치하도록 표시 | Playwright |
| REQ-FUNC-023 | IMPLEMENT | 폼·요약에 입력값 비전달 고지 표시 | Playwright 문구 노출 확인 |
| REQ-FUNC-024 | IMPLEMENT | 환경변수 `HOTEL_OUTBOUND_URL`을 새 탭 오픈, `noopener,noreferrer` 적용 | Playwright: query 미부착 확인 |
| REQ-FUNC-025 | IMPLEMENT | 호텔 폼도 서버 API/DB 없이 클라이언트 상태로만 처리 | 코드 리뷰 + 네트워크 탭 점검 |
| REQ-FUNC-026 | IMPLEMENT | URL 오류 시 이동 차단, 현재 입력 유지, Toast 오류 표시(운영 로그 시스템은 별도 구축 안 함) | Playwright |

### 6.4 F4. Travel Mate (027~045)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-027 | IMPLEMENT | Supabase Auth 세션 확인 가드(서버 액션/미들웨어)로 비로그인 쓰기 차단 | Playwright: 비로그인 접근 401/리다이렉트 확인 |
| REQ-FUNC-028 | IMPLEMENT | `user_profile.is_adult`, `adult_verified_at`만 저장, 생년월일 미저장 | 코드 리뷰(스키마 확인) |
| REQ-FUNC-029 | IMPLEMENT | 닉네임·연령대·여행 스타일 필수, 성별 선택 프로필 폼 | Playwright |
| REQ-FUNC-030 | IMPLEMENT | Supabase 쿼리로 국가/지역/기간 겹침/연령대/성별/스타일/모집상태 필터, 차단 사용자 글 제외 | Playwright + RLS 확인 |
| REQ-FUNC-031 | IMPLEMENT | 제목/국가/지역/기간/인원/조건/스타일/설명/안전수칙 동의 입력 폼, 필수값·역전 날짜·과거 종료일 차단 | Playwright |
| REQ-FUNC-032 | IMPLEMENT (축소) | 정규식 기반 전화번호·이메일·메신저 ID 패턴 탐지 후 제출 차단 | 샘플 패턴 유닛/Playwright 테스트로 검증(95% 탐지율/5% 오탐 KPI는 별도 정량 측정하지 않음) |
| REQ-FUNC-033 | IMPLEMENT | 응답/렌더링에서 이메일·전화번호 등 연락처 필드 제외 | 코드 리뷰(응답 스키마 확인) |
| REQ-FUNC-034 | IMPLEMENT | 참가 메시지(≤500자) Supabase insert, PENDING 저장, RLS로 작성자·요청자만 열람 | Playwright + RLS 테스트 |
| REQ-FUNC-035 | IMPLEMENT | `post_id + applicant_id` 조합 unique 제약(PENDING/ACCEPTED) + UI 오류 안내 | 재요청 시나리오 테스트 |
| REQ-FUNC-036 | IMPLEMENT | 작성자만 status PATCH 가능하도록 RLS/서버 액션 권한 검사 | Playwright + 비작성자 403 확인 |
| REQ-FUNC-037 | IMPLEMENT | 배치/트리거 없이 조회 시점에 `end_date` 경과 여부를 계산해 CLOSED로 표시 | 날짜 mocking 테스트 |
| REQ-FUNC-038 | IMPLEMENT | 작성자 수동 마감/수정/삭제, 승인된 요청자가 있으면 경고 표시 | Playwright |
| REQ-FUNC-039 | IMPLEMENT | 사유 코드 + 설명 기반 신고 Supabase insert, 접수 즉시 ID 표시 | Playwright |
| REQ-FUNC-040 | IMPLEMENT | `user_block` 테이블 기반 차단/해제, 상호 노출 제한 쿼리 조건 적용 | 차단 후 프로필/글/요청 미노출 테스트 |
| REQ-FUNC-041 | IMPLEMENT (간소화) | `/my` 관리자 탭에서 OPEN/REVIEWING/RESOLVED/DISMISSED 상태 필터 목록만 제공(우선순위·담당자 배정 없음) | Playwright |
| REQ-FUNC-042 | IMPLEMENT (축소) | 신고 상태를 RESOLVED/DISMISSED로 변경 + 대상 글을 HIDDEN으로 전환하는 기능만 제공. 경고 발송, 계정 일시 제한 기능은 제공하지 않음 | Playwright |
| REQ-FUNC-043 | IMPLEMENT (축소) | 인앱 Toast/상태 배지로만 알림 제공, 실제 이메일 발송 없음 | Playwright: 상태 변경 후 Toast 노출 확인 |
| REQ-FUNC-044 | IMPLEMENT | Supabase RLS 정책으로 본인 글/요청, 요청 대상 작성자, Moderator/Admin만 비공개 데이터 열람 | 권한별 접근 테스트(403/빈 결과) |
| REQ-FUNC-045 | EXCLUDED | "반드시 직접 구현할 범위" 12개 항목에 회원 탈퇴 플로우가 포함되지 않음. 비식별화·예약 삭제 배치와 예외 사유 기록은 자동화 파이프라인·범용 감사 로그 제외 범위와 겹쳐 MVP에서 제외. 필요 시 Supabase 콘솔에서 수동 처리 | 해당 없음 |

### 6.5 F5. Country Safety (046~056)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-046 | IMPLEMENT | `src/data`에서 게시된 해외 국가와 안전정보를 1:1로 매핑 | 데이터 검증 스크립트 |
| REQ-FUNC-047 | IMPLEMENT | 안전정보 타입에 치안/사기/법규/교통/재난·기후/보건/문화·복장/긴급연락처 8개 필수 필드 정의 | 데이터 검증 스크립트 |
| REQ-FUNC-048 | IMPLEMENT | 출처명·URL·최종 확인일·편집자 필드를 정적 데이터에 기록 | 데이터 검증 스크립트 |
| REQ-FUNC-049 | IMPLEMENT | 외교부 해외안전여행 원문 링크를 `target=_blank`, `rel=noopener noreferrer`로 제공 | Playwright |
| REQ-FUNC-050 | IMPLEMENT | 렌더링 시 `verifiedAt`과 현재 시각 차이를 계산해 7일 초과 시 stale 경고 표시 | 날짜 mocking 테스트 |
| REQ-FUNC-051 | IMPLEMENT | 경보 단계·행동요령·적용 범위를 텍스트로 상단 표시(색상 단독 사용 금지) | 코드 리뷰 + Playwright |
| REQ-FUNC-052 | IMPLEMENT | `scope_type`/`scope_text` 필드를 지역 경보 게시 시 필수화 | 데이터 검증 스크립트 |
| REQ-FUNC-053 | IMPLEMENT | 현지 긴급전화·영사콜센터 연락 정보를 정적 데이터 필드로 렌더링 | 수동 확인 |
| REQ-FUNC-054 | IMPLEMENT | 안전정보가 공식 판단을 대체하지 않는다는 고지를 안전 페이지·항공 요약 화면에 고정 표시 | 코드 리뷰 |
| REQ-FUNC-055 | EXCLUDED | 콘텐츠는 `src/data` 정적 파일로 코드 변경/PR을 통해 관리한다. 인앱 작성·검수·게시 상태 전이 워크플로는 제외 목록의 "전체 콘텐츠 CMS"에 해당해 만들지 않음 | 해당 없음 |
| REQ-FUNC-056 | EXCLUDED | 변경 이력(이전값/새값/사유/담당자/시각) 보존은 제외 목록의 "범용 감사 로그"에 해당. 정적 데이터 변경 이력은 Git 커밋 기록으로 대체 | 해당 없음 |

### 6.6 F6. About free_traveler (057~063)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-057 | IMPLEMENT | 대표명·`50+ Trips`·`30+ Countries`를 단일 정적 데이터 소스로 홈/대표 페이지에서 공유 | Playwright: 두 위치 값 일치 확인 |
| REQ-FUNC-058 | IMPLEMENT | 소개문·여행 철학·편집 원칙을 정적 데이터로 표시 | 수동 확인 |
| REQ-FUNC-059 | IMPLEMENT | 30개국 이상 방문 국가 목록(이름+권역)을 정적 데이터로 표시 | 데이터 검증 스크립트(count ≥ 30) |
| REQ-FUNC-060 | IMPLEMENT | 연도·장소·요약을 포함한 여행 타임라인을 정적 데이터로 표시 | 수동 확인 |
| REQ-FUNC-061 | IMPLEMENT (축소) | 이미지 URL + alt 필수, 출처·작가·라이선스는 선택 캡션으로 최소 표기 | 코드 리뷰 |
| REQ-FUNC-062 | IMPLEMENT (축소) | 문의/SNS 링크를 정적 데이터로 하드코딩. 관리자 설정 범위는 신고 상태·외부 URL(항공/숙소)로 한정되므로 이 링크의 관리자 편집 UI는 제공하지 않음 | 코드 리뷰 + 링크 동작 확인 |
| REQ-FUNC-063 | IMPLEMENT | 정적 데이터 cross-reference로 대표 추천 여행지 6개 연결, 비공개 여행지 자동 제외 | 수동 확인 |

### 6.7 F7. Common, Admin, Governance (064~080)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-064 | IMPLEMENT | 전역 Layout 컴포넌트에 내비게이션/푸터 구현 | Playwright: 핵심 기능·정책 페이지 2회 이내 도달 |
| REQ-FUNC-065 | IMPLEMENT | Tailwind 반응형 유틸리티로 320px~데스크톱 레이아웃 대응 | Playwright viewport 테스트 |
| REQ-FUNC-066 | IMPLEMENT | Supabase Auth로 이메일 가입/인증/로그인/로그아웃/비밀번호 재설정 구현 | Playwright smoke |
| REQ-FUNC-067 | IMPLEMENT | 정적 데이터 기반 통합 검색 함수로 여행지·안전정보 결과에 유형 라벨 표시 | Playwright |
| REQ-FUNC-068 | IMPLEMENT | localStorage에 즐겨찾기 destinationId 배열 저장, 중복 방지 로직 적용 | Playwright: localStorage 값 확인 |
| REQ-FUNC-069 | IMPLEMENT | Web Share API 시도 후 실패 시 URL 클립보드 복사로 폴백 | Playwright: 폴백 동작 확인 |
| REQ-FUNC-070 | IMPLEMENT | Next.js Metadata API로 공개 페이지별 title/description/canonical/OG/구조화 데이터 적용 | Playwright: head 태그 존재 확인 |
| REQ-FUNC-071 | EXCLUDED | "반드시 직접 구현할 범위" 12개 항목에 별도 행동 분석 이벤트 파이프라인이 포함되지 않음. MVP는 핵심 기능 검증에 집중하고 이벤트 수집·스키마는 구현하지 않음 | 해당 없음 |
| REQ-FUNC-072 | EXCLUDED | 제외 목록 "전체 콘텐츠 CMS"에 해당. 콘텐츠는 `src/data` 정적 파일로 관리 | 해당 없음 |
| REQ-FUNC-073 | EXCLUDED | 제외 목록 "미디어 업로드·라이선스 승인 워크플로"에 해당. 이미지는 URL + alt만 사용 | 해당 없음 |
| REQ-FUNC-074 | IMPLEMENT (대체) | 관리자 게시 워크플로 대신 데이터 검증 스크립트/테스트로 필수 필드 누락을 빌드·테스트 단계에서 검출 | 스크립트/CI 실행 결과 |
| REQ-FUNC-075 | EXCLUDED | 관리자 탭 범위를 "신고 상태와 외부 URL 설정"으로 한정했으므로 담당자 필터를 포함한 별도 stale 대시보드는 제공하지 않음. stale 표시 자체는 REQ-FUNC-050으로 충족 | 해당 없음 |
| REQ-FUNC-076 | EXCLUDED | 제외 목록 "범용 감사 로그"에 해당 | 해당 없음 |
| REQ-FUNC-077 | IMPLEMENT | 관리자 탭에서 항공/숙소 외부 URL을 HTTPS·허용목록 내 값으로만 저장(HTTP/`javascript:`/`data:` 거부) | Playwright + 저장값 검증 |
| REQ-FUNC-078 | IMPLEMENT | Next.js 커스텀 404/500/권한없음/외부연결실패 페이지에 재시도·홈 이동 버튼 제공 | Playwright |
| REQ-FUNC-079 | IMPLEMENT | 폼/모달/탭/알림에 시맨틱 HTML과 ARIA 속성을 코드 작성 시 적용(자동 스캔 도구는 사용하지 않음) | 코드 리뷰 + Playwright 키보드 동작 확인 |
| REQ-FUNC-080 | IMPLEMENT | 이용약관/개인정보처리방침/동행 안전수칙/콘텐츠 면책 정적 페이지 제공, 모집글 작성 시 동의 체크박스와 동의 시각을 Supabase에 저장 | Playwright |

---

## 7. 비기능 요구사항 상태 (REQ-NF-001~034)

### 7.1 Performance (001~007)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-001 | IMPLEMENT | 정적 데이터 + `next/image` 최적화로 LCP 목표 설계 | 수동 Lighthouse 측정(자동 CI 게이트 미구축) |
| REQ-NF-002 | IMPLEMENT | 경량 클라이언트 상태, 불필요한 리렌더 최소화로 INP 목표 설계 | 수동 측정 |
| REQ-NF-003 | IMPLEMENT | 이미지 크기 명시, 폰트 스왑 최소화로 CLS 목표 설계 | 수동 측정 |
| REQ-NF-004 | IMPLEMENT | 정적 데이터 클라이언트 필터로 네트워크 왕복 없이 즉시 응답하도록 구조화 | 수동 확인(부하 테스트 도구 미사용, 정적 데이터 구조상 자명) |
| REQ-NF-005 | IMPLEMENT | Supabase 단순 insert/update로 쓰기 API 구현 | 수동 측정(정식 부하 테스트 제외) |
| REQ-NF-006 | IMPLEMENT | `next/image` 컴포넌트로 반응형·lazy load 적용, LCP 이미지는 priority 지정 | 코드 리뷰 |
| REQ-NF-007 | EXCLUDED | 자동 Lighthouse CI 게이트는 "자동 백업·장애 알림·부하 테스트" 제외 범위와 동일 맥락으로 구축하지 않음. 필요 시 수동 점검으로 대체 | 해당 없음 |

### 7.2 Reliability and Recovery (008~011)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-008 | EXCLUDED | 가용성 SLA 모니터링 체계는 제외 목록 "자동 백업·장애 알림"에 해당. Vercel/Supabase 표준 SLA에 의존 | 해당 없음 |
| REQ-NF-009 | EXCLUDED | 5xx 비율 모니터링 대시보드는 위와 동일 사유로 제외 | 해당 없음 |
| REQ-NF-010 | EXCLUDED | DB 백업 RPO/RTO 별도 구축은 제외 목록 "자동 백업"에 해당. Supabase 기본 백업 정책에 의존 | 해당 없음 |
| REQ-NF-011 | EXCLUDED | 외부 링크 주 1회 자동 검사 및 Admin 알림은 제외 목록 "장애 알림" 자동화에 해당 | 해당 없음 |

### 7.3 Security and Privacy (012~018)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-012 | IMPLEMENT | Vercel/Supabase 기본 제공 HTTPS 사용 | 배포 URL HTTPS 확인 |
| REQ-NF-013 | IMPLEMENT | Supabase RLS 정책으로 인증/역할을 서버에서 검증 | 권한별 접근 테스트 |
| REQ-NF-014 | IMPLEMENT | Next.js Server Actions 내장 보호 + Supabase Auth 쿠키 SameSite 설정 적용 | 설정 코드 리뷰 |
| REQ-NF-015 | IMPLEMENT | React 기본 이스케이프 + 서버 측 입력 검증으로 저장 XSS 차단 | 코드 리뷰 + 테스트 케이스 |
| REQ-NF-016 | IMPLEMENT | `.env.local`/Vercel 환경변수로 비밀키 관리, 클라이언트 번들 미포함 확인 | 빌드 산출물 점검 |
| REQ-NF-017 | IMPLEMENT | 항공/호텔 폼 전용 서버 API를 만들지 않아 원시 입력값을 서버·분석에 보존하지 않음 | 네트워크/DB 점검 |
| REQ-NF-018 | EXCLUDED | "반드시 직접 구현할 범위" 12개 항목에 미포함. REQ-FUNC-045와 동일 사유로 MVP 제외, 필요 시 Supabase 콘솔에서 수동 처리 | 해당 없음 |

### 7.4 Safety and Moderation (019~022)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-019 | IMPLEMENT | Supabase 단순 insert로 신고 접수 즉시 응답 | 수동 측정 |
| REQ-NF-020 | EXCLUDED | 신고 1차 검토 24h 90% 지표는 운영 SLA로, 자동 모니터링 인프라가 필요해 "장애 알림" 제외 범위와 동일 맥락으로 제외 | 해당 없음 |
| REQ-NF-021 | EXCLUDED | "반드시 직접 구현할 범위" 12개 항목에 미포함. Rate limiting 미들웨어는 MVP에서 제외하고 신고·차단 기능으로 악용에 대응 | 해당 없음 |
| REQ-NF-022 | EXCLUDED | 제외 목록 "범용 감사 로그"에 해당 | 해당 없음 |

### 7.5 Accessibility (023~025)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-023 | IMPLEMENT | 시맨틱 HTML/ARIA 적용 원칙으로 WCAG 2.2 AA를 목표로 설계 | 코드 리뷰 |
| REQ-NF-024 | EXCLUDED | 테스트 도구는 "Playwright 핵심 Smoke Test"로 한정, axe 등 자동 접근성 스캔 도구는 도입하지 않음 | 해당 없음 |
| REQ-NF-025 | IMPLEMENT (축소) | 핵심 흐름에 대한 키보드 탐색 수동 점검(스크린리더 전수 검사·100% 인증은 제외) | Playwright + 수동 점검 |

### 7.6 Content, Freshness, SEO, Copyright (026~030)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-026 | IMPLEMENT | 데이터 검증 스크립트로 여행지 콘텐츠 완전성 100% 확인 | 스크립트 실행 |
| REQ-NF-027 | IMPLEMENT | 데이터 검증 스크립트로 해외 국가 안전정보 커버리지 100% 확인 | 스크립트 실행 |
| REQ-NF-028 | IMPLEMENT | REQ-FUNC-050의 stale 계산 로직 재사용. "7일 이내 95% 이상 최신 유지"는 콘텐츠 운영 지표로 코드 검증 범위 밖이며, stale 배지 노출 정확성만 검증 | 날짜 mocking 테스트 |
| REQ-NF-029 | EXCLUDED | 제외 목록 "미디어 업로드·라이선스 승인 워크플로"에 해당. 이미지는 URL + alt만 사용 | 해당 없음 |
| REQ-NF-030 | IMPLEMENT | Next.js Metadata API를 전 공개 페이지에 적용(REQ-FUNC-070과 동일 구현) | Playwright |

### 7.7 Maintainability, Monitoring, Cost (031~034)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-031 | IMPLEMENT | TypeScript strict + ESLint + Playwright 핵심 Smoke Test를 병합 전 확인 절차로 사용(별도 단위 테스트 프레임워크는 도입하지 않음) | CI/로컬 명령 실행 결과 |
| REQ-NF-032 | EXCLUDED | 범용 구조화 로깅/모니터링 파이프라인은 "범용 감사 로그"·"장애 알림" 제외 범위와 동일 맥락으로 구축하지 않음. Vercel 기본 로그로 대체 | 해당 없음 |
| REQ-NF-033 | EXCLUDED | 제외 목록 "장애 알림"에 해당 | 해당 없음 |
| REQ-NF-034 | IMPLEMENT | Vercel + Supabase 무료/최소 유료 플랜 사용으로 월 인프라 비용 목표 충족 | 요금제 확인(자동 비용 모니터링 도구는 구축하지 않음) |

---

## 8. 검증 요약

| 구분 | 총 개수 | IMPLEMENT | EXCLUDED |
|---|---:|---:|---:|
| REQ-FUNC-001~080 | 80 | 72 | 8 |
| REQ-NF-001~034 | 34 | 21 | 13 |
| 합계 | 114 | 93 | 21 |

EXCLUDED 목록: REQ-FUNC-045, 055, 056, 071, 072, 073, 075, 076 / REQ-NF-007, 008, 009, 010, 011, 018, 020, 021, 022, 024, 029, 032, 033
