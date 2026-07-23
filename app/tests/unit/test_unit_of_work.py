import pytest
from app.services.unit_of_work import UnitOfWork


class TestUnitOfWork:
    def test_uow_has_commit_method(self):
        assert hasattr(UnitOfWork, "commit")

    def test_uow_has_rollback_method(self):
        assert hasattr(UnitOfWork, "rollback")

    def test_uow_can_be_instantiated(self):
        uow = UnitOfWork()
        assert uow is not None


class TestGetUow:
    def test_get_uow_is_function(self):
        from app.services.unit_of_work import get_uow
        assert get_uow is not None
        assert callable(get_uow)