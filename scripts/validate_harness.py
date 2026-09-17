#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validates the Free Traveler "harness" itself — CLAUDE.md, the
traveler-project-pipeline Skill, and the 7 pipeline/execution Commands —
rather than the Task content that scripts/audit_tasks.py checks.

This answers a different question than audit_tasks.py: "is the governance
scaffolding (rule files) present and internally consistent?" vs. "are the
generated Tasks correct?".

Usage:
    python scripts/validate_harness.py

Exit codes:
    0 = VALIDATE_HARNESS_PASS
    1 = one or more checks failed
"""

import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import _traveler_common as common

CLAUDE_MD_PATH = common.ROOT / "CLAUDE.md"
SKILL_PATH = common.ROOT / ".claude" / "skills" / "traveler-project-pipeline" / "SKILL.md"
COMMANDS_DIR = common.ROOT / ".claude" / "commands"

REQUIRED_COMMANDS = [
    "gen-tasklist.md",
    "gen-task-details.md",
    "audit-tasks.md",
    "prepare-task.md",
    "implement-task.md",
    "run-wave.md",
    "release-check.md",
]


def read(path):
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def corpus(*paths):
    """Concatenates the text of several harness files for rule-content
    checks that may legitimately live in either CLAUDE.md or the Skill."""
    parts = []
    for p in paths:
        text = read(p)
        if text:
            parts.append(text)
    return "\n".join(parts)


def check_1_claude_md_exists(report):
    if CLAUDE_MD_PATH.exists():
        report.info("CLAUDE.md 존재 확인: {}".format(CLAUDE_MD_PATH.relative_to(common.ROOT)))
    else:
        report.fail("CLAUDE.md가 없습니다: {}".format(CLAUDE_MD_PATH.relative_to(common.ROOT)))


def check_2_skill_exists(report):
    if SKILL_PATH.exists():
        report.info("Skill 파일 존재 확인: {}".format(SKILL_PATH.relative_to(common.ROOT)))
    else:
        report.fail("traveler-project-pipeline Skill 파일이 없습니다: {}".format(SKILL_PATH.relative_to(common.ROOT)))


def check_3_seven_commands_exist(report):
    missing = [c for c in REQUIRED_COMMANDS if not (COMMANDS_DIR / c).exists()]
    if missing:
        report.fail("다음 Command 파일이 없습니다: {}".format(missing))
    else:
        report.info("7개 Command 파일 모두 존재 확인: {}".format(REQUIRED_COMMANDS))


def check_4_harness_schema_marker(report, claude_text):
    if claude_text is None:
        report.fail("CLAUDE.md를 읽을 수 없어 HARNESS_SCHEMA Marker를 확인할 수 없습니다")
        return
    if "HARNESS_SCHEMA=traveler-screen-route-v1" not in claude_text:
        report.fail("CLAUDE.md에 'HARNESS_SCHEMA=traveler-screen-route-v1' Marker가 없습니다")
    else:
        report.info("HARNESS_SCHEMA=traveler-screen-route-v1 Marker 확인")


def check_5_design_path_matches(report, claude_text):
    if claude_text is None:
        report.fail("CLAUDE.md를 읽을 수 없어 DESIGN_PATH를 확인할 수 없습니다")
        return
    m = re.search(r'DESIGN_PATH=(\S+)', claude_text)
    if not m:
        report.fail("CLAUDE.md에 DESIGN_PATH Marker가 없습니다")
        return
    design_path = m.group(1)
    if design_path != "design-reference/D-001/DESIGN.md":
        report.fail("DESIGN_PATH가 'design-reference/D-001/DESIGN.md'가 아니라 '{}'입니다".format(design_path))
        return
    if not (common.ROOT / design_path).exists():
        report.fail("DESIGN_PATH가 가리키는 파일이 실제로 없습니다: {}".format(design_path))
        return
    report.info("DESIGN_PATH 경로 일치 확인: {}".format(design_path))


def check_6_screen_contract_matches(report, claude_text):
    if claude_text is None:
        report.fail("CLAUDE.md를 읽을 수 없어 SCREEN_CONTRACT를 확인할 수 없습니다")
        return
    m = re.search(r'SCREEN_CONTRACT=(\S+)', claude_text)
    if not m:
        report.fail("CLAUDE.md에 SCREEN_CONTRACT Marker가 없습니다")
        return
    contract_path = m.group(1)
    if contract_path != "design-reference/SCREEN_ROUTE_CONTRACT.json":
        report.fail("SCREEN_CONTRACT가 'design-reference/SCREEN_ROUTE_CONTRACT.json'가 아니라 '{}'입니다".format(contract_path))
        return
    data, err = common.load_json(contract_path)
    if err:
        report.fail(err)
        return
    if data.get("schema_version") != common.HARNESS_SCHEMA:
        report.fail(
            "SCREEN_CONTRACT의 schema_version이 {!r}이 아니라 {!r}입니다".format(
                common.HARNESS_SCHEMA, data.get("schema_version")
            )
        )
        return
    report.info("SCREEN_CONTRACT 경로·schema_version 일치 확인: {}".format(contract_path))


def check_7_page_owner_rule(report, text):
    has_owner_entry = "Page Owner" in text and "Page Entry" in text
    has_exactly_five = re.search(r'정확히\s*5개', text) is not None
    if has_owner_entry and has_exactly_five:
        report.info("Page Owner 5개 규칙 확인")
    else:
        report.fail("Page Owner가 Page Entry를 조립하고 정확히 5개라는 규칙을 CLAUDE.md/Skill에서 찾을 수 없습니다")


def check_8_db_table_scope_rule(report, text):
    if re.search(r'6개[^\n]{0,15}테이블|테이블[^\n]{0,15}6개', text):
        report.info("DB Table 6개 기본 범위 규칙 확인")
    else:
        report.fail("DB Table을 6개로 제한한다는 규칙을 CLAUDE.md/Skill에서 찾을 수 없습니다")


def check_9_no_persist_external_input_rule(report, text):
    if re.search(r'(항공|숙소)[^\n]{0,40}(전송하지 않는다|저장하지 않는다|보내지 않는다)', text):
        report.info("항공·숙소 외부 입력 비저장 규칙 확인")
    else:
        report.fail("항공·숙소 입력값을 서버·DB·URL·로그로 보내지 않는다는 규칙을 CLAUDE.md/Skill에서 찾을 수 없습니다")


def check_10_playwright_chromium_smoke_rule(report, text):
    if "Playwright" in text and "chromium" in text.lower() and ("Smoke" in text or "핵심" in text):
        report.info("Playwright Chromium Smoke 규칙 확인")
    else:
        report.fail("Playwright는 Chromium Smoke만 사용한다는 규칙을 CLAUDE.md/Skill에서 찾을 수 없습니다")


def check_11_auto_merge_false(report, claude_text):
    if claude_text is None:
        report.fail("CLAUDE.md를 읽을 수 없어 AUTO_MERGE를 확인할 수 없습니다")
        return
    if "AUTO_MERGE=false" not in claude_text:
        report.fail("CLAUDE.md에 'AUTO_MERGE=false' Marker가 없습니다")
    else:
        report.info("AUTO_MERGE=false 확인")


def check_12_aws_enabled_false(report, claude_text):
    if claude_text is None:
        report.fail("CLAUDE.md를 읽을 수 없어 AWS_ENABLED를 확인할 수 없습니다")
        return
    if "AWS_ENABLED=false" not in claude_text:
        report.fail("CLAUDE.md에 'AWS_ENABLED=false' Marker가 없습니다")
    else:
        report.info("AWS_ENABLED=false 확인")


def check_13_excluded_protection_rule(report, text):
    if re.search(r'EXCLUDED[^\n]{0,30}(임의로 구현|구현하지 않는다)', text):
        report.info("EXCLUDED 보호 규칙 확인")
    else:
        report.fail("EXCLUDED 기능을 임의로 구현하지 않는다는 규칙을 CLAUDE.md/Skill에서 찾을 수 없습니다")


def main():
    report = common.Report("Free Traveler Pipeline - Harness Validation")

    claude_text = read(CLAUDE_MD_PATH)
    skill_text = read(SKILL_PATH)
    combined = corpus(CLAUDE_MD_PATH, SKILL_PATH)

    check_1_claude_md_exists(report)
    check_2_skill_exists(report)
    check_3_seven_commands_exist(report)
    check_4_harness_schema_marker(report, claude_text)
    check_5_design_path_matches(report, claude_text)
    check_6_screen_contract_matches(report, claude_text)
    check_7_page_owner_rule(report, combined)
    check_8_db_table_scope_rule(report, combined)
    check_9_no_persist_external_input_rule(report, combined)
    check_10_playwright_chromium_smoke_rule(report, combined)
    check_11_auto_merge_false(report, claude_text)
    check_12_aws_enabled_false(report, claude_text)
    check_13_excluded_protection_rule(report, combined)

    code = report.print_and_return_code()
    print("")
    if code == 0:
        print("VALIDATE_HARNESS_PASS")
    else:
        print("VALIDATE_HARNESS_FAIL")
    return code


if __name__ == "__main__":
    sys.exit(main())
