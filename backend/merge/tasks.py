from celery import Celery
from sqlalchemy.orm import Session
from models import Reminder
from scheduler import reminders_fired, reminders_failed

celery_app = Celery("reminders")
celery_app.conf.beat_schedule = {
    'check-reminders-every-minute': {
        'task': 'check_due_reminders',
        'schedule': 60.0
    }
}

@celery_app.task(name='check_due_reminders')
def check_due_reminders():
    with db_session() as db:
        now = datetime.utcnow()
        due = db.query(Reminder).filter(
            Reminder.fire_at <= now,
            Reminder.is_active == True,
            Reminder.status == "scheduled"
        ).all()

        for reminder in due:
            try:
                # Placeholder for actual notification logic
                print(f"[Reminder] {reminder.action}")
                reminder.status = "fired"
                reminders_fired.inc()
            except Exception:
                reminder.status = "failed"
                reminders_failed.inc()

        db.commit()
