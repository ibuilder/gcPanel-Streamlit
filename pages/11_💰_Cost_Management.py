"""
Cost Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(page_title="Cost Management - gcPanel", page_icon="💰", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("💰 Cost Management")
st.markdown("Highland Tower Development - Budget Tracking & Cost Control")
st.markdown("---")

if 'cost_items' not in st.session_state:
    st.session_state.cost_items = [
        {
            "id": "CST-001",
            "category": "Labor",
            "description": "Foundation Work - Week 12",
            "budgeted": 125000,
            "actual": 118500,
            "variance": -6500,
            "date": "2024-12-15",
            "status": "Completed"
        }
    ]

tab1, tab2, tab3 = st.tabs(["📊 Cost Tracking", "📝 Add Cost Item", "📈 Budget Analysis"])

with tab1:
    st.subheader("📊 Cost Tracking")
    
    if st.session_state.cost_items:
        df = pd.DataFrame(st.session_state.cost_items)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search cost items...")
        with col2:
            category_filter = st.selectbox("Category", ["All", "Labor", "Materials", "Equipment", "Subcontractors"])
        with col3:
            status_filter = st.selectbox("Status", ["All", "Planned", "In Progress", "Completed"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
            
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        st.write(f"**Total Cost Items:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            display_df = filtered_df.copy()
            if 'budgeted' in display_df.columns:
                display_df['Budget'] = display_df['budgeted'].apply(lambda x: f"${x:,.2f}")
            if 'actual' in display_df.columns:
                display_df['Actual'] = display_df['actual'].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(clean_dataframe_for_display(display_df), use_container_width=True, hide_index=True)
    else:
        st.info("No cost items tracked. Add your first cost item in the Add tab!")

with tab2:
    st.subheader("📝 Add Cost Item")
    
    with st.form("cost_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Cost Category", 
                ["Labor", "Materials", "Equipment", "Subcontractors", "Other"])
            description = st.text_input("Description", placeholder="Detailed cost description")
            budgeted_amount = st.number_input("Budgeted Amount ($)", min_value=0.0, format="%.2f")
            actual_amount = st.number_input("Actual Amount ($)", min_value=0.0, format="%.2f")
        
        with col2:
            cost_date = st.date_input("Cost Date", value=date.today())
            cost_code = st.text_input("Cost Code", placeholder="WBS or accounting code")
            vendor = st.text_input("Vendor/Supplier", placeholder="Company name")
            status = st.selectbox("Status", ["Pending", "Approved", "Completed", "Rejected"])
        
        notes = st.text_area("Notes", placeholder="Additional cost information...")
        
        submitted = st.form_submit_button("💰 Add Cost Item", type="primary", use_container_width=True)
        
        if submitted and description and budgeted_amount:
            variance = actual_amount - budgeted_amount
            new_cost = {
                "id": f"CST-{len(st.session_state.cost_items) + 1:03d}",
                "category": category,
                "description": description,
                "budgeted": budgeted_amount,
                "actual": actual_amount,
                "variance": variance,
                "date": str(cost_date),
                "cost_code": cost_code,
                "vendor": vendor,
                "status": status,
                "notes": notes
            }
            st.session_state.cost_items.insert(0, new_cost)
            st.success(f"Cost item {new_cost['id']} added successfully!")
            st.rerun()

with tab2:
    st.subheader("📊 Cost Tracking")
    
    if st.session_state.cost_items:
        df = pd.DataFrame(st.session_state.cost_items)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search cost items...")
        with col2:
            category_filter = st.selectbox("Category", ["All", "Labor", "Materials", "Equipment"])
        with col3:
            status_filter = st.selectbox("Status", ["All", "Pending", "Approved", "Completed"])
        
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
        
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
            
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        st.write(f"**Total Cost Items:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            display_df = filtered_df.copy()
            display_df['Budgeted'] = display_df['budgeted'].apply(lambda x: f"${x:,.2f}")
            display_df['Actual'] = display_df['actual'].apply(lambda x: f"${x:,.2f}")
            display_df['Variance'] = display_df['variance'].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(clean_dataframe_for_display(display_df), use_container_width=True, hide_index=True)
    else:
        st.info("No cost items recorded. Add your first cost item above!")

with tab3:
    st.subheader("📈 Budget Analysis")
    
    if st.session_state.cost_items:
        df = pd.DataFrame(st.session_state.cost_items)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_budgeted = df['budgeted'].sum()
            st.metric("Total Budgeted", f"${total_budgeted:,.0f}")
        
        with col2:
            total_actual = df['actual'].sum()
            st.metric("Total Actual", f"${total_actual:,.0f}")
        
        with col3:
            total_variance = df['variance'].sum()
            st.metric("Total Variance", f"${total_variance:,.0f}", delta_color="inverse")
        
        with col4:
            variance_percent = (total_variance / total_budgeted * 100) if total_budgeted > 0 else 0
            st.metric("Variance %", f"{variance_percent:.1f}%", delta_color="inverse")