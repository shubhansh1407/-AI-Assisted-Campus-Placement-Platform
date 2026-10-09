import streamlit as st
import pandas as pd
import io
from database.database import (
    insert_company_role, insert_placement, get_existing_student_names, 
    get_company_names, get_roles_by_company, get_company_roles, get_placements
)
from utils.helpers import STANDARDIZED_SKILLS

st.title("Placement Management (Admin)")

if 'logged_in' not in st.session_state or st.session_state['role'] != 'admin':
    st.warning("Admin access required.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["Add Company / Role", "Add Placement Record", "CSV Bulk Upload"])

with tab1:
    st.subheader("Add a New Company / Role")
    with st.form("add_role_form"):
        company_name = st.text_input("Company Name (Required)")
        role = st.text_input("Role (Required)")
        minimum_cgpa = st.number_input("Minimum CGPA", min_value=0.0, max_value=10.0, step=0.1)
        required_skills = st.multiselect("Required Skills (Required)", options=STANDARDIZED_SKILLS)
        package = st.number_input("Package (in LPA)", min_value=0.0, step=0.1)
        
        submitted_role = st.form_submit_button("Save Company / Role")
        
        if submitted_role:
            if not company_name.strip():
                st.error("Company name cannot be empty.")
            elif not role.strip():
                st.error("Role cannot be empty.")
            elif not required_skills:
                st.error("At least one required skill must be selected.")
            elif package <= 0:
                st.error("Package must be a positive number.")
            else:
                req_skills_str = ", ".join(required_skills)
                package_str = f"{package} LPA"
                insert_company_role(company_name.strip(), role.strip(), minimum_cgpa, req_skills_str, package_str)
                st.success(f"Successfully added {role.strip()} at {company_name.strip()}!")
                
    st.divider()
    st.subheader("Existing Company Roles")
    roles_data = get_company_roles()
    if roles_data:
        st.dataframe(pd.DataFrame(roles_data), use_container_width=True)
    else:
        st.info("No company roles found.")

with tab2:
    st.subheader("Add a Placement Record")
    
    from database.database import get_students
    students_data = get_students()
    student_display_options = []
    display_to_username = {}
    if students_data:
        for s in students_data:
            disp = f"{s['full_name']} ({s['name']})" if s.get('full_name') and str(s.get('full_name')).strip() else s['name']
            student_display_options.append(disp)
            display_to_username[disp] = s['name']
            
    company_names = get_company_names()
    
    with st.form("add_placement_form"):
        selected_student_disp = st.selectbox("Student Name", options=[""] + student_display_options) if student_display_options else st.text_input("Student Name (Enter manually)")
        selected_company = st.selectbox("Company Name", options=[""] + company_names) if company_names else st.text_input("Company Name (Enter manually)")
        role_p = st.text_input("Role")
        
        package_p = st.number_input("Package (in LPA, positive)", min_value=0.0, step=0.1)
        year_p = st.number_input("Year", min_value=2000, max_value=2100, value=2024, step=1)
        
        submitted_placement = st.form_submit_button("Save Placement Record")
        
        if submitted_placement:
            selected_student = display_to_username.get(selected_student_disp, selected_student_disp)
            if not selected_student or not selected_student.strip():
                st.error("Student Name cannot be empty.")
            elif not selected_company or not selected_company.strip():
                st.error("Company Name cannot be empty.")
            elif not role_p.strip():
                st.error("Role cannot be empty.")
            elif package_p <= 0:
                st.error("Package must be positive.")
            else:
                package_p_str = f"{package_p} LPA"
                insert_placement(selected_student.strip(), selected_company.strip(), role_p.strip(), package_p_str, year_p)
                st.success(f"Placement record saved for {selected_student.strip()} at {selected_company.strip()}!")
                
    st.divider()
    st.subheader("Existing Placements")
    placements_data = get_placements()
    if placements_data:
        df_p = pd.DataFrame(placements_data)
        if students_data:
            df_s = pd.DataFrame(students_data)
            df_p = pd.merge(df_p, df_s[['name', 'full_name']], left_on='student_name', right_on='name', how='left')
            df_p['student_name'] = df_p.apply(lambda r: f"{r['full_name']} ({r['student_name']})" if pd.notnull(r.get('full_name')) and str(r.get('full_name')).strip() else r['student_name'], axis=1)
            df_p.drop(columns=['name', 'full_name'], inplace=True, errors='ignore')
        st.dataframe(df_p, use_container_width=True)
    else:
        st.info("No placement records found.")

with tab3:
    st.subheader("CSV Bulk Upload (Company Roles)")
    st.markdown("Upload a CSV file containing company roles. Expected columns: `Company,Role,Min_CGPA,Required_Skills,Package`")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("### Uploaded Data Preview")
            st.dataframe(df.head())
            
            required_cols = ['Company', 'Role', 'Min_CGPA', 'Required_Skills', 'Package']
            if not all(col in df.columns for col in required_cols):
                st.error(f"CSV must contain exactly these columns: {', '.join(required_cols)}")
            else:
                # Clean formatting
                df['Company'] = df['Company'].astype(str).str.strip()
                df['Role'] = df['Role'].astype(str).str.strip()
                df['Required_Skills'] = df['Required_Skills'].astype(str).str.strip()
                
                total_rows = len(df)
                
                # Missing values check
                missing_mask = df[required_cols].isnull().any(axis=1) | (df['Company'] == '') | (df['Role'] == '') | (df['Company'] == 'nan') | (df['Role'] == 'nan')
                
                # Invalid numeric check (Min_CGPA)
                df['Min_CGPA'] = pd.to_numeric(df['Min_CGPA'], errors='coerce')
                invalid_cgpa_mask = (df['Min_CGPA'].isnull()) | (df['Min_CGPA'] < 0) | (df['Min_CGPA'] > 10)
                
                # Invalid package check (strip text and check if positive)
                df['Package_Numeric'] = pd.to_numeric(df['Package'].astype(str).str.extract(r'(\d+\.?\d*)')[0], errors='coerce')
                invalid_package_mask = (df['Package_Numeric'].isnull()) | (df['Package_Numeric'] <= 0)
                
                # Duplicates
                duplicate_mask = df.duplicated(subset=['Company', 'Role'], keep=False)
                
                # Total invalid
                invalid_rows_mask = missing_mask | invalid_cgpa_mask | invalid_package_mask
                
                valid_df = df[~invalid_rows_mask].drop_duplicates(subset=['Company', 'Role'])
                invalid_df = df[invalid_rows_mask]
                duplicates_df = df[duplicate_mask]
                
                st.write("### Validation Summary")
                st.write(f"- **Total rows:** {total_rows}")
                st.write(f"- **Valid rows:** {len(valid_df)}")
                st.write(f"- **Invalid rows:** {len(invalid_df)}")
                st.write(f"- **Duplicate rows:** {len(duplicates_df)}")
                
                if len(invalid_df) > 0:
                    st.warning("Invalid rows (Skipped):")
                    st.dataframe(invalid_df)
                    
                if len(duplicates_df) > 0:
                    st.warning("Duplicate roles detected:")
                    st.dataframe(duplicates_df)
                
                if st.button("Confirm and Insert Valid Records"):
                    inserted_count = 0
                    for _, row in valid_df.iterrows():
                        package_str = f"{row['Package_Numeric']} LPA"
                        insert_company_role(
                            row['Company'], 
                            row['Role'], 
                            row['Min_CGPA'], 
                            row['Required_Skills'], 
                            package_str
                        )
                        inserted_count += 1
                    st.success(f"Successfully inserted {inserted_count} records into the database.")
                    
        except Exception as e:
            st.error(f"Error processing CSV: {e}")
