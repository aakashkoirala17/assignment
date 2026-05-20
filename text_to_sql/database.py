"""
text_to_sql/database.py
========================
Synchronous PostgreSQL connection for the Text-to-SQL pipeline.
Uses psycopg (v3) — compatible with Python 3.14.
Reads credentials from the project root .env file.
"""

import os
import psycopg
from dotenv import load_dotenv

# Load .env from the project root (one level up from this file)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


def get_connection():
    """
    Returns a live psycopg (v3) connection to the PostgreSQL database.
    Reads POSTGRES_* variables from .env.
    """
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
        port=int(os.getenv("POSTGRES_PORT", 5432)),
        dbname=os.getenv("POSTGRES_DB", "mydatabase"),
        user=os.getenv("POSTGRES_USER", "admin"),
        password=os.getenv("POSTGRES_PASSWORD", ""),
    )


def execute_query(sql: str) -> dict:
    """
    Executes a SQL query and returns rows as a list of dicts.

    Returns:
        {
            "status": "success" | "error",
            "rows": [...],
            "row_count": int,
            "error": None | str
        }
    """
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            # Already plain dicts thanks to dict_row factory
            rows = [dict(row) for row in rows]
            return {
                "status": "success",
                "rows": rows,
                "row_count": len(rows),
                "error": None,
            }
    except Exception as e:
        return {
            "status": "error",
            "rows": [],
            "row_count": 0,
            "error": str(e),
        }
    finally:
        if conn:
            conn.close()
