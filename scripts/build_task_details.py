#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert TASKS/00_TASK_LIST.md rows into per-task detail files.

Reads the single Markdown Task List (source of truth for this project —
there is no separate tasks/TASK_LIST.json), validates it, and writes
TASKS/TASK-<ID>.md for every implementation Task row (1:1). EXCLUDED
requirement rows live only in the NON_IMPLEMENTATION table and never get a
detail file.

Usage:
    python scripts/build_task_details.py

Exit code 0 = files written successfully (pre-checks passed).
Exit code 1 = validation failed, no files written.
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
TASK_LIST_PATH = ROOT / "TASKS" / "00_TASK_LIST.md"
OUT_DIR = ROOT / "TASKS"

COLS = [
    "task_id", "title", "category", "impl_status", "req_ref",
    "screen", "route", "page_entry", "depends_on", "expected_files",
]


def parse_task_list(text):
    """Parses every '| <seq> | ... |' row in TASKS/00_TASK_LIST.md into dicts."""
    tasks = []
    for line in text.splitlines():
        m = re.match(r'^\|\s*(\d+)\s*\|(.*)\|\s*$', line)
        if not m:
            continue
        seq = int(m.group(1))
        rest = [c.strip() for c in m.group(2).split('|')]
        if len(rest) != len(COLS):
            continue  # not a task-table row (e.g. a 2-column summary row)
        row = {"seq": seq}
        row.update(dict(zip(COLS, rest)))
        tasks.append(row)
    return tasks


def parse_excluded(text):
    excluded = []
    in_section = False
    for line in text.splitlines():
        if line.startswith("## 1. NON_IMPLEMENTATION"):
            in_section = True
            continue
        if in_section and line.startswith("## 2."):
            break
        if in_section:
            m = re.match(r'^\|\s*(REQ-(?:FUNC|NF)-\d{3})\s*\|', line)
            if m:
                excluded.append(m.group(1))
    return excluded


def split_ids(cell):
    if cell in ("-", "", "없음"):
        return []
    return [x.strip() for x in cell.split(",") if x.strip() and x.strip() != "-"]


def validate(tasks, excluded):
    errors = []

    ids = [t["task_id"] for t in tasks]
    dupes = sorted(set(x for x in ids if ids.count(x) > 1))
    if dupes:
        errors.append("중복 Task ID: {}".format(dupes))

    for t in tasks:
        for required in ("task_id", "title", "category", "impl_status"):
            if not t.get(required):
                errors.append("Task {} 의 필수 열 '{}' 이 비어 있습니다".format(t.get("task_id", "?"), required))

    id_set = set(ids)
    for t in tasks:
        for dep in split_ids(t["depends_on"]):
            dep_clean = dep.strip("` ")
            # Some dependency notes carry parenthetical detail, e.g. "PAGE-SCR001~005(배포 후)"
            base = re.split(r'[\(（]', dep_clean)[0].strip()
            if "~" in base or "*" in base:
                continue  # documented wildcard/range note, not a literal single ID
            if base and base not in id_set:
                errors.append("Task {} 의 Depends On '{}' 이 Task List에 없습니다".format(t["task_id"], base))

    excl_dupes = sorted(set(x for x in excluded if excluded.count(x) > 1))
    if excl_dupes:
        errors.append("NON_IMPLEMENTATION 표에 중복된 Requirement: {}".format(excl_dupes))

    overlap = id_set & set(excluded)
    if overlap:
        errors.append("Task ID와 EXCLUDED Requirement ID가 겹칩니다: {}".format(overlap))

    db_tasks = [t for t in tasks if t["category"] == "Database"]
    if len(db_tasks) > 6:
        errors.append("Database Task가 6개를 초과합니다: {}개".format(len(db_tasks)))

    page_owners = [t for t in tasks if t["category"] == "Page Owner"]
    seen_entries = {}
    for t in page_owners:
        pe = t["page_entry"]
        if pe in seen_entries:
            errors.append("Page Entry {} 를 {}와 {}가 동시에 소유합니다".format(pe, seen_entries[pe], t["task_id"]))
        seen_entries[pe] = t["task_id"]

    return errors


# ---------------------------------------------------------------------------
# Hand-authored per-task metadata (priority, verify, context, test cases,
# design ref, extra forbidden items). Group-level AC text is reproduced
# verbatim from TASKS/00_TASK_LIST.md so it stays consistent with the
# approved Task List rather than being re-derived.
# ---------------------------------------------------------------------------

PRIORITY = {
    "PAGE-SCR001": "P0", "PAGE-SCR002": "P1", "PAGE-SCR003": "P0", "PAGE-SCR004": "P0", "PAGE-SCR005": "P0",
    "COMP-SCR001-HERO-SEARCH": "P0", "COMP-SCR001-DOMESTIC-GRID": "P0", "COMP-SCR001-OVERSEAS-GRID": "P0",
    "COMP-SCR001-DEST-DRAWER": "P1", "COMP-SCR001-THEME-CHIPS": "P1", "COMP-SCR001-SAFETY-PANEL": "P0",
    "COMP-SCR001-MATES-TEASER": "P1", "COMP-SCR001-FOUNDER-BAND": "P1",
    "COMP-SCR002-HERO": "P1", "COMP-SCR002-STATS": "P1", "COMP-SCR002-INTRO": "P2",
    "COMP-SCR002-TIMELINE": "P1", "COMP-SCR002-COUNTRY-CHIPS": "P2", "COMP-SCR002-GALLERY": "P1",
    "COMP-SCR002-MEMORABLE-CTA": "P2",
    "COMP-SCR003-INTRO-TABS-SHELL": "P1", "COMP-SCR003-FLIGHT-FORM": "P0", "COMP-SCR003-HOTEL-FORM": "P0",
    "COMP-SCR003-SUMMARY-ACTION": "P0", "COMP-SCR003-TIPS": "P2", "COMP-SCR003-MATE-LOGIN-GATE": "P0",
    "COMP-SCR003-MATE-WRITE-FORM": "P0",
    "COMP-SCR004-FILTER-BAR": "P0", "COMP-SCR004-POST-LIST": "P0", "COMP-SCR004-DETAIL-PANEL": "P0",
    "COMP-SCR004-APPLY-FORM": "P0", "COMP-SCR004-REPORT-ACTION": "P1", "COMP-SCR004-BLOCK-ACTION": "P1",
    "COMP-SCR005-AUTH": "P0", "COMP-SCR005-PROFILE": "P0", "COMP-SCR005-MY-ACTIVITY": "P0",
    "COMP-SCR005-ADMIN-REPORTS": "P1", "COMP-SCR005-ADMIN-URL-SETTINGS": "P1",
    "COMP-GLOBAL-HEADER-FOOTER": "P0", "COMP-GLOBAL-TOAST": "P0", "COMP-GLOBAL-EMPTY-STATE": "P0",
    "COMP-GLOBAL-DESIGN-TOKENS": "P0", "COMP-GLOBAL-LOADING-STATE": "P0", "COMP-GLOBAL-ERROR-STATE": "P0",
    "COMP-TECH-ERROR-PAGES": "P1", "COMP-TECH-POLICY-PAGES": "P2",
    "DATA-DESTINATIONS": "P0", "DATA-SAFETY": "P0", "DATA-REPRESENTATIVE": "P1", "DATA-VALIDATION-SCRIPT": "P0",
    "DB-SCHEMA-BASE": "P0", "DB-RLS-BASE": "P0", "DB-ACCESS": "P0", "DB-SEED-BASE": "P2",
    "API-MATE-POSTS": "P0", "API-MATE-APPLICATIONS": "P0", "API-BLOCKS-REPORTS": "P0",
    "API-AUTH-PROFILE": "P0", "API-ADMIN-SETTINGS": "P0",
    "UNIT-TRAVEL-DATES": "P0", "UNIT-CONTACT-DETECTION": "P0", "UNIT-MATE-STATE": "P0",
    "TEST-RLS-BASIC": "P0",
    "E2E-PUBLIC-SMOKE": "P0", "E2E-TRAVEL-TOOLS": "P0", "E2E-MATE-AUTH": "P0",
    "MANUAL-RESPONSIVE-DENSITY": "P1", "MANUAL-ACCESSIBILITY-KEYBOARD": "P1", "MANUAL-PERFORMANCE-LIGHTHOUSE": "P1",
    "CI-QUALITY-GATE": "P0", "RELEASE-CHECK-VERCEL-SUPABASE": "P1",
}

VERIFY = {
    "PAGE-SCR001": "E2E-PUBLIC-SMOKE, MANUAL-RESPONSIVE-DENSITY",
    "PAGE-SCR002": "E2E-PUBLIC-SMOKE, MANUAL-RESPONSIVE-DENSITY",
    "PAGE-SCR003": "E2E-TRAVEL-TOOLS, UNIT-TRAVEL-DATES, MANUAL-RESPONSIVE-DENSITY",
    "PAGE-SCR004": "E2E-MATE-AUTH, TEST-RLS-BASIC, MANUAL-RESPONSIVE-DENSITY",
    "PAGE-SCR005": "E2E-MATE-AUTH, TEST-RLS-BASIC, MANUAL-RESPONSIVE-DENSITY",
    "_SCR001_COMPONENT": "E2E-PUBLIC-SMOKE",
    "_SCR002_COMPONENT": "E2E-PUBLIC-SMOKE",
    "_SCR003_COMPONENT": "E2E-TRAVEL-TOOLS, E2E-MATE-AUTH, UNIT-TRAVEL-DATES",
    "_SCR004_COMPONENT": "E2E-MATE-AUTH, TEST-RLS-BASIC, UNIT-MATE-STATE",
    "_SCR005_COMPONENT": "E2E-MATE-AUTH, TEST-RLS-BASIC",
    "_GLOBAL": "MANUAL-ACCESSIBILITY-KEYBOARD, MANUAL-RESPONSIVE-DENSITY",
    "_TECH": "E2E-PUBLIC-SMOKE",
    "_DATA": "DATA-VALIDATION-SCRIPT 자체 실행(CI-QUALITY-GATE에 포함)",
    "_DB": "TEST-RLS-BASIC",
    "_API": "TEST-RLS-BASIC, UNIT-MATE-STATE, E2E-MATE-AUTH",
    "_UNIT": "CI-QUALITY-GATE",
    "TEST-RLS-BASIC": "CI-QUALITY-GATE",
    "_E2E": "CI-QUALITY-GATE",
    "_MANUAL": "없음(Manual Check 자체가 검증 수단)",
    "CI-QUALITY-GATE": "CI 실행 로그",
    "RELEASE-CHECK-VERCEL-SUPABASE": "CI 실행 로그",
}

GROUP_VERIFY_KEY = {
    "COMP-SCR001": "_SCR001_COMPONENT", "COMP-SCR002": "_SCR002_COMPONENT",
    "COMP-SCR003": "_SCR003_COMPONENT", "COMP-SCR004": "_SCR004_COMPONENT",
    "COMP-SCR005": "_SCR005_COMPONENT", "COMP-GLOBAL": "_GLOBAL", "COMP-TECH": "_TECH",
    "DATA": "_DATA", "DB": "_DB", "API": "_API",
    "UNIT": "_UNIT", "E2E": "_E2E", "MANUAL": "_MANUAL",
}


def verify_for(task_id, category):
    if task_id in VERIFY:
        return VERIFY[task_id]
    for prefix, key in GROUP_VERIFY_KEY.items():
        if task_id.startswith(prefix):
            return VERIFY[key]
    return "-"


# Group-level common AC text, copied verbatim from TASKS/00_TASK_LIST.md so the
# detail files stay word-for-word consistent with the approved Task List.
GROUP_AC = {
    "COMP-SCR001": {
        "functional": "각 Component는 지정된 구현 방법을 따른다 — 여행지/안전/대표 콘텐츠는 `DATA-*` 정적 데이터만 읽고 DB를 호출하지 않는다(REQ-FUNC-008/046/052 데이터 계층 검증은 DATA-VALIDATION-SCRIPT 담당). 즐겨찾기는 localStorage(`favorites` key, JSON 배열)만 사용한다. API-MATE-POSTS를 호출하는 MATES-TEASER는 COMP-GLOBAL-LOADING-STATE/COMP-GLOBAL-ERROR-STATE로 로딩·오류 상태를 표시한다(나머지 Component는 정적 데이터만 사용하므로 해당 없음).",
        "visual": "Card는 사진 우선(`radius.md`), 국내/해외 Grid는 배경 톤 또는 배지로 시각적으로 구분한다(동일 레이아웃 반복 금지). 빈 Card·Lorem ipsum·준비 중 금지.",
        "security": "전부 Public 컴포넌트, 인증 불필요. 안전정보 배지는 텍스트+아이콘 병기(색상 단독 금지).",
    },
    "COMP-SCR002": {
        "functional": "전부 `DATA-REPRESENTATIVE` 정적 데이터만 사용. Gallery 이미지는 실제 촬영 장소를 설명하는 alt 텍스트를 필수로 가진다(일반 URL 이미지, 업로드 워크플로 없음).",
        "visual": "Section마다 시각 패턴을 다르게 한다(Hero/Stat/좌우분할/Timeline/Chip/Gallery/CTA Banner가 서로 다른 레이아웃). Lorem ipsum·빈 Card 금지.",
        "security": "전부 Public.",
    },
    "COMP-SCR003": {
        "functional": "항공·숙소·동행 작성 세 영역은 서로 다른 파일/컴포넌트로 분리하고, 세 영역의 입력·검증·완료 상태는 서로 독립적으로 유지한다(탭 전환 시 값 보존은 IntroTabsShell이 상위 상태로 관리).",
        "visual": "각 Form은 라벨+도움말+오류 영역을 갖추고 Lorem ipsum·준비 중 금지. MATE-LOGIN-GATE(인증 상태 확인)와 MATE-WRITE-FORM(제출)은 COMP-GLOBAL-LOADING-STATE/COMP-GLOBAL-ERROR-STATE를 사용하고, FLIGHT-FORM/HOTEL-FORM/SUMMARY-ACTION/TIPS/INTRO-TABS-SHELL은 서버 호출이 없어 해당 없음.",
        "security": "FLIGHT-FORM/HOTEL-FORM은 입력값을 `useState` 등 브라우저 상태로만 유지하고 서버 API·URL 쿼리로 전송하지 않는다(REQ-FUNC-017, REQ-FUNC-025). MATE-WRITE-FORM은 제출 전 정규식으로 전화번호·이메일·메신저 ID 패턴을 탐지해 차단한다(REQ-FUNC-032, UNIT-CONTACT-DETECTION 연동).",
    },
    "COMP-SCR004": {
        "functional": "목록·필터·상세·참가·신고·차단을 각각 독립 컴포넌트/파일로 유지한다(단일 컴포넌트로 합치지 않음). 신고·차단은 상세에서 열람 중인 특정 게시글·작성자를 대상으로 동작하며(COMP-SCR004-DETAIL-PANEL 의존), 대상 없이 독립적으로 호출되지 않는다. 차단된 상대의 글은 목록·상세에서 제외한다.",
        "visual": "검색 결과 0건은 COMP-GLOBAL-EMPTY-STATE(필터 초기화+작성 CTA+이용 방법)로 표시. Supabase 조회/제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도 포함)를 표시한다(POST-LIST/DETAIL-PANEL/APPLY-FORM/REPORT-ACTION/BLOCK-ACTION). Lorem ipsum·빈 Card 금지.",
        "security": "참가 요청 내용은 작성자·요청자만 열람(RLS). 신고·차단은 로그인 필요. 응답/렌더링에 이메일·전화번호 노출 금지(REQ-FUNC-033).",
    },
    "COMP-SCR005": {
        "functional": "Guest/Member/Admin 4영역(Auth/Profile/My Activity/Admin)을 파일 단위로 분리한다. Admin 컴포넌트는 Admin 역할이 아니면 import된 채로도 렌더링되지 않는다(조건부 렌더링, 코드 존재 자체는 금지 아님).",
        "visual": "My Activity의 각 목록(내 글/참가요청/차단/즐겨찾기) 0건 시 완성형 Empty State. Supabase 조회/제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도 포함)를 표시한다(AUTH/PROFILE/MY-ACTIVITY/ADMIN-REPORTS/ADMIN-URL-SETTINGS 전부). Lorem ipsum·빈 Card 금지.",
        "security": "성인 인증은 `is_adult`/`adult_verified_at`만 저장하고 생년월일 원본은 저장하지 않는다(REQ-FUNC-028). Admin 컴포넌트는 서버 측 역할 검증과 함께 사용(클라이언트 조건부 렌더링만으로 신뢰하지 않음).",
    },
    "COMP-GLOBAL": {
        "functional": "`design-reference/D-001/DESIGN.md`의 Color Token·Typography·Spacing·Radius·Shadow를 Tailwind 테마로 그대로 옮긴다. Toast는 서버 저장 없이 클라이언트 상태(예: `useToast` 훅)로만 동작한다. Supabase에서 데이터를 읽거나 쓰는 모든 Component(POST-LIST/DETAIL-PANEL/APPLY-FORM/REPORT-ACTION/BLOCK-ACTION/AUTH/PROFILE/MY-ACTIVITY/ADMIN-REPORTS/ADMIN-URL-SETTINGS/MATE-LOGIN-GATE/MATE-WRITE-FORM/MATES-TEASER)는 COMP-GLOBAL-LOADING-STATE(요청 진행 중)와 COMP-GLOBAL-ERROR-STATE(요청 실패+재시도 버튼)를 공용으로 사용한다 — 정적 데이터만 쓰는 Component(SCR-001/002의 나머지, SCR-003의 FLIGHT-FORM/HOTEL-FORM/SUMMARY-ACTION/TIPS/INTRO-TABS-SHELL)는 해당 없음.",
        "visual": "Header는 Desktop 72px/Mobile 56px 높이, nav 4개(여행지/여행 도구/동행/대표소개) + 로그인 영역. Footer는 서비스/정책/문의 3컬럼(Mobile 1컬럼). LoadingState는 Skeleton 또는 Spinner+안내 문구, ErrorState는 오류 메시지+재시도 버튼을 갖춘 완성형 블록으로 빈 화면·무한 스피너를 남기지 않는다.",
        "security": "해당 없음(순수 UI/스타일 계층).",
    },
    "COMP-TECH": {
        "functional": "404/500 화면은 각각 홈으로 이동·다시 시도 중 최소 1개 복구 행동을 제공한다. 정책 페이지는 정적 콘텐츠이며 COMP-SCR003-MATE-WRITE-FORM의 동의 체크박스가 이 페이지를 링크한다.",
        "visual": "Lorem ipsum·준비 중 금지, 실제 정책 문구를 채운다.",
        "security": "해당 없음.",
    },
    "DATA": {
        "functional": "지정된 구현 방법 = 정적 데이터(TypeScript 배열/객체, DB 미사용). `DATA-DESTINATIONS`는 국내 10개 이상·해외 15개국 30개 도시 이상을 포함하고 소개·명소 5개 이상·1일/3일 일정·예산·교통·음식 3개 이상·에티켓·출처·수정일 필드를 강제하는 TypeScript 타입을 가진다. `DATA-SAFETY`는 치안/사기/법규/교통/재난/보건/문화/긴급연락처 8개 카테고리와 출처·확인일·편집자 필드를 강제한다. `DATA-VALIDATION-SCRIPT`는 `npm run build` 전(또는 별도 `npm run validate:content`)에 수량·필수 필드 누락을 검사해 실패 시 빌드를 중단한다.",
        "visual": "해당 없음(데이터 계층).",
        "security": "이미지 URL은 일반 인터넷 URL만 사용, 업로드 저장소 없음.",
    },
    "DB": {
        "functional": "테이블은 정확히 6개로 제한한다(여행지·안전·대표 콘텐츠는 DB에 넣지 않고 정적 데이터로 처리). `mate_posts`에 `safety_consent_at`(REQ-FUNC-080 동의 시각) 컬럼을 포함한다.",
        "visual": "해당 없음.",
        "security": "6개 테이블 모두 RLS 활성화, 본인/요청 대상 작성자/Moderator·Admin만 비공개 행 열람. `DB-ACCESS`는 이메일·전화번호를 클라이언트 응답에서 select 단계부터 제외한다(REQ-FUNC-033). CSRF/SameSite·입력 검증은 Server Action 기본 보호+명시적 zod 스키마 검증으로 처리.",
    },
    "API": {
        "functional": "모든 쓰기는 Supabase Server Action을 통해서만 수행하고 클라이언트에서 직접 테이블을 쓰지 않는다. `API-MATE-POSTS`의 자동 마감은 별도 배치 없이 조회 시점에 `end_date` 경과 여부를 계산해 표시한다(REQ-FUNC-037).",
        "visual": "해당 없음(서버 계층).",
        "security": "`API-ADMIN-SETTINGS`는 HTTPS·허용목록 도메인만 저장하고 `http:`/`javascript:`/`data:` URL을 거부한다(REQ-FUNC-077). `API-AUTH-PROFILE`은 생년월일 원본을 저장하지 않는다(REQ-FUNC-028).",
    },
    "UNIT": {
        "functional": "날짜 검증은 경계값(오늘, 당일 체크인/체크아웃, 역전 날짜)을 포함한다. 연락처 탐지는 기준 테스트셋에서 탐지율/오탐률을 기록만 하고(정량 KPI는 축소) 정규식 케이스를 유닛으로 고정한다. 상태 전이는 중복 요청 차단·비작성자 승인 거부·자동 마감 포함.",
        "visual": "해당 없음.",
        "security": "해당 없음.",
    },
    "TEST-RLS-BASIC": {
        "functional": "본인/타인/Moderator/Admin 4개 역할 조합으로 각 테이블 select/insert/update를 시도해 허용·거부가 설계대로 동작하는지 확인.",
        "visual": "해당 없음.",
        "security": "비인가 접근이 전부 403 또는 빈 결과인지 확인.",
    },
    "E2E": {
        "functional": "`playwright.config.ts`는 `chromium` 프로젝트만 정의한다(firefox/webkit 프로젝트 없음). 3개 Task가 여행지 탐색, 안전정보 열람, 대표소개, 항공 이동, 숙소 이동, 동행 작성+로그인 유도, 참가 요청까지 핵심 5~7개 흐름을 커버한다.",
        "visual": "각 흐름에서 Lorem ipsum·준비 중·빈 Card가 렌더링되지 않는지 텍스트 스냅샷으로 확인.",
        "security": "외부 이동 시 새 탭 URL에 목적지·날짜 쿼리가 없는지 확인(REQ-FUNC-016, REQ-FUNC-024).",
    },
    "MANUAL": {
        "functional": "자동 CI 게이트가 없는 항목(REQ-NF-007/024 EXCLUDED)을 사람이 배포 후 직접 확인하고 결과를 `TASKS/checks/*.md`에 기록한다.",
        "visual": "SCR-001/SCR-003 Card Grid가 Desktop 3열/Mobile 1열로 전환되는지, 빈 여백이 과도하지 않은지 스크린샷으로 확인.",
        "security": "해당 없음.",
    },
    "CI": {
        "functional": "CI는 `tsc --noEmit`, `eslint`, `playwright test --project=chromium`을 병합 전 필수로 실행한다. EC2·AWS 인프라, 자동 Merge Runner는 만들지 않는다.",
        "visual": "해당 없음.",
        "security": "비밀키는 Vercel/GitHub Actions 환경변수로만 관리하고 클라이언트 번들에 포함되지 않는지 빌드 산출물로 확인. HTTPS(TLS 1.2+)는 Vercel 기본값 확인.",
    },
}


def group_key_for(task_id, category):
    if category == "Page Owner":
        return None
    if task_id.startswith("COMP-SCR001"):
        return "COMP-SCR001"
    if task_id.startswith("COMP-SCR002"):
        return "COMP-SCR002"
    if task_id.startswith("COMP-SCR003"):
        return "COMP-SCR003"
    if task_id.startswith("COMP-SCR004"):
        return "COMP-SCR004"
    if task_id.startswith("COMP-SCR005"):
        return "COMP-SCR005"
    if task_id.startswith("COMP-GLOBAL"):
        return "COMP-GLOBAL"
    if task_id.startswith("COMP-TECH"):
        return "COMP-TECH"
    if task_id.startswith("DATA"):
        return "DATA"
    if task_id.startswith("DB"):
        return "DB"
    if task_id.startswith("API"):
        return "API"
    if task_id.startswith("UNIT"):
        return "UNIT"
    if task_id == "TEST-RLS-BASIC":
        return "TEST-RLS-BASIC"
    if task_id.startswith("E2E"):
        return "E2E"
    if task_id.startswith("MANUAL"):
        return "MANUAL"
    if task_id in ("CI-QUALITY-GATE", "RELEASE-CHECK-VERCEL-SUPABASE"):
        return "CI"
    return None


# Page-Owner-specific AC, copied verbatim from TASKS/00_TASK_LIST.md.
PAGE_OWNER_AC = {
    "PAGE-SCR001": {
        "functional": [
            "create-next-app Starter(로고·\"Get started\"·Vercel 배포 링크) 완전 제거 후 교체.",
            "Section 순서: ①검색 Hero ②국내 여행지 6개 Card ③해외 여행지 6개 Card ④여행 동기 6개 Chip ⑤국가별 주의사항 6개 Card ⑥최근 동행글 3개 또는 완성형 Empty State ⑦free_traveler 소개.",
            "Section별 데이터 출처: ②③ DATA-DESTINATIONS, ⑤ DATA-SAFETY, ⑦ DATA-REPRESENTATIVE, ⑥ API-MATE-POSTS.",
            "Desktop(1440px) 콘텐츠 최대폭 1200~1280px·Section 여백 64~96px·Card 3열, Mobile(390px) 여백 40~64px·Card 1열.",
            "이 Task는 Component를 새로 만들지 않고 Depends On에 있는 Component/Data/API Task의 결과물만 import해 조립한다.",
        ],
        "visual": [
            "Hero 높이 제한 — 1440px 기준 다음 Section 제목이 폴드 안에 보여야 함.",
            "Lorem ipsum·\"준비 중\"·\"정보 확인 필요\"·내용 없는 빈 Card 금지.",
            "⑥ 동행글 0건 시 안내 문장+이용 방법 3단계+\"동행 모집글 작성하기\" CTA를 갖춘 완성형 Empty State.",
            "⑥ 동행글 로딩 중 COMP-GLOBAL-LOADING-STATE, 조회 실패 시 COMP-GLOBAL-ERROR-STATE(재시도) 표시.",
        ],
        "security": [
            "전 Section Public 열람 가능.",
            "즐겨찾기는 localStorage만 사용하고 서버로 전송하지 않음.",
        ],
    },
    "PAGE-SCR002": {
        "functional": [
            "Section 순서: ①Profile Hero ②여행 지표 ③소개·철학 ④Timeline ⑤방문 국가 ⑥Gallery ⑦기억에 남는 여행지+CTA.",
            "최소 콘텐츠 수: Timeline 6개 이상, 방문 국가 30개(권역별), Gallery 8장 이상(실제 지명 alt), 추천 여행지 4개.",
            "전 Section 데이터 출처: DATA-REPRESENTATIVE.",
            "Desktop 콘텐츠 최대폭 1200~1280px, Section 여백 64~96px.",
            "이 Task는 Component를 새로 만들지 않고 Depends On의 Component/Data Task 결과물만 조립한다.",
        ],
        "visual": [
            "Hero 높이 제한, 다음 Section 폴드 내 노출.",
            "Lorem ipsum·준비 중·정보 확인 필요·빈 Card 금지.",
            "정적 콘텐츠이므로 Empty State 없음 — 대신 최소 콘텐츠 수 미달 시 DATA-VALIDATION-SCRIPT가 게시를 차단.",
            "전 Section이 빌드 타임 정적 데이터만 사용해 런타임 네트워크 호출이 없으므로 Loading/Error State도 해당 없음.",
        ],
        "security": ["전체 Public, 인증 불필요."],
    },
    "PAGE-SCR003": {
        "functional": [
            "Section 순서: ①Intro(3단계 안내) ②탭(항공편 찾기/숙소 찾기/동행 구하기) ③여행정보 Form ④입력 요약·외부 이동 ⑤찾기 Tip 3개 ⑥동행 작성 또는 로그인 안내·안전 안내.",
            "3탭을 하나의 탭 컨테이너에 실제로 조립하고 탭 전환 시 다른 탭 입력 상태를 유지.",
            "항공·숙소 입력값은 브라우저 상태로만 처리, 서버 API·DB·분석·외부 URL 쿼리 어디에도 전송하지 않음.",
            "이 Task는 FlightForm/HotelForm/MateWriteForm 등 하위 Component를 새로 만들지 않고 Depends On의 결과물만 탭 컨테이너에 조립한다.",
        ],
        "visual": [
            "Lorem ipsum·준비 중·정보 확인 필요·빈 Card 금지.",
            "동행 탭 비로그인 시 완성형 로그인 안내(설명+CTA)를 표시(빈 화면 금지).",
            "로그인 상태 확인 중과 동행글 제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도)를 표시(항공·숙소 탭은 서버 호출이 없어 해당 없음).",
        ],
        "security": [
            "동행 작성은 로그인+성인 인증 필요(COMP-SCR003-MATE-LOGIN-GATE).",
            "항공·호텔 입력값 비전송(REQ-FUNC-017, REQ-FUNC-025).",
            "외부 링크는 `noopener,noreferrer`로 새 탭.",
        ],
    },
    "PAGE-SCR004": {
        "functional": [
            "Section 순서: ①Intro+작성 CTA ②Filter·결과 요약 ③동행 목록(최대 8개 우선 노출) ④상세(Desktop 좌우 분할/Mobile 상세 Drawer, 작성자·게시글 대상 신고·차단 버튼 포함) ⑤신청 방법 3단계 ⑥동행 안전수칙 요약 안내.",
            "목록·필터·상세·참가·신고·차단을 각각 별도 Component Task로 조립(단일 컴포넌트로 합치지 않음), 신고·차단은 상세에서 열람 중인 특정 게시글·작성자를 대상으로 동작한다.",
            "이 Task는 하위 Component를 새로 만들지 않고 Depends On의 결과물만 페이지에 배치한다.",
        ],
        "visual": [
            "검색 결과 0건 시 필터 초기화+작성 CTA+이용 방법을 갖춘 완성형 Empty State.",
            "Lorem ipsum·준비 중·정보 확인 필요·빈 Card 금지.",
            "목록·상세 조회 중과 참가·신고·차단 제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도)를 표시.",
        ],
        "security": [
            "참가 요청·신고·차단은 로그인 필요.",
            "RLS로 본인 글/요청만 비공개 데이터 열람(DB-RLS-BASE).",
        ],
    },
    "PAGE-SCR005": {
        "functional": [
            "Section(역할별 영역) 순서 - Guest: 계정 Intro → 로그인/가입/비밀번호 재설정 Card → 로그인 후 가능한 기능 안내 → 보안 안내. Member: 프로필·성인 확인 요약 → 내 글 → 참가 요청 → 차단 목록 → 즐겨찾기 목록 → 새 동행글 작성 CTA. Admin: 관리 Intro → 신고 상태 변경(+대상 글 숨김) → 항공·숙소 외부 URL 설정.",
            "현재 역할(Guest/Member/Admin)의 Intro→핵심 작업→도움말/다음 행동을 실제로 조건부 렌더링.",
            "역할에 없는 관리 영역(예: Member의 Admin 탭)은 렌더링 자체를 하지 않음.",
            "Dashboard·통계형 화면을 만들지 않음.",
            "이 Task는 Auth/Profile/MyActivity/AdminReports/AdminUrlSettings Component를 새로 만들지 않고 역할별 조건부 조립만 한다.",
        ],
        "visual": [
            "내 글/참가 요청/차단/즐겨찾기/신고 큐가 0건일 때 각각 완성형 Empty State(설명+이용 방법+다음 행동 CTA).",
            "Lorem ipsum·준비 중·정보 확인 필요·빈 Card 금지.",
            "인증·프로필·활동 내역·관리자 데이터 조회·제출 중에는 COMP-GLOBAL-LOADING-STATE, 실패 시 COMP-GLOBAL-ERROR-STATE(재시도)를 표시.",
        ],
        "security": [
            "Guest는 Member/Admin 탭에 접근 불가(탭 자체 미노출).",
            "Admin 범위는 신고 상태 변경·외부 URL 설정으로 한정(콘텐츠 CRUD·감사 로그 없음).",
        ],
    },
}

# Per-task Context (1-3 sentences) and Test Cases (2-5 concrete scenarios).
# Hand-written per task so this content is genuinely specific, not boilerplate.
TASK_NOTES = {
    "PAGE-SCR001": {
        "context": "SCR-001(`/`)의 Page Owner Task. create-next-app 기본 스캐폴드를 완전히 교체하고, 이미 만들어진 8개 Component와 3개 Data Task의 결과물을 7개 Section 순서로 조립하는 것이 유일한 책임이다.",
        "test_cases": [
            "빌드 후 `/`에 접속하면 create-next-app 기본 로고/문구가 전혀 남아있지 않다.",
            "1440px 뷰포트에서 Hero 아래로 스크롤 없이 Section ②의 제목이 보인다.",
            "동행글이 0건인 계정으로 접속했을 때 Section ⑥이 완성형 Empty State로 렌더링된다(빈 화면 아님).",
        ],
    },
    "PAGE-SCR002": {
        "context": "SCR-002(`/about`)의 Page Owner Task. `DATA-REPRESENTATIVE` 하나의 데이터 소스와 7개 Component를 순서대로 배치해 대표 소개 페이지를 완성한다.",
        "test_cases": [
            "Timeline이 6개 이상, 방문 국가가 30개, Gallery가 8장 이상 렌더링된다.",
            "Gallery 이미지 각각에 실제 장소를 설명하는 alt 텍스트가 있다.",
            "기억에 남는 여행지 Card를 클릭하면 SCR-001의 상세 Drawer로 이동한다.",
        ],
    },
    "PAGE-SCR003": {
        "context": "SCR-003(`/travel-tools`)의 Page Owner Task. 항공/숙소/동행 구하기 3탭을 실제로 하나의 화면에 조립하고, 탭 전환 시 각 탭의 입력 상태가 독립적으로 보존되도록 상위 상태를 관리한다.",
        "test_cases": [
            "항공 탭에 값을 입력한 뒤 숙소 탭으로 전환하고 다시 항공 탭으로 돌아오면 입력값이 그대로 남아 있다.",
            "네트워크 탭을 확인했을 때 항공/숙소 폼 제출로 인한 서버 요청이 발생하지 않는다.",
            "비로그인 상태에서 동행 구하기 탭을 열면 작성 Form 대신 로그인 안내 카드가 보인다.",
        ],
    },
    "PAGE-SCR004": {
        "context": "SCR-004(`/mates`)의 Page Owner Task. Filter/목록/상세/참가/신고/차단 6개 Component를 조립해 목록形+상세 분할(Desktop) 또는 목록→Drawer(Mobile) 레이아웃을 완성한다.",
        "test_cases": [
            "조건에 맞는 글이 없을 때 필터 초기화 버튼과 작성 CTA가 있는 Empty State가 보인다.",
            "Desktop 1440px에서는 좌측 목록+우측 상세 패널이 동시에 보이고, Mobile 390px에서는 상세가 Drawer로 열린다.",
            "차단한 사용자의 글이 목록에 나타나지 않는다.",
        ],
    },
    "PAGE-SCR005": {
        "context": "SCR-005(`/account`)의 Page Owner Task. 로그인 상태와 역할(Guest/Member/Admin)에 따라 5개 Component 중 해당하는 것만 조건부로 렌더링한다.",
        "test_cases": [
            "Guest로 접속하면 로그인/가입 폼만 보이고 Profile·My Activity·Admin 탭은 DOM에 존재하지 않는다.",
            "Member로 로그인하면 Admin 탭이 보이지 않는다.",
            "Admin으로 로그인하면 신고 큐와 외부 URL 설정만 보이고 콘텐츠 CRUD·통계 화면은 없다.",
        ],
    },
    "COMP-SCR001-HERO-SEARCH": {
        "context": "SCR-001 Hero 안의 여행지/국가/테마 키워드 검색 Bar. 날짜·인원 선택 없이 텍스트 검색만 제공한다.",
        "test_cases": [
            "키워드 입력 후 검색 시 DATA-DESTINATIONS 기준으로 국내+해외 결과가 필터링된다.",
            "빈 검색어로 제출해도 오류 없이 전체 목록이 유지된다.",
            "검색창에 날짜 선택기나 인원 선택 UI가 없다.",
        ],
    },
    "COMP-SCR001-DOMESTIC-GRID": {
        "context": "국내 여행지 6개를 Card Grid로 렌더링한다. DATA-DESTINATIONS에서 scope가 국내인 항목만 사용한다.",
        "test_cases": [
            "6개 Card가 Desktop 3열/Mobile 1열로 렌더링된다.",
            "Card 클릭 시 COMP-SCR001-DEST-DRAWER가 같은 화면 위에 열린다.",
            "즐겨찾기 버튼 클릭 시 localStorage의 `favorites` 배열에 destinationId가 추가/제거된다.",
        ],
    },
    "COMP-SCR001-OVERSEAS-GRID": {
        "context": "해외 여행지 6개를 Card Grid로 렌더링하고 각 Card에 국가 안전 배지를 표시한다.",
        "test_cases": [
            "6개 Card가 국내 Grid와 다른 배경 톤/배지로 시각적으로 구분된다.",
            "국가 배지 클릭 시 COMP-SCR001-SAFETY-PANEL의 해당 국가 상세가 열린다.",
        ],
    },
    "COMP-SCR001-DEST-DRAWER": {
        "context": "여행지 상세 정보를 같은 화면 위 Drawer로 표시한다. 소개/명소/일정/예산/교통/음식/에티켓/출처/수정일 필드를 렌더링한다.",
        "test_cases": [
            "관련 여행지 추천이 최대 6개까지만 표시된다.",
            "공유 버튼 클릭 시 Web Share API 또는 실패 시 클립보드 복사 폴백이 동작한다.",
            "해외 여행지의 경우 안전정보로 이동하는 링크가 있다.",
        ],
    },
    "COMP-SCR001-THEME-CHIPS": {
        "context": "여행 동기·테마 6개를 Chip으로 표시하고 선택 시 목록 필터와 URL query를 동기화한다.",
        "test_cases": [
            "Chip 선택 시 국내/해외 Grid가 해당 테마로 필터링된다.",
            "필터 적용 후 새로고침해도 동일한 Chip이 선택된 상태로 복원된다.",
        ],
    },
    "COMP-SCR001-SAFETY-PANEL": {
        "context": "국가별 주의사항 6개 Card와 상세 Modal/Drawer. 8개 필수 카테고리, 출처, 최종 확인일, 7일 초과 시 재확인 경고를 표시한다.",
        "test_cases": [
            "최종 확인일이 7일 이전인 국가 Card에 재확인 필요 배지가 텍스트로 표시된다(색상 단독 아님).",
            "외교부 원문 링크가 새 탭 + `noopener,noreferrer`로 열린다.",
            "중대 경보는 텍스트로 상단에 표시되고 색상만으로 구분되지 않는다.",
        ],
    },
    "COMP-SCR001-MATES-TEASER": {
        "context": "SCR-001 하단에 최근 동행글 3개 또는 완성형 Empty State를 보여주는 티저. API-MATE-POSTS의 최신 3건을 재사용한다.",
        "test_cases": [
            "동행글이 3건 이상이면 최신 3건만 표시된다.",
            "0건일 때 아이콘+설명+3단계 이용 방법+작성 CTA를 갖춘 Empty State가 표시된다.",
        ],
    },
    "COMP-SCR001-FOUNDER-BAND": {
        "context": "free_traveler 대표 소개 요약과 SCR-002로 이동하는 CTA를 담은 좌우 분할 밴드.",
        "test_cases": [
            "50+ Trips / 30+ Countries 지표 값이 SCR-002와 동일하다.",
            "CTA 클릭 시 `/about`으로 이동한다.",
        ],
    },
    "COMP-SCR002-HERO": {
        "context": "대표 사진과 소개 한 줄 문장을 보여주는 Hero. 높이를 제한해 다음 Section이 폴드 안에 보이게 한다.",
        "test_cases": ["1440px에서 Hero 아래 여행 지표 Section 제목이 보인다."],
    },
    "COMP-SCR002-STATS": {
        "context": "50+ Trips / 30+ Countries 지표 카드.",
        "test_cases": ["두 지표 값이 SCR-001 FOUNDER-BAND와 동일하다."],
    },
    "COMP-SCR002-INTRO": {
        "context": "자기소개·여행을 시작한 이유·여행 철학 2~4개 문단과 문의/SNS 링크.",
        "test_cases": [
            "문단 수가 2~4개다.",
            "빈 링크는 렌더링하지 않고 허용된 프로토콜(https)만 연다.",
        ],
    },
    "COMP-SCR002-TIMELINE": {
        "context": "여행 Timeline, 최소 6개 시점을 연도·장소·요약과 함께 세로로 표시한다.",
        "test_cases": [
            "Timeline 항목이 6개 이상이다.",
            "각 항목에 연도/장소/한 줄 요약이 모두 있다.",
        ],
    },
    "COMP-SCR002-COUNTRY-CHIPS": {
        "context": "방문 국가 30개를 권역별로 그룹핑한 Chip 목록.",
        "test_cases": [
            "국가 수가 30개 이상이다.",
            "각 Chip에 국가명과 권역이 있다.",
        ],
    },
    "COMP-SCR002-GALLERY": {
        "context": "서로 다른 나라에서 찍은 사진 8장 이상의 Gallery.",
        "test_cases": [
            "사진이 8장 이상이다.",
            "각 사진 alt가 실제 장소를 설명한다(예: '페루 마추픽추 전망대').",
        ],
    },
    "COMP-SCR002-MEMORABLE-CTA": {
        "context": "기억에 남는 여행지 4개 Card와 항공·숙소 준비/동행 찾기 CTA.",
        "test_cases": [
            "Card가 4개다.",
            "비공개 여행지는 자동으로 추천 목록에서 제외된다.",
        ],
    },
    "COMP-SCR003-INTRO-TABS-SHELL": {
        "context": "3단계 이용 안내와 항공/숙소/동행 구하기 3탭 컨테이너. 탭 전환 시 각 탭의 입력 상태를 보존하는 상위 state를 관리한다.",
        "test_cases": [
            "탭을 전환해도 다른 탭에 입력한 값이 사라지지 않는다.",
            "3개 탭이 항상 항공→숙소→동행 구하기 순서로 존재한다.",
        ],
    },
    "COMP-SCR003-FLIGHT-FORM": {
        "context": "국가/지역/출발일/귀국일 입력 Form. 입력값은 브라우저 상태로만 유지한다.",
        "test_cases": [
            "출발일이 오늘 이전이면 제출이 차단된다.",
            "귀국일이 출발일보다 빠르면 제출이 차단된다.",
            "국가를 바꾸면 기존에 선택된 지역값이 초기화된다.",
            "브라우저 Network 탭에 입력값이 담긴 요청이 없다.",
        ],
    },
    "COMP-SCR003-HOTEL-FORM": {
        "context": "국가/지역/체크인/체크아웃 입력 Form. 입력값은 브라우저 상태로만 유지한다.",
        "test_cases": [
            "체크인이 오늘 이전이면 차단된다.",
            "체크아웃이 체크인과 같거나 이전이면 차단된다.",
            "Network 탭에 입력값 전송이 없다.",
        ],
    },
    "COMP-SCR003-SUMMARY-ACTION": {
        "context": "항공/숙소 입력 요약과 외부 사이트 이동 Action Card. 비전달 고지 문구를 포함한다.",
        "test_cases": [
            "요약 값이 입력 Form의 값과 정확히 일치한다.",
            "이동 버튼 클릭 시 새 탭이 `noopener,noreferrer`로 열리고 URL에 목적지/날짜 쿼리가 없다.",
            "외부 URL이 설정되지 않았거나 허용목록 밖이면 이동이 차단되고 재시도 안내가 보인다.",
        ],
    },
    "COMP-SCR003-TIPS": {
        "context": "항공·숙소 찾기 Tip 3개 Chip/Card.",
        "test_cases": ["Tip이 정확히 3개다."],
    },
    "COMP-SCR003-MATE-LOGIN-GATE": {
        "context": "동행 작성 접근 전 로그인+성인 인증 여부를 확인하는 게이트 UI.",
        "test_cases": [
            "비로그인 사용자에게는 작성 Form 대신 로그인 유도 카드가 보인다.",
            "로그인했지만 성인 인증이 안 된 사용자에게는 성인 인증 안내가 보인다.",
        ],
    },
    "COMP-SCR003-MATE-WRITE-FORM": {
        "context": "동행 모집글 작성 Form과 안전 안내. 제출 전 연락처 패턴을 탐지해 차단한다.",
        "test_cases": [
            "본문에 전화번호/이메일/메신저 ID 패턴이 있으면 제출이 차단되고 수정 안내가 보인다.",
            "안전수칙 동의 체크박스를 선택하지 않으면 제출할 수 없다.",
            "제출 성공 시 동의 시각이 함께 저장된다.",
        ],
    },
    "COMP-SCR004-FILTER-BAR": {
        "context": "국가/지역/기간/연령대/성별/스타일/모집상태 필터와 결과 요약.",
        "test_cases": [
            "여러 필터를 동시에 적용하면 AND 조건으로 결과가 좁혀진다.",
            "필터 초기화 버튼으로 전체 목록이 복원된다.",
        ],
    },
    "COMP-SCR004-POST-LIST": {
        "context": "동행글 목록, 최대 8개 우선 노출. 종료일이 지난 글은 자동으로 마감 표시한다.",
        "test_cases": [
            "종료일이 지난 글에 '마감' 배지가 표시된다(배치 없이 조회 시점 계산).",
            "본문/응답 어디에도 작성자의 이메일·전화번호가 노출되지 않는다.",
        ],
    },
    "COMP-SCR004-DETAIL-PANEL": {
        "context": "선택한 동행글의 상세 정보. Desktop은 목록 옆 패널, Mobile은 Drawer로 표시한다.",
        "test_cases": [
            "작성자 본인에게만 수정/마감/삭제 버튼이 보인다.",
            "비공개 데이터는 RLS로 본인/작성자만 조회된다.",
        ],
    },
    "COMP-SCR004-APPLY-FORM": {
        "context": "참가 요청 메시지(500자 이내) 작성 Form과 신청 방법 3단계 안내.",
        "test_cases": [
            "500자를 초과하면 제출이 막힌다.",
            "이미 PENDING/ACCEPTED 상태로 신청한 글에는 중복 신청이 차단된다.",
        ],
    },
    "COMP-SCR004-REPORT-ACTION": {
        "context": "사유 코드+설명으로 신고를 제출하는 UI.",
        "test_cases": [
            "신고 제출 시 접수 ID가 화면에 표시된다.",
            "사유 코드를 선택하지 않으면 제출할 수 없다.",
        ],
    },
    "COMP-SCR004-BLOCK-ACTION": {
        "context": "사용자 차단·해제 버튼과 안전 안내 CTA.",
        "test_cases": [
            "차단 후 해당 사용자의 글/프로필이 더 이상 목록에 보이지 않는다.",
            "차단 해제 시 다시 노출된다.",
        ],
    },
    "COMP-SCR005-AUTH": {
        "context": "Guest 대상 로그인/가입/비밀번호 재설정 Form.",
        "test_cases": [
            "이메일 인증 없이는 동행 쓰기 권한이 부여되지 않는다.",
            "비밀번호 재설정 이메일 발송 흐름이 동작한다.",
        ],
    },
    "COMP-SCR005-PROFILE": {
        "context": "Member 프로필(닉네임/연령대/여행 스타일/자기소개)과 성인 확인 상태 요약.",
        "test_cases": [
            "닉네임/연령대/여행 스타일은 필수, 성별은 선택 입력이다.",
            "성인 확인 상태가 배지로 표시된다.",
        ],
    },
    "COMP-SCR005-MY-ACTIVITY": {
        "context": "내 글/참가 요청/차단 목록/즐겨찾기를 한 곳에 모은 Member 전용 영역.",
        "test_cases": [
            "각 목록이 0건일 때 완성형 Empty State(설명+다음 행동 CTA)가 보인다.",
            "즐겨찾기 항목 클릭 시 SCR-001 상세 Drawer로 이동한다.",
        ],
    },
    "COMP-SCR005-ADMIN-REPORTS": {
        "context": "Admin 전용 신고 큐. OPEN/REVIEWING/RESOLVED/DISMISSED 상태 필터와 처리(상태 변경+글 숨김).",
        "test_cases": [
            "Admin이 아니면 이 영역이 전혀 렌더링되지 않는다.",
            "상태 변경 시 대상 글이 즉시 숨김 처리된다.",
        ],
    },
    "COMP-SCR005-ADMIN-URL-SETTINGS": {
        "context": "Admin 전용 항공·숙소 외부 URL 설정 Form.",
        "test_cases": [
            "`http://` 또는 `javascript:`/`data:` URL은 저장이 거부된다.",
            "허용목록 밖 도메인은 저장이 거부된다.",
        ],
    },
    "COMP-GLOBAL-HEADER-FOOTER": {
        "context": "5개 Screen 공통 상단 Header와 하단 Footer.",
        "test_cases": [
            "5개 Screen 모두에서 동일한 Header/Footer 컴포넌트 인스턴스가 렌더링된다.",
            "현재 페이지에 해당하는 nav 항목이 활성 스타일로 표시된다.",
            "Mobile에서는 nav가 햄버거 메뉴로 축약된다.",
        ],
    },
    "COMP-GLOBAL-TOAST": {
        "context": "참가 요청 접수/승인/거절/신고 접수 등 상태 변경을 알리는 인앱 Toast.",
        "test_cases": [
            "상태 변경 후 즉시 Toast가 나타난다.",
            "이메일 발송 실패가 있어도 Toast/상태 표시는 정상 동작한다(이메일은 선택 사항).",
        ],
    },
    "COMP-GLOBAL-EMPTY-STATE": {
        "context": "여러 화면에서 재사용하는 완성형 Empty State 블록(아이콘+설명+이용 방법+CTA).",
        "test_cases": ["아이콘·설명·이용 방법·CTA 네 props가 모두 없으면 개발 중 경고를 낸다."],
    },
    "COMP-GLOBAL-DESIGN-TOKENS": {
        "context": "D-001 DESIGN.md의 색상/타이포/spacing/radius/shadow 토큰을 Tailwind 설정으로 반영한다.",
        "test_cases": [
            "코랄(#FF6F59) 외의 임의 색상이 컴포넌트에 하드코딩되어 있지 않다.",
            "이미지에는 `next/image`의 반응형+lazy 옵션이 적용된다.",
        ],
    },
    "COMP-GLOBAL-LOADING-STATE": {
        "context": "여러 화면에서 재사용하는 Loading State 블록(Skeleton 또는 Spinner+안내 문구). Supabase 조회·제출이 진행 중일 때 표시한다.",
        "test_cases": [
            "API-MATE-POSTS 등 비동기 조회가 진행 중인 동안 Skeleton/Spinner가 보이고 빈 화면이 없다.",
            "조회가 완료되면 LoadingState가 사라지고 실제 콘텐츠 또는 EmptyState/ErrorState로 교체된다.",
        ],
    },
    "COMP-GLOBAL-ERROR-STATE": {
        "context": "여러 화면에서 재사용하는 Error State 블록(오류 메시지+재시도 버튼). Supabase 조회·제출이 실패했을 때 표시한다.",
        "test_cases": [
            "네트워크/서버 오류로 조회 또는 제출이 실패하면 오류 메시지와 재시도 버튼이 보인다.",
            "재시도 버튼 클릭 시 동일 요청이 다시 시도된다.",
        ],
    },
    "COMP-TECH-ERROR-PAGES": {
        "context": "404/500 오류 화면.",
        "test_cases": [
            "존재하지 않는 경로 접속 시 404 화면과 홈 이동 버튼이 보인다.",
            "런타임 오류 발생 시 500 화면과 다시 시도 버튼이 보인다.",
        ],
    },
    "COMP-TECH-POLICY-PAGES": {
        "context": "이용약관/개인정보처리방침/동행 안전수칙/콘텐츠 면책 정적 페이지.",
        "test_cases": [
            "4개 정책 페이지가 모두 실제 문구로 채워져 있다(Lorem ipsum 없음).",
            "COMP-SCR003-MATE-WRITE-FORM의 동의 링크가 올바른 정책 페이지로 연결된다.",
        ],
    },
    "DATA-DESTINATIONS": {
        "context": "여행지 정적 데이터. 국내 10개 이상, 해외 15개국 30개 도시 이상.",
        "test_cases": [
            "국내 항목 수 ≥ 10, 해외 국가 수 ≥ 15이고 도시 수 ≥ 30인지 DATA-VALIDATION-SCRIPT로 확인한다.",
            "각 항목에 명소 5개 이상, 음식 3개 이상, 에티켓 3개 이상이 있다.",
        ],
    },
    "DATA-SAFETY": {
        "context": "국가 안전정보 정적 데이터. 8개 필수 카테고리와 출처·확인일.",
        "test_cases": [
            "게시된 모든 해외 국가에 안전정보 레코드가 1:1로 존재한다.",
            "각 레코드에 8개 카테고리, 출처 URL, 최종 확인일, 편집자가 모두 있다.",
        ],
    },
    "DATA-REPRESENTATIVE": {
        "context": "대표 소개 정적 데이터(지표, 소개문, Timeline, 방문국가, Gallery, 추천 여행지).",
        "test_cases": [
            "50+/30+ 지표, Timeline 6개 이상, 방문국가 30개, Gallery 8장 이상, 추천 여행지 4개가 모두 데이터에 존재한다.",
        ],
    },
    "DATA-VALIDATION-SCRIPT": {
        "context": "빌드 전 콘텐츠 수량·완전성을 검사하는 스크립트. DATA-DESTINATIONS/SAFETY/REPRESENTATIVE 3개 데이터 소스를 모두 검사한다.",
        "test_cases": [
            "기준 미달(예: 국내 9개) 데이터로 실행하면 스크립트가 실패(non-zero exit)한다.",
            "기준을 만족하는 데이터로 실행하면 성공한다.",
        ],
    },
    "DB-SCHEMA-BASE": {
        "context": "6개 테이블(profiles, mate_posts, mate_applications, user_blocks, reports, outbound_url_settings) 스키마 마이그레이션.",
        "test_cases": [
            "마이그레이션 적용 후 테이블이 정확히 6개다(추가 테이블 없음).",
            "`mate_posts`에 `safety_consent_at` 컬럼이 있다.",
        ],
    },
    "DB-RLS-BASE": {
        "context": "6개 테이블에 대한 Row Level Security 정책.",
        "test_cases": [
            "타인 계정으로 비공개 행을 조회하면 빈 결과 또는 403이 반환된다.",
            "Moderator/Admin은 신고·차단 관련 테이블을 열람할 수 있다.",
        ],
    },
    "DB-ACCESS": {
        "context": "타입 안전 Supabase 쿼리/서버 액션 헬퍼. 이메일·전화번호를 응답에서 제외한다. 항공·숙소 입력값(REQ-FUNC-017)은 이 모듈의 어떤 함수도 받지 않으며 DB에 저장하지 않는다 - 전송하지 않는다/저장하지 않는다.",
        "test_cases": [
            "동행글 목록 조회 응답에 이메일/전화번호 필드가 전혀 포함되지 않는다.",
            "항공/숙소 폼에서 호출되는 쿼리 함수가 없다(해당 폼은 이 모듈을 사용하지 않음).",
        ],
    },
    "DB-SEED-BASE": {
        "context": "로컬 개발/E2E 테스트용 시드 데이터(테스트 계정, 샘플 동행글 등).",
        "test_cases": [
            "시드 실행 후 TEST-RLS-BASIC과 E2E-MATE-AUTH가 필요로 하는 최소 데이터(회원 2명 이상, 동행글 1건 이상)가 존재한다.",
        ],
    },
    "API-MATE-POSTS": {
        "context": "동행 모집글 CRUD와 조회 시점 자동 마감 계산.",
        "test_cases": [
            "종료일이 지난 글을 조회하면 status가 CLOSED로 계산되어 반환된다.",
            "비인증 사용자의 작성 요청은 401/리다이렉트로 거부된다.",
        ],
    },
    "API-MATE-APPLICATIONS": {
        "context": "참가 요청 생성과 작성자의 승인/거절 처리.",
        "test_cases": [
            "동일 사용자가 같은 글에 중복 PENDING 요청을 만들면 거부된다.",
            "글 작성자가 아닌 사용자가 승인/거절을 시도하면 403이다.",
        ],
    },
    "API-BLOCKS-REPORTS": {
        "context": "신고·차단 생성과 Admin의 신고 상태 처리.",
        "test_cases": [
            "신고 생성은 3초 이내 응답하고 신고 ID를 반환한다.",
            "Admin이 아닌 사용자가 신고 상태를 변경하려 하면 거부된다.",
        ],
    },
    "API-AUTH-PROFILE": {
        "context": "이메일 인증·로그인·프로필·성인 확인 서버 로직.",
        "test_cases": [
            "성인 확인 시 생년월일 원본이 아니라 `is_adult=true`와 확인 시각만 저장된다.",
            "이메일 인증 전에는 동행 쓰기 권한이 없다.",
        ],
    },
    "API-ADMIN-SETTINGS": {
        "context": "항공·숙소 외부 URL 허용목록 저장.",
        "test_cases": [
            "HTTPS가 아닌 URL 저장을 시도하면 거부된다.",
            "허용목록에 없는 도메인은 거부된다.",
        ],
    },
    "UNIT-TRAVEL-DATES": {
        "context": "항공/숙소 날짜 검증 로직 유닛 테스트.",
        "test_cases": [
            "출발일=오늘-1일 → 실패.",
            "체크아웃=체크인 → 실패.",
            "정상 범위 날짜 → 성공.",
        ],
    },
    "UNIT-CONTACT-DETECTION": {
        "context": "전화번호/이메일/메신저 ID 정규식 탐지 유닛 테스트.",
        "test_cases": [
            "'010-1234-5678' 포함 텍스트 → 탐지됨.",
            "'abc@example.com' 포함 텍스트 → 탐지됨.",
            "연락처가 없는 일반 문장 → 탐지되지 않음(오탐 최소화 확인).",
        ],
    },
    "UNIT-MATE-STATE": {
        "context": "동행 모집글/참가 요청 상태 전이 유닛 테스트.",
        "test_cases": [
            "PENDING → ACCEPTED 전이는 작성자만 수행 가능.",
            "이미 ACCEPTED인 요청에 중복 신청 시 거부.",
            "종료일 경과 시 CLOSED로 계산.",
        ],
    },
    "TEST-RLS-BASIC": {
        "context": "6개 테이블에 대한 RLS 통합 테스트. 실제 Supabase(로컬 또는 테스트 프로젝트)에 대해 실행한다.",
        "test_cases": [
            "본인 데이터 조회 → 성공.",
            "타인 비공개 데이터 조회 → 빈 결과/403.",
            "Admin 계정의 신고 테이블 조회 → 성공.",
        ],
    },
    "E2E-PUBLIC-SMOKE": {
        "context": "여행지 탐색, 안전정보 열람, 대표소개 등 비로그인 공개 흐름 Smoke Test.",
        "test_cases": [
            "`/` 접속 → 국내/해외 Card 클릭 → 상세 Drawer 열림.",
            "안전정보 Card 클릭 → Drawer 열림 → 외교부 링크 새 탭.",
            "`/about` 접속 → 7개 Section 모두 렌더링 확인.",
        ],
    },
    "E2E-TRAVEL-TOOLS": {
        "context": "항공/숙소 조건 입력→요약→외부 이동 흐름 E2E. 입력값(REQ-FUNC-017, REQ-FUNC-025)은 어떤 단계에서도 서버로 전송하지 않는다/저장하지 않는다 - Network 탭에서 확인한다.",
        "test_cases": [
            "항공 탭에서 조건 입력→요약 확인→외부 이동 새 탭 오픈 확인.",
            "숙소 탭에서 동일 흐름 확인.",
            "잘못된 날짜 입력 시 진행이 막히는지 확인.",
        ],
    },
    "E2E-MATE-AUTH": {
        "context": "로그인부터 동행 작성/참가 요청까지 인증이 필요한 핵심 흐름 E2E.",
        "test_cases": [
            "회원가입 → 이메일 인증(테스트 모드) → 로그인.",
            "로그인 후 동행 모집글 작성 → 목록에 노출 확인.",
            "다른 계정으로 참가 요청 → 작성자 승인 확인.",
        ],
    },
    "MANUAL-RESPONSIVE-DENSITY": {
        "context": "Desktop 1440px/Mobile 390px에서 콘텐츠 밀도(빈 여백, Card 열 전환)를 사람이 스크린샷으로 확인한다.",
        "test_cases": [
            "SCR-001/SCR-003을 1440px와 390px 두 해상도로 캡처해 `TASKS/checks/responsive-density.md`에 기록.",
        ],
    },
    "MANUAL-ACCESSIBILITY-KEYBOARD": {
        "context": "키보드 전용 내비게이션과 스크린리더 수동 점검.",
        "test_cases": [
            "Tab 키만으로 5개 Screen의 핵심 흐름을 완료할 수 있는지 확인.",
            "모든 인터랙티브 요소에서 포커스 표시가 보이는지 확인.",
        ],
    },
    "MANUAL-PERFORMANCE-LIGHTHOUSE": {
        "context": "배포된 사이트에서 Lighthouse로 LCP/INP/CLS를 수동 측정한다.",
        "test_cases": [
            "`/`, `/travel-tools` 등 핵심 페이지에서 Lighthouse Performance 점수와 Core Web Vitals를 기록.",
        ],
    },
    "CI-QUALITY-GATE": {
        "context": "병합 전 TypeScript strict, ESLint, Playwright(Chromium)를 실행하는 CI 게이트.",
        "test_cases": [
            "타입 오류가 있는 PR은 CI가 실패한다.",
            "Playwright chromium 프로젝트 테스트가 실패하면 병합이 막힌다.",
        ],
    },
    "RELEASE-CHECK-VERCEL-SUPABASE": {
        "context": "Vercel 배포와 Supabase 환경변수/TLS/비용 확인 체크리스트.",
        "test_cases": [
            "배포 URL이 HTTPS인지 확인.",
            "비밀키가 클라이언트 번들에 노출되지 않았는지 빌드 산출물에서 확인.",
            "월 예상 비용이 목표(10만원 이하) 범위인지 확인.",
        ],
    },
}


# ---------------------------------------------------------------------------
# Universal + task-specific Forbidden items (rule 9: modification outside
# Expected Files is forbidden for every Task, stated explicitly in every file).
# ---------------------------------------------------------------------------

UNIVERSAL_FORBIDDEN = [
    "Expected Files 목록 밖의 파일을 생성·수정·삭제하는 것.",
    "Lorem ipsum, \"준비 중\", \"정보 확인 필요\" 등 placeholder 문구, 또는 내용 없는 빈 Card를 남기는 것.",
    "별점(★)·리뷰 점수 UI, 실시간 항공/숙소 가격, 광고 배너를 추가하는 것.",
    "Airbnb 상표 요소(Rausch 색상명, Cereal 폰트, \"Guest favorite\" 배지, 3-Product Nav 등)를 재현하는 것.",
    "자동 Merge Runner, EC2/AWS 인프라 Task로 이 Task의 범위를 확장하는 것.",
    "이 문서에 명시되지 않은 새 DB 테이블·새 Screen·새 Route를 추가하는 것.",
]


def forbidden_for(task):
    tid, category = task["task_id"], task["category"]
    items = list(UNIVERSAL_FORBIDDEN)
    if category == "Page Owner":
        items.append("Depends On에 없는 하위 Component를 이 Task 안에서 직접 새로 만드는 것(조립만 허용).")
    if tid in ("COMP-SCR003-FLIGHT-FORM", "COMP-SCR003-HOTEL-FORM"):
        items.append("입력값(국가/지역/날짜)을 서버 API, DB, URL 쿼리, analytics 이벤트로 전송하는 것.")
    if tid == "COMP-SCR003-SUMMARY-ACTION":
        items.append("외부 이동 URL에 목적지·날짜 등 사용자 입력값을 쿼리 파라미터로 포함하는 것.")
    if tid == "COMP-SCR003-MATE-WRITE-FORM":
        items.append("연락처(전화번호/이메일/메신저 ID) 탐지 로직 없이 제출을 허용하는 것.")
    if category == "Database":
        items.append("정의된 6개 테이블(profiles/mate_posts/mate_applications/user_blocks/reports/outbound_url_settings) 외의 테이블을 추가하거나, RLS를 비활성화한 채 테이블을 남기는 것.")
    if tid in ("COMP-SCR005-ADMIN-URL-SETTINGS", "API-ADMIN-SETTINGS"):
        items.append("http:, javascript:, data: 스킴이나 허용목록 밖 도메인의 저장을 허용하는 것.")
    if category in ("E2E Test",):
        items.append("`playwright.config.ts`에 chromium 이외의 브라우저 프로젝트(firefox/webkit)를 추가하는 것.")
    if category == "Data":
        items.append("정적 데이터를 DB 테이블로 옮기거나, DATA-VALIDATION-SCRIPT의 최소 수량 기준을 낮추는 것.")
    return items


def design_ref_for(task):
    screen, category = task["screen"], task["category"]
    lines = []
    ui_categories = ("Page Owner", "Component", "Technical Route")
    if category in ui_categories and screen not in ("-", "", "전역", "기술 Route"):
        for s in re.split(r',\s*', screen):
            s = s.strip()
            if re.match(r'^SCR-00[1-5]$', s):
                lines.append("`design-reference/UI_CONTRACT.md` - {} 절".format(s))
    if category in ui_categories:
        lines.append("`design-reference/D-001/DESIGN.md` - Color Token / Typography / Spacing / Radius / Shadow, Do / Do Not 목록")
        if category == "Page Owner":
            lines.append("`design-reference/SCREEN_ROUTE_CONTRACT.json` - 해당 Screen 객체(section_order/key_components/forbidden_features)")
    else:
        lines.append("`design-reference/D-001/DESIGN.md` - Do / Do Not 목록(금지 색상·금지 키워드 확인용). 이 Task는 화면을 직접 그리지 않는 비-UI Task다.")
    return lines


def split_files(cell):
    if not cell or cell in ("-", "없음"):
        return ["없음"]
    parts = re.split(r',\s*(?=`)', cell)
    return [p.strip() for p in parts if p.strip()]


def bullets(items):
    return "\n".join("- {}".format(i) for i in items)


def numbered(items):
    return "\n".join("{}. {}".format(i + 1, x) for i, x in enumerate(items))


def render_task(task, excluded_set):
    tid = task["task_id"]
    category = task["category"]
    group_key = group_key_for(tid, category)
    notes = TASK_NOTES.get(tid, {"context": task["title"], "test_cases": ["(Test Cases 미작성 - 보완 필요)"]})
    priority = PRIORITY.get(tid, "-")
    verify = verify_for(tid, category)

    if category == "Page Owner":
        ac = PAGE_OWNER_AC[tid]
        functional_md = bullets(ac["functional"])
        visual_md = bullets(ac["visual"])
        security_md = bullets(ac["security"])
    else:
        ac = GROUP_AC.get(group_key, {
            "functional": "TASKS/00_TASK_LIST.md의 해당 Category 공통 AC를 따른다.",
            "visual": "TASKS/00_TASK_LIST.md의 해당 Category 공통 AC를 따른다.",
            "security": "TASKS/00_TASK_LIST.md의 해당 Category 공통 AC를 따른다.",
        })
        functional_md = ac["functional"]
        visual_md = ac["visual"]
        security_md = ac["security"]

    req_refs = split_ids(task["req_ref"]) or ["없음(이 Task는 특정 Requirement에 직접 매핑되지 않음)"]
    depends = split_ids(task["depends_on"]) or ["없음"]
    files = split_files(task["expected_files"])
    design_refs = design_ref_for(task)
    forbidden = forbidden_for(task)

    if req_refs and req_refs[0] != "없음(이 Task는 특정 Requirement에 직접 매핑되지 않음)":
        scope_note = (
            "이 Task가 다루는 모든 Requirement({})는 `docs/PROJECT_SCOPE.md` 기준 "
            "**{}**로 분류되어 있으며 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에서 "
            "이 Task ID로 추적된다. EXCLUDED Requirement는 이 Task에 배정되지 않는다."
        ).format(", ".join(req_refs), task["impl_status"])
    else:
        scope_note = (
            "이 Task는 개별 Requirement가 아니라 공통 인프라/전역 계층에 속하며, "
            "`docs/PROJECT_SCOPE.md`상 프로젝트 범위 내 **{}** 구현 방식을 지원한다.".format(task["impl_status"])
        )

    overlap = set(req_refs) & excluded_set
    if overlap:
        scope_note += " (경고: {} 는 NON_IMPLEMENTATION 표에도 등장하므로 재확인 필요)".format(sorted(overlap))

    lines = []
    lines.append("# {} - {}".format(tid, task["title"]))
    lines.append("")
    lines.append("Category: {} | Implementation Status: {} | Priority: {}".format(category, task["impl_status"], priority))
    lines.append("")
    lines.append("## Context")
    lines.append("")
    lines.append(notes["context"])
    lines.append("")
    lines.append("## Project Scope")
    lines.append("")
    lines.append(scope_note)
    lines.append("")
    lines.append("## Requirement Ref")
    lines.append("")
    lines.append(", ".join(req_refs))
    lines.append("")
    lines.append("## Screen / Route / Page Entry")
    lines.append("")
    lines.append("Screen: {}  ".format(task["screen"] or "-"))
    lines.append("Route: {}  ".format(task["route"] or "-"))
    lines.append("Page Entry: {}".format(task["page_entry"] or "-"))
    lines.append("")
    lines.append("## Design Ref")
    lines.append("")
    lines.append(bullets(design_refs))
    lines.append("")
    lines.append("## Depends On")
    lines.append("")
    lines.append(bullets(depends))
    lines.append("")
    lines.append("## Expected Files")
    lines.append("")
    lines.append(bullets(files))
    lines.append("")
    lines.append("## Functional AC")
    lines.append("")
    lines.append(functional_md)
    lines.append("")
    lines.append("## Visual AC")
    lines.append("")
    lines.append(visual_md)
    lines.append("")
    lines.append("## Security/Privacy AC")
    lines.append("")
    lines.append(security_md)
    lines.append("")
    lines.append("## Test Cases")
    lines.append("")
    lines.append(numbered(notes["test_cases"]))
    lines.append("")
    lines.append("## Verify")
    lines.append("")
    lines.append(verify)
    lines.append("")
    lines.append("## Definition of Done")
    lines.append("")
    lines.append(bullets([
        "위 Functional AC / Visual AC / Security-Privacy AC 항목을 모두 만족한다.",
        "Verify에 명시된 Task/Check가 통과한다.",
        "Expected Files 목록에 있는 파일만 생성·수정했다(그 외 파일 변경 없음).",
        "Forbidden 목록에 해당하는 요소가 결과물에 없다.",
        "Requirement Ref가 있는 경우 `docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적 가능하다.",
    ]))
    lines.append("")
    lines.append("## Forbidden")
    lines.append("")
    lines.append(bullets(forbidden))
    lines.append("")
    return "\n".join(lines)


def main():
    text = common_read(TASK_LIST_PATH)
    if text is None:
        print("TASKS/00_TASK_LIST.md 를 찾을 수 없습니다: {}".format(TASK_LIST_PATH))
        return 1

    tasks = parse_task_list(text)
    excluded = parse_excluded(text)

    errors = validate(tasks, excluded)
    if errors:
        print("사전 검사 실패 - 아무 파일도 생성하지 않았습니다:")
        for e in errors:
            print("  - {}".format(e))
        return 1

    print("사전 검사 통과: Task {}개, NON_IMPLEMENTATION Requirement {}개".format(len(tasks), len(excluded)))

    missing_notes = [t["task_id"] for t in tasks if t["task_id"] not in TASK_NOTES]
    if missing_notes:
        print("경고: TASK_NOTES에 없는 Task ID (기본 Context로 대체됨): {}".format(missing_notes))

    excluded_set = set(excluded)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    created, skipped = [], []
    for t in tasks:
        out_path = OUT_DIR / "TASK-{}.md".format(t["task_id"])
        if out_path.exists():
            skipped.append(t["task_id"])
            continue
        content = render_task(t, excluded_set)
        out_path.write_text(content, encoding="utf-8")
        created.append(t["task_id"])

    print("")
    print("생성됨: {}개, 이미 존재하여 건너뜀: {}개".format(len(created), len(skipped)))

    task_ids = set(t["task_id"] for t in tasks)
    existing_files = set(
        p.stem[len("TASK-"):]
        for p in OUT_DIR.glob("TASK-*.md")
    )
    missing_files = sorted(task_ids - existing_files)
    extra_files = sorted(existing_files - task_ids)

    print("")
    print("1:1 대조: Task List 구현 ID {}개 vs TASK-*.md 파일 {}개".format(len(task_ids), len(existing_files)))
    if missing_files:
        print("  - 파일이 없는 Task ID: {}".format(missing_files))
    if extra_files:
        print("  - Task List에 없는 TASK-*.md 파일: {}".format(extra_files))
    if not missing_files and not extra_files:
        print("  - 1:1 일치 확인됨.")
        return 0
    return 1


def common_read(path):
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
