import streamlit as st
import pandas as pd
from database.database import get_company_roles, get_placements

st.title("Data Quality Report")
st.markdown("This module analyzes the current data in the SQLite database to identify missing values, duplicates, and invalid entries.")

tab1, tab2 = st.tabs(["Company Roles Data Quality", "Placements Data Quality"])

with tab1:
    roles_data = get_company_roles()
    if roles_data:
        df_roles = pd.DataFrame(roles_data)
        st.write("### Raw Data Preview")
        st.dataframe(df_roles.head())
        
        total_records = len(df_roles)
        
        missing_mask = df_roles.isnull().any(axis=1) | (df_roles == '').any(axis=1)
        missing_count = missing_mask.sum()
        
        duplicate_mask = df_roles.duplicated(subset=['company_name', 'role'], keep=False)
        duplicate_count = duplicate_mask.sum()
        
        df_roles['minimum_cgpa_num'] = pd.to_numeric(df_roles['minimum_cgpa'], errors='coerce')
        invalid_cgpa_mask = df_roles['minimum_cgpa_num'].isnull() | (df_roles['minimum_cgpa_num'] < 0) | (df_roles['minimum_cgpa_num'] > 10)
        invalid_cgpa_count = invalid_cgpa_mask.sum()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Records", total_records)
        col2.metric("Missing Values", int(missing_count))
        col3.metric("Duplicate Records", int(duplicate_count))
        col4.metric("Invalid CGPA", int(invalid_cgpa_count))
        
        st.divider()
        if missing_count > 0:
            st.warning("Records with Missing Values:")
            st.dataframe(df_roles[missing_mask])
        if duplicate_count > 0:
            st.warning("Duplicate Records:")
            st.dataframe(df_roles[duplicate_mask])
        if invalid_cgpa_count > 0:
            st.warning("Records with Invalid CGPA:")
            st.dataframe(df_roles[invalid_cgpa_mask])
    else:
        st.info("No company role data available.")

with tab2:
    placements_data = get_placements()
    if placements_data:
        df_place = pd.DataFrame(placements_data)
        st.write("### Raw Data Preview")
        st.dataframe(df_place.head())
        
        total_records = len(df_place)
        
        missing_mask = df_place.isnull().any(axis=1) | (df_place == '').any(axis=1)
        missing_count = missing_mask.sum()
        
        df_place['package_num'] = pd.to_numeric(df_place['package'].astype(str).str.extract(r'(\d+\.?\d*)', expand=False)[0], errors='coerce')
        invalid_package_mask = df_place['package_num'].isnull() | (df_place['package_num'] <= 0)
        invalid_package_count = invalid_package_mask.sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", total_records)
        col2.metric("Missing Values", int(missing_count))
        col3.metric("Invalid Packages", int(invalid_package_count))
        
        st.divider()
        if missing_count > 0:
            st.warning("Records with Missing Values:")
            st.dataframe(df_place[missing_mask])
        if invalid_package_count > 0:
            st.warning("Records with Invalid Packages:")
            st.dataframe(df_place[invalid_package_mask])
    else:
        st.info("No placement data available.")
