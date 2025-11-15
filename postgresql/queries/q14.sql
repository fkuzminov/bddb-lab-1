SELECT s.full_name,
       e.course_id,
       e.grade,
       LEAD(e.grade) OVER (PARTITION BY e.student_id ORDER BY e.id) AS next_grade
FROM enrollments e
JOIN students s ON s.id = e.student_id
ORDER BY s.full_name, e.id;