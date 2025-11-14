SELECT
    o.order_id,
    o.order_date,
    oi.order_item_id,
    p.name AS product_name,
    oi.quantity,
    oi.item_price,
    oi.quantity * oi.item_price AS line_total
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_date DESC, o.order_id, oi.order_item_id;

