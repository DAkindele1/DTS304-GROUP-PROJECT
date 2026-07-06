import streamlit as st
from auth.authentication import hash_password

def fetch_available_roles(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT role_id, role_name FROM roles;")
    roles = cursor.fetchall()
    cursor.close()
    return roles

def render_user_management(get_connection_func):
    if st.session_state.get('role') != 'Administrator':
        st.error("Unauthorized Action: Access to this console is strictly restricted to Administrators.")
        return

    st.title("SIBAS Administration Console")
    st.write("Perform administrative operations on user accounts safely.")

    tab_create, tab_update, tab_delete = st.tabs([
        "Create User Account", 
        "Modify / Toggle Account", 
        "Terminate Record Data"
    ])

    with tab_create:
        st.subheader("Register System User Profile")

        conn = get_connection_func()
        roles_data = []
        if conn:
            try:
                roles_data = fetch_available_roles(conn)
            finally:
                conn.close()
            
        role_mapping = {r[1]: r[0] for r in roles_data}

        selected_role = st.selectbox(
            "Assign Authorization Role",
            list(role_mapping.keys())
        )

        with st.form("create_account_form"):
            new_username = st.text_input("Target Unique Username")
            new_password = st.text_input("Initial Access Password", type="password")

            full_name = ""
            email = None
            department_id = None

            if selected_role == "Lecturer":

                full_name = st.text_input("Full Name")
                email = st.text_input("Email")

                departments = {
                    "1 - Computer Science": 1,
                    "2 - Fashion Design & Technology": 2,
                    "3 - Creative Arts": 3,
                    "4 - Environmental Science": 4,
                    "5 - Philosophy & Magic Studies": 5
                }

                selected_department = st.selectbox(
                    "Department",
                    list(departments.keys())
                )

                department_id = departments[selected_department]

            elif selected_role == "Administrator":
                full_name = st.text_input("Full Name")

            submit_creation = st.form_submit_button("Commit User Creation")
            
            if submit_creation:
                if not new_username.strip() or not new_password.strip():
                    st.error(
                        "Processing Error: Input configurations cannot contain empty entries."
                    )

                elif selected_role == "Lecturer" and (
                    not full_name.strip()
                    or not email.strip()
                ):
                    st.error(
                        "Full Name and Email are required for lecturers."
                    )

                elif selected_role == "Administrator" and not full_name.strip():
                    st.error(
                        "Full Name is required for administrators."
                    )
                else:
                    conn = get_connection_func()
                    if conn:
                        try:
                            cursor = conn.cursor()
                            cursor.execute("SELECT username FROM users WHERE username = %s", (new_username.strip(),))
                            if cursor.fetchone():
                                st.error(f"Conflict Error: The user handle '{new_username}' is already claimed.")
                            else:
                                encrypted_hash = hash_password(new_password)
                                target_role_id = role_mapping[selected_role]
                                
                                cursor.execute(
                                    """
                                    INSERT INTO users
                                    (
                                        username,
                                        password,
                                        role_id,
                                        is_active
                                    )
                                    VALUES (%s, %s, %s, TRUE)
                                    RETURNING user_id
                                    """,
                                    (
                                        new_username.strip(),
                                        encrypted_hash,
                                        target_role_id
                                    )
                                )

                                user_id = cursor.fetchone()[0]
                                if selected_role == "Lecturer":
                                    cursor.execute(
                                        """
                                        INSERT INTO lecturers
                                        (
                                            user_id,
                                            full_name,
                                            email,
                                            department_id
                                        )
                                        VALUES (%s, %s, %s, %s)
                                        """,
                                        (
                                            user_id,
                                            full_name.strip(),
                                            email.strip(),
                                            department_id
                                        )
                                    )
                                elif selected_role == "Administrator":
                                    cursor.execute(
                                        """
                                        INSERT INTO administrators
                                        (
                                            user_id,
                                            full_name
                                        )
                                        VALUES (%s, %s)
                                        """,
                                        (
                                            user_id,
                                            full_name.strip()
                                        )
                                    )
                                conn.commit()
                                st.success(f"Success: User profile '{new_username}' created!")
                        except Exception as e:
                            conn.rollback()
                            st.error(f"Transaction aborted: An exception occurred at database engine: {e}")
                        finally:
                            cursor.close()
                            conn.close()

    with tab_update:
        st.subheader("Modify Properties and Active Privileges")
        conn = get_connection_func()
        registered_users = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT u.user_id, u.username, r.role_name, u.is_active, u.role_id 
                    FROM users u 
                    JOIN roles r ON u.role_id = r.role_id
                    ORDER BY u.username ASC;
                """)
                registered_users = cursor.fetchall()
            finally:
                cursor.close()
                conn.close()
        
        if registered_users:
            user_select_dict = {f"{u[1]} ({u[2]}) - Status: {'Active' if u[3] else 'Inactive'}": u for u in registered_users}
            selected_user_label = st.selectbox("Choose Target Profile to Adjust", list(user_select_dict.keys()))
            user_record = user_select_dict[selected_user_label]
            
            u_id, u_name, u_role_name, u_status, u_role_id = user_record
            
            with st.form("modify_account_form"):
                updated_username = st.text_input("Adjust Username Value", value=u_name)
                updated_password = st.text_input("Override Password String (Leave blank to preserve state)", type="password")
                
                role_labels = list(role_mapping.keys())
                default_idx = role_labels.index(u_role_name) if u_role_name in role_labels else 0
                updated_role_label = st.selectbox("Recalibrate Authorization Scope", role_labels, index=default_idx)
                
                active_flag = st.checkbox("Toggle Profile Status (Uncheck to Deactivate Account)", value=u_status)
                submit_modification = st.form_submit_button("Push Update Execution")
                
                if submit_modification:
                    conn = get_connection_func()
                    if conn:
                        try:
                            cursor = conn.cursor()
                            target_new_role_id = role_mapping[updated_role_label]
                            
                            if updated_password.strip():
                                rehashed_pw = hash_password(updated_password)
                                update_query = """
                                    UPDATE users 
                                    SET username = %s, password = %s, role_id = %s, is_active = %s 
                                    WHERE user_id = %s;
                                """
                                cursor.execute(update_query, (updated_username.strip(), rehashed_pw, target_new_role_id, active_flag, u_id))
                            else:
                                update_query = """
                                    UPDATE users 
                                    SET username = %s, role_id = %s, is_active = %s 
                                    WHERE user_id = %s;
                                """
                                cursor.execute(update_query, (updated_username.strip(), target_new_role_id, active_flag, u_id))
                                
                            conn.commit()
                            st.success(f"Modification execution compiled for user '{updated_username}'.")
                            st.rerun()
                        except Exception as e:
                            conn.rollback()
                            st.error(f"Update transaction failed: {e}")
                        finally:
                            cursor.close()
                            conn.close()
        else:
            st.info("No system profiles detected in backend storage.")

    with tab_delete:
        st.subheader("Execute Account Deletion")
        st.warning("Warning: Understand that deletion drops the core profile record immediately. This action is irreversible")
        
        if registered_users:
            deletion_mapping = {f"{u[1]} ({u[2]})": u[0] for u in registered_users}
            target_deletion_user = st.selectbox("Choose Profile for Removal", list(deletion_mapping.keys()), key="deletion_select_node")
            target_del_id = deletion_mapping[target_deletion_user]
            
            safety_confirmation = st.checkbox("I acknowledge this administrative operation is absolute and cannot be reversed.")
            submit_deletion = st.button("Purge Profile Permanently", type="primary")
            
            if submit_deletion:
                if not safety_confirmation:
                    st.error("Aborted: You must check the validation box to authorize this deletion sequence.")
                else:
                    conn = get_connection_func()
                    if conn:
                        try:
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM users WHERE user_id = %s;", (target_del_id,))
                            conn.commit()
                            st.success("Target profile purged successfully from data tables.")
                            st.rerun()
                        except Exception as e:
                            conn.rollback()
                            st.error(f"Failed to complete user purge: {e}")
                        finally:
                            cursor.close()
                            conn.close()