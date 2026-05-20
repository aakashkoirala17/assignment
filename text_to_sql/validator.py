"""
text_to_sql/validator.py
=========================
SQL Safety Validator.

Ensures that only safe read-only SELECT queries are allowed.
Blocks any attempt to modify or delete data (DML/DDL statements).
"""

import re

# Blocked SQL keywords — none of these should appear at the start of a statement
BLOCKED_KEYWORDS = [
    r"\bDROP\b",
    r"\bDELETE\b",
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"\bTRUNCATE\b",
    r"\bALTER\b",
    r"\bCREATE\b",
    r"\bREPLACE\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bEXECUTE\b",
    r"\bEXEC\b",
    r"\bCALL\b",
]


def validate_sql(sql: str) -> dict:
    """
    Validates that the SQL query is safe to execute.

    Returns:
        {
            "valid": bool,
            "reason": str | None   # None if valid, explanation if blocked
        }
    """
    if not sql or not sql.strip():
        return {"valid": False, "reason": "SQL query is empty."}

    sql_upper = sql.upper().strip()

    # Must start with SELECT
    if not sql_upper.startswith("SELECT"):
        return {
            "valid": False,
            "reason": f"Only SELECT queries are allowed. Query starts with: '{sql.strip().split()[0]}'",
        }

    # Check for any blocked keyword anywhere in the query
    for pattern in BLOCKED_KEYWORDS:
        if re.search(pattern, sql_upper):
            keyword = re.search(pattern, sql_upper).group(0)
            return {
                "valid": False,
                "reason": f"Blocked keyword detected: '{keyword}'. Only SELECT statements are permitted.",
            }

    return {"valid": True, "reason": None}
