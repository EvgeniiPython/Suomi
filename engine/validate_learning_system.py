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

CANONICAL_REQUIRED_FROM = date(2026, 8, 21)

CANONICAL_REQUIRED_HEADINGS = (
    "## session result",
    "## evidence",
    "## protocol completion",
    "## chunk decisions",
    "## mastery",
    "## retention",
    "## errors",
    "## next step",
)

REQUIRED_PROTOCOL_STAGES = (
    "retrieval",
    "listening_speaking",
    "deep_processing",
    "controlled_speaking",
    "finnish_dialogue",
    "error_repair_second_chance",
    "final_challenge_recall",
    "retention_record",
)

VALID_LESSON_STATUS = {"COMPLETED", "PARTIAL", "INTERRUPTED"}
VALID_DECISIONS = {"ACCEPT", "REJECT", "DEFER", "PROMOTE", "KEEP", "DEMOTE"}
VALID_LEVELS = {"ACTIVE", "CONSOLIDATING", "STABLE", "DORMANT"}
VALID_RETENTION = {"SCHEDULED", "DUE", "PASSED", "FAILED", "NOT_APPLICABLE"}
VALID_CONTINUATION = {"YES", "NO"}


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
    """Return True only for an explicit status/mastery assertion of STABLE."""
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


def list_field(text: str, field: str) -> list[str]:
    value = canonical_value(text, field)
    if not value or value in {"NONE", "N/A", "NOT_APPLICABLE"}:
        return []
    return [item.strip().lower() for item in re.split(r"[,;]", value) if item.strip()]


def validate_protocol_completion(text: str) -> tuple[list[str], str | None, str | None]:
    """Validate explicit protocol-stage accounting and return missing stages."""
    problems: list[str] = []
    completion_match = re.search(r"(?is)## protocol completion\s*(.*?)(?:## chunk decisions|## mastery|## retention|## errors|## next step|\Z)", text)
    block = completion_match.group(1) if completion_match else ""

    required = list_field(block, "required_stages")
    completed = set(list_field(block, "completed_stages"))
    declared_missing = set(list_field(block, "missing_stages"))
    continuation = canonical_value(block, "continuation_required")
    resume = canonical_value(block, "continuation_next_stage")

    if set(required) != set(REQUIRED_PROTOCOL_STAGES):
        problems.append("required_stages must contain the canonical eight macro-stages")

    unknown_completed = sorted(completed - set(REQUIRED_PROTOCOL_STAGES))
    if unknown_completed:
        problems.append("unknown completed stage(s): " + ", ".join(unknown_completed))

    missing = [stage for stage in REQUIRED_PROTOCOL_STAGES if stage not in completed]
    if set(declared_missing) != set(missing):
        problems.append("missing_stages does not match completed_stages")

    if continuation not in VALID_CONTINUATION:
        problems.append("invalid or missing continuation_required")

    if missing:
        if continuation != "YES":
            problems.append("incomplete protocol requires continuation_required: YES")
        if not resume or resume not in missing:
            problems.append("continuation_next_stage must be the first missing stage")
        if not nonempty_field(block, "continuation_reason"):
            problems.append("incomplete protocol requires continuation_reason")
    else:
        if continuation != "NO":
            problems.append("fully completed protocol requires continuation_required: NO")
        if resume not in {None, "", "NONE", "N/A"}:
            problems.append("completed protocol should not declare a continuation_next_stage")

    return problems, (missing[0] if missing else None), continuation


def validate_canonical_session(text: str) -> tuple[list[str], str | None, str | None]:
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

    retention_match = re.search(r"(?is)## retention\s*(.*?)(?:## errors|## next step|\Z)", text)
    retention_block = retention_match.group(1) if retention_match else ""
    retention_status = canonical_value(retention_block, "status")
    if retention_status not in VALID_RETENTION:
        problems.append("invalid or missing Retention status")

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

    protocol_problems, resume_stage, continuation = validate_protocol_completion(text)
    problems.extend(protocol_problems)

    if lesson_status in {"PARTIAL", "INTERRUPTED"} and not nonempty_field(text, "next_action"):
        problems.append("partial/interrupted lesson requires a next_action")

    if resume_stage and continuation == "YES" and lesson_status == "COMPLETED":
        problems.append("lesson_status cannot be COMPLETED while continuation is required")

    return problems, resume_stage, continuation


def validate_sessions(results: list[tuple[str, str, str]], continuation_directives: list[str]) -> None:
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
        "## тема", "## фокус", "## что закрепляли", "## материал", "## основные чанки",
        "## основной чанк", "## active material", "## goal", "## result", "## результат",
        "## ход урока", "## lesson design",
    )
    modern_markers = (
        "## статус", "## status", "## mastery / retention", "## retention result",
        "## candidate chunks", "## что реально вышло", "## session result",
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
            problems, resume_stage, continuation = validate_canonical_session(text)
            if problems:
                canonical_problems += len(problems)
                if session_date and session_date >= CANONICAL_REQUIRED_FROM:
                    future_schema_failures.append(f"{path.name}: " + "; ".join(problems))
                else:
                    warnings += len(problems)
            if resume_stage and continuation == "YES":
                continuation_directives.append(
                    f"{path.name}: RESUME_STAGE={resume_stage}; MISSING_STAGES="
                    + ",".join([s for s in REQUIRED_PROTOCOL_STAGES if s in list_field(re.search(r"(?is)## protocol completion\s*(.*?)(?:## chunk decisions|## mastery|## retention|## errors|## next step|\Z)", text).group(1) if re.search(r"(?is)## protocol completion\s*(.*?)(?:## chunk decisions|## mastery|## retention|## errors|## next step|\Z)", text) else "", "missing_stages")])
                )
        else:
            legacy += 1
            if session_date and session_date >= CANONICAL_REQUIRED_FROM:
                future_schema_failures.append(f"{path.name}: missing canonical-v1 Session Result")

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

    if continuation_directives:
        add_result(results, WARN, "Lesson continuation", f"{len(continuation_directives)} session(s) require continuation")
    else:
        add_result(results, PASS, "Lesson continuation", "No incomplete canonical lesson requires continuation")

    if warnings:
        add_result(results, WARN, "Potential evidence conflicts", f"Found {warnings} item(s) needing human review")
    else:
        add_result(results, PASS, "Potential evidence conflicts", "No obvious deterministic conflicts detected")


def validate_protocol_content(results: list[tuple[str, str, str]]) -> None:
    lesson_protocol = read_text(SYSTEM / "Lesson_Protocol.md")
    runtime_rules = read_text(SYSTEM / "Runtime_Rules.md")
    schema = read_text(SYSTEM / "Session_Record_Schema.md")

    required_phrases = [
        "Second Output", "Variation Chain", "Cold Recall", "Transfer", "Second Chance",
        "Mastery Ladder", "Rule новых chunks", "Canonical Session Result",
    ]
    lesson_lower = lesson_protocol.lower()
    phrase_variants = {"Rule новых chunks": ("правило новых chunks", "новых chunks")}

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
        "CONTINUATION_REQUIRED",
        "RESUME_STAGE",
    ]
    runtime_lower = runtime_rules.lower()
    missing_runtime = [p for p in runtime_requirements if p.lower() not in runtime_lower]
    if missing_runtime:
        add_result(results, FAIL, "Runtime gates", "Missing required rule(s): " + ", ".join(missing_runtime))
    else:
        add_result(results, PASS, "Runtime gates", "Critical runtime, canonical-record, and continuation rules present")

    schema_requirements = [
        "record_schema: canonical-v1", "## Session Result", "## Protocol Completion",
        "current_level", "evidence_score", "continuation_required", "continuation_next_stage",
    ]
    schema_lower = schema.lower()
    missing_schema = [p for p in schema_requirements if p.lower() not in schema_lower]
    if missing_schema:
        add_result(results, FAIL, "Session schema", "Missing required schema marker(s): " + ", ".join(missing_schema))
    else:
        add_result(results, PASS, "Session schema", "Canonical-v1 schema and continuation fields present")


def main() -> int:
    results: list[tuple[str, str, str]] = []
    continuation_directives: list[str] = []

    validate_system_files(results)
    validate_protocol_content(results)
    validate_sessions(results, continuation_directives)

    print("Finnish Learning System — Read-only Audit")
    print("=" * 52)
    for status, check, detail in results:
        print(f"[{status}] {check}: {detail}")

    if continuation_directives:
        print("\nCONTINUATION DIRECTIVES")
        print("-" * 52)
        for directive in continuation_directives:
            print(f"CONTINUATION_REQUIRED: YES | {directive}")
        print("ACTION: Load the continuation directive before selecting unrelated new material.")

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
