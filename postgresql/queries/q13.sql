SELECT s.full_name,
       l.full_name
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON e.course_id = c.id
JOIN teaching t ON t.course_id = c.id
JOIN lecturers l ON t.lecturer_id = l.id;