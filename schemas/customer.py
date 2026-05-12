"""
schemas/customer.py — The Blueprints Layer
==========================================
Pydantic models define the shape and validation rules of every piece of
data that enters or leaves the API.  Each schema serves one purpose:

  CustomerCreate  → what the client sends when creating a customer
  CustomerUpdate  → what the client sends when editing (all fields optional)
  CustomerOut     → what the API returns (includes orders & payments)

Pydantic v2 raises a ValidationError before bad data ever reaches the
database, acting as a strict gate-keeper.
"""

from __future__ import annotations

import logging
from datetime import date
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, model_validator

logger = logging.getLogger(__name__)


# ── Supporting schemas (for related data) ─────────────────────────────────────

class PaymentOut(BaseModel):
    """A payment record returned alongside a customer."""
    customerNumber: int
    checkNumber: str
    paymentDate: date
    amount: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderOut(BaseModel):
    """An order record returned alongside a customer."""
    orderNumber: int
    orderDate: date
    requiredDate: date
    shippedDate: Optional[date] = None
    status: str
    comments: Optional[str] = None
    customerNumber: int

    model_config = ConfigDict(from_attributes=True)


# ── Core customer schemas ──────────────────────────────────────────────────────

class CustomerBase(BaseModel):
    """
    Shared fields for all customer schemas.
    Every field is typed so Pydantic rejects wrong types automatically.
    """
    customerName: str
    contactLastName: str
    contactFirstName: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[Decimal] = None

    # ── Field-level validators ────────────────────────────────────────────────

    @field_validator("customerName", "contactLastName", "contactFirstName",
                     "phone", "addressLine1", "city", "country", mode="before")
    @classmethod
    def must_not_be_blank(cls, v: str, info) -> str:
        """Reject empty or whitespace-only strings for required text fields."""
        if not isinstance(v, str) or not v.strip():
            msg = f"Field '{info.field_name}' must be a non-empty string"
            logger.warning("Validation error: %s", msg)
            raise ValueError(msg)
        return v.strip()

    @field_validator("creditLimit", mode="before")
    @classmethod
    def credit_limit_non_negative(cls, v) -> Optional[Decimal]:
        """creditLimit must be ≥ 0 when provided."""
        if v is not None:
            d = Decimal(str(v))
            if d < 0:
                msg = "creditLimit must be greater than or equal to 0"
                logger.warning("Validation error: %s", msg)
                raise ValueError(msg)
            return d
        return v

    @field_validator("salesRepEmployeeNumber", mode="before")
    @classmethod
    def sales_rep_positive(cls, v) -> Optional[int]:
        """salesRepEmployeeNumber must be a positive integer when provided."""
        if v is not None:
            if not isinstance(v, int) or v <= 0:
                msg = "salesRepEmployeeNumber must be a positive integer"
                logger.warning("Validation error: %s", msg)
                raise ValueError(msg)
        return v


class CustomerCreate(CustomerBase):
    """
    Schema for POST /customers — creating a new customer.
    Step 4: This might not need an ID yet because the database creates that automatically.
    We make it Optional to support both manual and automatic ID assignment.
    """
    customerNumber: Optional[int] = None

    @field_validator("customerNumber", mode="before")
    @classmethod
    def customer_number_positive(cls, v) -> Optional[int]:
        if v is not None:
            if not isinstance(v, int) or v <= 0:
                msg = "customerNumber must be a positive integer"
                logger.warning("Validation error: %s", msg)
                raise ValueError(msg)
        return v


class CustomerUpdate(BaseModel):
    """
    Schema for PUT /customers/{id} — partial updates.
    Step 4: All the fields here should be optional.
    """
    customerName: Optional[str] = None
    contactLastName: Optional[str] = None
    contactFirstName: Optional[str] = None
    phone: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[Decimal] = None

    @model_validator(mode="after")
    def at_least_one_field(self) -> "CustomerUpdate":
        """Require at least one field to be set in an update request."""
        values = self.model_dump(exclude_none=True)
        if not values:
            msg = "At least one field must be provided for an update"
            logger.warning("Validation error: %s", msg)
            raise ValueError(msg)
        return self


class CustomerOut(CustomerBase):
    """
    Schema returned by GET /customers and GET /customers/{id}.
    Includes the primary key plus related orders and payments.
    Related lists default to [] so customers with no history still return cleanly.
    """
    customerNumber: int
    orders: List[OrderOut] = []
    payments: List[PaymentOut] = []

    model_config = ConfigDict(from_attributes=True)
