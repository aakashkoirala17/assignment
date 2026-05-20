"""
text_to_sql/sql_generator.py
=============================
LLM-based SQL Generator using Google Gemini.

Uses a two-prompt strategy:
  Prompt 1 (generate): Convert a natural language question to SQL
  Prompt 2 (fix):      Given an error + broken SQL, produce a corrected version

The full database schema is injected into every prompt as context so the
model knows exactly which tables, columns, and relationships exist.
"""

import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

MODEL_NAME = "gemini-1.5-flash"

# ── Database Schema Context ──────────────────────────────────────────────────
# Injected into every prompt so the model knows the exact schema.

SCHEMA_CONTEXT = """
You are a PostgreSQL SQL expert working with the Classic Models database.

CRITICAL RULE: All column names in this database use camelCase and MUST be
wrapped in double quotes in every query. For example:
  ✓ "customerNumber", "productLine", "orderDate", "buyPrice"
  ✗ customerNumber, productLine, orderDate, buyPrice (WRONG — Postgres folds to lowercase)

Table names are lowercase and do NOT need quotes.

== DATABASE SCHEMA ==

TABLE: customers
  "customerNumber"         INTEGER  PRIMARY KEY
  "customerName"           VARCHAR
  "contactLastName"        VARCHAR
  "contactFirstName"       VARCHAR
  "phone"                  VARCHAR
  "addressLine1"           VARCHAR
  "addressLine2"           VARCHAR
  "city"                   VARCHAR
  "state"                  VARCHAR
  "postalCode"             VARCHAR
  "country"                VARCHAR
  "salesRepEmployeeNumber" INTEGER  FK → employees("employeeNumber")
  "creditLimit"            NUMERIC

TABLE: employees
  "employeeNumber" INTEGER  PRIMARY KEY
  "lastName"       VARCHAR
  "firstName"      VARCHAR
  "extension"      VARCHAR
  "email"          VARCHAR
  "officeCode"     VARCHAR  FK → offices("officeCode")
  "reportsTo"      INTEGER  FK → employees("employeeNumber")  [self-join for manager]
  "jobTitle"       VARCHAR

TABLE: offices
  "officeCode"   VARCHAR  PRIMARY KEY
  "city"         VARCHAR
  "phone"        VARCHAR
  "addressLine1" VARCHAR
  "addressLine2" VARCHAR
  "state"        VARCHAR
  "country"      VARCHAR
  "postalCode"   VARCHAR
  "territory"    VARCHAR

TABLE: orders
  "orderNumber"    INTEGER  PRIMARY KEY
  "orderDate"      DATE
  "requiredDate"   DATE
  "shippedDate"    DATE
  "status"         VARCHAR  (values: Shipped, Cancelled, In Process, On Hold, Disputed, Resolved)
  "comments"       TEXT
  "customerNumber" INTEGER  FK → customers("customerNumber")

TABLE: orderdetails
  "orderNumber"     INTEGER  FK → orders("orderNumber")
  "productCode"     VARCHAR  FK → products("productCode")
  "quantityOrdered" INTEGER
  "priceEach"       NUMERIC
  "orderLineNumber" SMALLINT
  PRIMARY KEY ("orderNumber", "productCode")

TABLE: payments
  "customerNumber" INTEGER  FK → customers("customerNumber")
  "checkNumber"    VARCHAR
  "paymentDate"    DATE
  "amount"         NUMERIC
  PRIMARY KEY ("customerNumber", "checkNumber")

TABLE: products
  "productCode"        VARCHAR  PRIMARY KEY
  "productName"        VARCHAR
  "productLine"        VARCHAR  FK → productlines("productLine")
  "productScale"       VARCHAR
  "productVendor"      VARCHAR
  "productDescription" TEXT
  "quantityInStock"    INTEGER
  "buyPrice"           NUMERIC
  "MSRP"               NUMERIC

TABLE: productlines
  "productLine"     VARCHAR  PRIMARY KEY
  "textDescription" VARCHAR
  "htmlDescription" TEXT
  "image"           BYTEA
"""

GENERATE_PROMPT_TEMPLATE = """{schema}

== YOUR TASK ==
Convert the following natural language question into a valid PostgreSQL SELECT query.

RULES:
- Output ONLY the raw SQL query. No markdown, no explanation, no code fences.
- Use double quotes around ALL column names.
- Use table aliases (e.g. c for customers, o for orders) when joining tables.
- Add LIMIT 100 to queries that could return many rows, unless the question asks for aggregation.
- Never generate DELETE, INSERT, UPDATE, DROP, or any non-SELECT statement.

Question: {question}

SQL:"""

FIX_PROMPT_TEMPLATE = """{schema}

== YOUR TASK ==
The SQL query below failed when executed against PostgreSQL.
Fix it so it runs correctly.

RULES:
- Output ONLY the corrected SQL. No markdown, no explanation, no code fences.
- Remember: ALL column names must be wrapped in double quotes.
- Fix syntax errors, wrong column names, and missing JOIN conditions.

Failed SQL:
{sql}

Error Message:
{error}

Corrected SQL:"""


def _clean_sql(raw: str) -> str:
    """Strip markdown fences and extra whitespace from LLM output."""
    # Remove ```sql ... ``` or ``` ... ``` blocks
    raw = re.sub(r"```(?:sql)?", "", raw, flags=re.IGNORECASE)
    raw = raw.strip().strip("`").strip()
    return raw


def generate_sql(question: str) -> str:
    """
    Calls Gemini to generate a SQL query for the given NL question.
    Returns the raw SQL string.
    """
    prompt = GENERATE_PROMPT_TEMPLATE.format(
        schema=SCHEMA_CONTEXT,
        question=question,
    )
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return _clean_sql(response.text)


def fix_sql(sql: str, error: str) -> str:
    """
    Calls Gemini to fix a broken SQL query given the error message.
    Returns the corrected SQL string.
    """
    prompt = FIX_PROMPT_TEMPLATE.format(
        schema=SCHEMA_CONTEXT,
        sql=sql,
        error=error,
    )
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return _clean_sql(response.text)
