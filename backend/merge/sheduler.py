from models import Reminder
from prometheus_client import Counter
from sqlalchemy.orm import Session

reminders_fired = Counter('reminders_fired_total', 'Total reminders triggered')
reminders_failed = Counter('reminders_failed_total', 'Total reminders failed')

def schedule_reminder(reminder_data: dict, db: Session, user_id: int):
    reminder = Reminder(
        user_id=user_id,
        action=reminder_data["action"],
        fire_at=reminder_data["datetime"],
        raw_text=reminder_data["raw_text"],
    )
    db.add(reminder)
    db.commit()
