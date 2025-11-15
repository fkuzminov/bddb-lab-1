MATCH (w:Warehouse)-[r:STOCKS]->(p:Product {category: "Food"})
RETURN w.name AS warehouse, w.city AS city, COUNT(p) AS products_in_category
ORDER BY products_in_category DESC;