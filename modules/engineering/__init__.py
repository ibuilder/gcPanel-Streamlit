"""
Engineering module for the gcPanel Construction Management Dashboard.

This module provides engineering management functionality including RFIs (Requests for Information),
submittals, document management, and technical data analysis.

This module follows a clear CRUD pattern with:
1. List views for viewing all records with filtering/searching/sorting
2. Detail views for viewing individual records with Edit buttons
3. Add/Edit forms for creating and updating records
4. Analysis views for data visualization and metrics
"""

import streamlit as st
from modules.engineering.components.rfi_components import (
    render_rfi_list, 
    render_rfi_details, 
    render_rfi_form, 
    render_rfi_analysis
)

def render_engineering():
    """Render the engineering module"""
    
    # Header
    st.title("Engineering Management")
    
    # Add debug checkbox to help troubleshooting
    if st.checkbox("🔍 Debug state", value=False, key="engineering_debug_state"):
        st.write(f"Current RFI view: {st.session_state.get('rfi_view')}")
        st.write(f"Selected RFI ID: {st.session_state.get('selected_rfi_id')}")
        st.write(f"Edit RFI ID: {st.session_state.get('edit_rfi_id')}")
    
    # Initialize session state variables if not present
    if "rfi_view" not in st.session_state:
        st.session_state.rfi_view = "list"
    
    if "selected_rfi_id" not in st.session_state:
        st.session_state.selected_rfi_id = None
    
    if "edit_rfi_id" not in st.session_state:
        st.session_state.edit_rfi_id = None
    
    # Tab navigation for engineering management sections
    tab1, tab2, tab3 = st.tabs(["RFIs", "Submittals", "Document Library"])
    
    # RFIs Tab
    with tab1:
        # Get current view from session state
        current_view = st.session_state.rfi_view
        
        # Add navigation buttons at the top for non-list views
        if current_view != "list":
            # Back button at the top of any non-list view
            if st.button("← Back to RFI List", key="back_to_rfi_list"):
                st.session_state.rfi_view = "list"
                st.rerun()
        
        # Render the appropriate view based on session state
        if current_view == "list":
            render_rfi_list()
        elif current_view == "view":
            render_rfi_details()
        elif current_view == "edit":
            render_rfi_form(is_edit=True)
        elif current_view == "add":
            render_rfi_form(is_edit=False)
        elif current_view == "analysis":
            render_rfi_analysis()
    
    # Submittals Tab
    with tab2:
        st.write("Submittals module (Coming Soon)")
    
    # Document Library Tab
    with tab3:
        st.write("Document Library module (Coming Soon)")