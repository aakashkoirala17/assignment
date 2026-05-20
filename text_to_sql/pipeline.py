"""
text_to_sql/pipeline.py
========================
Main pipeline orchestrator.

Ties together:
  1. sql_generator  → Generate SQL from natural language
  2. executor       → Validate, execute, and retry
  3. logger         → Log every attempt to JSONL

Entry point for a single question:
  result = run_pipeline("Show all customers from France")
"""

import time
from text_to_sql import sql_generator, executor, logger


def run_pipeline(question: str) -> dict:
    """
    Full Text-to-SQL pipeline for a single natural language question.

    Steps:
      1. Call Gemini to generate SQL
      2. Validate + execute (with up to 1 retry on failure)
      3. Log the result
      4. Return structured output

    Returns:
    {
        "question":     str,
        "sql":          str,
        "status":       "success" | "error" | "blocked",
        "rows":         [...],
        "row_count":    int,
        "error":        str | None,
        "retried":      bool,
        "latency_ms":   float,
    }
    """
    # Step 1: Generate SQL with Gemini
    try:
        sql = sql_generator.generate_sql(question)
    except Exception as e:
        result = {
            "question": question,
            "sql": "",
            "original_sql": "",
            "retry_sql": None,
            "status": "error",
            "rows": [],
            "row_count": 0,
            "error": f"SQL generation failed: {e}",
            "retried": False,
            "latency_ms": 0.0,
        }
        logger.log_query(result)
        return result

    # Step 2: Execute with retry
    result = executor.run_with_retry(question=question, sql=sql)

    # Step 3: Log everything
    logger.log_query(result)

    return result


def format_answer(result: dict) -> str:
    """
    Produces a human-readable summary of the pipeline result.
    """
    q = result["question"]
    status = result["status"]
    rows = result["rows"]
    row_count = result["row_count"]
    sql = result["sql"]
    error = result["error"]
    latency = result["latency_ms"]
    retried = result["retried"]

    lines = [
        f"Question : {q}",
        f"Status   : {status.upper()}",
        f"SQL      : {sql}",
    ]

    if retried:
        lines.append(f"Retried  : Yes (original failed, LLM fixed and retried)")

    if status == "success":
        lines.append(f"Rows     : {row_count}")
        if rows:
            # Show column headers
            headers = list(rows[0].keys())
            lines.append("  " + " | ".join(headers))
            lines.append("  " + "-" * 60)
            for row in rows[:10]:  # show max 10 rows in terminal
                lines.append("  " + " | ".join(str(v) for v in row.values()))
            if row_count > 10:
                lines.append(f"  ... ({row_count - 10} more rows not shown)")
    else:
        lines.append(f"Error    : {error}")

    lines.append(f"Latency  : {latency} ms")
    return "\n".join(lines)
