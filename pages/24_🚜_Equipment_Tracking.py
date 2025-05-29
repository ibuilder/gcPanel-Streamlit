"""
Equipment Tracking Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Equipment Tracking - gcPanel", page_icon="🚜", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("🚜 Equipment Tracking")
st.markdown("Highland Tower Development - Construction Equipment Management")
st.markdown("---")

if 'equipment' not in st.session_state:
    st.session_state.equipment = []

tab1, tab2, tab3 = st.tabs(["📝 Add Equipment", "🚜 Equipment Fleet", "📊 Utilization"])

with tab1:
    st.subheader("📝 Add Equipment")
    
    with st.form("equipment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            equipment_name = st.text_input("Equipment Name", placeholder="Equipment description")
            equipment_type = st.selectbox("Equipment Type", 
                ["Crane", "Excavator", "Loader", "Truck", "Generator", "Pump", "Tool", "Other"])
            make_model = st.text_input("Make/Model", placeholder="Manufacturer and model")
            serial_number = st.text_input("Serial Number", placeholder="Equipment serial number")
        
        with col2:
            rental_owned = st.selectbox("Rental/Owned", ["Rental", "Owned", "Leased"])
            daily_rate = st.number_input("Daily Rate ($)", min_value=0.0, format="%.2f")
            operator_required = st.selectbox("Operator Required", ["Yes", "No"])
            current_location = st.text_input("Current Location", placeholder="Where equipment is located")
        
        with col1:
            start_date = st.date_input("Start Date")
            end_date = st.date_input("Expected End Date")
        
        with col2:
            status = st.selectbox("Status", ["Available", "In Use", "Maintenance", "Off Site"])
            assigned_operator = st.text_input("Assigned Operator", placeholder="Operator name")
        
        specifications = st.text_area("Specifications", placeholder="Equipment specifications and capabilities...")
        maintenance_notes = st.text_area("Maintenance Notes", placeholder="Maintenance schedule and notes...")
        
        submitted = st.form_submit_button("🚜 Add Equipment", type="primary", use_container_width=True)
        
        if submitted and equipment_name:
            new_equipment = {
                "id": f"EQ-{len(st.session_state.equipment) + 1:03d}",
                "equipment_name": equipment_name,
                "equipment_type": equipment_type,
                "make_model": make_model,
                "serial_number": serial_number,
                "rental_owned": rental_owned,
                "daily_rate": daily_rate,
                "operator_required": operator_required,
                "current_location": current_location,
                "start_date": str(start_date),
                "end_date": str(end_date),
                "status": status,
                "assigned_operator": assigned_operator,
                "specifications": specifications,
                "maintenance_notes": maintenance_notes,
                "hours_used": 0,
                "added_date": str(date.today())
            }
            st.session_state.equipment.insert(0, new_equipment)
            st.success(f"Equipment {new_equipment['id']} added successfully!")
            st.rerun()

with tab2:
    st.subheader("🚜 Equipment Fleet")
    
    if st.session_state.equipment:
        df = pd.DataFrame(st.session_state.equipment)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("Search equipment...")
        with col2:
            type_filter = st.selectbox("Equipment Type", ["All", "Crane", "Excavator", "Loader", "Truck"])
        with col3:
            status_filter = st.selectbox("Status", ["All", "Available", "In Use", "Maintenance"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['equipment_type'] == type_filter]
            
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        st.write(f"**Total Equipment:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            display_df = filtered_df.copy()
            display_df['Daily Rate'] = display_df['daily_rate'].apply(lambda x: f"${x:.2f}")
            
            st.dataframe(clean_dataframe_for_display(display_df), use_container_width=True, hide_index=True)
    else:
        st.info("No equipment registered. Add your first equipment above!")

with tab3:
    st.subheader("📊 Equipment Utilization")
    
    if st.session_state.equipment:
        df = pd.DataFrame(st.session_state.equipment)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_equipment = len(df)
            st.metric("Total Equipment", total_equipment)
        
        with col2:
            in_use = len(df[df['status'] == 'In Use'])
            st.metric("Currently In Use", in_use)
        
        with col3:
            daily_cost = df['daily_rate'].sum()
            st.metric("Total Daily Cost", f"${daily_cost:,.0f}")
        
        with col4:
            available = len(df[df['status'] == 'Available'])
            st.metric("Available", available)
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Equipment", "0")
        with col2:
            st.metric("Currently In Use", "0")
        with col3:
            st.metric("Total Daily Cost", "$0")
        with col4:
            st.metric("Available", "0")