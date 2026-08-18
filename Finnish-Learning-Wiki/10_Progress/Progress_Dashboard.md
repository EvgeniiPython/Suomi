# Progress Dashboard

## Текущий этап
Переход от заученных предложений к автоматическим чанкам и связной профессиональной речи.

## Новая система метрик — active from 18.08.2026

Основные показатели остаются:

```text
Recall / Fluency / Transfer
```

Для ключевых patterns добавляется evidence score 0–3:

```text
0 = not yet
1 = assisted
2 = independent in familiar context
3 = flexible in changed context
```

Дополнительные показатели записываются только когда реально измерены:

```text
Accuracy
Repair rate
Contrast success
Speaking state: automatic / hesitant / blocked
```

Исторические оценки не пересчитываются задним числом как измеренные. Если значение восстановлено по старым записям, оно должно быть помечено `reconstructed`.

## Последняя сессия
**18.08.2026 — Speaking-First lesson + system upgrade**

Качественный результат: пользователь самостоятельно восстановил и варьировал конструкции вокруг `minun täytyy + infinitive`, отрицания, звонка/e-mail клиенту и договорённости о встрече; выполнил controlled speaking, transfer, Finnish dialogue, Final Speaking Challenge и Final Recall.

### Подтверждено
- `minun täytyy + infinitive` используется в нескольких ситуациях.
- `lounaan jälkeen` воспроизводится без подсказки.
- `en soita` и `en lähetä` воспроизведены после repair.
- `lähettää` и `lähteä` всё ещё конкурируют.
- `sähköpostia / sähköpostin` различение работает в простых контекстах, но требует mixed-choice проверки.
- Transfer и Final Speaking Challenge выполнены.
- Final Recall: 3 самостоятельных предложения выполнены.

## Current Evidence Snapshot

| Pattern | Evidence 0–3 | Recall | Fluency | Transfer | Mastery state |
|---|---:|---|---|---|---|
| `minun täytyy + infinitive` | 2 | independent | hesitant under load | achieved | consolidating |
| `lounaan jälkeen` | 2 | good | good | achieved | consolidating |
| `en soita / soitan` | 2 | independent after repair | hesitant | achieved in dialogue | consolidating |
| `en lähetä / lähetän` | 1–2 | mixed | hesitant | partial | active watch |
| `lähettää / lähteä` | 1–2 | mixed | hesitant | not robust | active watch |
| `sähköpostia / sähköpostin` | 1–2 | context-dependent | hesitant | partial | active watch |
| `sovimme tapaamisesta` | 2 | working | medium | achieved | consolidating |

These are lesson-evidence ratings, not standardized proficiency test scores.

## Historical Formal Metrics

**14.08.2026 — maintenance**
- Recall: 8.5/10
- Грамматика: 8.5/10
- Понимание: 9.5/10
- Беглость: 8/10
- Произношение: 8/10
- Самостоятельность: 8/10

**13.08.2026 — D+1**
- Recall: 9/10
- Грамматика: 8.5/10
- Понимание: 9/10
- Произношение: 8/10
- Беглость: 7.5/10

These older metrics remain historical. We now use the explicit 0–3 evidence score for key patterns and preserve the three primary metrics Recall / Fluency / Transfer.

## Active Error Watch

```text
en soita / soitan -> contrast_selection + retrieval
 en lähetä / lähetän -> contrast_selection + retrieval
sähköpostia / sähköpostin -> contrast_selection
lähettää / lähteä -> contrast_selection
 täytyy + infinitive -> retrieval under processing load
```

## Next Measurement Point

**19.08.2026 — D+3**

```text
blind recall
maximum 3 priority repairs
2–4 variation prompts
unlabeled mixed-choice check
transfer
listening -> speaking only if recall is stable
```

At D+3 record evidence score movement and whether any active-watch pattern can move from active to consolidating.

## Decision Gate For New Chunks

```text
stable recall + variation + transfer -> 2–3 new chunks may be introduced
broadly stable with 1–2 local errors -> repair first, then at most 1–2 new chunks
unstable recall or active grammar trigger -> no new chunks
```
