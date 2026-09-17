#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final audit for the Free Traveler task-generation pipeline.

Checks TASKS/00_TASK_LIST.md and TASKS/TASK-<ID>.md against 18 numbered
rules (see module-level CHECKS list) and writes two output artifacts:

    TASKS/TASK_MANIFEST.csv    - one row per implementation Task
    TASKS/TASK_AUDIT_REPORT.md - PASS/FAIL detail for every rule

Inputs:
    TASKS/00_TASK_LIST.md
    TASKS/TASK-*.md
    docs/PROJECT_SCOPE.md              (authoritative IMPLEMENT/EXCLUDED
                                         classification for all 114
                                         Requirements)
    design-reference/SCREEN_ROUTE_CONTRACT.json

Usage:
    python scripts/audit_tasks.py

Exit codes:
    0 = AUDIT_PASS
    1 = violations found
    2 = NOT_GENERATED (TASKS/00_TASK_LIST.md does not exist yet)
"""

import csv
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import _traveler_common as common
from build_task_details import (
    parse_task_list, parse_excluded, split_ids, split_files,
    PRIORITY, verify_for,
)

TASK_LIST_PATH = common.ROOT / "TASKS" / "00_TASK_LIST.md"
TASKS_DIR = common.ROOT / "TASKS"
MANIFEST_PATH = TASKS_DIR / "TASK_MANIFEST.csv"
REPORT_PATH = TASKS_DIR / "TASK_AUDIT_REPORT.md"

CANONICAL_TABLES = [
    "profiles", "mate_posts", "mate_applications",
    "user_blocks", "reports", "outbound_url_settings",
]
REQUIRED_DB_TASK_IDS = ["DB-SCHEMA-BASE", "DB-RLS-BASE", "DB-ACCESS", "DB-SEED-BASE"]

NON_TRANSMISSION_PHRASES = ["전송하지 않는다", "저장하지 않는다", "보내지 않는다", "전달하지 않는다", "비전송", "비전달"]
STATIC_DATA_REQ_PREFIXES = set(
    ["REQ-FUNC-{:03d}".format(n) for n in range(1, 11)]
    + ["REQ-FUNC-{:03d}".format(n) for n in range(46, 55)]
    + ["REQ-FUNC-{:03d}".format(n) for n in range(57, 64)]
)

MIN_E2E_TASKS, MAX_E2E_TASKS = 2, 3

# A line mentioning a banned keyword/browser only counts as a real violation
# when it is NOT paired with a negation marker on the same line - Task detail
# files legitimately name a forbidden/absent item while prohibiting it (e.g.
# a "## Forbidden" section, or "chromium 프로젝트만 정의한다(firefox/webkit 없음)").
NEGATION_MARKERS = ["금지", "없음", "제거", "거부", "않"]

INFRA_TITLE_MARKERS = ["EC2", "AWS", "자동 Merge", "자동 병합", "auto-merge"]


def strip_forbidden_section(text):
    return re.split(r'\n## Forbidden\n', text)[0]


def line_has_unnegated_hit(text, keyword):
    for line in text.splitlines():
        if keyword.lower() in line.lower() and not any(neg in line for neg in NEGATION_MARKERS):
            return True
    return False


def detail_path(task_id):
    return TASKS_DIR / "TASK-{}.md".format(task_id)


def read_detail(task_id):
    path = detail_path(task_id)
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def by_id(tasks):
    return {t["task_id"]: t for t in tasks}


BACKTICK_PATH_RE = re.compile(r'^`([^`]+)`')


def extract_path(cell):
    """Pulls the backtick-quoted path out of a cell that may carry a
    trailing parenthetical note, e.g. '`src/app/page.tsx`(신규 생성)' -> the
    naive str.strip("` ") mishandles this because the string doesn't end in
    a backtick, so it strips only the leading one and leaves a stray
    trailing backtick attached to the path."""
    m = BACKTICK_PATH_RE.match(cell.strip())
    return m.group(1) if m else cell.strip("` ")


SCREEN_ID_RE = re.compile(r'^SCR-00[1-5]$')


# ---------------------------------------------------------------------------
# The 18 checks. Each takes (ctx) and returns a list of violation strings
# (empty list = PASS). ctx is a dict built once in main().
# ---------------------------------------------------------------------------

def check_1_one_to_one(ctx):
    violations = []
    task_ids = [t["task_id"] for t in ctx["tasks"]]
    existing = ctx["existing_detail_ids"]
    for tid in task_ids:
        if tid not in existing:
            violations.append("Task {} 의 상세 파일이 없습니다: TASKS/TASK-{}.md".format(tid, tid))
    for d in sorted(existing - set(task_ids)):
        violations.append("Task List에 없는 상세 파일이 존재합니다(1:1 위반): TASKS/TASK-{}.md".format(d))
    return violations


def check_2_no_duplicate_ids(ctx):
    ids = [t["task_id"] for t in ctx["tasks"]]
    dupes = sorted(set(x for x in ids if ids.count(x) > 1))
    return ["중복 Task ID: {}".format(d) for d in dupes]


def check_3_depends_on_resolved(ctx):
    violations = []
    id_set = set(ctx["by_id"].keys())
    for t in ctx["tasks"]:
        for dep in split_ids(t["depends_on"]):
            dep_clean = dep.strip("` ")
            base = re.split(r'[\(（]', dep_clean)[0].strip()
            if "~" in base or "*" in base:
                continue
            if base and base not in id_set:
                violations.append("{} 의 Depends On '{}' 이 Task List에 없습니다".format(t["task_id"], base))
    return violations


def check_4_no_dependency_cycles(ctx):
    id_set = set(ctx["by_id"].keys())
    graph = {}
    for t in ctx["tasks"]:
        deps = []
        for dep in split_ids(t["depends_on"]):
            base = re.split(r'[\(（]', dep.strip("` "))[0].strip()
            if base in id_set:
                deps.append(base)
        graph[t["task_id"]] = deps

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {tid: WHITE for tid in graph}
    violations = []
    cycle_found = set()

    def dfs(node, stack):
        color[node] = GRAY
        stack.append(node)
        for nxt in graph.get(node, []):
            if color.get(nxt) == GRAY:
                idx = stack.index(nxt)
                cycle = stack[idx:] + [nxt]
                key = tuple(sorted(cycle))
                if key not in cycle_found:
                    cycle_found.add(key)
                    violations.append("Dependency Cycle 발견: {}".format(" -> ".join(cycle)))
            elif color.get(nxt) == WHITE:
                dfs(nxt, stack)
        stack.pop()
        color[node] = BLACK

    for tid in graph:
        if color[tid] == WHITE:
            dfs(tid, [])
    return violations


def check_5_page_owner_per_screen(ctx):
    violations = []
    screens = ctx["contract"].get("screens", [])
    owners = [t for t in ctx["tasks"] if t["category"] == "Page Owner"]
    owners_by_screen = {}
    for o in owners:
        owners_by_screen.setdefault(o["screen"].strip(), []).append(o["task_id"])
    for s in screens:
        sid = s.get("id")
        matches = owners_by_screen.get(sid, [])
        if len(matches) != 1:
            violations.append(
                "Screen {}의 Page Owner Task가 정확히 1개가 아니라 {}개입니다: {}".format(
                    sid, len(matches), matches
                )
            )
    extra_screens = set(owners_by_screen) - {s.get("id") for s in screens}
    for sid in sorted(extra_screens):
        violations.append("SCREEN_ROUTE_CONTRACT.json에 없는 Screen {}에 Page Owner Task가 있습니다".format(sid))
    return violations


def check_6_route_page_entry_files_match(ctx):
    violations = []
    screens_by_id = {s.get("id"): s for s in ctx["contract"].get("screens", [])}
    owners = [t for t in ctx["tasks"] if t["category"] == "Page Owner"]
    for o in owners:
        s = screens_by_id.get(o["screen"].strip())
        if s is None:
            continue
        owner_route = extract_path(o["route"])
        owner_entry = extract_path(o["page_entry"])
        if owner_route != s.get("route"):
            violations.append(
                "{}의 Route '{}' 가 SCREEN_ROUTE_CONTRACT.json의 '{}' 와 다릅니다".format(
                    o["task_id"], owner_route, s.get("route")
                )
            )
        if owner_entry != s.get("page_entry"):
            violations.append(
                "{}의 Page Entry '{}' 가 SCREEN_ROUTE_CONTRACT.json의 '{}' 와 다릅니다".format(
                    o["task_id"], owner_entry, s.get("page_entry")
                )
            )
        expected_files = [extract_path(f) for f in split_files(o["expected_files"])]
        if owner_entry not in expected_files:
            violations.append(
                "{}의 Expected Files에 자신의 Page Entry '{}' 가 없습니다".format(o["task_id"], owner_entry)
            )
    return violations


def check_7_no_orphan_components(ctx):
    violations = []
    owners = [t for t in ctx["tasks"] if t["category"] == "Page Owner"]
    owned = set()
    for o in owners:
        owned.update(split_ids(o["depends_on"]))
    # Only screen-scoped Components (screen == SCR-00N) are checked here.
    # COMP-GLOBAL-*/COMP-TECH-* Tasks (screen "전역"/"기술 Route") are
    # foundational/config-level work (e.g. Tailwind tokens applied at build
    # time) that Page Owners benefit from without listing as a direct
    # Depends On, so they are legitimately not "owned" by any single Screen.
    components = [
        t for t in ctx["tasks"]
        if t["category"] == "Component" and SCREEN_ID_RE.match(t["screen"].strip())
    ]
    orphans = [c["task_id"] for c in components if c["task_id"] not in owned]
    if orphans:
        violations.append(
            "어떤 Page Owner에도 조립되지 않은 Component Task가 있습니다(Component-only Screen): {}".format(orphans)
        )
    return violations


def check_8_scr001_starter_removed(ctx):
    owner = ctx["owners_by_route"].get("/")
    if owner is None:
        return ["route '/' 의 Page Owner Task를 찾을 수 없습니다"]
    text = read_detail(owner["task_id"]) or ""
    if "Starter" not in text and "스타터" not in text:
        return ["{} (route '/')의 상세 파일에 Starter 템플릿 제거 AC가 없습니다".format(owner["task_id"])]
    return []


def check_9_scr003_three_tabs(ctx):
    owner = ctx["owners_by_route"].get("/travel-tools")
    if owner is None:
        return ["route '/travel-tools' 의 Page Owner Task를 찾을 수 없습니다"]
    text = read_detail(owner["task_id"]) or ""
    missing = [kw for kw in ("항공", "숙소", "동행") if kw not in text]
    if missing:
        return [
            "{} (route '/travel-tools')의 상세 파일에 '{}' 탭 조립 관련 내용이 없습니다".format(
                owner["task_id"], ", ".join(missing)
            )
        ]
    return []


def check_10_scr005_role_states(ctx):
    owner = ctx["owners_by_route"].get("/account")
    if owner is None:
        return ["route '/account' 의 Page Owner Task를 찾을 수 없습니다"]
    text = read_detail(owner["task_id"]) or ""
    guest_ok = "Guest" in text or "게스트" in text
    member_ok = "Member" in text or "회원" in text
    admin_ok = "Admin" in text or "관리자" in text
    if not (guest_ok and member_ok and admin_ok):
        return ["{} (route '/account')의 상세 파일에 Guest/Member/Admin 조립 내용이 모두 있어야 합니다".format(owner["task_id"])]
    return []


def check_11_db_tasks_exist(ctx):
    present = {t["task_id"] for t in ctx["tasks"] if t["category"] == "Database"}
    missing = [tid for tid in REQUIRED_DB_TASK_IDS if tid not in present]
    return ["필수 DB Task가 없습니다: {}".format(tid) for tid in missing]


def check_12_db_table_scope(ctx):
    violations = []
    schema_task = ctx["by_id"].get("DB-SCHEMA-BASE")
    if schema_task is None:
        return ["DB-SCHEMA-BASE Task가 없어 Table 범위를 확인할 수 없습니다"]
    schema_text = schema_task["title"] + " " + (read_detail("DB-SCHEMA-BASE") or "")
    missing_canonical = [tb for tb in CANONICAL_TABLES if tb not in schema_text]
    if missing_canonical:
        violations.append("DB-SCHEMA-BASE에 기본 테이블이 모두 언급되지 않았습니다: {}".format(missing_canonical))

    table_mention_re = re.compile(r'`([a-z][a-z_]{2,})`\s*테이블|테이블[^.\n]{0,10}?`([a-z][a-z_]{2,})`')
    extra_tokens = set()
    for t in ctx["tasks"]:
        if t["category"] != "Database":
            continue
        body = read_detail(t["task_id"]) or ""
        for m in table_mention_re.finditer(body):
            tok = m.group(1) or m.group(2)
            if tok and tok not in CANONICAL_TABLES:
                extra_tokens.add(tok)
    if extra_tokens:
        violations.append("기본 6개 테이블 외에 언급된 테이블이 있습니다: {}".format(sorted(extra_tokens)))
    return violations


def check_13_external_input_non_persistence(ctx):
    violations = []
    targets = [
        t for t in ctx["tasks"]
        if "REQ-FUNC-017" in split_ids(t["req_ref"]) or "REQ-FUNC-025" in split_ids(t["req_ref"])
    ]
    for t in targets:
        text = read_detail(t["task_id"]) or ""
        if not any(p in text for p in NON_TRANSMISSION_PHRASES):
            violations.append("{}의 상세 파일에 입력값 미전송/미저장 AC가 없습니다".format(t["task_id"]))
    return violations


def check_14_auth_adult_rls_ac(ctx):
    violations = []
    auth_text = read_detail("API-AUTH-PROFILE") or ""
    if not auth_text:
        violations.append("API-AUTH-PROFILE 상세 파일이 없습니다")
    else:
        if not ("로그인" in auth_text or "인증" in auth_text):
            violations.append("API-AUTH-PROFILE 상세 파일에 로그인/인증 관련 AC가 없습니다")
        if "성인" not in auth_text:
            violations.append("API-AUTH-PROFILE 상세 파일에 성인 인증 AC가 없습니다")
    rls_text = read_detail("DB-RLS-BASE") or ""
    if not rls_text:
        violations.append("DB-RLS-BASE 상세 파일이 없습니다")
    elif "RLS" not in rls_text and "Row Level Security" not in rls_text:
        violations.append("DB-RLS-BASE 상세 파일에 RLS AC가 없습니다")
    return violations


def check_15_playwright_chromium_smoke(ctx):
    violations = []
    e2e_tasks = [t for t in ctx["tasks"] if t["category"] == "E2E Test"]
    if not (MIN_E2E_TASKS <= len(e2e_tasks) <= MAX_E2E_TASKS):
        violations.append(
            "E2E Test Task가 {}~{}개 범위가 아니라 {}개입니다".format(MIN_E2E_TASKS, MAX_E2E_TASKS, len(e2e_tasks))
        )
    for t in e2e_tasks:
        text = strip_forbidden_section(read_detail(t["task_id"]) or "")
        if line_has_unnegated_hit(text, "firefox") or line_has_unnegated_hit(text, "webkit"):
            violations.append(
                "{}의 상세 파일에 firefox/webkit이 (부재를 명시하지 않은 채) 언급되어 있습니다".format(t["task_id"])
            )
        if "chromium" not in text.lower():
            violations.append("{}의 상세 파일에 chromium 명시가 없습니다".format(t["task_id"]))
    return violations


def check_16_no_infra_automerge_tasks(ctx):
    violations = []
    for t in ctx["tasks"]:
        title_hit = [m for m in INFRA_TITLE_MARKERS if m in t["title"]]
        if title_hit:
            violations.append("{} 의 제목에 금지된 인프라/자동화 키워드가 있습니다: {}".format(t["task_id"], title_hit))
        text = strip_forbidden_section(read_detail(t["task_id"]) or "")
        for kw in INFRA_TITLE_MARKERS:
            if line_has_unnegated_hit(text, kw):
                violations.append("{}의 상세 파일에 '{}' 를 실제로 구현하는 것처럼 보이는 문구가 있습니다".format(t["task_id"], kw))
    return violations


def check_17_all_requirements_accounted_for(ctx):
    violations = []
    requirements = ctx["scope_requirements"]
    all_ids = set(requirements.keys())
    if len(all_ids) != common.EXPECTED_TOTAL_REQ_COUNT:
        violations.append(
            "docs/PROJECT_SCOPE.md의 Requirement 총개수가 {}개가 아니라 {}개입니다".format(
                common.EXPECTED_TOTAL_REQ_COUNT, len(all_ids)
            )
        )
    covered = set()
    for t in ctx["tasks"]:
        covered.update(split_ids(t["req_ref"]))
    excluded_ids = set(ctx["excluded_ids"])
    accounted_for = covered | excluded_ids
    missing = all_ids - accounted_for
    if missing:
        violations.append(
            "다음 Requirement가 어떤 Task에도, NON_IMPLEMENTATION 표에도 없습니다: {}".format(sorted(missing))
        )

    scope_excluded = {r for r, v in requirements.items() if common.is_excluded_status(v["status"])}
    mismatched_not_excluded = excluded_ids - scope_excluded
    if mismatched_not_excluded:
        violations.append(
            "NON_IMPLEMENTATION 표에 있지만 PROJECT_SCOPE.md 기준 EXCLUDED가 아닌 항목: {}".format(
                sorted(mismatched_not_excluded)
            )
        )
    mismatched_missing = scope_excluded - excluded_ids
    if mismatched_missing:
        violations.append(
            "PROJECT_SCOPE.md 기준 EXCLUDED인데 NON_IMPLEMENTATION 표에서 빠졌습니다: {}".format(
                sorted(mismatched_missing)
            )
        )
    return violations


def check_18_excluded_have_no_detail_files(ctx):
    violations = []
    excluded_ids = set(ctx["excluded_ids"])
    covered = set()
    for t in ctx["tasks"]:
        covered.update(split_ids(t["req_ref"]))
    illegally_covered = excluded_ids & covered
    if illegally_covered:
        violations.append(
            "EXCLUDED Requirement가 구현 Task에 배정되어 있습니다: {}".format(sorted(illegally_covered))
        )
    for req_id in sorted(excluded_ids):
        if detail_path(req_id).exists():
            violations.append("EXCLUDED Requirement {}에 대한 상세 구현 파일이 생성되어 있습니다".format(req_id))
    return violations


CHECKS = [
    (1, "Task List 구현 ID와 상세 Task 파일 1:1", check_1_one_to_one),
    (2, "중복 Task ID 0", check_2_no_duplicate_ids),
    (3, "Depends On 누락 0", check_3_depends_on_resolved),
    (4, "Dependency Cycle 0", check_4_no_dependency_cycles),
    (5, "Screen 5개 모두 Page Owner 정확히 1개", check_5_page_owner_per_screen),
    (6, "Route·Page Entry·Expected Files 일치", check_6_route_page_entry_files_match),
    (7, "Component-only Screen 0", check_7_no_orphan_components),
    (8, "SCR-001 Starter 제거 AC 존재", check_8_scr001_starter_removed),
    (9, "SCR-003 세 탭 조립 AC 존재", check_9_scr003_three_tabs),
    (10, "SCR-005 역할별 상태 조립 AC 존재", check_10_scr005_role_states),
    (11, "DB Schema·RLS·Access·Seed Task 존재", check_11_db_tasks_exist),
    (12, "DB Table 범위가 6개 기본 테이블을 크게 넘지 않음", check_12_db_table_scope),
    (13, "외부 입력 비저장 AC 존재", check_13_external_input_non_persistence),
    (14, "Auth·성인·기본 RLS AC 존재", check_14_auth_adult_rls_ac),
    (15, "Playwright Chromium Smoke Task 존재", check_15_playwright_chromium_smoke),
    (16, "AWS·EC2·자동 Merge 구현 Task 0", check_16_no_infra_automerge_tasks),
    (17, "REQ-FUNC 80개와 REQ-NF 34개가 Task 또는 EXCLUDED 표에 존재", check_17_all_requirements_accounted_for),
    (18, "EXCLUDED 상세 구현 파일이 생성되지 않음", check_18_excluded_have_no_detail_files),
]


def write_manifest_csv(ctx):
    fieldnames = [
        "Seq", "Task ID", "Title", "Category", "Implementation Status",
        "Requirement Ref", "Screen", "Route", "Page Entry", "Depends On",
        "Expected Files", "Priority", "Verify", "Detail File",
    ]
    with MANIFEST_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in ctx["tasks"]:
            tid = t["task_id"]
            has_detail = detail_path(tid).exists()
            writer.writerow({
                "Seq": t["seq"],
                "Task ID": tid,
                "Title": t["title"],
                "Category": t["category"],
                "Implementation Status": t["impl_status"],
                "Requirement Ref": t["req_ref"],
                "Screen": t["screen"],
                "Route": t["route"],
                "Page Entry": t["page_entry"],
                "Depends On": t["depends_on"],
                "Expected Files": t["expected_files"],
                "Priority": PRIORITY.get(tid, "-"),
                "Verify": verify_for(tid, t["category"]),
                "Detail File": "TASK-{}.md".format(tid) if has_detail else "(없음)",
            })


def write_audit_report(results, ctx):
    lines = []
    lines.append("# Free Traveler Task Audit Report")
    lines.append("")
    lines.append("Task 총 {}개, EXCLUDED Requirement {}개 (docs/PROJECT_SCOPE.md 기준)".format(
        len(ctx["tasks"]), len(ctx["excluded_ids"])
    ))
    lines.append("")
    lines.append("| # | 검사 | 결과 | 위반 |")
    lines.append("|---|---|---|---|")
    total_violations = 0
    for num, title, violations in results:
        total_violations += len(violations)
        status = "PASS" if not violations else "FAIL"
        detail = "위반 없음" if not violations else "{}건".format(len(violations))
        lines.append("| {} | {} | {} | {} |".format(num, title, status, detail))
    lines.append("")
    for num, title, violations in results:
        if not violations:
            continue
        lines.append("## {}. {} - FAIL".format(num, title))
        lines.append("")
        for v in violations:
            lines.append("- {}".format(v))
        lines.append("")

    overall = "AUDIT_PASS" if total_violations == 0 else "AUDIT_FAIL"
    lines.append("## 종합 결과")
    lines.append("")
    lines.append("- 총 검사 수: {}".format(len(results)))
    lines.append("- 통과: {}".format(sum(1 for _, _, v in results if not v)))
    lines.append("- 실패: {}".format(sum(1 for _, _, v in results if v)))
    lines.append("- 총 위반 건수: {}".format(total_violations))
    lines.append("- 결과: **{}**".format(overall))
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main():
    if not TASK_LIST_PATH.exists():
        print("=" * 72)
        print("Free Traveler Pipeline - Task Audit")
        print("=" * 72)
        print("  Task가 아직 생성되지 않았습니다 ({} 없음).".format(TASK_LIST_PATH.relative_to(common.ROOT)))
        print("  먼저 scripts/build_task_details.py 를 실행하세요.")
        print("")
        print("RESULT: NOT_GENERATED")
        return 2

    text = TASK_LIST_PATH.read_text(encoding="utf-8")
    tasks = parse_task_list(text)
    excluded_ids = parse_excluded(text)

    contract, contract_errors = common.load_screen_route_contract()
    scope_requirements, scope_errors = common.parse_project_scope_requirements()

    owners_by_route = {}
    for o in [t for t in tasks if t["category"] == "Page Owner"]:
        owners_by_route[o["route"].strip("` ")] = o

    ctx = {
        "tasks": tasks,
        "by_id": by_id(tasks),
        "excluded_ids": excluded_ids,
        "contract": contract or {"screens": []},
        "scope_requirements": scope_requirements,
        "owners_by_route": owners_by_route,
        "existing_detail_ids": {p.stem[len("TASK-"):] for p in TASKS_DIR.glob("TASK-*.md")},
    }

    results = []
    if contract_errors:
        results.append((0, "SCREEN_ROUTE_CONTRACT.json 로딩", list(contract_errors)))
    if scope_errors:
        results.append((0, "docs/PROJECT_SCOPE.md 로딩", list(scope_errors)))

    for num, title, fn in CHECKS:
        violations = fn(ctx)
        results.append((num, title, violations))

    write_manifest_csv(ctx)
    write_audit_report(results, ctx)

    print("=" * 72)
    print("Free Traveler Pipeline - Task Audit")
    print("=" * 72)
    total_violations = 0
    for num, title, violations in results:
        total_violations += len(violations)
        mark = "PASS" if not violations else "FAIL"
        print("  [{}] {}. {}".format(mark, num, title))
        for v in violations:
            print("        - {}".format(v))
    print("")
    print("출력: {}".format(MANIFEST_PATH.relative_to(common.ROOT).as_posix()))
    print("출력: {}".format(REPORT_PATH.relative_to(common.ROOT).as_posix()))
    print("")

    if total_violations:
        print("RESULT: AUDIT_FAIL ({}건 위반)".format(total_violations))
        return 1

    print("AUDIT_PASS")
    print("검사 수: {}".format(len(CHECKS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
