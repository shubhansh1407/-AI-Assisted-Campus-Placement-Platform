import streamlit as st
import pandas as pd
from database.database import insert_student, update_student, get_student_by_name, get_students
from utils.helpers import STANDARDIZED_SKILLS
from utils.gemini_helper import extract_resume_data

st.title("Student Profile")

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please login from the main page.")
    st.stop()

username = st.session_state['username']

from utils.helpers import apply_student_sidebar_hiding
apply_student_sidebar_hiding()

tab1, tab2 = st.tabs(["Manual Entry", "Resume/CV Upload (AI)"])

def save_profile(name, full_name, branch, cgpa, skills, projects, certifications):
    if not name.strip():
        return False, "Username cannot be empty."
    if not full_name.strip():
        return False, "Full Name cannot be empty."
    
    skills_str = ", ".join(skills) if isinstance(skills, list) else skills
    cgpa_val = float(cgpa) if cgpa else 0.0
    
    existing = get_student_by_name(name.strip())
    if existing:
        update_student(name.strip(), full_name.strip(), branch, cgpa_val, skills_str, projects, certifications)
        return True, f"Profile updated successfully for {name.strip()}!"
    else:
        insert_student(name.strip(), full_name.strip(), branch, cgpa_val, skills_str, projects, certifications)
        return True, f"Profile created successfully for {name.strip()}!"

with tab1:
    st.markdown("Enter your details to create or update your profile manually.")
    with st.form("manual_profile_form"):
        st.write(f"Editing profile for: {username}")
        name = username
        
        # Load existing data if profile exists
        existing = get_student_by_name(username)
        def_full_name = existing['full_name'] if existing and 'full_name' in existing.keys() and existing['full_name'] else ""
        def_branch = existing['branch'] if existing else ""
        def_cgpa = existing['cgpa'] if existing else 0.0
        def_skills = existing['skills'].split(', ') if existing and existing['skills'] else []
        def_projects = existing['projects'] if existing else ""
        def_cert = existing['certifications'] if existing else ""

        full_name = st.text_input("Full Name", value=def_full_name)
        branch = st.text_input("Branch", value=def_branch)
        cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, step=0.1, value=def_cgpa)
        
        # Ensure only standardized skills are selected to avoid errors
        safe_skills = [s for s in def_skills if s in STANDARDIZED_SKILLS]
        skills = st.multiselect("Skills", options=STANDARDIZED_SKILLS, default=safe_skills)
        
        projects = st.text_area("Projects (Brief descriptions)", value=def_projects)
        certifications = st.text_area("Certifications (Comma separated)", value=def_cert)
        
        if st.form_submit_button("Save Profile"):
            success, msg = save_profile(name, full_name, branch, cgpa, skills, projects, certifications)
            if success: st.success(msg)
            else: st.error(msg)

with tab2:
    st.markdown("Upload your PDF Resume to automatically extract your profile information using AI. You will be able to review and edit it before saving.")
    
    uploaded_file = st.file_uploader("Upload PDF Resume", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Extract Data from Resume"):
            with st.spinner("Extracting text from PDF and asking AI to analyze..."):
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(uploaded_file)
                    resume_text = ""
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            resume_text += page_text
                            
                    if not resume_text.strip():
                        st.error("Could not extract any text from the PDF.")
                    else:
                        extracted_data, err = extract_resume_data(resume_text, STANDARDIZED_SKILLS)
                        if err:
                            st.error(err)
                        else:
                            st.session_state['extracted_resume'] = extracted_data
                            st.success("Extraction complete! Please review below.")
                except Exception as e:
                    st.error(f"Failed to process PDF: {str(e)}")
                    
    if 'extracted_resume' in st.session_state:
        data = st.session_state['extracted_resume']
        st.subheader("Review & Edit Extracted Profile")
        
        with st.form("extracted_profile_form"):
            st.write(f"Editing profile for: {username}")
            name_val = username
            full_name_val = st.text_input("Full Name", value=data.get('name', ''))
            branch_val = st.text_input("Branch", value=data.get('branch', ''))
            
            try:
                cgpa_val = float(data.get('cgpa', 0.0))
            except:
                cgpa_val = 0.0
                
            cgpa_input = st.number_input("CGPA", min_value=0.0, max_value=10.0, step=0.1, value=min(10.0, max(0.0, cgpa_val)))
            
            ext_skills = data.get('skills', [])
            if not isinstance(ext_skills, list):
                ext_skills = [ext_skills]
                
            matched_skills = [s for s in ext_skills if s in STANDARDIZED_SKILLS]
            unmatched = [s for s in ext_skills if str(s).strip() and s not in STANDARDIZED_SKILLS]
            
            skills_input = st.multiselect("Standardized Skills", options=STANDARDIZED_SKILLS, default=matched_skills)
            
            if unmatched:
                st.warning(f"The following skills were extracted but didn't strictly match the standard list: {', '.join(unmatched)}")
            
            proj_str = data.get('projects', '')
            if isinstance(proj_str, list): proj_str = ", ".join(proj_str)
            projects_input = st.text_area("Projects", value=str(proj_str))
            
            cert_str = data.get('certifications', '')
            if isinstance(cert_str, list): cert_str = ", ".join(cert_str)
            certifications_input = st.text_area("Certifications", value=str(cert_str))
            
            if st.form_submit_button("Confirm & Save Profile"):
                all_skills = skills_input + [str(u) for u in unmatched]
                success, msg = save_profile(name_val, full_name_val, branch_val, cgpa_input, all_skills, projects_input, certifications_input)
                if success: 
                    st.success(msg)
                    del st.session_state['extracted_resume']
                else: 
                    st.error(msg)

st.divider()
st.subheader("Currently Stored Student Records")
if st.session_state['role'] == 'admin':
    students = get_students()
    if students:
        df = pd.DataFrame(students)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No student records found.")
else:
    students = get_students()
    my_profile = [s for s in students if s['name'] == username]
    if my_profile:
        st.dataframe(pd.DataFrame(my_profile), use_container_width=True)
    else:
        st.info("Your profile hasn't been created yet.")
