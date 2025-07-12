CREATE DATABASE Placement_portal;

-- Show databases
SHOW DATABASES;

-- ? Use the newly created database
USE Placement_portal;

-- ? Create Students Table
CREATE TABLE Students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender ENUM('Male', 'Female', 'Other'),
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    enrollment_year YEAR NOT NULL,
    course_batch VARCHAR(50),
    city VARCHAR(50),
    graduation_year YEAR
);

-- ? Create Programming Table
CREATE TABLE Programming (
    programming_id INT PRIMARY KEY,
    student_id INT,
    language VARCHAR(50),
    problems_solved INT,
    assessments_completed INT,
    mini_projects INT,
    certifications_earned INT,
    latest_project_score INT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
);

-- ? Create Soft Skills Table
CREATE TABLE SoftSkills (
    soft_skill_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    communication INT CHECK (communication BETWEEN 0 AND 100),
    teamwork INT CHECK (teamwork BETWEEN 0 AND 100),
    presentation INT CHECK (presentation BETWEEN 0 AND 100),
    leadership INT CHECK (leadership BETWEEN 0 AND 100),
    critical_thinking INT CHECK (critical_thinking BETWEEN 0 AND 100),
    interpersonal_skills INT CHECK (interpersonal_skills BETWEEN 0 AND 100),
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
);

-- ? Create Placements Table
CREATE TABLE Placements (
    placement_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    mock_interview_score INT CHECK (mock_interview_score BETWEEN 0 AND 100),
    internships_completed INT,
    placement_status ENUM('Ready', 'Not Ready', 'Placed'),
    company_name VARCHAR(100),
    placement_package DECIMAL(15,2),
    interview_rounds_cleared INT,
    placement_date DATE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
);
