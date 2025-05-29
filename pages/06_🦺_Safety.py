"""
Safety Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(
    page_title="Safety - gcPanel",
    page_icon="🦺",
    layout="wide"
)

initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("🦺 Safety Management")
st.markdown("Highland Tower Development - Workplace Safety & Compliance")
st.markdown("---")

# Initialize safety data
if 'safety_incidents' not in st.session_state:
    st.session_state.safety_incidents = [
        {
            "id": "SF-001",
            "date": "2024-12-10",
            "type": "Near Miss",
            "severity": "Low",
            "description": "Worker slipped on wet surface but caught balance",
            "location": "Level 3 - East Wing",
            "reported_by": "John Smith",
            "status": "Investigated"
        }
    ]

tab1, tab2, tab3 = st.tabs(["📝 Report Incident", "📊 Incidents", "📋 Safety Metrics"])

with tab1:
    st.subheader("📝 Report Safety Incident")
    
    with st.form("safety_incident_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            incident_date = st.date_input("Incident Date", value=date.today())
            incident_type = st.selectbox("Incident Type", 
                ["Near Miss", "First Aid", "Medical Treatment", "Lost Time", "Property Damage"])
            severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
            location = st.text_input("Location", placeholder="Building area, floor, specific location")
        
        with col2:
            reported_by = st.text_input("Reported By", value=st.session_state.get('user_name', ''))
            injured_person = st.text_input("Injured Person (if applicable)")
            weather_conditions = st.text_input("Weather Conditions")
            time_of_incident = st.time_input("Time of Incident")
        
        description = st.text_area("Incident Description", height=100,
            placeholder="Detailed description of what happened...")
        
        immediate_actions = st.text_area("Immediate Actions Taken", height=80,
            placeholder="Actions taken immediately after the incident...")
        
        submitted = st.form_submit_button("📤 Submit Report", type="primary", use_container_width=True)
        
        if submitted:
            new_incident = {
                "id": f"SF-{len(st.session_state.safety_incidents) + 1:03d}",
                "date": str(incident_date),
                "type": incident_type,
                "severity": severity,
                "description": description,
                "location": location,
                "reported_by": reported_by,
                "status": "Under Investigation",
                "injured_person": injured_person,
                "weather_conditions": weather_conditions,
                "time": str(time_of_incident),
                "immediate_actions": immediate_actions
            }
            st.session_state.safety_incidents.insert(0, new_incident)
            st.success(f"Safety incident {new_incident['id']} reported successfully!")
            st.rerun()

with tab2:
    st.subheader("📊 Safety Incidents Database")
    
    if st.session_state.safety_incidents:
        df = pd.DataFrame(st.session_state.safety_incidents)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search incidents...")
        with col2:
            severity_filter = st.selectbox("Severity", ["All", "Low", "Medium", "High", "Critical"])
        with col3:
            type_filter = st.selectbox("Type", ["All", "Near Miss", "First Aid", "Medical Treatment", "Lost Time"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[
                filtered_df.astype(str).apply(
                    lambda x: x.str.contains(search_term, case=False, na=False)
                ).any(axis=1)
            ]
        
        if severity_filter != "All":
            filtered_df = filtered_df[filtered_df['severity'] == severity_filter]
            
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['type'] == type_filter]
        
        st.write(f"**Total Incidents:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(
                clean_dataframe_for_display(filtered_df),
                column_config={
                    "id": st.column_config.TextColumn("Incident ID"),
                    "date": st.column_config.DateColumn("Date"),
                    "type": st.column_config.TextColumn("Type"),
                    "severity": st.column_config.TextColumn("Severity"),
                    "location": st.column_config.TextColumn("Location"),
                    "status": st.column_config.TextColumn("Status")
                },
                hide_index=True,
                use_container_width=True
            )

with tab3:
    st.subheader("📋 Safety Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Days Without Incident", "47", "2")
    
    with col2:
        st.metric("Total Incidents (Month)", "3", "-2")
    
    with col3:
        st.metric("Near Misses", "2", "0")
    
    with col4:
        st.metric("Safety Training %", "98%", "2%")