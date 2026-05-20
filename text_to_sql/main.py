"""
text_to_sql/main.py
====================
CLI entry point for the Text-to-SQL pipeline.

Usage:
    # Ask a single question interactively:
    python -m text_to_sql.main

    # Ask a single question directly:
    python -m text_to_sql.main "How many customers are from France?"

    # Run the full benchmark:
    python -m text_to_sql.main --benchmark
"""

import sys
import json
from text_to_sql.pipeline import run_pipeline, format_answer


def ask(question: str):
    """Run the pipeline for one question and pretty-print the result."""
    print()
    print("─" * 70)
    result = run_pipeline(question)
    print(format_answer(result))
    print("─" * 70)
    print()
    return result


def interactive_mode():
    """REPL loop: keep asking for questions until the user types 'exit'."""
    print("=" * 70)
    print("  TEXT-TO-SQL AGENT  (Classic Models Database)")
    print("  Type your question in plain English.")
    print("  Type 'exit' or press Ctrl+C to quit.")
    print("=" * 70)
    print()

    while True:
        try:
            question = input("Your question: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not question:
            continue

        if question.lower() in ("exit", "quit", "q"):
            print("Goodbye!")
            break

        ask(question)


def main():
    args = sys.argv[1:]

    if not args:
        interactive_mode()
        return

    if args[0] == "--benchmark":
        from text_to_sql.benchmark import run_benchmark
        run_benchmark()
        return

    if args[0] == "--help":
        print(__doc__)
        return

    # Treat all args joined as the question
    question = " ".join(args)
    result = ask(question)

    # Exit with code 1 if the query failed (useful for scripts/CI)
    if result["status"] != "success":
        sys.exit(1)


if __name__ == "__main__":
    main()
