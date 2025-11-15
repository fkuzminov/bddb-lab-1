SELECT c.course_name,
       COUNT(lecturer_id) AS teacher_count
FROM courses c
JOIN teaching t ON c.id = t.course_id
GROUP BY c.course_name
HAVING COUNT(t.lecturer_id) > 1;