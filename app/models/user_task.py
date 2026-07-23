from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: str = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=255)
    age: Optional[int] = Field(default=None, ge=0)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    hashed_password: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    __table_args__ = {"extend_existing": True}

    id: str = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: int = Field(default=1, ge=1, le=5)
    completed: bool = Field(default=False)
    user_id: str = Field(default=None, foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)