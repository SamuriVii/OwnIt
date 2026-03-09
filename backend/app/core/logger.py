import sys
from typing import TYPE_CHECKING

from loguru import logger

from app.core.config import settings

if TYPE_CHECKING:
    from loguru import Logger


def setup_logging() -> "Logger":
    """
    Setup logging configuration.
    Deletes default handlers and adds a new one with the specified format and level.
    """
    logger.remove()

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    logger.add(
        sys.stdout,  # Standard output for Docker/Console logging
        level=settings.LOG_LEVEL,  # Dynamically set level from .env (INFO/DEBUG)
        format=log_format,  # Use our custom colored format
        colorize=True,  # Enable colors for better readability in terminal
        backtrace=True,  # Enable full stack trace for better debugging
        diagnose=settings.is_dev,  # In DEV: include variable values in stack traces
        enqueue=True,  # Async-safe logging (prevents blocking)
    )

    return logger


# Global logger instance for application-wide use
log: "Logger" = logger
