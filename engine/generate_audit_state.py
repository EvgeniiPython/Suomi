#!/usr/bin/env python3
"""Generate machine-readable audit state for runtime consumers."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "Finnish-Learning-Wiki"
SESSIONS = WIKI / "03_Sessions"
SYSTEM = WIKI / "00_System"
REGISTRY_PATH = SYSTEM / "Session_Types_Registry.json"
OUT = SYSTEM / "Latest_Audit_State.json"
SESSION_RECORD_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_Session_Record\.md$")
SCHEMA_RE = re.compile(r"record_schema:\s*canonical-v(1|2)", re.IGNORECASE)
FAIL_RE = re.compile(r"^\[FAIL\]\s+([^:]+):\s*(.*)$", re.MULTILINE)


def load_registry() -> dict[str, dict[str, list[str]]]:
    raw = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    sessions = raw.get("sessions")
    if not isinstance(sessions, dict) or not sessions:
        raise RuntimeError("Session_Types_Registry.json must contain a non-empty 'sessions' object")
    registry: dict[str, dict[str, list[str]]] = {}
    for session_type, spec in sessions.items():
        required = spec.get("required_stages")
        optional = spec.get("optional_stages", [])
        if not isinstance(required, list) or not all(isinstance(x, str) for x in required):
            raise RuntimeError(f"Registry entry {session_type} has invalid required_stages")
        if not isinstance(optional, list) or not all(isinstance(x, str) for x in optional):
            raise RuntimeError(f"Registry entry {session_type} has invalid optional_stages")
        registry[session_type] = {"required_stages": required, "optional_stages": optional}
    return registry


def field(text: str, name: str) -> str | None:
    m = re.search(rf"(?im)^\s*{re.escape(name)}\s*:\s*([^\n#]+?)\s*$", text)
    return m.group(1).strip() if m else None


def session_info(path: Path, registry: dict[str, dict[str, list[str]]]) -> dict:
    text = path.read_text(encoding="utf-8")
    schema_match = SCHEMA_RE.search(text)
    schema = f"canonical-v{schema_match.group(1)}" if schema_match else None
    canonical = schema is not None and "## session result" in text.lower()
    session_type = (field(text, "session_type") or "FULL_LESSON").upper()
    if session_type not in registry:
        session_type = "FULL_LESSON"
    return {"path": path, "text": text, "schema": schema, "canonical": canonical, "eligible": canonical and SESSION_RECORD_RE.match(path.name) is not None, "session_type": session_type}


def latest_sessions(registry):
    latest = None
    latest_canonical = None
    for path in sorted(SESSIONS.glob("*.md"), key=lambda p: p.name, reverse=True):
        info = session_info(path, registry)
        if latest is None:
            latest = info
        if latest_canonical is None and info["eligible"]:
            latest_canonical = info
    return latest, latest_canonical


def list_field(text: str, name: str) -> list[str]:
    value = field(text, name)
    if not value or value.upper() in {"NONE", "N/A"}:
        return []
    return [x.strip().lower() for x in re.split(r"[,;]", value) if x.strip()]


def extract_failures(log: str) -> list[dict[str, str]]:
    return [{"check": check.strip(), "detail": detail.strip()} for check, detail in FAIL_RE.findall(log)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True)
    parser.add_argument("--exit-code", type=int, required=True)
    args = parser.parse_args()

    registry = load_registry()
    log = Path(args.log).read_text(encoding="utf-8", errors="replace")
    failures = extract_failures(log)
    if args.exit_code != 0:
        audit_status = "FAIL"
    elif "WARNING" in log:
        audit_status = "PASS_WITH_WARNINGS"
    else:
        audit_status = "PASS"

    latest, canonical = latest_sessions(registry)
    base = {
        "schema": "audit-state-v4",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "audit_status": audit_status,
        "validator_exit_code": args.exit_code,
        "failure_count": len(failures),
        "failed_checks": failures,
    }

    if canonical is None:
        state = {
            **base,
            "latest_session": latest["path"].name if latest else None,
            "latest_session_schema_status": latest["schema"].upper().replace("-", "_") if latest else "NONE",
            "latest_canonical_session": None,
            "session_type": latest["session_type"] if latest else None,
            "lesson_status": "UNKNOWN",
            "protocol_status": "UNKNOWN",
            "required_stage_count": 0,
            "completed_stage_count": 0,
            "required_stages": [],
            "missing_stages": [],
            "continuation_required": "UNKNOWN",
            "resume_stage": "NONE",
            "runtime_action": "Create a canonical-v2 Session Record before evaluating completion.",
        }
    else:
        text = canonical["text"]
        session_type = canonical["session_type"]
        required_stages = list(registry[session_type]["required_stages"])
        missing = list_field(text, "missing_stages")
        completed = list_field(text, "completed_stages")
        continuation = (field(text, "continuation_required") or "NO").upper()
        resume = (field(text, "continuation_next_stage") or "NONE").lower()
        lesson_status = (field(text, "lesson_status") or "UNKNOWN").upper()
        state = {
            **base,
            "latest_session": latest["path"].name if latest else canonical["path"].name,
            "latest_session_schema_status": latest["schema"].upper().replace("-", "_") if latest else "NONE",
            "latest_canonical_session": canonical["path"].name,
            "session_type": session_type,
            "lesson_status": lesson_status,
            "protocol_status": "COMPLETED" if not missing else "PARTIAL",
            "required_stage_count": len(required_stages),
            "completed_stage_count": len(completed),
            "required_stages": required_stages,
            "missing_stages": missing,
            "continuation_required": continuation,
            "resume_stage": resume,
            "runtime_action": "Continue the previous session from RESUME_STAGE before selecting a new session type." if continuation == "YES" else f"Run normal {session_type} runtime selection.",
        }

    OUT.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(state, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
