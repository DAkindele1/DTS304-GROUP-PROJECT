import psycopg2
import streamlit as st

def get_connection():
    try:
        return psycopg2.connect(
            dbname="sibas_db",
            user="postgres",
            password="incorrect6307",
            host="localhost",
            port="5433"
        )
    except Exception as e:
        st.error(f"Database Connection Failure: {e}")
        return None
