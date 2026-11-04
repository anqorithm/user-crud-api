from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=255)
    age: int | None = Field(default=None, ge=0)
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=255)
    age: int | None = Field(default=None, ge=0)
    password: str = Field(min_length=8, max_length=100)


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=1, max_length=255)
    age: int | None = Field(default=None, ge=0)


class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime | None = None


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    priority: int = Field(default=1, ge=1, le=5)
    completed: bool = False


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    priority: int = Field(default=1, ge=1, le=5)
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    priority: int | None = Field(default=None, ge=1, le=5)
    completed: bool | None = None


class TaskRead(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: str | None = None
    email: str | None = None


class RefreshToken(BaseModel):
    refresh_token: str


class LoginRequest(BaseModel):
    email: str
    password: str


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_prev: bool


class CursorPaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: str | None = None
    has_more: bool


class ApiResponse(BaseModel):
    success: bool = True
    message: str = "Operation successful"
    data: dict | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: str | None = None
    code: str | None = None


class HealthCheck(BaseModel):
    status: str
    version: str
    database: str
    redis: str
    uptime: float
