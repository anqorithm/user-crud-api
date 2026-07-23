import pytest
from app.core.exceptions import (
    AppException,
    NotFoundException,
    ConflictException,
    UnauthorizedException,
    ForbiddenException
)
from fastapi import HTTPException


class TestCustomExceptions:
    def test_app_exception(self):
        exc = AppException(status_code=400, detail="Bad Request")
        assert exc.status_code == 400
        assert exc.detail == "Bad Request"
        assert isinstance(exc, HTTPException)

    def test_not_found_exception_default(self):
        exc = NotFoundException()
        assert exc.status_code == 404
        assert exc.detail == "Resource not found"

    def test_not_found_exception_custom_message(self):
        exc = NotFoundException(detail="User not found")
        assert exc.status_code == 404
        assert exc.detail == "User not found"

    def test_conflict_exception_default(self):
        exc = ConflictException()
        assert exc.status_code == 409
        assert exc.detail == "Resource already exists"

    def test_conflict_exception_custom_message(self):
        exc = ConflictException(detail="Email already exists")
        assert exc.status_code == 409
        assert exc.detail == "Email already exists"

    def test_unauthorized_exception_default(self):
        exc = UnauthorizedException()
        assert exc.status_code == 401
        assert exc.detail == "Unauthorized"

    def test_unauthorized_exception_custom_message(self):
        exc = UnauthorizedException(detail="Invalid token")
        assert exc.status_code == 401
        assert exc.detail == "Invalid token"

    def test_forbidden_exception_default(self):
        exc = ForbiddenException()
        assert exc.status_code == 403
        assert exc.detail == "Forbidden"

    def test_forbidden_exception_custom_message(self):
        exc = ForbiddenException(detail="Access denied")
        assert exc.status_code == 403
        assert exc.detail == "Access denied"