
-- 1. ROLES

CREATE TABLE roles (
    role_id   SERIAL        PRIMARY KEY,
    role_name VARCHAR(50)   NOT NULL UNIQUE  -- e.g. Administrator, Lecturer, Student
);
 
 

-- 2. USERS

CREATE TABLE users (
    user_id      SERIAL        PRIMARY KEY,
    username     VARCHAR(50)   NOT NULL UNIQUE,
    password     VARCHAR(255)  NOT NULL,           
    role_id      INT           NOT NULL REFERENCES roles(role_id),
    is_active    BOOLEAN       NOT NULL DEFAULT TRUE,
    date_created TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
);
 
 

-- 3. DEPARTMENTS

CREATE TABLE departments (
    department_id   SERIAL       PRIMARY KEY,
    department_name VARCHAR(200) NOT NULL UNIQUE
);
 
 

-- 4. ADMINISTRATORS 

CREATE TABLE administrators (
    administrator_id SERIAL       PRIMARY KEY,
    user_id          INT          NOT NULL UNIQUE REFERENCES users(user_id),
    full_name        VARCHAR(200) NOT NULL
);
 
 

-- 5. STUDENTS

CREATE TABLE students (
    student_id    SERIAL        PRIMARY KEY,
    user_id       INT           NOT NULL UNIQUE REFERENCES users(user_id),
    department_id INT           NOT NULL REFERENCES departments(department_id),
    matric_no     VARCHAR(20)   NOT NULL UNIQUE,
    full_name     VARCHAR(200)  NOT NULL,
    email         VARCHAR(100)  NOT NULL UNIQUE,
    course        VARCHAR(100)  NOT NULL,   
    level         INT           NOT NULL 
);
 
 

-- 6. LECTURERS

CREATE TABLE lecturers (
    lecturer_id   SERIAL        PRIMARY KEY,
    user_id       INT           NOT NULL UNIQUE REFERENCES users(user_id),
    department_id INT           NOT NULL REFERENCES departments(department_id),
    full_name     VARCHAR(200)  NOT NULL,
    email         VARCHAR(100)  NOT NULL UNIQUE
);
 
 

-- 7. COURSES

CREATE TABLE courses (
    course_id     SERIAL        PRIMARY KEY,
    course_code   VARCHAR(20)   NOT NULL UNIQUE,
    course_title  VARCHAR(100)  NOT NULL UNIQUE,
    department_id INT           NOT NULL REFERENCES departments(department_id)
);
 
 

-- 8. LECTURER_TEACHES  (which lecturer teaches which course)

CREATE TABLE lecturer_teaches (
    lecturer_id INT NOT NULL REFERENCES lecturers(lecturer_id),
    course_id   INT NOT NULL REFERENCES courses(course_id),
    PRIMARY KEY (lecturer_id, course_id)
);
 
 

-- 9. STUDENT_ENROLLED  (which student is enrolled in which course)

CREATE TABLE student_enrolled (
    student_id INT NOT NULL REFERENCES students(student_id),
    course_id  INT NOT NULL REFERENCES courses(course_id),
    PRIMARY KEY (student_id, course_id)
);
 
 

-- 10. ATTENDANCE_SESSIONS (a single class session for which attendance is taken)

CREATE TABLE attendance_sessions (
    session_id   SERIAL    PRIMARY KEY,
    course_id    INT       NOT NULL REFERENCES courses(course_id),
    lecturer_id  INT       NOT NULL REFERENCES lecturers(lecturer_id),
    session_date DATE      NOT NULL,
    session_time TIME,                     
    status       VARCHAR(20) NOT NULL CHECK (status IN ('Open', 'Closed')) DEFAULT 'Open',
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
 
 

-- 11. ATTENDANCE_RECORDS (one row per student per session)

CREATE TABLE attendance_records (
    attendance_id SERIAL      PRIMARY KEY,
    session_id    INT         NOT NULL REFERENCES attendance_sessions(session_id),
    student_id    INT         NOT NULL REFERENCES students(student_id),
    status        VARCHAR(20) NOT NULL CHECK (status IN ('Present', 'Absent')),
    UNIQUE (session_id, student_id)          
);
 
 

-- 12. ATTENDANCE_THRESHOLDS 

CREATE TABLE attendance_thresholds (
    threshold_id         SERIAL       PRIMARY KEY,
    threshold_percentage NUMERIC(5,2) NOT NULL DEFAULT 80.00,
    effective_date       DATE         NOT NULL
);
 
 

-- Seed: default roles

INSERT INTO roles (role_name) VALUES
    ('Administrator'),
    ('Lecturer'),
    ('Student');