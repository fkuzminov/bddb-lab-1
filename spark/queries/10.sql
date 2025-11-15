SELECT c.id, c.full_name, ROUND(SUM(l.loan_amount), 2) AS total_loan_amount
FROM customers c
JOIN loans l ON c.id = l.customer_id
GROUP BY c.id, c.full_name
ORDER BY total_loan_amount DESC;