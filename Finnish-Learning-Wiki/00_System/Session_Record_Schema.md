---
title: Canonical Session Result Schema
type: system-rule
version: canonical-v1
source: 2026-08-21 schema-validator alignment
tags: [session, diary, evidence, mastery, retention, audit, continuation]
---

# Canonical Session Result Schema

## Purpose

All new lessons must end with exactly one canonical `## Session Result` section. The lesson narrative may remain natural and detailed before that section. Durable state is recorded only inside `Session Result`.

The Python validator checks this exact structure. Markdown protocols remain the source of truth for pedagogical policy.

## Canonical structure

```text
record_schema: canonical-v1

## Session Result
lesson_status: COMPLETED | PARTIAL | INTERRUPTED
primary_skill:

### Evidence
observed:
evidence_score: 0 | 1 | 2 | 3

### Protocol Completion
required_stages: retrieval, listening_speaking, deep_processing, controlled_speaking, finnish_dialogue, error_repair_second_chance, final_challenge_recall, retention_record
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

## Required protocol stages

The eight required macro-stages are:

1. `retrieval`
2. `listening_speaking`
3. `deep_processing`
4. `controlled_speaking`
5. `finnish_dialogue`
6. `error_repair_second_chance`
7. `final_challenge_recall`
8. `retention_record`

Optional techniques are not completion gates.

## Completion semantics

If one or more required stages are missing:

- `lesson_status` must be `PARTIAL` or `INTERRUPTED`;
- `continuation_required` must be `YES`;
- `missing_stages` must exactly equal the required stages not in `completed_stages`;
- `continuation_reason` is required;
- `continuation_next_stage` must be the first missing stage;
- `### Next Step.next_action` is required.

If all required stages are completed:

- `lesson_status` may be `COMPLETED`;
- `continuation_required` must be `NO`;
- `missing_stages` must be empty or `NONE`;
- no `continuation_next_stage` should be declared.

The validator never invents missing evidence or converts `PARTIAL` into `COMPLETED`.

## Evidence and mastery semantics

`evidence_score` means:

- `0` = not yet;
- `1` = assisted / model or heavy hint required;
- `2` = independent in a familiar context;
- `3` = flexible independent use in a changed context.

A score of `3` in one lesson is not stable mastery.

`current_level: CONSOLIDATING` requires evidence of a correct second output and at least one delayed rebuild according to `Mastery_Criteria.md`.

`current_level: STABLE` requires the delayed +1/+3/+7 evidence series, a new personal context, and a passed unlabeled mixed-choice check when competing forms exist. Immediate post-correction success is never sufficient.

The validator checks these prerequisites only when they are explicitly represented in the canonical evidence text. It does not infer pedagogical mastery from prose outside `Session Result`.

## Retention semantics

`SCHEDULED` means a delayed check is planned but not yet passed. `PASSED` requires explicit evidence of the completed retention check. `FAILED` requires explicit evidence of failure. `NOT_APPLICABLE` is reserved for cases where retention genuinely does not apply.

A `PARTIAL` lesson normally remains `SCHEDULED` until delayed evidence exists.

## Continuation directive

For incomplete sessions the validator emits:

```text
CONTINUATION_REQUIRED: YES
RESUME_STAGE: <first missing stage>
MISSING_STAGES: <remaining missing stages>
ACTION: Continue the lesson from RESUME_STAGE before introducing unrelated new material.
```

This is a runtime instruction, not learner evidence.

## Historical records

Legacy records before the canonical-v1 adoption date may remain in their historical format. New records must use the canonical structure above.

## No fabricated precision

Do not invent accuracy, fluency, transfer, review dates, evidence scores, or mastery evidence. If something was not measured, say so explicitly or omit it where the schema permits.
