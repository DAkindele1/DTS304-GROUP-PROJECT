import psycopg2
import streamlit as st


def _connect_with_kwargs(kwargs):
    return psycopg2.connect(**kwargs)


def get_connection():
    try:
        if "DATABASE_URL" in st.secrets:
            return psycopg2.connect(
                st.secrets["DATABASE_URL"],
                sslmode=st.secrets.get("DB_SSLMODE", "require")
            )

        db_host = st.secrets["DB_HOST"]
        db_user = st.secrets["DB_USER"]
        sslmode = st.secrets.get("DB_SSLMODE")
        if not sslmode and db_host not in {"localhost", "127.0.0.1", "::1"}:
            sslmode = "require"

        connect_kwargs = {
            "dbname": st.secrets["DB_NAME"],
            "user": db_user,
            "password": st.secrets["DB_PASSWORD"],
            "host": db_host,
            "port": st.secrets["DB_PORT"],
            "sslmode": sslmode,
        }

        try:
            return _connect_with_kwargs(connect_kwargs)
        except Exception as inner_error:
            # Supabase pooler can reject when tenant ID routing is not resolved.
            # Retry once using the direct host derived from postgres.<project_ref>.
            error_text = str(inner_error)
            is_pooler = db_host.endswith("pooler.supabase.com")
            has_project_user = isinstance(db_user, str) and db_user.startswith("postgres.")
            if "ENOIDENTIFIER" in error_text and is_pooler and has_project_user:
                project_ref = db_user.split(".", 1)[1]
                connect_kwargs["host"] = f"db.{project_ref}.supabase.co"
                connect_kwargs["port"] = "5432"
                connect_kwargs["user"] = "postgres"
                connect_kwargs["sslmode"] = "require"
                return _connect_with_kwargs(connect_kwargs)
            raise inner_error
    except Exception as e:
        st.error(f"Database Connection Failure: {e}")
        return None
