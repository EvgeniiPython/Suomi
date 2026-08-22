# Daily Speaking-First Protocol

## Общий принцип

Главная цель ежедневной практики — уменьшать задержку между мыслью и финской фразой.

Перед началом сначала определить:

```text
session_type = FULL_LESSON | RETENTION_SESSION
```

и проверить `Latest_Audit_State.json` на continuation.

## FULL_LESSON — 90 минут

Полный маршрут Speaking-First. Все 8 macro-stages обязательны.

### 0–10 — Retrieval
Без подсказок вспомнить материал предыдущих занятий и проверить 2–3 приоритетные ошибки.

### 10–25 — Listening → Speaking
Короткий финский диалог/история, общий смысл, Meaning Blocks, самостоятельный retell и 2–3 полезных chunks.

### 25–35 — Deep Processing / Encoding
Для 2–3 центральных chunks: смысл, вариативность, контраст и личный пример. Без длинной лекции.

### 35–50 — Controlled Speaking
Attempt → repair if needed → 3–4 variation → cold recall.

### 50–70 — Real Situation / Finnish Dialogue
Самостоятельная речь и короткий финский диалог с follow-up. Длинную речь не перебивать; ждать «я закончил, говори».

### 70–80 — Error Repair + Second Chance
Максимум 3 приоритетные ошибки. После correction обязательно получить second output и позже провести second chance.

### 80–87 — Final Speaking Challenge + Final Recall
Реальная ситуация без подсказок + 3 разных предложения с главным pattern.

### 87–90 — Retention / Lesson Record
Зафиксировать durable state, errors, mastery, next review и canonical Session Result.

## RETENTION_SESSION — сокращённый маршрут

Retention session не обязана повторять полный 90-минутный урок. Цель — delayed recall, automaticity и transfer.

### 1. Retrieval
Blind recall 3–5 приоритетных chunks/patterns.

### 2. Controlled Speaking
3–4 вариации, cold recall и unlabeled mixed-choice для competing forms.

### 3. Finnish Dialogue
Короткий вопрос → ответ → follow-up → ответ.

### 4. Error Repair + Second Chance
Максимум 3 priority repairs, затем повторная проверка в новом контексте.

### 5. Final Speaking Challenge + Final Recall
Changed-context speaking challenge и 3 самостоятельных предложения с главным pattern.

### 6. Retention / Lesson Record
Зафиксировать evidence, mastery, errors и следующую retention date.

`Listening → Speaking` и `Deep Processing` можно добавить в retention session при реальной пользе, но их отсутствие не является незавершённой macro-stage.

## Правило continuation

Если `Latest_Audit_State.json` содержит `continuation_required = YES`, сначала завершить missing stages исходного `session_type`. Не превращать continuation в retention session.

## Правило помощи

**Attempt → Hint 1 → Self-correction → Hint 2 if needed → Answer only as last resort → Retry**

## Transfer

Transfer должен менять ситуацию или коммуникативную цель и требовать самостоятельного выбора знакомого pattern.

## Что считается активным

Не считать материал active только по чтению, объяснению, повторению вслед за преподавателем или одному немедленному правильному ответу.

Надёжное evidence включает recall без подсказки, variation, cold recall, transfer, dialogue/free speech, Second Chance и delayed retrieval.

## SRS

Использовать выборочно для материала, который продолжает забываться после речевой практики. Предпочтение — production cards с целыми chunks.

## Новые chunks

- устойчивый recall + variation + transfer → 2–3 новых chunks;
- локальные ошибки при в целом устойчивом recall → repair → максимум 1–2 новых;
- нестабильный recall или активный trigger → новых chunks не добавлять.

## Главное правило

**Не путать тип сессии с уровнем mastery. FULL_LESSON и RETENTION_SESSION — разные маршруты проверки, но используют одну Speaking-First методику.**
