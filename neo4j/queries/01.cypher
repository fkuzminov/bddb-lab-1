MATCH (w:Warehouse)
RETURN w.name AS warehouse_name, w.city AS city
ORDER BY w.city;
