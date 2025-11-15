SELECT l.full_name,
       COUNT(DISTINCT t.course_id) AS course_count
FROM lecturers l
LEFT JOIN teaching t ON t.lecturer_id = l.id
GROUP BY l.full_name