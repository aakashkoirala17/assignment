"""
crud/customer.py — The Kitchen Layer
=====================================
This module is the ONLY place that talks to the database.
It never makes HTTP calls or imports from routers/.

Each function represents one operation:
  create_customer  → INSERT
  get_customer     → SELECT by PK (with orders + payments)
  get_customers    → SELECT paginated list
  update_customer  → UPDATE partial fields
  delete_customer  → DELETE by PK

SQLAlchemy's async ORM keeps our queries in Python; swapping the
database engine (Factor IV) requires zero changes here.
"""

from typing import Optional
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from logger import get_logger
from models.all_models import Customer, Order, Payment
from schemas.customer import CustomerCreate, CustomerUpdate

logger = get_logger(__name__)


# ── CREATE ─────────────────────────────────────────────────────────────────────

async def create_customer(db: AsyncSession, data: CustomerCreate) -> Customer:
    """
    Insert a new customer row.
    If customerNumber is not provided (Step 4), we find the next available ID.
    Raises ValueError if a provided customerNumber already exists.
    """
    customer_data = data.model_dump(exclude_none=True)
    
    if "customerNumber" not in customer_data:
        logger.info("customerNumber not provided, generating automatically...")
        result = await db.execute(select(func.max(Customer.customerNumber)))
        max_id = result.scalar() or 0
        customer_data["customerNumber"] = max_id + 1
        logger.info("Generated new customerNumber: %s", customer_data["customerNumber"])

    logger.info("CREATE customer: customerNumber=%s name='%s'",
                customer_data["customerNumber"], data.customerName)

    # Check for duplicate PK
    existing = await db.get(Customer, customer_data["customerNumber"])
    if existing:
        logger.warning("Create failed — customerNumber %s already exists", customer_data["customerNumber"])
        raise ValueError(f"Customer with customerNumber {customer_data['customerNumber']} already exists")

    customer = Customer(**customer_data)
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    logger.info("Customer %s created successfully", customer.customerNumber)
    return customer


# ── READ (single) ──────────────────────────────────────────────────────────────

async def get_customer(db: AsyncSession, customer_number: int) -> Optional[Customer]:
    """
    Fetch a single customer by primary key, eagerly loading their
    related orders and payments so the router can return them together.
    Returns None if the customer does not exist.
    """
    logger.info("READ customer: customerNumber=%s", customer_number)

    result = await db.execute(
        select(Customer)
        .options(
            selectinload(Customer.orders),
            selectinload(Customer.payments),
        )
        .where(Customer.customerNumber == customer_number)
    )
    customer = result.scalar_one_or_none()

    if customer is None:
        logger.warning("Customer not found: customerNumber=%s", customer_number)
    else:
        logger.info("Customer %s retrieved (orders=%d payments=%d)",
                    customer_number,
                    len(customer.orders),
                    len(customer.payments))
    return customer


# ── READ (list) ────────────────────────────────────────────────────────────────

async def get_customers(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
) -> list[Customer]:
    """
    Return a paginated list of customers.
    skip  — how many rows to pass over (offset)
    limit — how many rows to return (page size)
    """
    logger.info("READ customers list: skip=%d limit=%d", skip, limit)

    result = await db.execute(
        select(Customer)
        .options(
            selectinload(Customer.orders),
            selectinload(Customer.payments),
        )
        .offset(skip)
        .limit(limit)
        .order_by(Customer.customerNumber)
    )
    customers = list(result.scalars().all())
    logger.info("Returned %d customers", len(customers))
    return customers


# ── UPDATE ─────────────────────────────────────────────────────────────────────

async def update_customer(
    db: AsyncSession,
    customer_number: int,
    data: CustomerUpdate,
) -> Optional[Customer]:
    """
    Partially update a customer.
    Only fields that are explicitly set in the request body are changed;
    omitted fields keep their current database values.
    Returns None if the customer does not exist.
    """
    logger.info("UPDATE customer: customerNumber=%s fields=%s",
                customer_number, list(data.model_dump(exclude_none=True).keys()))

    customer = await db.get(Customer, customer_number)
    if customer is None:
        logger.warning("Update failed — Customer not found: customerNumber=%s", customer_number)
        return None

    update_data = data.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(customer, field, value)

    await db.commit()
    await db.refresh(customer)
    logger.info("Customer %s updated successfully", customer_number)
    return customer


# ── DELETE ─────────────────────────────────────────────────────────────────────

async def delete_customer(db: AsyncSession, customer_number: int) -> bool:
    """
    Delete a customer by primary key.
    Returns True if deleted, False if the customer was not found.
    """
    logger.info("DELETE customer: customerNumber=%s", customer_number)

    customer = await db.get(Customer, customer_number)
    if customer is None:
        logger.warning("Delete failed — Customer not found: customerNumber=%s", customer_number)
        return False

    await db.execute(delete(Customer).where(Customer.customerNumber == customer_number))
    await db.commit()
    logger.info("Customer %s deleted successfully", customer_number)
    return True
