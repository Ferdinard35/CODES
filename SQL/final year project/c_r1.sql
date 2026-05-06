SELECT 
    s.first_name, 
    s.last_name, 
    c.course_name, 
    p.attendance_percentage,
    p.assignment_score,
    p.midterm_score,
    p.final_score
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN courses c ON e.course_id = c.course_id
JOIN performance p ON e.enrollment_id = p.enrollment_id;