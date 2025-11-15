MATCH (sup:Supplier)-[:SUPPLIES]->(w:Warehouse)-[:STOCKS]->(p:Product)
WITH p, COUNT(DISTINCT sup) AS supplier_count
WHERE supplier_count > 1
RETURN p.name AS product, p.category AS category, supplier_count
ORDER BY supplier_count DESC, p.name
LIMIT 10;
