import streamlit as st
from db.connection import get_connection
from attendance.attendance_upload import upload_attendance_csv


def get_lecturer_id(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT lecturer_id
        FROM lecturers
        WHERE user_id = %s
    """, (user_id,))

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result[0] if result else None


def create_attendance_session():

    st.subheader("Create Attendance Session")

    lecturer_id = get_lecturer_id(
        st.session_state["user_id"]
    )

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.course_id,
               c.course_code,
               c.course_title
        FROM courses c
        JOIN lecturer_teaches lt
            ON c.course_id = lt.course_id
        WHERE lt.lecturer_id = %s
    """, (lecturer_id,))

    courses = cur.fetchall()

    cur.close()
    conn.close()

    if not courses:
        st.warning("No assigned courses found.")
        return

    course_map = {
        f"{c[1]} - {c[2]}": c[0]
        for c in courses
    }

    selected_course = st.selectbox(
        "Select Course",
        list(course_map.keys())
    )

    session_date = st.date_input(
        "Session Date"
    )

    session_time = st.time_input(
        "Session Time"
    )

    if st.button("Create Session"):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO attendance_sessions
            (
                course_id,
                lecturer_id,
                session_date,
                session_time
            )
            VALUES (%s,%s,%s,%s)
        """,
        (
            course_map[selected_course],
            lecturer_id,
            session_date,
            session_time
        ))

        conn.commit()

        cur.close()
        conn.close()

        st.success("Attendance session created.")


def attendance_correction():

    st.subheader("Attendance Correction")

    session_id = st.number_input(
        "Session ID",
        min_value=1
    )

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            ar.attendance_id,
            s.matric_no,
            s.full_name,
            ar.status
        FROM attendance_records ar
        JOIN students s
            ON ar.student_id = s.student_id
        WHERE ar.session_id = %s
    """, (session_id,))

    records = cur.fetchall()

    cur.close()
    conn.close()

    if not records:
        st.info("No records found.")
        return

    student_map = {
        f"{r[1]} - {r[2]}": r
        for r in records
    }

    selected_student = st.selectbox(
        "Student",
        list(student_map.keys())
    )

    attendance_record = student_map[selected_student]

    new_status = st.selectbox(
        "New Status",
        ["Present", "Absent"]
    )

    if st.button("Update Attendance"):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE attendance_records
            SET status = %s
            WHERE attendance_id = %s
        """,
        (
            new_status,
            attendance_record[0]
        ))

        conn.commit()

        cur.close()
        conn.close()

        st.success("Attendance updated successfully.")


def attendance_page():

    st.title("Attendance Management")

    action = st.radio(
        "Select Action",
        [
            "Create Session",
            "Upload Attendance",
            "Correct Attendance"
        ]
    )

    if action == "Create Session":
        create_attendance_session()

    elif action == "Upload Attendance":

        session_id = st.number_input(
            "Session ID",
            min_value=1
        )

        upload_attendance_csv(session_id)

    elif action == "Correct Attendance":
        attendance_correction()