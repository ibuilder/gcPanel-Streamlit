"""
Cost Management module for the gcPanel Construction Management Dashboard.

This module provides cost management functionality including budgets, expenses,
forecasting, and financial reporting.

This module follows a clear CRUD pattern with:
1. List views for viewing all records with filtering/searching/sorting
2. Detail views for viewing individual records with Edit buttons
3. Add/Edit forms for creating and updating records
4. Analysis views for data visualization and metrics
"""

import streamlit as st
from modules.cost_management.budget_components import (
    render_budget_list, 
    render_budget_details, 
    render_budget_form, 
    render_budget_analysis
)

def render_cost_management():
    """Render the cost management module"""
    
    # Header
    st.title("Cost Management")
    
    # Add debug checkbox
    if st.checkbox("🔍 Debug state", value=False, key="cost_debug_state"):
        st.write(f"Current cost view: {st.session_state.get('cost_view')}")
        st.write(f"Selected budget ID: {st.session_state.get('selected_budget_id')}")
        st.write(f"Edit budget ID: {st.session_state.get('edit_budget_id')}")
    
    # Initialize session state variables if not present
    if "cost_view" not in st.session_state:
        st.session_state.cost_view = "list"
    
    if "selected_budget_id" not in st.session_state:
        st.session_state.selected_budget_id = None
    
    if "edit_budget_id" not in st.session_state:
        st.session_state.edit_budget_id = None
    
    # Tab navigation for cost management sections
    tab1, tab2, tab3 = st.tabs(["Budget", "Change Orders", "Forecasting"])
    
    # Budget Tab
    with tab1:
        # Get current view from session state
        current_view = st.session_state.cost_view
        
        # Add navigation buttons at the top for non-list views
        if current_view != "list":
            # Back button at the top of any non-list view
            if st.button("← Back to Budget List", key="back_to_budget_list"):
                st.session_state.cost_view = "list"
                st.rerun()
        
        # Render the appropriate view based on session state
        if current_view == "list":
            render_budget_list()
        elif current_view == "view":
            render_budget_details()
        elif current_view == "edit":
            render_budget_form(is_edit=True)
        elif current_view == "add":
            render_budget_form(is_edit=False)
        elif current_view == "analysis":
            render_budget_analysis()
    
    # Change Orders Tab
    with tab2:
        st.write("Change Orders module (Coming Soon)")
    
    # Forecasting Tab
    with tab3:
        st.write("Forecasting module (Coming Soon)")