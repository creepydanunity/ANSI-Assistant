from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    fire_at = Column(DateTime, nullable=False)
    raw_text = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    status = Column(String, default="scheduled")  # scheduled, fired, failed
    created_at = Column(DateTime, default=datetime.utcnow)
