SELECT s.full_name,
       ROUND(AVG(e.grade), 2) AS average_grade
FROM students s
JOIN enrollments e ON s.id = e.student_id
GROUP BY s.full_name
HAVING AVG(e.grade) > 4
ORDER BY average_grade DESC
LIMIT 10;