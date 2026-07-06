import streamlit as st
from auth.authentication import login_screen, logout_user
from auth.user_management import render_user_management
from students.student_dashboard import student_dashboard
from students.student_management import student_management_page
from students.csv_import import bulk_upload_students
from admin.dashboard import render_admin_dashboard
from attendance.attendance_management import attendance_page
from db.connection import get_connection as get_db_connection

def main():
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

    if not st.session_state['authenticated']:
        login_screen(get_db_connection)
    else:
        st.sidebar.markdown(f"### Welcome, **{st.session_state['full_name']}**")
        st.sidebar.info(f"Designated Role: {st.session_state['role']}")

        options = []
        
        if st.session_state['role'] == 'Administrator':
            options.append("Admin Dashboard") 
            options.append("Manage Users")
            options.append("Student Management")
            options.append("Bulk Upload Students")  
        elif st.session_state['role'] == 'Lecturer':
            options.append("Attendance Roster Sessions")
        elif st.session_state['role'] == 'Student':
            options.append("Student Dashboard")
            
        choice = st.sidebar.radio("Navigation Panel Menu", options)

        if st.sidebar.button("Terminate Session (Sign Out)"):
            logout_user()

        if choice == "Student Dashboard":
            student_dashboard(st.session_state['student_id']) 
        elif choice == "Manage Users":
            render_user_management(get_db_connection)
        elif choice == "Student Management":
            student_management_page()
        elif choice == "Admin Dashboard":
            render_admin_dashboard(get_db_connection)
        elif choice == "Bulk Upload Students":
            bulk_upload_students()
        elif choice == "Attendance Roster Sessions":
            attendance_page()

if __name__ == "__main__":
    main()