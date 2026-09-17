#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Checks that the 5 fixed Free Traveler Screens stay consistent across
design-reference/SCREEN_ROUTE_CONTRACT.json (design contract),
TASKS/TASK_MANIFEST.csv (Page Owner Task plan), and src/app (actual
Next.js App Router files) - at three different points in the pipeline.

Modes:
    plan    - checks the Page Owner plan only (contract + manifest).
              Does not require any src/app implementation to exist yet.
    ci      - plan's checks, plus the implemented Page files and the
              actually-reachable public routes under src/app.
    release - ci's checks, plus a human Preview Checkpoint record per
              Screen (docs/preview-checks/SCR-00N.md).

Usage:
    python scripts/check_screen_contract.py --mode=plan
    python scripts/check_screen_contract.py --mode=ci
    python scripts/check_screen_contract.py --mode=release

Exit codes:
    0 = all checks for the requested mode passed
    1 = one or more checks failed (each failure prints file/screen/hint)
"""

import argparse
import csv
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import _traveler_common as common

ROOT = common.ROOT
APP_DIR = ROOT / "src" / "app"
MANIFEST_PATH = ROOT / "TASKS" / "TASK_MANIFEST.csv"
CONTRACT_PATH = ROOT / "design-reference" / "SCREEN_ROUTE_CONTRACT.json"
PREVIEW_CHECKS_DIR = ROOT / "docs" / "preview-checks"

# 고정 화면 5개 - 이 스크립트가 검증하는 유일한 정답 집합.
FIXED_SCREENS = [
    {"id": "SCR-001", "route": "/", "page_entry": "src/app/page.tsx"},
    {"id": "SCR-002", "route": "/about", "page_entry": "src/app/about/page.tsx"},
    {"id": "SCR-003", "route": "/travel-tools", "page_entry": "src/app/travel-tools/page.tsx"},
    {"id": "SCR-004", "route": "/mates", "page_entry": "src/app/mates/page.tsx"},
    {"id": "SCR-005", "route": "/account", "page_entry": "src/app/account/page.tsx"},
]
FIXED_SCREEN_IDS = [s["id"] for s in FIXED_SCREENS]
ROUTE_BY_ID = {s["id"]: s["route"] for s in FIXED_SCREENS}
PAGE_ENTRY_BY_ID = {s["id"]: s["page_entry"] for s in FIXED_SCREENS}

# 허용 기술 경로 - 사용자 화면 5개로 세지 않는다.
ALLOWED_TECHNICAL_ROUTES = ["/auth/callback", "/api/**", "not-found"]

# 여행지 상세·안전정보는 SCR-001 안의 Drawer/Modal로 통합되었다(docs/06_SRS_UIUX_REVISED.md §3).
# 이 두 경로 아래에 별도 Page가 다시 생기면 그 통합 결정을 되돌리는 것이다.
FORBIDDEN_NEW_PAGE_PREFIXES = [
    ("destinations", "여행지 상세"),
    ("safety", "안전정보"),
]

# SCR-003는 여행 입력(항공/숙소)과 동행 작성 두 요구를 모두 포함해야 한다.
TRAVEL_INPUT_REQS = {"REQ-FUNC-{:03d}".format(n) for n in range(11, 27)}  # 011~026
MATE_WRITE_REQS = {"REQ-FUNC-027", "REQ-FUNC-028", "REQ-FUNC-031", "REQ-FUNC-032", "REQ-FUNC-080"}


class Errors:
    def __init__(self):
        self.items = []

    def add(self, file, screen_id, message, hint):
        self.items.append({"file": file, "screen": screen_id, "message": message, "hint": hint})

    def ok(self):
        return not self.items

    def print_all(self, mode):
        print("=" * 72)
        print("Free Traveler Screen Contract Check (mode={})".format(mode))
        print("=" * 72)
        if not self.items:
            print("")
            print("SCREEN_CONTRACT_PASS (mode={})".format(mode))
            return 0
        print("")
        print("FAIL - {}건의 오류:".format(len(self.items)))
        for e in self.items:
            print("  [FAIL] file={} | screen={} | {}".format(e["file"], e["screen"], e["message"]))
            print("         힌트: {}".format(e["hint"]))
        print("")
        print("SCREEN_CONTRACT_FAIL (mode={})".format(mode))
        return 1


# ---------------------------------------------------------------------------
# Shared loaders
# ---------------------------------------------------------------------------

def load_contract(errors):
    data, contract_errors = common.load_screen_route_contract()
    for e in contract_errors:
        errors.add(str(CONTRACT_PATH.relative_to(ROOT)), "-", e,
                    "design-reference/SCREEN_ROUTE_CONTRACT.json을 5개 Screen·고유 route/page_entry로 다시 맞춘다.")
    return data


def split_ids(cell):
    cell = (cell or "").strip()
    if cell in ("", "-", "없음"):
        return []
    return [x.strip() for x in cell.split(",") if x.strip() and x.strip() != "-"]


def load_manifest(errors):
    if not MANIFEST_PATH.exists():
        errors.add(
            str(MANIFEST_PATH.relative_to(ROOT)), "-",
            "TASK_MANIFEST.csv가 없습니다",
            "python scripts/audit_tasks.py를 먼저 실행해 TASK_MANIFEST.csv를 생성한다.",
        )
        return []
    with MANIFEST_PATH.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    required_cols = {"Task ID", "Category", "Screen", "Route", "Page Entry", "Requirement Ref"}
    missing = required_cols - set(rows[0].keys() if rows else [])
    if missing:
        errors.add(
            str(MANIFEST_PATH.relative_to(ROOT)), "-",
            "TASK_MANIFEST.csv에 필수 열이 없습니다: {}".format(sorted(missing)),
            "python scripts/audit_tasks.py를 다시 실행해 TASK_MANIFEST.csv를 최신 스키마로 재생성한다.",
        )
        return []
    return rows


def page_owner_rows_by_screen(rows):
    by_screen = {}
    for r in rows:
        if r.get("Category") != "Page Owner":
            continue
        for s in [x.strip() for x in (r.get("Screen") or "").split(",") if x.strip()]:
            by_screen.setdefault(s, []).append(r)
    return by_screen


def strip_backticks(cell):
    return (cell or "").strip().strip("`")


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_1_five_fixed_screens(contract, errors):
    """1. 고정 화면 5개가 정확히 존재한다."""
    if contract is None:
        return
    screens = contract.get("screens", [])
    ids = [s.get("id") for s in screens]
    if sorted(ids) != sorted(FIXED_SCREEN_IDS):
        errors.add(
            str(CONTRACT_PATH.relative_to(ROOT)), "-",
            "screens 배열의 Screen ID 집합이 고정 화면 5개({})와 다릅니다: {}".format(FIXED_SCREEN_IDS, ids),
            "SCREEN_ROUTE_CONTRACT.json의 screens를 SCR-001~005 5개로 맞춘다.",
        )
        return
    by_id = {s["id"]: s for s in screens}
    for sid in FIXED_SCREEN_IDS:
        s = by_id[sid]
        if s.get("route") != ROUTE_BY_ID[sid]:
            errors.add(
                str(CONTRACT_PATH.relative_to(ROOT)), sid,
                "route가 고정값 '{}'이 아니라 '{}'입니다".format(ROUTE_BY_ID[sid], s.get("route")),
                "{}의 route를 '{}'로 고정한다.".format(sid, ROUTE_BY_ID[sid]),
            )
        if s.get("page_entry") != PAGE_ENTRY_BY_ID[sid]:
            errors.add(
                str(CONTRACT_PATH.relative_to(ROOT)), sid,
                "page_entry가 고정값 '{}'이 아니라 '{}'입니다".format(PAGE_ENTRY_BY_ID[sid], s.get("page_entry")),
                "{}의 page_entry를 '{}'로 고정한다.".format(sid, PAGE_ENTRY_BY_ID[sid]),
            )


def check_2_one_page_owner_per_screen(rows, errors):
    """2. 각 화면 Page Owner Task가 정확히 하나다(+ Route/Page Entry가 계획과 일치)."""
    by_screen = page_owner_rows_by_screen(rows)
    for sid in FIXED_SCREEN_IDS:
        owners = by_screen.get(sid, [])
        if len(owners) != 1:
            errors.add(
                str(MANIFEST_PATH.relative_to(ROOT)), sid,
                "Page Owner Task가 정확히 1개가 아니라 {}개입니다: {}".format(
                    len(owners), [o.get("Task ID") for o in owners]
                ),
                "{}의 Page Owner Task를 정확히 1개(PAGE-{})로 유지한다.".format(sid, sid.replace("-", "")),
            )
            continue
        owner = owners[0]
        route = strip_backticks(owner.get("Route"))
        page_entry = strip_backticks(owner.get("Page Entry"))
        if route != ROUTE_BY_ID[sid]:
            errors.add(
                str(MANIFEST_PATH.relative_to(ROOT)), sid,
                "Page Owner {}의 Route가 '{}'이 아니라 '{}'입니다".format(owner.get("Task ID"), ROUTE_BY_ID[sid], route),
                "TASKS/00_TASK_LIST.md에서 {}의 Route 열을 '{}'로 고친다.".format(owner.get("Task ID"), ROUTE_BY_ID[sid]),
            )
        if page_entry != PAGE_ENTRY_BY_ID[sid]:
            errors.add(
                str(MANIFEST_PATH.relative_to(ROOT)), sid,
                "Page Owner {}의 Page Entry가 '{}'이 아니라 '{}'입니다".format(
                    owner.get("Task ID"), PAGE_ENTRY_BY_ID[sid], page_entry
                ),
                "TASKS/00_TASK_LIST.md에서 {}의 Page Entry 열을 '{}'로 고친다.".format(owner.get("Task ID"), PAGE_ENTRY_BY_ID[sid]),
            )


def route_from_page_file(page_path):
    rel_dir = page_path.relative_to(APP_DIR).parent
    if str(rel_dir) == ".":
        return "/"
    parts = [p for p in rel_dir.parts if not (p.startswith("(") and p.endswith(")"))]
    return "/" + "/".join(parts)


def is_allowed_technical(route):
    if route == "/auth/callback":
        return True
    if route == "/api" or route.startswith("/api/"):
        return True
    return False


def discover_pages():
    if not APP_DIR.exists():
        return []
    return sorted(APP_DIR.rglob("page.tsx"))


def check_3a_all_five_screens_implemented(errors):
    """3(ci 전제). mode=ci/release는 '구현된 Page 파일'을 검사하므로 5개 화면의
    Page Entry 파일이 실제로 존재하는지부터 확인한다."""
    for sid in FIXED_SCREEN_IDS:
        page_entry = PAGE_ENTRY_BY_ID[sid]
        if not (ROOT / page_entry).exists():
            errors.add(
                page_entry, sid,
                "고정 화면 {}의 Page Entry 파일이 아직 없습니다".format(sid),
                "PAGE-{} Task를 구현해 {}를 생성한다.".format(sid.replace("-", ""), page_entry),
            )


def check_3b_no_extra_screens_from_technical_routes(errors):
    """3. 기술 경로를 사용자 화면으로 세지 않는다(구현된 page.tsx만 화면으로 집계)."""
    expected_routes = set(ROUTE_BY_ID.values())
    for page_path in discover_pages():
        route = route_from_page_file(page_path)
        rel = page_path.relative_to(ROOT).as_posix()
        if route in expected_routes:
            continue
        if is_allowed_technical(route):
            # 허용된 기술 경로에 page.tsx가 놓여 있다 - route.ts여야 하므로 그 자체가 문제.
            errors.add(
                rel, "-",
                "기술 경로 '{}'에 Page(page.tsx)가 있습니다 - 기술 경로는 화면으로 집계하지 않지만 "
                "Route Handler(route.ts)여야 합니다".format(route),
                "{}를 route.ts로 옮기거나 삭제한다.".format(rel),
            )
            continue
        errors.add(
            rel, "-",
            "고정 화면 5개({})와 허용 기술 경로({}) 어디에도 속하지 않는 새 경로 '{}'가 있습니다".format(
                sorted(expected_routes), ALLOWED_TECHNICAL_ROUTES, route
            ),
            "이 Page가 승인된 화면이 아니면 삭제하고, 필요하면 먼저 docs/06_SRS_UIUX_REVISED.md·"
            "design-reference/SCREEN_ROUTE_CONTRACT.json을 갱신한다.",
        )


def check_4_no_destination_or_safety_pages(errors):
    """4. 여행지 상세·안전정보를 새 Page로 만들지 않았는지 검사한다."""
    for page_path in discover_pages():
        rel_dir = page_path.relative_to(APP_DIR).parent
        top = rel_dir.parts[0] if rel_dir.parts and str(rel_dir) != "." else None
        for prefix, label in FORBIDDEN_NEW_PAGE_PREFIXES:
            if top == prefix:
                rel = page_path.relative_to(ROOT).as_posix()
                errors.add(
                    rel, "SCR-001",
                    "{}는 SCR-001의 Drawer/Modal로 통합되었는데 별도 Page '{}'가 생성되었습니다".format(
                        label, "/" + "/".join(rel_dir.parts)
                    ),
                    "이 Page를 삭제하고 COMP-SCR001-DEST-DRAWER 또는 COMP-SCR001-SAFETY-PANEL의 "
                    "Drawer/Modal로 구현한다(docs/06_SRS_UIUX_REVISED.md §3).",
                )


def check_5_scr003_covers_travel_input_and_mate_write(rows, errors):
    """5. SCR-003 Task가 여행 입력과 동행 작성 양쪽 요구를 포함한다."""
    scr003_reqs = set()
    for r in rows:
        screens = [x.strip() for x in (r.get("Screen") or "").split(",") if x.strip()]
        if "SCR-003" not in screens:
            continue
        scr003_reqs.update(split_ids(r.get("Requirement Ref")))

    if not (scr003_reqs & TRAVEL_INPUT_REQS):
        errors.add(
            str(MANIFEST_PATH.relative_to(ROOT)), "SCR-003",
            "SCR-003 Task 중 여행 입력(항공·숙소, REQ-FUNC-011~026) 요구를 다루는 Task가 없습니다",
            "COMP-SCR003-FLIGHT-FORM/HOTEL-FORM처럼 REQ-FUNC-011~026을 Requirement Ref에 포함한 "
            "Task를 SCR-003에 유지한다.",
        )
    if not (scr003_reqs & MATE_WRITE_REQS):
        errors.add(
            str(MANIFEST_PATH.relative_to(ROOT)), "SCR-003",
            "SCR-003 Task 중 동행 작성(REQ-FUNC-027/028/031/032/080) 요구를 다루는 Task가 없습니다",
            "COMP-SCR003-MATE-LOGIN-GATE/MATE-WRITE-FORM처럼 해당 REQ를 Requirement Ref에 포함한 "
            "Task를 SCR-003에 유지한다.",
        )


def check_6_release_preview_checkpoints(errors):
    """6. release 모드에서는 docs/preview-checks/SCR-001.md ~ SCR-005.md를 확인한다."""
    for sid in FIXED_SCREEN_IDS:
        path = PREVIEW_CHECKS_DIR / "{}.md".format(sid)
        rel = path.relative_to(ROOT).as_posix()
        if not path.exists():
            errors.add(
                rel, sid,
                "release 모드에 필요한 사람 Preview Checkpoint 기록이 없습니다",
                "{} 배포본을 사람이 직접 확인한 뒤 {}를 작성한다(CLAUDE.md 규칙 22).".format(sid, rel),
            )
            continue
        if not path.read_text(encoding="utf-8").strip():
            errors.add(
                rel, sid,
                "Preview Checkpoint 파일이 비어 있습니다",
                "{}에 확인 결과(PASS/FAIL, 확인 시각, 확인자)를 기록한다.".format(rel),
            )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode", choices=["plan", "ci", "release"], default="ci",
        help="plan|ci|release (기본값 ci - npm run screen:contract가 --mode 없이 호출하므로).",
    )
    args = parser.parse_args()

    errors = Errors()

    contract = load_contract(errors)
    rows = load_manifest(errors)

    # mode=plan 이상: Page Owner·경로 계획 검사.
    check_1_five_fixed_screens(contract, errors)
    check_2_one_page_owner_per_screen(rows, errors)
    check_5_scr003_covers_travel_input_and_mate_write(rows, errors)

    # mode=ci 이상: 구현된 Page 파일과 공개 경로 검사.
    if args.mode in ("ci", "release"):
        check_3a_all_five_screens_implemented(errors)
        check_3b_no_extra_screens_from_technical_routes(errors)
        check_4_no_destination_or_safety_pages(errors)

    # mode=release: CI 검사 + Preview Checkpoint 존재 확인.
    if args.mode == "release":
        check_6_release_preview_checkpoints(errors)

    return errors.print_all(args.mode)


if __name__ == "__main__":
    sys.exit(main())
