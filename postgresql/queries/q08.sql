SELECT c.course_name,
       e.grade,
       ARRAY_AGG(s.full_name) AS students_with_same_grade
FROM enrollments e
JOIN students s ON e.student_id = s.id
JOIN courses c ON e.course_id = c.id
GROUP BY c.course_name, e.grade
HAVING COUNT(*) > 1
ORDER BY c.course_name, e.grade;