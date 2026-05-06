CREATE TABLE performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    enrollment_id INT,
    attendance_percentage DECIMAL(5,2),
    assignment_score DECIMAL(5,2),
    midterm_score DECIMAL(5,2),
    final_score DECIMAL(5,2),
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(enrollment_id)
);
