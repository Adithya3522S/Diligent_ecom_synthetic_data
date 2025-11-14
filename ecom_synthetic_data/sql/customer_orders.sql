SELECT
    c.customer_id,
    c.name AS customer_name,
    o.order_id,
    o.total_amount,
    p.status AS payment_status,
    p.payment_method,
    p.payment_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN payments p ON p.order_id = o.order_id
ORDER BY o.order_date DESC, o.order_id;

