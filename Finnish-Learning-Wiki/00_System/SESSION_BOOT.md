# SESSION BOOT

## Перед каждым уроком

1. Прочитать `00_System/Latest_Audit_State.json`.
2. Прочитать `00_System/Current_State.md`.
3. Прочитать `01_Today/Today.md`.
4. Прочитать `02_Retention/Retention_Dashboard.md`.
5. Проверить Active Focus и приоритетные ошибки.
6. Следовать `00_System/Lesson_Protocol.md`.
7. Использовать `00_System/Daily_Speaking_First_Protocol.md` для `FULL_LESSON`.
8. Для `RETENTION_SESSION` использовать retention-маршрут из `Lesson_Protocol.md`.
9. При изменениях базы соблюдать `DATA_INTEGRITY.md`.

## Runtime decision order

`Latest_Audit_State.json` определяет незавершённость предыдущей сессии и точку continuation.

### 1. Continuation имеет абсолютный приоритет

Если:

```text
continuation_required = YES
```

то:

- сохранить `session_type` предыдущей сессии;
- начать именно с `resume_stage`;
- закрыть остальные незавершённые обязательные стадии этого же типа;
- не превращать continuation в `RETENTION_SESSION` только потому, что сегодня наступил retention date;
- не выбирать новый материал, пока continuation не закрыт.

Continuation — это режим продолжения, а не третий тип сессии.

### 2. Если continuation не требуется

Если:

```text
continuation_required = NO
```

то определить тип текущей сессии:

```text
Today.session_type, если он явно задан;
иначе RETENTION_SESSION, если есть due retention;
иначе FULL_LESSON.
```

Тип должен быть явно зафиксирован в Session Record:

```text
FULL_LESSON
RETENTION_SESSION
```

### 3. Тип определяет completion gate

`FULL_LESSON` требует 8 macro-stages:

```text
retrieval
listening_speaking
deep_processing
controlled_speaking
finnish_dialogue
error_repair_second_chance
final_challenge_recall
retention_record
```

`RETENTION_SESSION` требует 6 macro-stages:

```text
retrieval
controlled_speaking
finnish_dialogue
error_repair_second_chance
final_challenge_recall
retention_record
```

`listening_speaking` и `deep_processing` в retention не считаются пропущенными, если они не использовались.

## Источники истины

- `Latest_Audit_State.json` — незавершённость, session type и continuation point.
- `Current_State.md` — текущее учебное состояние, mastery, ошибки и контекст.
- `Today.md` — оперативная цель и явно выбранный тип сессии.
- `Retention_Dashboard.md` — due retention и retention context.
- `Lesson_Protocol.md` — правила проведения соответствующего типа.

При конфликте по continuation приоритет у `Latest_Audit_State.json`.

## Правила урока

- Главная цель — самостоятельная разговорная речь.
- Не добавлять новые chunks при незавершённом continuation или нестабильном retention.
- Не выдавать готовый ответ до минимальной подсказки и попытки самостоятельной коррекции.
- Для длинной речи ждать сигнала пользователя «я закончил, говори».
- После исправления получать второй output.
- Для конкурирующих форм использовать unlabeled mixed-choice.
- Значимую ошибку проверять через Second Chance позже в новом контексте.
- Не объявлять mastery стабильным по одной успешной сессии.

## После урока

Обновить соответствующие durable records и записать один canonical Session Result с явным `session_type`.

## Главный принцип

Сначала определить **тип сессии и continuation**, затем выполнять соответствующий маршрут. Нельзя использовать правила `FULL_LESSON` для `RETENTION_SESSION` и наоборот.
