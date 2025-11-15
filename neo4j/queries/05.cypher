MATCH (s:Supplier)-[:SUPPLIES]->(w:Warehouse)
RETURN s.name AS supplier_name, collect(w.name) AS warehouses
ORDER BY s.name;