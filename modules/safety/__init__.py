"""
Safety Module for gcPanel Construction Management Dashboard.

This module provides comprehensive safety management functionality
with incident tracking, inspections, toolbox talks, and hazard management.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from modules.safety.service import SafetyService
from assets.safety_styles import apply_safety_styles

def render_safety():
    """Render the safety management module."""
    # Initialize the service
    SafetyService.initialize_data_files()
    
    # Apply custom styles to improve layout
    apply_safety_styles()
    
    # Render the main UI with enhanced header
    st.markdown('<h1 class="safety-header">Safety Management</h1>', unsafe_allow_html=True)
    
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
    
    # Get inspection data
    inspections = SafetyService.get_inspections()
    
    # Initialize session state for inspection management
    if "inspection_view" not in st.session_state:
        st.session_state.inspection_view = "list"
    if "selected_inspection_id" not in st.session_state:
        st.session_state.selected_inspection_id = None
    
    # Show appropriate view based on state
    if st.session_state.inspection_view == "list":
        # Add search and filter options
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_term = st.text_input("Search Inspections", placeholder="Search by ID, location, or type...", key="inspection_search")
        
        with col2:
            inspection_types = ["All Types"] + sorted(list(set(i.get("type", "") for i in inspections)))
            type_filter = st.selectbox("Inspection Type", options=inspection_types, key="inspection_type_filter")
        
        with col3:
            # Add a create button
            if st.button("+ New Inspection", key="new_inspection_btn"):
                st.session_state.inspection_view = "create"
                st.rerun()
        
        # Filter inspections
        filtered_inspections = inspections
        
        if search_term:
            search_term = search_term.lower()
            filtered_inspections = [i for i in filtered_inspections if
                                search_term in i.get("id", "").lower() or
                                search_term in i.get("location", "").lower() or
                                search_term in i.get("type", "").lower()]
        
        if type_filter and type_filter != "All Types":
            filtered_inspections = [i for i in filtered_inspections if i.get("type") == type_filter]
        
        # Display inspections
        if filtered_inspections:
            # Create a table of inspections
            inspection_data = {
                "ID": [i.get("id", "") for i in filtered_inspections],
                "Date": [i.get("date", "") for i in filtered_inspections],
                "Type": [i.get("type", "") for i in filtered_inspections],
                "Location": [i.get("location", "") for i in filtered_inspections],
                "Score": [f"{i.get('score', 0)}%" for i in filtered_inspections],
                "Status": [i.get("status", "") for i in filtered_inspections]
            }
            
            df = pd.DataFrame(inspection_data)
            
            # Use a CSS selector for hover effect and clickable rows
            st.markdown("""
            <style>
            .inspection-row:hover {
                background-color: rgba(0, 0, 0, 0.05);
                cursor: pointer;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Display the table
            st.dataframe(df, hide_index=True, use_container_width=True)
            
            # Selection for actions
            selected_id = st.selectbox("Select an inspection to perform actions:", 
                                      options=inspection_data["ID"],
                                      label_visibility="collapsed")
            
            # Action buttons for the selected inspection
            if selected_id:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("View Details", key=f"view_inspection_{selected_id}"):
                        st.session_state.selected_inspection_id = selected_id
                        st.session_state.inspection_view = "detail"
                        st.rerun()
                
                with col2:
                    if st.button("Edit", key=f"edit_inspection_{selected_id}"):
                        st.session_state.selected_inspection_id = selected_id
                        st.session_state.inspection_view = "edit"
                        st.rerun()
                
                with col3:
                    if st.button("Delete", key=f"delete_inspection_{selected_id}"):
                        # Confirm deletion
                        st.warning(f"Are you sure you want to delete inspection {selected_id}?")
                        
                        confirm_col1, confirm_col2 = st.columns(2)
                        with confirm_col1:
                            if st.button("Yes, Delete", key=f"confirm_delete_inspection"):
                                # Implement deletion logic here
                                st.success(f"Inspection {selected_id} deleted successfully.")
                                st.rerun()
                        
                        with confirm_col2:
                            if st.button("Cancel", key=f"cancel_delete_inspection"):
                                st.rerun()
        else:
            st.info("No inspections found matching your criteria.")
    
    elif st.session_state.inspection_view == "create":
        render_inspection_form()
    
    elif st.session_state.inspection_view == "edit":
        # Get the selected inspection
        inspection = next((i for i in inspections if i.get("id") == st.session_state.selected_inspection_id), None)
        
        if inspection:
            render_inspection_form(inspection)
        else:
            st.error("Selected inspection not found.")
            st.session_state.inspection_view = "list"
            st.rerun()
    
    elif st.session_state.inspection_view == "detail":
        # Get the selected inspection
        inspection = next((i for i in inspections if i.get("id") == st.session_state.selected_inspection_id), None)
        
        if inspection:
            render_inspection_detail(inspection)
        else:
            st.error("Selected inspection not found.")
            st.session_state.inspection_view = "list"
            st.rerun()

def render_inspection_form(inspection=None):
    """
    Render a form for creating or editing an inspection.
    
    Args:
        inspection (dict, optional): Existing inspection data for editing
    """
    is_edit = inspection is not None
    form_title = "Edit Inspection" if is_edit else "Create New Inspection"
    
    st.header(form_title)
    
    # Back button
    if st.button("← Back to List", key="back_to_inspection_list"):
        st.session_state.inspection_view = "list"
        st.rerun()
    
    with st.form("inspection_form"):
        # Basic information
        col1, col2 = st.columns(2)
        
        with col1:
            if is_edit:
                st.text_input("Inspection ID", value=inspection.get("id", ""), disabled=True, key="inspection_id")
            
            inspection_date = st.date_input(
                "Date",
                value=datetime.strptime(inspection.get("date", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d") if is_edit else datetime.now(),
                key="inspection_date"
            )
            
            inspection_type = st.selectbox(
                "Inspection Type",
                ["Weekly Site Inspection", "Monthly Equipment Inspection", "Safety Audit", "Pre-task Hazard Assessment", "Other"],
                index=["Weekly Site Inspection", "Monthly Equipment Inspection", "Safety Audit", "Pre-task Hazard Assessment", "Other"].index(inspection.get("type")) if is_edit and inspection.get("type") in ["Weekly Site Inspection", "Monthly Equipment Inspection", "Safety Audit", "Pre-task Hazard Assessment", "Other"] else 0,
                key="inspection_type"
            )
        
        with col2:
            status = st.selectbox(
                "Status",
                ["Scheduled", "In Progress", "Completed"],
                index=["Scheduled", "In Progress", "Completed"].index(inspection.get("status")) if is_edit and inspection.get("status") in ["Scheduled", "In Progress", "Completed"] else 0,
                key="inspection_status"
            )
            
            location = st.text_input("Location", value=inspection.get("location", "") if is_edit else "", key="inspection_location")
            
            inspector = st.text_input("Inspector", value=inspection.get("inspector", "") if is_edit else "", key="inspection_inspector")
        
        # Findings
        st.subheader("Inspection Items")
        
        # Initialize findings in session state if not present
        if "inspection_findings" not in st.session_state:
            if is_edit and "findings" in inspection:
                st.session_state.inspection_findings = inspection["findings"]
            else:
                st.session_state.inspection_findings = [
                    {"item": "", "status": "Compliant", "notes": ""}
                ]
        
        # Display the findings items
        for i, finding in enumerate(st.session_state.inspection_findings):
            cols = st.columns([3, 2, 5])
            
            with cols[0]:
                item = st.text_input(f"Item #{i+1}", value=finding.get("item", ""), key=f"finding_item_{i}")
                st.session_state.inspection_findings[i]["item"] = item
            
            with cols[1]:
                status = st.selectbox(
                    f"Status #{i+1}",
                    ["Compliant", "Non-compliant", "Partially compliant", "N/A"],
                    index=["Compliant", "Non-compliant", "Partially compliant", "N/A"].index(finding.get("status")) if finding.get("status") in ["Compliant", "Non-compliant", "Partially compliant", "N/A"] else 0,
                    key=f"finding_status_{i}"
                )
                st.session_state.inspection_findings[i]["status"] = status
            
            with cols[2]:
                notes = st.text_input(f"Notes #{i+1}", value=finding.get("notes", ""), key=f"finding_notes_{i}")
                st.session_state.inspection_findings[i]["notes"] = notes
        
        # Add/remove finding buttons
        col1, col2 = st.columns(2)
        with col1:
            add_finding = st.form_submit_button("+ Add Item")
        with col2:
            remove_finding = st.form_submit_button("- Remove Last Item")
        
        # Overall score
        score = st.slider(
            "Overall Inspection Score (%)",
            min_value=0,
            max_value=100,
            value=inspection.get("score", 85) if is_edit else 85,
            key="inspection_score"
        )
        
        # Submit buttons
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("Save Inspection")
        with col2:
            cancel_button = st.form_submit_button("Cancel")
    
    # Handle add/remove finding buttons
    if add_finding:
        st.session_state.inspection_findings.append({"item": "", "status": "Compliant", "notes": ""})
        st.rerun()
    
    if remove_finding and len(st.session_state.inspection_findings) > 1:
        st.session_state.inspection_findings.pop()
        st.rerun()
    
    # Handle form submission
    if submit_button:
        # Validate required fields
        if not location:
            st.error("Location is required.")
            return
        
        if not inspector:
            st.error("Inspector is required.")
            return
        
        # Prepare inspection data
        inspection_data = {
            "date": inspection_date.strftime("%Y-%m-%d"),
            "type": inspection_type,
            "location": location,
            "inspector": inspector,
            "status": status,
            "findings": st.session_state.inspection_findings,
            "score": score
        }
        
        # Save the inspection
        if is_edit:
            # Update existing inspection
            inspection_data["id"] = inspection["id"]
            st.success("Inspection updated successfully!")
        else:
            # Create new inspection
            st.success("Inspection created successfully!")
        
        # Clear session state for findings
        if "inspection_findings" in st.session_state:
            del st.session_state.inspection_findings
        
        # Return to list view
        st.session_state.inspection_view = "list"
        st.rerun()
    
    if cancel_button:
        # Clear session state for findings
        if "inspection_findings" in st.session_state:
            del st.session_state.inspection_findings
            
        # Return to list view
        st.session_state.inspection_view = "list"
        st.rerun()

def render_inspection_detail(inspection):
    """
    Render detailed view of an inspection.
    
    Args:
        inspection (dict): The inspection data to display
    """
    st.header(f"Inspection: {inspection.get('id')}")
    
    # Back button
    if st.button("← Back to List", key="back_to_inspection_list_from_detail"):
        st.session_state.inspection_view = "list"
        st.rerun()
    
    # Display inspection information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Date:** {inspection.get('date')}")
        st.markdown(f"**Type:** {inspection.get('type')}")
        st.markdown(f"**Location:** {inspection.get('location')}")
    
    with col2:
        st.markdown(f"**Inspector:** {inspection.get('inspector')}")
        st.markdown(f"**Status:** {inspection.get('status')}")
        
        # Display the score with color based on value
        score = inspection.get('score', 0)
        score_color = "green" if score >= 85 else "orange" if score >= 70 else "red"
        st.markdown(f"**Score:** <span style='color:{score_color};'>{score}%</span>", unsafe_allow_html=True)
    
    # Display findings
    st.subheader("Inspection Items")
    
    findings = inspection.get("findings", [])
    if findings:
        # Create a table for the findings
        finding_data = {
            "Item": [f.get("item", "") for f in findings],
            "Status": [f.get("status", "") for f in findings],
            "Notes": [f.get("notes", "") for f in findings]
        }
        
        df = pd.DataFrame(finding_data)
        
        # Add custom styling for status column
        def color_status(val):
            color = ""
            if val == "Compliant":
                color = "green"
            elif val == "Non-compliant":
                color = "red"
            elif val == "Partially compliant":
                color = "orange"
            return f'color: {color}'
        
        # Display the styled dataframe
        st.dataframe(
            df.style.applymap(color_status, subset=['Status']),
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No inspection items recorded.")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Edit Inspection", key="edit_inspection_detail"):
            st.session_state.inspection_view = "edit"
            st.rerun()
    
    with col2:
        if inspection.get("status") != "Completed":
            if st.button("Mark as Completed", key="complete_inspection"):
                st.success(f"Inspection {inspection.get('id')} marked as completed.")
                st.rerun()
    
    with col3:
        if st.button("Delete Inspection", key="delete_inspection_detail"):
            st.warning(f"Are you sure you want to delete this inspection?")
            
            confirm_col1, confirm_col2 = st.columns(2)
            with confirm_col1:
                if st.button("Yes, Delete", key="confirm_delete_inspection_detail"):
                    st.success(f"Inspection {inspection.get('id')} deleted successfully.")
                    st.session_state.inspection_view = "list"
                    st.rerun()
            
            with confirm_col2:
                if st.button("Cancel", key="cancel_delete_inspection_detail"):
                    st.rerun()

def render_toolbox_talks():
    """Render the toolbox talks management UI."""
    st.header("Toolbox Talks")
    
    # Get toolbox talks data
    from modules.safety.service import TOOLBOX_TALKS_FILE
    toolbox_talks = SafetyService._load_from_file(TOOLBOX_TALKS_FILE)
    
    # Initialize session state for toolbox talks management
    if "toolbox_view" not in st.session_state:
        st.session_state.toolbox_view = "list"
    if "selected_toolbox_id" not in st.session_state:
        st.session_state.selected_toolbox_id = None
    
    # Show appropriate view based on state
    if st.session_state.toolbox_view == "list":
        # Add search and filter options
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_term = st.text_input("Search Toolbox Talks", placeholder="Search by topic or presenter...", key="toolbox_search")
        
        with col2:
            # Get unique topics for filtering
            topics = ["All Topics"] + sorted(list(set(talk.get("topic", "") for talk in toolbox_talks)))
            topic_filter = st.selectbox("Topic", options=topics, key="toolbox_topic_filter")
        
        with col3:
            # Add a create button
            if st.button("+ New Toolbox Talk", key="new_toolbox_btn"):
                st.session_state.toolbox_view = "create"
                st.rerun()
        
        # Filter toolbox talks
        filtered_talks = toolbox_talks
        
        if search_term:
            search_term = search_term.lower()
            filtered_talks = [t for t in filtered_talks if
                            search_term in t.get("topic", "").lower() or
                            search_term in t.get("presenter", "").lower()]
        
        if topic_filter and topic_filter != "All Topics":
            filtered_talks = [t for t in filtered_talks if t.get("topic") == topic_filter]
        
        # Display toolbox talks
        if filtered_talks:
            # Format the data for display
            for talk in filtered_talks:
                with st.container():
                    # Apply card styling 
                    st.markdown('<div class="safety-card">', unsafe_allow_html=True)
                    
                    # Talk header
                    st.subheader(f"{talk.get('topic', 'Untitled Talk')}")
                    
                    # Meta information in columns
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    with col1:
                        st.markdown(f"**ID:** {talk.get('id', '')}")
                        st.markdown(f"**Date:** {talk.get('date', '')}")
                    
                    with col2:
                        st.markdown(f"**Presenter:** {talk.get('presenter', '')}")
                        st.markdown(f"**Duration:** {talk.get('duration', 0)} minutes")
                    
                    with col3:
                        attendee_count = len(talk.get('attendees', []))
                        st.markdown(f"**Attendees:** {attendee_count}")
                        
                    # Talk notes as expandable
                    with st.expander("View Notes"):
                        st.write(talk.get('notes', 'No notes provided.'))
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("View Details", key=f"view_{talk.get('id')}"):
                            st.session_state.selected_toolbox_id = talk.get('id')
                            st.session_state.toolbox_view = "detail"
                            st.rerun()
                    
                    with col2:
                        if st.button("Edit", key=f"edit_{talk.get('id')}"):
                            st.session_state.selected_toolbox_id = talk.get('id')
                            st.session_state.toolbox_view = "edit"
                            st.rerun()
                    
                    with col3:
                        if st.button("Print Attendance", key=f"print_{talk.get('id')}"):
                            st.info("Attendance sheet ready for printing.")
                            # This would generate a printable attendance sheet in a real implementation
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.info("No toolbox talks found matching your criteria.")
            
    elif st.session_state.toolbox_view == "create":
        # Form for creating a new toolbox talk
        st.subheader("Schedule New Toolbox Talk")
        
        with st.form("toolbox_talk_form"):
            # Basic information
            col1, col2 = st.columns(2)
            
            with col1:
                topic = st.text_input("Topic *", key="toolbox_topic")
                date = st.date_input("Date *", key="toolbox_date")
            
            with col2:
                presenter = st.text_input("Presenter *", key="toolbox_presenter")
                duration = st.number_input("Duration (minutes)", min_value=5, max_value=120, value=30, step=5, key="toolbox_duration")
            
            # Meeting notes
            notes = st.text_area("Meeting Notes", height=150, key="toolbox_notes")
            
            # Materials
            materials = st.multiselect(
                "Training Materials",
                options=["Handouts", "Video", "Slideshow", "Equipment Demo", "Quiz"],
                key="toolbox_materials"
            )
            
            # Submit buttons
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Schedule Talk")
            with col2:
                cancel = st.form_submit_button("Cancel")
        
        # Handle form submission
        if submit:
            if not topic or not presenter:
                st.error("Please enter a topic and presenter name.")
            else:
                st.success(f"Toolbox talk on '{topic}' scheduled for {date.strftime('%Y-%m-%d')}.")
                st.session_state.toolbox_view = "list"
                st.rerun()
        
        if cancel:
            st.session_state.toolbox_view = "list"
            st.rerun()
            
    elif st.session_state.toolbox_view == "detail":
        # Get the selected toolbox talk
        talk = next((t for t in toolbox_talks if t.get("id") == st.session_state.selected_toolbox_id), None)
        
        if talk:
            # Back button
            if st.button("← Back to List", key="back_to_toolbox_list"):
                st.session_state.toolbox_view = "list"
                st.rerun()
            
            # Talk details
            st.subheader(talk.get("topic", "Untitled Talk"))
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Date:** {talk.get('date', '')}")
                st.markdown(f"**Presenter:** {talk.get('presenter', '')}")
            
            with col2:
                st.markdown(f"**Duration:** {talk.get('duration', 0)} minutes")
                st.markdown(f"**ID:** {talk.get('id', '')}")
            
            # Notes and additional information
            st.subheader("Meeting Notes")
            st.write(talk.get("notes", "No notes provided."))
            
            # Attendees
            st.subheader("Attendance")
            
            attendees = talk.get("attendees", [])
            if attendees:
                # Create attendance data for table
                attendance_data = {
                    "Name": [a.get("name", "") for a in attendees],
                    "Company": [a.get("company", "") for a in attendees],
                    "Signature": ["✓" if a.get("signature", False) else "❌" for a in attendees]
                }
                
                # Display table
                st.dataframe(pd.DataFrame(attendance_data), hide_index=True, use_container_width=True)
                
                # Attendance summary
                st.info(f"{len(attendees)} workers attended this toolbox talk.")
            else:
                st.info("No attendance records found for this toolbox talk.")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Edit Talk", key="edit_talk_detail"):
                    st.session_state.toolbox_view = "edit"
                    st.rerun()
            
            with col2:
                if st.button("Print Attendance", key="print_attendance_detail"):
                    st.success("Attendance sheet generated.")
            
            with col3:
                if st.button("Delete Talk", key="delete_talk_detail"):
                    st.warning("Are you sure you want to delete this toolbox talk?")
                    
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", key="confirm_delete_talk"):
                            st.success(f"Toolbox talk deleted successfully.")
                            st.session_state.toolbox_view = "list"
                            st.rerun()
                    
                    with confirm_col2:
                        if st.button("Cancel", key="cancel_delete_talk"):
                            st.rerun()
        else:
            st.error("Selected toolbox talk not found.")
            st.session_state.toolbox_view = "list"
            st.rerun()

def render_hazards():
    """Render the hazards management UI."""
    st.header("Hazard Management")
    
    # Get hazards data
    from modules.safety.service import HAZARDS_FILE
    hazards = SafetyService._load_from_file(HAZARDS_FILE)
    
    # Initialize session state for hazard management
    if "hazard_view" not in st.session_state:
        st.session_state.hazard_view = "list"
    if "selected_hazard_id" not in st.session_state:
        st.session_state.selected_hazard_id = None
    
    # Show appropriate view based on state
    if st.session_state.hazard_view == "list":
        # Add search and filter options
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Search bar
            search_term = st.text_input("Search Hazards", placeholder="Search by location, description, or type...", key="hazard_search")
            
            # Status filter as checkboxes
            status_options = st.multiselect(
                "Status Filter",
                options=["Open", "Mitigated", "In Progress"],
                default=["Open", "In Progress"],
                key="hazard_status_filter"
            )
        
        with col2:
            # Create button
            if st.button("+ Identify New Hazard", key="new_hazard_btn"):
                st.session_state.hazard_view = "create"
                st.rerun()
        
        # Filter hazards
        filtered_hazards = hazards
        
        if search_term:
            search_term = search_term.lower()
            filtered_hazards = [h for h in filtered_hazards if
                             search_term in h.get("location", "").lower() or
                             search_term in h.get("description", "").lower() or
                             search_term in h.get("type", "").lower() or
                             search_term in h.get("identified_by", "").lower()]
        
        if status_options:
            filtered_hazards = [h for h in filtered_hazards if h.get("status") in status_options]
        
        # Display hazards in a modern card layout
        if filtered_hazards:
            # Use a grid layout with 2 columns for the hazard cards
            for i in range(0, len(filtered_hazards), 2):
                cols = st.columns(2)
                
                # First column
                if i < len(filtered_hazards):
                    hazard = filtered_hazards[i]
                    with cols[0]:
                        render_hazard_card(hazard)
                
                # Second column
                if i + 1 < len(filtered_hazards):
                    hazard = filtered_hazards[i + 1]
                    with cols[1]:
                        render_hazard_card(hazard)
        else:
            st.info("No hazards found matching your criteria.")
            
    elif st.session_state.hazard_view == "create":
        render_hazard_form()
        
    elif st.session_state.hazard_view == "edit":
        # Get the selected hazard
        hazard = next((h for h in hazards if h.get("id") == st.session_state.selected_hazard_id), None)
        
        if hazard:
            render_hazard_form(hazard)
        else:
            st.error("Selected hazard not found.")
            st.session_state.hazard_view = "list"
            st.rerun()
            
    elif st.session_state.hazard_view == "detail":
        # Get the selected hazard
        hazard = next((h for h in hazards if h.get("id") == st.session_state.selected_hazard_id), None)
        
        if hazard:
            render_hazard_detail(hazard)
        else:
            st.error("Selected hazard not found.")
            st.session_state.hazard_view = "list"
            st.rerun()

def render_hazard_card(hazard):
    """
    Render a hazard card for the list view.
    
    Args:
        hazard (dict): The hazard data to display
    """
    # Determine status color
    status = hazard.get("status", "")
    status_color = {
        "Open": "red",
        "In Progress": "orange",
        "Mitigated": "green"
    }.get(status, "gray")
    
    # Determine severity color
    severity = hazard.get("severity", "")
    severity_color = {
        "Low": "green",
        "Medium": "orange",
        "High": "red"
    }.get(severity, "gray")
    
    # Apply card styling
    st.markdown(
        f"""
        <div class="safety-card">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span><strong>{hazard.get('id', '')}</strong></span>
                <span style="color: {status_color}; font-weight: bold;">{status}</span>
            </div>
            <div style="margin-bottom: 10px;">
                <span style="font-weight: bold; font-size: 1.1rem;">{hazard.get('type', 'Unknown')} Hazard</span>
            </div>
            <div style="margin-bottom: 10px;">
                <span>{hazard.get('location', '')}</span>
            </div>
            <div style="margin-bottom: 10px;">
                <span style="display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {hazard.get('description', 'No description')[:75]}...
                </span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: {severity_color}; font-weight: bold;">
                    Severity: {severity}
                </span>
                <span>
                    Identified: {hazard.get('date_identified', '')}
                </span>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("View", key=f"view_hazard_{hazard.get('id')}"):
            st.session_state.selected_hazard_id = hazard.get('id')
            st.session_state.hazard_view = "detail"
            st.rerun()
    
    with col2:
        if st.button("Edit", key=f"edit_hazard_{hazard.get('id')}"):
            st.session_state.selected_hazard_id = hazard.get('id')
            st.session_state.hazard_view = "edit"
            st.rerun()
    
    with col3:
        if hazard.get("status") != "Mitigated":
            if st.button("Mitigate", key=f"mitigate_hazard_{hazard.get('id')}"):
                st.success(f"Hazard {hazard.get('id')} marked as mitigated.")
                st.rerun()

def render_hazard_form(hazard=None):
    """
    Render a form for creating or editing a hazard.
    
    Args:
        hazard (dict, optional): Existing hazard data for editing
    """
    is_edit = hazard is not None
    form_title = "Edit Hazard" if is_edit else "Identify New Hazard"
    
    st.subheader(form_title)
    
    # Back button
    if st.button("← Back to List", key="back_to_hazard_list"):
        st.session_state.hazard_view = "list"
        st.rerun()
    
    with st.form("hazard_form"):
        # Basic information
        col1, col2 = st.columns(2)
        
        with col1:
            if is_edit:
                st.text_input("Hazard ID", value=hazard.get("id", ""), disabled=True, key="hazard_id")
            
            hazard_date = st.date_input(
                "Date Identified",
                value=datetime.strptime(hazard.get("date_identified", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d") if is_edit else datetime.now(),
                key="hazard_date"
            )
            
            hazard_type = st.selectbox(
                "Hazard Type",
                ["Physical", "Chemical", "Biological", "Ergonomic", "Psychological", "Environmental", "Other"],
                index=["Physical", "Chemical", "Biological", "Ergonomic", "Psychological", "Environmental", "Other"].index(hazard.get("type")) if is_edit and hazard.get("type") in ["Physical", "Chemical", "Biological", "Ergonomic", "Psychological", "Environmental", "Other"] else 0,
                key="hazard_type"
            )
        
        with col2:
            status = st.selectbox(
                "Status",
                ["Open", "In Progress", "Mitigated"],
                index=["Open", "In Progress", "Mitigated"].index(hazard.get("status")) if is_edit and hazard.get("status") in ["Open", "In Progress", "Mitigated"] else 0,
                key="hazard_status"
            )
            
            severity = st.selectbox(
                "Severity",
                ["Low", "Medium", "High"],
                index=["Low", "Medium", "High"].index(hazard.get("severity")) if is_edit and hazard.get("severity") in ["Low", "Medium", "High"] else 1,  # Default to Medium
                key="hazard_severity"
            )
        
        location = st.text_input("Location", value=hazard.get("location", "") if is_edit else "", key="hazard_location")
        
        description = st.text_area(
            "Description",
            value=hazard.get("description", "") if is_edit else "",
            height=100,
            key="hazard_description"
        )
        
        identified_by = st.text_input(
            "Identified By",
            value=hazard.get("identified_by", "") if is_edit else "",
            key="hazard_identified_by"
        )
        
        # Mitigation information
        st.subheader("Mitigation Plan")
        
        mitigation = st.text_area(
            "Mitigation Measures",
            value=hazard.get("mitigation", "") if is_edit else "",
            height=100,
            key="hazard_mitigation"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            due_date = st.date_input(
                "Due Date",
                value=datetime.strptime(hazard.get("due_date", (datetime.now() + pd.Timedelta(days=7)).strftime("%Y-%m-%d")), "%Y-%m-%d") if is_edit else (datetime.now() + pd.Timedelta(days=7)),
                key="hazard_due_date"
            )
        
        with col2:
            if is_edit and hazard.get("completed_date"):
                completed_date = st.date_input(
                    "Completion Date",
                    value=datetime.strptime(hazard.get("completed_date"), "%Y-%m-%d") if hazard.get("completed_date") else None,
                    key="hazard_completed_date"
                )
            else:
                # Only show completion date if status is Mitigated
                if status == "Mitigated":
                    completed_date = st.date_input(
                        "Completion Date",
                        value=datetime.now(),
                        key="hazard_completed_date"
                    )
        
        # Submit buttons
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("Save Hazard")
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
        
        # Prepare hazard data
        hazard_data = {
            "date_identified": hazard_date.strftime("%Y-%m-%d"),
            "type": hazard_type,
            "location": location,
            "description": description,
            "status": status,
            "severity": severity,
            "identified_by": identified_by,
            "mitigation": mitigation,
            "due_date": due_date.strftime("%Y-%m-%d"),
            "completed_date": completed_date.strftime("%Y-%m-%d") if status == "Mitigated" else None
        }
        
        # Save the hazard
        if is_edit:
            # Update existing hazard
            hazard_data["id"] = hazard["id"]
            st.success("Hazard updated successfully!")
        else:
            # Create new hazard with a new ID
            # This would be handled by the service in a real implementation
            hazard_data["id"] = f"HAZ-2025-{len(SafetyService._load_from_file(SafetyService.HAZARDS_FILE)) + 1:03d}"
            st.success("Hazard created successfully!")
        
        # Return to list view
        st.session_state.hazard_view = "list"
        st.rerun()
    
    if cancel_button:
        # Return to list view
        st.session_state.hazard_view = "list"
        st.rerun()

def render_hazard_detail(hazard):
    """
    Render detailed view of a hazard.
    
    Args:
        hazard (dict): The hazard data to display
    """
    # Back button
    if st.button("← Back to List", key="back_to_hazard_list_detail"):
        st.session_state.hazard_view = "list"
        st.rerun()
    
    # Determine status color
    status = hazard.get("status", "")
    status_color = {
        "Open": "red",
        "In Progress": "orange",
        "Mitigated": "green"
    }.get(status, "gray")
    
    # Determine severity color
    severity = hazard.get("severity", "")
    severity_color = {
        "Low": "green",
        "Medium": "orange",
        "High": "red"
    }.get(severity, "gray")
    
    # Header with ID and status
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2>{hazard.get('id', '')}</h2>
            <div style="background-color: {status_color}; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">
                {status}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Type and location
    st.markdown(f"**Type:** {hazard.get('type', '')} Hazard")
    st.markdown(f"**Location:** {hazard.get('location', '')}")
    
    # Description
    st.subheader("Description")
    st.write(hazard.get("description", "No description provided."))
    
    # Identification details
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**Identified By:** {hazard.get('identified_by', '')}")
    
    with col2:
        st.markdown(f"**Date Identified:** {hazard.get('date_identified', '')}")
    
    with col3:
        st.markdown(f"**Severity:** <span style='color:{severity_color};'>{severity}</span>", unsafe_allow_html=True)
    
    # Mitigation information
    st.subheader("Mitigation")
    st.write(hazard.get("mitigation", "No mitigation plan provided."))
    
    # Timeline
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Due Date:** {hazard.get('due_date', 'Not specified')}")
    
    with col2:
        if hazard.get("completed_date"):
            st.markdown(f"**Completed Date:** {hazard.get('completed_date')}")
        else:
            st.markdown("**Completed Date:** Not completed")
    
    # Progress bar for visual indication
    if status == "Mitigated":
        progress = 100
    elif status == "In Progress":
        progress = 50
    else:
        progress = 0
    
    st.progress(progress / 100)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Edit Hazard", key="edit_hazard_detail"):
            st.session_state.hazard_view = "edit"
            st.rerun()
    
    with col2:
        if status != "Mitigated":
            if st.button("Mark as Mitigated", key="mitigate_hazard_detail"):
                st.success(f"Hazard {hazard.get('id')} marked as mitigated.")
                st.rerun()
    
    with col3:
        if st.button("Delete Hazard", key="delete_hazard_detail"):
            st.warning("Are you sure you want to delete this hazard?")
            
            confirm_col1, confirm_col2 = st.columns(2)
            with confirm_col1:
                if st.button("Yes, Delete", key="confirm_delete_hazard"):
                    st.success(f"Hazard {hazard.get('id')} deleted successfully.")
                    st.session_state.hazard_view = "list"
                    st.rerun()
            
            with confirm_col2:
                if st.button("Cancel", key="cancel_delete_hazard"):
                    st.rerun()

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