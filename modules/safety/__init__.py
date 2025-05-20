"""
Safety module for the gcPanel Construction Management Dashboard.

This module provides safety management features including incident tracking,
safety inspections, safety metrics visualization, and gamified safety badges. 

This module follows a clear CRUD pattern with:
1. List views for viewing all records with filtering/searching/sorting
2. Detail views for viewing individual records with Edit buttons
3. Add/Edit forms for creating and updating records
4. Analysis views for data visualization and metrics
"""

import streamlit as st
from modules.safety.incident_components import (
    render_incident_list, 
    render_incident_details, 
    render_incident_form, 
    render_incidents_analysis
)
from modules.safety.badges import render_badges

def render_safety():
    """Render the safety module"""
    
    # Header
    st.title("Safety Management")
    
    # Debug information to track navigation
    if st.checkbox("🐛 Show Debug Info", value=False, key="show_debug"):
        st.write(f"Current view: {st.session_state.get('safety_view', 'not set')}")
        st.write(f"Selected incident ID: {st.session_state.get('selected_incident_id', 'none')}")
        st.write(f"Edit incident ID: {st.session_state.get('edit_incident_id', 'none')}")
        st.write(f"View query params: {dict(st.query_params)}")
    
    # Hard-coded URI parameters for direct navigation
    if "view" in st.query_params:
        st.session_state.safety_view = st.query_params["view"]
    if "incident_id" in st.query_params:
        st.session_state.selected_incident_id = st.query_params["incident_id"]
        st.session_state.edit_incident_id = st.query_params["incident_id"]
    
    # Make sure session state variables are initialized
    if "safety_view" not in st.session_state:
        st.session_state.safety_view = "list"
    
    if "selected_incident_id" not in st.session_state:
        st.session_state.selected_incident_id = None
    
    # Tab navigation for safety sections - main module categories
    tab1, tab2, tab3, tab4 = st.tabs(["Incidents", "Inspections", "Training", "Safety Badges"])
    
    # Incidents Tab
    with tab1:
        # For debugging: Print what the current view should be
        if st.checkbox("🔍 Debug state", value=False, key="debug_state"):
            st.write(f"Current safety view: {st.session_state.get('safety_view')}")
            st.write(f"Selected incident ID: {st.session_state.get('selected_incident_id')}")
            st.write(f"Edit incident ID: {st.session_state.get('edit_incident_id')}")
        
        # Get current view from session state
        current_view = st.session_state.safety_view
        
        # Add navigation buttons at the top
        if current_view != "list":
            # Back button at the top of any non-list view
            if st.button("← Back to Incidents List", key="top_back_to_list", use_container_width=True):
                st.session_state.safety_view = "list"
                st.session_state.selected_incident_id = None
                st.rerun()
        else:
            # Action buttons at the top of the list view
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➕ Add Incident", key="add_incident_btn", type="primary", use_container_width=True):
                    st.session_state.safety_view = "add"
                    st.rerun()
                    
            with col2:
                if st.button("📊 View Analysis", key="view_analysis", use_container_width=True):
                    st.session_state.safety_view = "analysis"
                    st.rerun()
        
        # Render the appropriate view
        if current_view == "list":
            # Show list view with incidents table
            st.info("Click on an incident title below to view detailed information")
            render_incident_list()
            
        elif current_view == "view":
            # Show detailed view of a specific incident
            render_incident_details()
            
        elif current_view == "add" or current_view == "edit":
            # Show add/edit form
            is_edit = (current_view == "edit")
            render_incident_form(is_edit=is_edit)
            
        elif current_view == "analysis":
            # Show analysis charts and metrics
            render_incidents_analysis()
    
    # Inspections Tab - Placeholder for similar CRUD structure as above
    with tab2:
        st.info("Inspections module will use the same CRUD pattern as Incidents")
        st.write("This module will include:")
        st.markdown("""
        - **List View**: Table of all inspections with filtering and sorting
        - **View Record**: Detailed view of a single inspection record
        - **Add/Edit**: Form for creating and updating inspection records
        - **Analysis**: Charts and metrics for inspection data analysis
        """)
    
    # Training Tab - Placeholder for similar CRUD structure as above
    with tab3:
        st.info("Training module will use the same CRUD pattern as Incidents")
        st.write("This module will include:")
        st.markdown("""
        - **List View**: Table of all training records with filtering and sorting
        - **View Record**: Detailed view of a single training record
        - **Add/Edit**: Form for creating and updating training records
        - **Analysis**: Charts and metrics for training data analysis
        """)
        
    # Safety Badges Tab
    with tab4:
        render_badges()
