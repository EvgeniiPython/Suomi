---
title: Active Focus
type: system
source: current learning state 2026-08-18 system upgrade
tags: [active-focus, runtime, speaking]
---

# Active Focus

## Current Focus Areas

```text
1. Speaking-first retention with delayed evidence.
2. Professional workday / client communication transfer.
3. minun täytyy + infinitive.
4. en soita / soitan.
5. en lähetä / lähetän.
6. lähettää / lähteä.
7. sähköpostia / sähköpostin.
8. lounaan jälkeen and sovimme tapaamisesta.
```

## Active Core Chunks (Next Recall)

```text
Huomenna lounaan jälkeen minun täytyy lähettää sähköposti asiakkaalle.
Huomenna lounaan jälkeen en soita asiakkaalle.
Tänään en lähetä sähköpostia, koska olen väsynyt.
Sovimme tapaamisesta ensi viikolle.
Minun täytyy mennä kurssille.
```

## Active Weak Patterns

```text
täytyy + infinitive, not täytyy + personal verb form
en soita / soitan
en lähetä / lähetän
lähettää / lähteä
sähköpostia / sähköpostin
ensi viikolla / ensi viikolle
tapaamiseen / tapaamisesta
```

## Error Cause Watch

```text
en soita / soitan -> contrast_selection + retrieval
 en lähetä / lähetän -> contrast_selection + retrieval
lähettää / lähteä -> contrast_selection
sähköpostia / sähköpostin -> contrast_selection
täytyy + infinitive -> retrieval under processing load
```

## Trigger Watch State

Format:

```text
pattern_id | recent_failures=N | failure_days=N | state=watch/priority_due/micro_due/focused_due/repair_completed_waiting_delayed | next_action=...
```

Current watch:

```text
en_soita_soitan | recent_failures=2 | failure_days=2 | state=repair_completed_waiting_delayed | next_action=unlabeled_mixed_choice_d3
en_laheta_lahetan | recent_failures=2 | failure_days=2 | state=repair_completed_waiting_delayed | next_action=unlabeled_mixed_choice_d3
lahettaa_lahtea | recent_failures=2 | failure_days=2 | state=watch | next_action=contrast_check
taytyy_infinitive | recent_failures=1 | failure_days=1 | state=watch | next_action=delayed_recall
sahkopostia_sahkopostin | recent_failures=1 | failure_days=1 | state=watch | next_action=mixed_choice_d3
```

## Mastery Movement Target

Do not promote a pattern to stable until it passes the delayed evidence gate in `Mastery_Criteria.md`.
