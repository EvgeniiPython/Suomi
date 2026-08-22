---
title: Canonical Session Result Schema
type: system-rule
version: canonical-v2
source: 2026-08-22 session-type alignment
tags: [session, diary, evidence, mastery, retention, audit, continuation, session-type]
---

# Canonical Session Result Schema

## Purpose

All new lessons must end with exactly one canonical `## Session Result` section. The lesson narrative may remain natural and detailed before that section. Durable state is recorded only inside `Session Result`.

Canonical-v2 adds explicit `session_type` so the runtime and validator know which protocol gates apply.

### Machine source

`00_System/Session_Types_Registry.json` is the single machine-readable source for required and optional macro-stages by session type.

This document is the canonical human-readable documentation of that contract. Do not maintain a second machine-readable stage list elsewhere.

Historical canonical-v1 records remain valid and are treated as `FULL_LESSON` unless a newer canonical record explicitly declares another type.

## Session types

```text
FULL_LESSON
RETENTION_SESSION
```

`CONTINUATION` is not a third session type. It is a runtime mode that resumes the previously declared session type until its required stages are closed.

### FULL_LESSON

A normal Speaking-First lesson. The registry defines all eight required macro-stages:

1. `retrieval`
2. `listening_speaking`
3. `deep_processing`
4. `controlled_speaking`
5. `finnish_dialogue`
6. `error_repair_second_chance`
7. `final_challenge_recall`
8. `retention_record`

### RETENTION_SESSION

A D+1 / D+3 / D+6 / long-term retention session designed to test delayed retrieval and transfer rather than introduce a full new lesson.

The registry defines these six required macro-stages:

1. `retrieval`
2. `controlled_speaking`
3. `finnish_dialogue`
4. `error_repair_second_chance`
5. `final_challenge_recall`
6. `retention_record`

`transfer`, `variation`, `cold_recall`, `mixed_choice`, and `second_chance` are behaviors/evidence inside macro-stages rather than separate completion gates.

`listening_speaking` and `deep_processing` are optional in a `RETENTION_SESSION` when they add real value.

## Canonical structure

```text
record_schema: canonical-v2
session_type: FULL_LESSON | RETENTION_SESSION

## Session Result
lesson_status: COMPLETED | PARTIAL | INTERRUPTED
primary_skill:

### Evidence
observed:
evidence_score: 0 | 1 | 2 | 3

### Protocol Completion
required_stages:
completed_stages:
missing_stages:
continuation_required: YES | NO
continuation_reason:
continuation_next_stage:

### Chunk Decisions
candidate:
decision: ACCEPT | REJECT | DEFER | PROMOTE | KEEP | DEMOTE
reason:
evidence:
next_action:

### Mastery
current_level: ACTIVE | CONSOLIDATING | STABLE | DORMANT
reason:
evidence:

### Retention
status: SCHEDULED | DUE | PASSED | FAILED | NOT_APPLICABLE
next_review:
evidence:

### Errors
recurring:
correction:
cause:
next_action:

### Next Step
next_action:
```

Multiple chunk decisions are represented by repeating the complete `### Chunk Decisions` block. The validator checks each block independently.

## Completion semantics

The `required_stages` field must match the declared `session_type` and the central registry.

If one or more required stages are missing:

- `lesson_status` must be `PARTIAL` or `INTERRUPTED`;
- `continuation_required` must be `YES`;
- `missing_stages` must exactly equal the required stages not in `completed_stages`;
- `continuation_reason` is required;
- `continuation_next_stage` must be the first missing required stage;
- `### Next Step.next_action` is required.

If all required stages are completed:

- `lesson_status` may be `COMPLETED`;
- `continuation_required` must be `NO`;
- `missing_stages` must be empty or `NONE`;
- no `continuation_next_stage` should be declared.

The validator never invents missing evidence or converts `PARTIAL` into `COMPLETED`.

## Continuation semantics

When `continuation_required: YES`, the next runtime must resume the same `session_type` from `continuation_next_stage` before selecting unrelated new material or a new session type.

A continuation does not create a new protocol definition. It closes the unfinished stages of the existing session type.

## Evidence and mastery semantics

`evidence_score` means:

- `0` = not yet;
- `1` = assisted / model or heavy hint required;
- `2` = independent in a familiar context;
- `3` = flexible independent use in a changed context.

A score of `3` in one session is not stable mastery.

`current_level: CONSOLIDATING` requires evidence of a correct second output and at least one delayed rebuild according to `Mastery_Criteria.md`.

`current_level: STABLE` requires the delayed +1/+3/+7 evidence series, a new personal context, and a passed unlabeled mixed-choice check when competing forms exist. Immediate post-correction success is never sufficient.

## Retention semantics

`SCHEDULED` means a delayed check is planned but not yet passed. `PASSED` requires explicit evidence of the completed retention check. `FAILED` requires explicit evidence of failure. `NOT_APPLICABLE` is reserved for cases where retention genuinely does not apply.

A completed `RETENTION_SESSION` normally records the current retention check as `PASSED` or schedules its next delayed check.

## Historical records

Legacy records before canonical-v2 may remain in historical format. Canonical-v1 records remain valid. New records should use canonical-v2 and must explicitly declare `session_type`.

## No fabricated precision

Do not invent accuracy, fluency, transfer, review dates, evidence scores, or mastery evidence. If something was not measured, say so explicitly or omit it where the schema permits.
