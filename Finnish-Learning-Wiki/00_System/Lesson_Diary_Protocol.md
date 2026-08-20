---
title: Lesson Diary Protocol
type: system-rule
source: 2026-08-20 agent-architecture upgrade
tags: [diary, session, decisions, memory, audit]
---

# Lesson Diary Protocol

## Purpose

A lesson record should preserve not only what happened, but also the important decisions that explain why the learning system changed (or did not change) after the lesson.

The normal session file remains the main human-readable lesson record. A diary adds decision traceability without replacing the existing session protocol.

## Minimum Diary Fields

```text
Lesson
Date
Primary Can-Do
Initial plan
Observed evidence
Priority errors
Repairs performed
Important deviations from plan
Chunk candidates and decisions
Mastery decisions
Retention decisions
Next actions
```

## Decision Record

For every meaningful state-changing decision, record:

```text
object:
decision: ACCEPT | REJECT | DEFER | PROMOTE | KEEP | DEMOTE
reason:
evidence:
next_action:
```

## Rejected Decisions

Do not silently discard rejected candidates. When a candidate is educationally plausible but not accepted, preserve the reason briefly.

Examples:

```text
candidate: new chunk X
decision: DEFER
reason: transfer evidence insufficient
next_action: revisit after next recall cycle
```

## Deviation Rule

If the actual lesson diverged materially from the planned sequence, record the deviation and whether it affected mastery, retention, or chunk decisions.

## Closing Rule

At lesson close, the diary must remain concise enough to audit. Prefer evidence and decisions over narrative commentary.
