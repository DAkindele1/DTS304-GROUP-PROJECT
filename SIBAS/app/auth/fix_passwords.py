import psycopg2
import bcrypt

def reset_sample_passwords():
    # 1. Generate a real bcrypt hash for the default testing password
    default_password = "password123"
    salt = bcrypt.gensalt()
    real_hash = bcrypt.hashpw(default_password.encode('utf-8'), salt).decode('utf-8')

    try:
        # 2. Connect to the database (Ensure password matches your local pgAdmin setup)
        conn = psycopg2.connect(
            dbname="sibas_db",
            user="postgres",
            password="incorrect6307", 
            host="localhost",
            port="5433"
        )
        cursor = conn.cursor()

        # 3. Overwrite all fake string hashes with the real bcrypt hash
        cursor.execute("UPDATE users SET password = %s;", (real_hash,))
        conn.commit()
        
        print(f"✅ Success! All user passwords have been encrypted properly.")
        print(f"You can now log in using the password: {default_password}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    reset_sample_passwords()