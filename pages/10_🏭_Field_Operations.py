"""
Field Operations Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Field Operations - gcPanel", page_icon="🏭", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("🏭 Field Operations")
st.markdown("Highland Tower Development - Field Activity Management")
st.markdown("---")

if 'field_activities' not in st.session_state:
    st.session_state.field_activities = []

tab1, tab2 = st.tabs(["📝 Log Activity", "📊 Operations Log"])

with tab1:
    st.subheader("📝 Log Field Activity")
    
    with st.form("field_activity_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            activity_date = st.date_input("Activity Date", value=date.today())
            activity_type = st.selectbox("Activity Type", 
                ["Construction", "Inspection", "Survey", "Testing", "Installation", "Maintenance"])
            crew_lead = st.text_input("Crew Lead", placeholder="Lead supervisor name")
            crew_size = st.number_input("Crew Size", min_value=1, max_value=50, value=5)
        
        with col2:
            start_time = st.time_input("Start Time")
            end_time = st.time_input("End Time")
            location = st.text_input("Location", placeholder="Building area, floor, grid")
            equipment_used = st.text_input("Equipment Used", placeholder="Heavy equipment, tools")
        
        description = st.text_area("Activity Description", placeholder="Detailed description of work performed...")
        materials_used = st.text_area("Materials Used", placeholder="Materials consumed during activity...")
        
        submitted = st.form_submit_button("📋 Log Activity", type="primary", use_container_width=True)
        
        if submitted:
            new_activity = {
                "id": f"FO-{len(st.session_state.field_activities) + 1:03d}",
                "date": str(activity_date),
                "type": activity_type,
                "crew_lead": crew_lead,
                "crew_size": crew_size,
                "start_time": str(start_time),
                "end_time": str(end_time),
                "location": location,
                "equipment_used": equipment_used,
                "description": description,
                "materials_used": materials_used,
                "logged_by": st.session_state.get('user_name', 'User')
            }
            st.session_state.field_activities.insert(0, new_activity)
            st.success(f"Field activity {new_activity['id']} logged successfully!")
            st.rerun()

with tab2:
    st.subheader("📊 Field Operations Log")
    
    if st.session_state.field_activities:
        df = pd.DataFrame(st.session_state.field_activities)
        
        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("🔍 Search activities...")
        with col2:
            type_filter = st.selectbox("Activity Type", ["All", "Construction", "Inspection", "Survey"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['type'] == type_filter]
        
        st.write(f"**Total Activities:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No field activities logged. Log your first activity above!")