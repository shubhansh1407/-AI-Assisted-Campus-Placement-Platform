import streamlit as st
import pandas as pd
from database.database import get_students, get_company_roles
from utils.gemini_helper import generate_ai_response

st.title("🤖 AI Career Assistant")
st.markdown("Ask the AI Assistant for career advice or compare roles. *Disclaimer: AI recommendations are guidance, not guaranteed placement outcomes.*")

tab1, tab2 = st.tabs(["Q&A Assistant", "Role Comparison"])

with tab1:
    st.subheader("Ask a Career Question")
    
    students_data = get_students()
    if students_data:
        student_names = [s['name'] for s in students_data]
        selected_student = st.selectbox("Select your profile (optional context for AI):", ["(None - General Question)"] + student_names)
    else:
        selected_student = "(None - General Question)"
        
    question = st.text_input("What is your question? (e.g., 'How can I improve my technical profile?')")
    
    if st.button("Ask AI"):
        if not question.strip():
            st.error("Please enter a question.")
        else:
            profile_context = ""
            if selected_student != "(None - General Question)":
                df_s = pd.DataFrame(students_data)
                student_info = df_s[df_s['name'] == selected_student].iloc[0]
                profile_context = f"""
                The student asking this question has the following profile:
                - Branch: {student_info.get('branch', 'N/A')}
                - CGPA: {student_info.get('cgpa', 'N/A')}
                - Current Skills: {student_info.get('skills', 'N/A')}
                - Projects: {student_info.get('projects', 'N/A')}
                """
                
            prompt = f"""
            You are a helpful AI Career Assistant for college students.
            {profile_context}
            
            The student asks: "{question}"
            
            Provide a practical, beginner-friendly answer based on their profile. Do not guarantee placements or invent statistics.
            """
            
            with st.spinner("Assistant is thinking..."):
                response = generate_ai_response(prompt)
                st.info(response)

with tab2:
    st.subheader("Compare Career Roles")
    roles_data = get_company_roles()
    
    if not roles_data:
        st.info("No company roles available to compare.")
    else:
        df_roles = pd.DataFrame(roles_data)
        df_roles['company_role'] = df_roles['company_name'] + " - " + df_roles['role']
        role_list = df_roles['company_role'].tolist()
        
        role1 = st.selectbox("Select Role 1:", role_list)
        role2 = st.selectbox("Select Role 2:", role_list, index=min(1, len(role_list)-1))
        
        if st.button("Compare Roles"):
            if role1 == role2:
                st.warning("Please select two different roles.")
            else:
                r1_data = df_roles[df_roles['company_role'] == role1].iloc[0]
                r2_data = df_roles[df_roles['company_role'] == role2].iloc[0]
                
                prompt = f"""
                Compare these two career roles factually:
                
                Role 1: {role1}
                - Required Skills: {r1_data['required_skills']}
                - Minimum CGPA: {r1_data['minimum_cgpa']}
                
                Role 2: {role2}
                - Required Skills: {r2_data['required_skills']}
                - Minimum CGPA: {r2_data['minimum_cgpa']}
                
                Explain the difference between the roles, important skills for each, and the general learning direction for a student considering either. Do not create numerical compatibility scores or invent placement odds.
                """
                with st.spinner("Analyzing roles..."):
                    response = generate_ai_response(prompt)
                    st.write(response)
