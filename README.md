# Classic Models — FastAPI + Text-to-SQL Assignment

A layered FastAPI application built on top of the Classic Models PostgreSQL database, submitted as part of the **Text-to-SQL Agent** coursework.

---

## Project Structure

```
.
├── main.py                     # FastAPI app entry point
├── database.py                 # Async SQLAlchemy connection & session
├── logger.py                   # Centralised logging (Twelve-Factor)
├── docker-compose.yml          # PostgreSQL container setup
├── requirements.txt            # Python dependencies
├── seed.sql                    # Database schema + sample data
│
├── models/                     # SQLAlchemy ORM table definitions
├── schemas/                    # Pydantic request/response models
├── crud/                       # Database query logic (CRUD layer)
├── GROUND_TRUTH_QUERIES.md     # Task 1 Part 1: All 50 benchmark SQL queries
├── EVALUATION_STRATEGY.md      # Task 1 Part 2: Evaluation framework design
├── QUERY_DECOMPOSITION.md      # Task 2: Structured decomposition of questions
│
├── text_to_sql/                # Task 3 & 4: Text-to-SQL Pipeline & AI Agent
│   ├── ARCHITECTURE.md         # Detailed design docs for the pipeline
│   ├── pipeline.py             # Task 3 Core pipeline
│   ├── benchmark.py            # Task 3 Automated evaluator
│   └── agent.py                # Task 4 SQL Agent logic with retries
│
├── routers/                    # FastAPI route handlers
│   ├── customers.py
│   ├── stats.py
│   └── agent.py                # Task 4 Agent POST endpoint
├── PYTHON_COMMANDS.md          # Setup guide: venv, pip, uvicorn
├── DOCKER_COMMANDS.md          # Setup guide: docker-compose, psql
└── POSTGRES_COMMANDS.md        # PostgreSQL query reference
```

---

## Getting Started

### 1. Start the Database

Make sure Docker Desktop is running, then:

```bash
docker-compose up -d
```

This will spin up a PostgreSQL container and automatically load all tables and data from `seed.sql`.

### 2. Set Up Python Environment

```bash
python3 -m venv venv
source venv/bin/activate       # macOS/Linux
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the API

```bash
uvicorn main:app --reload
```

Open your browser at:
- **API Docs (Swagger):** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/

---

## Deliverables

| File/Module | Task | Description |
| :--- | :--- | :--- |
| `GROUND_TRUTH_QUERIES.md` | Task 1 | 50 natural language questions with hand-written SQL queries |
| `EVALUATION_STRATEGY.md` | Task 1 | Proposed framework for evaluating a Text-to-SQL agent system |
| `QUERY_DECOMPOSITION.md` | Task 2 | Structured decomposition of all 50 questions |
| `text_to_sql/ARCHITECTURE.md` | Task 3 | Design docs for the Text-to-SQL pipeline layers |
| `text_to_sql/` module | Task 3 | The fully automated, LLM-powered SQL generation & execution pipeline |
| `text_to_sql/benchmark.py` | Task 3 | Benchmark runner outputting metrics to `logs/benchmark_report.json` |
| `text_to_sql/agent.py` | Task 4 | Core agent loop (Decompose → Generate → Execute → Retry → Summarize) |
| `routers/agent.py` | Task 4 | `POST /agent/sql` FastAPI endpoint exposing the mini SQL agent |

---

## Database Schema

The Classic Models database contains 8 tables:

| Table | Description |
| :--- | :--- |
| `customers` | Customer details and credit limits |
| `employees` | Employee info with manager hierarchy |
| `offices` | Office locations worldwide |
| `orders` | Customer orders and statuses |
| `orderdetails` | Line items per order |
| `payments` | Customer payment history |
| `products` | Product catalog with pricing |
| `productlines` | Product category descriptions |

> **Note:** All column names use camelCase and must be wrapped in double quotes in PostgreSQL queries (e.g. `"customerName"`, `"productLine"`).

---

## Design Principles (Twelve-Factor App)

- **Config (Factor III):** All secrets stored in `.env`, never hardcoded
- **Backing Services (Factor IV):** PostgreSQL runs as an independent Docker service
- **Dev/Prod Parity (Factor X):** Same Docker image and seed data used in all environments
