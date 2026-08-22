# Lesson Protocol

## System model

Наша система остаётся **Speaking-First**, но теперь различает два типа сессий:

```text
FULL_LESSON
RETENTION_SESSION
```

Continuation не является третьим типом. Это режим продолжения незавершённой сессии её исходного типа.

Главный учебный цикл:

**Attempt → Check → Correct → Repair → Second Output → Variation → Cold Recall → Transfer → Finnish Dialogue → Second Chance → Final Speaking Challenge → Final Recall → Retention**

## FULL_LESSON

### Цель
Полный 90-минутный урок: развитие самостоятельной речи, controlled practice, listening-to-speaking, deep processing и перенос в новые ситуации.

### Обязательные macro-stages

1. **Retrieval — 10 мин**: старые chunks и приоритетные ошибки без подсказки.
2. **Listening → Speaking — 15 мин**: короткий input, общий смысл, meaning blocks, пересказ и 2–3 полезных chunks.
3. **Deep Processing / Encoding — 10 мин**: маленькая concept network вокруг 2–3 полезных chunks; без длинной лекции.
4. **Controlled Speaking — 15 мин**: попытка → 3–4 вариации → cold recall.
5. **Real Situation / Finnish Dialogue — 20 мин**: самостоятельная речь и короткий диалог преимущественно на финском.
6. **Error Repair + Second Chance — 10 мин**: максимум 3 приоритетные ошибки и повторная проверка позже.
7. **Final Speaking Challenge + Final Recall — 7 мин**: свободная задача и 3 новых предложения с главным pattern.
8. **Retention / Lesson Record — 3 мин**: durable state, retention date, errors и canonical Session Result.

Для `FULL_LESSON` все восемь stages обязательны.

## RETENTION_SESSION

### Цель
Проверить delayed retrieval, автоматизацию и transfer уже изученных patterns. Новые chunks не являются целью и добавляются только при устойчивом evidence и отсутствии блокирующих triggers.

### Обязательные macro-stages

1. **Retrieval** — blind recall 3–5 приоритетных chunks/patterns.
2. **Controlled Speaking** — 3–4 вариации, cold recall и при необходимости unlabeled mixed-choice.
3. **Finnish Dialogue** — короткий диалог с follow-up, преимущественно на финском.
4. **Error Repair + Second Chance** — максимум 3 приоритетные ошибки, затем повторная проверка.
5. **Final Speaking Challenge + Final Recall** — самостоятельный changed-context output и 3 предложения с главным pattern.
6. **Retention / Lesson Record** — зафиксировать результат, mastery evidence, next review и remaining errors.

### Optional в retention

`Listening → Speaking` и `Deep Processing` можно добавить, когда они реально усиливают конкретный retention task. Их отсутствие **не является missing stage** и не превращает retention session в PARTIAL.

### Правило retention

Retention session должна быть направлена на recall и transfer, а не на механическое воспроизведение старого урока. Для competing forms unlabeled mixed-choice является обязательным, когда это релевантно.

## Continuation

Если сессия любого типа завершена не полностью:

```text
lesson_status = PARTIAL | INTERRUPTED
continuation_required = YES
continuation_next_stage = first missing required stage
```

Следующая сессия:

1. сохраняет исходный `session_type`;
2. начинает с `continuation_next_stage`;
3. закрывает остальные missing stages этого же типа;
4. не переключается на новый session type только из-за due retention;
5. только после полного закрытия continuation возвращается к обычному runtime selection.

Пример:

```text
FULL_LESSON
6/8
missing: listening_speaking, deep_processing
        ↓
CONTINUATION
        ↓
listening_speaking
        ↓
deep_processing
        ↓
FULL_LESSON complete
```

## Помощь

**Attempt → Hint 1 → Self-correction → Hint 2 if needed → Answer only as last resort → Retry**

Не выдавать готовый ответ, пока пользователь способен продолжить с подсказкой.

## Variation Chain

После успешного воспроизведения важного pattern сделать 3–4 вариации, меняя по одному параметру: субъект, время, объект, обстоятельство, отрицание, вопрос или причина.

## Cold Recall

После примерно 3–5 упражнений убрать подсказки и проверить самостоятельное воспроизведение.

## Transfer

Задача должна менять ситуацию или коммуникативную цель и заставлять пользователя самому распознать подходящий pattern.

## Finnish Dialogue

**Question → User answer → Follow-up → User response**.

Русский используется только для краткой подсказки или объяснения, когда это действительно необходимо.

## Second Chance

Значимая ошибка возвращается позже в новом контексте:

**Error → Repair → Correct Output → Delayed Re-test → New Context**

Исправление сразу после модели не является delayed mastery.

## Mixed Choice Check

При конкурирующих формах после repair дать минимум одну unlabeled mixed-choice check. Не объявлять заранее, какое правило проверяется.

## Listening усиленный протокол

Для `FULL_LESSON`:

**Listen → Big Picture → Meaning Blocks → Recall → Notice → optional Shadowing → Retell → Variation → Transfer → Delayed Recall**

Первый проход — без текста; не переводить input целиком.

## Deep Processing

Для 1–2 центральных chunks:

- Где я это реально использую?
- Что можно изменить, сохранив структуру?
- Какая ситуация естественно приводит к этой фразе?
- С чем её легко перепутать?
- Какой личный пример я могу сказать?

Цель — маленькая смысловая сеть, а не длинная грамматическая лекция.

## Mastery

Используем:

```text
active → consolidating → stable → dormant
```

Для stable нужны delayed +1/+3/+7 evidence, новый личный контекст и mixed-choice check при конкурирующих формах.

## New chunks

```text
устойчивый recall + variation + transfer → 2–3 новых chunks
локальные ошибки при в целом устойчивом recall → repair → максимум 1–2 новых
нестабильный recall или активный trigger → новых chunks не добавлять
```

## Canonical Session Result

Каждая новая сессия должна заканчиваться одной canonical `## Session Result` записью с:

- `session_type`;
- `lesson_status`;
- evidence;
- protocol completion;
- chunk decisions;
- mastery;
- retention;
- errors;
- next step.

Для `FULL_LESSON` completion проверяется по 8 stages. Для `RETENTION_SESSION` — по 6 stages.

## Главное правило

Сначала определить **session type + continuation**, затем выполнять соответствующий маршрут. Нельзя требовать восемь stages от retention session и нельзя использовать retention shortcut для незавершённого full lesson.
