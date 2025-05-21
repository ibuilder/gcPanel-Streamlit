"""
BIM (Building Information Modeling) module for the gcPanel Construction Management Dashboard.

This module provides BIM visualization and management functionality including:
- 3D model viewing
- Clash detection
- Model analytics
- Issue tracking
- Element properties and metadata

This module follows a clear CRUD pattern with:
1. List views for model selection with filtering/searching
2. Detail views for viewing model metadata and properties
3. Upload/Edit forms for adding and updating models
4. Analytics dashboards for model statistics
"""

import streamlit as st
from modules.bim.components.model_viewer import (
    render_model_list,
    render_model_viewer,
    render_model_details,
    render_model_upload,
    render_model_analytics
)

def render_bim():
    """Render the BIM module"""
    
    # Header
    st.title("BIM Management")
    
    # Add debug checkbox to help troubleshooting
    if st.checkbox("🔍 Debug state", value=False, key="bim_debug_state"):
        st.write(f"Current BIM view: {st.session_state.get('bim_view')}")
        st.write(f"Selected model ID: {st.session_state.get('selected_model_id')}")
        st.write(f"Update model ID: {st.session_state.get('update_model_id')}")
    
    # Initialize session state variables if not present
    if "bim_view" not in st.session_state:
        st.session_state.bim_view = "list"
    
    if "selected_model_id" not in st.session_state:
        st.session_state.selected_model_id = None
    
    if "update_model_id" not in st.session_state:
        st.session_state.update_model_id = None
    
    # Get current view from session state
    current_view = st.session_state.bim_view
    
    # Add navigation buttons at the top for non-list views
    if current_view != "list":
        # Back button at the top of any non-list view
        if st.button("← Back to Model List", key="back_to_model_list"):
            st.session_state.bim_view = "list"
            # Clear update model ID if present
            if st.session_state.get("update_model_id"):
                st.session_state.update_model_id = None
            st.rerun()
    
    # Render the appropriate view based on session state
    if current_view == "list":
        render_model_list()
    elif current_view == "view":
        render_model_viewer()
    elif current_view == "details":
        render_model_details()
    elif current_view == "upload":
        render_model_upload()
    elif current_view == "analytics":
        render_model_analytics()