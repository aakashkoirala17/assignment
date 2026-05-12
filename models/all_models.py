"""
models/all_models.py — SQLAlchemy ORM Models
=============================================
One class per database table.  Relationships are declared here so that
crud.py can use selectinload() to fetch related data in a single query
without any N+1 problem.
"""

from sqlalchemy import (
    Column, Integer, String, Numeric, ForeignKey,
    Date, SmallInteger, Text, LargeBinary,
)
from sqlalchemy.orm import relationship
from database import Base


class ProductLine(Base):
    __tablename__ = "productlines"

    productLine      = Column(String(50), primary_key=True)
    textDescription  = Column(String(4000))
    htmlDescription  = Column(Text)
    image            = Column(LargeBinary)

    products = relationship("Product", back_populates="product_line")


class Product(Base):
    __tablename__ = "products"

    productCode        = Column(String(15), primary_key=True)
    productName        = Column(String(70),   nullable=False)
    productLine        = Column(String(50),   ForeignKey("productlines.productLine"), nullable=False)
    productScale       = Column(String(10),   nullable=False)
    productVendor      = Column(String(50),   nullable=False)
    productDescription = Column(Text,         nullable=False)
    quantityInStock    = Column(Integer,      nullable=False)
    buyPrice           = Column(Numeric(10, 2), nullable=False)
    MSRP               = Column(Numeric(10, 2), nullable=False)

    product_line   = relationship("ProductLine", back_populates="products")
    order_details  = relationship("OrderDetail",  back_populates="product")


class Office(Base):
    __tablename__ = "offices"

    officeCode   = Column(String(10), primary_key=True)
    city         = Column(String(50), nullable=False)
    phone        = Column(String(50), nullable=False)
    addressLine1 = Column(String(50), nullable=False)
    addressLine2 = Column(String(50))
    state        = Column(String(50))
    country      = Column(String(50), nullable=False)
    postalCode   = Column(String(15), nullable=False)
    territory    = Column(String(10), nullable=False)

    employees = relationship("Employee", back_populates="office")


class Employee(Base):
    __tablename__ = "employees"

    employeeNumber = Column(Integer,     primary_key=True)
    lastName       = Column(String(50),  nullable=False)
    firstName      = Column(String(50),  nullable=False)
    extension      = Column(String(10),  nullable=False)
    email          = Column(String(100), nullable=False)
    officeCode     = Column(String(10),  ForeignKey("offices.officeCode"), nullable=False)
    reportsTo      = Column(Integer,     ForeignKey("employees.employeeNumber"))
    jobTitle       = Column(String(50),  nullable=False)

    office      = relationship("Office",   back_populates="employees")
    subordinates = relationship("Employee", back_populates="manager",   foreign_keys=[reportsTo])
    manager      = relationship("Employee", back_populates="subordinates", remote_side=[employeeNumber])
    customers    = relationship("Customer", back_populates="sales_rep")


class Customer(Base):
    __tablename__ = "customers"

    customerNumber          = Column(Integer,      primary_key=True)
    customerName            = Column(String(50),   nullable=False)
    contactLastName         = Column(String(50),   nullable=False)
    contactFirstName        = Column(String(50),   nullable=False)
    phone                   = Column(String(50),   nullable=False)
    addressLine1            = Column(String(50),   nullable=False)
    addressLine2            = Column(String(50))
    city                    = Column(String(50),   nullable=False)
    state                   = Column(String(50))
    postalCode              = Column(String(15))
    country                 = Column(String(50),   nullable=False)
    salesRepEmployeeNumber  = Column(Integer,      ForeignKey("employees.employeeNumber"))
    creditLimit             = Column(Numeric(10, 2))

    # Relationships — used by selectinload in crud.py
    sales_rep = relationship("Employee", back_populates="customers")
    orders    = relationship("Order",    back_populates="customer",  cascade="all, delete-orphan")
    payments  = relationship("Payment",  back_populates="customer",  cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"

    customerNumber = Column(Integer,      ForeignKey("customers.customerNumber"), primary_key=True)
    checkNumber    = Column(String(50),   primary_key=True)
    paymentDate    = Column(Date,         nullable=False)
    amount         = Column(Numeric(10, 2), nullable=False)

    customer = relationship("Customer", back_populates="payments")


class Order(Base):
    __tablename__ = "orders"

    orderNumber    = Column(Integer,    primary_key=True)
    orderDate      = Column(Date,       nullable=False)
    requiredDate   = Column(Date,       nullable=False)
    shippedDate    = Column(Date)
    status         = Column(String(15), nullable=False)
    comments       = Column(Text)
    customerNumber = Column(Integer,    ForeignKey("customers.customerNumber"), nullable=False)

    customer      = relationship("Customer",    back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order", cascade="all, delete-orphan")


class OrderDetail(Base):
    __tablename__ = "orderdetails"

    orderNumber     = Column(Integer,      ForeignKey("orders.orderNumber"),   primary_key=True)
    productCode     = Column(String(15),   ForeignKey("products.productCode"), primary_key=True)
    quantityOrdered = Column(Integer,      nullable=False)
    priceEach       = Column(Numeric(10, 2), nullable=False)
    orderLineNumber = Column(SmallInteger, nullable=False)

    order   = relationship("Order",   back_populates="order_details")
    product = relationship("Product", back_populates="order_details")
