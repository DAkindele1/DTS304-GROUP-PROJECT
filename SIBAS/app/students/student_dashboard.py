import streamlit as st
import pandas as pd
from db.connection import get_connection


DEFAULT_ATTENDANCE_THRESHOLD = 80


def student_dashboard(student_id):
    st.title("Student Dashboard")

    conn = get_connection()

    try:
        profile_query = """
            SELECT 
                matric_no,
                full_name,
                email,
                course,
                level
            FROM students
            WHERE student_id = %s
        """

        attendance_query = """
            SELECT
                c.course_code,
                c.course_title,
                COUNT(ar.attendance_id) AS total_sessions,
                SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END) AS sessions_present,
                ROUND(
                    (
                        SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END)::numeric
                        / NULLIF(COUNT(ar.attendance_id), 0)
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

        if profile_df.empty:
            st.warning("Profile not found.")
        else:
            st.dataframe(profile_df)

        st.subheader("My Attendance Records")

        if attendance_df.empty:
            st.info("No attendance records found.")
        else:
            attendance_df["eligibility_status"] = attendance_df["attendance_score"].apply(
                lambda score: "ELIGIBLE" if score >= DEFAULT_ATTENDANCE_THRESHOLD else "INELIGIBLE"
            )

            st.dataframe(attendance_df)

            st.subheader("Attendance Summary")

            for _, row in attendance_df.iterrows():
                course_code = row["course_code"]
                score = row["attendance_score"]
                status = row["eligibility_status"]

                if status == "ELIGIBLE":
                    st.success(f"{course_code}: {score}% - {status}")
                else:
                    st.error(f"{course_code}: {score}% - {status}")

    except Exception as e:
        st.error(f"Error loading student dashboard: {e}")

    finally:
        conn.close()