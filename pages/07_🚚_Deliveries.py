"""
Deliveries Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Deliveries - gcPanel", page_icon="🚚", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("🚚 Deliveries Management")
st.markdown("Highland Tower Development - Material Delivery Tracking")
st.markdown("---")

if 'deliveries' not in st.session_state:
    st.session_state.deliveries = []

tab1, tab2 = st.tabs(["📊 Delivery Records", "📝 Log Delivery"])

with tab1:
    st.subheader("📊 Delivery Records")
    
    if st.session_state.deliveries:
        df = pd.DataFrame(st.session_state.deliveries)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search deliveries...")
        with col2:
            material_filter = st.selectbox("Material", ["All", "Concrete", "Steel", "Lumber", "Electrical"])
        with col3:
            date_filter = st.date_input("Filter by Date")
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if material_filter != "All":
            filtered_df = filtered_df[filtered_df['material_type'] == material_filter]
        
        st.write(f"**Total Deliveries:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No deliveries recorded. Log your first delivery in the Log tab!")

with tab2:
    st.subheader("📝 Log New Delivery")
    
    with st.form("delivery_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            delivery_date = st.date_input("Delivery Date", value=date.today())
            supplier = st.text_input("Supplier", placeholder="Company name")
            material_type = st.selectbox("Material Type", 
                ["Concrete", "Steel", "Lumber", "Electrical", "Plumbing", "HVAC", "Other"])
            quantity = st.number_input("Quantity", min_value=0.0, format="%.2f")
            unit = st.text_input("Unit", placeholder="tons, yards, pieces, etc.")
        
        with col2:
            delivery_time = st.time_input("Delivery Time")
            received_by = st.text_input("Received By", value=st.session_state.get('user_name', ''))
            location = st.text_input("Storage Location", placeholder="Where materials were placed")
            po_number = st.text_input("PO Number", placeholder="Purchase order reference")
        
        description = st.text_area("Description & Notes", placeholder="Detailed description of delivered materials...")
        
        submitted = st.form_submit_button("📦 Log Delivery", type="primary", use_container_width=True)
        
        if submitted and supplier and material_type:
            new_delivery = {
                "id": f"DEL-{len(st.session_state.deliveries) + 1:03d}",
                "date": str(delivery_date),
                "time": str(delivery_time),
                "supplier": supplier,
                "material_type": material_type,
                "quantity": quantity,
                "unit": unit,
                "received_by": received_by,
                "location": location,
                "po_number": po_number,
                "description": description,
                "status": "Delivered"
            }
            st.session_state.deliveries.insert(0, new_delivery)
            st.success(f"Delivery {new_delivery['id']} logged successfully!")
            st.rerun()

with tab2:
    st.subheader("📊 Delivery Records")
    
    if st.session_state.deliveries:
        df = pd.DataFrame(st.session_state.deliveries)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search deliveries...")
        with col2:
            material_filter = st.selectbox("Material", ["All", "Concrete", "Steel", "Lumber", "Electrical"])
        with col3:
            date_filter = st.date_input("Filter by Date")
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if material_filter != "All":
            filtered_df = filtered_df[filtered_df['material_type'] == material_filter]
        
        st.write(f"**Total Deliveries:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No deliveries recorded. Log your first delivery above!")