"""
routers/customers.py — The Front Desk Layer
============================================
Handles all HTTP requests for the /customers resource.
Each endpoint:
  1. Logs the incoming request
  2. Calls the appropriate crud.py function (never touches the DB directly)
  3. Logs and returns the response, or raises an HTTPException on error

Endpoints
---------
GET  /customers/              → paginated list of customers
GET  /customers/{id}          → single customer with orders & payments
POST /customers/              → create a new customer
PUT  /customers/{id}          → partially update a customer
DELETE /customers/{id}        → delete a customer
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from logger import get_logger
import crud.customer as customer_crud
from schemas.customer import CustomerCreate, CustomerOut, CustomerUpdate

logger = get_logger(__name__)

router = APIRouter(prefix="/customers", tags=["Customers"])


# ── GET /customers/ ────────────────────────────────────────────────────────────

@router.get(
    "/",
    response_model=List[CustomerOut],
    summary="List customers (paginated)",
    description=(
        "Returns a paginated list of customers. "
        "Use **skip** to offset and **limit** to control page size."
    ),
)
async def list_customers(
    skip: int  = Query(default=0,  ge=0,  description="Number of records to skip"),
    limit: int = Query(default=10, ge=1, le=200, description="Max records to return"),
    db: AsyncSession = Depends(get_db),
):
    logger.info("GET /customers/ — skip=%d limit=%d", skip, limit)
    customers = await customer_crud.get_customers(db, skip=skip, limit=limit)
    logger.info("GET /customers/ — returning %d customers", len(customers))
    return customers


# ── GET /customers/{customer_number} ──────────────────────────────────────────

@router.get(
    "/{customer_number}",
    response_model=CustomerOut,
    summary="Get a single customer",
    description=(
        "Fetch a customer by their unique customerNumber. "
        "The response includes their full order history and payment records. "
        "Returns **404** if the customer does not exist."
    ),
)
async def get_customer(
    customer_number: int,
    db: AsyncSession = Depends(get_db),
):
    logger.info("GET /customers/%d — requested", customer_number)
    customer = await customer_crud.get_customer(db, customer_number)

    if customer is None:
        logger.warning("GET /customers/%d — 404 Not Found", customer_number)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with customerNumber {customer_number} not found",
        )

    logger.info(
        "GET /customers/%d — found '%s', orders=%d payments=%d",
        customer_number,
        customer.customerName,
        len(customer.orders),
        len(customer.payments),
    )
    return customer


# ── POST /customers/ ───────────────────────────────────────────────────────────

@router.post(
    "/",
    response_model=CustomerOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new customer",
    description=(
        "Create a new customer record. The **customerNumber** must be unique. "
        "Returns **409 Conflict** if it already exists."
    ),
)
async def create_customer(
    payload: CustomerCreate,
    db: AsyncSession = Depends(get_db),
):
    logger.info("POST /customers/ — customerNumber=%s name='%s'",
                payload.customerNumber, payload.customerName)
    try:
        customer = await customer_crud.create_customer(db, payload)
    except ValueError as exc:
        logger.warning("POST /customers/ — 409 Conflict: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )

    logger.info("POST /customers/ — created customerNumber=%s", customer.customerNumber)
    # Re-fetch with relationships so the response includes orders/payments
    return await customer_crud.get_customer(db, customer.customerNumber)


# ── PUT /customers/{customer_number} ──────────────────────────────────────────

@router.put(
    "/{customer_number}",
    response_model=CustomerOut,
    summary="Update a customer (partial)",
    description=(
        "Partially update an existing customer. "
        "Only the fields you include in the request body are changed. "
        "Returns **404** if the customer does not exist."
    ),
)
async def update_customer(
    customer_number: int,
    payload: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
):
    logger.info("PUT /customers/%d — fields=%s",
                customer_number, list(payload.model_dump(exclude_none=True).keys()))

    customer = await customer_crud.update_customer(db, customer_number, payload)

    if customer is None:
        logger.warning("PUT /customers/%d — 404 Not Found", customer_number)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with customerNumber {customer_number} not found",
        )

    logger.info("PUT /customers/%d — updated successfully", customer_number)
    return await customer_crud.get_customer(db, customer.customerNumber)


# ── DELETE /customers/{customer_number} ───────────────────────────────────────

@router.delete(
    "/{customer_number}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a customer",
    description=(
        "Permanently delete a customer and all their associated orders and payments. "
        "Returns **404** if the customer does not exist."
    ),
)
async def delete_customer(
    customer_number: int,
    db: AsyncSession = Depends(get_db),
):
    logger.info("DELETE /customers/%d — requested", customer_number)
    deleted = await customer_crud.delete_customer(db, customer_number)

    if not deleted:
        logger.warning("DELETE /customers/%d — 404 Not Found", customer_number)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with customerNumber {customer_number} not found",
        )

    logger.info("DELETE /customers/%d — deleted successfully", customer_number)
    # 204 No Content — return nothing
