import streamlit as st
import pandas as pd
from app.db.connection import get_connection


def student_dashboard(student_id):
    st.title("Student Dashboard")

    conn = get_connection()

    try:
        profile_query = """
            SELECT 
                matric_no,
                full_name,
                email,
                programme,
                level
            FROM students
            WHERE student_id = %s
        """

        attendance_query = """
            SELECT
                c.course_code,
                c.course_title,
                COUNT(ar.attendance_record_id) AS total_sessions,
                SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END) AS sessions_present,
                ROUND(
                    (
                        SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END)::numeric
                        / NULLIF(COUNT(ar.attendance_record_id), 0)
                    ) * 100, 2
                ) AS attendance_score
            FROM attendance_records ar
            JOIN attendance_sessions ats
                ON ar.session_id = ats.session_id
            JOIN courses c
                ON ats.course_id = c.course_id
            WHERE ar.student_id = %s
            GROUP BY c.course_code, c.course_title
        """

        profile_df = pd.read_sql(profile_query, conn, params=(student_id,))
        attendance_df = pd.read_sql(attendance_query, conn, params=(student_id,))

        st.subheader("My Profile")
        st.dataframe(profile_df)

        st.subheader("My Attendance Records")
        st.dataframe(attendance_df)

    except Exception as e:
        st.error(f"Error loading student dashboard: {e}")

    finally:
        conn.close()