SELECT c.id, c.full_name,
       ROW_NUMBER() OVER (PARTITION BY c.city ORDER BY SUM(t.amount) DESC) AS city_rank,
       ROUND(SUM(t.amount), 2) AS total_transactions
FROM customers c
JOIN accounts a ON c.id = a.customer_id
JOIN transactions t ON a.id = t.account_id
GROUP BY c.id, c.full_name, c.city
HAVING c.city = 'Hechingen'
ORDER BY city_rank;