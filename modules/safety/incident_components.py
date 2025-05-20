"""
Incident components for the Safety module.

This module provides the UI components for incident management including:
- Incident list view
- Incident details view
- Incident form (add/edit)
- Incident analysis view
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

def render_incident_list():
    """Render the incidents list view with filtering and sorting"""
    
    # Debug: Print safety_view value to understand navigation
    st.write(f"Current safety view: {st.session_state.get('safety_view', 'not set')}")
    
    # Initialize session state variables if they don't exist
    if "show_incident_modal" not in st.session_state:
        st.session_state.show_incident_modal = False
        
    if "modal_incident_data" not in st.session_state:
        st.session_state.modal_incident_data = None
    
    st.header("Incidents List")
    
    # Show success message if coming from form submission
    if st.session_state.get("show_incident_success", False):
        st.success("Incident created successfully!")
        st.session_state.show_incident_success = False
    
    # Filters in columns
    with st.expander("Filters", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Date range selector
            start_date = st.date_input("Start Date", datetime.now() - timedelta(days=90), key="incident_start_date")
        
        with col2:
            end_date = st.date_input("End Date", datetime.now(), key="incident_end_date")
        
        with col3:
            # Filter by severity
            severity = st.multiselect(
                "Severity", 
                ["Near Miss", "Minor", "Moderate", "Serious", "Critical"],
                default=["Minor", "Moderate", "Serious", "Critical"],
                key="incident_severity"
            )
            
        # Additional filters in second row
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Filter by location
            location = st.multiselect(
                "Location",
                ["Building A", "Building B", "Site Work", "Staging Area", "All Locations"],
                default=["All Locations"],
                key="incident_location_filter"
            )
            
        with col2:
            # Filter by status
            status = st.multiselect(
                "Status",
                ["Open", "Under Investigation", "Closed", "Resolved"],
                default=["Open", "Under Investigation"],
                key="incident_status_filter"
            )
            
        with col3:
            # Search by keyword
            search = st.text_input("Search", key="incident_search")
            
    # Clear filters button
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Clear Filters", key="clear_incident_filters"):
            # Reset all filter values in session state
            st.session_state.incident_start_date = datetime.now() - timedelta(days=90)
            st.session_state.incident_end_date = datetime.now()
            st.session_state.incident_severity = ["Minor", "Moderate", "Serious", "Critical"]
            st.session_state.incident_location_filter = ["All Locations"]
            st.session_state.incident_status_filter = ["Open", "Under Investigation"]
            st.session_state.incident_search = ""
            st.rerun()
    
    # Action buttons now handled in the main Safety module
    
    # Datatable styling for better appearance
    st.markdown("""
    <style>
    .st-emotion-cache-13oz8n3 {
        padding: 0.5rem;
    }
    .st-emotion-cache-13oz8n3 th {
        background-color: #f1f5f9;
        color: #334155;
        font-weight: 600;
        text-align: left;
        padding: 0.75rem 0.5rem;
    }
    .st-emotion-cache-13oz8n3 td {
        padding: 0.75rem 0.5rem;
        border-bottom: 1px solid #e2e8f0;
    }
    .st-emotion-cache-13oz8n3 tr:hover {
        background-color: #f8fafc;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get sample incident data
    incidents = generate_sample_incidents()
    
    # Removed the modal implementation for now
    
    # Apply filters to incidents
    filtered_incidents = []
    for incident in incidents:
        # Filter by date range
        if not (start_date <= incident['date'].date() <= end_date):
            continue
            
        # Filter by severity
        if incident['severity'] not in severity:
            continue
            
        # Filter by location if not "All Locations"
        if "All Locations" not in location and not any(loc in incident['location'] for loc in location):
            continue
            
        # Filter by status
        if incident['status'] not in status:
            continue
            
        # Filter by search text
        if search and search.lower() not in incident['title'].lower() and search.lower() not in incident['description'].lower():
            continue
            
        filtered_incidents.append(incident)
    
    # Display results count
    st.write(f"Showing {len(filtered_incidents)} incidents")
    
    # Create datatable with action buttons
    if filtered_incidents:
        # Prepare data for display in a cleaner format
        display_data = []
        for incident in filtered_incidents:
            display_data.append({
                "ID": incident['id'],
                "Date": incident['date'].strftime("%Y-%m-%d"),
                "Title": incident['title'],
                "Location": incident['location'],
                "Severity": incident['severity'],
                "Status": incident['status'],
                "Reported By": incident['reported_by']
            })
            
        # Convert to DataFrame for display
        df = pd.DataFrame(display_data)
        
        # Pagination controls
        if "incidents_page" not in st.session_state:
            st.session_state.incidents_page = 0
            
        # Define items per page
        items_per_page = 5
        total_pages = len(display_data) // items_per_page + (1 if len(display_data) % items_per_page > 0 else 0)
        
        # Determine which items to show on current page
        start_idx = st.session_state.incidents_page * items_per_page
        end_idx = min(start_idx + items_per_page, len(display_data))
        current_page_data = display_data[start_idx:end_idx]
        
        # Create table with incident list for current page
        for i, incident in enumerate(current_page_data):
            # Create a row for each incident with clickable title
            with st.container():
                # Add a subtle divider between incidents
                if i > 0:
                    st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
                    
                col1, col2, col3, col4 = st.columns([2, 3, 2, 2])
                
                with col1:
                    st.write(f"**{incident['Date']}**")
                    st.caption(f"ID: {incident['ID']}")
                
                with col2:
                    # Create a clickable title that navigates to the detail view
                    if st.button(f"📋 {incident['Title']}", key=f"incident_title_{incident['ID']}", use_container_width=True):
                        # Store the incident ID and switch view
                        st.session_state.selected_incident_id = incident['ID']
                        st.session_state.safety_view = "view"
                        st.rerun()
                
                with col3:
                    st.write(f"**Location:**")
                    st.write(f"{incident['Location']}")
                
                with col4:
                    severity_color = {
                        "Critical": "red",
                        "Serious": "orange",
                        "Moderate": "gold",
                        "Minor": "lightgreen",
                        "Near Miss": "green"
                    }.get(incident['Severity'], "grey")
                    
                    st.markdown(f"<span style='color:{severity_color};'>**{incident['Severity']}**</span>", unsafe_allow_html=True)
                    st.write(f"Status: {incident['Status']}")
                    
        # Add pagination controls
        st.markdown("<hr>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            if st.session_state.incidents_page > 0:
                if st.button("← Previous", key="prev_page", use_container_width=True):
                    st.session_state.incidents_page -= 1
                    st.rerun()
        
        with col2:
            st.markdown(f"<div style='text-align: center'>Page {st.session_state.incidents_page + 1} of {total_pages}</div>", unsafe_allow_html=True)
            
        with col3:
            if st.session_state.incidents_page < total_pages - 1:
                if st.button("Next →", key="next_page", use_container_width=True):
                    st.session_state.incidents_page += 1
                    st.rerun()
            

        
        # Action buttons now handled in the parent component
    else:
        st.info("No incidents match the selected filters")

def render_incident_details():
    """Render the incident details view (single record view)"""
    
    st.header("Incident Details")
    
    # Check if an incident ID is selected in session state
    if "selected_incident_id" not in st.session_state or not st.session_state.selected_incident_id:
        st.info("Please select an incident from the List View to see details")
        
        # Back button to return to list view
        if st.button("Return to List View", key="return_to_list_from_details"):
            st.session_state.safety_view = "list"  # Switch to list view
            st.rerun()
        return
    
    # Get all incidents data for lookup
    all_incidents = generate_sample_incidents()
    display_data = []
    for inc in all_incidents:
        display_data.append({
            "ID": inc['id'],
            "Date": inc['date'].strftime("%Y-%m-%d"),
            "Title": inc['title'],
            "Location": inc['location'],
            "Severity": inc['severity'],
            "Status": inc['status'],
            "Reported By": inc['reported_by'],
            "Description": inc['description'],
            "Actions": inc.get('actions_taken', 'No actions recorded'),
            "Type": inc.get('type', 'Not specified')
        })
    
    # Find the incident in our dataset
    incident_id = st.session_state.selected_incident_id
    incident = None
    
    try:
        # Try to convert to int if it's a string number
        if isinstance(incident_id, str) and incident_id.isdigit():
            incident_id = int(incident_id)
    except:
        pass
        
    # Find the matching incident
    for inc in display_data:
        if inc["ID"] == incident_id:
            incident = inc
            break
    
    # Handle case where incident isn't found
    if not incident:
        st.error(f"Incident with ID {incident_id} not found. Please select an incident from the List View.")
        
        # Back button to return to list view
        if st.button("Return to List View", key="return_to_list_from_error"):
            st.session_state.safety_view = "list"  # Switch to list view
            st.rerun()
        return
    
    # Layout in columns for clean presentation
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Incident information 
        st.subheader(f"Incident #{incident['ID']}: {incident['Title']}")
        
        # Status indicator with appropriate color
        status_colors = {
            "Open": "🔴",
            "Under Investigation": "🟠",
            "Closed": "🟢",
            "Resolved": "🟢"
        }
        status_icon = status_colors.get(incident['Status'], "⚪")
        st.markdown(f"**Status**: {status_icon} {incident['Status']}")
        
        # Incident metadata
        st.markdown(f"**Date**: {incident['Date']}")
        st.markdown(f"**Location**: {incident['Location']}")
        st.markdown(f"**Type**: {incident['Type']}")
        st.markdown(f"**Severity**: {incident['Severity']}")
        st.markdown(f"**Reported By**: {incident['Reported By']}")
        
        # Description
        st.markdown("### Description")
        st.write(incident['Description'])
        
        # Actions Taken
        st.markdown("### Actions Taken")
        st.write(incident['Actions'])
    
    with col2:
        # Back button to return to list view
        if st.button("← Back to List", key="back_to_list_from_details", use_container_width=True):
            st.session_state.safety_view = "list"  # Switch to list view
            st.rerun()
            
        # Edit button for this incident
        if st.button("✏️ Edit Incident", key="edit_incident_details", use_container_width=True):
            st.session_state.edit_incident_id = incident['ID']  # Use incident dictionary value
            st.session_state.safety_view = "edit"  # Switch to edit mode
            st.rerun()
        
        # Status update button
        st.markdown("### Update Status")
        new_status = st.selectbox(
            "New Status",
            ["Open", "Under Investigation", "Closed", "Resolved"],
            index=["Open", "Under Investigation", "Closed", "Resolved"].index(incident['Status']),
            key="status_update_detail"
        )
        
        if st.button("Update Status", key="update_status_btn_detail", use_container_width=True):
            st.success(f"Status updated to: {new_status}")
            
        # Attachments section
        st.markdown("### Attachments")
        st.write("No attachments")
        
        # Upload new attachment button
        st.file_uploader("Upload New Attachment", key="upload_attachment_detail")

def render_incident_form(is_edit=False):
    """Render the incident creation/edit form"""
    
    if is_edit:
        st.header("Edit Incident")
        editing_id = st.session_state.get("edit_incident_id")
        if not editing_id:
            st.warning("No incident selected for editing")
            st.button("Return to List View", key="return_to_list_from_edit_error", 
                     on_click=lambda: st.session_state.update({"safety_tab_selection": {"incidents": 0}}))
            return
        
        # Find the incident data for editing
        incidents = generate_sample_incidents()
        incident = next((inc for inc in incidents if inc["id"] == editing_id), None)
        if not incident:
            st.error("Incident not found")
            st.button("Return to List View", key="return_to_list_from_no_incident", 
                     on_click=lambda: st.session_state.update({"safety_tab_selection": {"incidents": 0}}))
            return
        
        form_title = "Edit Incident"
        submit_label = "Update Incident"
    else:
        st.header("Add New Incident")
        incident = {
            "date": datetime.now(),
            "status": "Open",
            "severity": "Minor"
        }
        form_title = "New Incident"
        submit_label = "Create Incident"
    
    # Form implementation
    with st.form(key=f"incident_form_{'edit' if is_edit else 'new'}"):
        st.subheader(form_title)
        
        # Layout in columns for better organization
        col1, col2 = st.columns(2)
        
        with col1:
            incident_date = st.date_input(
                "Date", 
                value=incident.get('date', datetime.now()),
                key="incident_form_date"
            )
            
            incident_title = st.text_input(
                "Incident Title",
                value=incident.get('title', ''),
                key="incident_form_title"
            )
            
            incident_location = st.text_input(
                "Location",
                value=incident.get('location', ''),
                key="incident_form_location"
            )
            
            incident_type = st.selectbox(
                "Type",
                ["Slip/Trip/Fall", "Struck By", "Caught In/Between", "Electrical", "Chemical Exposure", "Ergonomic", "Other"],
                index=["Slip/Trip/Fall", "Struck By", "Caught In/Between", "Electrical", "Chemical Exposure", "Ergonomic", "Other"].index(incident.get('type', 'Other')) if incident.get('type') else 0,
                key="incident_form_type"
            )
        
        with col2:
            incident_severity = st.selectbox(
                "Severity",
                ["Near Miss", "Minor", "Moderate", "Serious", "Critical"],
                index=["Near Miss", "Minor", "Moderate", "Serious", "Critical"].index(incident.get('severity', 'Minor')),
                key="incident_form_severity"
            )
            
            incident_status = st.selectbox(
                "Status",
                ["Open", "Under Investigation", "Closed", "Resolved"],
                index=["Open", "Under Investigation", "Closed", "Resolved"].index(incident.get('status', 'Open')),
                key="incident_form_status"
            )
            
            incident_reported_by = st.text_input(
                "Reported By",
                value=incident.get('reported_by', ''),
                key="incident_form_reported_by"
            )
            
            # If we're editing, show the incident ID as read-only
            if is_edit:
                st.text_input(
                    "Incident ID",
                    value=incident.get('id', ''),
                    disabled=True,
                    key="incident_form_id"
                )
        
        # Description and actions taken - full width
        incident_description = st.text_area(
            "Description",
            value=incident.get('description', ''),
            height=150,
            key="incident_form_description"
        )
        
        incident_actions = st.text_area(
            "Actions Taken",
            value=incident.get('actions_taken', ''),
            height=100,
            key="incident_form_actions"
        )
        
        # Witnesses - expandable section
        with st.expander("Witnesses", expanded=bool(incident.get('witnesses'))):
            witness_count = st.number_input(
                "Number of Witnesses",
                min_value=0,
                max_value=10,
                value=len(incident.get('witnesses', [])),
                key="incident_form_witness_count"
            )
            
            witnesses = []
            for i in range(witness_count):
                witness = st.text_input(
                    f"Witness {i+1}",
                    value=incident.get('witnesses', [])[i] if i < len(incident.get('witnesses', [])) else '',
                    key=f"incident_form_witness_{i}"
                )
                witnesses.append(witness)
        
        # Form submission
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            back_button = st.form_submit_button("Cancel", type="secondary")
            
        with col3:
            submit_button = st.form_submit_button(submit_label, type="primary")
        
        if back_button:
            if is_edit:
                # If editing, return to details view
                st.session_state.safety_view = "view"
            else:
                # If adding new, return to list view
                st.session_state.safety_view = "list"
            st.rerun()
            
        if submit_button:
            if not incident_title:
                st.error("Incident title is required")
            elif not incident_location:
                st.error("Incident location is required")
            elif not incident_description:
                st.error("Incident description is required")
            elif not incident_reported_by:
                st.error("Reported by is required")
            else:
                # In a real app, we would save the data here
                st.success(f"Incident {'updated' if is_edit else 'created'} successfully!")
                
                # Clear form state or return to appropriate view
                if is_edit:
                    # Return to details view of this incident
                    st.session_state.safety_view = "view"
                    st.rerun()
                else:
                    # Set a flag to show success message on list view
                    st.session_state.show_incident_success = True
                    st.session_state.safety_view = "list"
                    st.rerun()

def render_incidents_analysis():
    """Render the incidents analysis view with charts and metrics"""
    
    st.header("Incident Analysis")
    
    # Get sample data
    incidents = generate_sample_incidents()
    
    # Create a DataFrame for analysis
    df = pd.DataFrame([{
        'id': inc['id'],
        'date': inc['date'],
        'title': inc['title'],
        'location': inc['location'],
        'type': inc['type'],
        'severity': inc['severity'],
        'status': inc['status'],
        'reported_by': inc['reported_by']
    } for inc in incidents])
    
    # Layout in columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_incidents = len(df)
        st.metric("Total Incidents", total_incidents)
        
    with col2:
        open_incidents = len(df[df['status'].isin(['Open', 'Under Investigation'])])
        st.metric("Open Incidents", open_incidents)
        
    with col3:
        critical_incidents = len(df[df['severity'] == 'Critical'])
        st.metric("Critical Incidents", critical_incidents)
        
    with col4:
        resolved_rate = round(len(df[df['status'] == 'Resolved']) / total_incidents * 100, 1) if total_incidents > 0 else 0
        st.metric("Resolved Rate", f"{resolved_rate}%")
    
    # Tabs for different analysis views
    analysis_tabs = st.tabs(["Trends", "By Type", "By Location", "By Severity"])
    
    with analysis_tabs[0]:
        st.subheader("Incident Trends")
        
        # Incidents by month
        df['month'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
        monthly_counts = df.groupby('month').size()
        incidents_by_month = pd.DataFrame({
            'month': monthly_counts.index,
            'count': monthly_counts.values
        })
        
        if not incidents_by_month.empty:
            fig = px.bar(
                incidents_by_month, 
                x='month', 
                y='count',
                title="Incidents by Month",
                labels={"month": "Month", "count": "Number of Incidents"}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with analysis_tabs[1]:
        st.subheader("Incidents by Type")
        
        # Incidents by type
        incidents_by_type = df['type'].value_counts().reset_index()
        incidents_by_type.columns = ['type', 'count']
        
        if not incidents_by_type.empty:
            fig = px.pie(
                incidents_by_type,
                values='count',
                names='type',
                title="Incidents by Type"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with analysis_tabs[2]:
        st.subheader("Incidents by Location")
        
        # Extract building and floor from location
        df['building'] = df['location'].apply(lambda x: x.split('-')[0].strip() if '-' in x else x)
        
        incidents_by_building = df['building'].value_counts().reset_index()
        incidents_by_building.columns = ['building', 'count']
        
        if not incidents_by_building.empty:
            fig = px.bar(
                incidents_by_building,
                x='building',
                y='count',
                title="Incidents by Building",
                labels={"building": "Building", "count": "Number of Incidents"}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with analysis_tabs[3]:
        st.subheader("Incidents by Severity")
        
        # Incidents by severity
        severity_order = ["Near Miss", "Minor", "Moderate", "Serious", "Critical"]
        incidents_by_severity = df['severity'].value_counts().reset_index()
        incidents_by_severity.columns = ['severity', 'count']
        
        # Sort by severity level
        incidents_by_severity['severity_order'] = incidents_by_severity['severity'].apply(lambda x: severity_order.index(x) if x in severity_order else 999)
        incidents_by_severity = incidents_by_severity.sort_values('severity_order')
        
        if not incidents_by_severity.empty:
            fig = px.bar(
                incidents_by_severity,
                x='severity',
                y='count',
                title="Incidents by Severity",
                labels={"severity": "Severity", "count": "Number of Incidents"},
                color='severity',
                color_discrete_map={
                    "Near Miss": "green",
                    "Minor": "lightgreen",
                    "Moderate": "gold",
                    "Serious": "orange",
                    "Critical": "red"
                }
            )
            st.plotly_chart(fig, use_container_width=True)

# Helper function to generate sample incidents
def generate_sample_incidents():
    """Generate sample incidents for demonstration"""
    incidents = []
    
    # Generate random incidents
    for i in range(1, 25):
        incident_date = datetime.now() - timedelta(days=random.randint(1, 180))
        
        incident_type = random.choice([
            "Slip/Trip/Fall", 
            "Struck By", 
            "Caught In/Between", 
            "Electrical", 
            "Chemical Exposure", 
            "Ergonomic",
            "Other"
        ])
        
        incident_severity = random.choice([
            "Near Miss", 
            "Minor", 
            "Moderate", 
            "Serious", 
            "Critical"
        ])
        
        incident_status = random.choice([
            "Open", 
            "Under Investigation", 
            "Closed", 
            "Resolved"
        ])
        
        incident_location = random.choice([
            "Building A - Floor 1 - North Wing",
            "Building A - Floor 2 - South Wing",
            "Building B - Floor 1 - East Wing",
            "Building B - Floor 3 - West Wing",
            "Site Work - Excavation",
            "Site Work - Utility Installation",
            "Staging Area - Materials Storage"
        ])
        
        # Generate a title based on the incident type
        title_prefixes = {
            "Slip/Trip/Fall": ["Worker slipped on", "Visitor tripped over", "Employee fell from"],
            "Struck By": ["Worker struck by", "Employee hit by", "Collision with"],
            "Caught In/Between": ["Hand caught in", "Worker trapped between", "Finger pinched in"],
            "Electrical": ["Electrical shock from", "Short circuit in", "Exposure to live"],
            "Chemical Exposure": ["Chemical spill of", "Exposure to", "Inhalation of"],
            "Ergonomic": ["Strain injury from", "Back pain due to", "Repetitive motion injury while"],
            "Other": ["Incident involving", "Issue with", "Problem reported with"]
        }
        
        title_suffixes = {
            "Slip/Trip/Fall": ["wet floor", "extension cord", "uneven surface", "temporary stairs", "scaffold"],
            "Struck By": ["moving equipment", "falling object", "swinging door", "forklift", "crane load"],
            "Caught In/Between": ["machinery", "door", "moving parts", "equipment", "materials"],
            "Electrical": ["exposed wiring", "damaged cord", "power tool", "junction box", "panel"],
            "Chemical Exposure": ["solvent", "adhesive", "paint", "cleaning product", "concrete mix"],
            "Ergonomic": ["lifting heavy materials", "awkward positioning", "improper tools", "repetitive task"],
            "Other": ["weather conditions", "third-party work", "unexpected event", "equipment failure"]
        }
        
        prefix = random.choice(title_prefixes.get(incident_type, title_prefixes["Other"]))
        suffix = random.choice(title_suffixes.get(incident_type, title_suffixes["Other"]))
        incident_title = f"{prefix} {suffix}"
        
        # Random descriptions based on type and severity
        description_templates = [
            "Worker reported {severity} incident while working on {location}. {details}",
            "A {severity} incident occurred at {location} when {details}",
            "During routine work at {location}, a {severity} incident happened involving {details}",
            "{severity} incident reported: {details} This occurred at {location}."
        ]
        
        detail_templates = {
            "Slip/Trip/Fall": [
                "The individual lost footing on a slippery surface.",
                "There was a trip hazard that wasn't properly marked.",
                "The worker fell from an elevated position.",
                "The guardrail was not properly secured leading to the fall."
            ],
            "Struck By": [
                "An unsecured object fell from above.",
                "Moving equipment made contact with the worker.",
                "Material being moved struck the individual.",
                "A tool was dropped from an elevated work area."
            ],
            "Caught In/Between": [
                "A body part was caught between moving equipment parts.",
                "The worker's clothing was caught in machinery.",
                "Hands were trapped between materials being positioned.",
                "Fingers were pinched in a closing mechanism."
            ],
            "Electrical": [
                "Contact was made with energized electrical component.",
                "Improper lockout/tagout procedures were followed.",
                "Damaged insulation led to exposure to live current.",
                "Water infiltration into electrical equipment caused a short."
            ],
            "Chemical Exposure": [
                "A container was damaged resulting in spillage.",
                "Inadequate ventilation led to inhalation of fumes.",
                "Improper PPE was used when handling chemicals.",
                "Splashing occurred during transfer between containers."
            ],
            "Ergonomic": [
                "Improper lifting technique was used for heavy materials.",
                "Extended work in awkward position caused strain.",
                "Repetitive motions without adequate breaks led to injury.",
                "Tools not ergonomically designed contributed to the issue."
            ],
            "Other": [
                "Unusual circumstances led to this incident.",
                "Third-party contractors were involved in the incident.",
                "Equipment failure occurred unexpectedly.",
                "Environmental factors contributed to the situation."
            ]
        }
        
        details = random.choice(detail_templates.get(incident_type, detail_templates["Other"]))
        description_template = random.choice(description_templates)
        incident_description = description_template.format(
            severity=incident_severity.lower(),
            location=incident_location,
            details=details
        )
        
        # Generate random actions taken based on status
        actions_templates = {
            "Open": [
                "Initial report filed. Investigation pending.",
                "Preliminary assessment completed. Awaiting full investigation.",
                "Area secured. Safety team notified.",
                "No actions taken yet. Scheduled for review."
            ],
            "Under Investigation": [
                "Safety team conducting interviews with witnesses.",
                "Site inspection in progress to identify contributing factors.",
                "Review of safety procedures related to the incident underway.",
                "Documentation and evidence being collected."
            ],
            "Closed": [
                "Investigation completed. Cause identified as {cause}. Recommendations implemented.",
                "Root cause analysis finished. Safety briefing conducted with all staff.",
                "Corrective actions implemented: {corrections}",
                "Case reviewed by safety committee. Procedural changes made."
            ],
            "Resolved": [
                "All recommended actions implemented. Verification completed.",
                "Follow-up training conducted. New safety measures in place.",
                "Engineering controls added to prevent recurrence. Case closed.",
                "Hazard eliminated through {solution}. Final report filed."
            ]
        }
        
        causes = [
            "inadequate training", 
            "equipment failure", 
            "procedural non-compliance", 
            "environmental factors",
            "improper risk assessment", 
            "lack of proper PPE", 
            "insufficient supervision"
        ]
        
        corrections = [
            "additional guardrails installed", 
            "new PPE requirements", 
            "revised work procedures",
            "additional training provided", 
            "improved signage", 
            "engineering modifications"
        ]
        
        solutions = [
            "design modification", 
            "process change", 
            "automation of hazardous task",
            "elimination of the hazard", 
            "substitution with safer alternative"
        ]
        
        actions_template = random.choice(actions_templates.get(incident_status, actions_templates["Open"]))
        actions_taken = actions_template.format(
            cause=random.choice(causes),
            corrections=random.choice(corrections),
            solution=random.choice(solutions)
        )
        
        # Random reported by names
        first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", 
                      "David", "Susan", "Richard", "Jessica", "Joseph", "Sarah", "Thomas", "Karen", "Charles", "Nancy"]
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", 
                      "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]
        reported_by = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        # Generate random witnesses (only for more serious incidents)
        witnesses = []
        if incident_severity in ["Moderate", "Serious", "Critical"] and random.random() > 0.3:
            witness_count = random.randint(1, 3)
            for _ in range(witness_count):
                witness_name = f"{random.choice(first_names)} {random.choice(last_names)}"
                while witness_name == reported_by or witness_name in witnesses:
                    witness_name = f"{random.choice(first_names)} {random.choice(last_names)}"
                witnesses.append(witness_name)
        
        # Generate random attachments (more likely for serious incidents)
        attachments = []
        if random.random() > 0.6:
            attachment_count = random.randint(1, 3)
            attachment_types = ["Photo", "Report", "Statement", "Medical Record", "Diagram"]
            for j in range(attachment_count):
                attachment_type = random.choice(attachment_types)
                attachment = {
                    "id": f"ATT-{i:03d}-{j:02d}",
                    "name": f"{attachment_type} - {incident_date.strftime('%Y-%m-%d')}",
                    "type": attachment_type.lower().replace(" ", "_"),
                    "date_uploaded": incident_date + timedelta(days=random.randint(0, 5))
                }
                attachments.append(attachment)
        
        # Create the incident record
        incident = {
            "id": f"INC-{2025}-{i:03d}",
            "date": incident_date,
            "title": incident_title,
            "location": incident_location,
            "type": incident_type,
            "severity": incident_severity,
            "status": incident_status,
            "reported_by": reported_by,
            "description": incident_description,
            "actions_taken": actions_taken
        }
        
        # Add optional fields
        if witnesses:
            incident["witnesses"] = witnesses
        
        if attachments:
            incident["attachments"] = attachments
        
        incidents.append(incident)
    
    # Sort by date, newest first
    incidents.sort(key=lambda x: x['date'], reverse=True)
    
    return incidents