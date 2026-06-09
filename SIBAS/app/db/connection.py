import psycopg2
import streamlit as st

def get_connection():
    try:
        return psycopg2.connect(
            dbname="sibas_db",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
    except Exception as e:
        st.error(f"Database Connection Failure: {e}")
        return None
