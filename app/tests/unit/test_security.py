import pytest
from app.core.security import create_access_token, decode_token
from app.core.config import Settings
from datetime import timedelta


class TestJWTToken:
    def test_create_access_token(self):
        data = {"sub": "user123", "email": "test@example.com"}
        token = create_access_token(data)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_expiry(self):
        data = {"sub": "user123"}
        token = create_access_token(data, expires_delta=timedelta(minutes=5))
        assert isinstance(token, str)

    def test_decode_token_valid(self):
        data = {"sub": "user123", "email": "test@example.com"}
        token = create_access_token(data)
        decoded = decode_token(token)
        assert decoded["sub"] == "user123"
        assert decoded["email"] == "test@example.com"
        assert "exp" in decoded

    def test_decode_token_invalid(self):
        from app.core.exceptions import UnauthorizedException
        with pytest.raises(UnauthorizedException):
            decode_token("invalid.token.here")

    def test_decode_token_tampered(self):
        from app.core.exceptions import UnauthorizedException
        data = {"sub": "user123"}
        token = create_access_token(data)
        tampered = token[:-5] + "xxxxx"
        with pytest.raises(UnauthorizedException):
            decode_token(tampered)


class TestSettings:
    def test_default_settings(self):
        settings = Settings()
        assert settings.app_name == "User CRUD API"
        assert settings.app_version == "1.0.0"
        assert settings.cache_ttl == 300
        assert settings.rate_limit_per_minute == 60

    def test_settings_jwt_defaults(self):
        settings = Settings()
        assert settings.jwt_algorithm == "HS256"
        assert settings.access_token_expire_minutes == 30

    def test_settings_redis_url(self):
        settings = Settings()
        assert settings.redis_url.startswith("redis://")

    def test_settings_celery_broker(self):
        settings = Settings()
        assert settings.celery_broker_url is not None

    def test_settings_model_config(self):
        settings = Settings()
        assert settings.model_config is not None