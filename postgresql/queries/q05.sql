SELECT f.faculty_name,
       COUNT(s.id) AS student_count
FROM faculties f
LEFT JOIN groups g ON f.id = g.faculty_id
LEFT JOIN students s ON g.id = s.group_id
GROUP BY f.faculty_name