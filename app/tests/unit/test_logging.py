import pytest
from app.core.logging import setup_logging, log


class TestLogging:
    def test_setup_logging_returns_logger(self):
        logger = setup_logging()
        assert logger is not None

    def test_log_global_instance(self):
        assert log is not None

    def test_log_has_info_level(self):
        assert hasattr(log, "info")

    def test_log_has_error_level(self):
        assert hasattr(log, "error")

    def test_log_has_debug_level(self):
        assert hasattr(log, "debug")

    def test_log_has_warning_level(self):
        assert hasattr(log, "warning")