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
from modules.engineering.components.submittal_components import (
    render_submittal_list,
    render_submittal_details,
    render_submittal_form,
    render_submittal_analysis
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
        st.write(f"Current Submittal view: {st.session_state.get('submittal_view')}")
        st.write(f"Selected Submittal ID: {st.session_state.get('selected_submittal_id')}")
        st.write(f"Edit Submittal ID: {st.session_state.get('edit_submittal_id')}")
    
    # Initialize session state variables for RFIs if not present
    if "rfi_view" not in st.session_state:
        st.session_state.rfi_view = "list"
    
    if "selected_rfi_id" not in st.session_state:
        st.session_state.selected_rfi_id = None
    
    if "edit_rfi_id" not in st.session_state:
        st.session_state.edit_rfi_id = None
    
    # Initialize session state variables for Submittals if not present
    if "submittal_view" not in st.session_state:
        st.session_state.submittal_view = "list"
    
    if "selected_submittal_id" not in st.session_state:
        st.session_state.selected_submittal_id = None
    
    if "edit_submittal_id" not in st.session_state:
        st.session_state.edit_submittal_id = None
    
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
        # Get current view from session state
        current_view = st.session_state.submittal_view
        
        # Add navigation buttons at the top for non-list views
        if current_view != "list":
            # Back button at the top of any non-list view
            if st.button("← Back to Submittal List", key="back_to_submittal_list"):
                st.session_state.submittal_view = "list"
                st.rerun()
        
        # Render the appropriate view based on session state
        if current_view == "list":
            render_submittal_list()
        elif current_view == "view":
            render_submittal_details()
        elif current_view == "edit":
            render_submittal_form(is_edit=True)
        elif current_view == "add":
            render_submittal_form(is_edit=False)
        elif current_view == "analysis":
            render_submittal_analysis()
    
    # Document Library Tab
    with tab3:
        st.write("Document Library module (Coming Soon)")