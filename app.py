import streamlit as st
import pandas as pd
from database.database import get_students, get_company_roles, get_placements, verify_user, insert_user
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Campus Placement Platform", page_icon="🎓", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.session_state['username'] = None

if not st.session_state['logged_in']:
    st.title("🎓 Login Gateway")
    
    tab1, tab2, tab3 = st.tabs(["Student Login", "Student Signup", "Admin Login"])
    
    with tab1:
        st.subheader("Student Login")
        s_username = st.text_input("Username", key="s_log_user")
        s_password = st.text_input("Password", type="password", key="s_log_pass")
        if st.button("Login as Student"):
            role = verify_user(s_username, s_password)
            if role == "student":
                st.session_state['logged_in'] = True
                st.session_state['role'] = "student"
                st.session_state['username'] = s_username
                st.rerun()
            else:
                st.error("Invalid student credentials")
                
    with tab2:
        st.subheader("Student Signup")
        new_username = st.text_input("New Username", key="s_sign_user")
        new_password = st.text_input("New Password", type="password", key="s_sign_pass")
        if st.button("Signup as Student"):
            if new_username and new_password:
                if insert_user(new_username, new_password, "student"):
                    st.success("Signup successful! Please login.")
                else:
                    st.error("Username already exists!")
            else:
                st.error("Please fill all fields.")
                
    with tab3:
        st.subheader("Admin Login")
        a_username = st.text_input("Admin Username", key="a_log_user")
        a_password = st.text_input("Admin Password", type="password", key="a_log_pass")
        if st.button("Login as Admin"):
            if a_username == "admin" and a_password == "admin123":
                st.session_state['logged_in'] = True
                st.session_state['role'] = "admin"
                st.session_state['username'] = "admin"
                st.rerun()
            else:
                st.error("Invalid admin credentials")
                
    # Hide the sidebar for logged out users
    st.markdown(
        """
        <style>
            [data-testid="collapsedControl"] {
                display: none;
            }
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# IF LOGGED IN
st.sidebar.markdown(f"**Logged in as: {st.session_state['username']} ({st.session_state['role'].capitalize()})**")
if st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.session_state['username'] = None
    st.rerun()

from utils.helpers import apply_student_sidebar_hiding
apply_student_sidebar_hiding()

st.title("🎓 AI-Assisted Campus Placement Platform")

st.markdown("""
Welcome to the **AI-Assisted Campus Placement Analytics and Skill-Gap Recommendation Platform**.

This platform combines factual data management, strict analytical reporting, and powerful AI guidance to help students achieve their career goals.
""")

st.subheader("System Workflow")
st.markdown("`Data Collection` → `Data Quality & Analytics` → `Rule-Based Skill Gap` → `AI Explanations & Guidance`")

st.divider()

st.subheader("Platform Overview")

try:
    students_data = get_students()
    roles_data = get_company_roles()
    placements_data = get_placements()
except Exception as e:
    st.error(f"Database error: {str(e)}. Have you run 'python populate_db.py'?")
    st.stop()

total_students = len(students_data) if students_data else 0
total_roles = len(roles_data) if roles_data else 0
total_placements = len(placements_data) if placements_data else 0

avg_package = 0.0
if placements_data:
    df_place = pd.DataFrame(placements_data)
    df_place['package_num'] = pd.to_numeric(df_place['package'].astype(str).str.extract(r'(\d+\.?\d*)', expand=True)[0], errors='coerce')
    valid = df_place.dropna(subset=['package_num'])
    if not valid.empty:
        avg_package = valid['package_num'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", total_students)
col2.metric("Total Company Roles", total_roles)
col3.metric("Placement Records", total_placements)
col4.metric("Avg Package (LPA)", f"{avg_package:.2f}")

st.info("👈 Use the sidebar to navigate to specific modules!")
