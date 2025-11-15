SELECT e.id, e.full_name, COUNT(distinct c.id) AS client_count
FROM employees e
JOIN branches b ON e.branch_id = b.id
JOIN accounts a ON b.id = a.branch_id
JOIN customers c ON a.customer_id = c.id
GROUP BY e.id, e.full_name
ORDER BY e.id;