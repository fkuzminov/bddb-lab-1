SELECT
    c.id AS customer_id,
    c.full_name,
    t.transaction_date,
    t.amount AS current_amount,
    LEAD(t.amount) OVER (
        PARTITION BY c.id
        ORDER BY t.transaction_date
    ) AS next_amount
FROM customers c
JOIN accounts a ON c.id = a.customer_id
JOIN transactions t ON a.id = t.account_id
ORDER BY c.id, t.transaction_date;