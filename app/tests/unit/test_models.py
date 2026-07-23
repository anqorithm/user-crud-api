import pytest
from app.models.user_task import User, Task


class TestUserModel:
    def test_user_table_name(self):
        assert User.__tablename__ == "users"

    def test_user_fields_exist(self):
        assert hasattr(User, "id")
        assert hasattr(User, "name")
        assert hasattr(User, "email")
        assert hasattr(User, "age")
        assert hasattr(User, "is_active")
        assert hasattr(User, "is_superuser")
        assert hasattr(User, "hashed_password")
        assert hasattr(User, "created_at")
        assert hasattr(User, "updated_at")

    def test_user_optional_fields(self):
        user = User(
            id="test-id",
            name="Test User",
            email="test@example.com"
        )
        assert user.age is None
        assert user.hashed_password is None
        assert user.updated_at is None


class TestTaskModel:
    def test_task_table_name(self):
        assert Task.__tablename__ == "tasks"

    def test_task_fields_exist(self):
        assert hasattr(Task, "id")
        assert hasattr(Task, "title")
        assert hasattr(Task, "description")
        assert hasattr(Task, "priority")
        assert hasattr(Task, "completed")
        assert hasattr(Task, "user_id")
        assert hasattr(Task, "created_at")
        assert hasattr(Task, "updated_at")

    def test_task_defaults(self):
        task = Task(
            id="test-id",
            title="Test Task",
            user_id="user-id"
        )
        assert task.priority == 1
        assert task.completed is False
        assert task.description is None


class TestDatabaseConfig:
    def test_database_url_uses_asyncpg(self):
        from app.core.config import settings
        assert "asyncpg" in settings.database_url
        assert "postgresql" in settings.database_url

    def test_redis_url_format(self):
        from app.core.config import settings
        assert settings.redis_url.startswith("redis://")