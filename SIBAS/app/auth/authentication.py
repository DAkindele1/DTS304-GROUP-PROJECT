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
    # Explicitly pull user parameters alongside their assigned role name.
    # Note: Column is u.password matching the SIBAS schema.
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
        
        # BR17: Deactivated users shall not be allowed system entry
        if not is_active:
            st.error("Authentication Failure: This user account has been deactivated.")
            return False
        
        # Verify plain text entry against stored hash
        if verify_password(password, hashed_pw):
            st.session_state['authenticated'] = True
            st.session_state['user_id'] = user_id
            st.session_state['username'] = uname
            st.session_state['role'] = role_name
            return True
            
    return False

def logout_user():
    """Flushes active context from state storage to safely terminate the session."""
    st.session_state['authenticated'] = False
    st.session_state['user_id'] = None
    st.session_state['username'] = None
    st.session_state['role'] = None
    st.rerun()

def login_screen(get_connection_func):
    """Renders the front-facing Streamlit login card components."""
    st.markdown("<h2 style='text-align: center;'>SIBAS Login Portal</h2>", unsafe_allow_html=True)
    
    # Render interactive input boxes within a standard secure container form
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