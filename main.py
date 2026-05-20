"""
main.py — Application Entry Point
===================================
Registers all routers and starts the FastAPI app.
Visit http://localhost:8000/docs for interactive Swagger UI.
"""

from fastapi import FastAPI
from logger import get_logger
from routers import customers, stats, agent

logger = get_logger(__name__)

app = FastAPI(
    title="Classic Models Customer API",
    description=(
        "A layered FastAPI application for the Classic Models database.\n\n"
        "**Layers:**\n"
        "- `database.py` — connection & session management\n"
        "- `schemas/` — Pydantic validation blueprints\n"
        "- `crud/` — database operations (Create, Read, Update, Delete)\n"
        "- `routers/` — HTTP endpoints (Front Desk)\n"
        "- `logger.py` — centralised logging across all layers\n\n"
        "Built following the **Twelve-Factor App** methodology."
    ),
    version="1.0.0",
    contact={"name": "Classic Models Team"},
)

# ── Register routers ──────────────────────────────────────────────────────────
app.include_router(customers.router)
app.include_router(stats.router)
app.include_router(agent.router)

logger.info("Classic Models API started — routers registered: /customers, /stats, /agent")


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    logger.info("GET / — health check")
    return {
        "status": "ok",
        "message": "Welcome to the Classic Models API.",
        "docs": "http://localhost:8000/docs",
    }
