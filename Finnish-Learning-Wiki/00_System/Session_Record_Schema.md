---
title: Canonical Session Record Schema
type: system-rule
version: canonical-v1
source: 2026-08-20 lesson-record hardening
tags: [session, diary, evidence, mastery, retention, audit]
---

# Canonical Session Record Schema

## Purpose

All new completed lessons must end with one machine-readable, human-readable `Session Result` block. The lesson narrative may remain natural and detailed, but durable state must be recorded in the canonical fields below.

This schema prevents ambiguous wording from being mistaken for a state change and gives the read-only validator stable fields to audit.

## Required marker

New session records use:

```text
record_schema: canonical-v1
```

and contain exactly one final section:

```text
## Session Result
```

Historical/legacy sessions are retained and are not rewritten only to satisfy this schema.

## Canonical fields

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

## Status semantics

- `lesson_status` describes the session itself, not mastery.
- `current_level` is the only canonical field that declares the mastery state of the primary pattern/chunk.
- The word `stable` elsewhere in the lesson narrative is descriptive text, not a state declaration.
- `evidence_score` must describe observed evidence from the lesson; do not infer a score from intention or explanation alone.
- `PROMOTE` or `current_level: STABLE` requires explicit evidence and must not be based only on an immediately corrected answer.
- If there is no meaningful mastery change, record the current level and state that no promotion occurred rather than inventing evidence.

## Multiple chunks

If several chunks require decisions, repeat a complete `Chunk Decisions` block for each chunk. Do not combine unrelated decisions into one sentence.

## No fabricated precision

If a metric was not measured, leave it out or mark it as not measured. Never invent accuracy, fluency, transfer, review dates, or evidence scores merely to complete the template.

## Closing principle

The narrative explains what happened. The canonical `Session Result` explains what the system is allowed to believe after the lesson.
