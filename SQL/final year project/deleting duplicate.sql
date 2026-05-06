USE student_performance_system;

-- First delete performance records linked to duplicate enrollments
DELETE FROM performance 
WHERE enrollment_id IN (11,12,13,14,15,16,17,18,19,20,31,32,33,34,35,36,37,38,39,40);

-- Then delete the duplicate enrollments
DELETE FROM enrollments 
WHERE enrollment_id IN (11,12,13,14,15,16,17,18,19,20,31,32,33,34,35,36,37,38,39,40);