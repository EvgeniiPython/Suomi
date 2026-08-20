---
title: Lesson Diary Protocol
type: system-rule
source: 2026-08-20 agent-architecture upgrade
tags: [diary, session, decisions, memory, audit]
---

# Lesson Diary Protocol

## Purpose

A lesson record should preserve not only what happened, but also the important decisions that explain why the learning system changed (or did not change) after the lesson.

The normal session file remains the main human-readable lesson record. A diary adds decision traceability without replacing the existing session protocol.

## Minimum Diary Fields

```text
Lesson
Date
Primary Can-Do
Initial plan
Observed evidence
Priority errors
Repairs performed
Important deviations from plan
Chunk candidates and decisions
Mastery decisions
Retention decisions
Next actions
```

## Canonical closing record

Starting with the canonical-v1 protocol, every new completed lesson must finish with a structured `## Session Result` section using `record_schema: canonical-v1`.

The narrative portion of the lesson may use normal prose. The final durable state must not rely on prose wording alone.

Required canonical fields:

```text
record_schema: canonical-v1
lesson_status: COMPLETED | PARTIAL | INTERRUPTED
primary_skill:

## Evidence
observed:
evidence_score: 0 | 1 | 2 | 3

## Chunk Decisions
candidate:
decision: ACCEPT | REJECT | DEFER | PROMOTE | KEEP | DEMOTE
reason:
evidence:
next_action:

## Mastery
current_level: ACTIVE | CONSOLIDATING | STABLE | DORMANT
reason:
evidence:

## Retention
status: SCHEDULED | DUE | PASSED | FAILED | NOT_APPLICABLE
next_review:
evidence:

## Errors
recurring:
correction:
cause:
next_action:

## Next Step
next_action:
```

See `Session_Record_Schema.md` for the authoritative field semantics and validation rules.

## Decision Record

For every meaningful state-changing decision, record:

```text
object:
decision: ACCEPT | REJECT | DEFER | PROMOTE | KEEP | DEMOTE
reason:
evidence:
next_action:
```

## Rejected Decisions

Do not silently discard rejected candidates. When a candidate is educationally plausible but not accepted, preserve the reason briefly.

Examples:

```text
candidate: new chunk X
decision: DEFER
reason: transfer evidence insufficient
next_action: revisit after next recall cycle
```

## Deviation Rule

If the actual lesson diverged materially from the planned sequence, record the deviation and whether it affected mastery, retention, or chunk decisions.

## Closing Rule

At lesson close, the diary must remain concise enough to audit. Prefer evidence and decisions over narrative commentary. Do not use narrative mentions of `stable` as a substitute for the canonical `current_level` field.
