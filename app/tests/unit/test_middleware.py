import pytest
from app.core.middleware import RequestIDMiddleware, RateLimitMiddleware


class TestRequestIDMiddlewareDetails:
    def test_middleware_class_exists(self):
        assert RequestIDMiddleware is not None

    def test_middleware_dispatch_exists(self):
        assert hasattr(RequestIDMiddleware, "dispatch") or hasattr(RequestIDMiddleware, "process_request")


class TestRateLimitMiddlewareDetails:
    def test_rate_limit_tracks_requests(self):
        middleware = RateLimitMiddleware(app=None)
        assert hasattr(middleware, "requests_per_minute")
        assert middleware.requests_per_minute == 60

    def test_rate_limit_custom_limit(self):
        middleware = RateLimitMiddleware(app=None, requests_per_minute=100)
        assert middleware.requests_per_minute == 100


class TestMiddlewareIntegration:
    def test_middleware_can_be_applied_to_app(self):
        from fastapi import FastAPI
        app = FastAPI()
        app.add_middleware(RequestIDMiddleware)
        assert len(app.user_middleware) > 0