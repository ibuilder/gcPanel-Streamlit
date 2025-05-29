"""
Material Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Material Management - gcPanel", page_icon="📦", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("📦 Material Management")
st.markdown("Highland Tower Development - Material Inventory & Tracking")
st.markdown("---")

if 'materials' not in st.session_state:
    st.session_state.materials = []

tab1, tab2, tab3 = st.tabs(["📦 Material Inventory", "📝 Add Material", "📊 Usage Tracking"])

with tab1:
    st.subheader("📦 Material Inventory")
    
    if st.session_state.materials:
        df = pd.DataFrame(st.session_state.materials)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search materials...", key="material_management_search_1")
        with col2:
            category_filter = st.selectbox("Category", ["All", "Concrete", "Steel", "Lumber", "Electrical"])
        with col3:
            status_filter = st.selectbox("Status", ["All", "In Stock", "Low Stock", "Out of Stock"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
            
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        st.write(f"**Total Materials:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
    else:
        st.info("No materials in inventory. Add your first material in the Add tab!")

with tab2:
    st.subheader("📝 Add Material to Inventory")
    
    with st.form("material_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            material_name = st.text_input("Material Name", placeholder="Material description")
            category = st.selectbox("Category", 
                ["Concrete", "Steel", "Lumber", "Electrical", "Plumbing", "HVAC", "Finishes", "Other"])
            supplier = st.text_input("Supplier", placeholder="Supplier company name")
            unit_of_measure = st.text_input("Unit of Measure", placeholder="e.g., tons, pieces, SF")
        
        with col2:
            quantity_received = st.number_input("Quantity Received", min_value=0.0, format="%.2f")
            unit_cost = st.number_input("Unit Cost ($)", min_value=0.0, format="%.2f")
            delivery_date = st.date_input("Delivery Date", value=date.today())
            storage_location = st.text_input("Storage Location", placeholder="Where material is stored")
        
        specifications = st.text_area("Specifications", placeholder="Material specifications and standards...")
        po_number = st.text_input("PO Number", placeholder="Purchase order reference")
        
        submitted = st.form_submit_button("📦 Add to Inventory", type="primary", use_container_width=True)
        
        if submitted and material_name:
            total_cost = quantity_received * unit_cost
            new_material = {
                "id": f"MAT-{len(st.session_state.materials) + 1:03d}",
                "material_name": material_name,
                "category": category,
                "supplier": supplier,
                "unit_of_measure": unit_of_measure,
                "quantity_received": quantity_received,
                "quantity_remaining": quantity_received,
                "unit_cost": unit_cost,
                "total_cost": total_cost,
                "delivery_date": str(delivery_date),
                "storage_location": storage_location,
                "specifications": specifications,
                "po_number": po_number,
                "status": "In Stock"
            }
            st.session_state.materials.insert(0, new_material)
            st.success(f"Material {new_material['id']} added to inventory!")
            st.rerun()

with tab2:
    st.subheader("📦 Material Inventory")
    
    if st.session_state.materials:
        df = pd.DataFrame(st.session_state.materials)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("Search materials...")
        with col2:
            category_filter = st.selectbox("Category", ["All", "Concrete", "Steel", "Lumber", "Electrical"])
        with col3:
            status_filter = st.selectbox("Status", ["All", "In Stock", "Low Stock", "Out of Stock"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
            
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        st.write(f"**Total Material Items:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            display_df = filtered_df.copy()
            display_df['Unit Cost'] = display_df['unit_cost'].apply(lambda x: f"${x:.2f}")
            display_df['Total Cost'] = display_df['total_cost'].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(clean_dataframe_for_display(display_df), use_container_width=True, hide_index=True)
    else:
        st.info("No materials in inventory. Add your first material above!")

with tab3:
    st.subheader("📊 Material Usage & Analytics")
    
    if st.session_state.materials:
        df = pd.DataFrame(st.session_state.materials)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_items = len(df)
            st.metric("Total Items", total_items)
        
        with col2:
            total_value = df['total_cost'].sum()
            st.metric("Total Inventory Value", f"${total_value:,.0f}")
        
        with col3:
            in_stock = len(df[df['status'] == 'In Stock'])
            st.metric("Items In Stock", in_stock)
        
        with col4:
            avg_cost = df['unit_cost'].mean()
            st.metric("Average Unit Cost", f"${avg_cost:.2f}")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Items", "0")
        with col2:
            st.metric("Total Inventory Value", "$0")
        with col3:
            st.metric("Items In Stock", "0")
        with col4:
            st.metric("Average Unit Cost", "$0.00")