import streamlit as st
import bcrypt

def hash_password(password: str) -> str:
    """Hashes a plain-text password using bcrypt string formatting."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against an existing bcrypt hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def login_user(connection, username, password):
    """
    Authenticates a user against database records.
    Uses parameterized statements to absolutely eliminate SQL injection risk.
    """
    cursor = connection.cursor()

    query = """
        SELECT u.user_id, u.username, u.password, r.role_name, u.is_active
        FROM users u
        JOIN roles r ON u.role_id = r.role_id
        WHERE u.username = %s;
    """

    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        user_id, uname, hashed_pw, role_name, is_active = user

        if not is_active:
            st.error(
                "Authentication Failure: This user account has been deactivated."
            )
            return False

        if verify_password(password, hashed_pw):

            st.session_state['authenticated'] = True
            st.session_state['user_id'] = user_id
            st.session_state['username'] = uname
            st.session_state['role'] = role_name
            st.session_state['student_id'] = None

            st.session_state['full_name'] = uname

            cursor = connection.cursor()

            if role_name == "Student":

                cursor.execute(
                    """
                    SELECT student_id, full_name
                    FROM students
                    WHERE user_id = %s
                    """,
                    (user_id,)
                )

                result = cursor.fetchone()

                if result:
                    st.session_state['student_id'] = result[0]
                    st.session_state['full_name'] = result[1]

            elif role_name == "Lecturer":

                cursor.execute(
                    """
                    SELECT full_name
                    FROM lecturers
                    WHERE user_id = %s
                    """,
                    (user_id,)
                )

                result = cursor.fetchone()

                if result:
                    st.session_state['full_name'] = result[0]

            elif role_name == "Administrator":

                cursor.execute(
                    """
                    SELECT full_name
                    FROM administrators
                    WHERE user_id = %s
                    """,
                    (user_id,)
                )

                result = cursor.fetchone()

                if result:
                    st.session_state['full_name'] = result[0]

            cursor.close()

            return True

    return False

def logout_user():
    """Flushes active context from state storage to safely terminate the session."""
    st.session_state['authenticated'] = False
    st.session_state['user_id'] = None
    st.session_state['username'] = None
    st.session_state['role'] = None
    st.session_state['student_id'] = None
    st.session_state['full_name'] = None
    st.rerun()

def login_screen(get_connection_func):
    """Renders the front-facing Streamlit login card components."""
    st.markdown("<h2 style='text-align: center;'>SIBAS Login Portal</h2>", unsafe_allow_html=True)

    with st.form("sibas_login_form"):
        username = st.text_input("Username Input", placeholder="Enter username...")
        password = st.text_input("Password Input", type="password", placeholder="Enter password...")
        submit_btn = st.form_submit_button("Sign In")
        
        if submit_btn:
            if not username or not password:
                st.warning("Please supply both authentication values.")
            else:
                conn = get_connection_func()
                if conn:
                    try:
                        if login_user(conn, username, password):
                            st.success("Access Granted. Redirecting to landing portal...")
                            st.rerun()
                        else:
                            st.error("Invalid credentials or access rejected.")
                    except Exception as e:
                        st.error(f"System Error encountered: {e}")
                    finally:
                        conn.close()