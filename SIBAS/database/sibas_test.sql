-- ============================================================
-- SIBAS - Database Testing Script
-- Run after: sibas_schema.sql → sibas_indexes.sql → sibas_sample_data.sql
-- ============================================================


-- ============================================================
-- TEST 1: Verify all tables exist and have data
-- ============================================================
SELECT 'roles'                AS table_name, COUNT(*) AS row_count FROM roles
UNION ALL
SELECT 'users',                              COUNT(*) FROM users
UNION ALL
SELECT 'departments',                        COUNT(*) FROM departments
UNION ALL
SELECT 'administrators',                     COUNT(*) FROM administrators
UNION ALL
SELECT 'lecturers',                          COUNT(*) FROM lecturers
UNION ALL
SELECT 'students',                           COUNT(*) FROM students
UNION ALL
SELECT 'courses',                            COUNT(*) FROM courses
UNION ALL
SELECT 'lecturer_teaches',                   COUNT(*) FROM lecturer_teaches
UNION ALL
SELECT 'student_enrolled',                    COUNT(*) FROM student_enrolled
UNION ALL
SELECT 'attendance_sessions',                COUNT(*) FROM attendance_sessions
UNION ALL
SELECT 'attendance_records',                 COUNT(*) FROM attendance_records
UNION ALL
SELECT 'attendance_thresholds',              COUNT(*) FROM attendance_thresholds;


-- ============================================================
-- TEST 2: Verify FK integrity — every user has a valid role
-- ============================================================
SELECT u.user_id, u.username, r.role_name
FROM users u
JOIN roles r ON u.role_id = r.role_id
ORDER BY r.role_name, u.username;


-- ============================================================
-- TEST 3: Verify every student is linked to a valid user and department
-- ============================================================
SELECT s.student_id, s.matric_no, s.full_name, s.level,
       u.username, d.department_name
FROM students s
JOIN users       u ON s.user_id       = u.user_id
JOIN departments d ON s.department_id = d.department_id
ORDER BY s.student_id;


-- ============================================================
-- TEST 4: Verify every lecturer is linked to a valid user and department
-- ============================================================
SELECT l.lecturer_id, l.full_name, l.email,
       u.username, d.department_name
FROM lecturers l
JOIN users       u ON l.user_id       = u.user_id
JOIN departments d ON l.department_id = d.department_id
ORDER BY l.lecturer_id;


-- ============================================================
-- TEST 5: List all courses with their department and assigned lecturer(s)
-- ============================================================
SELECT c.course_code, c.course_title, d.department_name,
       l.full_name AS lecturer
FROM courses c
JOIN departments    d  ON c.department_id  = d.department_id
LEFT JOIN lecturer_teaches lc ON lc.course_id   = c.course_id
LEFT JOIN lecturers        l  ON l.lecturer_id  = lc.lecturer_id
ORDER BY c.course_code;


-- ============================================================
-- TEST 6: List all students enrolled in each course
-- ============================================================
SELECT c.course_code, c.course_title,
       s.matric_no, s.full_name AS student_name
FROM student_enrolled sc
JOIN students s ON sc.student_id = s.student_id
JOIN courses  c ON sc.course_id  = c.course_id
ORDER BY c.course_code, s.full_name;


-- ============================================================
-- TEST 7: Full attendance records — session, student, status
-- ============================================================
SELECT
    c.course_code,
    asess.session_date,
    asess.session_time,
    s.matric_no,
    s.full_name  AS student_name,
    ar.status
FROM attendance_records ar
JOIN attendance_sessions asess ON ar.session_id  = asess.session_id
JOIN students            s     ON ar.student_id  = s.student_id
JOIN courses             c     ON asess.course_id = c.course_id
ORDER BY c.course_code, asess.session_date, s.full_name;


-- ============================================================
-- TEST 8: Attendance summary per student per course
--         (total sessions vs sessions attended)
-- ============================================================
SELECT
    c.course_code,
    s.matric_no,
    s.full_name,
    COUNT(ar.attendance_id)                                         AS total_sessions,
    SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END)         AS sessions_present,
    SUM(CASE WHEN ar.status = 'Absent'  THEN 1 ELSE 0 END)         AS sessions_absent,
    ROUND(
        SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END)::NUMERIC
        / COUNT(ar.attendance_id) * 100, 2
    )                                                               AS attendance_pct
FROM attendance_records ar
JOIN attendance_sessions asess ON ar.session_id  = asess.session_id
JOIN students            s     ON ar.student_id  = s.student_id
JOIN courses             c     ON asess.course_id = c.course_id
GROUP BY c.course_code, s.matric_no, s.full_name
ORDER BY c.course_code, s.full_name;


-- ============================================================
-- TEST 9: Flag students below the attendance threshold
-- ============================================================
WITH student_attendance AS (
    SELECT
        c.course_code,
        s.student_id,
        s.matric_no,
        s.full_name,
        ROUND(
            SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END)::NUMERIC
            / COUNT(ar.attendance_id) * 100, 2
        ) AS attendance_pct
    FROM attendance_records ar
    JOIN attendance_sessions asess ON ar.session_id  = asess.session_id
    JOIN students            s     ON ar.student_id  = s.student_id
    JOIN courses             c     ON asess.course_id = c.course_id
    GROUP BY c.course_code, s.student_id, s.matric_no, s.full_name
),
current_threshold AS (
    SELECT threshold_percentage
    FROM attendance_thresholds
    ORDER BY effective_date DESC
    LIMIT 1
)
SELECT
    sa.course_code,
    sa.matric_no,
    sa.full_name,
    sa.attendance_pct,
    ct.threshold_percentage AS required_pct,
    CASE
        WHEN sa.attendance_pct < ct.threshold_percentage THEN 'BELOW THRESHOLD'
        ELSE 'OK'
    END AS standing
FROM student_attendance sa
CROSS JOIN current_threshold ct
ORDER BY sa.course_code, sa.attendance_pct;


-- ============================================================
-- TEST 10: Constraint tests — these should FAIL 
-- ============================================================

-- 10a: Duplicate matric number (should violate UNIQUE constraint)
-- INSERT INTO students (user_id, department_id, matric_no, full_name, email, course, level)
-- VALUES (6, 1, '2023/CS/001', 'Fake Student', 'fake@student.edu.ng', 'Computer Science', 300);

-- 10b: Invalid attendance status (should violate CHECK constraint)
-- INSERT INTO attendance_records (session_id, student_id, status)
-- VALUES (1, 1, 'Late');

-- 10c: Duplicate attendance record for same session + student (should violate UNIQUE constraint)
-- INSERT INTO attendance_records (session_id, student_id, status)
-- VALUES (1, 1, 'Absent');

-- 10d: FK violation — referencing a non-existent department
-- INSERT INTO courses (course_code, course_title, department_id)
-- VALUES ('XXX999', 'Ghost Course', 999);
