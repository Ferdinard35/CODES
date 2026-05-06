USE student_performance_system;

SELECT e.enrollment_id, s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id
ORDER BY s.student_id;