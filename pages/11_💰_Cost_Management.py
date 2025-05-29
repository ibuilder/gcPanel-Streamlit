"""
Cost Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Cost Management - gcPanel", page_icon="💰", layout="wide")
# Check authentication
if not check_authentication():
    st.error("🔒 Please log in to access this page")
    st.stop()


st.title("💰 Cost Management")
st.markdown("Highland Tower Development - Project Cost Control & Budget Management")
st.markdown("---")

# Initialize session state for cost data
if 'cost_items' not in st.session_state:
    st.session_state.cost_items = [
        {
            "id": "COST-001",
            "category": "Labor",
            "description": "Structural Steel Installation - Floors 20-25",
            "budget": 1250000,
            "actual": 1175000,
            "committed": 1200000,
            "variance": 75000,
            "status": "On Budget",
            "last_updated": "2024-12-15"
        },
        {
            "id": "COST-002", 
            "category": "Materials",
            "description": "Concrete & Rebar - Foundation & Structure",
            "budget": 850000,
            "actual": 875000,
            "committed": 850000,
            "variance": -25000,
            "status": "Over Budget",
            "last_updated": "2024-12-14"
        }
    ]

# Main tabs
tab1, tab2, tab3 = st.tabs(["📊 Cost Overview", "📝 Add Cost Item", "📈 Budget Analysis"])

with tab1:
    st.subheader("📊 Cost Database")
    if st.session_state.cost_items:
        df = pd.DataFrame(st.session_state.cost_items)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No cost data available")

with tab2:
    st.subheader("📝 Add New Cost Item")
    st.info("Cost item creation form coming soon")

with tab3:
    st.subheader("📈 Budget Analysis")
    if st.session_state.cost_items:
        df = pd.DataFrame(st.session_state.cost_items)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_budget = sum(item['budget'] for item in st.session_state.cost_items)
            st.metric("Total Budget", f"${total_budget:,.0f}")
        
        with col2:
            total_actual = sum(item['actual'] for item in st.session_state.cost_items)
            st.metric("Total Actual", f"${total_actual:,.0f}")
        
        with col3:
            total_variance = sum(item['variance'] for item in st.session_state.cost_items)
            st.metric("Total Variance", f"${total_variance:,.0f}")
        
        with col4:
            on_budget_count = len([item for item in st.session_state.cost_items if item['status'] == 'On Budget'])
            st.metric("On Budget Items", f"{on_budget_count}/{len(st.session_state.cost_items)}")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Budget by Category")
            category_budget = df.groupby('category')['budget'].sum()
            st.bar_chart(category_budget)
        
        with col2:
            st.subheader("Status Distribution")
            status_counts = df['status'].value_counts()
            st.bar_chart(status_counts)
    else:
        st.info("No cost data available for analysis")
