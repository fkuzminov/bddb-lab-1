MATCH (s:Store)-[o:ORDERS]->(p:Product)
WHERE p.name = "MacBook Pro M4 13"
RETURN
  s.name AS store_name,
  SUM(o.quantity) AS total_quantity
ORDER BY total_quantity DESC;