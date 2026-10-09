STANDARDIZED_SKILLS = [
    "Python", "Java", "C", "C++", "SQL", "Pandas", "NumPy",
    "Machine Learning", "Deep Learning", "TensorFlow", "NLP",
    "Excel", "Power BI", "Tableau", "Statistics",
    "HTML", "CSS", "JavaScript", "React", "Node.js", "Express", "Django", "Spring Boot",
    "Git", "Docker", "Kubernetes", "AWS",
    "Go", "MongoDB", "Data Structures", "Algorithms", "OOP",
    "AutoCAD", "SolidWorks", "MATLAB", "Microcontrollers", "PLC", "SCADA", "VHDL", "Verilog", "Robotics",
    "Communication"
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
