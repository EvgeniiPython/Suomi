---
title: Audit Protocol
type: system-rule
source: 2026-08-20 agent-architecture upgrade
tags: [audit, verification, evidence, runtime]
---

# Audit Protocol

## Purpose

The lesson teacher/LLM proposes and conducts learning activity. The audit layer independently checks whether the recorded result is consistent with the system rules.

The auditor does not invent missing evidence and does not silently repair missing records.

## Lesson Audit Checks

For a substantial lesson, check as applicable:

```text
1. Can-Do outcome exists
2. unaided first output was preserved
3. priority errors are identifiable
4. repair evidence exists for priority errors
5. second output exists after correction
6. variation was performed when required
7. cold recall was performed when required
8. transfer was performed when required
9. dialogue / final speaking evidence exists when required
10. retention action is recorded
11. mastery changes have supporting evidence
12. new chunk decisions have supporting evidence
13. no fabricated numeric metrics
```

## Audit Status

Use:

```text
PASS
PASS_WITH_WARNINGS
FAIL
```

`PASS_WITH_WARNINGS` means the lesson is usable but one or more non-blocking issues should be corrected later.

`FAIL` means a critical gate is violated or required evidence is missing.

## Missing Evidence

Do not infer evidence from intent. For example:

```text
planned transfer ≠ completed transfer
correct immediately after hint ≠ delayed mastery
candidate chunk ≠ accepted chunk
```

## Read-Only First

The first implementation of the Python audit engine is read-only:

```text
READ → CHECK → REPORT
```

It must not modify learner state, session records, mastery, retention, or chunks automatically.

## Independence Principle

The component that conducts or generates the lesson must not be the sole judge of whether the lesson met its gates.

**Finder is not the judge.**
