---
title: Canonical Session Record Schema
type: system-rule
version: canonical-v1
source: 2026-08-20 lesson-record hardening
tags: [session, diary, evidence, mastery, retention, audit, continuation]
---

# Canonical Session Record Schema

## Purpose

All new lessons must end with one machine-readable, human-readable `Session Result` block. The lesson narrative may remain natural and detailed, but durable state must be recorded in the canonical fields below.

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

## Protocol Completion
required_stages: retrieval, listening_speaking, deep_processing, controlled_speaking, finnish_dialogue, error_repair_second_chance, final_challenge_recall, retention_record
completed_stages:
missing_stages:
continuation_required: YES | NO
continuation_reason:
continuation_next_stage:

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

## Protocol Completion semantics

The canonical protocol has eight required macro-stages:

1. `retrieval`
2. `listening_speaking`
3. `deep_processing`
4. `controlled_speaking`
5. `finnish_dialogue`
6. `error_repair_second_chance`
7. `final_challenge_recall`
8. `retention_record`

These are the minimum completion gates for a normal full lesson. Optional techniques such as Micro-Shadowing are not required completion stages.

The lesson record must explicitly state which required stages were completed. The validator compares `completed_stages` with `required_stages` and derives whether continuation is required.

If one or more required stages are missing:

- `lesson_status` must be `PARTIAL` or `INTERRUPTED`;
- `continuation_required` must be `YES`;
- `missing_stages` must list the unfinished stages;
- `continuation_reason` must explain why the lesson stopped;
- `continuation_next_stage` must identify the first stage to resume;
- `Next Step.next_action` must tell the next lesson what to do.

If all required stages are completed:

- `lesson_status` may be `COMPLETED`;
- `continuation_required` must be `NO`;
- `missing_stages` should be empty or `NONE`.

The validator does not silently convert a partial lesson into a completed one and does not invent missing stages.

## Continuation directive

When validation detects missing required stages, it emits a machine-readable continuation signal:

```text
CONTINUATION_REQUIRED: YES
RESUME_STAGE: <first missing stage>
MISSING_STAGES: <remaining missing stages>
ACTION: Continue the lesson from RESUME_STAGE before introducing unrelated new material.
```

This signal is an instruction to the next lesson runtime, not a new learner result. The original session record remains unchanged.

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

The narrative explains what happened. The canonical `Session Result` explains what the system is allowed to believe after the lesson. If the lesson is incomplete, the record also tells the next runtime exactly where to continue.
