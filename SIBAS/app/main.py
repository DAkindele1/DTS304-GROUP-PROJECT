import streamlit as st
import psycopg2
from auth.authentication import login_screen, logout_user
from auth.user_management import render_user_management
from students.student_dashboard import student_dashboard
from students.student_management import student_management_page


# Secure Connection Method Wrapper passed dynamically to modules
def get_db_connection():
    try:
        return psycopg2.connect(
            dbname="sibas_db",
            user="postgres",
            password="incorrect6307",
            host="localhost",
            port="5433"
        )
    except Exception as e:
        st.error(f"Database Connection Failure: {e}")
        return None

def main():
    """Main application entry point with proper Streamlit initialization."""
    # Instantiate default state variables safely
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'role' not in st.session_state:
        st.session_state['role'] = None
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
    if 'student_id' not in st.session_state:
        st.session_state['student_id'] = None
    if 'full_name' not in st.session_state:
        st.session_state['full_name'] = None

    # Application Routing Engine
    if not st.session_state['authenticated']:
        login_screen(get_db_connection)
    else:
        # Sidebar Context Panel Layout
        st.sidebar.markdown(f"### Welcome, **{st.session_state['full_name']}**")
        st.sidebar.info(f"Designated Role: {st.session_state['role']}")
        
        # Conditional Navigation based on Role Capabilities (RBAC Engine)
        options = []
        
        if st.session_state['role'] == 'Administrator':
            options.append("Admin Dashboard") 
            options.append("Manage Users")
            options.append("Student Management")  # Raymond's module
            options.append("System Audit Reports")  # David Akindele's module
        elif st.session_state['role'] == 'Lecturer':
            options.append("Attendance Roster Sessions")  # David Okenla's module
        elif st.session_state['role'] == 'Student':
            options.append("Student Dashboard")  # Raymond's Dashboard
            
        choice = st.sidebar.radio("Navigation Panel Menu", options)
        
        # Instantiate Logout Trigger Option 
        if st.sidebar.button("Terminate Session (Sign Out)"):
            logout_user()

        # Route Selected Action Target Block
        if choice == "Student Dashboard":
            student_dashboard(st.session_state['student_id'])  # Pass student_id for personalized data retrieval
        elif choice == "Manage Users":
            render_user_management(get_db_connection)
        elif choice == "Student Management":
            student_management_page()
        # Remaining layout checks link cleanly into alternative developer modules...

if __name__ == "__main__":
    main()