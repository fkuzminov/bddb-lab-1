SELECT f.faculty_name,
       SUM(c.credits) AS total_credits
FROM faculties f
JOIN groups g ON f.id = g.faculty_id
JOIN students s ON g.id = s.group_id
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.id
GROUP BY f.faculty_name
ORDER BY f.faculty_name;