"""
text_to_sql/logger.py
======================
Structured JSON logger for the Text-to-SQL pipeline.

Every query attempt is written to logs/query_log.jsonl
(JSON Lines format — one JSON object per line).
"""

import json
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, "query_log.jsonl")


def _ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)


def log_query(result: dict):
    """
    Appends a query result entry to the JSONL log file.
    Adds a timestamp automatically.
    """
    _ensure_log_dir()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "question": result.get("question"),
        "original_sql": result.get("original_sql"),
        "final_sql": result.get("sql"),
        "retried": result.get("retried", False),
        "retry_sql": result.get("retry_sql"),
        "status": result.get("status"),
        "row_count": result.get("row_count", 0),
        "error": result.get("error"),
        "latency_ms": result.get("latency_ms", 0.0),
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def get_log_path() -> str:
    return LOG_FILE
