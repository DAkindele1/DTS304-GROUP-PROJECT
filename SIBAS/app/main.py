import streamlit as st
import psycopg2
from auth.authentication import login_screen, logout_user
from auth.user_management import render_user_management
from admin.dashboard import render_admin_dashboard

# Secure Connection Method Wrapper passed dynamically to modules
def get_db_connection():
    try:
        return psycopg2.connect(
            dbname="sibas_db",
            user="postgres",
            password="Nnamo28",
            host="localhost",
            port="5432"
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

    # Application Routing Engine
    if not st.session_state['authenticated']:
        login_screen(get_db_connection)
    else:
        # Sidebar Context Panel Layout
        st.sidebar.markdown(f"### Welcome, **{st.session_state['username']}**")
        st.sidebar.info(f"Designated Role: {st.session_state['role']}")
        
        # Conditional Navigation based on Role Capabilities (RBAC Engine)
        options = ["Home Dashboard"]
        
        if st.session_state['role'] == 'Administrator':
            options.append("Manage Users")
            options.append("Student Registry")  # Raymond's module
            options.append("System Audit Reports")  # David Akindele's module
        elif st.session_state['role'] == 'Lecturer':
            options.append("Attendance Roster Sessions")  # David Okenla's module
        elif st.session_state['role'] == 'Student':
            options.append("Personal Performance Tracking")  # Raymond's Dashboard
            
        choice = st.sidebar.radio("Navigation Panel Menu", options)
        
        # Instantiate Logout Trigger Option 
        if st.sidebar.button("Terminate Session (Sign Out)"):
            logout_user()

        # Route Selected Action Target Block
        if choice == "Home Dashboard":
            if st.session_state['role'] == 'Administrator':
                render_admin_dashboard(get_db_connection)
            else:
                st.write(f"Welcome to your dashboard view, {st.session_state['username']}!")
        elif choice == "Manage Users":
            render_user_management(get_db_connection)
        # Remaining layout checks link cleanly into alternative developer modules...

if __name__ == "__main__":
    main()