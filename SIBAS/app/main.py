import streamlit as st

from students.student_management import student_management_page
from students.csv_import import bulk_upload_students


def main():
    st.set_page_config(
        page_title="SIBAS Attendance System",
        page_icon="📘",
        layout="wide"
    )

    st.title("SIBAS Attendance Management System")

    menu = st.sidebar.selectbox(
        "Main Menu",
        [
            "Home",
            "Student Management",
            "Bulk Student Upload",
            "Attendance Management",
            "Reports"
        ]
    )

    if menu == "Home":
        st.subheader("Welcome to SIBAS")
        st.write("This system manages students, courses, attendance sessions, and attendance reports.")

    elif menu == "Student Management":
        student_management_page()

    elif menu == "Bulk Student Upload":
        bulk_upload_students()

    elif menu == "Attendance Management":
        st.info("Attendance Management module will be added by the attendance developer.")

    elif menu == "Reports":
        st.info("Reports module will be added by the reporting developer.")


if __name__ == "__main__":
    main()