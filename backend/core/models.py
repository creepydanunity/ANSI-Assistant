from datetime import date, datetime, timezone
from typing import List

from sqlalchemy import Date, String, Integer, DateTime, ForeignKey, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now()
    )

    projects: Mapped[List["UserProject"]] = relationship(
        "UserProject", back_populates="user"
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now()
    )

    users: Mapped[List["UserProject"]] = relationship(
        "UserProject", back_populates="project"
    )
    repos: Mapped[List["ProjectRepo"]] = relationship(
        "ProjectRepo", back_populates="project"
    )
    conversations: Mapped[List["ConversationSession"]] = relationship(
        "ConversationSession", back_populates="project"
    )


class ProjectRepo(Base):
    __tablename__ = "repos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    repo_url: Mapped[str] = mapped_column(String, nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now()
    )

    project: Mapped["Project"] = relationship("Project", back_populates="repos")


class UserProject(Base):
    __tablename__ = "user_projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))

    user: Mapped["User"] = relationship("User", back_populates="projects")
    project: Mapped["Project"] = relationship("Project", back_populates="users")

class ConversationSession(Base):
    __tablename__ = "conversation_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
    session_date: Mapped[date] = mapped_column(Date, nullable=False, unique=True, index=True)

    messages: Mapped[List["Message"]] = relationship(
        "Message",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    project: Mapped["Project"] = relationship("Project", back_populates="conversation_sessions")

    def __repr__(self) -> str:
        return f"<ConversationSession(id={self.id}, session_date={self.session_date})>"


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("conversation_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    speaker: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    session: Mapped["ConversationSession"] = relationship(
        "ConversationSession",
        back_populates="messages",
    )

    __table_args__ = (
        UniqueConstraint("session_id", "timestamp", "speaker", name="uq_session_time_speaker"),
    )

    def __repr__(self) -> str:
        ts = self.timestamp.strftime("%Y-%m-%d %H:%M")
        return f"<Message(id={self.id}, session_id={self.session_id}, ts={ts}, speaker={self.speaker})>"