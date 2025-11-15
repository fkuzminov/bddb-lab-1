MATCH (w:Warehouse)-[r:ROUTE]->(s:Store)
RETURN w.name AS warehouse, s.name AS store, r.distance AS distance
ORDER BY r.distance DESC
LIMIT 30;