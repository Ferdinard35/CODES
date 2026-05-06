SELECT student_id, COUNT(*) as count 
FROM enrollments 
GROUP BY student_id 
HAVING COUNT(*) > 1;