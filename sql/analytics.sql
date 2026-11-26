-- Total Revenue
SELECT SUM(total_amount) AS total_revenue FROM orders;

-- Total Orders
SELECT COUNT(*) AS total_orders FROM orders;

-- Average Order Value
SELECT ROUND(AVG(total_amount), 2) AS avg_order_value FROM orders;

-- Revenue by Product Category
SELECT p.category, SUM(o.total_amount) AS revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;

-- Monthly Revenue
SELECT DATE_TRUNC('month', order_date) AS month,
       SUM(total_amount) AS revenue
FROM orders
GROUP BY month
ORDER BY month;

-- Top 10 Customers
SELECT c.customer_name, SUM(o.total_amount) AS revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY revenue DESC
LIMIT 10;
