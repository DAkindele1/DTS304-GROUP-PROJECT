import psycopg2
import streamlit as st

def get_connection():
    try:
        if "DATABASE_URL" in st.secrets:
            return psycopg2.connect(
                st.secrets["DATABASE_URL"],
                sslmode=st.secrets.get("DB_SSLMODE", "require")
            )

        db_host = st.secrets["DB_HOST"]
        sslmode = st.secrets.get("DB_SSLMODE")
        if not sslmode and db_host not in {"localhost", "127.0.0.1", "::1"}:
            sslmode = "require"

        return psycopg2.connect(
            dbname=st.secrets["DB_NAME"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            host=db_host,
            port=st.secrets["DB_PORT"],
            sslmode=sslmode
        )
    except Exception as e:
        st.error(f"Database Connection Failure: {e}")
        return None
