MATCH (sup:Supplier)-[:SUPPLIES]->(w:Warehouse)
WITH sup, COLLECT(DISTINCT w.city) AS cities
WHERE SIZE(cities) > 1
RETURN sup.name AS supplier, sup.country AS supplier_country, SIZE(cities) AS different_cities
ORDER BY different_cities DESC;