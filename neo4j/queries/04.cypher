MATCH (w:Warehouse)-[r:STOCKS]->(p:Product)
WHERE p.category = "Food"
RETURN w.name AS warehouse, COUNT(p) AS products_in_category
ORDER BY products_in_category DESC;