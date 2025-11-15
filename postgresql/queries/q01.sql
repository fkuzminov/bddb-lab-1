SELECT s.full_name,
       g.group_name,
       f.faculty_name
FROM students s
LEFT JOIN groups g ON s.group_id = g.id
LEFT JOIN faculties f ON g.faculty_id = f.id;