import json
import time
from text_to_sql.sql_generator import (
    generate_sql,
    fix_sql,
    _call_gemini_with_retry,
    SCHEMA_CONTEXT
)
from text_to_sql.database import execute_query
from text_to_sql.validator import validate_sql
from logger import get_logger

logger = get_logger(__name__)

DECOMPOSE_PROMPT = """{schema}

== YOUR TASK ==
Decompose the following natural language question into structured parts to prepare for SQL generation.

Identify:
- Intent (what is being asked)
- Tables involved
- Columns needed
- Filters/conditions
- Joins (if any)

Output a JSON object ONLY, with the following keys: intent, tables, columns, filters, joins.
Do not use markdown formatting.

Question: {question}
"""

SUMMARIZE_PROMPT = """
You are a helpful data assistant.
Given a user's original question and the structured JSON results from a PostgreSQL query, write a brief, human-readable summary of the answer.
If the result is a number, explicitly state it. Do not include raw JSON or SQL in your answer.

Question: {question}
Result: {result}
"""

def run_agent(question: str) -> dict:
    """
    Executes the full agent loop for Task 4.
    """
    logger.info(f"Agent started for question: '{question}'")
    
    # Step 1: Decompose
    logger.info("Step 1: Decomposing question...")
    decompose_text = _call_gemini_with_retry(
        DECOMPOSE_PROMPT.format(schema=SCHEMA_CONTEXT, question=question)
    )
    logger.info(f"Decomposition result: {decompose_text[:100]}...")
    
    # Step 2: Generate SQL
    logger.info("Step 2: Generating SQL...")
    sql = generate_sql(question)
    
    # Step 3 & 4: Validate, Execute, and Retry Loop
    max_retries = 3
    attempt = 0
    result_data = None
    final_sql = sql
    error_msg = None
    
    while attempt <= max_retries:
        logger.info(f"Step 3/4 (Attempt {attempt+1}): Executing SQL: {final_sql}")
        
        # Validate
        val = validate_sql(final_sql)
        if not val["valid"]:
            error_msg = val["reason"]
            break # Safety error, don't retry
            
        # Execute
        db_res = execute_query(final_sql)
        if db_res["status"] == "success":
            result_data = db_res["rows"]
            error_msg = None
            
            # If the output is just one row with one key and it's a number, extract it for simplicity
            if len(result_data) == 1 and len(result_data[0]) == 1:
                val = list(result_data[0].values())[0]
                if isinstance(val, (int, float)):
                    result_data = val
            break
        else:
            error_msg = db_res["error"]
            logger.warning(f"Execution failed: {error_msg}")
            if attempt < max_retries:
                logger.info("Attempting to fix SQL...")
                final_sql = fix_sql(final_sql, error_msg)
            attempt += 1
            
    if error_msg:
        # Fallback if all retries fail
        logger.error(f"Agent failed after {max_retries} retries: {error_msg}")
        return {
            "sql": final_sql,
            "result": None,
            "summary": "I'm sorry, I was unable to retrieve the data due to a database error. Please try rephrasing your question.",
            "status": "error",
            "error": error_msg
        }
        
    # Step 5: Final Output / Summarize
    logger.info("Step 5: Summarizing result...")
    summary = _call_gemini_with_retry(
        SUMMARIZE_PROMPT.format(question=question, result=json.dumps(result_data))
    ).strip()
    
    logger.info("Agent successfully completed task.")
    return {
        "sql": final_sql,
        "result": result_data,
        "summary": summary,
        "status": "success",
        "error": None
    }
