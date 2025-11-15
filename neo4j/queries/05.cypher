MATCH (s:Supplier)-[:SUPPLIES]->(w:Warehouse)
RETURN s.name AS supplier_name, w.name AS warehouse_name, w.city AS warehouse_city
ORDER BY s.name, w.name;