SELECT b.branch_name, count(distinct c.id) AS customers_count
FROM branches b
JOIN accounts a ON b.id = a.branch_id
JOIN customers c ON a.customer_id = c.id
GROUP BY b.branch_name;