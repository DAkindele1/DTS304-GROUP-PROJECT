import psycopg2
import streamlit as st

def get_connection():
    try:
        return psycopg2.connect(
            dbname=st.secrets["DB_NAME"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            host=st.secrets["DB_HOST"],
            port=st.secrets["DB_PORT"]
        )
    except Exception as e:
        st.error(f"Database Connection Failure: {e}")
        return None
