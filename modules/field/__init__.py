"""
Field module for the gcPanel Construction Management Dashboard.

This module provides field operations management functionality including daily reports, 
photo logs, quality control, and field inspections.

This module follows a clear CRUD pattern with:
1. List views for viewing all records with filtering/searching/sorting
2. Detail views for viewing individual records with Edit buttons
3. Add/Edit forms for creating and updating records
4. Analysis views for data visualization and metrics
"""

import streamlit as st
from modules.field.components.daily_report_components import (
    render_daily_report_list, 
    render_daily_report_details, 
    render_daily_report_form, 
    render_daily_report_analysis
)

def render_field():
    """Render the field operations module"""
    
    # Header
    st.title("Field Operations")
    
    # Add debug checkbox to help troubleshooting
    if st.checkbox("🔍 Debug state", value=False, key="field_debug_state"):
        st.write(f"Current daily report view: {st.session_state.get('daily_report_view')}")
        st.write(f"Selected daily report ID: {st.session_state.get('selected_daily_report_id')}")
        st.write(f"Edit daily report ID: {st.session_state.get('edit_daily_report_id')}")
    
    # Initialize session state variables if not present
    if "daily_report_view" not in st.session_state:
        st.session_state.daily_report_view = "list"
    
    if "selected_daily_report_id" not in st.session_state:
        st.session_state.selected_daily_report_id = None
    
    if "edit_daily_report_id" not in st.session_state:
        st.session_state.edit_daily_report_id = None
    
    # Tab navigation for field operations sections
    tab1, tab2, tab3 = st.tabs(["Daily Reports", "Photo Log", "Field Inspections"])
    
    # Daily Reports Tab
    with tab1:
        # Get current view from session state
        current_view = st.session_state.daily_report_view
        
        # Add navigation buttons at the top for non-list views
        if current_view != "list":
            # Back button at the top of any non-list view
            if st.button("← Back to Daily Reports List", key="back_to_daily_report_list"):
                st.session_state.daily_report_view = "list"
                st.rerun()
        
        # Render the appropriate view based on session state
        if current_view == "list":
            render_daily_report_list()
        elif current_view == "view":
            render_daily_report_details()
        elif current_view == "edit":
            render_daily_report_form(is_edit=True)
        elif current_view == "add":
            render_daily_report_form(is_edit=False)
        elif current_view == "analysis":
            render_daily_report_analysis()
    
    # Photo Log Tab
    with tab2:
        st.write("Photo Log module (Coming Soon)")
    
    # Field Inspections Tab
    with tab3:
        st.write("Field Inspections module (Coming Soon)")