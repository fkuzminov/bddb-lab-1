MATCH (w:Warehouse)-[:ROUTE]->(s:Store)
WHERE w.city = s.city
RETURN w.name AS warehouse, w.city AS city, COLLECT(s.name) AS stores_in_same_city
ORDER BY w.city;