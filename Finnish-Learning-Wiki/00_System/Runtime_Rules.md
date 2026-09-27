---
title: Runtime Rules
type: system-rule
source: 2026-08-22 session-type alignment
---

# Runtime Rules

## System responsibilities

- SESSION_BOOT.md performs runtime routing.
- Session_Types_Registry.json defines required and optional macro-stages by session type.
- Lesson_Protocol.md defines the pedagogical route.
- Latest_Audit_State.json is the machine-readable continuation/audit state.
- Current_State.md, Today.md, and Retention_Dashboard.md are current-state inputs; they do not redefine protocol rules.

## Continuation

When continuation_required = YES:
1. Preserve the previous session type.
2. Resume from resume_stage.
3. Close the remaining required stages for that same type.
4. Do not switch to retention or unrelated new material before continuation is closed.
5. Record the continuation result as a new Session Record; do not rewrite the historical record.

Continuation is a runtime mode, not a session type.

## Session integrity

- Every new session uses YYYY-MM-DD_Session_Record.md.
- New records use record_schema: canonical-v2 and explicitly declare session_type.
- The canonical Session Result is the durable session record.
- A saved lesson is not automatically a completed lesson.
- PARTIAL / INTERRUPTED lessons require a valid continuation directive when required stages remain.

## Acquisition routing

Runtime must keep two decisions separate:

review_priority = urgency of existing-material review
acquisition_eligibility = whether new chunks/patterns may be introduced

Do not infer acquisition_eligibility = BLOCKED merely because a pattern is still consolidating.

Default behavior:
- consolidating + broadly functional recall + repairable local errors -> acquisition may remain ALLOWED
- isolated spelling/surface slip -> no acquisition block
- repeated meaningful conceptual failure / active micro-focused trigger -> reduce or defer acquisition according to Lesson_Protocol.md

Old weak/consolidating material continues to be interleaved with new material; 100% automation is not a prerequisite.

## Candidate Chunk Bank

Candidate_Chunks.md is the staging bank for potentially useful future material.

1. Newly discovered words, chunks, collocations, and grammar patterns do not enter Active_Vocabulary.md automatically.
2. Record useful but unselected material in Candidate_Chunks.md.
3. Check whether the user already knows a candidate before selecting it.
4. Promote only selected, high-value candidates to active learning.
5. Candidate accumulation does not prevent acquisition.
6. A candidate can remain in the bank until there is a good reason to promote it.

Lifecycle: candidate -> selected -> active -> consolidating -> stable -> dormant.

The candidate bank is a reservoir, not a second active vocabulary list.

## Pedagogical boundaries

Do not duplicate or override the detailed teaching route here. Follow Lesson_Protocol.md for attempts and correction, variation, cold recall, transfer, Finnish dialogue, Second Chance, listening, deep processing, mastery, new-chunk rules, and candidate selection.

## Data integrity

Before changing a durable file:
Read -> Compare -> Merge/Update -> Write -> Verify

Do not silently overwrite conflicting state. Historical records remain historical.

## Close

After a session, update only the durable state required for session result, continuation state, mastery state, error watch, retention schedule, progress evidence, and candidate discoveries.
