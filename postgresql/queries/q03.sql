SELECT s.full_name,
       AVG(e.grade) AS average_grade
FROM students s
JOIN enrollments e ON s.id = e.student_id
GROUP BY s.full_name
HAVING AVG(e.grade) > 4;