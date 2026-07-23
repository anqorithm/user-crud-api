from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os


class Settings(BaseSettings):
    app_name: str = "User CRUD API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"

    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/users_db"
    redis_url: str = "redis://redis:6379"
    cache_ttl: int = 300

    jwt_secret_key: str = "change-this-in-production-use-env-var"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    rate_limit_per_minute: int = 60
    max_upload_size_mb: int = 10

    email_enabled: bool = False
    smtp_host: str = "localhost"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = "noreply@example.com"

    celery_broker_url: str = "redis://redis:6379/1"
    celery_result_backend: str = "redis://redis:6379/2"

    sentry_dsn: str = ""

    otel_exporter_endpoint: str = ""
    otel_service_name: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()