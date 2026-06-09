#!/usr/bin/env python3
"""
Update SIBAS database with proper bcrypt hashed passwords.
This script connects to PostgreSQL and replaces plain-text passwords with bcrypt hashes.
"""
import psycopg2
from psycopg2 import Error

# Database connection details
DB_CONFIG = {
    'dbname': 'sibas_db',
    'user': 'postgres',
    'password': 'incorrect6307',
    'host': 'localhost',
    'port': '5433'
}

# Bcrypt hashes (generated with cost factor 12)
ADMIN_HASH = '$2b$12$pwGv8oCpP.b3pM2gThlP2uZn7OTm1hvXCMvNkF9W3XuXUEYOfS47O'
LECTURER_HASH = '$2b$12$qnCjOyXPZEu0F2z4iydjJujWWXa4pkoYkMjkJc.YfUZpqQUnVrF.2'
STUDENT_HASH = '$2b$12$vkr0BsZBJmWYFZOVcQp.yu8XIqBX95QV2x5KMGOeknnkNeDp2/e/m'

# Password mapping: role_id -> hash
PASSWORD_BY_ROLE = {
    1: ADMIN_HASH,      # Administrator
    2: LECTURER_HASH,   # Lecturer
    3: STUDENT_HASH     # Student
}

def update_passwords():
    """Update all user passwords in the database with bcrypt hashes."""
    try:
        # Connect to database
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("=" * 70)
        print("SIBAS DATABASE PASSWORD UPDATE SCRIPT")
        print("=" * 70)
        print()
        
        # Get current user count
        cursor.execute("SELECT COUNT(*) FROM users;")
        total_users = cursor.fetchone()[0]
        print(f"📊 Total users in database: {total_users}")
        print()
        
        # Display current passwords (for verification)
        print("Current passwords in database:")
        print("-" * 70)
        cursor.execute("SELECT user_id, username, password, role_id FROM users LIMIT 5;")
        for row in cursor.fetchall():
            user_id, username, password, role_id = row
            print(f"  {user_id}. {username:30} | Password: {password[:30]}...")
        print()
        
        # Update passwords by role
        updated_count = 0
        for role_id, hash_value in PASSWORD_BY_ROLE.items():
            cursor.execute(
                "UPDATE users SET password = %s WHERE role_id = %s;",
                (hash_value, role_id)
            )
            rows_updated = cursor.rowcount
            updated_count += rows_updated
            
            role_names = {1: 'Administrator', 2: 'Lecturer', 3: 'Student'}
            print(f"✅ Updated {rows_updated} {role_names[role_id]} account(s)")
        
        # Commit changes
        connection.commit()
        print()
        print("=" * 70)
        print(f"✨ SUCCESS! Updated {updated_count} user passwords")
        print("=" * 70)
        print()
        
        # Verify update
        print("Verification - Passwords after update:")
        print("-" * 70)
        cursor.execute("SELECT user_id, username, password, role_id FROM users LIMIT 5;")
        for row in cursor.fetchall():
            user_id, username, password, role_id = row
            print(f"  {user_id}. {username:30} | Hash: {password[:30]}...")
        print()
        
        print("=" * 70)
        print("TEST CREDENTIALS:")
        print("=" * 70)
        print("Admin:     admin_ford_pines   / admin_password")
        print("Lecturer:  lec_eda_clawthorne / lecturer_password")
        print("Student:   stu_marinette_dupain / student_password")
        print("=" * 70)
        
        cursor.close()
        
    except Error as e:
        print(f"❌ Database Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if connection:
            connection.close()
            print("\n✓ Database connection closed")
    
    return True

if __name__ == "__main__":
    success = update_passwords()
    exit(0 if success else 1)
