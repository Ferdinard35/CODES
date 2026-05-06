SELECT s.first_name, s.last_name, p.final_score, p.attendance_percentage
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN performance p ON e.enrollment_id = p.enrollment_id
WHERE p.final_score < 50;