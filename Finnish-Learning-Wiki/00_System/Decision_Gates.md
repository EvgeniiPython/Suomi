---
title: Decision Gates
type: system-rule
source: 2026-08-20 agent-architecture upgrade
tags: [gates, runtime, evidence, chunks, mastery]
---

# Decision Gates

## Purpose

Decision Gates convert critical learning rules from advisory instructions into explicit, testable conditions.

Markdown remains the source of truth for pedagogical policy. The future Python validator may enforce the conditions below, but it must not invent pedagogical decisions.

## Gate 1 — New Chunk

A new chunk may be accepted only when the current evidence supports expansion.

Required by default:

```text
recall = stable
variation = passed
transfer = passed
no active grammar trigger blocking expansion
not a duplicate of an existing chunk
```

Allowed outcomes:

```text
ACCEPT
REJECT
DEFER
```

A rejected or deferred candidate must keep its reason.

## Gate 2 — Mastery Promotion

A pattern may move upward on the Mastery Ladder only when the corresponding evidence exists.

Immediate success after a hint or model answer is not delayed mastery.

`stable` additionally requires the criteria defined in `Mastery_Criteria.md`.

## Gate 3 — Error Closure

A substantial repeated error cannot be marked closed merely because the user produced a correct answer immediately after correction.

Minimum closure path:

```text
error
→ repair
→ second output
→ delayed re-test
→ changed context
→ independent success
```

## Gate 4 — Topic Expansion

Do not introduce substantial new material while a required trigger action is unfinished.

Examples of blockers:

```text
active grammar trigger
unstable cold recall
unfinished priority repair
required second output missing
required retention action missed
```

## Gate 5 — Lesson Close

A lesson may be considered complete only when its required durable evidence has been recorded:

```text
lesson result
mastery state / unchanged state
priority error status
retention action
progress evidence
```

## Gate Philosophy

The LLM may reason about the learner and propose an action. The gate decides whether that action is permitted by the system policy.

**Prompt persuades. Gate enforces.**
