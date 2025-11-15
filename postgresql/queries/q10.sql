SELECT s.enrollment_year,
       g.group_name,
       ARRAY_AGG(s.full_name)
FROM students s
JOIN groups g ON s.group_id = g.id
GROUP BY s.enrollment_year, g.group_name
ORDER BY s.enrollment_year DESC, g.group_name;
