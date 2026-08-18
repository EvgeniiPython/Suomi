---
title: Runtime Rules
type: system-rule
source: archive recovery + 2026-08-18 system upgrade
tags: [runtime, lesson, metrics, data-integrity]
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
```

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
mastery state
error watch
retention schedule
progress evidence
```

Do not create duplicate or conflicting records.

## Audit Rule

Every 14 days, check:

```text
runtime files remain short and current
mastery states agree with lesson evidence
trigger counts are consistent
delayed retention tasks are not silently dropped
historical numeric metrics are not fabricated
```
