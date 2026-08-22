---
title: Runtime Rules
type: system-rule
source: 2026-08-22 session-type alignment
 tags: [runtime, lesson, metrics, data-integrity, continuation, session-type]
---

# Runtime Rules

## Session types

```text
FULL_LESSON
RETENTION_SESSION
```

`CONTINUATION` is a runtime mode of the previous session type, not a third type.

### FULL_LESSON required stages

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

### RETENTION_SESSION required stages

```text
retrieval
controlled_speaking
finnish_dialogue
error_repair_second_chance
final_challenge_recall
retention_record
```

`listening_speaking` and `deep_processing` are optional in retention and are not missing merely because they were not used.

## Fast Lesson Runtime

For a normal session, load `Latest_Audit_State.json`, `Current_State.md`, `Today.md`, and the due retention context before starting the lesson. Open full historical logs only when the lesson or audit requires them.

## Runtime decision rules

```text
1. Set one observable Can-Do outcome before the first substantial output.
2. Determine continuation before choosing a new session type.
3. If continuation_required = YES, preserve the previous session_type.
4. Resume from resume_stage and close all missing required stages of that same type.
5. If continuation_required = NO, use Today.session_type when explicitly set; otherwise use RETENTION_SESSION when retention is due, else FULL_LESSON.
6. Preserve unaided first output as evidence.
7. Start from active core chunks before model answers.
8. Use maximum 3 priority repairs in a normal session.
9. Repair before explaining too much.
10. Require Second Output after correction.
11. Use unlabeled Mixed Choice when competing forms exist.
12. Record one Error Cause when repeated-error evidence supports it.
13. Record mastery-state changes only when evidence supports them.
14. Use 0–3 evidence scores for substantial sessions.
15. Record numeric auxiliary metrics only when actually measured.
16. New chunks require stable recall + variation + transfer; active triggers block automatic expansion.
17. New sessions use canonical-v2 and explicit session_type.
18. Mastery state is declared only in canonical current_level.
19. Never silently mark an incomplete session COMPLETED.
20. A RETENTION_SESSION may finish with fewer macro-stages than FULL_LESSON only when its declared retention gate is complete.
```

## Continuation Runtime

When a session stops before all required macro-stages for its type are complete:

```text
1. Save the session as PARTIAL or INTERRUPTED.
2. Record completed_stages and missing_stages for that session_type.
3. Set continuation_required: YES.
4. Set continuation_next_stage to the first missing required stage.
5. On the next start, preserve the same session_type.
6. Resume at the named stage before unrelated new material or a different session type.
7. Only after continuation is complete may normal runtime selection resume.
```

Continuation is a runtime instruction, not a mastery decision.

## Short Recall Completion Gate

Applicable mainly to retrieval/retention work:

```text
1. Use 3–5 active chunks.
2. Preserve first unaided output.
3. Returned watched-pattern error -> priority repair + changed-context rebuild.
4. micro_due -> complete Micro Grammar Repair before changing topic.
5. After repeated target prompts, do closed-text spoken recall unless declined.
6. Mark repairs completed or deferred.
7. Immediate success after a model is repair evidence, not delayed mastery.
```

## Closing Rule

At session close, update the smallest durable state needed for:

```text
session result
protocol completion state
continuation state
mastery state
error watch
retention schedule
progress evidence
```

The session file must contain the canonical Session Result defined in `Session_Record_Schema.md`. Do not create duplicate or conflicting records.

## Audit Rule

Every 14 days, check:

```text
runtime files remain short and current
mastery states agree with lesson evidence
session_type agrees with required/completed stages
delayed retention tasks are not silently dropped
historical numeric metrics are not fabricated
new session records use canonical-v2
continuation directives are not silently dropped
```
