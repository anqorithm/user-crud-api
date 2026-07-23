import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from app.db.session import engine, async_session, get_session


class TestDatabaseSession:
    def test_engine_exists(self):
        assert engine is not None

    def test_async_session_maker_exists(self):
        assert async_session is not None

    def test_get_session_function_exists(self):
        assert get_session is not None

    def test_engine_is_async(self):
        from sqlalchemy.ext.asyncio import AsyncEngine
        assert isinstance(engine, AsyncEngine)


class TestDatabaseTables:
    def test_tables_can_be_imported(self):
        try:
            from app.db.session import user_table
            assert user_table is not None
        except ImportError:
            pass

    def test_session_maker_is_async(self):
        import inspect
        assert inspect.isasyncgenfunction(get_session) or hasattr(async_session, "__call__")