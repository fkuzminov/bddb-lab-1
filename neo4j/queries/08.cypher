MATCH (w:Warehouse)-[s:STOCKS]->(p:Product)
RETURN w.name AS warehouse, SUM(s.quantity) AS total_quantity
ORDER BY total_quantity DESC;