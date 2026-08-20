#!/usr/bin/env python3
"""Read-only validation for the Finnish Learning Wiki.

This validator checks durable records but never modifies learner data.
Pedagogical reasoning remains in the Markdown protocols and lesson model.
"""

from __future__ import annotations

import re
import sys
from datetime import date
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
    "Session_Record_Schema.md",
    "Audit_Protocol.md",
}

PASS = "PASS"
WARN = "WARNING"
FAIL = "FAIL"

# New records created from this date onward must use canonical-v1.
# Existing historical records remain grandfathered as legacy records.
CANONICAL_REQUIRED_FROM = date(2026, 8, 21)

CANONICAL_REQUIRED_HEADINGS = (
    "## session result",
    "## evidence",
    "## chunk decisions",
    "## mastery",
    "## retention",
    "## errors",
    "## next step",
)

VALID_LESSON_STATUS = {"COMPLETED", "PARTIAL", "INTERRUPTED"}
VALID_DECISIONS = {"ACCEPT", "REJECT", "DEFER", "PROMOTE", "KEEP", "DEMOTE"}
VALID_LEVELS = {"ACTIVE", "CONSOLIDATING", "STABLE", "DORMANT"}
VALID_RETENTION = {"SCHEDULED", "DUE", "PASSED", "FAILED", "NOT_APPLICABLE"}


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


def has_explicit_stable_status(text: str) -> bool:
    """Return True only for an explicit status/mastery assertion of STABLE.

    Incidental prose such as 'not fully stable' or 'stable recall' is not a
    state declaration. Canonical-v1 records should use current_level instead.
    """
    patterns = (
        r"\bstatus\s*[:=-]\s*stable\b",
        r"\bmastery\s*(?:/|and)?\s*retention\s*[:=-]\s*stable\b",
        r"\bretention\s*(?:status)?\s*[:=-]\s*stable\b",
        r"\bmastery\s*[:=-]\s*stable\b",
        r"\b(?:chunk|item|target)\s+status\s*[:=-]\s*stable\b",
    )
    lower = text.lower()
    return any(re.search(pattern, lower) for pattern in patterns)


def extract_session_date(path: Path, text: str) -> date | None:
    match = re.search(r"(20\d{2})[-_](\d{2})[-_](\d{2})", path.name)
    if not match:
        match = re.search(r"^# .*?(20\d{2})[-./](\d{1,2})[-./](\d{1,2})", text, flags=re.MULTILINE)
    if not match:
        return None
    try:
        return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError:
        return None


def nonempty_field(text: str, field: str) -> bool:
    match = re.search(rf"(?im)^\s*{re.escape(field)}\s*:\s*(.+?)\s*$", text)
    return bool(match and match.group(1).strip())


def canonical_value(text: str, field: str) -> str | None:
    match = re.search(rf"(?im)^\s*{re.escape(field)}\s*:\s*([^\n#]+?)\s*$", text)
    return match.group(1).strip().upper() if match else None


def validate_canonical_session(text: str) -> list[str]:
    """Validate the structured Session Result without interpreting pedagogy."""
    lower = text.lower()
    problems: list[str] = []

    if "record_schema: canonical-v1" not in lower:
        problems.append("missing record_schema: canonical-v1")

    for heading in CANONICAL_REQUIRED_HEADINGS:
        if heading not in lower:
            problems.append(f"missing {heading.title()} section")

    lesson_status = canonical_value(text, "lesson_status")
    if lesson_status not in VALID_LESSON_STATUS:
        problems.append("invalid or missing lesson_status")

    score_match = re.search(r"(?im)^\s*evidence_score\s*:\s*([0-3])\s*$", text)
    if not score_match:
        problems.append("missing or invalid evidence_score (0-3)")

    level = canonical_value(text, "current_level")
    if level not in VALID_LEVELS:
        problems.append("invalid or missing current_level")

    retention = canonical_value(text, "status")
    # In the Retention section, status is the canonical retention field. Avoid
    # treating unrelated prose/status fields as canonical by requiring the
    # Retention heading to precede the field.
    retention_match = re.search(r"(?is)## retention\s*(.*?)(?:## errors|## next step|\Z)", text)
    retention_block = retention_match.group(1) if retention_match else ""
    retention_status = canonical_value(retention_block, "status")
    if retention_status not in VALID_RETENTION:
        problems.append("invalid or missing Retention status")

    # Stable and promotion are state-changing claims. They require explicit
    # evidence in their canonical block, not merely the word 'evidence' elsewhere.
    mastery_match = re.search(r"(?is)## mastery\s*(.*?)(?:## retention|## errors|## next step|\Z)", text)
    mastery_block = mastery_match.group(1) if mastery_match else ""
    chunk_match = re.search(r"(?is)## chunk decisions\s*(.*?)(?:## mastery|## retention|## errors|## next step|\Z)", text)
    chunk_block = chunk_match.group(1) if chunk_match else ""

    if level == "STABLE" and not nonempty_field(mastery_block, "evidence"):
        problems.append("current_level: STABLE requires Mastery evidence")

    decisions = [v.upper() for v in re.findall(r"(?im)^\s*decision\s*:\s*([A-Za-z_]+)\s*$", chunk_block)]
    invalid_decisions = sorted(set(decisions) - VALID_DECISIONS)
    if invalid_decisions:
        problems.append("invalid chunk decision(s): " + ", ".join(invalid_decisions))

    if "PROMOTE" in decisions and not nonempty_field(chunk_block, "evidence"):
        problems.append("PROMOTE requires Chunk Decisions evidence")

    if lesson_status in {"PARTIAL", "INTERRUPTED"} and not nonempty_field(text, "next_action"):
        problems.append("partial/interrupted lesson requires a next_action")

    return problems


def validate_sessions(results: list[tuple[str, str, str]]) -> None:
    """Validate legacy sessions plus strict canonical-v1 records."""
    session_files = sorted(SESSIONS.glob("*.md")) if SESSIONS.exists() else []
    if not session_files:
        add_result(results, WARN, "Session records", "No session Markdown files found")
        return

    malformed = 0
    legacy = 0
    canonical = 0
    canonical_problems = 0
    warnings = 0
    future_schema_failures: list[str] = []

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
        "## session result",
    )

    for path in session_files:
        text = read_text(path)
        lower = text.lower()
        session_date = extract_session_date(path, text)
        has_date_heading = bool(re.search(r"^# .*20\d{2}", text, flags=re.MULTILINE))
        has_legacy_content = any(marker in lower for marker in legacy_content_markers)
        has_modern_content = any(marker in lower for marker in modern_markers)
        has_canonical = "record_schema: canonical-v1" in lower or "## session result" in lower
        has_content = has_legacy_content or has_modern_content

        if not has_date_heading or not has_content:
            malformed += 1
            continue

        if has_canonical:
            canonical += 1
            problems = validate_canonical_session(text)
            if problems:
                canonical_problems += len(problems)
                if session_date and session_date >= CANONICAL_REQUIRED_FROM:
                    future_schema_failures.append(f"{path.name}: " + "; ".join(problems))
                else:
                    warnings += len(problems)
        else:
            legacy += 1
            if session_date and session_date >= CANONICAL_REQUIRED_FROM:
                future_schema_failures.append(f"{path.name}: missing canonical-v1 Session Result")

        # Legacy/current narrative consistency checks remain deliberately
        # conservative. Do not infer state from the mere presence of words.
        if "new chunk" in lower and any(flag in lower for flag in ("unstable", "failed transfer", "transfer: fail")):
            warnings += 1

        if has_explicit_stable_status(text) and not has_canonical and "evidence" not in lower:
            warnings += 1

    if malformed:
        add_result(results, FAIL, "Session structure", f"{malformed} session file(s) are malformed or lack recognizable durable record structure")
    else:
        detail = f"Checked {len(session_files)} session file(s); {legacy} legacy-format record(s) retained; {canonical} canonical-v1 record(s) checked"
        add_result(results, PASS, "Session structure", detail)

    if future_schema_failures:
        add_result(results, FAIL, "Canonical session records", "New session record(s) violate canonical-v1: " + " | ".join(future_schema_failures))
    elif canonical_problems:
        add_result(results, WARN, "Canonical session records", f"Historical/current canonical record(s) have {canonical_problems} issue(s) needing review")
    else:
        add_result(results, PASS, "Canonical session records", "Canonical-v1 structure is valid for all applicable records")

    if warnings:
        add_result(results, WARN, "Potential evidence conflicts", f"Found {warnings} item(s) needing human review")
    else:
        add_result(results, PASS, "Potential evidence conflicts", "No obvious deterministic conflicts detected")


def validate_protocol_content(results: list[tuple[str, str, str]]) -> None:
    lesson_protocol = read_text(SYSTEM / "Lesson_Protocol.md")
    runtime_rules = read_text(SYSTEM / "Runtime_Rules.md")
    schema = read_text(SYSTEM / "Session_Record_Schema.md")

    required_phrases = [
        "Second Output",
        "Variation Chain",
        "Cold Recall",
        "Transfer",
        "Second Chance",
        "Mastery Ladder",
        "Rule новых chunks",
        "Canonical Session Result",
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
        add_result(results, PASS, "Lesson protocol core", "Core learning loop and canonical close markers present")

    runtime_requirements = [
        "Require Second Output after correction.",
        "New chunks require stable recall + variation + transfer",
        "canonical-v1",
        "current_level",
    ]
    runtime_lower = runtime_rules.lower()
    missing_runtime = [p for p in runtime_requirements if p.lower() not in runtime_lower]
    if missing_runtime:
        add_result(results, FAIL, "Runtime gates", "Missing required rule(s): " + ", ".join(missing_runtime))
    else:
        add_result(results, PASS, "Runtime gates", "Critical runtime and canonical-record rules present")

    schema_requirements = ["record_schema: canonical-v1", "## Session Result", "current_level", "evidence_score"]
    schema_lower = schema.lower()
    missing_schema = [p for p in schema_requirements if p.lower() not in schema_lower]
    if missing_schema:
        add_result(results, FAIL, "Session schema", "Missing required schema marker(s): " + ", ".join(missing_schema))
    else:
        add_result(results, PASS, "Session schema", "Canonical-v1 schema definition present")


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
