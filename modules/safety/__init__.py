"""
Safety module for the gcPanel Construction Management Dashboard.

This module provides safety management features including incident tracking,
safety inspections, and safety metrics visualization. 

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

def render_safety():
    """Render the safety module"""
    
    # Header
    st.title("Safety Management")
    
    # Tab navigation for safety sections - main module categories
    tab1, tab2, tab3 = st.tabs(["Incidents", "Inspections", "Training"])
    
    # Incidents Tab
    with tab1:
        # Initialize view state
        if "safety_view" not in st.session_state:
            st.session_state.safety_view = "list"
            
        # Check which view to show
        current_view = st.session_state.safety_view
        
        if current_view == "list":
            # Show list view with incidents table
            render_incident_list()
            
            # Add Analysis button on top of list
            if st.button("📊 View Analysis", key="view_analysis"):
                st.session_state.safety_view = "analysis"
                st.rerun()
                
        elif current_view == "view":
            # Show detailed view of a specific incident
            render_incident_details()
            
            # Back button to return to list
            if st.button("← Back to List", key="back_to_list"):
                st.session_state.safety_view = "list"
                st.rerun()
                
        elif current_view == "add" or current_view == "edit":
            # Show add/edit form
            is_edit = (current_view == "edit")
            render_incident_form(is_edit=is_edit)
            
            # Back button is handled in the form component
            
        elif current_view == "analysis":
            # Show analysis charts and metrics
            render_incidents_analysis()
            
            # Back button to return to list
            if st.button("← Back to List", key="back_to_list_from_analysis"):
                st.session_state.safety_view = "list"
                st.rerun()
    
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
