MATCH (w:Warehouse)-[r:ROUTE]->(s:Store)
WHERE r.time > 800
RETURN w.name as warehouse, s.name as store, r.time AS delivery_time
ORDER BY r.time DESC