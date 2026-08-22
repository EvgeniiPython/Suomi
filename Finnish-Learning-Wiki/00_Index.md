# Finnish Learning Wiki

Главная точка входа в Wiki для занятий финским языком.

## Старт урока
1. `00_System/SESSION_BOOT.md`
2. `00_System/Current_State.md`
3. `01_Today/Today.md`
4. `02_Retention/Retention_Dashboard.md`
5. `00_System/Latest_Audit_State.json`
6. Активные chunks и приоритетные ошибки.
7. `00_System/Lesson_Protocol.md` — основной протокол урока.
8. `00_System/Daily_Speaking_First_Protocol.md` — полный 90-минутный Speaking-First режим для `FULL_LESSON`.

## Типы сессий
- `FULL_LESSON` — полный 8-этапный Speaking-First урок.
- `RETENTION_SESSION` — отдельная retention-сессия с собственным completion gate.
- `CONTINUATION` — режим продолжения незавершённой сессии; не является отдельным `session_type`.
- `00_System/Latest_Audit_State.json` определяет continuation state и `resume_stage`.

## Завершение урока
1. `00_System/Lesson_Diary_Protocol.md` — что сохранять после урока.
2. `00_System/Session_Record_Schema.md` — канонический формат `Session Result` и типов сессий.
3. `00_System/DATA_INTEGRITY.md` — правила безопасной записи истории.
4. `engine/validate_learning_system.py` — автоматическая структурная и evidence-проверка.
5. `engine/generate_audit_state.py` — формирование runtime audit state.

## Основные разделы
- `00_System/` — протоколы, runtime state и системные правила.
- `01_Today/` — текущий план занятия.
- `02_Retention/` — retention rules и текущие due-задачи.
- `03_Sessions/` — история занятий; новые canonical records используют `YYYY-MM-DD_Session_Record.md`.
- `04_Errors/` — исторический журнал ошибок.
- `10_Progress/` — текущий progress dashboard.
- `11_Concepts/` — методика и специализированные learning protocols.
- `13_Cards/` — карточки и contrast checks.
- `Progress/` — исторические/дополнительные метрики.

## Главный принцип

**Attempt → Check → Correct → Repair → Second Output → Variation → Transfer → Spoken Recall → Retention**

Главная цель — не изучить как можно больше нового материала, а быстрее сформировать самостоятельный доступ к финской речи.
