-- ============================================================
-- SIBAS - Sample Data Insertion Script with BCRYPT HASHES
-- ============================================================
-- IMPORTANT: All passwords are bcrypt hashed
-- Passwords used:
--   Admin accounts: 'admin_password' → $2b$12$Y1vR8X5...
--   Lecturer accounts: 'lecturer_password' → $2b$12$Z2wS9Y6...
--   Student accounts: 'student_password' → $2b$12$A3xT0Z7...
--
-- Generated with: bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
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
-- 3. USERS - WITH BCRYPT HASHED PASSWORDS
-- ============================================================

-- Administrators (role_id = 1) — Gravity Falls
-- Password: admin_password
INSERT INTO users (username, password, role_id) VALUES
    ('admin_ford_pines',   '$2b$12$pwGv8oCpP.b3pM2gThlP2uZn7OTm1hvXCMvNkF9W3XuXUEYOfS47O', 1),
    ('admin_grunkle_stan', '$2b$12$pwGv8oCpP.b3pM2gThlP2uZn7OTm1hvXCMvNkF9W3XuXUEYOfS47O', 1);

-- Lecturers (role_id = 2) — Owl House & Star vs Forces of Evil
-- Password: lecturer_password
INSERT INTO users (username, password, role_id) VALUES
    ('lec_eda_clawthorne',  '$2b$12$qnCjOyXPZEu0F2z4iydjJujWWXa4pkoYkMjkJc.YfUZpqQUnVrF.2', 2),
    ('lec_queen_moon',      '$2b$12$qnCjOyXPZEu0F2z4iydjJujWWXa4pkoYkMjkJc.YfUZpqQUnVrF.2', 2),
    ('lec_alador_blight',   '$2b$12$qnCjOyXPZEu0F2z4iydjJujWWXa4pkoYkMjkJc.YfUZpqQUnVrF.2', 2);

-- Students (role_id = 3)
-- Password: student_password
-- Miraculous Ladybug
INSERT INTO users (username, password, role_id) VALUES
    ('stu_marinette_dupain',   '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_adrien_agreste',     '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_alya_cesaire',       '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_nino_lahiffe',       '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_chloe_bourgeois',    '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3);

-- Gravity Falls
INSERT INTO users (username, password, role_id) VALUES
    ('stu_dipper_pines',       '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_mabel_pines',        '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_wendy_corduroy',     '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3);

-- Equestria Girls
INSERT INTO users (username, password, role_id) VALUES
    ('stu_twilight_sparkle',   '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_rainbow_dash',       '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_rarity',             '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_applejack',          '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_fluttershy',         '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_pinkie_pie',         '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_sunset_shimmer',     '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3);

-- Owl House
INSERT INTO users (username, password, role_id) VALUES
    ('stu_luz_noceda',         '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_amity_blight',       '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_willow_park',        '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_gus_porter',         '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_hunter',             '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3);

-- Star vs Forces of Evil
INSERT INTO users (username, password, role_id) VALUES
    ('stu_star_butterfly',     '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_marco_diaz',         '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_janna_ordonia',      '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3),
    ('stu_starfan13',          '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m', 3);


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
    (3, 5, 'Eda Clawthorne',   'eda.clawthorne@pau.edu.ng'),
    (4, 3, 'Queen Moon Butterfly', 'moon.butterfly@pau.edu.ng'),
    (5, 1, 'Alador Blight',    'alador.blight@pau.edu.ng');


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
    (23, 5, '2023/PM/003', 'Willow Park',   'willow.park@pau.edu.ng',   'Philosophy & Magic Studies', 300),
    (24, 1, '2023/CS/008', 'Gus Porter',    'gus.porter@pau.edu.ng',    'Computer Science',           200),
    (25, 1, '2023/CS/009', 'Hunter Wittebane', 'hunter.w@pau.edu.ng',   'Computer Science',           300);

-- Star vs Forces of Evil (user_id 26–29)
INSERT INTO students (user_id, department_id, matric_no, full_name, email, course, level) VALUES
    (26, 5, '2023/PM/004', 'Star Butterfly', 'star.butterfly@pau.edu.ng', 'Philosophy & Magic Studies', 300),
    (27, 1, '2023/CS/010', 'Marco Diaz',     'marco.diaz@pau.edu.ng',     'Computer Science',           300),
    (28, 5, '2023/PM/005', 'Janna Ordonia',  'janna.ordonia@pau.edu.ng',  'Philosophy & Magic Studies', 200),
    (29, 3, '2023/CA/005', 'StarFan13',      'starfan13@pau.edu.ng',      'Creative Arts',              200);


-- ============================================================
-- 7. COURSES
-- ============================================================
INSERT INTO courses (course_code, course_title, department_id) VALUES
    ('CSC301', 'Data Structures and Algorithms',     1),
    ('CSC305', 'Object-Oriented Programming',        1),
    ('CSC309', 'Database Management Systems',        1),
    ('FDT201', 'Textile Design Fundamentals',        2),
    ('CAP201', 'Visual Arts & Digital Media',        3),
    ('ENV301', 'Ecology and Conservation',           4),
    ('PMS301', 'Advanced Magic Theory',              5),
    ('PMS201', 'Introduction to Spellcasting',       5);


-- ============================================================
-- 8. LECTURER_TEACHES
-- lecturer_id 1 = Eda, 2 = Queen Moon, 3 = Alador
-- ============================================================
INSERT INTO lecturer_teaches (lecturer_id, course_id) VALUES
    (3, 1),   -- Alador teaches CSC301
    (3, 2),   -- Alador teaches CSC305
    (3, 3),   -- Alador teaches CSC309
    (2, 5),   -- Queen Moon teaches CAP201
    (1, 7),   -- Eda teaches Advanced Magic Theory
    (1, 8);   -- Eda teaches Intro to Spellcasting


-- ============================================================
-- 9. STUDENT_ENROLLED
-- ============================================================

INSERT INTO student_enrolled (student_id, course_id) VALUES
    (1, 1), (1, 2), (1, 3),   -- Marinette: all CS courses
    (2, 1), (2, 2),           -- Adrien: CSC301 + CSC305
    (3, 1), (3, 3),           -- Alya: CSC301 + CSC309
    (4, 2), (4, 3),           -- Nino: CSC305 + CSC309
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
    (13, 7),                   -- Fluttershy: Advanced Magic Theory
    (14, 5), (14, 3),          -- Pinkie Pie: Visual Arts + CSC309
    (15, 1), (15, 2), (15, 3); -- Sunset Shimmer: all CS courses

INSERT INTO student_enrolled (student_id, course_id) VALUES
    (16, 7), (16, 8),          -- Luz: both magic courses
    (17, 1),                   -- Amity: CSC301
    (18, 7), (18, 8),          -- Willow: both magic courses
    (19, 2),                   -- Gus: CSC305
    (20, 1), (20, 3);          -- Hunter: CSC301 + CSC309

INSERT INTO student_enrolled (student_id, course_id) VALUES
    (21, 7), (21, 8),          -- Star: both magic courses
    (22, 1), (22, 2),          -- Marco: CSC301 + CSC305
    (23, 8),                   -- Janna: Intro to Spellcasting
    (24, 5);                   -- StarFan13: Visual Arts


-- ============================================================
-- 10. ATTENDANCE_SESSIONS
-- ============================================================
INSERT INTO attendance_sessions (course_id, lecturer_id, session_date, session_time) VALUES
    (1, 3, '2025-01-13', '08:00:00'),   -- CSC301 session 1
    (1, 3, '2025-01-15', '08:00:00'),   -- CSC301 session 2
    (1, 3, '2025-01-17', '08:00:00'),   -- CSC301 session 3
    (2, 3, '2025-01-13', '10:00:00'),   -- CSC305 session 1
    (2, 3, '2025-01-15', '10:00:00'),   -- CSC305 session 2
    (3, 3, '2025-01-14', '08:00:00'),   -- CSC309 session 1
    (5, 2, '2025-01-16', '09:00:00'),   -- Visual Arts session 1
    (7, 1, '2025-01-14', '14:00:00'),   -- Advanced Magic Theory session 1
    (7, 1, '2025-01-16', '14:00:00'),   -- Advanced Magic Theory session 2
    (8, 1, '2025-01-18', '13:00:00');   -- Intro to Spellcasting session 1


-- ============================================================
-- 11. ATTENDANCE_RECORDS
-- ============================================================

-- CSC301 session 1 (session_id=1)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (1, 1,  'Present'),
    (1, 2,  'Present'),
    (1, 3,  'Present'),
    (1, 4,  'Absent'),
    (1, 9,  'Present'),
    (1, 15, 'Present'),
    (1, 17, 'Present'),
    (1, 20, 'Present'),
    (1, 22, 'Present');

-- CSC301 session 2 (session_id=2)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (2, 1,  'Present'),
    (2, 2,  'Absent'),
    (2, 3,  'Present'),
    (2, 4,  'Present'),
    (2, 9,  'Present'),
    (2, 15, 'Present'),
    (2, 17, 'Present'),
    (2, 20, 'Present'),
    (2, 22, 'Present');

-- CSC301 session 3 (session_id=3)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (3, 1,  'Present'),
    (3, 2,  'Present'),
    (3, 3,  'Present'),
    (3, 4,  'Present'),
    (3, 9,  'Present'),
    (3, 15, 'Present'),
    (3, 17, 'Present'),
    (3, 20, 'Absent'),
    (3, 22, 'Absent');

-- CSC305 session 1 (session_id=4)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (4, 1,  'Present'),
    (4, 2,  'Present'),
    (4, 9,  'Present'),
    (4, 15, 'Present'),
    (4, 17, 'Present');

-- CSC305 session 2 (session_id=5)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (5, 1,  'Absent'),
    (5, 2,  'Present'),
    (5, 9,  'Present'),
    (5, 15, 'Present'),
    (5, 17, 'Present');

-- CSC309 session 1 (session_id=6)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (6, 1,  'Present'),
    (6, 3,  'Present'),
    (6, 4,  'Present'),
    (6, 14, 'Present'),
    (6, 20, 'Present'),
    (6, 22, 'Present');

-- Visual Arts session 1 (session_id=7)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (7, 7,  'Present'),
    (7, 10, 'Present'),
    (7, 14, 'Present'),
    (7, 19, 'Present');

-- Advanced Magic Theory session 1 (session_id=8)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (8, 16, 'Present'),
    (8, 18, 'Present'),
    (8, 21, 'Present'),
    (8, 23, 'Absent');

-- Advanced Magic Theory session 2 (session_id=9)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (9, 16, 'Present'),
    (9, 18, 'Present'),
    (9, 21, 'Present'),
    (9, 23, 'Present');

-- Intro to Spellcasting session 1 (session_id=10)
INSERT INTO attendance_records (session_id, student_id, status) VALUES
    (10, 13, 'Present'),
    (10, 16, 'Present'),
    (10, 18, 'Absent'),
    (10, 21, 'Present');


-- ============================================================
-- 12. ATTENDANCE_THRESHOLDS
-- ============================================================
INSERT INTO attendance_thresholds (threshold_percentage, effective_date) VALUES
    (80.00, '2025-01-01');
