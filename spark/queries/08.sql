SELECT c.id, c.full_name, COUNT(l.id) AS loan_count
FROM customers c
JOIN loans l ON c.id = l.customer_id
GROUP BY c.id, c.full_name
HAVING COUNT(l.id) > 1
ORDER BY c.id;