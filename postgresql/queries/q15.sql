SELECT
    g.group_name,
    s.full_name,
    ROUND(AVG(e.grade), 2) AS avg_grade,
    RANK() OVER (PARTITION BY g.id ORDER BY AVG(e.grade) DESC) AS rank_in_group
FROM students s
JOIN groups g ON s.group_id = g.id
JOIN enrollments e ON e.student_id = s.id
GROUP BY g.id, g.group_name, s.id, s.full_name
ORDER BY g.group_name, rank_in_group;