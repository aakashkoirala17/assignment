"""
text_to_sql/executor.py
========================
SQL Executor with automatic retry.

Step 1: Validate the SQL (safety check — SELECT only)
Step 2: Execute against PostgreSQL
Step 3: If it fails, call the LLM to fix it and retry ONCE
Step 4: Return structured result
"""

import time
from text_to_sql.validator import validate_sql
from text_to_sql.database import execute_query
from text_to_sql import sql_generator


def run_with_retry(question: str, sql: str) -> dict:
    """
    Validates and executes the SQL query.
    On failure, asks the LLM to fix it and retries once.

    Returns a structured result dict:
    {
        "question":       str,
        "sql":            str,       # the SQL that was actually executed
        "original_sql":   str,       # the first SQL generated
        "retried":        bool,      # whether a retry happened
        "retry_sql":      str|None,  # the fixed SQL (if retry happened)
        "status":         "success" | "error" | "blocked",
        "rows":           [...],
        "row_count":      int,
        "error":          str|None,
        "latency_ms":     float,
    }
    """
    start = time.time()

    result = {
        "question": question,
        "sql": sql,
        "original_sql": sql,
        "retried": False,
        "retry_sql": None,
        "status": "error",
        "rows": [],
        "row_count": 0,
        "error": None,
        "latency_ms": 0.0,
    }

    # ── Step 1: Safety Validation ─────────────────────────────────────────────
    validation = validate_sql(sql)
    if not validation["valid"]:
        result["status"] = "blocked"
        result["error"] = validation["reason"]
        result["latency_ms"] = round((time.time() - start) * 1000, 2)
        return result

    # ── Step 2: Execute ───────────────────────────────────────────────────────
    db_result = execute_query(sql)

    if db_result["status"] == "success":
        result.update({
            "status": "success",
            "rows": db_result["rows"],
            "row_count": db_result["row_count"],
            "error": None,
        })
        result["latency_ms"] = round((time.time() - start) * 1000, 2)
        return result

    # ── Step 3: Retry with LLM Fix ───────────────────────────────────────────
    original_error = db_result["error"]
    result["error"] = original_error

    try:
        fixed_sql = sql_generator.fix_sql(sql=sql, error=original_error)
    except Exception as e:
        result["error"] = f"LLM fix failed: {e}. Original error: {original_error}"
        result["latency_ms"] = round((time.time() - start) * 1000, 2)
        return result

    result["retried"] = True
    result["retry_sql"] = fixed_sql
    result["sql"] = fixed_sql

    # Validate the fix before executing
    fix_validation = validate_sql(fixed_sql)
    if not fix_validation["valid"]:
        result["status"] = "blocked"
        result["error"] = f"Fixed SQL blocked: {fix_validation['reason']}"
        result["latency_ms"] = round((time.time() - start) * 1000, 2)
        return result

    # Execute the fixed SQL
    retry_result = execute_query(fixed_sql)

    if retry_result["status"] == "success":
        result.update({
            "status": "success",
            "rows": retry_result["rows"],
            "row_count": retry_result["row_count"],
            "error": None,
        })
    else:
        result["status"] = "error"
        result["error"] = f"Retry also failed: {retry_result['error']}"

    result["latency_ms"] = round((time.time() - start) * 1000, 2)
    return result
