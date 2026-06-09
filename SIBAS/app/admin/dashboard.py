import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render_admin_dashboard(get_connection_func):
    """
    Admin Dashboard - Central control panel for system administrators.
    Displays key metrics, system statistics, and quick actions.
    """
    st.set_page_config(layout="wide")
    st.title("📊 SIBAS Admin Dashboard")
    st.markdown("---")
    
    try:
        conn = get_connection_func()
        if not conn:
            st.error("Failed to connect to database")
            return
        
        cursor = conn.cursor()
        
        # ============================================================
        # KEY METRICS - Row 1
        # ============================================================
        col1, col2, col3, col4 = st.columns(4)
        
        # Total Users
        with col1:
            cursor.execute("SELECT COUNT(*) FROM users;")
            total_users = cursor.fetchone()[0]
            st.metric("👥 Total Users", total_users, delta="Active")
        
        # Total Students
        with col2:
            cursor.execute("SELECT COUNT(*) FROM students;")
            total_students = cursor.fetchone()[0]
            st.metric("🎓 Total Students", total_students)
        
        # Total Lecturers
        with col3:
            cursor.execute("SELECT COUNT(*) FROM lecturers;")
            total_lecturers = cursor.fetchone()[0]
            st.metric("👨‍🏫 Total Lecturers", total_lecturers)
        
        # Total Courses
        with col4:
            cursor.execute("SELECT COUNT(*) FROM courses;")
            total_courses = cursor.fetchone()[0]
            st.metric("📚 Total Courses", total_courses)
        
        st.markdown("---")
        
        # ============================================================
        # SYSTEM OVERVIEW - Row 2
        # ============================================================
        col1, col2 = st.columns(2)
        
        # User Distribution by Role
        with col1:
            st.subheader("👥 User Distribution by Role")
            cursor.execute("""
                SELECT r.role_name, COUNT(u.user_id) as count
                FROM users u
                JOIN roles r ON u.role_id = r.role_id
                GROUP BY r.role_name
                ORDER BY count DESC;
            """)
            role_data = cursor.fetchall()
            
            if role_data:
                df_roles = pd.DataFrame(role_data, columns=['Role', 'Count'])
                st.bar_chart(data=df_roles.set_index('Role'), height=300)
            else:
                st.info("No user data available")
        
        # Student Distribution by Department
        with col2:
            st.subheader("🏢 Students by Department")
            cursor.execute("""
                SELECT d.department_name, COUNT(s.student_id) as count
                FROM students s
                JOIN departments d ON s.department_id = d.department_id
                GROUP BY d.department_name
                ORDER BY count DESC;
            """)
            dept_data = cursor.fetchall()
            
            if dept_data:
                df_dept = pd.DataFrame(dept_data, columns=['Department', 'Count'])
                st.bar_chart(data=df_dept.set_index('Department'), height=300)
            else:
                st.info("No student data available")
        
        st.markdown("---")
        
        # ============================================================
        # ATTENDANCE OVERVIEW - Row 3
        # ============================================================
        st.subheader("📋 Attendance Summary")
        
        cursor.execute("""
            SELECT 
                c.course_code,
                COUNT(DISTINCT ar.session_id) as total_sessions,
                COUNT(DISTINCT ar.student_id) as students_tracked,
                SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END) as total_present,
                ROUND(
                    SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END)::NUMERIC 
                    / COUNT(*) * 100, 2
                ) as attendance_rate
            FROM attendance_records ar
            JOIN attendance_sessions asess ON ar.session_id = asess.session_id
            JOIN courses c ON asess.course_id = c.course_id
            GROUP BY c.course_code
            ORDER BY c.course_code;
        """)
        
        attendance_data = cursor.fetchall()
        if attendance_data:
            df_attendance = pd.DataFrame(
                attendance_data,
                columns=['Course', 'Sessions', 'Students', 'Present', 'Attendance %']
            )
            st.dataframe(df_attendance, use_container_width=True, hide_index=True)
        else:
            st.info("No attendance records available")
        
        st.markdown("---")
        
        # ============================================================
        # RECENT ACTIVITY - Row 4
        # ============================================================
        col1, col2 = st.columns(2)
        
        # Active Lecturers (with courses)
        with col1:
            st.subheader("👨‍🏫 Lecturers & Their Courses")
            cursor.execute("""
                SELECT 
                    l.full_name,
                    COUNT(lt.course_id) as courses_teaching,
                    d.department_name
                FROM lecturers l
                LEFT JOIN lecturer_teaches lt ON l.lecturer_id = lt.lecturer_id
                JOIN departments d ON l.department_id = d.department_id
                GROUP BY l.lecturer_id, l.full_name, d.department_name
                ORDER BY courses_teaching DESC;
            """)
            lecturer_data = cursor.fetchall()
            
            if lecturer_data:
                df_lecturers = pd.DataFrame(
                    lecturer_data,
                    columns=['Lecturer', 'Courses', 'Department']
                )
                st.dataframe(df_lecturers, use_container_width=True, hide_index=True)
            else:
                st.info("No lecturer data available")
        
        # Student Enrollment Stats
        with col2:
            st.subheader("📚 Course Enrollment")
            cursor.execute("""
                SELECT 
                    c.course_code,
                    c.course_title,
                    COUNT(se.student_id) as enrollment_count
                FROM courses c
                LEFT JOIN student_enrolled se ON c.course_id = se.course_id
                GROUP BY c.course_id, c.course_code, c.course_title
                ORDER BY enrollment_count DESC
                LIMIT 10;
            """)
            enrollment_data = cursor.fetchall()
            
            if enrollment_data:
                df_enrollment = pd.DataFrame(
                    enrollment_data,
                    columns=['Course Code', 'Course Title', 'Enrolled']
                )
                st.dataframe(df_enrollment, use_container_width=True, hide_index=True)
            else:
                st.info("No enrollment data available")
        
        st.markdown("---")
        
        # ============================================================
        # SYSTEM STATUS
        # ============================================================
        st.subheader("⚙️ System Status")
        
        col1, col2, col3 = st.columns(3)
        
        # Active Users
        with col1:
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = TRUE;")
            active_users = cursor.fetchone()[0]
            st.metric("✅ Active Users", active_users)
        
        # Inactive Users
        with col2:
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = FALSE;")
            inactive_users = cursor.fetchone()[0]
            st.metric("❌ Inactive Users", inactive_users)
        
        # Last Updated
        with col3:
            st.metric("🕐 Dashboard Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        st.error(f"Error loading admin dashboard: {str(e)}")
        st.info("Make sure PostgreSQL is running and the database is accessible.")
