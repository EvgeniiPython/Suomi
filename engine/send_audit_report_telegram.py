#!/usr/bin/env python3
"""Send the latest machine-readable audit state to Telegram.

Configuration is supplied through environment variables so Telegram
credentials never have to be committed to the repository.

Required environment variables:
  TELEGRAM_BOT_TOKEN
  TELEGRAM_CHAT_ID

Usage:
  python engine/send_audit_report_telegram.py
  python engine/send_audit_report_telegram.py --state path/to/state.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib import error, parse, request

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE = ROOT / "Finnish-Learning-Wiki" / "00_System" / "Latest_Audit_State.json"
TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def env_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def status_icon(status: str) -> str:
    return {
        "PASS": "🟢",
        "PASS_WITH_WARNINGS": "🟡",
        "FAIL": "🔴",
    }.get(status, "⚪")


def pretty(value: object) -> str:
    if value is None:
        return "—"
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "none"
    return str(value)


def build_message(state: dict) -> str:
    audit_status = str(state.get("audit_status", "UNKNOWN"))
    icon = status_icon(audit_status)
    protocol = state.get("protocol_status", "UNKNOWN")
    continuation = state.get("continuation_required", "UNKNOWN")
    missing = state.get("missing_stages") or []

    lines = [
        "🇫🇮 <b>Finnish Learning System — Audit</b>",
        "",
        f"{icon} <b>Audit:</b> {audit_status}",
        f"<b>Protocol:</b> {protocol}",
        f"<b>Lesson:</b> {pretty(state.get('lesson_status'))}",
        f"<b>Validator exit code:</b> {pretty(state.get('validator_exit_code'))}",
        "",
        f"<b>Latest session:</b> {pretty(state.get('latest_session'))}",
        f"<b>Canonical session:</b> {pretty(state.get('latest_canonical_session'))}",
        f"<b>Stages:</b> {state.get('completed_stage_count', 0)}/{state.get('required_stage_count', 0)}",
        f"<b>Continuation:</b> {continuation}",
        f"<b>Resume stage:</b> {pretty(state.get('resume_stage'))}",
    ]

    if missing:
        lines.extend(["", "⚠️ <b>Missing stages:</b>", *[f"• {stage}" for stage in missing]])

    runtime_action = state.get("runtime_action")
    if runtime_action:
        lines.extend(["", f"<b>Action:</b> {runtime_action}"])

    generated = state.get("generated_at_utc")
    if generated:
        lines.extend(["", f"<i>Generated: {generated}</i>"])

    return "\n".join(lines)


def send_message(token: str, chat_id: str, text: str) -> dict:
    url = TELEGRAM_API.format(token=token)
    body = parse.urlencode(
        {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": "true",
        }
    ).encode("utf-8")

    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Telegram API HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Telegram API connection failed: {exc}") from exc

    if not payload.get("ok"):
        raise RuntimeError(f"Telegram API error: {payload}")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    args = parser.parse_args()

    try:
        token = env_required("TELEGRAM_BOT_TOKEN")
        chat_id = env_required("TELEGRAM_CHAT_ID")

        if not args.state.exists():
            raise FileNotFoundError(f"Audit state file not found: {args.state}")

        state = json.loads(args.state.read_text(encoding="utf-8"))
        text = build_message(state)
        send_message(token, chat_id, text)
        print("Telegram audit report sent successfully")
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
