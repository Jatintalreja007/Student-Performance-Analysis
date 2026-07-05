create database coll_project;
use coll_project;


CREATE TABLE temp_students (
    student_id varchar(255),
    age INT,
    gender VARCHAR(10),
    major VARCHAR(100),
    GPA DECIMAL(3,2),
    course_load INT,
    avg_course_grade DECIMAL(5,2),
    attendance_rate DECIMAL(5,2),
    enrollment_status VARCHAR(20),
    lms_logins_past_month INT,
    avg_session_duration_minutes DECIMAL(6,2),
    assignment_submission_rate DECIMAL(5,2),
    forum_participation_count INT,
    video_completion_rate DECIMAL(5,2),
    risk_level VARCHAR(20)
);

SHOW VARIABLES LIKE 'local_infile';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/college_student_management_data.csv'
INTO TABLE temp_students
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

CREATE TABLE students (
    student_id varchar(255) PRIMARY KEY,
    age INT,
    gender VARCHAR(20),
    major VARCHAR(100),
    enrollment_status VARCHAR(50)
);

CREATE TABLE academic_performance (
    student_id varchar(255) PRIMARY KEY,
    GPA DECIMAL(4,2),
    course_load INT,
    avg_course_grade DECIMAL(5,2),
    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE engagement_metrics (
    student_id varchar(255) PRIMARY KEY,
    attendance_rate DECIMAL(5,2),
    lms_logins_past_month INT,
    avg_session_duration_minutes DECIMAL(6,2),
    assignment_submission_rate DECIMAL(5,2),
    forum_participation_count INT,
    video_completion_rate DECIMAL(5,2),
    risk_level VARCHAR(20),
    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO students (student_id, age, gender, major, enrollment_status)
SELECT student_id, age, gender, major, enrollment_status
FROM temp_students;

INSERT INTO academic_performance (student_id, GPA, course_load, avg_course_grade)
SELECT student_id, GPA, course_load, avg_course_grade
FROM temp_students;

INSERT INTO engagement_metrics
(student_id, attendance_rate, lms_logins_past_month,
 avg_session_duration_minutes, assignment_submission_rate,
 forum_participation_count, video_completion_rate, risk_level)

SELECT student_id, attendance_rate, lms_logins_past_month,
       avg_session_duration_minutes, assignment_submission_rate,
       forum_participation_count, video_completion_rate, risk_level
FROM temp_students;

SELECT s.student_id,
       s.major,
       a.GPA,
       e.attendance_rate,
       e.risk_level
FROM students s
INNER JOIN academic_performance a
    ON s.student_id = a.student_id
INNER JOIN engagement_metrics e
    ON s.student_id = e.student_id;


SELECT s.student_id, s.major, a.GPA, e.risk_level
FROM students s
INNER JOIN academic_performance a
    ON s.student_id = a.student_id
INNER JOIN engagement_metrics e
    ON s.student_id = e.student_id
WHERE e.risk_level = 'High';

SELECT s.major, AVG(a.GPA) AS average_gpa
FROM students s
INNER JOIN academic_performance a
    ON s.student_id = a.student_id
GROUP BY s.major;

SELECT s.student_id, a.GPA, e.attendance_rate
FROM students s
INNER JOIN academic_performance a
    ON s.student_id = a.student_id
INNER JOIN engagement_metrics e
    ON s.student_id = e.student_id;
    
    
DELIMITER //

CREATE PROCEDURE GetFullStudentReport()
BEGIN
    SELECT s.student_id,
           s.age,
           s.gender,
           s.major,
           s.enrollment_status,
           a.GPA,
           a.course_load,
           a.avg_course_grade,
           e.attendance_rate,
           e.lms_logins_past_month,
           e.assignment_submission_rate,
           e.risk_level
    FROM students s
    INNER JOIN academic_performance a
        ON s.student_id = a.student_id
    INNER JOIN engagement_metrics e
        ON s.student_id = e.student_id;
END //

DELIMITER ;

CALL GetFullStudentReport();

SELECT VERSION();
SELECT user, host, plugin 
FROM mysql.user;



















