---
title: Runtime Rules
type: system-rule
source: 2026-08-22 session-type alignment
---

# Runtime Rules

## System responsibilities

- `SESSION_BOOT.md` performs runtime routing.
- `Session_Types_Registry.json` defines required and optional macro-stages by session type.
- `Lesson_Protocol.md` defines the pedagogical route.
- `Latest_Audit_State.json` is the machine-readable continuation/audit state.
- `Current_State.md`, `Today.md`, and `Retention_Dashboard.md` are current-state inputs; they do not redefine protocol rules.

## Continuation

When `continuation_required = YES`:

1. Preserve the previous session type.
2. Resume from `resume_stage`.
3. Close the remaining required stages for that same type.
4. Do not switch to retention or unrelated new material before continuation is closed.
5. Record the continuation result as a new Session Record; do not rewrite the historical record.

Continuation is a runtime mode, not a session type.

## Session integrity

- Every new session uses `YYYY-MM-DD_Session_Record.md`.
- New records use `record_schema: canonical-v2` and explicitly declare `session_type`.
- The canonical Session Result is the durable session record.
- A saved lesson is not automatically a completed lesson.
- `PARTIAL` / `INTERRUPTED` lessons require a valid continuation directive when required stages remain.

## Pedagogical boundaries

Do not duplicate or override the detailed teaching route here. Follow `Lesson_Protocol.md` for:

- attempts and correction;
- variation, cold recall, and transfer;
- Finnish dialogue;
- Second Chance;
- listening and deep processing;
- mastery and new-chunk rules.

## Data integrity

Before changing a durable file:

```text
Read → Compare → Merge/Update → Write → Verify
```

Do not silently overwrite conflicting state. Historical records remain historical.

## Close

After a session, update only the durable state required for:

```text
session result
continuation state
mastery state
error watch
retention schedule
progress evidence
```
