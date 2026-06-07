import streamlit as st
import psycopg2
from app.db.connection import get_connection


def register_student():
    st.subheader("Register New Student")

    matric_no = st.text_input("Matriculation Number")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    department_id = st.number_input("Department ID", min_value=1, step=1)
    programme = st.text_input("Programme / Course of Study")
    level = st.selectbox("Level", ["100", "200", "300", "400", "500"])

    if st.button("Register Student"):
        if not matric_no or not full_name or not email or not programme:
            st.error("Please fill all required fields.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO students 
                (matric_no, full_name, email, department_id, programme, level)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (matric_no, full_name, email, department_id, programme, level)
            )

            conn.commit()
            st.success("Student registered successfully.")

        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            st.error("A student with this matric number or email already exists.")

        except Exception as e:
            conn.rollback()
            st.error(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()


def assign_student_to_course():
    st.subheader("Assign Student to Course")

    matric_no = st.text_input("Enter Student Matric Number")
    course_id = st.number_input("Course ID", min_value=1, step=1)

    if st.button("Assign Course"):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT student_id FROM students WHERE matric_no = %s",
                (matric_no,)
            )

            student = cursor.fetchone()

            if student is None:
                st.error("Student not found.")
                return

            student_id = student[0]

            cursor.execute(
                """
                INSERT INTO student_course (student_id, course_id)
                VALUES (%s, %s)
                """,
                (student_id, course_id)
            )

            conn.commit()
            st.success("Student assigned to course successfully.")

        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            st.warning("This student is already assigned to this course.")

        except Exception as e:
            conn.rollback()
            st.error(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()


def student_management_page():
    st.title("Student Management")

    menu = st.sidebar.selectbox(
        "Student Management Menu",
        ["Register Student", "Assign Course"]
    )

    if menu == "Register Student":
        register_student()

    elif menu == "Assign Course":
        assign_student_to_course()