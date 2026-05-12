"""
logger.py — Central Logging Configuration
==========================================
A single place to configure logging for the entire application.
Import `get_logger` in every module to get a named, consistent logger.

Log levels used across layers:
  INFO    → normal successful operations
  WARNING → unexpected but handled situations (e.g. 404 not found)
  ERROR   → failures / exceptions
"""

import logging
import sys
from logging.handlers import RotatingFileHandler

# ── Constants ────────────────────────────────────────────────────────────────
LOG_FILE = "app.log"
LOG_FORMAT = "[%(asctime)s] %(levelname)-8s %(name)s — %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_LEVEL = logging.INFO


def _configure_root_logger() -> None:
    """Configure the root logger once when this module is first imported."""
    root = logging.getLogger()
    if root.handlers:
        # Already configured (e.g. during testing), skip
        return

    root.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    # Console handler — shows logs in the terminal
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)

    # Rotating file handler — writes to app.log, max 5 MB, keeps 3 backups
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(formatter)

    root.addHandler(console_handler)
    root.addHandler(file_handler)


# Run configuration on import
_configure_root_logger()


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger.

    Usage:
        from logger import get_logger
        logger = get_logger(__name__)
        logger.info("Something happened")
    """
    return logging.getLogger(name)
