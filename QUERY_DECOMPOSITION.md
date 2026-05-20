# Task 2 — Query Understanding & Decomposition

Before writing any SQL, a good Text-to-SQL agent should first break down the natural language question into its logical components. This helps avoid mistakes and makes sure we know exactly what tables, columns, filters, and joins are needed.

Below is the structured decomposition for all 50 benchmark questions.

---

## Part A — Simple SELECT Queries (Q1–Q20)

---

### Q1. List all products

- **Intent:** Retrieve every product record
- **Tables:** `products`
- **Columns:** All columns (`*`)
- **Filters:** None
- **Joins:** None

---

### Q2. Get all customers

- **Intent:** Retrieve every customer record
- **Tables:** `customers`
- **Columns:** All columns (`*`)
- **Filters:** None
- **Joins:** None

---

### Q3. Show all orders

- **Intent:** Retrieve every order record
- **Tables:** `orders`
- **Columns:** All columns (`*`)
- **Filters:** None
- **Joins:** None

---

### Q4. List all employees

- **Intent:** Retrieve every employee record
- **Tables:** `employees`
- **Columns:** All columns (`*`)
- **Filters:** None
- **Joins:** None

---

### Q5. Get all offices

- **Intent:** Retrieve every office record
- **Tables:** `offices`
- **Columns:** All columns (`*`)
- **Filters:** None
- **Joins:** None

---

### Q6. Show all product lines

- **Intent:** Retrieve every product line category
- **Tables:** `productlines`
- **Columns:** `productLine`, `textDescription`
- **Filters:** None
- **Joins:** None

---

### Q7. List all payments

- **Intent:** Retrieve every payment transaction record
- **Tables:** `payments`
- **Columns:** All columns (`*`)
- **Filters:** None
- **Joins:** None

---

### Q8. Get product names and prices

- **Intent:** Retrieve product name with its cost and retail price
- **Tables:** `products`
- **Columns:** `productName`, `buyPrice`, `MSRP`
- **Filters:** None
- **Joins:** None

---

### Q9. Get customer names and cities

- **Intent:** Retrieve each customer's name and the city they are from
- **Tables:** `customers`
- **Columns:** `customerName`, `city`
- **Filters:** None
- **Joins:** None

---

### Q10. List employee first and last names

- **Intent:** Retrieve the full names of all employees
- **Tables:** `employees`
- **Columns:** `firstName`, `lastName`
- **Filters:** None
- **Joins:** None

---

### Q11. Get all order dates

- **Intent:** Retrieve the order number and all associated date columns for each order
- **Tables:** `orders`
- **Columns:** `orderNumber`, `orderDate`, `requiredDate`, `shippedDate`
- **Filters:** None
- **Joins:** None

---

### Q12. Show product vendor list

- **Intent:** Retrieve the unique list of product suppliers/vendors
- **Tables:** `products`
- **Columns:** `productVendor`
- **Filters:** None (use `DISTINCT` to deduplicate)
- **Joins:** None

---

### Q13. Get all product codes

- **Intent:** Retrieve the unique identifier and name for every product
- **Tables:** `products`
- **Columns:** `productCode`, `productName`
- **Filters:** None
- **Joins:** None

---

### Q14. List all countries from offices

- **Intent:** Retrieve the unique list of countries where the company has offices
- **Tables:** `offices`
- **Columns:** `country`
- **Filters:** None (use `DISTINCT` to deduplicate)
- **Joins:** None

---

### Q15. Show all order statuses

- **Intent:** Retrieve the unique set of status values used across all orders
- **Tables:** `orders`
- **Columns:** `status`
- **Filters:** None (use `DISTINCT`)
- **Joins:** None

---

### Q16. Get all payment amounts

- **Intent:** Retrieve every individual payment record with its amount
- **Tables:** `payments`
- **Columns:** `customerNumber`, `checkNumber`, `paymentDate`, `amount`
- **Filters:** None
- **Joins:** None

---

### Q17. List all job titles

- **Intent:** Retrieve the unique set of job roles/titles in the company
- **Tables:** `employees`
- **Columns:** `jobTitle`
- **Filters:** None (use `DISTINCT`)
- **Joins:** None

---

### Q18. Get customer phone numbers

- **Intent:** Retrieve each customer's name and their phone contact number
- **Tables:** `customers`
- **Columns:** `customerName`, `phone`
- **Filters:** None
- **Joins:** None

---

### Q19. Show product MSRP values

- **Intent:** Retrieve each product with its manufacturer's suggested retail price
- **Tables:** `products`
- **Columns:** `productName`, `MSRP`
- **Filters:** None
- **Joins:** None

---

### Q20. List order numbers

- **Intent:** Retrieve the order number alongside the date and status for each order
- **Tables:** `orders`
- **Columns:** `orderNumber`, `orderDate`, `status`
- **Filters:** None
- **Joins:** None

---

## Part B — JOIN Queries (Q21–Q30)

---

### Q21. Get orders with customer names

- **Intent:** Retrieve each order record combined with the name of the customer who placed it
- **Tables:** `orders`, `customers`
- **Columns:** `orders.orderNumber`, `orders.orderDate`, `orders.status`, `customers.customerName`
- **Filters:** None
- **Joins:** `orders` JOIN `customers` ON `orders.customerNumber = customers.customerNumber`

---

### Q22. Get employees with office city

- **Intent:** Show each employee alongside the city of the office they work in
- **Tables:** `employees`, `offices`
- **Columns:** `employees.firstName`, `employees.lastName`, `employees.jobTitle`, `offices.city`
- **Filters:** None
- **Joins:** `employees` JOIN `offices` ON `employees.officeCode = offices.officeCode`

---

### Q23. Get payments with customer names

- **Intent:** Show each payment transaction alongside the customer's name
- **Tables:** `payments`, `customers`
- **Columns:** `customers.customerName`, `payments.checkNumber`, `payments.paymentDate`, `payments.amount`
- **Filters:** None
- **Joins:** `payments` JOIN `customers` ON `payments.customerNumber = customers.customerNumber`

---

### Q24. Get order details with product names

- **Intent:** Show each order line item with the readable product name instead of just the product code
- **Tables:** `orderdetails`, `products`
- **Columns:** `orderdetails.orderNumber`, `products.productName`, `orderdetails.quantityOrdered`, `orderdetails.priceEach`
- **Filters:** None
- **Joins:** `orderdetails` JOIN `products` ON `orderdetails.productCode = products.productCode`

---

### Q25. Get products with product line description

- **Intent:** Attach the product line's text description to each product record
- **Tables:** `products`, `productlines`
- **Columns:** `products.productName`, `products.productLine`, `productlines.textDescription`
- **Filters:** None
- **Joins:** `products` JOIN `productlines` ON `products.productLine = productlines.productLine`

---

### Q26. Get customers with sales rep names

- **Intent:** Show each customer alongside the full name of their assigned sales representative
- **Tables:** `customers`, `employees`
- **Columns:** `customers.customerName`, `customers.country`, `employees.firstName`, `employees.lastName`
- **Filters:** None
- **Joins:** `customers` LEFT JOIN `employees` ON `customers.salesRepEmployeeNumber = employees.employeeNumber`
- **Note:** Must use LEFT JOIN because some customers have no assigned sales rep (NULL)

---

### Q27. Get orders with customer city

- **Intent:** Show each order alongside the customer's name and city
- **Tables:** `orders`, `customers`
- **Columns:** `orders.orderNumber`, `orders.orderDate`, `orders.status`, `customers.customerName`, `customers.city`
- **Filters:** None
- **Joins:** `orders` JOIN `customers` ON `orders.customerNumber = customers.customerNumber`

---

### Q28. Get employees and their manager

- **Intent:** Show each employee alongside the name of the person they report to
- **Tables:** `employees` (self-join — the same table used twice)
- **Columns:** `emp.employeeNumber`, `emp.firstName`, `emp.lastName`, `emp.jobTitle`, `mgr.firstName`, `mgr.lastName`
- **Filters:** None
- **Joins:** `employees emp` LEFT JOIN `employees mgr` ON `emp.reportsTo = mgr.employeeNumber`
- **Note:** This is a self-join. The `employees` table is joined to itself. LEFT JOIN is needed so the President (who has no manager) still appears.

---

### Q29. Get order details with product vendor

- **Intent:** Show each order line item with the name and vendor of the product ordered
- **Tables:** `orderdetails`, `products`
- **Columns:** `orderdetails.orderNumber`, `products.productName`, `products.productVendor`, `orderdetails.quantityOrdered`, `orderdetails.priceEach`
- **Filters:** None
- **Joins:** `orderdetails` JOIN `products` ON `orderdetails.productCode = products.productCode`

---

### Q30. Get payments with customer country

- **Intent:** Show each payment alongside the country the customer is from
- **Tables:** `payments`, `customers`
- **Columns:** `customers.customerName`, `customers.country`, `payments.amount`, `payments.paymentDate`
- **Filters:** None
- **Joins:** `payments` JOIN `customers` ON `payments.customerNumber = customers.customerNumber`

---

## Part C — Aggregation Queries (Q31–Q40)

---

### Q31. Count customers per country

- **Intent:** Find out how many customers exist in each country
- **Tables:** `customers`
- **Columns:** `country`, `COUNT(*)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `COUNT(*)` grouped by `country`

---

### Q32. Total payments per customer

- **Intent:** Calculate the total amount each customer has ever paid
- **Tables:** `payments`, `customers`
- **Columns:** `customers.customerName`, `SUM(payments.amount)`
- **Filters:** None
- **Joins:** `payments` JOIN `customers` ON `payments.customerNumber = customers.customerNumber`
- **Aggregation:** `SUM(amount)` grouped by `customerName`

---

### Q33. Number of orders per status

- **Intent:** Count how many orders fall into each status category (Shipped, Cancelled, etc.)
- **Tables:** `orders`
- **Columns:** `status`, `COUNT(*)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `COUNT(*)` grouped by `status`

---

### Q34. Products per product line

- **Intent:** Count how many products belong to each product line category
- **Tables:** `products`
- **Columns:** `productLine`, `COUNT(*)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `COUNT(*)` grouped by `productLine`

---

### Q35. Employees per office

- **Intent:** Count how many employees are based in each office
- **Tables:** `offices`, `employees`
- **Columns:** `offices.city`, `offices.country`, `COUNT(employees.employeeNumber)`
- **Filters:** None
- **Joins:** `offices` LEFT JOIN `employees` ON `offices.officeCode = employees.officeCode`
- **Aggregation:** `COUNT(employeeNumber)` grouped by `offices.officeCode`, `city`, `country`

---

### Q36. Total stock per product vendor

- **Intent:** Calculate the total number of units in stock supplied by each vendor
- **Tables:** `products`
- **Columns:** `productVendor`, `SUM(quantityInStock)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `SUM(quantityInStock)` grouped by `productVendor`

---

### Q37. Average buy price per product line

- **Intent:** Calculate the average cost price of products in each product line category
- **Tables:** `products`
- **Columns:** `productLine`, `AVG(buyPrice)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `AVG(buyPrice)` grouped by `productLine`

---

### Q38. Orders per customer

- **Intent:** Count the total number of orders each customer has placed
- **Tables:** `customers`, `orders`
- **Columns:** `customers.customerName`, `COUNT(orders.orderNumber)`
- **Filters:** None
- **Joins:** `customers` LEFT JOIN `orders` ON `customers.customerNumber = orders.customerNumber`
- **Aggregation:** `COUNT(orderNumber)` grouped by `customerName`
- **Note:** LEFT JOIN ensures customers with zero orders are still shown

---

### Q39. Max MSRP per product line

- **Intent:** Find the highest retail price product in each product line
- **Tables:** `products`
- **Columns:** `productLine`, `MAX(MSRP)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `MAX(MSRP)` grouped by `productLine`

---

### Q40. Min buy price per vendor

- **Intent:** Find the cheapest product (by cost price) offered by each vendor
- **Tables:** `products`
- **Columns:** `productVendor`, `MIN(buyPrice)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `MIN(buyPrice)` grouped by `productVendor`

---

## Part D — Summary / Single Value Stats (Q41–Q50)

---

### Q41. Total number of customers

- **Intent:** Count how many customer records exist in total
- **Tables:** `customers`
- **Columns:** `COUNT(*)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `COUNT(*)` — single value result

---

### Q42. Total number of products

- **Intent:** Count how many products exist in the catalog
- **Tables:** `products`
- **Columns:** `COUNT(*)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `COUNT(*)` — single value result

---

### Q43. Total revenue from payments

- **Intent:** Sum all payment amounts to get the overall total revenue
- **Tables:** `payments`
- **Columns:** `SUM(amount)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `SUM(amount)` — single value result

---

### Q44. Average product price

- **Intent:** Calculate the average cost price and average retail price across all products
- **Tables:** `products`
- **Columns:** `AVG(buyPrice)`, `AVG(MSRP)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `AVG(buyPrice)`, `AVG(MSRP)` — single row result

---

### Q45. Max payment amount

- **Intent:** Find the single largest payment ever made
- **Tables:** `payments`
- **Columns:** `MAX(amount)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `MAX(amount)` — single value result

---

### Q46. Min payment amount

- **Intent:** Find the single smallest payment ever made
- **Tables:** `payments`
- **Columns:** `MIN(amount)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `MIN(amount)` — single value result

---

### Q47. Count total orders

- **Intent:** Count how many order records exist in total
- **Tables:** `orders`
- **Columns:** `COUNT(*)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `COUNT(*)` — single value result

---

### Q48. Total quantity in stock

- **Intent:** Sum the stock quantity across all products to get total inventory units
- **Tables:** `products`
- **Columns:** `SUM(quantityInStock)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `SUM(quantityInStock)` — single value result

---

### Q49. Average MSRP

- **Intent:** Calculate the average recommended retail price across all products
- **Tables:** `products`
- **Columns:** `AVG(MSRP)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `AVG(MSRP)` — single value result

---

### Q50. Number of employees

- **Intent:** Count the total number of employee records
- **Tables:** `employees`
- **Columns:** `COUNT(*)`
- **Filters:** None
- **Joins:** None
- **Aggregation:** `COUNT(*)` — single value result
