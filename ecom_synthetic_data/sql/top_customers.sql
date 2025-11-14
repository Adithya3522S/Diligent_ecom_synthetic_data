SELECT
    c.customer_id,
    c.name AS customer_name,
    SUM(o.total_amount) AS total_spent,
    COUNT(o.order_id) AS order_count,
    MIN(o.order_date) AS first_order_date,
    MAX(o.order_date) AS last_order_date
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC
LIMIT 10;

