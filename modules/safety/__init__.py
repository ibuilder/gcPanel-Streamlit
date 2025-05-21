"""
Safety Module for gcPanel Construction Management Dashboard.

This module provides comprehensive safety management functionality
with incident tracking, inspections, toolbox talks, and hazard management.
"""

import streamlit as st
from datetime import datetime
from modules.safety.service import SafetyService

def render_safety():
    """Render the safety management module."""
    # Initialize the service
    SafetyService.initialize_data_files()
    
    # Render the main UI
    st.title("Safety Management")
    
    # Create tabs for different safety components
    tabs = st.tabs(["Incidents", "Inspections", "Toolbox Talks", "Hazards", "Analytics"])
    
    # Render each tab content
    with tabs[0]:
        render_incidents()
    
    with tabs[1]:
        render_inspections()
    
    with tabs[2]:
        render_toolbox_talks()
        
    with tabs[3]:
        render_hazards()
        
    with tabs[4]:
        render_safety_analytics()

def render_incidents():
    """Render the incidents management UI."""
    st.header("Safety Incidents")
    
    # Get incident data
    incidents = SafetyService.get_incidents()
    
    # Initialize session state for incident management
    if "incident_view" not in st.session_state:
        st.session_state.incident_view = "list"
    if "selected_incident_id" not in st.session_state:
        st.session_state.selected_incident_id = None
    
    # Show appropriate view based on state
    if st.session_state.incident_view == "list":
        # Add search and filter options
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_term = st.text_input("Search Incidents", placeholder="Search by ID, location, or description...")
        
        with col2:
            status_options = ["All"] + sorted(list(set(i.get("status", "") for i in incidents)))
            status_filter = st.selectbox("Status", options=status_options)
        
        with col3:
            # Add a create button
            if st.button("+ New Incident"):
                st.session_state.incident_view = "create"
                st.rerun()
        
        # Filter incidents
        filtered_incidents = incidents
        
        if search_term:
            search_term = search_term.lower()
            filtered_incidents = [i for i in filtered_incidents if
                                search_term in i.get("id", "").lower() or
                                search_term in i.get("location", "").lower() or
                                search_term in i.get("description", "").lower()]
        
        if status_filter and status_filter != "All":
            filtered_incidents = [i for i in filtered_incidents if i.get("status") == status_filter]
        
        # Display incidents
        if filtered_incidents:
            for incident in filtered_incidents:
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
                    
                    with col1:
                        st.write(f"**ID:** {incident.get('id')}")
                        st.write(f"**Date:** {incident.get('date')}")
                    
                    with col2:
                        st.write(f"**Type:** {incident.get('type')}")
                        st.write(f"**Location:** {incident.get('location')}")
                    
                    with col3:
                        severity = incident.get('severity', 'Unknown')
                        severity_color = {
                            'Low': 'green',
                            'Medium': 'orange',
                            'High': 'red'
                        }.get(severity, 'gray')
                        
                        st.write(f"**Severity:** <span style='color:{severity_color};'>{severity}</span>", unsafe_allow_html=True)
                        st.write(f"**Status:** {incident.get('status')}")
                    
                    with col4:
                        st.button("View", key=f"view_{incident.get('id')}", 
                                  on_click=lambda id=incident.get('id'): set_incident_view("detail", id))
                        st.button("Edit", key=f"edit_{incident.get('id')}", 
                                  on_click=lambda id=incident.get('id'): set_incident_view("edit", id))
                
                st.markdown("---")
        else:
            st.info("No incidents found matching your criteria.")
    
    elif st.session_state.incident_view == "create":
        render_incident_form()
    
    elif st.session_state.incident_view == "edit":
        # Load the selected incident
        incident = SafetyService.get_incident(st.session_state.selected_incident_id)
        if incident:
            render_incident_form(incident)
        else:
            st.error("Selected incident not found.")
            st.session_state.incident_view = "list"
            st.rerun()
    
    elif st.session_state.incident_view == "detail":
        # Load the selected incident
        incident = SafetyService.get_incident(st.session_state.selected_incident_id)
        if incident:
            render_incident_detail(incident)
        else:
            st.error("Selected incident not found.")
            st.session_state.incident_view = "list"
            st.rerun()

def set_incident_view(view, incident_id=None):
    """
    Set the incident view and optionally the selected incident.
    
    Args:
        view (str): The view to set ('list', 'create', 'edit', 'detail')
        incident_id (str, optional): The ID of the selected incident
    """
    st.session_state.incident_view = view
    if incident_id:
        st.session_state.selected_incident_id = incident_id

def render_incident_form(incident=None):
    """
    Render a form for creating or editing an incident.
    
    Args:
        incident (dict, optional): Existing incident data for editing
    """
    is_edit = incident is not None
    form_title = "Edit Incident" if is_edit else "Create New Incident"
    
    st.header(form_title)
    
    # Back button
    if st.button("← Back to List"):
        st.session_state.incident_view = "list"
        st.rerun()
    
    with st.form("incident_form"):
        # Basic information
        col1, col2 = st.columns(2)
        
        with col1:
            if is_edit:
                st.text_input("Incident ID", value=incident.get("id", ""), disabled=True)
            
            incident_date = st.date_input(
                "Date",
                value=datetime.strptime(incident.get("date", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d") if is_edit else None
            )
            
            incident_type = st.selectbox(
                "Incident Type",
                ["Near Miss", "Injury", "Property Damage", "Environmental", "Other"],
                index=["Near Miss", "Injury", "Property Damage", "Environmental", "Other"].index(incident.get("type")) if is_edit and incident.get("type") else 0
            )
        
        with col2:
            status = st.selectbox(
                "Status",
                ["Open", "In Progress", "Closed"],
                index=["Open", "In Progress", "Closed"].index(incident.get("status")) if is_edit and incident.get("status") else 0
            )
            
            severity = st.selectbox(
                "Severity",
                ["Low", "Medium", "High"],
                index=["Low", "Medium", "High"].index(incident.get("severity")) if is_edit and incident.get("severity") else 0
            )
            
            location = st.text_input("Location", value=incident.get("location", "") if is_edit else "")
        
        # Description and details
        description = st.text_area(
            "Description",
            value=incident.get("description", "") if is_edit else "",
            height=100
        )
        
        reported_by = st.text_input(
            "Reported By",
            value=incident.get("reported_by", "") if is_edit else ""
        )
        
        # Witnesses
        witnesses_str = ", ".join(incident.get("witnesses", [])) if is_edit else ""
        witnesses = st.text_input(
            "Witnesses (comma-separated)",
            value=witnesses_str
        )
        
        # Corrective action
        corrective_action = st.text_area(
            "Corrective Action",
            value=incident.get("corrective_action", "") if is_edit else "",
            height=100
        )
        
        # File upload for photos
        st.file_uploader("Upload Photos", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
        
        # Submit buttons
        col1, col2, col3 = st.columns([1, 1, 3])
        
        with col1:
            submit_button = st.form_submit_button("Save Incident")
        
        with col2:
            cancel_button = st.form_submit_button("Cancel")
    
    # Handle form submission
    if submit_button:
        # Validate required fields
        if not location:
            st.error("Location is required.")
            return
            
        if not description:
            st.error("Description is required.")
            return
        
        # Prepare incident data
        incident_data = {
            "date": incident_date.strftime("%Y-%m-%d"),
            "status": status,
            "type": incident_type,
            "location": location,
            "description": description,
            "reported_by": reported_by,
            "severity": severity,
            "corrective_action": corrective_action,
            "witnesses": [w.strip() for w in witnesses.split(",")] if witnesses else [],
            "photos": []  # We would handle photo uploads here in a real implementation
        }
        
        # Save the incident
        if is_edit:
            SafetyService.update_incident(incident.get("id"), incident_data)
            st.success("Incident updated successfully!")
        else:
            SafetyService.create_incident(incident_data)
            st.success("Incident created successfully!")
        
        # Return to list view
        st.session_state.incident_view = "list"
        st.rerun()
    
    if cancel_button:
        # Return to list view
        st.session_state.incident_view = "list"
        st.rerun()

def render_incident_detail(incident):
    """
    Render detailed view of an incident.
    
    Args:
        incident (dict): The incident data to display
    """
    st.header(f"Incident: {incident.get('id')}")
    
    # Back button
    if st.button("← Back to List"):
        st.session_state.incident_view = "list"
        st.rerun()
    
    # Display incident details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Date:** {incident.get('date')}")
        st.markdown(f"**Type:** {incident.get('type')}")
        st.markdown(f"**Location:** {incident.get('location')}")
        st.markdown(f"**Reported By:** {incident.get('reported_by')}")
    
    with col2:
        severity = incident.get('severity', 'Unknown')
        severity_color = {
            'Low': 'green',
            'Medium': 'orange',
            'High': 'red'
        }.get(severity, 'gray')
        
        st.markdown(f"**Severity:** <span style='color:{severity_color};'>{severity}</span>", unsafe_allow_html=True)
        st.markdown(f"**Status:** {incident.get('status')}")
        st.markdown(f"**Witnesses:** {', '.join(incident.get('witnesses', []))}")
    
    # Description and corrective action
    st.subheader("Description")
    st.write(incident.get("description", "No description provided."))
    
    st.subheader("Corrective Action")
    st.write(incident.get("corrective_action", "No corrective action provided."))
    
    # Photos
    st.subheader("Photos")
    if incident.get("photos"):
        # Display photos
        photo_cols = st.columns(3)
        for i, photo in enumerate(incident.get("photos", [])):
            with photo_cols[i % 3]:
                st.image(photo)
    else:
        st.info("No photos available.")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Edit Incident"):
            st.session_state.incident_view = "edit"
            st.rerun()
    
    with col2:
        if incident.get("status") != "Closed":
            if st.button("Mark as Closed"):
                # Update status
                incident["status"] = "Closed"
                SafetyService.update_incident(incident.get("id"), incident)
                st.success("Incident marked as closed.")
                st.rerun()
    
    with col3:
        if st.button("Delete Incident"):
            # Show confirmation
            st.warning("Are you sure you want to delete this incident?")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Yes, Delete"):
                    SafetyService.delete_incident(incident.get("id"))
                    st.success("Incident deleted successfully!")
                    st.session_state.incident_view = "list"
                    st.rerun()
            
            with col2:
                if st.button("Cancel"):
                    st.rerun()

def render_inspections():
    """Render the inspections management UI."""
    st.header("Safety Inspections")
    
    # Here you would implement similar functionality as for incidents
    st.info("Inspections module is under development. Coming soon!")

def render_toolbox_talks():
    """Render the toolbox talks management UI."""
    st.header("Toolbox Talks")
    
    # Here you would implement similar functionality as for incidents
    st.info("Toolbox Talks module is under development. Coming soon!")

def render_hazards():
    """Render the hazards management UI."""
    st.header("Hazard Management")
    
    # Here you would implement similar functionality as for incidents
    st.info("Hazard Management module is under development. Coming soon!")

def render_safety_analytics():
    """Render safety analytics dashboard."""
    st.header("Safety Analytics")
    
    # Sample metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Incidents YTD", "7")
    
    with col2:
        st.metric("Days Since Last Incident", "24", "+5")
    
    with col3:
        st.metric("Inspection Score", "92%", "+3%")
    
    with col4:
        st.metric("Open Hazards", "3", "-2")
    
    # Incident trends chart
    st.subheader("Incident Trends")
    
    # Here you would add an actual chart with Plotly or similar
    # For now, just display a placeholder
    st.info("Incident trends chart will be displayed here.")
    
    # Safety scores by area
    st.subheader("Safety Scores by Area")
    
    # Here you would add an actual chart with Plotly or similar
    # For now, just display a placeholder
    st.info("Safety scores chart will be displayed here.")