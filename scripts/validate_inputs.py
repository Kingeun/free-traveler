#!/usr/bin/env python3
"""Pre-flight input validation for the Free Traveler task-generation pipeline.

Run before /gen-tasklist. Verifies that every input document the pipeline
depends on exists and is internally consistent (schema version, screen
count/uniqueness, full 114-requirement coverage in the traceability doc),
and snapshots the real src/app file tree so Task generation never has to
guess which files already exist.

Usage:
    python scripts/validate_inputs.py

Exit code 0 = PASS, 1 = FAIL. A JSON report is also written to
tasks/validate_inputs_report.json (the tasks/ directory is created if
missing) so later pipeline steps and humans can inspect the last run.
"""

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import _traveler_common as common


def check_required_docs(report):
    for rel_path in common.REQUIRED_INPUT_DOCS:
        if (common.ROOT / rel_path).exists():
            report.info("입력 문서 확인: {}".format(rel_path))
        else:
            report.fail("필수 입력 문서가 없습니다: {}".format(rel_path))


def check_package_json(report):
    data, err = common.load_json("package.json")
    if err:
        report.fail(err)
        return
    if "next" not in data.get("dependencies", {}):
        report.fail("package.json dependencies에 next가 없습니다")
    else:
        report.info(
            "package.json 확인: next {}".format(data["dependencies"].get("next"))
        )


def check_screen_route_contract(report):
    data, errors = common.load_screen_route_contract()
    if data is None:
        for e in errors:
            report.fail(e)
        return None
    for e in errors:
        report.fail(e)
    screens = data.get("screens", [])
    report.info(
        "SCREEN_ROUTE_CONTRACT.json 확인: schema_version={}, screens={}개".format(
            data.get("schema_version"), len(screens)
        )
    )
    for s in screens:
        report.info(
            "  Screen {} -> {} ({})".format(
                s.get("id"), s.get("route"), s.get("page_entry")
            )
        )
    tech_routes = data.get("technical_routes", [])
    report.info("기술 Route {}개 확인(Screen 수에 미포함)".format(len(tech_routes)))
    return data


def check_traceability(report):
    requirements, errors = common.parse_traceability_requirements()
    for e in errors:
        report.fail(e)
    if not requirements:
        return requirements

    total = len(requirements)
    excluded = [r for r, v in requirements.items() if common.is_excluded_status(v["status"])]
    implement = [r for r in requirements if r not in excluded]
    report.info(
        "UIUX_TRACEABILITY.md 확인: 총 {}개(IMPLEMENT 계열 {}개, EXCLUDED {}개)".format(
            total, len(implement), len(excluded)
        )
    )
    if total != common.EXPECTED_TOTAL_REQ_COUNT:
        report.fail(
            "Requirement 총개수가 {}개가 아니라 {}개입니다".format(
                common.EXPECTED_TOTAL_REQ_COUNT, total
            )
        )
    return requirements


def check_src_app_tree(report):
    files = common.scan_app_tree()
    if not files:
        report.fail("src/app 아래에서 파일을 하나도 찾지 못했습니다")
        return files
    report.info("src/app 실제 파일 {}개 확인:".format(len(files)))
    for f in files:
        report.info("  - {}".format(f))
    return files


def check_design_reference(report):
    contract_text = common.read_text("design-reference/UI_CONTRACT.md")
    if contract_text is None:
        report.fail("design-reference/UI_CONTRACT.md 파일이 없습니다")
    else:
        for screen_id in ["SCR-001", "SCR-002", "SCR-003", "SCR-004", "SCR-005"]:
            if screen_id not in contract_text:
                report.fail(
                    "UI_CONTRACT.md에 {} 항목이 보이지 않습니다".format(screen_id)
                )

    design_text = common.read_text("design-reference/D-001/DESIGN.md")
    if design_text is None:
        report.fail("design-reference/D-001/DESIGN.md 파일이 없습니다")
    else:
        if "Do Not" not in design_text and "Do / Do Not" not in design_text:
            report.fail("D-001/DESIGN.md에 Do Not 섹션이 보이지 않습니다")


def write_report_file(payload):
    tasks_dir = common.ROOT / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    out_path = tasks_dir / "validate_inputs_report.json"
    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return out_path


def main():
    report = common.Report("Free Traveler Pipeline - Input Validation")

    check_required_docs(report)
    contract = check_screen_route_contract(report)
    requirements = check_traceability(report)
    app_files = check_src_app_tree(report)
    check_design_reference(report)

    code = report.print_and_return_code()

    payload = {
        "harness_schema": common.HARNESS_SCHEMA,
        "ok": report.ok(),
        "violations": report.violations,
        "screen_count": len(contract.get("screens", [])) if contract else 0,
        "requirement_count": len(requirements),
        "src_app_files": app_files,
    }
    out_path = write_report_file(payload)
    print("")
    print("리포트 저장: {}".format(out_path.relative_to(common.ROOT).as_posix()))

    return code


if __name__ == "__main__":
    sys.exit(main())
