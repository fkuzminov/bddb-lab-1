MATCH (w:Warehouse)-[r:ROUTE]->(s:Store)
RETURN w.name AS warehouse, s.name AS store, r.distance AS distance, r.time AS time
ORDER BY r.distance ASC;