"""Shared helpers for the Free Traveler task-generation pipeline scripts.

Used by validate_inputs.py and audit_tasks.py. Not a standalone entry point.
Stdlib only (Python 3.9+ compatible) so no project dependencies are required
to run the pipeline scripts.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HARNESS_SCHEMA = "traveler-screen-route-v1"
EXPECTED_SCREEN_COUNT = 5
EXPECTED_REQ_FUNC_COUNT = 80
EXPECTED_REQ_NF_COUNT = 34
EXPECTED_TOTAL_REQ_COUNT = EXPECTED_REQ_FUNC_COUNT + EXPECTED_REQ_NF_COUNT

MAX_DB_TABLES = 6
EXPECTED_TEST_SMOKE_COUNT = EXPECTED_SCREEN_COUNT  # one Chromium smoke task per screen

REQUIRED_INPUT_DOCS = [
    "docs/06_SRS_UIUX_REVISED.md",
    "docs/PROJECT_SCOPE.md",
    "docs/UIUX_TRACEABILITY.md",
    "design-reference/D-001/DESIGN.md",
    "design-reference/UI_CONTRACT.md",
    "design-reference/SCREEN_ROUTE_CONTRACT.json",
    "package.json",
]

FORBIDDEN_KEYWORDS = [
    "EC2",
    "AWS",
    "자동 병합",
    "자동 Merge",
    "auto-merge",
    "별점",
    "★",  # ★
    "Lorem ipsum",
    "준비 중",  # 준비 중
    "정보 확인 필요",  # 정보 확인 필요
    "Rausch",
    "Guest favorite",
]

REQ_ROW_RE = re.compile(
    r"^\|\s*(REQ-(?:FUNC|NF)-\d{3})\s*\|\s*([^|]+?)\s*\|"
)


class Report:
    """Collects violations and info lines for a pipeline script run."""

    def __init__(self, title):
        self.title = title
        self.violations = []
        self.notes = []

    def fail(self, message):
        self.violations.append(message)

    def info(self, message):
        self.notes.append(message)

    def ok(self):
        return len(self.violations) == 0

    def print_and_return_code(self):
        print("=" * 72)
        print(self.title)
        print("=" * 72)
        for line in self.notes:
            print("  - " + line)
        if self.violations:
            print("")
            print("FAIL - {} violation(s):".format(len(self.violations)))
            for v in self.violations:
                print("  [FAIL] " + v)
            print("")
            print("RESULT: FAIL")
            return 1
        print("")
        print("RESULT: PASS")
        return 0


def read_text(relative_path):
    path = ROOT / relative_path
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def load_json(relative_path):
    text = read_text(relative_path)
    if text is None:
        return None, "파일이 없습니다: {}".format(relative_path)
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, "JSON 파싱 실패({}): {}".format(relative_path, exc)


def load_screen_route_contract():
    """Returns (data, errors). data is None if the contract could not be loaded."""
    errors = []
    data, err = load_json("design-reference/SCREEN_ROUTE_CONTRACT.json")
    if err:
        errors.append(err)
        return None, errors

    if data.get("schema_version") != HARNESS_SCHEMA:
        errors.append(
            "schema_version이 {!r}이 아니라 {!r}입니다".format(
                HARNESS_SCHEMA, data.get("schema_version")
            )
        )

    screens = data.get("screens", [])
    if len(screens) != EXPECTED_SCREEN_COUNT:
        errors.append(
            "screens 배열 개수가 {}개가 아니라 {}개입니다".format(
                EXPECTED_SCREEN_COUNT, len(screens)
            )
        )

    routes = [s.get("route") for s in screens]
    if len(set(routes)) != len(routes):
        errors.append("screens의 route 값에 중복이 있습니다: {}".format(routes))

    entries = [s.get("page_entry") for s in screens]
    if len(set(entries)) != len(entries):
        errors.append("screens의 page_entry 값에 중복이 있습니다: {}".format(entries))

    return data, errors


def parse_requirement_table(relative_path):
    """Parses any doc with '| REQ-FUNC-xxx | <status> | ...' table rows.

    Returns (requirements, errors) where requirements is a dict:
        { "REQ-FUNC-001": {"status": "IMPLEMENT"}, ... }
    Only real table rows are matched, so prose mentions elsewhere in the
    document are ignored.
    """
    errors = []
    text = read_text(relative_path)
    if text is None:
        errors.append("{} 파일이 없습니다".format(relative_path))
        return {}, errors

    requirements = {}
    for line in text.splitlines():
        m = REQ_ROW_RE.match(line)
        if not m:
            continue
        req_id, status = m.group(1), m.group(2).strip()
        # Guard against accidentally matching summary-table rows such as
        # "REQ-FUNC-001~080" which the regex's \d{3} anchor already excludes,
        # but keep a defensive check in case the doc format changes.
        if "~" in req_id:
            continue
        requirements[req_id] = {"status": status}

    func_ids = [r for r in requirements if r.startswith("REQ-FUNC-")]
    nf_ids = [r for r in requirements if r.startswith("REQ-NF-")]
    if len(func_ids) != EXPECTED_REQ_FUNC_COUNT:
        errors.append(
            "{}: REQ-FUNC 행 개수가 {}개가 아니라 {}개입니다".format(
                relative_path, EXPECTED_REQ_FUNC_COUNT, len(func_ids)
            )
        )
    if len(nf_ids) != EXPECTED_REQ_NF_COUNT:
        errors.append(
            "{}: REQ-NF 행 개수가 {}개가 아니라 {}개입니다".format(
                relative_path, EXPECTED_REQ_NF_COUNT, len(nf_ids)
            )
        )

    return requirements, errors


def parse_traceability_requirements():
    """Parses docs/UIUX_TRACEABILITY.md. See parse_requirement_table()."""
    return parse_requirement_table("docs/UIUX_TRACEABILITY.md")


def parse_project_scope_requirements():
    """Parses docs/PROJECT_SCOPE.md. See parse_requirement_table()."""
    return parse_requirement_table("docs/PROJECT_SCOPE.md")


def is_excluded_status(status_text):
    return "EXCLUDED" in status_text.upper()


def scan_app_tree():
    """Returns a sorted list of POSIX-style relative paths under src/app."""
    app_dir = ROOT / "src" / "app"
    if not app_dir.exists():
        return []
    paths = []
    for p in app_dir.rglob("*"):
        if p.is_file():
            paths.append(p.relative_to(ROOT).as_posix())
    return sorted(paths)


def scan_forbidden_keywords(text):
    found = []
    for kw in FORBIDDEN_KEYWORDS:
        if kw in text:
            found.append(kw)
    return found
