import streamlit as st
import pandas as pd
from database.database import get_company_roles, get_placements

st.title("Company & Placement Records")

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please login from the main page.")
    st.stop()

from utils.helpers import apply_student_sidebar_hiding
apply_student_sidebar_hiding()

st.markdown("Browse all available company roles and existing placement records.")

tab1, tab2 = st.tabs(["Company Roles Data", "Placements Data"])

with tab1:
    roles_data = get_company_roles()
    if roles_data:
        df_roles = pd.DataFrame(roles_data)
        st.markdown(f"#### Total Company Roles: `{len(df_roles)}`")
        
        search_company = st.text_input("🔍 Search by Company or Role", key="search_roles", placeholder="e.g., Google or Software Engineer")
        if search_company:
            mask = df_roles['company_name'].str.contains(search_company, case=False, na=False) | df_roles['role'].str.contains(search_company, case=False, na=False)
            df_roles = df_roles[mask]
            
        st.dataframe(df_roles, use_container_width=True)
    else:
        st.info("No company role data available.")

with tab2:
    placements_data = get_placements()
    if placements_data:
        df_place = pd.DataFrame(placements_data)
        st.markdown(f"#### Total Placements: `{len(df_place)}`")
        
        search_placement = st.text_input("🔍 Search by Student or Company", key="search_place", placeholder="e.g., Alice or Microsoft")
        if search_placement:
            mask = df_place['student_name'].str.contains(search_placement, case=False, na=False) | df_place['company_name'].str.contains(search_placement, case=False, na=False)
            df_place = df_place[mask]
            
        st.dataframe(df_place, use_container_width=True)
    else:
        st.info("No placement data available.")
