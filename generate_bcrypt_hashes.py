#!/usr/bin/env python3
"""
Generate bcrypt hashes for SIBAS database sample data.
Run this to see what the actual hashes should be.
"""
import bcrypt

# Passwords for different roles
admin_password = "admin_password"
lecturer_password = "lecturer_password"
student_password = "student_password"

# Generate hashes
admin_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
lecturer_hash = bcrypt.hashpw(lecturer_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
student_hash = bcrypt.hashpw(student_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print("=" * 70)
print("BCRYPT HASH GENERATOR FOR SIBAS DATABASE")
print("=" * 70)
print()
print(f"Admin Password:    '{admin_password}'")
print(f"Admin Hash:        {admin_hash}")
print()
print(f"Lecturer Password: '{lecturer_password}'")
print(f"Lecturer Hash:     {lecturer_hash}")
print()
print(f"Student Password:  '{student_password}'")
print(f"Student Hash:      {student_hash}")
print()
print("=" * 70)
print("SQL TEMPLATE FOR USERS TABLE:")
print("=" * 70)
print()
print("-- Administrators")
print("INSERT INTO users (username, password, role_id) VALUES")
print(f"    ('admin_ford_pines',   '{admin_hash}', 1),")
print(f"    ('admin_grunkle_stan', '{admin_hash}', 1);")
print()
print("-- Lecturers")
print("INSERT INTO users (username, password, role_id) VALUES")
print(f"    ('lec_eda_clawthorne',  '{lecturer_hash}', 2),")
print(f"    ('lec_queen_moon',      '{lecturer_hash}', 2),")
print(f"    ('lec_alador_blight',   '{lecturer_hash}', 2);")
print()
print("-- Students (sample)")
print("INSERT INTO users (username, password, role_id) VALUES")
print(f"    ('stu_marinette_dupain',   '{student_hash}', 3),")
print(f"    ('stu_adrien_agreste',     '{student_hash}', 3),")
print(f"    ('stu_alya_cesaire',       '{student_hash}', 3);")
print()
print("=" * 70)
print("TEST CREDENTIALS:")
print("=" * 70)
print("Admin:     Username: admin_ford_pines    | Password: admin_password")
print("Lecturer:  Username: lec_eda_clawthorne  | Password: lecturer_password")
print("Student:   Username: stu_marinette_dupain | Password: student_password")
print("=" * 70)
