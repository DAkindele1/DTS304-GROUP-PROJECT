-- ============================================================
-- SIBAS - Sample Data Insertion Script (Cartoon Characters Edition)
-- ============================================================
-- Run order: sibas_schema.sql → sibas_indexes.sql → this file
-- ============================================================


-- ============================================================
-- 1. ROLES (seeded in schema already)
-- ============================================================
-- role_id 1 = Administrator, 2 = Lecturer, 3 = Student


-- ============================================================
-- 2. DEPARTMENTS
-- ============================================================
INSERT INTO departments (department_name) VALUES
    ('Computer Science'),
    ('Fashion Design & Technology'),
    ('Creative Arts'),
    ('Environmental Science'),
    ('Philosophy & Magic Studies');


-- ============================================================
-- 3. USERS
-- ============================================================

-- Administrators (role_id = 1) — Gravity Falls
INSERT INTO users (username, password, role_id) VALUES
    ('admin_ford_pines',   'hashed_password_001', 1),
    ('admin_grunkle_stan', 'hashed_password_002', 1);

-- Lecturers (role_id = 2) — Owl House & Star vs Forces of Evil
INSERT INTO users (username, password, role_id) VALUES
    ('lec_eda_clawthorne',  'hashed_password_003', 2),   -- Owl House
    ('lec_queen_moon',      'hashed_password_004', 2),   -- Star vs Forces of Evil
    ('lec_alador_blight',   'hashed_password_005', 2);   -- Owl House

-- Students (role_id = 3)
-- Miraculous Ladybug
INSERT INTO users (username, password, role_id) VALUES
    ('stu_marinette_dupain',   'hashed_password_006', 3),
    ('stu_adrien_agreste',     'hashed_password_007', 3),
    ('stu_alya_cesaire',       'hashed_password_008', 3),
    ('stu_nino_lahiffe',       'hashed_password_009', 3),
    ('stu_chloe_bourgeois',    'hashed_password_010', 3);

-- Gravity Falls
INSERT INTO users (username, password, role_id) VALUES
    ('stu_dipper_pines',       'hashed_password_011', 3),
    ('stu_mabel_pines',        'hashed_password_012', 3),
    ('stu_wendy_corduroy',     'hashed_password_013', 3);

-- Equestria Girls
INSERT INTO users (username, password, role_id) VALUES
    ('stu_twilight_sparkle',   'hashed_password_014', 3),
    ('stu_rainbow_dash',       'hashed_password_015', 3),
    ('stu_rarity',             'hashed_password_016', 3),
    ('stu_applejack',          'hashed_password_017', 3),
    ('stu_fluttershy',         'hashed_password_018', 3),
    ('stu_pinkie_pie',         'hashed_password_019', 3),
    ('stu_sunset_shimmer',     'hashed_password_020', 3);

-- Owl House
INSERT INTO users (username, password, role_id) VALUES
    ('stu_luz_noceda',         'hashed_password_021', 3),
    ('stu_amity_blight',       'hashed_password_022', 3),
    ('stu_willow_park',        'hashed_password_023', 3),
    ('stu_gus_porter',         'hashed_password_024', 3),
    ('stu_hunter',             'hashed_password_025', 3);

-- Star vs Forces of Evil
INSERT INTO users (username, password, role_id) VALUES
    ('stu_star_butterfly',     'hashed_password_026', 3),
    ('stu_marco_diaz',         'hashed_password_027', 3),
    ('stu_janna_ordonia',      'hashed_password_028', 3),
    ('stu_starfan13',          'hashed_password_029', 3);


-- ============================================================
-- 4. ADMINISTRATORS — Gravity Falls
-- user_id 1 = admin_ford_pines, 2 = admin_grunkle_stan
-- ============================================================
INSERT INTO administrators (user_id, full_name) VALUES
    (1, 'Ford Pines'),
    (2, 'Stanford "Grunkle Stan" Pines');


-- ============================================================
-- 5. LECTURERS
-- user_id 3 = Eda, 4 = Queen Moon, 5 = Alador
-- ============================================================
INSERT INTO lecturers (user_id, department_id, full_name, email) VALUES
    (3, 5, 'Eda Clawthorne',   'eda.clawthorne@pau.edu.ng'),      -- Philosophy & Magic Studies
    (4, 3, 'Queen Moon Butterfly', 'moon.butterfly@pau.edu.ng'),  -- Creative Arts
    (5, 1, 'Alador Blight',    'alador.blight@pau.edu.ng');       -- Computer Science


-- ============================================================
-- 6. STUDENTS
-- ============================================================

-- Miraculous Ladybug (user_id 6–10) — Computer Science (dept 1)
INSERT INTO students (user_id, department_id, matric_no, full_name, email, course, level) VALUES
    (6,  1, '2023/CS/001', 'Marinette Dupain-Cheng', 'marinette.dupain@pau.edu.ng',  'Computer Science', 300),
    (7,  1, '2023/CS/002', 'Adrien Agreste',          'adrien.agreste@pau.edu.ng',    'Computer Science', 300),
    (8,  1, '2023/CS/003', 'Alya Cesaire',            'alya.cesaire@pau.edu.ng',      'Computer Science', 300),
    (9,  1, '2023/CS/004', 'Nino Lahiffe',            'nino.lahiffe@pau.edu.ng',      'Computer Science', 300),
    (10, 2, '2023/FD/001', 'Chloe Bourgeois',         'chloe.bourgeois@pau.edu.ng',   'Fashion Design & Technology', 200);

-- Gravity Falls (user_id 11–13) — Environmental Science (dept 4)
INSERT INTO students (user_id, department_id, matric_no, full_name, email, course, level) VALUES
    (11, 4, '2023/ES/001', 'Dipper Pines',   'dipper.pines@pau.edu.ng',   'Environmental Science', 200),
    (12, 3, '2023/CA/001', 'Mabel Pines',    'mabel.pines@pau.edu.ng',    'Creative Arts',         200),
    (13, 4, '2023/ES/002', 'Wendy Corduroy', 'wendy.corduroy@pau.edu.ng', 'Environmental Science', 100);

-- Equestria Girls (user_id 14–20)
INSERT INTO students (user_id, department_id, matric_no, full_name, email, course, level) VALUES
    (14, 1, '2023/CS/005', 'Twilight Sparkle',  'twilight.sparkle@pau.edu.ng',  'Computer Science',            400),
    (15, 3, '2023/CA/002', 'Rainbow Dash',       'rainbow.dash@pau.edu.ng',      'Creative Arts',               300),
    (16, 2, '2023/FD/002', 'Rarity',             'rarity@pau.edu.ng',            'Fashion Design & Technology', 400),
    (17, 4, '2023/ES/003', 'Applejack',           'applejack@pau.edu.ng',         'Environmental Science',       300),
    (18, 5, '2023/PM/001', 'Fluttershy',          'fluttershy@pau.edu.ng',        'Philosophy & Magic Studies',  200),
    (19, 3, '2023/CA/003', 'Pinkie Pie',          'pinkie.pie@pau.edu.ng',        'Creative Arts',               200),
    (20, 1, '2023/CS/006', 'Sunset Shimmer',      'sunset.shimmer@pau.edu.ng',    'Computer Science',            400);

-- Owl House (user_id 21–25)
INSERT INTO students (user_id, department_id, matric_no, full_name, email, course, level) VALUES
    (21, 5, '2023/PM/002', 'Luz Noceda',    'luz.noceda@pau.edu.ng',    'Philosophy & Magic Studies', 200),
    (22, 1, '2023/CS/007', 'Amity Blight',  'amity.blight@pau.edu.ng',  'Computer Science',           300),
    (23, 4, '2023/ES/004', 'Willow Park',   'willow.park@pau.edu.ng',   'Environmental Science',      300),
    (24, 3, '2023/CA/004', 'Gus Porter',    'gus.porter@pau.edu.ng',    'Creative Arts',              200),
    (25, 1, '2023/CS/008', 'Hunter Wittebane', 'hunter.w@pau.edu.ng',   'Computer Science',           300);

-- Star vs Forces of Evil (user_id 26–29)
INSERT INTO students (user_id, department_id, matric_no, full_name, email, course, level) VALUES
    (26, 5, '2023/PM/003', 'Star Butterfly', 'star.butterfly@pau.edu.ng', 'Philosophy & Magic Studies', 300),
    (27, 1, '2023/CS/009', 'Marco Diaz',     'marco.diaz@pau.edu.ng',     'Computer Science',           300),
    (28, 5, '2023/PM/004', 'Janna Ordonia',  'janna.ordonia@pau.edu.ng',  'Philosophy & Magic Studies', 300),
    (29, 3, '2023/CA/005', 'StarFan13',      'starfan13@pau.edu.ng',      'Creative Arts',              200);


-- ============================================================
-- 7. COURSES
-- ============================================================
INSERT INTO courses (course_code, course_title, department_id) VALUES
    ('CSC301', 'Data Structures and Algorithms',     1),
    ('CSC305', 'Database Management Systems',        1),
    ('CSC309', 'Software Engineering',               1),
    ('FDT201', 'Textile Design and Construction',    2),
    ('CAT201', 'Visual Arts and Animation',          3),
    ('ENV201', 'Ecology and Nature Studies',         4),
    ('PMS301', 'Advanced Magic Theory',              5),
    ('PMS201', 'Introduction to Spellcasting',       5);


-- ============================================================
-- 8. lecturer_teaches
-- lecturer_id 1 = Eda, 2 = Queen Moon, 3 = Alador
-- ============================================================
INSERT INTO lecturer_teaches (lecturer_id, course_id) VALUES
    (3, 1),   -- Alador teaches CSC301
    (3, 2),   -- Alador teaches CSC305
    (3, 3),   -- Alador teaches CSC309
    (2, 5),   -- Queen Moon teaches Visual Arts
    (1, 7),   -- Eda teaches Advanced Magic Theory
    (1, 8);   -- Eda teaches Intro to Spellcasting


-- ============================================================
-- 9. student_enrolled
-- ============================================================

INSERT INTO student_enrolled (student_id, course_id) VALUES
    (1, 1), (1, 2), (1, 3),   -- Marinette: all CS courses
    (2, 1), (2, 2), (2, 3),   -- Adrien: all CS courses
    (3, 1), (3, 2),            -- Alya: CSC301 + CSC305
    (4, 1), (4, 3),            -- Nino: CSC301 + CSC309
    (5, 4);                    -- Chloe: Textile Design

INSERT INTO student_enrolled (student_id, course_id) VALUES
    (6, 6),                    -- Dipper: Ecology
    (7, 5),                    -- Mabel: Visual Arts
    (8, 6);                    -- Wendy: Ecology

INSERT INTO student_enrolled (student_id, course_id) VALUES
    (9,  1), (9,  2),          -- Twilight: CSC301 + CSC305
    (10, 5),                   -- Rainbow Dash: Visual Arts
    (11, 4),                   -- Rarity: Textile Design
    (12, 6),                   -- Applejack: Ecology
    (13, 8),                   -- Fluttershy: Intro to Spellcasting
    (14, 5),                   -- Pinkie Pie: Visual Arts
    (15, 1), (15, 2), (15, 3); -- Sunset Shimmer: all CS courses

INSERT INTO student_enrolled (student_id, course_id) VALUES
    (16, 7), (16, 8),          -- Luz: both magic courses
    (17, 1), (17, 2),          -- Amity: CSC301 + CSC305
    (18, 6),                   -- Willow: Ecology
    (19, 5),                   -- Gus: Visual Arts
    (20, 1), (20, 3);          -- Hunter: CSC301 + CSC309

INSERT INTO student_enrolled (student_id, course_id) VALUES
    (21, 7), (21, 8),          -- Star: both magic courses
    (22, 1), (22, 3),          -- Marco: CSC301 + CSC309
    (23, 7),                   -- Janna: Advanced Magic Theory
    (24, 5);                   -- StarFan13: Visual Arts


-- ============================================================
-- 10. ATTENDANCE_SESSIONS
-- ============================================================
INSERT INTO attendance_sessions (course_id, lecturer_id, session_date, session_time) VALUES
    (1, 3, '2025-01-13', '08:00:00'),   -- CSC301 session 1
    (1, 3, '2025-01-20', '08:00:00'),   -- CSC301 session 2
    (1, 3, '2025-01-27', '08:00:00'),   -- CSC301 session 3
    (2, 3, '2025-01-14', '10:00:00'),   -- CSC305 session 1
    (2, 3, '2025-01-21', '10:00:00'),   -- CSC305 session 2
    (3, 3, '2025-01-15', '12:00:00'),   -- CSC309 session 1
    (5, 2, '2025-01-16', '09:00:00'),   -- Visual Arts session 1
    (7, 1, '2025-01-17', '11:00:00'),   -- Advanced Magic Theory session 1
    (7, 1, '2025-01-24', '11:00:00'),   -- Advanced Magic Theory session 2
    (8, 1, '2025-01-18', '13:00:00');   -- Intro to Spellcasting session 1


-- ============================================================
-- 11. ATTENDANCE_RECORDS
-- ============================================================

-- CSC301 session 1 (session_id=1) — students: Marinette(1), Adrien(2), Alya(3), Nino(4), Twilight(9), Sunset(15), Amity(17), Hunter(20), Marco(22)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (1, 1,  'Present'),
    (1, 2,  'Present'),
    (1, 3,  'Present'),
    (1, 4,  'Absent'),
    (1, 9,  'Present'),
    (1, 15, 'Present'),
    (1, 17, 'Present'),
    (1, 20, 'Absent'),
    (1, 22, 'Present');

-- CSC301 session 2 (session_id=2)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (2, 1,  'Present'),
    (2, 2,  'Absent'),
    (2, 3,  'Present'),
    (2, 4,  'Present'),
    (2, 9,  'Present'),
    (2, 15, 'Present'),
    (2, 17, 'Absent'),
    (2, 20, 'Present'),
    (2, 22, 'Present');

-- CSC301 session 3 (session_id=3)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (3, 1,  'Present'),
    (3, 2,  'Present'),
    (3, 3,  'Absent'),
    (3, 4,  'Present'),
    (3, 9,  'Absent'),
    (3, 15, 'Present'),
    (3, 17, 'Present'),
    (3, 20, 'Present'),
    (3, 22, 'Absent');

-- CSC305 session 1 (session_id=4)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (4, 1,  'Present'),
    (4, 2,  'Present'),
    (4, 3,  'Present'),
    (4, 9,  'Present'),
    (4, 15, 'Absent'),
    (4, 17, 'Present');

-- CSC305 session 2 (session_id=5)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (5, 1,  'Absent'),
    (5, 2,  'Present'),
    (5, 3,  'Present'),
    (5, 9,  'Present'),
    (5, 15, 'Present'),
    (5, 17, 'Present');

-- CSC309 session 1 (session_id=6)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (6, 1,  'Present'),
    (6, 2,  'Present'),
    (6, 4,  'Absent'),
    (6, 15, 'Present'),
    (6, 20, 'Present'),
    (6, 22, 'Present');

-- Visual Arts session 1 (session_id=7)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (7, 7,  'Present'),   -- Mabel
    (7, 10, 'Present'),   -- Rainbow Dash
    (7, 14, 'Absent'),    -- Pinkie Pie
    (7, 19, 'Present');   -- Gus

-- Advanced Magic Theory session 1 (session_id=8)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (8, 16, 'Present'),   -- Luz
    (8, 21, 'Present'),   -- Star
    (8, 23, 'Absent');    -- Janna

-- Advanced Magic Theory session 2 (session_id=9)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (9, 16, 'Present'),   -- Luz
    (9, 21, 'Absent'),    -- Star
    (9, 23, 'Present');   -- Janna

-- Intro to Spellcasting session 1 (session_id=10)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (10, 13, 'Present'),  -- Fluttershy
    (10, 16, 'Present'),  -- Luz
    (10, 21, 'Present');  -- Star


-- ============================================================
-- 12. ATTENDANCE_THRESHOLDS
-- ============================================================
INSERT INTO attendance_thresholds (threshold_percentage, effective_date) VALUES
    (80.00, '2025-01-01');