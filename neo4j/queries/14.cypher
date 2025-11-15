MATCH (p:Product)
WITH AVG(p.price) AS avg_price
MATCH (p:Product)
WHERE p.price > avg_price
RETURN p.name AS product, p.category AS category, p.price AS price
ORDER BY p.price DESC;