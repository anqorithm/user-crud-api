import pytest
from unittest.mock import Mock, patch, MagicMock
from app.main import app


class TestMainApp:
    def test_app_exists(self):
        assert app is not None

    def test_app_has_routes(self):
        routes = app.routes
        assert len(routes) > 0

    def test_app_title(self):
        assert app.title == "User CRUD API"

    def test_app_version(self):
        assert app.version == "1.0.0"

    def test_app_debug_default(self):
        assert app.debug is False


class TestMainAppMiddlewares:
    def test_app_has_middlewares(self):
        assert hasattr(app, "user_middleware")
        assert len(app.user_middleware) > 0


class TestMainAppLifespan:
    def test_app_has_router(self):
        assert hasattr(app, "router")