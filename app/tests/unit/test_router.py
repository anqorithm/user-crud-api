import pytest
from app.api.v1.router import api_router


class TestAPIRouter:
    def test_api_router_exists(self):
        assert api_router is not None

    def test_api_router_has_prefix(self):
        assert api_router.prefix == "/api/v1"

    def test_api_router_has_routes(self):
        routes = list(api_router.routes)
        assert len(routes) > 0

    def test_api_router_is_fastapi_router(self):
        from fastapi import APIRouter
        assert isinstance(api_router, APIRouter)