MATCH (w:Warehouse)-[r:ROUTE]->(s:Store)
WHERE w.name = 'West Ruthfort Warehouse North'
ORDER BY r.distance ASC
LIMIT 5
RETURN s.name AS store, r.distance;