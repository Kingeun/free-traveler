#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds an execution-Wave plan from TASKS/TASK_MANIFEST.csv.

Reads:
    TASKS/TASK_MANIFEST.csv                  (task_id/category/screen/depends_on/expected_files/...)
    TASKS/TASK-<ID>.md                       (cross-checked against the manifest's Depends On / Expected Files)
    design-reference/SCREEN_ROUTE_CONTRACT.json (schema/screen sanity check)

Writes:
    TASKS/TASK_DAG.md          (dependency graph reference: deps/dependents/Wave per Task)
    TASKS/WAVE_PLAN.md         (the Wave breakdown other Commands treat as authoritative)
    TASKS/WAVE_STATE.json      (per-Wave execution state, all "pending" at generation time)
    TASKS/TASK_MANIFEST.csv    (rewritten in place with a trailing wave_id column)

Design note - why a Wave never spans two dependency layers:
    Rule 6 says execution *inside* a Wave still runs one Task at a time in
    plain Task ID lexical order (not Depends-On order). Task IDs are not
    guaranteed to sort in dependency-safe order (e.g. "DB-ACCESS" sorts
    before "DB-RLS-BASE" although it depends on it). The only way to make
    "Task ID 순으로 한 개씩 실행" always safe is to guarantee no Task ever
    shares a Wave with one of its own dependencies. So Wave boundaries here
    follow strict topological *layers* (longest-path depth): a layer is
    split into more than one Wave when it exceeds MAX_WAVE_SIZE, but two
    different layers are never merged into one Wave even when that would
    make a small Wave closer to the "4~7" default - correctness of rule 2
    takes precedence over the sizing default, which the rules themselves
    only call a default ("기본적으로").

Usage:
    python scripts/build_waves.py

Exit 0 = all outputs written. Exit 1 = validation failed, nothing written.
"""

import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import _traveler_common as common

ROOT = common.ROOT
TASKS_DIR = ROOT / "TASKS"
MANIFEST_PATH = TASKS_DIR / "TASK_MANIFEST.csv"
DAG_PATH = TASKS_DIR / "TASK_DAG.md"
WAVE_PLAN_PATH = TASKS_DIR / "WAVE_PLAN.md"
WAVE_STATE_PATH = TASKS_DIR / "WAVE_STATE.json"

WAVE_SCHEMA = "traveler-wave-state-v1"
MIN_WAVE_SIZE = 4
MAX_WAVE_SIZE = 7

GROUP_ORDER = [
    (1, "Scaffold, 문서, Harness 확인"),
    (2, "Airbnb 스타일 공통 UI, 정적 데이터, Layout"),
    (3, "Supabase Auth, 6개 Table, 기본 RLS"),
    (4, "SCR-001 메인 Component와 Page Owner"),
    (5, "SCR-002 대표 소개 Component와 Page Owner"),
    (6, "SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner"),
    (7, "SCR-004 동행 목록·상세·신청 Component와 Page Owner"),
    (8, "SCR-005 계정·내 활동·간단 관리자 Component와 Page Owner"),
    (9, "Unit·Playwright·접근성·CI"),
    (10, "Vercel Preview와 Release 확인"),
]
GROUP_TITLE = dict(GROUP_ORDER)
SCREEN_TO_GROUP = {"SCR-001": 4, "SCR-002": 5, "SCR-003": 6, "SCR-004": 7, "SCR-005": 8}
TEST_CATEGORIES = {"Unit Test", "Integration Test", "E2E Test", "Manual Check"}


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def read_manifest(errors):
    if not MANIFEST_PATH.exists():
        errors.append("TASKS/TASK_MANIFEST.csv 가 없습니다. 먼저 scripts/audit_tasks.py를 실행하세요.")
        return None, None
    with MANIFEST_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    if "wave_id" in (fieldnames or []):
        errors.append(
            "TASK_MANIFEST.csv에 이미 wave_id 열이 있습니다. 재생성 전 기존 열을 제거하거나 이 스크립트가 "
            "다시 쓰도록 그대로 두십시오(이 실행은 wave_id 값을 새로 계산해 덮어씁니다)."
        )
    return rows, [c for c in (fieldnames or []) if c != "wave_id"]


def split_ids(cell):
    if cell is None:
        return []
    cell = cell.strip()
    if cell in ("", "-", "없음"):
        return []
    return [x.strip() for x in cell.split(",") if x.strip() and x.strip() != "-"]


def extract_paths(cell):
    if not cell:
        return []
    return re.findall(r'`([^`]+)`', cell)


def expand_dep_token(token, all_ids, errors, owner_id):
    """Resolves one Depends On token to zero or more concrete Task IDs.

    Handles a plain ID, a trailing parenthetical note ("ID(설명)"), a
    prefix wildcard ("UNIT-*", "E2E-*"), and a zero-padded numeric range
    ("PAGE-SCR001~005").
    """
    token = token.strip().strip("`")
    if not token or token in ("-", "없음"):
        return []
    base = re.split(r'[\(（]', token)[0].strip()
    if base.endswith("*"):
        prefix = base[:-1]
        matches = sorted(i for i in all_ids if i.startswith(prefix))
        if not matches:
            errors.append("{}: 와일드카드 '{}' 에 해당하는 Task ID가 없습니다".format(owner_id, token))
        return matches
    m = re.match(r'^(.*?)(\d+)~(\d+)$', base)
    if m:
        prefix, start, end = m.group(1), m.group(2), m.group(3)
        width = len(start)
        lo, hi = int(start), int(end)
        ids = ["{}{:0{}d}".format(prefix, n, width) for n in range(lo, hi + 1)]
        missing = [i for i in ids if i not in all_ids]
        if missing:
            errors.append("{}: 범위 표기 '{}' 가 만든 ID 중 없는 것: {}".format(owner_id, token, missing))
        return [i for i in ids if i in all_ids]
    if base not in all_ids:
        errors.append("{}: Depends On '{}' 이 Task Manifest에 없습니다".format(owner_id, token))
        return []
    return [base]


def cross_check_detail_files(rows, errors):
    for row in rows:
        tid = row["Task ID"]
        path = TASKS_DIR / "TASK-{}.md".format(tid)
        if not path.exists():
            errors.append("{}: 상세 파일이 없습니다 ({})".format(tid, path.name))
            continue
        text = path.read_text(encoding="utf-8")
        sections = re.split(r'\n## ', text)
        body = {}
        for sec in sections[1:]:
            head, _, rest = sec.partition("\n")
            body[head.strip()] = rest.strip()

        detail_depends = set(
            re.split(r'[\(（]', line[2:].strip())[0].strip()
            for line in body.get("Depends On", "").splitlines() if line.startswith("- ")
        )
        detail_depends.discard("없음")
        manifest_bases = set(
            re.split(r'[\(（]', tok)[0].strip() for tok in split_ids(row["Depends On"])
        )
        if detail_depends != manifest_bases:
            errors.append(
                "{}: TASK-{}.md의 Depends On({})이 TASK_MANIFEST.csv({})과 다릅니다".format(
                    tid, tid, sorted(detail_depends), sorted(manifest_bases)
                )
            )

        detail_files = set(re.findall(r'`([^`]+)`', body.get("Expected Files", "")))
        manifest_files = set(extract_paths(row["Expected Files"]))
        if detail_files != manifest_files:
            errors.append(
                "{}: TASK-{}.md의 Expected Files({})가 TASK_MANIFEST.csv({})와 다릅니다".format(
                    tid, tid, sorted(detail_files), sorted(manifest_files)
                )
            )


# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------

def build_edges(rows, errors):
    all_ids = set(r["Task ID"] for r in rows)
    edges = {}
    for r in rows:
        tid = r["Task ID"]
        deps = set()
        for tok in split_ids(r["Depends On"]):
            deps.update(expand_dep_token(tok, all_ids, errors, tid))
        deps.discard(tid)
        edges[tid] = deps
    return edges


def detect_cycles(nodes, edges):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in nodes}
    cycles = []
    stack = []

    def visit(n):
        color[n] = GRAY
        stack.append(n)
        for dep in sorted(edges.get(n, ())):
            if dep not in color:
                continue
            if color[dep] == GRAY:
                i = stack.index(dep)
                cycles.append(stack[i:] + [dep])
            elif color[dep] == WHITE:
                visit(dep)
        stack.pop()
        color[n] = BLACK

    for n in sorted(nodes):
        if color[n] == WHITE:
            visit(n)
    return cycles


def group_for(task_id, category, screen, errors):
    if category == "Data":
        return 2
    if category == "Technical Route":
        return 2
    if task_id.startswith("COMP-GLOBAL"):
        return 2
    if category == "Database":
        return 3
    if category == "API":
        return 3
    if category in ("Page Owner", "Component"):
        screens = [s.strip() for s in screen.split(",")] if screen else []
        mapped = {SCREEN_TO_GROUP[s] for s in screens if s in SCREEN_TO_GROUP}
        if len(mapped) == 1:
            return next(iter(mapped))
        errors.append("{}: Screen '{}' 로 Wave 그룹을 하나로 정할 수 없습니다".format(task_id, screen))
        return None
    if category in TEST_CATEGORIES:
        return 9
    if task_id == "CI-QUALITY-GATE":
        return 9
    if task_id == "RELEASE-CHECK-VERCEL-SUPABASE":
        return 10
    errors.append("{}: 어떤 Wave 그룹에도 매칭되지 않는 Category '{}' 입니다".format(task_id, category))
    return None


def compute_group_layers(group_task_ids, edges):
    """Longest-path layering using only edges internal to this group."""
    in_group = set(group_task_ids)
    memo = {}

    def depth(tid):
        if tid in memo:
            return memo[tid]
        deps = [d for d in edges.get(tid, ()) if d in in_group]
        d = 0 if not deps else 1 + max(depth(x) for x in deps)
        memo[tid] = d
        return d

    layers = {}
    for tid in group_task_ids:
        layers.setdefault(depth(tid), []).append(tid)
    return [sorted(layers[k]) for k in sorted(layers)]


def chunk_layer(layer_ids):
    """Splits an oversized layer into balanced chunks of at most MAX_WAVE_SIZE.

    Tasks within one layer have no dependency on each other, so any split
    or ordering between the resulting chunks is dependency-safe.
    """
    n = len(layer_ids)
    if n <= MAX_WAVE_SIZE:
        return [layer_ids]
    num_chunks = -(-n // MAX_WAVE_SIZE)  # ceil
    base, rem = divmod(n, num_chunks)
    chunks, i = [], 0
    for c in range(num_chunks):
        size = base + (1 if c < rem else 0)
        chunks.append(layer_ids[i:i + size])
        i += size
    return chunks


def split_file_conflicts(waves, files_by_id, notes):
    """Rule 5: Tasks in the same Wave must not touch overlapping Expected
    Files. Single pass - conflicting Tasks (beyond the first, by Task ID
    order) are pushed into one freshly inserted Wave right after."""
    result = []
    for wave in waves:
        if len(wave) <= 1:
            result.append(wave)
            continue
        seen = {}
        keep, moved = [], []
        for tid in wave:
            fs = files_by_id.get(tid, set())
            if any(f in seen for f in fs):
                moved.append(tid)
            else:
                keep.append(tid)
                for f in fs:
                    seen[f] = tid
        result.append(keep)
        if moved:
            notes.append("파일 충돌로 분리됨 → 새 Wave: {}".format(moved))
            result.append(moved)
    return result


def build_group_waves(group_num, members, tasks_by_id, edges, files_by_id, notes):
    if not members:
        return []
    owners = [t for t in members if tasks_by_id[t]["Category"] == "Page Owner"]
    others = [t for t in members if t not in owners]
    waves = []
    if others:
        for layer in compute_group_layers(others, edges):
            waves.extend(chunk_layer(layer))
        waves = split_file_conflicts(waves, files_by_id, notes)
    for o in sorted(owners):
        waves.append([o])  # rule 4: Page Owner alone, as the group's final Wave
    return waves


# ---------------------------------------------------------------------------
# Output rendering
# ---------------------------------------------------------------------------

def render_dag(rows_by_id, edges, wave_of, cycles):
    dependents = {tid: set() for tid in rows_by_id}
    for tid, deps in edges.items():
        for d in deps:
            dependents.setdefault(d, set()).add(tid)

    lines = [
        "# TASK_DAG — Free Traveler Task 의존성 그래프",
        "",
        "`scripts/build_waves.py`가 `TASKS/TASK_MANIFEST.csv`에서 생성했다. 이 문서는 참고용 그래프",
        "스냅샷이며, Wave 배치의 정본은 `TASKS/WAVE_PLAN.md`다.",
        "",
        "## 순환 의존성 검사",
        "",
    ]
    if cycles:
        lines.append("**FAIL** — {}개의 순환 의존성이 발견되었다:".format(len(cycles)))
        for c in cycles:
            lines.append("- " + " → ".join(c))
    else:
        lines.append("**PASS** — 순환 의존성 0개.")
    lines += [
        "",
        "## Task별 의존 관계",
        "",
        "| Task ID | Category | Wave | Depends On | Depended On By |",
        "|---|---|---|---|---|",
    ]
    for tid in sorted(rows_by_id):
        row = rows_by_id[tid]
        deps = ", ".join(sorted(edges.get(tid, ()))) or "없음"
        deped = ", ".join(sorted(dependents.get(tid, ()))) or "없음"
        lines.append("| {} | {} | {} | {} | {} |".format(
            tid, row["Category"], wave_of.get(tid, "-"), deps, deped
        ))
    lines.append("")
    return "\n".join(lines)


def render_wave_plan(wave_list, tasks_by_id, notes):
    lines = [
        "# WAVE_PLAN — Free Traveler 실행 Wave 계획",
        "",
        "`scripts/build_waves.py`가 `TASKS/TASK_MANIFEST.csv`의 Depends On을 바탕으로 생성했다.",
        "여기 적힌 Wave ID가 `/run-wave`·`TASKS/WAVE_STATE.json`이 사용하는 정본이다 — W00~W10으로",
        "미리 고정하지 않고, 실제 Task 수·의존관계·파일 충돌에 따라 그룹당 1개 이상의 Wave로 나뉜다.",
        "",
        "## Wave 배치 규칙 요약",
        "",
        "1. 순환 의존성은 0이어야 하며, 있으면 이 문서 자체가 생성되지 않는다.",
        "2. 선행 Task는 항상 그 Task보다 앞선 Wave에만 배치된다(같은 Wave에도 배치하지 않는다 — "
        "rule 6이 한 Wave 안에서도 Task ID 순으로 하나씩 실행하도록 정했기 때문에, 의존 관계가 있는 "
        "두 Task를 같은 Wave에 두면 Task ID 정렬이 우연히 의존 순서와 어긋날 때 실행 순서가 깨질 수 있다).",
        "3. Wave당 기본 4~7개를 목표로 하되, 실제 의존 사슬이 그보다 좁으면(예: DB Schema→RLS→Access처럼 "
        "한 단계씩 순차 의존) 규칙 2를 지키기 위해 더 작은 Wave가 된다 — 이는 결함이 아니라 의존 구조를 "
        "정직하게 반영한 결과다.",
        "4. Page Owner는 해당 Screen 그룹의 마지막 Wave에 단독으로 배치되고, 사람 Preview Checkpoint가 걸린다.",
        "5. 같은 Wave 안에서 Expected Files가 겹치는 Task가 있으면 자동으로 다음 Wave로 분리한다.",
        "6. 한 Wave 안에서도 Task ID 순으로 한 Task씩 실행한다.",
        "7. 자동 Branch·PR·Merge 기능은 포함하지 않는다(생성 스크립트도, 이 계획서도 그런 기능을 정의하지 않는다).",
        "",
        "## Wave 그룹 순서(10개)",
        "",
        "| 그룹 | 제목 | 매칭된 Task 수 |",
        "|---|---|---|",
    ]
    group_counts = {}
    for w in wave_list:
        group_counts[w["group"]] = group_counts.get(w["group"], 0) + len(w["task_ids"])
    for gnum, gtitle in GROUP_ORDER:
        count = group_counts.get(gnum, 0)
        note = "" if count else " (현재 Task List에 매칭되는 Task 없음 — Task 목록 밖의 사전 점검 단계)"
        lines.append("| {} | {} | {}{} |".format(gnum, gtitle, count, note))

    lines += ["", "## Wave 목록", "", "| Wave ID | 그룹 | Task 수 | Checkpoint 필요 | Task ID 목록 |", "|---|---|---|---|---|"]
    for w in wave_list:
        lines.append("| {} | {}. {} | {} | {} | {} |".format(
            w["wave_id"], w["group"], GROUP_TITLE[w["group"]], len(w["task_ids"]),
            "예" if w["checkpoint_required"] else "아니오",
            ", ".join(w["task_ids"]),
        ))

    if notes:
        lines += ["", "## 파일 충돌 분리 기록", ""]
        for n in notes:
            lines.append("- " + n)

    lines += ["", "## Checkpoint 안내", "",
              "`checkpoint_required=예`인 Wave는 CLAUDE.md 규칙 22에 따라 사람이 Preview를 확인해야 "
              "다음 Wave로 진행한다(`/run-wave`가 해당 Wave 완료 후 `WAITING_FOR_PREVIEW`로 멈춘다). "
              "SCR-001~005 Page Owner Wave 5개와 최종 `RELEASE-CHECK-VERCEL-SUPABASE` Wave가 여기 해당한다.", ""]
    return "\n".join(lines)


def render_wave_state(wave_list, generated_at):
    return json.dumps({
        "schema_version": WAVE_SCHEMA,
        "generated_at": generated_at,
        "waves": [
            {
                "wave_id": w["wave_id"],
                "title": "{}. {}".format(w["group"], GROUP_TITLE[w["group"]]),
                "task_ids": w["task_ids"],
                "status": "pending",
                "checkpoint_required": w["checkpoint_required"],
                "checkpoint_result": None,
            }
            for w in wave_list
        ],
    }, ensure_ascii=False, indent=2) + "\n"


def rewrite_manifest(rows, fieldnames, wave_of):
    out_fieldnames = fieldnames + ["wave_id"]
    with MANIFEST_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames)
        writer.writeheader()
        for r in rows:
            row = {k: r[k] for k in fieldnames}
            row["wave_id"] = wave_of.get(r["Task ID"], "")
            writer.writerow(row)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    errors = []

    contract, contract_errors = common.load_screen_route_contract()
    errors.extend(contract_errors)

    rows, fieldnames = read_manifest(errors)
    if rows is None:
        for e in errors:
            print("  - " + e)
        return 1

    required_cols = {"Task ID", "Category", "Screen", "Depends On", "Expected Files"}
    missing_cols = required_cols - set(fieldnames or [])
    if missing_cols:
        errors.append("TASK_MANIFEST.csv에 필수 열이 없습니다: {}".format(sorted(missing_cols)))
        for e in errors:
            print("  - " + e)
        return 1

    cross_check_detail_files(rows, errors)

    seen = set()
    for r in rows:
        if r["Task ID"] in seen:
            errors.append("중복 Task ID: {}".format(r["Task ID"]))
        seen.add(r["Task ID"])
    tasks_by_id = {r["Task ID"]: r for r in rows}
    all_ids = set(tasks_by_id)

    edges = build_edges(rows, errors)
    files_by_id = {tid: set(extract_paths(tasks_by_id[tid]["Expected Files"])) for tid in tasks_by_id}

    cycles = detect_cycles(all_ids, edges)
    if cycles:
        errors.append("순환 의존성 {}개 발견 — Wave를 배치할 수 없습니다.".format(len(cycles)))
        for c in cycles:
            errors.append("  순환: " + " → ".join(c))

    if errors:
        print("사전 검사 실패 - 아무 파일도 생성하지 않았습니다:")
        for e in errors:
            print("  - {}".format(e))
        return 1

    group_of = {}
    for tid, row in tasks_by_id.items():
        g = group_for(tid, row["Category"], row["Screen"], errors)
        group_of[tid] = g
    if errors:
        print("사전 검사 실패 - 아무 파일도 생성하지 않았습니다:")
        for e in errors:
            print("  - {}".format(e))
        return 1

    notes = []
    wave_list = []
    seq = 0
    for gnum, _ in GROUP_ORDER:
        members = sorted(tid for tid in all_ids if group_of[tid] == gnum)
        group_waves = build_group_waves(gnum, members, tasks_by_id, edges, files_by_id, notes)
        for task_ids in group_waves:
            seq += 1
            wave_id = "W{:02d}".format(seq)
            is_owner_wave = len(task_ids) == 1 and tasks_by_id[task_ids[0]]["Category"] == "Page Owner"
            is_release_wave = "RELEASE-CHECK-VERCEL-SUPABASE" in task_ids
            wave_list.append({
                "wave_id": wave_id,
                "group": gnum,
                "task_ids": task_ids,
                "checkpoint_required": bool(is_owner_wave or is_release_wave),
            })

    wave_of = {tid: w["wave_id"] for w in wave_list for tid in w["task_ids"]}

    # Global rule-2 sanity check: every dependency must land in a strictly
    # earlier Wave than its dependent, regardless of group.
    wave_index = {w["wave_id"]: i for i, w in enumerate(wave_list)}
    for tid, deps in edges.items():
        for d in deps:
            if wave_index[wave_of[d]] >= wave_index[wave_of[tid]]:
                errors.append(
                    "규칙 2 위반: {} (Wave {})가 선행 Task {} (Wave {})보다 앞서거나 같은 Wave에 배치됨".format(
                        tid, wave_of[tid], d, wave_of[d]
                    )
                )
    if errors:
        print("Wave 배치 후 검증 실패 - 아무 파일도 생성하지 않았습니다:")
        for e in errors:
            print("  - {}".format(e))
        return 1

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    DAG_PATH.write_text(render_dag(tasks_by_id, edges, wave_of, cycles), encoding="utf-8")
    WAVE_PLAN_PATH.write_text(render_wave_plan(wave_list, tasks_by_id, notes), encoding="utf-8")
    WAVE_STATE_PATH.write_text(render_wave_state(wave_list, generated_at), encoding="utf-8")
    rewrite_manifest(rows, fieldnames, wave_of)

    print("출력: {}".format(DAG_PATH.relative_to(ROOT)))
    print("출력: {}".format(WAVE_PLAN_PATH.relative_to(ROOT)))
    print("출력: {}".format(WAVE_STATE_PATH.relative_to(ROOT)))
    print("출력: {} (wave_id 열 갱신)".format(MANIFEST_PATH.relative_to(ROOT)))
    print("")
    print("순환 의존성 수: 0")
    print("")
    print("Wave별 Task 수:")
    for w in wave_list:
        flag = " [checkpoint]" if w["checkpoint_required"] else ""
        print("  {} (그룹 {}): {}개{}".format(w["wave_id"], w["group"], len(w["task_ids"]), flag))
    print("")
    print("Page Owner 위치:")
    for tid in sorted(tid for tid in all_ids if tasks_by_id[tid]["Category"] == "Page Owner"):
        print("  {} → {}".format(tid, wave_of[tid]))
    if notes:
        print("")
        print("파일 충돌 분리:")
        for n in notes:
            print("  - " + n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
