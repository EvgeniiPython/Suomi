#!/usr/bin/env python3
"""Read-only validation for the Finnish Learning Wiki.

This is the first safety-oriented prototype: it validates durable records but
never modifies learner data. Keep deterministic checks here; pedagogical
reasoning remains in the Markdown protocols and the lesson model.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "Finnish-Learning-Wiki"
SESSIONS = WIKI / "03_Sessions"
SYSTEM = WIKI / "00_System"

REQUIRED_SYSTEM_FILES = {
    "Lesson_Protocol.md",
    "Runtime_Rules.md",
    "Current_State.md",
    "Mastery_Criteria.md",
    "Metrics_And_Audit.md",
    "Decision_Gates.md",
    "Prior_Art_Search.md",
    "Lesson_Diary_Protocol.md",
    "Audit_Protocol.md",
}

PASS = "PASS"
WARN = "WARNING"
FAIL = "FAIL"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Cannot read {path}: {exc}") from exc


def add_result(results: list[tuple[str, str, str]], status: str, check: str, detail: str) -> None:
    results.append((status, check, detail))


def validate_system_files(results: list[tuple[str, str, str]]) -> None:
    existing = {p.name for p in SYSTEM.glob("*.md")}
    missing = sorted(REQUIRED_SYSTEM_FILES - existing)
    if missing:
        add_result(results, FAIL, "Required system protocols", "Missing: " + ", ".join(missing))
    else:
        add_result(results, PASS, "Required system protocols", "All required files are present")


def validate_sessions(results: list[tuple[str, str, str]]) -> None:
    """Validate both legacy and current session records.

    Historical sessions predate the new diary/audit protocol and use several
    legitimate schemas (e.g. Topic/Result, Metrics/Next step, Retention).
    They must not fail merely because they lack the newer word 'lesson' or a
    modern retention heading. Newer records can be checked more strictly.
    """
    session_files = sorted(SESSIONS.glob("*.md")) if SESSIONS.exists() else []
    if not session_files:
        add_result(results, WARN, "Session records", "No session Markdown files found")
        return

    malformed = 0
    legacy = 0
    warnings = 0

    legacy_content_markers = (
        "## тема",
        "## фокус",
        "## что закрепляли",
        "## материал",
        "## основные чанки",
        "## основной чанк",
        "## active material",
        "## goal",
        "## result",
        "## результат",
        "## ход урока",
        "## lesson design",
    )
    modern_markers = (
        "## статус",
        "## status",
        "## mastery / retention",
        "## retention result",
        "## candidate chunks",
        "## что реально вышло",
    )

    for path in session_files:
        text = read_text(path)
        lower = text.lower()
        has_date_heading = bool(re.search(r"^# .*20\d{2}", text, flags=re.MULTILINE))
        has_content = any(marker in lower for marker in legacy_content_markers)
        has_modern = any(marker in lower for marker in modern_markers)

        if not has_date_heading or not has_content:
            malformed += 1
            continue

        if not has_modern:
            legacy += 1

        # High-value deterministic consistency checks. These do not judge
        # whether the lesson was pedagogically good; they only catch obvious
        # missing-record contradictions.
        if "new chunk" in lower and any(flag in lower for flag in ("unstable", "failed transfer", "transfer: fail")):
            warnings += 1

        if "stable" in lower and "evidence" not in lower:
            warnings += 1

    if malformed:
        add_result(results, FAIL, "Session structure", f"{malformed} session file(s) are malformed or lack recognizable durable record structure")
    elif legacy:
        add_result(results, PASS, "Session structure", f"Checked {len(session_files)} session file(s); {legacy} legacy-format record(s) retained")
    else:
        add_result(results, PASS, "Session structure", f"Checked {len(session_files)} current-format session file(s)")

    if warnings:
        add_result(results, WARN, "Potential evidence conflicts", f"Found {warnings} item(s) needing human review")
    else:
        add_result(results, PASS, "Potential evidence conflicts", "No obvious deterministic conflicts detected")


def validate_protocol_content(results: list[tuple[str, str, str]]) -> None:
    lesson_protocol = read_text(SYSTEM / "Lesson_Protocol.md")
    runtime_rules = read_text(SYSTEM / "Runtime_Rules.md")

    required_phrases = [
        "Second Output",
        "Variation Chain",
        "Cold Recall",
        "Transfer",
        "Second Chance",
        "Mastery Ladder",
        "Rule новых chunks",
    ]
    lesson_lower = lesson_protocol.lower()
    phrase_variants = {
        "Rule новых chunks": ("правило новых chunks", "новых chunks"),
    }

    missing = []
    for phrase in required_phrases:
        if phrase.lower() in lesson_lower:
            continue
        variants = phrase_variants.get(phrase, ())
        if variants and any(v in lesson_lower for v in variants):
            continue
        missing.append(phrase)

    if missing:
        add_result(results, WARN, "Lesson protocol core", "Expected markers missing: " + ", ".join(missing))
    else:
        add_result(results, PASS, "Lesson protocol core", "Core learning loop markers present")

    runtime_requirements = [
        "Require Second Output after correction.",
        "New chunks require stable recall + variation + transfer",
    ]
    runtime_lower = runtime_rules.lower()
    missing_runtime = [p for p in runtime_requirements if p.lower() not in runtime_lower]
    if missing_runtime:
        add_result(results, FAIL, "Runtime gates", "Missing required rule(s): " + ", ".join(missing_runtime))
    else:
        add_result(results, PASS, "Runtime gates", "Critical runtime rules present")


def main() -> int:
    results: list[tuple[str, str, str]] = []
    validate_system_files(results)
    validate_protocol_content(results)
    validate_sessions(results)

    print("Finnish Learning System — Read-only Audit")
    print("=" * 52)
    for status, check, detail in results:
        print(f"[{status}] {check}: {detail}")

    critical_failures = sum(1 for status, _, _ in results if status == FAIL)
    warnings = sum(1 for status, _, _ in results if status == WARN)

    if critical_failures:
        print(f"\nSTATUS: FAIL ({critical_failures} critical issue(s), {warnings} warning(s))")
        return 1

    if warnings:
        print(f"\nSTATUS: PASS_WITH_WARNINGS ({warnings} warning(s))")
        return 0

    print("\nSTATUS: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
