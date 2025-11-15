SELECT c.id, c.full_name
FROM customers c
LEFT JOIN accounts a ON c.id = a.customer_id
WHERE a.id IS NULL
ORDER BY c.id;