#!/usr/bin/env python3
"""Generate machine-readable audit state for runtime consumers.

Canonical-v1 records are retained as historical FULL_LESSON records. New
canonical-v2 records declare an explicit session_type so required stages are
computed from the session route rather than from one global eight-stage list.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "Finnish-Learning-Wiki"
SESSIONS = WIKI / "03_Sessions"
OUT = WIKI / "00_System" / "Latest_Audit_State.json"

FULL_STAGES = (
    "retrieval", "listening_speaking", "deep_processing", "controlled_speaking",
    "finnish_dialogue", "error_repair_second_chance", "final_challenge_recall",
    "retention_record",
)
RETENTION_STAGES = (
    "retrieval", "controlled_speaking", "finnish_dialogue",
    "error_repair_second_chance", "final_challenge_recall", "retention_record",
)
STAGES_BY_TYPE = {
    "FULL_LESSON": FULL_STAGES,
    "RETENTION_SESSION": RETENTION_STAGES,
}
SESSION_RECORD_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_Session_Record\.md$")
SCHEMA_RE = re.compile(r"record_schema:\s*canonical-v(1|2)", re.IGNORECASE)


def field(text: str, name: str) -> str | None:
    m = re.search(rf"(?im)^\s*{re.escape(name)}\s*:\s*([^\n#]+?)\s*$", text)
    return m.group(1).strip() if m else None


def session_info(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    schema_match = SCHEMA_RE.search(text)
    schema = f"canonical-v{schema_match.group(1)}" if schema_match else None
    canonical = schema is not None and "## session result" in text.lower()
    session_type = (field(text, "session_type") or "FULL_LESSON").upper()
    if session_type not in STAGES_BY_TYPE:
        session_type = "FULL_LESSON"
    return {
        "path": path,
        "text": text,
        "schema": schema,
        "canonical": canonical,
        "eligible": canonical,
        "session_type": session_type,
    }


def latest_sessions():
    latest = None
    latest_canonical = None
    for path in sorted(SESSIONS.glob("*.md"), key=lambda p: p.name, reverse=True):
        info = session_info(path)
        if latest is None:
            latest = info
        if latest_canonical is None and SESSION_RECORD_RE.match(path.name) and info["eligible"]:
            latest_canonical = info
    return latest, latest_canonical


def list_field(text: str, name: str) -> list[str]:
    value = field(text, name)
    if not value or value.upper() in {"NONE", "N/A"}:
        return []
    return [x.strip().lower() for x in re.split(r"[,;]", value) if x.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True)
    parser.add_argument("--exit-code", type=int, required=True)
    args = parser.parse_args()

    log = Path(args.log).read_text(encoding="utf-8", errors="replace")
    if args.exit_code != 0:
        audit_status = "FAIL"
    elif "WARNING" in log:
        audit_status = "PASS_WITH_WARNINGS"
    else:
        audit_status = "PASS"

    latest, canonical = latest_sessions()

    if canonical is None:
        state = {
            "schema": "audit-state-v3",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "audit_status": audit_status,
            "validator_exit_code": args.exit_code,
            "latest_session": latest["path"].name if latest else None,
            "latest_session_schema_status": latest["schema"].upper().replace("-", "_") if latest else "NONE",
            "latest_canonical_session": None,
            "session_type": latest["session_type"] if latest else None,
            "lesson_status": "UNKNOWN",
            "protocol_status": "UNKNOWN",
            "required_stage_count": 0,
            "completed_stage_count": 0,
            "missing_stages": [],
            "continuation_required": "UNKNOWN",
            "resume_stage": "NONE",
            "runtime_action": (
                "Create a canonical-v2 Session Record before evaluating completion."
                if latest else "Create a canonical-v2 Session Record before evaluating completion."
            ),
        }
    else:
        text = canonical["text"]
        session_type = canonical["session_type"]
        expected = list(STAGES_BY_TYPE[session_type])
        missing = list_field(text, "missing_stages")
        completed = list_field(text, "completed_stages")
        continuation = (field(text, "continuation_required") or "NO").upper()
        resume = (field(text, "continuation_next_stage") or "NONE").lower()
        lesson_status = (field(text, "lesson_status") or "UNKNOWN").upper()
        state = {
            "schema": "audit-state-v3",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "audit_status": audit_status,
            "validator_exit_code": args.exit_code,
            "latest_session": latest["path"].name if latest else canonical["path"].name,
            "latest_session_schema_status": latest["schema"].upper().replace("-", "_") if latest else "NONE",
            "latest_canonical_session": canonical["path"].name,
            "session_type": session_type,
            "lesson_status": lesson_status,
            "protocol_status": "COMPLETED" if not missing else "PARTIAL",
            "required_stage_count": len(expected),
            "completed_stage_count": len(completed),
            "required_stages": expected,
            "missing_stages": missing,
            "continuation_required": continuation,
            "resume_stage": resume,
            "runtime_action": (
                "Continue the previous session from RESUME_STAGE before selecting a new session type."
                if continuation == "YES"
                else f"Run normal {session_type} runtime selection."
            ),
        }

    OUT.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(state, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
