SELECT s.department, AVG(p.final_score) AS avg_final_score
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN performance p ON e.enrollment_id = p.enrollment_id
GROUP BY s.department;