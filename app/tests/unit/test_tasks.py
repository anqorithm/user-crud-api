
import pytest

try:
    import celery  # noqa: F401
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False


@pytest.mark.skipif(not CELERY_AVAILABLE, reason="Celery not installed")
class TestCeleryTasks:
    def test_send_email_task_exists(self):
        from app.services.celery_app import send_email_task
        assert send_email_task is not None
        assert callable(send_email_task)

    def test_cleanup_expired_cache_task_exists(self):
        from app.services.celery_app import cleanup_expired_cache_task
        assert cleanup_expired_cache_task is not None
        assert callable(cleanup_expired_cache_task)

    def test_generate_report_task_exists(self):
        from app.services.celery_app import generate_report_task
        assert generate_report_task is not None
        assert callable(generate_report_task)

    def test_celery_app_config(self):
        from app.services.celery_app import celery_app
        assert celery_app.conf.task_serializer == "json"
        assert celery_app.conf.result_serializer == "json"
        assert celery_app.conf.timezone == "UTC"
        assert celery_app.conf.enable_utc is True

    def test_celery_app_broker_configured(self):
        from app.services.celery_app import celery_app
        assert celery_app.conf.broker_url is not None
        assert celery_app.conf.result_backend is not None

    def test_cleanup_expired_cache_task_returns_count(self):
        from unittest.mock import AsyncMock, MagicMock, patch

        from app.services.celery_app import cleanup_expired_cache_task

        async def scan_iter(match):
            for key in ["expired:a", "expired:b"]:
                yield key

        client = MagicMock(scan_iter=scan_iter, delete=AsyncMock(), close=AsyncMock())
        with patch("redis.asyncio.from_url", return_value=client):
            assert cleanup_expired_cache_task() == {"cleaned": 2}
        client.delete.assert_awaited_once_with("expired:a", "expired:b")
