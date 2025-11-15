MATCH (w:Warehouse)-[r:ROUTE]->(s:Store)
WHERE w.name = 'Denisefort Warehouse West'
RETURN s.name AS store, r.distance
ORDER BY r.distance ASC
LIMIT 5;
