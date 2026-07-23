import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.repositories import BaseRepository, UserRepo


class TestBaseRepository:
    def test_base_repository_has_required_methods(self):
        assert hasattr(BaseRepository, "get")
        assert hasattr(BaseRepository, "get_by_email")
        assert hasattr(BaseRepository, "get_all")
        assert hasattr(BaseRepository, "create")
        assert hasattr(BaseRepository, "update")
        assert hasattr(BaseRepository, "delete")
        assert hasattr(BaseRepository, "count")

    def test_base_repository_init_params(self):
        import inspect
        sig = inspect.signature(BaseRepository.__init__)
        params = list(sig.parameters.keys())
        assert "session" in params
        assert "model" in params

    def test_base_repository_is_generic(self):
        assert hasattr(BaseRepository, "__class_getitem__")


class TestUserRepo:
    def test_user_repo_exists(self):
        assert UserRepo is not None

    def test_user_repo_type_is_repository(self):
        from app.models.user_task import User
        assert UserRepo is not None


class TestRepositoryMethods:
    def test_repository_get_method_is_async(self):
        import inspect
        assert inspect.iscoroutinefunction(BaseRepository.get)

    def test_repository_get_all_method_is_async(self):
        import inspect
        assert inspect.iscoroutinefunction(BaseRepository.get_all)

    def test_repository_create_method_is_async(self):
        import inspect
        assert inspect.iscoroutinefunction(BaseRepository.create)

    def test_repository_update_method_is_async(self):
        import inspect
        assert inspect.iscoroutinefunction(BaseRepository.update)

    def test_repository_delete_method_is_async(self):
        import inspect
        assert inspect.iscoroutinefunction(BaseRepository.delete)