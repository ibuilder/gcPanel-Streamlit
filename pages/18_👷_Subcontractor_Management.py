"""
Subcontractor Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Subcontractors - gcPanel", page_icon="👷", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("👷 Subcontractor Management")
st.markdown("Highland Tower Development - Subcontractor Coordination & Tracking")
st.markdown("---")

if 'subcontractors' not in st.session_state:
    st.session_state.subcontractors = []

tab1, tab2, tab3 = st.tabs(["📊 Subcontractor Directory", "📝 Add Subcontractor", "📈 Performance Tracking"])

with tab1:
    st.subheader("📊 Subcontractor Directory")
    
    if st.session_state.subcontractors:
        df = pd.DataFrame(st.session_state.subcontractors)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search subcontractors...")
        with col2:
            trade_filter = st.selectbox("Trade", ["All", "Electrical", "Plumbing", "HVAC", "Flooring"])
        with col3:
            status_filter = st.selectbox("Status", ["All", "Active", "Inactive", "Under Review"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if trade_filter != "All":
            filtered_df = filtered_df[filtered_df['trade'] == trade_filter]
            
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        st.write(f"**Total Subcontractors:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No subcontractors registered. Add your first subcontractor in the Add tab!")

with tab2:
    st.subheader("📝 Add New Subcontractor")
    
    with st.form("subcontractor_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name", placeholder="Subcontractor company name")
            trade = st.selectbox("Trade", 
                ["General", "Electrical", "Plumbing", "HVAC", "Drywall", "Flooring", "Roofing", "Concrete", "Steel"])
            contact_person = st.text_input("Primary Contact", placeholder="Main contact person")
            phone = st.text_input("Phone Number", placeholder="Primary phone number")
        
        with col2:
            email = st.text_input("Email", placeholder="Primary email address")
            license_number = st.text_input("License Number", placeholder="Professional license number")
            insurance_expiry = st.date_input("Insurance Expiry")
            contract_value = st.number_input("Contract Value ($)", min_value=0.0, format="%.2f")
        
        address = st.text_area("Address", placeholder="Company address...")
        scope_of_work = st.text_area("Scope of Work", placeholder="Detailed scope description...")
        
        col3, col4 = st.columns(2)
        with col3:
            start_date = st.date_input("Start Date")
            status = st.selectbox("Status", ["Qualified", "Active", "Completed", "Suspended"])
        with col4:
            end_date = st.date_input("Expected End Date")
            performance_rating = st.selectbox("Performance Rating", ["Excellent", "Good", "Fair", "Poor", "Not Rated"])
        
        submitted = st.form_submit_button("👷 Add Subcontractor", type="primary", use_container_width=True)
        
        if submitted and company_name and trade:
            new_subcontractor = {
                "id": f"SUB-{len(st.session_state.subcontractors) + 1:03d}",
                "company_name": company_name,
                "trade": trade,
                "contact_person": contact_person,
                "phone": phone,
                "email": email,
                "license_number": license_number,
                "insurance_expiry": str(insurance_expiry),
                "contract_value": contract_value,
                "address": address,
                "scope_of_work": scope_of_work,
                "start_date": str(start_date),
                "end_date": str(end_date),
                "status": status,
                "performance_rating": performance_rating,
                "added_date": str(date.today())
            }
            st.session_state.subcontractors.insert(0, new_subcontractor)
            st.success(f"Subcontractor {new_subcontractor['id']} added successfully!")
            st.rerun()

with tab2:
    st.subheader("📊 Subcontractor Directory")
    
    if st.session_state.subcontractors:
        df = pd.DataFrame(st.session_state.subcontractors)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("Search subcontractors...")
        with col2:
            trade_filter = st.selectbox("Trade", ["All", "Electrical", "Plumbing", "HVAC", "Drywall"])
        with col3:
            status_filter = st.selectbox("Status", ["All", "Qualified", "Active", "Completed"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if trade_filter != "All":
            filtered_df = filtered_df[filtered_df['trade'] == trade_filter]
            
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        st.write(f"**Total Subcontractors:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            display_df = filtered_df.copy()
            display_df['Contract Value'] = display_df['contract_value'].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(clean_dataframe_for_display(display_df), use_container_width=True, hide_index=True)
    else:
        st.info("No subcontractors registered. Add your first subcontractor above!")

with tab3:
    st.subheader("📈 Subcontractor Performance")
    
    if st.session_state.subcontractors:
        df = pd.DataFrame(st.session_state.subcontractors)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_subs = len(df)
            st.metric("Total Subcontractors", total_subs)
        
        with col2:
            active_subs = len(df[df['status'] == 'Active'])
            st.metric("Active", active_subs)
        
        with col3:
            total_value = df['contract_value'].sum()
            st.metric("Total Contract Value", f"${total_value:,.0f}")
        
        with col4:
            avg_rating = len(df[df['performance_rating'].isin(['Excellent', 'Good'])])
            st.metric("Good+ Rated", avg_rating)
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Subcontractors", "0")
        with col2:
            st.metric("Active", "0")
        with col3:
            st.metric("Total Contract Value", "$0")
        with col4:
            st.metric("Good+ Rated", "0")