---
title: Runtime Rules
type: system-rule
source: archive recovery + 2026-08-20 continuation protocol
tags: [runtime, lesson, metrics, data-integrity, continuation]
---

# Runtime Rules

## Fast Lesson Runtime

For a normal lesson, load the current state, active focus, due retention, and retention rules first. Open full historical logs only when the lesson or audit requires them.

## Lesson Runtime Rules

```text
1. Set one observable Can-Do outcome before the first substantial output.
2. Start from active core chunks before showing model answers.
3. Preserve unaided first output as evidence.
4. Keep a live repair ledger and link repeated conceptual errors to Trigger Watch.
5. Use maximum 3 priority repairs in a normal lesson.
6. Repair before explaining too much.
7. Require Second Output after correction.
8. Use unlabeled Mixed Choice when competing forms exist.
9. Record one Error Cause when repeated-error evidence supports it.
10. End substantial lessons with Spoken Recall and Final Recall.
11. Record mastery-state changes only when evidence supports them.
12. Use 0–3 evidence scores for substantial lessons and audits.
13. Record numeric auxiliary metrics only when actually measured.
14. Complete required trigger actions before changing topic.
15. New chunks require stable recall + variation + transfer; active triggers block automatic expansion.
16. New completed lessons must use record_schema: canonical-v1 and finish with one canonical Session Result block.
17. Mastery state is declared only in the canonical current_level field, not by incidental prose.
18. PROMOTE and current_level: STABLE require explicit evidence; immediate post-correction success is not delayed mastery.
19. Every new session must record Protocol Completion. The validator is authoritative for detecting missing required macro-stages.
20. If CONTINUATION_REQUIRED is YES, the next lesson resumes from RESUME_STAGE before unrelated new material is introduced.
21. A partial or interrupted lesson is valid historical evidence when saved correctly; it is not treated as a failed lesson.
22. Never silently mark an incomplete lesson COMPLETED merely because the record was saved.
```

## Required Protocol Completion Stages

For a normal full lesson, the runtime tracks these eight macro-stages:

```text
retrieval
listening_speaking
deep_processing
controlled_speaking
finnish_dialogue
error_repair_second_chance
final_challenge_recall
retention_record
```

Optional techniques such as Micro-Shadowing are not completion gates.

## Continuation Runtime

When a lesson stops before all required macro-stages are complete:

```text
1. Save the lesson normally.
2. Set lesson_status to PARTIAL or INTERRUPTED.
3. Record completed_stages and missing_stages.
4. Set continuation_required: YES.
5. Set continuation_next_stage to the first unfinished stage.
6. Explain the reason for stopping.
7. Give a concrete Next Step action.
8. The validator emits CONTINUATION_REQUIRED: YES.
9. On the next lesson, load that continuation directive before selecting new material.
10. Resume at the named stage; do not replay the entire previous lesson unless evidence shows that recall has degraded.
11. After continuation, record the new session separately. Never rewrite the historical session to make it look complete.
```

The continuation signal is a runtime instruction, not a mastery decision.

## Short Recall Completion Gate

```text
1. Use 3–5 active chunks.
2. Preserve first unaided output.
3. Returned watched-pattern error -> priority repair + changed-context rebuild.
4. micro_due -> complete Micro Grammar Repair before changing topic.
5. After repeated target prompts, do closed-text spoken recall unless declined.
6. Mark each repair completed or deferred.
7. Immediate success after a model is repair evidence, not delayed mastery.
```

## Closing Rule

At lesson close, update the smallest set of durable files needed for:

```text
lesson result
protocol completion state
continuation state
mastery state
error watch
retention schedule
progress evidence
```

For new completed lessons, the lesson file itself must also contain the canonical `Session Result` block defined in `Session_Record_Schema.md`. Do not create duplicate or conflicting records.

## Audit Rule

Every 14 days, check:

```text
runtime files remain short and current
mastery states agree with lesson evidence
trigger counts are consistent
delayed retention tasks are not silently dropped
historical numeric metrics are not fabricated
new session records use canonical-v1
continuation directives are not silently dropped
```
