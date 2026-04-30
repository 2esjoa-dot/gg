"""Structured JSON logging configuration with file rotation."""

import logging
import os
from contextvars import ContextVar
from logging.handlers import TimedRotatingFileHandler

from pythonjsonlogger import jsonlogger

from app.config import settings

request_id_var: ContextVar[str] = ContextVar("request_id", default="")


class RequestIDFilter(logging.Filter):
    """Inject request_id from ContextVar into log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get("")  # type: ignore[attr-defined]
        return True


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with standard fields."""

    def add_fields(self, log_record: dict, record: logging.LogRecord, message_dict: dict) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        if hasattr(record, "request_id"):
            log_record["request_id"] = record.request_id  # type: ignore[attr-defined]


def setup_logging() -> None:
    """Configure application logging with JSON format and file rotation."""
    os.makedirs(settings.LOG_DIR, exist_ok=True)

    formatter = CustomJsonFormatter(
        fmt="%(timestamp)s %(level)s %(name)s %(message)s",
        rename_fields={"timestamp": "timestamp", "levelname": "level"},
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.addFilter(RequestIDFilter())

    # File handler with daily rotation
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(settings.LOG_DIR, "app.log"),
        when="midnight",
        interval=1,
        backupCount=settings.LOG_MAX_DAYS,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.addFilter(RequestIDFilter())

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
