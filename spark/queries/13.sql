SELECT c.id, c.full_name, ARRAY_AGG(DISTINCT b.branch_name) AS branch_names
FROM customers c
JOIN accounts a ON c.id = a.customer_id
JOIN branches b ON a.branch_id = b.id
GROUP BY c.id, c.full_name
HAVING COUNT(DISTINCT b.id) > 1
ORDER BY c.id;