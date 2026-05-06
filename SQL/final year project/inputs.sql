use student_performance_system;

INSERT INTO students (first_name, last_name, gender, date_of_birth, department)
VALUES 
('Fiifi', 'Agyeman', 'Male', '2002-03-12', 'Computer Science'),
('Adwoa', 'Sarpong', 'Female', '2001-09-18', 'Mathematics'),
('Kweku', 'Asare', 'Male', '2003-04-22', 'Information Technology'),
('Abiba', 'Seidu', 'Female', '2002-07-30', 'Computer Science'),
('Nana', 'Osei', 'Male', '2001-12-05', 'Mathematics'),
('Efua', 'Acheampong', 'Female', '2003-01-14', 'Information Technology'),
('Kwabena', 'Tetteh', 'Male', '2002-06-28', 'Computer Science'),
('Akua', 'Mensah', 'Female', '2001-08-17', 'Mathematics'),
('Yoofi', 'Larbi', 'Male', '2003-02-09', 'Information Technology'),
('Maame', 'Asante', 'Female', '2002-11-23', 'Computer Science');

INSERT INTO enrollments (student_id, course_id, semester, year)
VALUES 
(9, 1, 'First', 2025),
(10, 2, 'First', 2025),
(11, 3, 'First', 2025),
(12, 4, 'First', 2025),
(13, 5, 'First', 2025),
(14, 1, 'First', 2025),
(15, 2, 'First', 2025),
(16, 3, 'First', 2025),
(17, 4, 'First', 2025),
(18, 5, 'First', 2025);


INSERT INTO performance (enrollment_id, attendance_percentage, assignment_score, midterm_score, final_score)
VALUES 
(21, 92.00, 88.00, 86.00, 90.00),
(22, 45.00, 40.00, 38.00, 35.00),
(23, 78.00, 74.00, 70.00, 76.00),
(24, 55.00, 50.00, 48.00, 52.00),
(25, 88.00, 84.00, 82.00, 87.00),
(26, 38.00, 32.00, 28.00, 25.00),
(27, 95.00, 91.00, 89.00, 94.00),
(28, 62.00, 58.00, 55.00, 60.00),
(29, 72.00, 68.00, 65.00, 70.00),
(30, 48.00, 44.00, 40.00, 42.00);