# Task 1 — SQL Benchmark: Ground Truth Queries

**Database:** Classic Models (PostgreSQL)  
**Total Questions:** 50  
**Grouped into:** Simple SELECT → JOINs → Aggregations → Summary Stats

> **Note on this database:** All column names use camelCase and must be wrapped in double quotes in PostgreSQL (e.g. `"customerName"`, `"productLine"`). Table names are lowercase and do NOT need quotes.

---

## Part A — Simple SELECT Queries (Q1–Q20)

---

### Q1. List all products

**Question:** List all products

```sql
SELECT *
FROM products;
```

**Explanation:** Retrieves every row and column from the `products` table. No filter or join needed.

---

### Q2. Get all customers

**Question:** Get all customers

```sql
SELECT *
FROM customers;
```

**Explanation:** Retrieves every row from the `customers` table.

---

### Q3. Show all orders

**Question:** Show all orders

```sql
SELECT *
FROM orders;
```

**Explanation:** Returns all records from the `orders` table including dates and status.

---

### Q4. List all employees

**Question:** List all employees

```sql
SELECT *
FROM employees;
```

**Explanation:** Returns all rows from the `employees` table.

---

### Q5. Get all offices

**Question:** Get all offices

```sql
SELECT *
FROM offices;
```

**Explanation:** Returns all rows from the `offices` table.

---

### Q6. Show all product lines

**Question:** Show all product lines

```sql
SELECT *
FROM productlines;
```

**Explanation:** Returns all product line categories from the `productlines` table.

---

### Q7. List all payments

**Question:** List all payments

```sql
SELECT *
FROM payments;
```

**Explanation:** Returns all payment records including amounts and dates.

---

### Q8. Get product names and prices

**Question:** Get product names and prices

```sql
SELECT "productName", "buyPrice", "MSRP"
FROM products;
```

**Explanation:** Selects only the name, cost price, and retail price columns from `products`.

---

### Q9. Get customer names and cities

**Question:** Get customer names and cities

```sql
SELECT "customerName", "city"
FROM customers;
```

**Explanation:** Selects only the customer name and city columns from the `customers` table.

---

### Q10. List employee first and last names

**Question:** List employee first and last names

```sql
SELECT "firstName", "lastName"
FROM employees;
```

**Explanation:** Selects just the name columns from the `employees` table.

---

### Q11. Get all order dates

**Question:** Get all order dates

```sql
SELECT "orderNumber", "orderDate", "requiredDate", "shippedDate"
FROM orders;
```

**Explanation:** Pulls the order number alongside all three date columns to show order timelines.

---

### Q12. Show product vendor list

**Question:** Show product vendor list

```sql
SELECT DISTINCT "productVendor"
FROM products
ORDER BY "productVendor";
```

**Explanation:** Uses `DISTINCT` to return each unique vendor name only once, sorted alphabetically.

---

### Q13. Get all product codes

**Question:** Get all product codes

```sql
SELECT "productCode", "productName"
FROM products;
```

**Explanation:** Returns the unique product code alongside the product name for easy reference.

---

### Q14. List all countries from offices

**Question:** List all countries from offices

```sql
SELECT DISTINCT "country"
FROM offices
ORDER BY "country";
```

**Explanation:** Uses `DISTINCT` so each country appears only once even if multiple offices exist there.

---

### Q15. Show all order statuses

**Question:** Show all order statuses

```sql
SELECT DISTINCT "status"
FROM orders;
```

**Explanation:** Returns each unique order status value (e.g. Shipped, Cancelled, In Process).

---

### Q16. Get all payment amounts

**Question:** Get all payment amounts

```sql
SELECT "customerNumber", "checkNumber", "paymentDate", "amount"
FROM payments
ORDER BY "amount" DESC;
```

**Explanation:** Returns all payment records with their amounts, sorted from highest to lowest.

---

### Q17. List all job titles

**Question:** List all job titles

```sql
SELECT DISTINCT "jobTitle"
FROM employees
ORDER BY "jobTitle";
```

**Explanation:** Returns each unique job title found in the `employees` table.

---

### Q18. Get customer phone numbers

**Question:** Get customer phone numbers

```sql
SELECT "customerName", "phone"
FROM customers
ORDER BY "customerName";
```

**Explanation:** Returns customer names with their contact phone numbers.

---

### Q19. Show product MSRP values

**Question:** Show product MSRP values

```sql
SELECT "productName", "MSRP"
FROM products
ORDER BY "MSRP" DESC;
```

**Explanation:** Returns product names and their recommended retail price, sorted highest first.

---

### Q20. List order numbers

**Question:** List order numbers

```sql
SELECT "orderNumber", "orderDate", "status"
FROM orders
ORDER BY "orderNumber";
```

**Explanation:** Returns all order numbers with their date and current status.

---

## Part B — JOIN Queries (Q21–Q39)

---

### Q21. Get orders with customer names

**Question:** Get orders with customer names

```sql
SELECT
    o."orderNumber",
    o."orderDate",
    o."status",
    c."customerName"
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber"
ORDER BY o."orderDate" DESC;
```

**Explanation:** Joins `orders` to `customers` on the shared `customerNumber` key to attach the customer name to each order.

---

### Q22. Get employees with office city

**Question:** Get employees with office city

```sql
SELECT
    e."firstName",
    e."lastName",
    e."jobTitle",
    o."city" AS "officeCity"
FROM employees e
JOIN offices o ON e."officeCode" = o."officeCode"
ORDER BY o."city";
```

**Explanation:** Joins `employees` to `offices` using `officeCode` to show which city each employee works in.

---

### Q23. Get payments with customer names

**Question:** Get payments with customer names

```sql
SELECT
    c."customerName",
    p."checkNumber",
    p."paymentDate",
    p."amount"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber"
ORDER BY p."paymentDate" DESC;
```

**Explanation:** Joins `payments` to `customers` to attach the customer name to each payment record.

---

### Q24. Get order details with product names

**Question:** Get order details with product names

```sql
SELECT
    od."orderNumber",
    p."productName",
    od."quantityOrdered",
    od."priceEach"
FROM orderdetails od
JOIN products p ON od."productCode" = p."productCode"
ORDER BY od."orderNumber";
```

**Explanation:** Joins `orderdetails` to `products` to replace the raw product code with a readable product name.

---

### Q25. Get products with product line description

**Question:** Get products with product line description

```sql
SELECT
    p."productName",
    p."productLine",
    pl."textDescription"
FROM products p
JOIN productlines pl ON p."productLine" = pl."productLine"
ORDER BY p."productLine";
```

**Explanation:** Joins `products` to `productlines` to attach the text description for each product's category.

---

### Q26. Get customers with sales rep names

**Question:** Get customers with sales rep names

```sql
SELECT
    c."customerName",
    c."country",
    e."firstName" || ' ' || e."lastName" AS "salesRepName"
FROM customers c
LEFT JOIN employees e ON c."salesRepEmployeeNumber" = e."employeeNumber"
ORDER BY c."customerName";
```

**Explanation:** Uses a `LEFT JOIN` so customers with no assigned sales rep (NULL) are still included. Concatenates first and last name into a single readable column.

---

### Q27. Get orders with customer city

**Question:** Get orders with customer city

```sql
SELECT
    o."orderNumber",
    o."orderDate",
    o."status",
    c."customerName",
    c."city"
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber"
ORDER BY c."city";
```

**Explanation:** Joins `orders` and `customers` to show which city each order came from.

---

### Q28. Get employees and their manager

**Question:** Get employees and their manager

```sql
SELECT
    emp."employeeNumber",
    emp."firstName" || ' ' || emp."lastName" AS "employeeName",
    emp."jobTitle",
    mgr."firstName" || ' ' || mgr."lastName" AS "managerName"
FROM employees emp
LEFT JOIN employees mgr ON emp."reportsTo" = mgr."employeeNumber"
ORDER BY emp."employeeNumber";
```

**Explanation:** Self-join on the `employees` table — the same table is joined to itself using `reportsTo` as the link. `LEFT JOIN` ensures the top-level president (who has no manager) still appears.

---

### Q29. Get order details with product vendor

**Question:** Get orderdetails with product vendor

```sql
SELECT
    od."orderNumber",
    p."productName",
    p."productVendor",
    od."quantityOrdered",
    od."priceEach"
FROM orderdetails od
JOIN products p ON od."productCode" = p."productCode"
ORDER BY p."productVendor";
```

**Explanation:** Joins `orderdetails` and `products` to include the vendor name alongside each order line item.

---

### Q30. Get payments with customer country

**Question:** Get payments with customer country

```sql
SELECT
    c."customerName",
    c."country",
    p."amount",
    p."paymentDate"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber"
ORDER BY c."country";
```

**Explanation:** Joins `payments` to `customers` to show which country each payment came from.

---

## Part C — Aggregation Queries (Q31–Q49)

---

### Q31. Count customers per country

**Question:** Count customers per country

```sql
SELECT
    "country",
    COUNT(*) AS "customerCount"
FROM customers
GROUP BY "country"
ORDER BY "customerCount" DESC;
```

**Explanation:** Groups all customers by their country and counts how many exist in each. Sorted so the countries with most customers appear first.

---

### Q32. Total payments per customer

**Question:** Total payments per customer

```sql
SELECT
    c."customerName",
    SUM(p."amount") AS "totalPaid"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber"
GROUP BY c."customerName"
ORDER BY "totalPaid" DESC;
```

**Explanation:** Joins payments to customers, then uses `SUM()` and `GROUP BY` to calculate the total amount each customer has paid.

---

### Q33. Number of orders per status

**Question:** Number of orders per status

```sql
SELECT
    "status",
    COUNT(*) AS "orderCount"
FROM orders
GROUP BY "status"
ORDER BY "orderCount" DESC;
```

**Explanation:** Groups orders by their status value (Shipped, Cancelled, etc.) and counts how many orders fall into each category.

---

### Q34. Products per product line

**Question:** Products per product line

```sql
SELECT
    "productLine",
    COUNT(*) AS "productCount"
FROM products
GROUP BY "productLine"
ORDER BY "productCount" DESC;
```

**Explanation:** Groups products by their category line and counts how many products belong to each one.

---

### Q35. Employees per office

**Question:** Employees per office

```sql
SELECT
    o."city",
    o."country",
    COUNT(e."employeeNumber") AS "employeeCount"
FROM offices o
LEFT JOIN employees e ON o."officeCode" = e."officeCode"
GROUP BY o."officeCode", o."city", o."country"
ORDER BY "employeeCount" DESC;
```

**Explanation:** Joins `offices` to `employees` and counts how many employees are based in each office location.

---

### Q36. Total stock per product vendor

**Question:** Total stock per product vendor

```sql
SELECT
    "productVendor",
    SUM("quantityInStock") AS "totalStock"
FROM products
GROUP BY "productVendor"
ORDER BY "totalStock" DESC;
```

**Explanation:** Groups products by vendor and sums up their total inventory stock.

---

### Q37. Average buy price per product line

**Question:** Average buy price per product line

```sql
SELECT
    "productLine",
    ROUND(AVG("buyPrice"), 2) AS "avgBuyPrice"
FROM products
GROUP BY "productLine"
ORDER BY "avgBuyPrice" DESC;
```

**Explanation:** Calculates the average cost price for products within each product line category. `ROUND` limits the output to 2 decimal places.

---

### Q38. Orders per customer

**Question:** Orders per customer

```sql
SELECT
    c."customerName",
    COUNT(o."orderNumber") AS "totalOrders"
FROM customers c
LEFT JOIN orders o ON c."customerNumber" = o."customerNumber"
GROUP BY c."customerName"
ORDER BY "totalOrders" DESC;
```

**Explanation:** Joins customers to orders and counts how many orders each customer has placed. `LEFT JOIN` includes customers with zero orders.

---

### Q39. Max MSRP per product line

**Question:** Max MSRP per product line

```sql
SELECT
    "productLine",
    MAX("MSRP") AS "maxMSRP"
FROM products
GROUP BY "productLine"
ORDER BY "maxMSRP" DESC;
```

**Explanation:** Finds the highest retail price product in each product line category.

---

### Q40. Min buy price per vendor

**Question:** Min buy price per vendor

```sql
SELECT
    "productVendor",
    MIN("buyPrice") AS "minBuyPrice"
FROM products
GROUP BY "productVendor"
ORDER BY "minBuyPrice" ASC;
```

**Explanation:** Finds the cheapest product (by cost price) for each vendor.

---

## Part D — Summary / Single Value Stats (Q41–Q50)

---

### Q41. Total number of customers

**Question:** Total number of customers

```sql
SELECT COUNT(*) AS "totalCustomers"
FROM customers;
```

**Explanation:** Counts all rows in the `customers` table to get the total customer count.

---

### Q42. Total number of products

**Question:** Total number of products

```sql
SELECT COUNT(*) AS "totalProducts"
FROM products;
```

**Explanation:** Counts all rows in the `products` table.

---

### Q43. Total revenue from payments

**Question:** Total revenue from payments

```sql
SELECT
    ROUND(SUM("amount"), 2) AS "totalRevenue"
FROM payments;
```

**Explanation:** Sums every payment amount in the `payments` table to get the total revenue figure.

---

### Q44. Average product price

**Question:** Average product price

```sql
SELECT
    ROUND(AVG("buyPrice"), 2) AS "avgBuyPrice",
    ROUND(AVG("MSRP"), 2) AS "avgMSRP"
FROM products;
```

**Explanation:** Calculates the average cost and retail price across all products in the catalog.

---

### Q45. Max payment amount

**Question:** Max payment amount

```sql
SELECT
    MAX("amount") AS "maxPayment"
FROM payments;
```

**Explanation:** Finds the single largest individual payment ever recorded.

---

### Q46. Min payment amount

**Question:** Min payment amount

```sql
SELECT
    MIN("amount") AS "minPayment"
FROM payments;
```

**Explanation:** Finds the smallest individual payment ever recorded.

---

### Q47. Count total orders

**Question:** Count total orders

```sql
SELECT COUNT(*) AS "totalOrders"
FROM orders;
```

**Explanation:** Counts all rows in the `orders` table to return the total number of orders placed.

---

### Q48. Total quantity in stock

**Question:** Total quantity in stock

```sql
SELECT
    SUM("quantityInStock") AS "totalStockUnits"
FROM products;
```

**Explanation:** Sums the `quantityInStock` column across all products to get total inventory units.

---

### Q49. Average MSRP

**Question:** Average MSRP

```sql
SELECT
    ROUND(AVG("MSRP"), 2) AS "avgMSRP"
FROM products;
```

**Explanation:** Calculates the average recommended retail price across all products.

---

### Q50. Number of employees

**Question:** Number of employees

```sql
SELECT COUNT(*) AS "totalEmployees"
FROM employees;
```

**Explanation:** Counts all rows in the `employees` table to return the total headcount.
