WITH monthly_max AS (
    SELECT
        YEAR(t.transaction_date) AS year,
        MONTH(t.transaction_date) AS month,
        MAX(t.amount) AS max_amount
    FROM transactions t
    GROUP BY YEAR(t.transaction_date), MONTH(t.transaction_date)
)
SELECT c.id, c.full_name, CONCAT(mm.year, '-', mm.month) as month, t.amount, t.transaction_date
FROM customers c
JOIN accounts a ON c.id = a.customer_id
JOIN transactions t ON a.id = t.account_id
JOIN monthly_max mm ON YEAR(t.transaction_date) = mm.year
                    AND MONTH(t.transaction_date) = mm.month
                    AND t.amount = mm.max_amount
ORDER BY mm.year, mm.month;