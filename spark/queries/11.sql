SELECT b.id, b.branch_name, ROUND(SUM(a.balance)) AS total_balance
FROM branches b
JOIN accounts a ON b.id = a.branch_id
GROUP BY b.id, b.branch_name
HAVING SUM(a.balance) > 7000000
ORDER BY b.id;