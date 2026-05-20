"""
text_to_sql/benchmark.py
=========================
Benchmark runner: tests the Text-to-SQL pipeline against all 50 questions
from the dataset and produces an evaluation report.

Usage:
    python -m text_to_sql.benchmark

Output:
    - Prints a summary table to the terminal
    - Saves a full JSON report to logs/benchmark_report.json
"""

import json
import os
import time
from datetime import datetime

from text_to_sql.pipeline import run_pipeline

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
REPORT_FILE = os.path.join(LOG_DIR, "benchmark_report.json")

# ── The 50 benchmark questions ────────────────────────────────────────────────
BENCHMARK_QUESTIONS = [
    # Part A: Simple SELECT
    "List all products",
    "Get all customers",
    "Show all orders",
    "List all employees",
    "Get all offices",
    "Show all product lines",
    "List all payments",
    "Get product names and prices",
    "Get customer names and cities",
    "List employee first and last names",
    "Get all order dates",
    "Show product vendor list",
    "Get all product codes",
    "List all countries from offices",
    "Show all order statuses",
    "Get all payment amounts",
    "List all job titles",
    "Get customer phone numbers",
    "Show product MSRP values",
    "List order numbers",
    # Part B: JOINs
    "Get orders with customer names",
    "Get employees with office city",
    "Get payments with customer names",
    "Get order details with product names",
    "Get products with product line description",
    "Get customers with sales rep names",
    "Get orders with customer city",
    "Get employees and their manager",
    "Get orderdetails with product vendor",
    "Get payments with customer country",
    # Part C: Aggregations
    "Count customers per country",
    "Total payments per customer",
    "Number of orders per status",
    "Products per product line",
    "Employees per office",
    "Total stock per product vendor",
    "Average buy price per product line",
    "Orders per customer",
    "Max MSRP per product line",
    "Min buy price per vendor",
    # Part D: Summary stats
    "Total number of customers",
    "Total number of products",
    "Total revenue from payments",
    "Average product price",
    "Max payment amount",
    "Min payment amount",
    "Count total orders",
    "Total quantity in stock",
    "Average MSRP",
    "Number of employees",
]


def run_benchmark(delay_seconds: float = 1.0) -> dict:
    """
    Runs the pipeline against every benchmark question.

    Args:
        delay_seconds: Pause between questions to avoid rate-limiting the LLM.

    Returns:
        A full report dict containing per-question results and summary metrics.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    print("=" * 70)
    print("  TEXT-TO-SQL BENCHMARK RUNNER")
    print(f"  Questions: {len(BENCHMARK_QUESTIONS)}")
    print(f"  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()

    results = []
    total = len(BENCHMARK_QUESTIONS)

    for i, question in enumerate(BENCHMARK_QUESTIONS, start=1):
        print(f"[{i:02d}/{total}] {question}", end="  →  ", flush=True)

        result = run_pipeline(question)

        status = result["status"]
        retried = "🔁 retried" if result.get("retried") else ""
        row_count = result.get("row_count", 0)

        if status == "success":
            print(f"✅ SUCCESS  ({row_count} rows)  {retried}")
        elif status == "blocked":
            print(f"🚫 BLOCKED  {retried}")
        else:
            print(f"❌ ERROR    {retried}")
            print(f"          Error: {result.get('error', '')[:100]}")

        results.append({
            "id": i,
            "question": question,
            "status": status,
            "sql": result.get("sql"),
            "original_sql": result.get("original_sql"),
            "retried": result.get("retried", False),
            "retry_sql": result.get("retry_sql"),
            "row_count": row_count,
            "error": result.get("error"),
            "latency_ms": result.get("latency_ms", 0.0),
        })

        # Small delay to respect Gemini API rate limits
        if i < total:
            time.sleep(delay_seconds)

    # ── Compute metrics ───────────────────────────────────────────────────────
    success_count  = sum(1 for r in results if r["status"] == "success")
    error_count    = sum(1 for r in results if r["status"] == "error")
    blocked_count  = sum(1 for r in results if r["status"] == "blocked")
    retried_count  = sum(1 for r in results if r["retried"])
    retry_success  = sum(1 for r in results if r["retried"] and r["status"] == "success")

    latencies = [r["latency_ms"] for r in results if r["latency_ms"] > 0]
    avg_latency = round(sum(latencies) / len(latencies), 2) if latencies else 0.0

    execution_success_rate = round((success_count / total) * 100, 1)
    retry_success_rate = round((retry_success / retried_count) * 100, 1) if retried_count else 0.0

    report = {
        "generated_at": datetime.now().isoformat(),
        "total_questions": total,
        "metrics": {
            "execution_success_rate_pct": execution_success_rate,
            "success_count": success_count,
            "error_count": error_count,
            "blocked_count": blocked_count,
            "retried_count": retried_count,
            "retry_success_count": retry_success,
            "retry_success_rate_pct": retry_success_rate,
            "avg_latency_ms": avg_latency,
        },
        "results": results,
    }

    # ── Print summary ─────────────────────────────────────────────────────────
    print()
    print("=" * 70)
    print("  BENCHMARK SUMMARY")
    print("=" * 70)
    print(f"  Total Questions        : {total}")
    print(f"  Successful             : {success_count}  ({execution_success_rate}%)")
    print(f"  Errors                 : {error_count}")
    print(f"  Blocked (unsafe SQL)   : {blocked_count}")
    print(f"  Queries retried        : {retried_count}")
    print(f"  Retry success rate     : {retry_success_rate}%")
    print(f"  Average latency        : {avg_latency} ms")
    print("=" * 70)

    # ── Save full report ──────────────────────────────────────────────────────
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n  Full report saved to: {REPORT_FILE}")
    print()

    return report


if __name__ == "__main__":
    run_benchmark()
