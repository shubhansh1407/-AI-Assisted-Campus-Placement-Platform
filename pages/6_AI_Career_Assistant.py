import streamlit as st
import pandas as pd
from database.database import get_students, get_company_roles
from utils.gemini_helper import generate_ai_response

st.title("🤖 AI Career Assistant")

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please login from the main page.")
    st.stop()

from utils.helpers import apply_student_sidebar_hiding
apply_student_sidebar_hiding()
st.markdown("Ask the AI Assistant for career advice or compare roles. *Disclaimer: AI recommendations are guidance, not guaranteed placement outcomes.*")

tab1, tab2 = st.tabs(["Q&A Assistant", "Role Comparison"])

with tab1:
    st.subheader("Ask a Career Question")
    
    colA, colB = st.columns([3, 1])
    with colA:
        students_data = get_students()
        if students_data:
            student_names = [s['name'] for s in students_data]
            if st.session_state['role'] == 'admin':
                selected_student = st.selectbox("Profile Context (Optional):", ["(None)"] + student_names)
            else:
                selected_student = st.session_state['username']
                st.info(f"Context: {selected_student}")
        else:
            selected_student = "(None)"
            
    with colB:
        if st.button("🗑️ Clear Chat", key="clear_qa"):
            st.session_state["qa_messages"] = []
            st.rerun()

    if "qa_messages" not in st.session_state:
        st.session_state["qa_messages"] = []
        
    for msg in st.session_state["qa_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if question := st.chat_input("What is your career question?", key="qa_chat"):
        st.session_state["qa_messages"].append({"role": "user", "content": question})
        
        profile_context = ""
        if selected_student != "(None)":
            df_s = pd.DataFrame(students_data)
            s_info = df_s[df_s['name'] == selected_student].iloc[0]
            profile_context = f"Student Profile - Branch: {s_info.get('branch', 'N/A')}, CGPA: {s_info.get('cgpa', 'N/A')}, Skills: {s_info.get('skills', 'N/A')}."
            
        history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state["qa_messages"][:-1]])
        full_prompt = f"You are an AI Career Assistant.\n{profile_context}\n\nHistory:\n{history}\n\nUser: {question}\nAssistant:"
        
        with st.spinner("Assistant is thinking..."):
            response = generate_ai_response(full_prompt)
            
        st.session_state["qa_messages"].append({"role": "assistant", "content": response})
        st.rerun()

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
        
        if "compare_messages" not in st.session_state:
            st.session_state["compare_messages"] = []
            
        if st.button("Compare Roles"):
            if role1 == role2:
                st.warning("Please select two different roles.")
            else:
                r1_data = df_roles[df_roles['company_role'] == role1].iloc[0]
                r2_data = df_roles[df_roles['company_role'] == role2].iloc[0]
                
                prompt = f"""
                Compare these two career roles factually:
                Role 1: {role1} (Skills: {r1_data['required_skills']}, CGPA: {r1_data['minimum_cgpa']})
                Role 2: {role2} (Skills: {r2_data['required_skills']}, CGPA: {r2_data['minimum_cgpa']})
                Explain the difference and learning direction. No numerical scores.
                """
                
                st.session_state["compare_messages"] = [{"role": "user", "content": f"Please compare {role1} and {role2}."}]
                
                with st.spinner("Analyzing roles..."):
                    response = generate_ai_response(prompt)
                st.session_state["compare_messages"].append({"role": "assistant", "content": response})
                st.rerun()
                
        for msg in st.session_state["compare_messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        if st.session_state["compare_messages"]:
            if question := st.chat_input("Ask follow-up about these roles...", key="compare_chat"):
                st.session_state["compare_messages"].append({"role": "user", "content": question})
                
                history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state["compare_messages"][:-1]])
                full_prompt = f"Context: Comparing {role1} and {role2}.\n\nHistory:\n{history}\n\nUser: {question}\nAssistant:"
                
                with st.spinner("Thinking..."):
                    response = generate_ai_response(full_prompt)
                st.session_state["compare_messages"].append({"role": "assistant", "content": response})
                st.rerun()
