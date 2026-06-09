import streamlit as st
import psycopg2

from auth.authentication import login_screen, logout_user
from auth.user_management import render_user_management
from students.student_dashboard import student_dashboard
from students.student_management import student_management_page
from students.csv_import import bulk_upload_students


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
    st.set_page_config(
        page_title="SIBAS Attendance System",
        page_icon="📘",
        layout="wide"
    )

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "role" not in st.session_state:
        st.session_state["role"] = None
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    if "student_id" not in st.session_state:
        st.session_state["student_id"] = None
    if "full_name" not in st.session_state:
        st.session_state["full_name"] = None

    if not st.session_state["authenticated"]:
        login_screen(get_db_connection)
    else:
        st.sidebar.markdown(f"### Welcome, **{st.session_state['full_name']}**")
        st.sidebar.info(f"Role: {st.session_state['role']}")

        options = ["Home"]

        if st.session_state["role"] == "Administrator":
            options.append("Manage Users")
            options.append("Student Management")
            options.append("Bulk Student Upload")
            options.append("System Audit Reports")

        elif st.session_state["role"] == "Lecturer":
            options.append("Attendance Roster Sessions")

        elif st.session_state["role"] == "Student":
            options.append("Student Dashboard")

        choice = st.sidebar.radio("Navigation Panel Menu", options)

        if st.sidebar.button("Logout"):
            logout_user()

        if choice == "Home":
            st.title("SIBAS Attendance Management System")
            st.write("Welcome to the Student Information and Biometric Attendance System.")

        elif choice == "Student Dashboard":
            student_dashboard(st.session_state["student_id"])

        elif choice == "Manage Users":
            render_user_management(get_db_connection)

        elif choice == "Student Management":
            student_management_page()

        elif choice == "Bulk Student Upload":
            bulk_upload_students()

        elif choice == "Attendance Roster Sessions":
            st.info("Attendance module will be added here.")

        elif choice == "System Audit Reports":
            st.info("Reports module will be added here.")


if __name__ == "__main__":
    main()