import pytest
from app.services.email import send_email, send_welcome_email, send_password_reset_email
from app.core.config import settings


class TestEmailService:
    def test_send_email_disabled(self, monkeypatch):
        monkeypatch.setattr(settings, "email_enabled", False)
        result = send_email("test@example.com", "Subject", "Body")
        assert result["status"] == "disabled"

    def test_send_email_returns_dict(self, monkeypatch):
        monkeypatch.setattr(settings, "email_enabled", False)
        result = send_email("test@example.com", "Subject", "Body")
        assert isinstance(result, dict)
        assert "status" in result

    def test_send_welcome_email_returns_none(self, monkeypatch):
        monkeypatch.setattr(settings, "email_enabled", False)
        result = send_welcome_email("user@example.com", "John")
        assert result is None

    def test_send_password_reset_email_returns_none(self, monkeypatch):
        monkeypatch.setattr(settings, "email_enabled", False)
        result = send_password_reset_email("user@example.com", "reset_token_123")
        assert result is None