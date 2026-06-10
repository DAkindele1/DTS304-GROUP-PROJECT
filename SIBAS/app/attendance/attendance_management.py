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
            RETURNING session_id
        """,
        (
            course_map[selected_course],
            lecturer_id,
            session_date,
            session_time
        ))

        session_id = cur.fetchone()[0]

        conn.commit()

        cur.close()
        conn.close()

        st.success(
            f"Attendance session created successfully. "
            f"Session ID: {session_id}"
        )

def end_attendance_session():

    st.subheader("End Attendance Session")

    lecturer_id = get_lecturer_id(
        st.session_state["user_id"]
    )

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            session_id,
            session_date,
            session_time,
            c.course_code
        FROM attendance_sessions a
        JOIN courses c
            ON a.course_id = c.course_id
        WHERE a.lecturer_id = %s
        AND a.status = 'Open'
        ORDER BY a.session_date DESC
    """, (lecturer_id,))

    sessions = cur.fetchall()

    if not sessions:
        st.info("No open attendance sessions found.")
        cur.close()
        conn.close()
        return

    session_map = {
        f"Session {s[0]} - {s[1]} ({s[2]} at {s[3]})": s[0]
        for s in sessions
    }

    selected_session = st.selectbox(
        "Select Session to End",
        list(session_map.keys())
    )

    if st.button("End Session"):

        cur.execute("""
            UPDATE attendance_sessions
            SET status = 'Closed'
            WHERE session_id = %s
        """, (session_map[selected_session],))

        conn.commit()

        st.success("Attendance session closed successfully.")

    cur.close()
    conn.close()

def attendance_correction():

    st.subheader("Attendance Correction")

    lecturer_id = get_lecturer_id(
        st.session_state["user_id"]
    )

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            a.session_id,
            c.course_code,
            a.session_date,
            a.session_time
        FROM attendance_sessions a
        JOIN courses c
            ON a.course_id = c.course_id
        WHERE a.lecturer_id = %s
        ORDER BY a.session_date DESC,
                a.session_time DESC
    """, (lecturer_id,))

    sessions = cur.fetchall()

    cur.close()
    conn.close()

    if not sessions:
        st.info("No attendance sessions found.")
        return

    session_map = {
        f"Session {s[0]} - {s[1]} ({s[2]} at {s[3]})": s[0]
        for s in sessions
    }

    selected_session = st.selectbox(
        "Select Session",
        list(session_map.keys())
    )

    session_id = session_map[selected_session]
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
            "Correct Attendance",
            "End Session"
        ]
    )

    if action == "Create Session":
        create_attendance_session()

    elif action == "Upload Attendance":

        lecturer_id = get_lecturer_id(
            st.session_state["user_id"]
        )

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                a.session_id,
                c.course_code,
                a.session_date,
                a.session_time
            FROM attendance_sessions a
            JOIN courses c
                ON a.course_id = c.course_id
            WHERE a.lecturer_id = %s
             AND a.status = 'Open'
            ORDER BY a.session_date DESC,
                    a.session_time DESC
        """, (lecturer_id,))

        sessions = cur.fetchall()

        cur.close()
        conn.close()

        if not sessions:
            st.info("No attendance sessions found.")
            return

        session_map = {
            f"Session {s[0]} - {s[1]} ({s[2]} at {s[3]})": s[0]
            for s in sessions
        }

        selected_session = st.selectbox(
            "Select Session",
            list(session_map.keys())
        )

        session_id = session_map[selected_session]

        upload_attendance_csv(session_id)

    elif action == "Correct Attendance":
        attendance_correction()

    elif action == "End Session":
        end_attendance_session()