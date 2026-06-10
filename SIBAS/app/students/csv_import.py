import streamlit as st
import pandas as pd
import psycopg2
import re
from db.connection import get_connection


def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, str(email)) is not None


def validate_student_csv(df):
    required_columns = [
        "user_id",
        "matric_no",
        "full_name",
        "email",
        "department_id",
        "course",
        "level"
    ]

    errors = []

    if list(df.columns) != required_columns:
        errors.append(
            "CSV must have these columns: user_id, matric_no, full_name, email, department_id, course, level"
        )
        return errors

    allowed_levels = ["100", "200", "300", "400", "500"]

    for index, row in df.iterrows():
        row_number = index + 2

        if row.isnull().any():
            errors.append(f"Row {row_number}: Empty fields are not allowed.")

        if not is_valid_email(row["email"]):
            errors.append(f"Row {row_number}: Invalid email address.")

        if str(row["level"]) not in allowed_levels:
            errors.append(f"Row {row_number}: Level must be 100, 200, 300, 400, or 500.")

    duplicated_matric = df[df["matric_no"].duplicated()]["matric_no"].tolist()

    if duplicated_matric:
        errors.append(f"Duplicate matric numbers found in CSV: {duplicated_matric}")

    duplicated_email = df[df["email"].duplicated()]["email"].tolist()

    if duplicated_email:
        errors.append(f"Duplicate emails found in CSV: {duplicated_email}")

    return errors


def bulk_upload_students():
    st.subheader("Bulk Upload Students")

    st.warning("The uploaded CSV file should have the following colunms only: user_id, matric_no, full_name, email, department_id, course, level")

    uploaded_file = st.file_uploader("Upload Students CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        validation_errors = validate_student_csv(df)

        if validation_errors:
            st.error("CSV validation failed.")
            for error in validation_errors:
                st.write(f"- {error}")
            return

        st.success("CSV validation passed.")
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
                        (user_id, matric_no, full_name, email, department_id, course, level)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            int(row["user_id"]),
                            row["matric_no"],
                            row["full_name"],
                            row["email"],
                            int(row["department_id"]),
                            row["course"],
                            str(row["level"])
                        )
                    )

                conn.commit()
                st.success("Students uploaded successfully.")

            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                st.error("Upload failed. One or more students already exist in the database.")

            except Exception as e:
                conn.rollback()
                st.error(f"Upload failed: {e}")

            finally:
                cursor.close()
                conn.close()