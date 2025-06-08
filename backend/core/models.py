from datetime import date, datetime, timezone
from typing import List

from sqlalchemy import Date, String, Integer, DateTime, ForeignKey, Text, func
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
    conversation_sessions: Mapped[List["Transcription"]] = relationship(
        "Transcription", back_populates="project"
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

class Transcription(Base):
    __tablename__ = "transcriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
    last_update: Mapped[datetime] = mapped_column(
        DateTime(),
        default=lambda: datetime.now(),
        server_default=func.now()
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    project: Mapped["Project"] = relationship("Project", back_populates="transcriptions")

    def __repr__(self) -> str:
        return f"<Transcription(id={self.id}, session_date={self.session_date})>"