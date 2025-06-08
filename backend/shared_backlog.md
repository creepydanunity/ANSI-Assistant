## Analytics Dashboard
- Status: In Progress
- Last updated: 2025-10-01
- Summary: UI is in early stages, backend API endpoints mismatched.
- History:
  - 2025-03-01: UI for Analytics Dashboard is fully done. Backend endpoints and JWT-based access control are to be implemented.
  - 2025-06-01: UI is still in early stages, first layout started.
  - 2025-06-01: Backend API endpoints implemented as /api/v2/metrics/summary and /metrics/daily, which differs from spec.
- Alerts:
  - 2025-06-01: UI status contradiction: previously reported as complete, now reported as just started.
  - 2025-06-01: Backend API endpoints mismatch with spec.

## Voice Command
- Status: In Progress
- Last updated: 2025-10-01
- Summary: On hold
- History:
  - 2025-03-01: Voice Command is on hold due to pending decision on STT backend.

## Smart Reminder System
- Status: Open
- Last updated: 2025-10-01
- Summary: Planning to implement scheduling reminders and parsing user intent functions.
- History:
  - 2025-08-01: Frontend will expose a modal for user input. Backend will parse the input with a function called parse_reminder_intent.
  - 2025-08-01: ReminderObject will be used to store parsed data.
  - 2025-08-01: Parsed reminders will be scheduled with schedule_reminder function.
  - 2025-08-01: Celery beat + Redis will be used for scheduling.
  - 2025-08-01: Reminders can be soft-deleted by setting is_active = false.
  - 2025-08-01: Metrics on reminders will be observed by emitting Prometheus events inside schedule_reminder.

