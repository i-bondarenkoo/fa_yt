SELECT orders.promocode, orders.created_at, orders.id 
FROM orders 
ORDER BY orders.id;
SELECT orders_1.id AS orders_1_id, 
products.name AS products_name, 
products.description AS products_description, 
products.price AS products_price, 
products.id AS products_id,
FROM orders AS orders_1 
JOIN order_product_association AS order_product_association_1 
    ON orders_1.id = order_product_association_1.order_id 
    JOIN products ON products.id = order_product_association_1.product_id
WHERE orders_1.id IN (1, 2)
