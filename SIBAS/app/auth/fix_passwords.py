import psycopg2
import bcrypt

def reset_sample_passwords():
    default_password = "password123"
    salt = bcrypt.gensalt()
    real_hash = bcrypt.hashpw(default_password.encode('utf-8'), salt).decode('utf-8')

    try:
        conn = psycopg2.connect(
            dbname="sibas_db",
            user="postgres",
            password="incorrect6307", 
            host="localhost",
            port="5433"
        )
        cursor = conn.cursor()

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