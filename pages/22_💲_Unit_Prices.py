"""
Unit Prices Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Unit Prices - gcPanel", page_icon="💲", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("💲 Unit Prices Management")
st.markdown("Highland Tower Development - Construction Unit Price Database")
st.markdown("---")

if 'unit_prices' not in st.session_state:
    st.session_state.unit_prices = []

tab1, tab2, tab3 = st.tabs(["📝 Add Unit Price", "📊 Price Database", "📈 Price Analysis"])

with tab1:
    st.subheader("📝 Add Unit Price")
    
    with st.form("unit_price_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            item_description = st.text_input("Item Description", placeholder="Work item or material description")
            category = st.selectbox("Category", 
                ["Labor", "Materials", "Equipment", "Subcontractor", "Other"])
            unit = st.text_input("Unit of Measure", placeholder="e.g., SF, LF, CY, EA")
            unit_price = st.number_input("Unit Price ($)", min_value=0.0, format="%.2f")
        
        with col2:
            effective_date = st.date_input("Effective Date", value=date.today())
            supplier_contractor = st.text_input("Supplier/Contractor", placeholder="Source of pricing")
            location = st.text_input("Location", placeholder="Where price applies")
            validity_period = st.number_input("Valid for (days)", min_value=1, value=30)
        
        specifications = st.text_area("Specifications", placeholder="Detailed specifications and requirements...")
        notes = st.text_area("Notes", placeholder="Additional pricing information...")
        
        submitted = st.form_submit_button("💲 Add Unit Price", type="primary", use_container_width=True)
        
        if submitted and item_description and unit_price > 0:
            new_price = {
                "id": f"UP-{len(st.session_state.unit_prices) + 1:03d}",
                "item_description": item_description,
                "category": category,
                "unit": unit,
                "unit_price": unit_price,
                "effective_date": str(effective_date),
                "supplier_contractor": supplier_contractor,
                "location": location,
                "validity_period": validity_period,
                "specifications": specifications,
                "notes": notes,
                "status": "Active",
                "created_date": str(date.today())
            }
            st.session_state.unit_prices.insert(0, new_price)
            st.success(f"Unit price {new_price['id']} added successfully!")
            st.rerun()

with tab2:
    st.subheader("📊 Unit Price Database")
    
    if st.session_state.unit_prices:
        df = pd.DataFrame(st.session_state.unit_prices)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("Search items...")
        with col2:
            category_filter = st.selectbox("Category", ["All", "Labor", "Materials", "Equipment"])
        with col3:
            supplier_filter = st.selectbox("Supplier", ["All"] + list(df['supplier_contractor'].unique()) if len(df) > 0 else ["All"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
            
        if supplier_filter != "All":
            filtered_df = filtered_df[filtered_df['supplier_contractor'] == supplier_filter]
        
        st.write(f"**Total Unit Prices:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            display_df = filtered_df.copy()
            display_df['Unit Price'] = display_df['unit_price'].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(clean_dataframe_for_display(display_df), use_container_width=True, hide_index=True)
    else:
        st.info("No unit prices entered. Add your first unit price above!")

with tab3:
    st.subheader("📈 Price Analysis")
    
    if st.session_state.unit_prices:
        df = pd.DataFrame(st.session_state.unit_prices)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_items = len(df)
            st.metric("Total Items", total_items)
        
        with col2:
            avg_price = df['unit_price'].mean()
            st.metric("Average Unit Price", f"${avg_price:.2f}")
        
        with col3:
            highest_price = df['unit_price'].max()
            st.metric("Highest Price", f"${highest_price:.2f}")
        
        with col4:
            active_prices = len(df[df['status'] == 'Active'])
            st.metric("Active Prices", active_prices)
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Items", "0")
        with col2:
            st.metric("Average Unit Price", "$0.00")
        with col3:
            st.metric("Highest Price", "$0.00")
        with col4:
            st.metric("Active Prices", "0")