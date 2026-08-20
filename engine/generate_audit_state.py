#!/usr/bin/env python3
"""Generate a small machine-readable audit state for runtime consumers.

The validator remains read-only with respect to learner records. This helper
only materializes its audit result into the dedicated runtime-state file when
called by CI.
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
STAGES = (
    "retrieval", "listening_speaking", "deep_processing", "controlled_speaking",
    "finnish_dialogue", "error_repair_second_chance", "final_challenge_recall",
    "retention_record",
)


def field(text: str, name: str) -> str | None:
    m = re.search(rf"(?im)^\s*{re.escape(name)}\s*:\s*([^\n#]+?)\s*$", text)
    return m.group(1).strip() if m else None


def latest_session():
    files = sorted(SESSIONS.glob("*.md"), reverse=True)
    for path in files:
        text = path.read_text(encoding="utf-8")
        if "record_schema: canonical-v1" in text.lower() and "## session result" in text.lower():
            return path, text
    return None, ""


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

    path, text = latest_session()
    missing = list_field(text, "missing_stages")
    completed = list_field(text, "completed_stages")
    continuation = (field(text, "continuation_required") or "NO").upper()
    resume = (field(text, "continuation_next_stage") or "NONE").lower()
    lesson_status = (field(text, "lesson_status") or "UNKNOWN").upper()

    state = {
        "schema": "audit-state-v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "audit_status": audit_status,
        "validator_exit_code": args.exit_code,
        "latest_session": path.name if path else None,
        "lesson_status": lesson_status,
        "protocol_status": "COMPLETED" if not missing else "PARTIAL",
        "required_stage_count": len(STAGES),
        "completed_stage_count": len(completed),
        "missing_stages": missing,
        "continuation_required": continuation,
        "resume_stage": resume,
        "runtime_action": (
            "Continue the lesson from RESUME_STAGE before unrelated new material."
            if continuation == "YES" else
            "No continuation required; follow normal runtime selection."
        ),
    }

    OUT.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(state, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
