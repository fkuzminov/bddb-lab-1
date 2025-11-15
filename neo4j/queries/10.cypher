MATCH (p:Product)<-[r:ORDERS]-(s:Store)
RETURN p.name AS product, SUM(r.quantity) AS total_ordered
ORDER BY total_ordered DESC
LIMIT 10;