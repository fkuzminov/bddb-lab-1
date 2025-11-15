SELECT s.full_name, c.course_name, e.grade
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON e.course_id = c.id
WHERE (e.course_id, e.grade) IN (
    SELECT c.id, MAX(e.grade)
    FROM courses c
    JOIN enrollments e ON e.course_id = c.id
    GROUP BY c.id
)
