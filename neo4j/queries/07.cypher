MATCH (w:Warehouse)-[r:ROUTE]->(s:Store)
WHERE w.name = 'North Glenn Warehouse Central'
RETURN s.name AS store, r.distance
ORDER BY r.distance ASC
LIMIT 5;
