STANDARDIZED_SKILLS = [
    "Python", "Java", "C++", "SQL", "Pandas", "NumPy",
    "Machine Learning", "Excel", "Power BI", "Statistics",
    "HTML", "CSS", "JavaScript", "React", "Git", "Communication"
]

def apply_student_sidebar_hiding():
    import streamlit as st
    if st.session_state.get('role') == 'student':
        st.markdown(
            """
            <style>
                [data-testid="stSidebarNavItems"] li:has(a[href*="Placement_Management"]) {
                    display: none !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
