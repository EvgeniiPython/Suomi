---
title: Prior-Art Search
type: system-rule
source: 2026-08-20 agent-architecture upgrade
tags: [prior-art, retrieval, chunks, patterns, memory]
---

# Prior-Art Search

## Purpose

Before creating or changing a meaningful learning object, first search the existing knowledge base and recent session history.

The goal is to prevent the system from solving the same learning problem repeatedly or creating duplicate chunks, patterns, drills, or rules.

## When Search Is Required

Run a prior-art search before:

- accepting a new chunk;
- creating a new pattern drill for an existing target;
- changing a mastery state when the historical evidence is unclear;
- creating a new error entry for a possibly known problem;
- changing system rules or lesson mechanics.

## Search Targets

Search, in this order as practical:

```text
1. active chunks / patterns
2. recent errors
3. retention items
4. recent sessions
5. concepts
6. system rules / protocols
```

## Required Questions

Before creating the new object, answer:

```text
Does an equivalent object already exist?
Was this attempted before?
Was there a prior error or repair?
Is the proposed item already scheduled for retention?
Does an existing rule already cover this case?
```

## Decision

After search, record one of:

```text
REUSE    — existing object is sufficient
EXTEND   — existing object needs a controlled variation
NEW      — genuinely new object is justified
DEFER    — evidence is insufficient
```

## Evidence Rule

A search result is evidence about what the system already knows; it is not by itself evidence that the learner has mastered the item.

## Runtime Principle

Retrieval precedes generation for non-trivial learning decisions:

```text
Search → Understand → Decide → Generate
```
