# Current State

**Последнее занятие:** 24 августа 2026

## Текущий уровень
Finnish A2 with growing A2+/B1 control in familiar personal and professional topics.

## Текущий фокус
Профессиональный разговорный финский: `minun täytyy + infinitive`, звонок/e-mail клиенту, `lounaan jälkeen`, `ennen lounasta`, `tapaamisen jälkeen`, `lähetän / lähden`, `sähköpostia / sähköpostin`, `saada projekti valmiiksi`, `pyytää häntä tekemään / lähettämään` и `jos en ehdi...`.

## Session model

```text
FULL_LESSON
RETENTION_SESSION
```

Continuation is a mode of the previous session type, not a third type.

## Учебное ядро

**Attempt → Check → Correct → Repair → Second Output → Variation → Cold Recall → Transfer → Finnish Dialogue → Second Chance → Final Speaking Challenge → Final Recall → Retention**

## Текущие статусы

### Active / Flexible
- `minun täytyy + infinitive`
- `lähetän / lähden` — correctly distinguished in unlabeled mixed-choice and production; continue active monitoring.
- `en lähetä / lähetän` — improved, but keep under active watch.

### Consolidating / требует дальнейшего delayed recall
- `lounaan jälkeen`
- `ennen lounasta`
- `en soita / soitan`
- `lähettää / lähteä`
- `sähköpostia / sähköpostin`
- `saada projekti valmiiksi`
- `pyytää häntä tekemään / lähettämään`
- `jos en ehdi saada projektia valmiiksi, ...`
- `minun / hänen / pojan täytyy + infinitive`

## Последнее занятие — 24.08.2026

- Начат `FULL_LESSON`.
- Выполнены Retrieval, Controlled Speaking, Finnish Dialogue, Error Repair + Second Chance, Final Speaking Challenge и Final Recall.
- `lähetän / lähden` успешно различены в unlabeled mixed-choice.
- `minun täytyy + infinitive` воспроизведено самостоятельно в трёх новых предложениях.
- `saada projekti valmiiksi`, `jos en ehdi...` и `pyytää häntä lähettämään` использованы в changed-context transfer.
- Были исправлены `lounaan jälkeen`, `en lähetä`, `lähettämään`, `valmiiksi`, `asiakkaalle`, `piirustukset` и `töihin`.
- Новых chunks не добавляли.
- Урок сохранён как `PARTIAL`, потому что обязательные для `FULL_LESSON` stages `listening_speaking`, `deep_processing` и `retention_record` ещё не закрыты.
- `continuation_required = YES`; продолжение должно сохранить тип `FULL_LESSON` и начаться с `listening_speaking`.

## Error Cause Watch

```text
en soittaa -> en soita | contrast_selection / retrieval | improved, continue delayed check
en lähetä -> lähetän | retrieval / contrast_selection | improved, continue mixed-choice
sähköpostin -> sähköpostia in negative construction | contrast_selection | context-dependent, active watch
lähettää vs lähteä | contrast_selection | improved after mixed-choice, continue monitoring
kotiin vs kotona | processing/context selection | corrected, delayed check optional
lounan jälkeen -> lounaan jälkeen | retrieval/encoding | corrected, continue delayed check
lähetämään -> lähettämään | spelling/encoding | corrected, continue monitoring
valmiksi -> valmiiksi | spelling/encoding | corrected
Hänelle/Pojalle täytyy -> Hänen/Pojan täytyy | subject-form selection | repaired and independently reproduced
```

## Current Mastery Evidence

| Pattern | 0–3 evidence | Recall | Fluency | Transfer | Status |
|---|---:|---|---|---|---|
| `minun täytyy + infinitive` | 3 | independent | medium | achieved | active-watch / consolidating |
| `lounaan jälkeen` | 3 | independent after repair | medium | achieved | consolidating |
| `ennen lounasta` | 3 | independent | medium | achieved | consolidating |
| `en soita / soitan` | 3 | independent | medium | achieved | consolidating |
| `en lähetä / lähetän` | 3 | independent after repair | medium | achieved | active-watch / consolidating |
| `lähettää / lähteä` | 3 | independent mixed-choice | medium | achieved | active-watch |
| `sähköpostia / sähköpostin` | 2 | context-dependent | hesitant | partial | active watch |
| `saada projekti valmiiksi` | 3 | independent | medium | achieved | consolidating |
| `pyytää häntä tekemään / lähettämään` | 3 | independent after repair | medium | achieved | consolidating |
| `jos en ehdi ...` | 3 | independent | medium | achieved | consolidating |
| `minun / hänen / pojan täytyy` | 2 | independent after repair | medium | achieved in new contexts | consolidating |

These scores are current evidence, not standardized test scores.

## Главные ошибки

- `täytyy` + личная форма → после `täytyy` нужен infinitive.
- `lähettää` vs `lähteä`.
- `en soittaa` → `en soita`.
- `en lähetä` vs `lähetän`.
- `sähköpostia` vs `sähköpostin` по контексту.
- `ensi viikolla` vs `ensi viikolle`.
- `tapaamiseen` vs `tapaamisesta`.
- `kotiin` vs `kotona` по направлению/местонахождению.
- `ennen lounaan` → `ennen lounasta`.
- `lounan jälkeen` → `lounaan jälkeen`.
- `lähetämään` → `lähettämään`.
- `valmiksi` → `valmiiksi`.
- субъектные формы с `täytyy`: `Hänen/Pojan`, а не `Hänelle/Pojalle` в соответствующих значениях.

## Retention

- 22.08.2026 — D+6 delayed recall + mixed-choice + changed-context transfer выполнены.
- 02.09.2026 — долгосрочный recall профессиональных chunks.
- 12.09.2026 — контроль и пересмотр статусов.

## Следующее занятие / continuation

Текущее занятие 24.08.2026 является незавершённым `FULL_LESSON`.

`continuation_required = YES`
`continuation_next_stage = listening_speaking`

Следующий runtime должен продолжить **этот же FULL_LESSON** с `Listening → Speaking`, затем выполнить `Deep Processing` и оставшиеся обязательные стадии. Нельзя переключаться на `RETENTION_SESSION` только из-за retention schedule, пока continuation не закрыт.

## Правило новых chunks

Новые chunks добавляются только после устойчивого **recall + variation + transfer**. При активном grammar trigger новые chunks не добавляются автоматически.

## Source of truth

- [[Lesson_Protocol]]
- [[Mastery_Criteria]]
- [[Grammar_Trigger_Rule]]
- [[Metrics_And_Audit]]
- [[../02_Retention/Retention_Rules]]
