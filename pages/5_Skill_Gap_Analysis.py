import streamlit as st
import pandas as pd
from database.database import get_students, get_company_roles

st.title("Skill-Gap Analysis")
st.markdown("Compare a student's current skills against the required skills for a target role.")

students_data = get_students()
roles_data = get_company_roles()

if not students_data or not roles_data:
    st.warning("Please ensure there is at least one student and one company role in the database.")
else:
    df_students = pd.DataFrame(students_data)
    df_roles = pd.DataFrame(roles_data)
    
    col1, col2 = st.columns(2)
    with col1:
        student_names = df_students['name'].tolist()
        selected_student = st.selectbox("Select Student", student_names)
    
    with col2:
        df_roles['company_role'] = df_roles['company_name'] + " - " + df_roles['role']
        company_role_list = df_roles['company_role'].tolist()
        selected_target = st.selectbox("Select Target Company & Role", company_role_list)
        
    if st.button("Analyze Skill Gap"):
        st.divider()
        
        student_row = df_students[df_students['name'] == selected_student].iloc[0]
        student_skills_str = student_row['skills'] if pd.notnull(student_row['skills']) else ""
        student_skills = set([s.strip() for s in student_skills_str.split(',') if s.strip()])
        
        role_row = df_roles[df_roles['company_role'] == selected_target].iloc[0]
        required_skills_str = role_row['required_skills'] if pd.notnull(role_row['required_skills']) else ""
        required_skills = set([s.strip() for s in required_skills_str.split(',') if s.strip()])
        
        already_have = student_skills.intersection(required_skills)
        skill_gap = required_skills.difference(student_skills)
        
        st.session_state['gap_analysis'] = {
            'target': selected_target,
            'already_have': already_have,
            'skill_gap': skill_gap
        }

if 'gap_analysis' in st.session_state:
    gap_data = st.session_state['gap_analysis']
    
    st.subheader("Skill-Gap Summary")
    st.markdown(f"**Target:** {gap_data['target']}")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.success("#### Skills already available")
        if gap_data['already_have']:
            for skill in sorted(gap_data['already_have']):
                st.write(f"- {skill}")
        else:
            st.write("*None*")
            
    with c2:
        st.error("#### Skills to develop (Gap)")
        if gap_data['skill_gap']:
            for skill in sorted(gap_data['skill_gap']):
                st.write(f"- {skill}")
        else:
            st.write("*None! You have all required skills.*")
            
    st.divider()
    
    st.subheader("🤖 AI Career Explanation")
    if st.button("Get AI Recommendations for this Gap"):
        with st.spinner("AI is analyzing your skill gap..."):
            prompt = f"""
            A student wants to apply for a '{gap_data['target']}' role.
            They already have these skills: {", ".join(gap_data['already_have']) if gap_data['already_have'] else 'None'}
            They are missing these required skills: {", ".join(gap_data['skill_gap']) if gap_data['skill_gap'] else 'None'}
            
            Explain briefly:
            1. Why the missing skills matter for this specific role.
            2. Which missing skill they should learn first and why.
            3. A very short learning roadmap.
            4. One or two project ideas to practice the missing skills.
            
            Do not invent placement statistics. Give practical, beginner-friendly advice.
            """
            from utils.gemini_helper import generate_ai_response
            ai_response = generate_ai_response(prompt)
            st.write(ai_response)
