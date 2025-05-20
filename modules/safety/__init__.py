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
        # Check if we have a tab selection in session state
        if "safety_tab_selection" not in st.session_state:
            st.session_state.safety_tab_selection = {}
            
        if "incidents" not in st.session_state.safety_tab_selection:
            st.session_state.safety_tab_selection["incidents"] = 0
            
        # Create tabs with the selected tab activated
        incident_tabs = st.tabs(["List View", "View Record", "Add/Edit", "Analysis"])
        
        # Determine which tab to show based on session state
        selected_tab = st.session_state.safety_tab_selection["incidents"]
        
        # Render the appropriate tab content
        if selected_tab == 0:  # List View
            with incident_tabs[0]:
                render_incident_list()
        elif selected_tab == 1:  # View Record
            with incident_tabs[1]:
                render_incident_details()
        elif selected_tab == 2:  # Add/Edit
            with incident_tabs[2]:
                # Check if we're editing an existing record
                if "edit_incident_id" in st.session_state and st.session_state.edit_incident_id:
                    render_incident_form(is_edit=True)
                else:
                    render_incident_form(is_edit=False)
        elif selected_tab == 3:  # Analysis
            with incident_tabs[3]:
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
