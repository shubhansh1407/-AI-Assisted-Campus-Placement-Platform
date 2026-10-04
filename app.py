import streamlit as st
import pandas as pd
from database.database import get_students, get_company_roles, get_placements
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Campus Placement Platform", page_icon="🎓", layout="wide")
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
