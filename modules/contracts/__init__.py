"""
Contracts module for the gcPanel Construction Management Dashboard.

This module provides contract management functionality including contract tracking,
change orders, payment applications, and subcontractor management.

This module follows a clear CRUD pattern with:
1. List views for viewing all records with filtering/searching/sorting
2. Detail views for viewing individual records with Edit buttons
3. Add/Edit forms for creating and updating records
4. Analysis views for data visualization and metrics
"""

import streamlit as st
from modules.contracts.components.contract_components import (
    render_contract_list, 
    render_contract_details, 
    render_contract_form, 
    render_contract_analysis
)

def render_contracts():
    """Render the contracts module"""
    
    # Header
    st.title("Contract Management")
    
    # Add debug checkbox to help troubleshooting
    if st.checkbox("🔍 Debug state", value=False, key="contract_debug_state"):
        st.write(f"Current contract view: {st.session_state.get('contract_view')}")
        st.write(f"Selected contract ID: {st.session_state.get('selected_contract_id')}")
        st.write(f"Edit contract ID: {st.session_state.get('edit_contract_id')}")
    
    # Initialize session state variables if not present
    if "contract_view" not in st.session_state:
        st.session_state.contract_view = "list"
    
    if "selected_contract_id" not in st.session_state:
        st.session_state.selected_contract_id = None
    
    if "edit_contract_id" not in st.session_state:
        st.session_state.edit_contract_id = None
    
    # Tab navigation for contract management sections
    tab1, tab2, tab3 = st.tabs(["Prime Contracts", "Subcontracts", "Change Orders"])
    
    # Prime Contracts Tab
    with tab1:
        # Get current view from session state
        current_view = st.session_state.contract_view
        
        # Add navigation buttons at the top for non-list views
        if current_view != "list":
            # Back button at the top of any non-list view
            if st.button("← Back to Contracts List", key="back_to_contract_list"):
                st.session_state.contract_view = "list"
                st.rerun()
        
        # Render the appropriate view based on session state
        if current_view == "list":
            render_contract_list()
        elif current_view == "view":
            render_contract_details()
        elif current_view == "edit":
            render_contract_form(is_edit=True)
        elif current_view == "add":
            render_contract_form(is_edit=False)
        elif current_view == "analysis":
            render_contract_analysis()
    
    # Subcontracts Tab
    with tab2:
        st.write("Subcontracts module (Coming Soon)")
    
    # Change Orders Tab
    with tab3:
        st.write("Change Orders module (Coming Soon)")