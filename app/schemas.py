from datetime import datetime
from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel, Field


T = TypeVar("T")


class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=255)
    age: Optional[int] = Field(default=None, ge=0)
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=255)
    age: Optional[int] = Field(default=None, ge=0)
    password: str = Field(min_length=8, max_length=100)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[str] = Field(default=None, min_length=1, max_length=255)
    age: Optional[int] = Field(default=None, ge=0)


class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: int = Field(default=1, ge=1, le=5)
    completed: bool = False


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: int = Field(default=1, ge=1, le=5)
    completed: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    completed: Optional[bool] = None


class TaskRead(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None
    email: Optional[str] = None


class RefreshToken(BaseModel):
    refresh_token: str


class LoginRequest(BaseModel):
    email: str
    password: str


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_prev: bool


class CursorPaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    next_cursor: Optional[str] = None
    has_more: bool


class ApiResponse(BaseModel):
    success: bool = True
    message: str = "Operation successful"
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None


class HealthCheck(BaseModel):
    status: str
    version: str
    database: str
    redis: str
    uptime: float