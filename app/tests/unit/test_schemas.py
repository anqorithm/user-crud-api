import pytest
from pydantic import ValidationError
from app.schemas import (
    UserCreate, UserUpdate, UserRead,
    TaskCreate, TaskUpdate, TaskRead,
    Token, PaginatedResponse, ErrorResponse,
    LoginRequest, ApiResponse
)
from datetime import datetime


class TestUserSchemas:
    def test_user_create_valid(self):
        user = UserCreate(
            name="John Doe",
            email="john@example.com",
            password="password123",
            age=30
        )
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.age == 30

    def test_user_create_minimal(self):
        user = UserCreate(
            name="Jane",
            email="jane@example.com",
            password="password123"
        )
        assert user.name == "Jane"
        assert user.email == "jane@example.com"
        assert user.age is None

    def test_user_create_empty_name(self):
        with pytest.raises(ValidationError):
            UserCreate(
                name="",
                email="test@test.com",
                password="password123"
            )

    def test_user_create_password_too_short(self):
        with pytest.raises(ValidationError):
            UserCreate(
                name="John",
                email="test@test.com",
                password="short"
            )

    def test_user_create_age_negative(self):
        with pytest.raises(ValidationError):
            UserCreate(
                name="John",
                email="test@test.com",
                password="password123",
                age=-1
            )

    def test_user_update_partial(self):
        update = UserUpdate(name="Updated Name")
        assert update.name == "Updated Name"
        assert update.email is None
        assert update.age is None

    def test_user_update_all_fields(self):
        update = UserUpdate(
            name="Updated",
            email="updated@example.com",
            age=25
        )
        assert update.name == "Updated"
        assert update.email == "updated@example.com"
        assert update.age == 25

    def test_user_read(self):
        user = UserRead(
            id="123",
            name="John",
            email="john@example.com",
            age=30,
            is_active=True,
            is_superuser=False,
            created_at=datetime.now(),
            updated_at=None
        )
        assert user.id == "123"
        assert user.is_active is True
        assert user.is_superuser is False


class TestTaskSchemas:
    def test_task_create_valid(self):
        task = TaskCreate(
            title="Fix bug",
            description="Fix login bug",
            priority=3,
            completed=False
        )
        assert task.title == "Fix bug"
        assert task.priority == 3

    def test_task_create_minimal(self):
        task = TaskCreate(title="New task")
        assert task.title == "New task"
        assert task.description is None
        assert task.priority == 1
        assert task.completed is False

    def test_task_create_invalid_priority_too_low(self):
        with pytest.raises(ValidationError):
            TaskCreate(title="Task", priority=0)

    def test_task_create_invalid_priority_too_high(self):
        with pytest.raises(ValidationError):
            TaskCreate(title="Task", priority=6)

    def test_task_update_partial(self):
        update = TaskUpdate(completed=True)
        assert update.completed is True
        assert update.title is None
        assert update.priority is None

    def test_task_read(self):
        task = TaskRead(
            id="456",
            title="Test Task",
            description="Description",
            priority=2,
            completed=False,
            user_id="user123",
            created_at=datetime.now(),
            updated_at=None
        )
        assert task.id == "456"
        assert task.user_id == "user123"


class TestTokenSchemas:
    def test_token(self):
        token = Token(access_token="abc123")
        assert token.access_token == "abc123"
        assert token.token_type == "bearer"

    def test_login_request(self):
        login = LoginRequest(email="test@example.com", password="password123")
        assert login.email == "test@example.com"
        assert login.password == "password123"


class TestPaginatedResponse:
    def test_paginated_response(self):
        items = [{"id": "1"}, {"id": "2"}]
        response = PaginatedResponse(
            items=items,
            total=10,
            page=1,
            page_size=2,
            pages=5,
            has_next=True,
            has_prev=False
        )
        assert len(response.items) == 2
        assert response.total == 10
        assert response.pages == 5
        assert response.has_next is True
        assert response.has_prev is False


class TestErrorResponse:
    def test_error_response(self):
        error = ErrorResponse(
            success=False,
            error="Not Found",
            detail="User not found",
            code="USER_NOT_FOUND"
        )
        assert error.success is False
        assert error.error == "Not Found"
        assert error.code == "USER_NOT_FOUND"

    def test_error_response_minimal(self):
        error = ErrorResponse(error="Internal Error")
        assert error.error == "Internal Error"
        assert error.success is False


class TestApiResponse:
    def test_api_response_default(self):
        response = ApiResponse()
        assert response.success is True
        assert response.message == "Operation successful"

    def test_api_response_custom(self):
        response = ApiResponse(success=False, message="Error", data={"key": "value"})
        assert response.success is False
        assert response.data == {"key": "value"}