---
title: Grammar Trigger Rule
type: system-rule
source: archive recovery + 2026-08-18 system upgrade
tags: [grammar, trigger, repair, runtime]
---

# Grammar Trigger Rule

## Purpose

Repeated errors should automatically change lesson mode without turning every small mistake into a grammar lecture.

## Trigger Levels

| Repetition | Status | Required action |
|---|---|---|
| 1 new conceptual error | watch | Brief correction; keep watching. |
| Returned error or 2nd relevant failure | priority_due | One short contrast/self-explanation + changed-context rebuild. |
| 3 failures in one lesson or across 2 consecutive study days | micro_due | 5–10 minute Micro Grammar Repair before moving on. |
| 5+ failures across days | focused_due | Focused Grammar Session + dedicated retention series. |

## Counting Rule

```text
Count a failure when the learner chooses or builds the target pattern incorrectly in an unaided retrieval attempt.
Do not count copied repetition after a displayed model as a new failure.
Do not increment for spelling-only slips when the conceptual choice is correct.
Immediate correct repetition repairs the output but does not reset the count.
Only delayed changed-context evidence can reduce the watch.
```

## Error Cause Classification

When evidence supports it, assign one primary cause:

```text
encoding = form/concept is not reliably known
retrieval = form is known but unavailable during output
contrast_selection = a competing form was selected
processing_load = form breaks inside longer speech
pronunciation_blocker = production breaks at sound/rhythm level
```

Do not invent a cause for one-off errors. Use the cause to choose the next drill.

## Trigger Watch States

```text
1 failure -> watch
2 failures -> priority_due
3-4 failures -> micro_due
5+ failures -> focused_due
same-lesson repair completed -> repair_completed_waiting_delayed
successful delayed changed-context check -> consolidating/watch/none per Mastery_Criteria.md
```

## Micro Grammar Repair

```text
1. Name the repeated error.
2. Explain only the required micro grammar.
3. Repair the core chunk.
4. Ask one short contrast question.
5. Make 3–5 controlled examples.
6. Make 2–3 personal transfer examples.
7. Use one unlabeled mixed-choice check if forms compete.
8. Do one spoken recall when the pattern is speech-relevant.
9. Schedule retention if still weak.
```

## Lesson Closing

If a grammar trigger fired, record:

```text
pattern:
repeated error:
primary cause:
repair chunk:
second output:
changed-context check:
retention date:
next trigger state:
```
