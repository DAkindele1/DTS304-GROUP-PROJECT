import streamlit as st
import pandas as pd
import psycopg2
import io

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from db.connection import get_connection

def create_attendance_pdf(student_info, attendance_df):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Student Attendance Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"Name: {student_info['full_name']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Matric No: {student_info['matric_no']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Department: {student_info['department_name']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Level: {student_info['level']}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 15))

    table_data = [attendance_df.columns.tolist()]

    for row in attendance_df.values.tolist():
        table_data.append(row)

    table = Table(table_data)

    table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
        ])
    )

    elements.append(table)

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf


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
    conn = get_connection()
    st.subheader("All Registered Students")

    try:
        # =========================
        # Department Filter
        # =========================
        dept_query = """
        SELECT department_id, department_name
        FROM departments
        ORDER BY department_name
        """

        departments = pd.read_sql(dept_query, conn)

        dept_options = ["All"] + departments["department_name"].tolist()

        selected_dept = st.selectbox(
            "Filter by Department",
            dept_options
        )

        # =========================
        # Course Filter
        # =========================
        course_query = """
        SELECT course_id, course_code, course_title
        FROM courses
        ORDER BY course_code
        """

        courses = pd.read_sql(course_query, conn)

        course_options = ["All"] + [
            f"{row.course_code} - {row.course_title}"
            for _, row in courses.iterrows()
        ]

        selected_course = st.selectbox(
            "Filter by Course",
            course_options
        )

        # =========================
        # Student Query
        # =========================
        query = """
        SELECT
            s.student_id,
            s.matric_no,
            s.full_name,
            s.email,
            d.department_name,
            s.level
        FROM students s
        JOIN departments d
            ON s.department_id = d.department_id
        WHERE 1=1
        """

        params = []

        if selected_dept != "All":
            query += " AND d.department_name = %s"
            params.append(selected_dept)

        if selected_course != "All":

            course_code = selected_course.split(" - ")[0]

            query += """
                AND EXISTS (
                    SELECT 1
                    FROM student_enrolled sc
                    JOIN courses c
                        ON sc.course_id = c.course_id
                    WHERE sc.student_id = s.student_id
                    AND c.course_code = %s
                )
            """

            params.append(course_code)

        query += " ORDER BY s.full_name"

        df = pd.read_sql(query, conn, params=params)

        if df.empty:
            st.info("No students found.")
            return

        st.dataframe(df, use_container_width=True)

        # =========================
        # Select Student
        # =========================
        student_names = [
            f"{row['matric_no']} - {row['full_name']}"
            for _, row in df.iterrows()
        ]

        selected_student = st.selectbox(
            "Select Student",
            student_names
        )

        selected_row = df[
            (df["matric_no"] + " - " + df["full_name"])
            == selected_student
        ]

        student_id = int(selected_row.iloc[0]["student_id"])

        st.markdown("### Student Details")

        st.write(
            f"**Name:** {selected_row.iloc[0]['full_name']}"
        )

        st.write(
            f"**Matric No:** {selected_row.iloc[0]['matric_no']}"
        )

        st.write(
            f"**Department:** {selected_row.iloc[0]['department_name']}"
        )

        st.write(
            f"**Level:** {selected_row.iloc[0]['level']}"
        )

        # =========================
        # Attendance Report
        # =========================
        attendance_query = """
        SELECT
            c.course_code,
            c.course_title,

            COUNT(a.attendance_id) AS total_sessions,

            SUM(
                CASE
                    WHEN a.status = 'Present'
                    THEN 1
                    ELSE 0
                END
            ) AS sessions_present,

            ROUND(
                (
                    SUM(
                        CASE
                            WHEN a.status='Present'
                            THEN 1
                            ELSE 0
                        END
                    )::numeric
                    /
                    NULLIF(
                        COUNT(a.attendance_id),
                        0
                    )
                ) * 100,
                2
            ) AS attendance_percentage

        FROM attendance_records a
        JOIN attendance_sessions ats
            ON a.session_id = ats.session_id

        JOIN courses c
            ON ats.course_id = c.course_id

        WHERE a.student_id = %s

        GROUP BY
            c.course_code,
            c.course_title

        ORDER BY c.course_code
        """

        attendance_df = pd.read_sql(
            attendance_query,
            conn,
            params=[student_id]
        )

        if attendance_df.empty:
            st.warning("No attendance records found.")
            return

        attendance_df["Status"] = attendance_df[
            "attendance_percentage"
        ].apply(
            lambda x:
            "Eligible"
            if x >= 80
            else "Ineligible"
        )

        st.subheader("Attendance Report")
        st.dataframe(attendance_df, use_container_width=True)

        # =========================
        # CSV Export
        # =========================
        csv = attendance_df.to_csv(index=False)

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{student_id}_attendance.csv",
            mime="text/csv"
        )
        student_info = {
            "full_name": selected_row.iloc[0]["full_name"],
            "matric_no": selected_row.iloc[0]["matric_no"],
            "department_name": selected_row.iloc[0]["department_name"],
            "level": selected_row.iloc[0]["level"]
        }

        pdf_data = create_attendance_pdf(
            student_info,
            attendance_df
        )

        st.download_button(
            label="Download PDF",
            data=pdf_data,
            file_name=f"{student_info['matric_no']}_attendance_report.pdf",
            mime="application/pdf"
        )
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