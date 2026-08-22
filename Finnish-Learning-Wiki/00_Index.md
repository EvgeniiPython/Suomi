# Finnish Learning Wiki

Главная точка входа в Wiki для занятий финским языком.

## Старт урока
1. `00_System/SESSION_BOOT.md`
2. `00_System/Latest_Audit_State.json`
3. `00_System/Current_State.md`
4. `01_Today/Today.md`
5. `02_Retention/Retention_Dashboard.md`
6. `00_System/Session_Types_Registry.json`
7. `00_System/Lesson_Protocol.md`

## Завершение урока
1. `00_System/Session_Record_Schema.md` — канонический формат `Session Result`.
2. `00_System/DATA_INTEGRITY.md` — правила безопасной записи.
3. `engine/validate_learning_system.py` — структурная и логическая проверка.
4. `engine/generate_audit_state.py` — генерация runtime audit state.

## Архитектура
- `00_System/` — runtime, policy и текущие системные состояния.
- `00_System/Session_Types_Registry.json` — единый machine-readable registry session types и macro-stages.
- `01_Today/` — только текущий operational plan.
- `02_Retention/` — только due/upcoming retention state.
- `03_Sessions/` — исторические canonical Session Records.
- `04_Errors/` — исторические записи ошибок.
- `10_Progress/` — progress dashboard.
- `11_Concepts/` — дополнительные методические материалы.
- `13_Cards/` — карточки и contrast materials.
- `engine/` — validator, audit generator и Telegram reporting.

## Session model

```text
FULL_LESSON
RETENTION_SESSION
```

Continuation — runtime mode исходного типа, а не третий тип сессии.

Главные источники истины:

```text
Session_Types_Registry.json → required/optional stages
Lesson_Protocol.md           → педагогический маршрут
Latest_Audit_State.json      → continuation/audit runtime state
Current_State.md             → текущий учебный snapshot
Today.md                     → текущий session plan
Retention_Dashboard.md       → due/upcoming retention
Session_Record               → исторический результат фактической сессии
```

## Главный принцип

**Attempt → Check → Correct → Repair → Second Output → Variation → Transfer → Spoken Recall → Retention**

Главная цель — не изучить как можно больше нового материала, а быстрее сформировать самостоятельный доступ к финской речи.
