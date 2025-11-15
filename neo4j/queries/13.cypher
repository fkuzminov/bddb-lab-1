MATCH (s1:Store)-[:ORDERS]->(p:Product)<-[:ORDERS]-(s2:Store)
WHERE s1 <> s2
RETURN DISTINCT s1.name AS store1, s2.name AS store2, p.name AS common_product
ORDER BY store1, store2
LIMIT 30;