import streamlit as st
import pandas as pd
import psycopg2
from db.connection import get_connection


def register_student():
    st.subheader("Register New Student")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            u.user_id,
            u.username
        FROM users u
        JOIN roles r
            ON u.role_id = r.role_id
        LEFT JOIN students s
            ON u.user_id = s.user_id
        WHERE r.role_name = 'Student'
        AND s.student_id IS NULL
        ORDER BY u.username
    """)

    available_users = cursor.fetchall()

    cursor.close()
    conn.close()

    if not available_users:
        st.warning(
            "No unlinked Student user accounts available. "
            "Create a Student user first."
        )
        return

    user_map = {
        f"{user[0]} - {user[1]}": user[0]
        for user in available_users
    }

    selected_user = st.selectbox(
        "Student User Account",
        list(user_map.keys())
    )

    user_id = user_map[selected_user]
    matric_no = st.text_input("Matriculation Number")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    department_course_map = {
        "Computer Science": (1, "Computer Science"),
        "Fashion Design & Technology": (2, "Fashion Design & Technology"),
        "Creative Arts": (3, "Creative Arts"),
        "Environmental Science": (4, "Environmental Science"),
        "Philosophy & Magic Studies": (5, "Philosophy & Magic Studies")
    }

    selected_department = st.selectbox(
        "Department",
        list(department_course_map.keys())
    )

    department_id, course = department_course_map[selected_department]

    st.text_input(
        "Course",
        value=course,
        disabled=True
    )
    level = st.selectbox("Level", ["100", "200", "300", "400", "500"])

    if st.button("Register Student"):
        if not matric_no or not full_name or not email or not course:
            st.error("Please fill all required fields.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO students 
                (user_id, matric_no, full_name, email, department_id, course, level)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (user_id, matric_no, full_name, email, department_id, course, level)
            )

            conn.commit()
            st.success("Student registered successfully.")

        except psycopg2.errors.UniqueViolation as e:
            conn.rollback()
            st.error(f"Unique constraint violated: {e}")

        except Exception as e:
            conn.rollback()
            st.error(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

def view_student_courses():
    st.subheader("View Student Courses")

    matric_no = st.text_input("Enter Student Matric Number")

    if st.button("View Courses"):
        conn = get_connection()

        try:
            query = """
                SELECT 
                    s.matric_no,
                    s.full_name,
                    c.course_code,
                    c.course_title
                FROM students s
                JOIN student_enrolled se
                    ON s.student_id = se.student_id
                JOIN courses c
                    ON se.course_id = c.course_id
                WHERE s.matric_no = %s
            """

            df = pd.read_sql(query, conn, params=(matric_no,))

            if df.empty:
                st.info("No courses found for this student.")
            else:
                st.dataframe(df)

        except Exception as e:
            st.error(f"Error loading student courses: {e}")

        finally:
            conn.close()

def view_all_students():
    st.subheader("All Registered Students")

    conn = get_connection()

    try:
        query = """
            SELECT 
                student_id,
                user_id,
                matric_no,
                full_name,
                email,
                department_id,
                course,
                level
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
                    user_id,
                    matric_no,
                    full_name,
                    email,
                    department_id,
                    course,
                    level
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
                SELECT student_id, full_name, email, course, level
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
        student_id, old_name, old_email, old_course, old_level = st.session_state["edit_student"]

        full_name = st.text_input("Full Name", value=old_name)
        email = st.text_input("Email", value=old_email)
        course = st.text_input("Course of Study", value=old_course)

        levels = ["100", "200", "300", "400", "500"]
        level_index = levels.index(str(old_level)) if str(old_level) in levels else 0

        level = st.selectbox("Level", levels, index=level_index)

        if st.button("Update Student"):
            conn = get_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    """
                    UPDATE students
                    SET full_name = %s,
                        email = %s,
                        course = %s,
                        level = %s
                    WHERE student_id = %s
                    """,
                    (full_name, email, course, level, student_id)
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


def assign_student_to_course():
    st.subheader("Assign Student to Course")

    matric_no = st.text_input("Enter Student Matric Number")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT course_id, course_code, course_title
            FROM courses
            ORDER BY course_id
        """)

        courses = cursor.fetchall()

        if not courses:
            st.warning("No courses found.")
            return

        course_map = {
            f"{c[0]} - {c[1]} ({c[2]})": c[0]
            for c in courses
        }

        selected_course = st.selectbox(
            "Select Course",
            list(course_map.keys())
        )

        course_id = course_map[selected_course]

        if st.button("Assign Course"):

            cursor.execute(
                """
                SELECT student_id
                FROM students
                WHERE matric_no = %s
                """,
                (matric_no,)
            )

            student = cursor.fetchone()

            if student is None:
                st.error("Student not found.")
                return

            student_id = student[0]

            cursor.execute(
                """
                INSERT INTO student_enrolled
                (student_id, course_id)
                VALUES (%s, %s)
                """,
                (student_id, course_id)
            )

            conn.commit()

            st.success(
                f"Student assigned to {selected_course} successfully."
            )

    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        st.warning(
            "This student is already assigned to this course."
        )

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
            "Assign Course",
            "View Student Courses"
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

    elif menu == "Assign Course":
        assign_student_to_course()
    
    elif menu == "View Student Courses":
        view_student_courses()