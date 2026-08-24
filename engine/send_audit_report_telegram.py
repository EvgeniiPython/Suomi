#!/usr/bin/env python3
"""Send the latest machine-readable audit state to Telegram."""
from __future__ import annotations

import argparse
import html
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
    return {"PASS": "🟢", "PASS_WITH_WARNINGS": "🟡", "FAIL": "🔴"}.get(status, "⚪")


def pretty(value: object) -> str:
    if value is None:
        return "—"
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "none"
    return str(value)


def build_message(state: dict) -> str:
    audit_status = str(state.get("audit_status", "UNKNOWN"))
    lines = [
        "🇫🇮 <b>Finnish Learning System — Audit</b>",
        "",
        f"{status_icon(audit_status)} <b>Audit:</b> {html.escape(audit_status)}",
        f"<b>Session type:</b> {html.escape(str(state.get('session_type', 'UNKNOWN')))}",
        f"<b>Protocol:</b> {html.escape(str(state.get('protocol_status', 'UNKNOWN')))}",
        f"<b>Lesson:</b> {html.escape(pretty(state.get('lesson_status')))}",
        f"<b>Validator exit code:</b> {html.escape(pretty(state.get('validator_exit_code')))}",
        "",
        f"<b>Latest session:</b> {html.escape(pretty(state.get('latest_session')))}",
        f"<b>Canonical session:</b> {html.escape(pretty(state.get('latest_canonical_session')))}",
        f"<b>Stages:</b> {state.get('completed_stage_count', 0)}/{state.get('required_stage_count', 0)}",
        f"<b>Continuation:</b> {html.escape(str(state.get('continuation_required', 'UNKNOWN')))}",
        f"<b>Resume stage:</b> {html.escape(pretty(state.get('resume_stage')))}",
    ]

    missing = state.get("missing_stages") or []
    if missing:
        lines.extend(["", "⚠️ <b>Missing stages:</b>", *[f"• {html.escape(str(stage))}" for stage in missing]])

    failures = state.get("failed_checks") or []
    if failures:
        lines.extend(["", "🛠️ <b>Failure diagnostics:</b>"])
        for item in failures:
            check = html.escape(str(item.get("check", "Unknown check")))
            detail = html.escape(str(item.get("detail", "")))
            lines.append(f"• <b>{check}</b>: {detail}")
        lines.append("<b>Action:</b> Fix the failed check(s) above and rerun the audit.")
    else:
        runtime_action = state.get("runtime_action")
        if runtime_action:
            lines.extend(["", f"<b>Action:</b> {html.escape(str(runtime_action))}"])

    generated = state.get("generated_at_utc")
    if generated:
        lines.extend(["", f"<i>Generated: {html.escape(str(generated))}</i>"])
    return "\n".join(lines)


def send_message(token: str, chat_id: str, text: str) -> dict:
    url = TELEGRAM_API.format(token=token)
    body = parse.urlencode({"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": "true"}).encode("utf-8")
    req = request.Request(url, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
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
        send_message(token, chat_id, build_message(state))
        print("Telegram audit report sent successfully")
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
