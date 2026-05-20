# Text-to-SQL Pipeline — Architecture & Design

## Overview

The pipeline is built in **5 layers** that each have a single responsibility.
A natural language question flows through all 5 layers and exits as a structured JSON result.

```
Natural Language Question
        │
        ▼
┌─────────────────────┐
│   sql_generator.py  │  ← Calls Gemini LLM to write SQL
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│    validator.py     │  ← Blocks any non-SELECT statement
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│    executor.py      │  ← Runs SQL against PostgreSQL
└─────────────────────┘
        │  (if error)
        ▼
┌─────────────────────┐
│  sql_generator.py   │  ← Gemini fixes the broken SQL (1 retry max)
│  (fix_sql prompt)   │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│     logger.py       │  ← Writes JSON entry to logs/query_log.jsonl
└─────────────────────┘
        │
        ▼
  Structured Result
```

---

## Module Descriptions

### `sql_generator.py` — LLM SQL Generation
- Uses **Google Gemini (gemini-1.5-flash)** as the LLM backend
- The entire database schema (all 8 tables, all columns, all foreign keys) is injected into every prompt as a system context so the model never guesses about column names
- A `generate_sql(question)` prompt asks for a SELECT query only
- A `fix_sql(sql, error)` prompt gives Gemini the broken SQL + the Postgres error message and asks it to correct the issue
- Both prompts strip markdown code fences from the output before returning

### `validator.py` — SQL Safety Guard
- Checks that the generated SQL starts with `SELECT`
- Scans for dangerous keywords: `DROP`, `DELETE`, `INSERT`, `UPDATE`, `TRUNCATE`, `ALTER`, `CREATE`, etc.
- Any blocked query gets a `"blocked"` status and never reaches the database

### `executor.py` — Execute with Retry
- Calls `validator.py` first
- Runs the query using `database.py`
- If execution fails, calls `sql_generator.fix_sql()` with the error message
- Retries the fixed SQL **once** (maximum 1 retry as required)
- Returns a structured result dict with status, rows, error, and latency

### `logger.py` — Structured Logging
- Every query attempt is written to `text_to_sql/logs/query_log.jsonl`
- Each log entry is a JSON object with: timestamp, original SQL, final SQL, retry info, status, row count, error, and latency
- JSONL format means one entry per line — easy to grep and parse

### `pipeline.py` — Orchestrator
- Ties all modules together into a single `run_pipeline(question)` call
- Also provides `format_answer(result)` for human-readable terminal output

### `benchmark.py` — Evaluation Runner
- Runs all 50 benchmark questions through the pipeline
- Computes metrics: execution success rate, retry rate, retry success rate, average latency
- Saves a full report to `logs/benchmark_report.json`

---

## Design Decisions

### Why Gemini?
Gemini 1.5 Flash is fast, has a generous free tier, and is available via Google AI Studio. It handles complex SQL generation well when given a clear schema context.

### Why inject the full schema into every prompt?
LLMs hallucinate column names easily. By always providing the exact table structure, we eliminate most schema-mismatch errors. The double-quote requirement for camelCase columns is explicitly called out in the prompt.

### Why 1 retry max?
The assignment specifies maximum 1 retry. In practice, one LLM correction round is enough to fix most syntax errors and wrong column name issues. Adding more retries would increase latency and cost.

### Why psycopg2 instead of SQLAlchemy?
The existing FastAPI app uses async SQLAlchemy. For this pipeline, a synchronous tool is simpler and more portable. psycopg2 directly maps to how you'd write database scripts in real data engineering workflows.

---

## How to Run

### Setup
```bash
# 1. Add your Gemini API key to .env
echo "GEMINI_API_KEY=your_key_here" >> .env

# 2. Make sure venv is active and deps are installed
source venv/bin/activate
pip install -r requirements.txt

# 3. Start the database
docker compose up -d
```

### Single Question
```bash
python -m text_to_sql.main "How many customers are from the USA?"
```

### Interactive Mode
```bash
python -m text_to_sql.main
```

### Run Full Benchmark (all 50 questions)
```bash
python -m text_to_sql.main --benchmark
```

---

## Example Outputs

### Successful Query

```
Question : How many customers are from the USA?
Status   : SUCCESS
SQL      : SELECT COUNT(*) AS "totalCustomers" FROM customers WHERE "country" = 'USA'
Rows     : 1
  totalCustomers
  ────────────────────────────────────────────────────────────
  36
Latency  : 1243.5 ms
```

### Failed Query with Successful Retry

```
Question : Get employees and their manager
Status   : SUCCESS
SQL      : SELECT emp."firstName" || ' ' || emp."lastName" AS "employeeName", ...
Retried  : Yes (original failed, LLM fixed and retried)
Rows     : 23
Latency  : 2871.2 ms
```

### Blocked Query (safety guard)

```
Question : DELETE FROM customers
Status   : BLOCKED
Error    : Only SELECT queries are allowed. Query starts with: 'DELETE'
```
