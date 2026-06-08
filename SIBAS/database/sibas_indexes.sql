-- ============================================================
-- SIBAS - Indexes
-- ============================================================

-- USERS
CREATE INDEX idx_users_role_id ON users(role_id);
CREATE INDEX idx_users_username ON users(username);

-- STUDENTS
CREATE INDEX idx_students_department_id ON students(department_id);
CREATE INDEX idx_students_matric_no ON students(matric_no);
CREATE INDEX idx_students_user_id ON students(user_id);
CREATE INDEX idx_students_level ON students(level);

-- LECTURERS
CREATE INDEX idx_lecturers_department_id ON lecturers(department_id);
CREATE INDEX idx_lecturers_user_id ON lecturers(user_id);

-- COURSES
CREATE INDEX idx_courses_department_id ON courses(department_id);
CREATE INDEX idx_courses_course_code ON courses(course_code);

-- lecturer_teaches
CREATE INDEX idx_lecturer_teaches_lecturer_id ON lecturer_teaches(lecturer_id);
CREATE INDEX idx_lecturer_teaches_course_id ON lecturer_teaches(course_id);

-- student_enrolled
CREATE INDEX idx_student_enrolled_student_id ON student_enrolled(student_id);
CREATE INDEX idx_student_enrolled_course_id ON student_enrolled(course_id);

-- ATTENDANCE_SESSIONS
CREATE INDEX idx_attendance_sessions_course_id ON attendance_sessions(course_id);
CREATE INDEX idx_attendance_sessions_lecturer_id ON attendance_sessions(lecturer_id);
CREATE INDEX idx_attendance_sessions_session_date ON attendance_sessions(session_date);

-- ATTENDANCE_RECORDS
CREATE INDEX idx_attendance_records_session_id ON attendance_records(session_id);
CREATE INDEX idx_attendance_records_student_id ON attendance_records(student_id);
CREATE INDEX idx_attendance_records_status ON attendance_records(status);

-- ATTENDANCE_THRESHOLDS
CREATE INDEX idx_attendance_thresholds_effective_date ON attendance_thresholds(effective_date);