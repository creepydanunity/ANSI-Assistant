## Analytics Dashboard
- 🔄 Status: In Progress
- 📅 Last updated: 2025-08-01
- 💬 Summary: UI layout just started, backend API endpoints mismatch with spec
- 🧠 History:
  - 2025-06-01: UI layout for Analytics Dashboard just started
  - 2025-06-01: Backend API endpoints implemented are /api/v2/metrics/summary and /metrics/daily, which mismatch with the spec
- ⚠️ Alerts:
  - 2025-06-01: UI progress contradicts with last update stating it was fully done
  - 2025-06-01: Backend API endpoints implemented do not match the spec

## Voice Command
- 🔄 Status: In Progress
- 📅 Last updated: 2025-08-01
- 💬 Summary: Decided to use local Whisper over WebSocket for STT backend
- 🧠 History:
  - 2025-06-01: Decided to use local Whisper over WebSocket for STT backend

## Smart Reminder System
- 🔄 Status: Open
- 📅 Last updated: 2025-08-01
- 💬 Summary: Planning to implement scheduling reminders and parsing user intent. Frontend will send raw text to backend. Backend will parse and schedule reminders.
- 🧠 History:
  - 2025-08-01: Discussed implementation of smart reminder system. Two core functions: scheduling reminders and parsing user intent.
  - 2025-08-01: Frontend will expose a modal where users type reminders. No need to validate input before sending.
  - 2025-08-01: Backend will handle raw text with a function called parse_reminder_intent(text: str) -> ReminderObject.
  - 2025-08-01: ReminderObject will have fields like 'action', 'datetime', 'repeat', 'raw_text'. Time parsing will be done using duckling and a small rule-based extractor for the verb.
  - 2025-08-01: Parsed reminders will be scheduled using schedule_reminder(reminder: ReminderObject). It will insert into a reminders table with a status, user_id, and fire_at timestamp.
  - 2025-08-01: Will use Celery beat + Redis for scheduling. Each minute it checks for due fire_at values and queues a delivery job.
  - 2025-08-01: If user deletes the reminder, it will be soft-deleted — flag is_active = false. The task runner will skip it automatically.
  - 2025-08-01: Will add observability — metrics on reminders fired, snoozed, failed. Will emit Prometheus events inside schedule_reminder.

