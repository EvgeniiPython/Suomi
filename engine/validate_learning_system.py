#!/usr/bin/env python3
"""Read-only validation for the Finnish Learning Wiki.

This is the first safety-oriented prototype: it validates durable records but
never modifies learner data. Keep deterministic checks here; pedagogical
reasoning remains in the Markdown protocols and the lesson model.
"""

from __future__ import annotations

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
    session_files = sorted(SESSIONS.glob("*.md")) if SESSIONS.exists() else []
    if not session_files:
        add_result(results, WARN, "Session records", "No session Markdown files found")
        return

    failures = 0
    warnings = 0

    for path in session_files:
        text = read_text(path).lower()
        if not ("lesson" in text and "retention" in text):
            failures += 1
            continue

        # High-value deterministic consistency checks. These do not judge
        # whether the lesson was pedagogically good; they only catch obvious
        # missing-record contradictions.
        if "new chunk" in text and any(flag in text for flag in ("unstable", "failed transfer", "transfer: fail")):
            warnings += 1

        if "stable" in text and "evidence" not in text:
            warnings += 1

    if failures:
        add_result(results, FAIL, "Session structure", f"{failures} session file(s) lack basic durable record fields")
    else:
        add_result(results, PASS, "Session structure", f"Checked {len(session_files)} session file(s)")

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
    # The repository uses Russian prose in several protocol headings while
    # keeping the technical terms in English; support both current forms.
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
