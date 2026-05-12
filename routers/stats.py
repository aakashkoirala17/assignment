"""
routers/stats.py — Aggregated Database Statistics
==================================================
Uses asyncio.gather to query all table counts concurrently in one request.
"""

import asyncio
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database import get_db
from logger import get_logger
from models.all_models import (
    Customer, Employee, Office, Order, OrderDetail, Payment, Product, ProductLine,
)

logger = get_logger(__name__)
router = APIRouter(prefix="/stats", tags=["Statistics"])


async def _count(db: AsyncSession, model) -> int:
    """Run a COUNT(*) query for any model table."""
    result = await db.execute(select(func.count()).select_from(model))
    return result.scalar()


@router.get(
    "/aggregated",
    summary="Aggregated row counts for all tables",
    description="Returns the row count for every table in a single request using concurrent queries.",
)
async def get_aggregated_stats(db: AsyncSession = Depends(get_db)):
    logger.info("GET /stats/aggregated — fetching counts for all tables concurrently")

    models = {
        "customers":    Customer,
        "employees":    Employee,
        "offices":      Office,
        "orders":       Order,
        "orderdetails": OrderDetail,
        "payments":     Payment,
        "products":     Product,
        "productlines": ProductLine,
    }

    results = await asyncio.gather(*[_count(db, m) for m in models.values()])
    stats = dict(zip(models.keys(), results))

    logger.info("GET /stats/aggregated — results: %s", stats)
    return stats


@router.get("/employees/count", summary="Count of employees")
async def get_employee_count(db: AsyncSession = Depends(get_db)):
    logger.info("GET /stats/employees/count")
    return {"count": await _count(db, Employee)}


@router.get("/offices/count", summary="Count of offices")
async def get_office_count(db: AsyncSession = Depends(get_db)):
    logger.info("GET /stats/offices/count")
    return {"count": await _count(db, Office)}


@router.get("/orders/count", summary="Count of orders")
async def get_order_count(db: AsyncSession = Depends(get_db)):
    logger.info("GET /stats/orders/count")
    return {"count": await _count(db, Order)}


@router.get("/products/count", summary="Count of products")
async def get_product_count(db: AsyncSession = Depends(get_db)):
    logger.info("GET /stats/products/count")
    return {"count": await _count(db, Product)}
