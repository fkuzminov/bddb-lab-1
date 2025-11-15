MATCH (w:Warehouse)-[:ROUTE]->(s:Store)
RETURN w.name, COUNT(DISTINCT s) AS store_count
ORDER BY store_count DESC;