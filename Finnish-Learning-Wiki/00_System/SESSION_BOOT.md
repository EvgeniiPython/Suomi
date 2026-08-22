# SESSION BOOT

## Runtime routing

Перед уроком прочитать:

1. `00_System/Latest_Audit_State.json`
2. `00_System/Current_State.md`
3. `01_Today/Today.md`
4. `02_Retention/Retention_Dashboard.md`
5. `00_System/Lesson_Protocol.md`
6. `00_System/Session_Types_Registry.json`

### Decision order

```text
1. Latest_Audit_State
2. continuation_required?
3. session_type
4. Today / due retention
5. matching Lesson_Protocol route
```

### Continuation

Если `continuation_required = YES`:

- сохранить `session_type` предыдущей сессии;
- начать с `resume_stage`;
- закрыть остальные missing required stages этого же типа;
- не переключаться на `RETENTION_SESSION` из-за due retention;
- не вводить unrelated new material;
- после закрытия continuation вернуться к обычному runtime selection.

Continuation — это режим, а не третий тип сессии.

### Normal selection

Если `continuation_required = NO`:

```text
Today.session_type
→ иначе due retention → RETENTION_SESSION
→ иначе FULL_LESSON
```

Тип обязательно записывается в следующий canonical Session Record.

### Type routing

- `FULL_LESSON` → полный Speaking-First маршрут из `Lesson_Protocol.md`.
- `RETENTION_SESSION` → retention-маршрут из `Lesson_Protocol.md`.
- Required/optional stages берутся только из `Session_Types_Registry.json`.

### Sources of truth

- `Latest_Audit_State.json` — continuation и текущий audit state.
- `Today.md` — оперативный план и явно выбранный session type.
- `Retention_Dashboard.md` — due/upcoming retention.
- `Current_State.md` — текущий учебный snapshot.
- `Session_Types_Registry.json` — canonical machine-readable stages by type.
- `Lesson_Protocol.md` — canonical pedagogical route.

### Rule

Сначала определить `session_type + continuation`, затем выполнять соответствующий маршрут. Не смешивать rules `FULL_LESSON` и `RETENTION_SESSION`.

### After lesson

Сохранить один canonical Session Record и обновить только необходимые durable state files.
