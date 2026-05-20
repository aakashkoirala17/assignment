# PostgreSQL Query & Command Guide

A tailored PostgreSQL quick-reference and query cheat sheet, specifically optimized for the **Classic Models** database schema.

---

> [!WARNING]
> **CRITICAL GOTCHA: CamelCase Column Names**
> The tables in `seed.sql` use camelCase names with double quotes (e.g., `"customerNumber"`, `"productLine"`, `"reportsTo"`).
>
> In PostgreSQL, identifiers that are not double-quoted are automatically folded to lowercase.
> * ❌ **Fails:** `SELECT customerNumber FROM customers;` (Postgres looks for `customernumber` in lowercase).
> *  **Succeeds:** `SELECT "customerNumber" FROM customers;` (Correct exact-match casing).

---

## 1. Connecting to the Database

### 🐳 Via Docker Container (Recommended)
Connect directly to the database interactive shell running inside the container:

```bash
docker exec -it postgres-db psql -U admin -d mydatabase
```

### 💻 Via Local Machine (If PostgreSQL client is installed)
```bash
psql -h 127.0.0.1 -p 5432 -U admin -d mydatabase
```

---

## 2. Handy `psql` Meta-Commands

Use these special slash-commands inside the interactive `psql` terminal:

| Command | Description |
| :--- | :--- |
| `\dt` | List all tables in the current database |
| `\d+ table_name` | Show table schema (columns, types, foreign keys, indexes) |
| `\l` | List all databases |
| `\dn` | List all schemas (typically `public`) |
| `\conninfo` | Show current connection details (user, host, port, db) |
| `\x` | Toggle expanded display (useful for wide rows/tables) |
| `\q` | Exit the `psql` CLI |

---

## 3. Useful Queries for Classic Models

Here are common SQL queries designed specifically for your database tables.

### 👥 1. Retrieve Customers and Their Sales Representatives
A simple `LEFT JOIN` showing which sales rep is assigned to each customer:

```sql
SELECT 
    c."customerNumber", 
    c."customerName", 
    e."firstName" || ' ' || e."lastName" AS "salesRepName",
    e."email" AS "salesRepEmail"
FROM customers c
LEFT JOIN employees e ON c."salesRepEmployeeNumber" = e."employeeNumber"
ORDER BY c."customerName" ASC;
```

---

### 📦 2. Find Total Orders and Amount Spent by Customer
Aggregates payments and order history for each customer:

```sql
SELECT 
    c."customerNumber", 
    c."customerName", 
    COUNT(DISTINCT o."orderNumber") AS "totalOrders",
    COALESCE(SUM(p."amount"), 0) AS "totalPaid"
FROM customers c
LEFT JOIN orders o ON c."customerNumber" = o."customerNumber"
LEFT JOIN payments p ON c."customerNumber" = p."customerNumber"
GROUP BY c."customerNumber", c."customerName"
ORDER BY "totalPaid" DESC;
```

---

### 🏆 3. Top 5 Best-Selling Products by Revenue
Aggregates sales revenue from `orderdetails` joined with `products`:

```sql
SELECT 
    p."productCode", 
    p."productName", 
    p."productLine",
    SUM(od."quantityOrdered") AS "unitsSold",
    SUM(od."quantityOrdered" * od."priceEach") AS "totalRevenue"
FROM products p
JOIN orderdetails od ON p."productCode" = od."productCode"
GROUP BY p."productCode", p."productName", p."productLine"
ORDER BY "totalRevenue" DESC
LIMIT 5;
```

---

### 👔 4. Employee Hierarchy (Self-Join)
Shows the reporting relationship among employees:

```sql
SELECT 
    emp."employeeNumber",
    emp."firstName" || ' ' || emp."lastName" AS "employeeName",
    emp."jobTitle",
    mgr."firstName" || ' ' || mgr."lastName" AS "reportsToManager"
FROM employees emp
LEFT JOIN employees mgr ON emp."reportsTo" = mgr."employeeNumber"
ORDER BY emp."employeeNumber";
```

---

### 🏬 5. Stock Alert (Low Inventory Products)
Find products that have a low quantity in stock:

```sql
SELECT 
    "productCode", 
    "productName", 
    "quantityInStock", 
    "buyPrice"
FROM products
WHERE "quantityInStock" < 1000
ORDER BY "quantityInStock" ASC;
```

---

## 4. Database Dump & Backup (Commands for CLI)

Run these command-line tools in your standard terminal (not inside the `psql` shell) to back up or restore your data.

### 💾 Backup the Database (`pg_dump`)
```bash
docker exec -t postgres-db pg_dump -U admin -d mydatabase > backup.sql
```

### 📥 Restore the Database from a File (`psql` pipe)
```bash
docker exec -i postgres-db psql -U admin -d mydatabase < backup.sql
```
