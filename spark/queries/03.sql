SELECT c.id, c.full_name, ROUND(SUM(a.balance), 2) AS total_balance
FROM customers c
JOIN accounts a ON c.id = a.customer_id
GROUP BY c.id, c.full_name
HAVING SUM(a.balance) > 200000
ORDER BY c.id;