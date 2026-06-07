import streamlit as st
import pandas as pd
import psycopg2
from app.db.connection import get_connection


def bulk_upload_students():
    st.subheader("Bulk Upload Students")

    uploaded_file = st.file_uploader("Upload Students CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        required_columns = [
            "matric_no",
            "full_name",
            "email",
            "department_id",
            "programme",
            "level"
        ]

        if list(df.columns) != required_columns:
            st.error("CSV must have these columns: matric_no, full_name, email, department_id, programme, level")
            return

        st.write("Preview of uploaded file:")
        st.dataframe(df)

        if st.button("Upload Students"):
            conn = get_connection()
            cursor = conn.cursor()

            try:
                for _, row in df.iterrows():
                    cursor.execute(
                        """
                        INSERT INTO students
                        (matric_no, full_name, email, department_id, programme, level)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            row["matric_no"],
                            row["full_name"],
                            row["email"],
                            int(row["department_id"]),
                            row["programme"],
                            str(row["level"])
                        )
                    )

                conn.commit()
                st.success("Students uploaded successfully.")

            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                st.error("Upload failed. One or more students already exist.")

            except Exception as e:
                conn.rollback()
                st.error(f"Upload failed: {e}")

            finally:
                cursor.close()
                conn.close()