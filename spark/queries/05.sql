SELECT c.id, c.full_name, ROUND(SUM(t.amount), 2) AS total_transaction_amount
FROM customers c
JOIN accounts a ON c.id = a.customer_id
JOIN transactions t ON a.id = t.account_id
GROUP BY c.id, c.full_name
ORDER BY c.id;
