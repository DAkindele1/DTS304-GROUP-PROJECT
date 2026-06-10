import streamlit as st
import pandas as pd
from db.connection import get_connection


VALID_STATUS = [
    "Present",
    "Absent"
]


def upload_attendance_csv(session_id):

    st.subheader("Attendance Upload")

    st.info("The uploaded CSV file should have the following colunms only: matric_no and status (Present or Absent)")

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file is None:
        return

    try:

        df = pd.read_csv(uploaded_file)

        expected_columns = [
            "matric_no",
            "status"
        ]

        if list(df.columns) != expected_columns:

            st.error(
                "CSV columns must be: matric_no,status"
            )

            return

        invalid_rows = df[
            ~df["status"].isin(VALID_STATUS)
        ]

        if not invalid_rows.empty:

            st.error(
                "Only Present or Absent are allowed."
            )

            st.dataframe(invalid_rows)

            return

        conn = get_connection()
        cur = conn.cursor()

        uploaded_count = 0

        for _, row in df.iterrows():

            cur.execute("""
                SELECT student_id
                FROM students
                WHERE matric_no = %s
            """,
            (row["matric_no"],)
            )

            student = cur.fetchone()

            if not student:
                continue

            student_id = student[0]

            cur.execute("""
                INSERT INTO attendance_records
                (
                    session_id,
                    student_id,
                    status
                )
                VALUES (%s,%s,%s)
                ON CONFLICT
                (
                    session_id,
                    student_id
                )
                DO UPDATE
                SET status = EXCLUDED.status
            """,
            (
                session_id,
                student_id,
                row["status"]
            ))

            uploaded_count += 1

        conn.commit()

        cur.close()
        conn.close()

        st.success(
            f"{uploaded_count} records uploaded."
        )

    except Exception as e:
        st.error(str(e))