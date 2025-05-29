"""
Inspections Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Inspections - gcPanel", page_icon="🔧", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("🔧 Inspections Management")
st.markdown("Highland Tower Development - Inspection Scheduling & Tracking")
st.markdown("---")

if 'inspections' not in st.session_state:
    st.session_state.inspections = []

tab1, tab2, tab3 = st.tabs(["📝 Schedule Inspection", "📊 Inspection Log", "📈 Compliance Tracking"])

with tab1:
    st.subheader("📝 Schedule New Inspection")
    
    with st.form("inspection_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            inspection_type = st.selectbox("Inspection Type", 
                ["Foundation", "Framing", "Electrical Rough-in", "Plumbing Rough-in", "Insulation", "Drywall", "Final"])
            requested_date = st.date_input("Requested Date")
            inspector = st.text_input("Inspector", placeholder="Inspector name or agency")
            contact_person = st.text_input("Site Contact", value=st.session_state.get('user_name', ''))
        
        with col2:
            work_area = st.text_input("Work Area", placeholder="Building area, floor, units")
            contractor = st.text_input("Contractor", placeholder="Responsible contractor")
            permit_number = st.text_input("Permit Number", placeholder="Building permit reference")
            priority = st.selectbox("Priority", ["Normal", "Urgent", "Emergency"])
        
        scope_description = st.text_area("Scope Description", placeholder="What work is ready for inspection...")
        special_requirements = st.text_area("Special Requirements", placeholder="Access requirements, safety notes...")
        
        submitted = st.form_submit_button("📅 Schedule Inspection", type="primary", use_container_width=True)
        
        if submitted and inspection_type and work_area:
            new_inspection = {
                "id": f"INS-{len(st.session_state.inspections) + 1:03d}",
                "inspection_type": inspection_type,
                "requested_date": str(requested_date),
                "inspector": inspector,
                "contact_person": contact_person,
                "work_area": work_area,
                "contractor": contractor,
                "permit_number": permit_number,
                "priority": priority,
                "scope_description": scope_description,
                "special_requirements": special_requirements,
                "status": "Scheduled",
                "result": "Pending",
                "scheduled_date": str(date.today())
            }
            st.session_state.inspections.insert(0, new_inspection)
            st.success(f"Inspection {new_inspection['id']} scheduled successfully!")
            st.rerun()

with tab2:
    st.subheader("📊 Inspection Log")
    
    if st.session_state.inspections:
        df = pd.DataFrame(st.session_state.inspections)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("Search inspections...")
        with col2:
            type_filter = st.selectbox("Type", ["All", "Foundation", "Framing", "Electrical Rough-in"])
        with col3:
            status_filter = st.selectbox("Status", ["All", "Scheduled", "Completed", "Failed", "Cancelled"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['inspection_type'] == type_filter]
            
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        st.write(f"**Total Inspections:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No inspections scheduled. Schedule your first inspection above!")

with tab3:
    st.subheader("📈 Compliance Tracking")
    
    if st.session_state.inspections:
        df = pd.DataFrame(st.session_state.inspections)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_inspections = len(df)
            st.metric("Total Inspections", total_inspections)
        
        with col2:
            completed = len(df[df['status'] == 'Completed'])
            st.metric("Completed", completed)
        
        with col3:
            pending = len(df[df['status'] == 'Scheduled'])
            st.metric("Pending", pending)
        
        with col4:
            failed = len(df[df['status'] == 'Failed'])
            st.metric("Failed", failed, delta_color="inverse")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Inspections", "0")
        with col2:
            st.metric("Completed", "0")
        with col3:
            st.metric("Pending", "0")
        with col4:
            st.metric("Failed", "0")