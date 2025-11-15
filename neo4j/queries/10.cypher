MATCH ()-[r:ORDERS]->(p:Product)
RETURN p.name AS product, SUM(r.quantity) AS total_ordered
ORDER BY total_ordered DESC
LIMIT 10;