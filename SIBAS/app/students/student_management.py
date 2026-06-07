import streamlit as st
import pandas as pd
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
                (matric_no, full_name, email, department_id, programme, level, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, TRUE)
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


def view_all_students():
    st.subheader("All Registered Students")

    conn = get_connection()

    try:
        query = """
            SELECT 
                student_id,
                matric_no,
                full_name,
                email,
                programme,
                level,
                is_active
            FROM students
            ORDER BY full_name
        """

        df = pd.read_sql(query, conn)

        if df.empty:
            st.info("No students found.")
        else:
            st.dataframe(df)

    except Exception as e:
        st.error(f"Error loading students: {e}")

    finally:
        conn.close()


def search_student():
    st.subheader("Search Student")

    matric_no = st.text_input("Enter Matriculation Number")

    if st.button("Search"):
        conn = get_connection()

        try:
            query = """
                SELECT 
                    student_id,
                    matric_no,
                    full_name,
                    email,
                    programme,
                    level,
                    is_active
                FROM students
                WHERE matric_no = %s
            """

            df = pd.read_sql(query, conn, params=(matric_no,))

            if df.empty:
                st.warning("Student not found.")
            else:
                st.dataframe(df)

        except Exception as e:
            st.error(f"Error searching student: {e}")

        finally:
            conn.close()


def update_student():
    st.subheader("Update Student Details")

    matric_no = st.text_input("Enter Student Matric Number")

    if st.button("Load Student"):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT student_id, full_name, email, programme, level
                FROM students
                WHERE matric_no = %s
                """,
                (matric_no,)
            )

            student = cursor.fetchone()

            if student is None:
                st.error("Student not found.")
            else:
                st.session_state["edit_student"] = student
                st.success("Student loaded successfully.")

        except Exception as e:
            st.error(f"Error loading student: {e}")

        finally:
            cursor.close()
            conn.close()

    if "edit_student" in st.session_state:
        student_id, old_name, old_email, old_programme, old_level = st.session_state["edit_student"]

        full_name = st.text_input("Full Name", value=old_name)
        email = st.text_input("Email", value=old_email)
        programme = st.text_input("Programme", value=old_programme)
        level = st.selectbox(
            "Level",
            ["100", "200", "300", "400", "500"],
            index=["100", "200", "300", "400", "500"].index(str(old_level))
        )

        if st.button("Update Student"):
            conn = get_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    """
                    UPDATE students
                    SET full_name = %s,
                        email = %s,
                        programme = %s,
                        level = %s
                    WHERE student_id = %s
                    """,
                    (full_name, email, programme, level, student_id)
                )

                conn.commit()
                st.success("Student updated successfully.")
                del st.session_state["edit_student"]

            except Exception as e:
                conn.rollback()
                st.error(f"Error updating student: {e}")

            finally:
                cursor.close()
                conn.close()


def deactivate_student():
    st.subheader("Deactivate Student")

    matric_no = st.text_input("Enter Matric Number to Deactivate")

    if st.button("Deactivate"):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                UPDATE students
                SET is_active = FALSE
                WHERE matric_no = %s
                """,
                (matric_no,)
            )

            if cursor.rowcount == 0:
                st.warning("Student not found.")
            else:
                conn.commit()
                st.success("Student deactivated successfully.")

        except Exception as e:
            conn.rollback()
            st.error(f"Error deactivating student: {e}")

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
        [
            "Register Student",
            "View All Students",
            "Search Student",
            "Update Student",
            "Deactivate Student",
            "Assign Course"
        ]
    )

    if menu == "Register Student":
        register_student()

    elif menu == "View All Students":
        view_all_students()

    elif menu == "Search Student":
        search_student()

    elif menu == "Update Student":
        update_student()

    elif menu == "Deactivate Student":
        deactivate_student()

    elif menu == "Assign Course":
        assign_student_to_course()