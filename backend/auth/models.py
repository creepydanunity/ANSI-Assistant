from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    projects = relationship("UserProject", back_populates="user")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    users = relationship("UserProject", back_populates="project")
    repos = relationship("ProjectRepo", back_populates="project")

class ProjectRepo(Base):
    __tablename__ = "repos"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    repo_url = Column(String, nullable=False)
    token = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    project = relationship("Project", back_populates="repos")

class UserProject(Base):
    __tablename__ = "user_projects"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))

    user = relationship("User", back_populates="projects")
    project = relationship("Project", back_populates="users")