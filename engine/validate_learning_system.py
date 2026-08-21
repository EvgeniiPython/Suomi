#!/usr/bin/env python3
"""Read-only structural validator for the Finnish Learning Wiki.

The Markdown protocols remain the pedagogical source of truth. This validator
checks that canonical-v1 session records are structurally and logically
consistent with those rules; it does not invent mastery decisions.
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
    "Lesson_Protocol.md", "Runtime_Rules.md", "Current_State.md",
    "Mastery_Criteria.md", "Metrics_And_Audit.md", "Decision_Gates.md",
    "Prior_Art_Search.md", "Lesson_Diary_Protocol.md",
    "Session_Record_Schema.md", "Audit_Protocol.md",
}
PASS, WARN, FAIL = "PASS", "WARNING", "FAIL"
CANONICAL_REQUIRED_FROM = date(2026, 8, 21)
REQUIRED_STAGES = (
    "retrieval", "listening_speaking", "deep_processing", "controlled_speaking",
    "finnish_dialogue", "error_repair_second_chance", "final_challenge_recall",
    "retention_record",
)
VALID_STATUS = {"COMPLETED", "PARTIAL", "INTERRUPTED"}
VALID_LEVELS = {"ACTIVE", "CONSOLIDATING", "STABLE", "DORMANT"}
VALID_RETENTION = {"SCHEDULED", "DUE", "PASSED", "FAILED", "NOT_APPLICABLE"}
VALID_CONTINUATION = {"YES", "NO"}

# Session records are the only files validated against canonical-v1. Other
# documents may live in 03_Sessions (for example Closure_Checklist) but are
# supporting artifacts, not session records, and must not fail the session
# schema gate.
SESSION_RECORD_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_Session_Record\.md$")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def add_result(results, status, check, detail):
    results.append((status, check, detail))


def canonical_value(text: str, field: str) -> str | None:
    m = re.search(rf"(?im)^\s*{re.escape(field)}\s*:\s*([^\n#]+?)\s*$", text)
    return m.group(1).strip().upper() if m else None


def field_value(text: str, field: str) -> str | None:
    m = re.search(rf"(?im)^\s*{re.escape(field)}\s*:\s*(.+?)\s*$", text)
    return m.group(1).strip() if m else None


def list_field(text: str, field: str) -> list[str]:
    value = field_value(text, field)
    if not value or value.upper() in {"NONE", "N/A", "NOT_APPLICABLE"}:
        return []
    return [x.strip().lower() for x in re.split(r"[,;]", value) if x.strip()]


def subsection(text: str, heading: str) -> str:
    m = re.search(rf"(?is)^### {re.escape(heading)}\s*$", text, re.MULTILINE)
    if not m:
        return ""
    tail = text[m.end():]
    n = re.search(r"(?m)^### (?!#)", tail)
    return tail[:n.start()] if n else tail


def extract_session_date(path: Path, text: str) -> date | None:
    m = re.search(r"(20\d{2})[-_](\d{2})[-_](\d{2})", path.name)
    if not m:
        m = re.search(r"^# .*?(20\d{2})[-./](\d{1,2})[-./](\d{1,2})", text, re.MULTILINE)
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def validate_protocol(block: str):
    problems = []
    required = list_field(block, "required_stages")
    completed = set(list_field(block, "completed_stages"))
    declared_missing = set(list_field(block, "missing_stages"))
    continuation = canonical_value(block, "continuation_required")
    resume = field_value(block, "continuation_next_stage")
    if set(required) != set(REQUIRED_STAGES):
        problems.append("required_stages must equal the canonical eight stages")
    unknown = sorted(completed - set(REQUIRED_STAGES))
    if unknown:
        problems.append("unknown completed stage(s): " + ", ".join(unknown))
    missing = [s for s in REQUIRED_STAGES if s not in completed]
    if declared_missing != set(missing):
        problems.append("missing_stages does not match completed_stages")
    if continuation not in VALID_CONTINUATION:
        problems.append("invalid or missing continuation_required")
    if missing:
        if continuation != "YES":
            problems.append("incomplete protocol requires continuation_required: YES")
        if not resume or resume.strip().lower() != missing[0]:
            problems.append("continuation_next_stage must be the first missing stage")
        if not field_value(block, "continuation_reason"):
            problems.append("incomplete protocol requires continuation_reason")
    else:
        if continuation != "NO":
            problems.append("completed protocol requires continuation_required: NO")
        if resume and resume.strip().upper() not in {"NONE", "N/A"}:
            problems.append("completed protocol must not declare continuation_next_stage")
    return problems, missing, continuation


def validate_canonical(text: str):
    problems = []
    if "record_schema: canonical-v1" not in text.lower():
        problems.append("missing record_schema: canonical-v1")
    result_positions = list(re.finditer(r"(?im)^## Session Result\s*$", text))
    if len(result_positions) != 1:
        problems.append("canonical-v1 requires exactly one final ## Session Result section")
        return problems
    result = text[result_positions[0].end():]
    if re.search(r"(?m)^## ", result):
        problems.append("Session Result must contain all canonical data; no sibling ## sections may follow it")
    required_subsections = ("Evidence", "Protocol Completion", "Chunk Decisions", "Mastery", "Retention", "Errors", "Next Step")
    for name in required_subsections:
        if not re.search(rf"(?im)^### {re.escape(name)}\s*$", result):
            problems.append(f"Session Result missing ### {name}")
    status = canonical_value(result, "lesson_status")
    if status not in VALID_STATUS:
        problems.append("invalid or missing lesson_status")
    score = field_value(subsection(result, "Evidence"), "evidence_score")
    if score not in {"0", "1", "2", "3"}:
        problems.append("Evidence requires evidence_score 0-3")
    level = canonical_value(subsection(result, "Mastery"), "current_level")
    if level not in VALID_LEVELS:
        problems.append("invalid or missing current_level")
    retention = subsection(result, "Retention")
    retention_status = canonical_value(retention, "status")
    if retention_status not in VALID_RETENTION:
        problems.append("invalid or missing Retention status")
    protocol = subsection(result, "Protocol Completion")
    p, missing, _ = validate_protocol(protocol)
    problems.extend(p)
    if status in {"PARTIAL", "INTERRUPTED"} and not field_value(subsection(result, "Next Step"), "next_action"):
        problems.append("partial/interrupted lesson requires Next Step.next_action")
    if missing and status == "COMPLETED":
        problems.append("lesson_status cannot be COMPLETED while required stages are missing")
    mastery = subsection(result, "Mastery")
    mastery_evidence = field_value(mastery, "evidence") or ""
    if level == "STABLE":
        if "delayed" not in mastery_evidence.lower():
            problems.append("STABLE requires delayed evidence to be named")
        if "mixed-choice" not in mastery_evidence.lower() and "mixed choice" not in mastery_evidence.lower():
            problems.append("STABLE requires unlabeled mixed-choice evidence to be named")
    evidence = subsection(result, "Evidence")
    observed = field_value(evidence, "observed") or ""
    score_int = int(score)
    combined = (observed + " " + mastery_evidence).lower()
    if score_int >= 2 and "independent" not in combined:
        problems.append("evidence_score >= 2 requires explicit independent evidence")
    if score_int == 3 and not any(x in combined for x in ("changed context", "changed-context", "transfer")):
        problems.append("evidence_score 3 requires changed-context or transfer evidence")
    return problems


def validate_system_files(results):
    existing = {p.name for p in SYSTEM.glob("*.md")}
    missing = sorted(REQUIRED_SYSTEM_FILES - existing)
    add_result(results, FAIL if missing else PASS, "Required system protocols", "Missing: " + ", ".join(missing) if missing else "All required files are present")


def validate_sessions(results, directives):
    files = sorted(p for p in SESSIONS.glob("*.md") if SESSION_RECORD_RE.match(p.name)) if SESSIONS.exists() else []
    if not files:
        add_result(results, WARN, "Session records", "No canonical Session_Record files found")
        return
    malformed = 0
    failures = []
    for path in files:
        text = read_text(path)
        lower = text.lower()
        session_date = extract_session_date(path, text)
        if "record_schema: canonical-v1" in lower:
            problems = validate_canonical(text)
            if problems and session_date and session_date >= CANONICAL_REQUIRED_FROM:
                failures.append(f"{path.name}: " + "; ".join(problems))
            if "continuation_required: yes" in lower:
                block = subsection(text, "Protocol Completion")
                resume = field_value(block, "continuation_next_stage")
                missing = list_field(block, "missing_stages")
                directives.append(f"{path.name}: RESUME_STAGE={resume}; MISSING_STAGES={','.join(missing)}")
        else:
            if session_date and session_date >= CANONICAL_REQUIRED_FROM:
                failures.append(f"{path.name}: missing canonical-v1 Session Result")
        if not re.search(r"^# .*20\d{2}", text, re.MULTILINE):
            malformed += 1
    add_result(results, FAIL if malformed else PASS, "Session structure", f"Checked {len(files)} Session_Record file(s)")
    add_result(results, FAIL if failures else PASS, "Canonical session records", " | ".join(failures) if failures else "All applicable canonical-v1 Session_Record files are structurally consistent")
    add_result(results, WARN if directives else PASS, "Lesson continuation", f"{len(directives)} session(s) require continuation" if directives else "No continuation directives")


def main() -> int:
    results = []
    directives = []
    validate_system_files(results)
    validate_sessions(results, directives)
    for status, check, detail in results:
        print(f"[{status}] {check}: {detail}")
    failures = sum(status == FAIL for status, _, _ in results)
    warnings = sum(status == WARN for status, _, _ in results)
    print(f"SUMMARY: FAIL={failures} WARNING={warnings} PASS={len(results)-failures-warnings}")
    if directives:
        print("CONTINUATION DIRECTIVES:")
        for directive in directives:
            print(directive)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
