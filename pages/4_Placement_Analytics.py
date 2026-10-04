import streamlit as st
import pandas as pd
import plotly.express as px
from database.database import get_company_roles, get_placements

st.title("Placement Analytics")

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please login from the main page.")
    st.stop()

from utils.helpers import apply_student_sidebar_hiding
apply_student_sidebar_hiding()
st.markdown("Descriptive analytics and visualization of campus placement data.")

placements_data = get_placements()
roles_data = get_company_roles()

if not placements_data:
    st.warning("No placement data available for analytics.")
else:
    df_place = pd.DataFrame(placements_data)
    # Correct extraction logic: expand=False returns Series if one group. We just use extract(r'(\d+\.?\d*)')[0] safely.
    df_place['package_num'] = pd.to_numeric(df_place['package'].astype(str).str.extract(r'(\d+\.?\d*)', expand=False).iloc[:, 0] if isinstance(df_place['package'].astype(str).str.extract(r'(\d+\.?\d*)', expand=False), pd.DataFrame) else df_place['package'].astype(str).str.extract(r'(\d+\.?\d*)', expand=False), errors='coerce')
    # Better yet, just use extract with expand=True and take column 0
    df_place['package_num'] = pd.to_numeric(df_place['package'].astype(str).str.extract(r'(\d+\.?\d*)', expand=True)[0], errors='coerce')

    valid_packages = df_place.dropna(subset=['package_num'])
    
    st.header("Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Placements", len(df_place))
    col2.metric("Total Companies", df_place['company_name'].nunique())
    col3.metric("Total Roles", df_place['role'].nunique())
    
    if not valid_packages.empty:
        col4.metric("Average Package (LPA)", f"{valid_packages['package_num'].mean():.2f}")
        
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.header("Company-wise Analysis")
        company_counts = df_place['company_name'].value_counts().reset_index()
        company_counts.columns = ['Company', 'Placements']
        fig_company = px.bar(company_counts, x='Company', y='Placements', title="Placements by Company")
        st.plotly_chart(fig_company, use_container_width=True)
        
    with col2:
        st.header("Role-wise Analysis")
        role_counts = df_place['role'].value_counts().reset_index()
        role_counts.columns = ['Role', 'Placements']
        fig_role = px.bar(role_counts, x='Role', y='Placements', title="Placements by Role", color_discrete_sequence=['#ff7f0e'])
        st.plotly_chart(fig_role, use_container_width=True)
        
    st.divider()
    
    st.header("Package & Year Analysis")
    col1, col2 = st.columns(2)
    with col1:
        if not valid_packages.empty:
            fig_pack = px.histogram(valid_packages, x='package_num', nbins=10, title="Package Distribution (LPA)")
            st.plotly_chart(fig_pack, use_container_width=True)
            
    with col2:
        if 'year' in df_place.columns and not df_place['year'].isnull().all():
            year_counts = df_place['year'].value_counts().reset_index()
            year_counts.columns = ['Year', 'Placements']
            year_counts = year_counts.sort_values('Year')
            fig_year = px.line(year_counts, x='Year', y='Placements', markers=True, title="Placements by Year")
            fig_year.update_xaxes(type='category')
            st.plotly_chart(fig_year, use_container_width=True)
            
    st.divider()
    
    st.header("Descriptive Statistics (Package)")
    st.markdown("Basic statistical measures of the packages offered (in LPA):")
    if not valid_packages.empty:
        stats = valid_packages['package_num'].describe().to_frame().T
        stats = stats[['count', 'mean', '50%', 'min', 'max', 'std']]
        stats.columns = ['Count', 'Mean (Average)', 'Median', 'Minimum', 'Maximum', 'Standard Deviation']
        st.dataframe(stats.style.format("{:.2f}"))
    else:
        st.info("Not enough valid numeric package data to compute statistics.")

st.divider()

if roles_data:
    st.header("Required Skills Analysis")
    df_roles = pd.DataFrame(roles_data)
    
    all_skills = []
    for skills_str in df_roles['required_skills'].dropna():
        skills = [s.strip() for s in skills_str.split(',') if s.strip()]
        all_skills.extend(skills)
        
    if all_skills:
        skill_counts = pd.Series(all_skills).value_counts().reset_index()
        skill_counts.columns = ['Skill', 'Frequency']
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(skill_counts)
        with col2:
            fig_skills = px.bar(skill_counts.head(10), x='Skill', y='Frequency', title="Top 10 Most Required Skills")
            st.plotly_chart(fig_skills, use_container_width=True)
    else:
        st.info("No skills data found in company roles.")
