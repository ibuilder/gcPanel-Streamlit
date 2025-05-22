"""
Safety Incidents Module for gcPanel

This module provides tracking and management of safety incidents with CRUD styling
for a consistent user experience across the application.
"""

import streamlit as st
import os
import json
from datetime import datetime, timedelta
import random
import pandas as pd

from modules.crud_template import CrudModule
from assets.crud_styler import (
    apply_crud_styles, 
    render_form_actions, 
    render_crud_fieldset
)

class SafetyIncidentModule(CrudModule):
    def __init__(self):
        """Initialize the Safety Incidents module with configuration."""
        super().__init__(
            module_name="Safety Incidents",
            data_file_path="data/safety/incidents.json",
            id_field="incident_id",
            list_columns=["incident_id", "incident_date", "location", "incident_type", "severity", "status"],
            default_sort_field="incident_date",
            default_sort_direction="desc",
            status_field="status",
            filter_options=["Open", "Investigating", "Resolved", "Closed"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        incident_types = [
            "Near Miss", 
            "First Aid", 
            "Medical Treatment", 
            "Lost Time Injury", 
            "Property Damage", 
            "Environmental"
        ]
        
        locations = [
            "Level 1 - North", 
            "Level 2 - East", 
            "Level 3 - South",
            "Level 4 - West", 
            "Basement",
            "Roof", 
            "Exterior Scaffolding",
            "Loading Dock", 
            "Parking Area"
        ]
        
        severities = ["Low", "Medium", "High", "Critical"]
        statuses = ["Open", "Investigating", "Resolved", "Closed"]
        
        # Employees for reporting and involvement
        employees = [
            "John Smith", 
            "Maria Garcia", 
            "Robert Johnson", 
            "Lisa Wong", 
            "David Miller",
            "Sarah Adams", 
            "Michael Chen", 
            "Emma Wilson"
        ]
        
        # Demo incidents
        demo_items = []
        
        # Create sample incidents
        for i in range(1, 21):
            # Set dates based on realistic timeframes
            incident_date = datetime.now() - timedelta(days=random.randint(1, 120))
            
            # Randomize incident details
            incident_type = random.choice(incident_types)
            location = random.choice(locations)
            severity = random.choice(severities)
            
            # Determine status based on date and severity
            days_since = (datetime.now() - incident_date).days
            
            if days_since < 7 and severity in ["High", "Critical"]:
                status = random.choice(["Open", "Investigating"])
                closed_date = None
            elif days_since < 14:
                status = random.choice(["Open", "Investigating", "Resolved"])
                closed_date = incident_date + timedelta(days=random.randint(1, days_since)) if status == "Resolved" else None
            else:
                status = random.choice(["Investigating", "Resolved", "Closed"])
                closed_date = incident_date + timedelta(days=random.randint(7, min(30, days_since))) if status in ["Resolved", "Closed"] else None
            
            # Generate specific description based on incident type
            if incident_type == "Near Miss":
                description = f"Near miss incident involving {random.choice(['falling object', 'slip hazard', 'electrical hazard', 'vehicle movement'])}. No injuries occurred."
            elif incident_type == "First Aid":
                description = f"Minor {random.choice(['cut', 'bruise', 'scrape', 'foreign object in eye'])} requiring first aid treatment only."
            elif incident_type == "Medical Treatment":
                description = f"Worker sustained {random.choice(['laceration', 'sprain', 'burn', 'eye injury'])} requiring medical treatment."
            elif incident_type == "Lost Time Injury":
                description = f"Worker sustained {random.choice(['back injury', 'fracture', 'crush injury', 'severe laceration'])} resulting in lost time."
            elif incident_type == "Property Damage":
                description = f"Damage to {random.choice(['equipment', 'structure', 'vehicle', 'temporary facilities'])} occurred during operation."
            else:  # Environmental
                description = f"{random.choice(['Spill', 'Dust emission', 'Noise violation', 'Water discharge'])} incident requiring environmental response."
            
            # Generate random incident time
            hour = random.randint(7, 17)  # Between 7 AM and 5 PM
            minute = random.choice([0, 15, 30, 45])
            incident_time = f"{hour:02d}:{minute:02d}"
            
            # Create the incident record
            item = {
                'incident_id': f'INC-{i:03d}',
                'incident_date': incident_date.strftime('%Y-%m-%d'),
                'incident_time': incident_time,
                'location': location,
                'incident_type': incident_type,
                'severity': severity,
                'status': status,
                'description': description,
                'reported_by': random.choice(employees),
                'witnesses': random.sample(employees, random.randint(0, 3)) if random.random() > 0.3 else [],
                'injured_persons': random.sample(employees, random.randint(0, 1)) if incident_type in ["First Aid", "Medical Treatment", "Lost Time Injury"] else [],
                'root_cause': random.choice(["Human Error", "Equipment Failure", "Environmental Conditions", "Procedural Deficiency", "Inadequate Training", "Inadequate Planning"]) if status in ["Resolved", "Closed"] else "",
                'corrective_actions': [] if status == "Open" else [
                    {
                        'action': f"Implement {random.choice(['additional training', 'new procedure', 'engineering control', 'administrative control'])}",
                        'assigned_to': random.choice(employees),
                        'due_date': (incident_date + timedelta(days=random.randint(7, 30))).strftime('%Y-%m-%d'),
                        'status': random.choice(["Pending", "In Progress", "Complete"])
                    }
                ] if random.random() > 0.2 else [],
                'closed_date': closed_date.strftime('%Y-%m-%d') if closed_date else None,
                'attachments': []
            }
            
            demo_items.append(item)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _create_new_item_template(self):
        """Create a template for a new safety incident with default values."""
        item_id = self._generate_new_id()
        
        # Set default dates
        today = datetime.now()
        
        return {
            'incident_id': f'INC-{int(item_id):03d}',
            'incident_date': today.strftime('%Y-%m-%d'),
            'incident_time': today.strftime('%H:%M'),
            'location': '',
            'incident_type': '',
            'severity': '',
            'status': 'Open',
            'description': '',
            'reported_by': '',
            'witnesses': [],
            'injured_persons': [],
            'root_cause': '',
            'corrective_actions': [],
            'closed_date': None,
            'attachments': []
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for safety incidents."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            item_id = item.get('incident_id', '')
            if item_id.startswith('INC-'):
                try:
                    num = int(item_id.split('-')[1])
                    max_id = max(max_id, num)
                except:
                    pass
        
        return str(max_id + 1)
    
    def _get_status_class(self, status):
        """Get the status class for a given status value."""
        status_classes = {
            'Open': 'danger',
            'Investigating': 'warning',
            'Resolved': 'info',
            'Closed': 'success'
        }
        return status_classes.get(status, 'secondary')
    
    def _get_severity_class(self, severity):
        """Get the severity class for a given severity value."""
        severity_classes = {
            'Low': 'success',
            'Medium': 'info',
            'High': 'warning',
            'Critical': 'danger'
        }
        return severity_classes.get(severity, 'secondary')
    
    def render_detail_view(self):
        """Render the detail view for creating, viewing, or editing a safety incident."""
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = "New Safety Incident"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Safety Incident with ID {item_id} not found")
                return
            detail_title = f"{item.get('incident_id', 'Safety Incident')}"
        
        # Render the detail container
        from assets.crud_styler import render_crud_detail_container, end_crud_detail_container
        
        mode_prefix = "New" if is_new else "Edit" if is_edit_mode else "View"
        container_title = f"{mode_prefix}: {detail_title}"
        
        detail_actions = render_crud_detail_container(
            title=container_title,
            is_new=is_new,
            back_button=True
        )
        
        # Check if back button was clicked
        if detail_actions['back_clicked']:
            st.session_state[f'{base_key}_view'] = 'list'
            st.rerun()
        
        # Display top action buttons for view mode
        if not is_new and not is_edit_mode:
            col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
            with col1:
                if st.button("✏️ Edit", type="primary", key=f"edit_{base_key}_action"):
                    st.session_state[f'{base_key}_edit_mode'] = True
                    st.rerun()
            with col2:
                if st.button("📄 PDF", type="secondary", key=f"pdf_{base_key}_action"):
                    st.info("This would generate a PDF incident report in a production environment.")
            with col3:
                if st.button("🗑️ Delete", type="secondary", key=f"delete_{base_key}_action"):
                    st.warning("Are you sure you want to delete this safety incident?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key=f"confirm_delete_{base_key}"):
                            self._delete_item(item['incident_id'])
                            st.success("Safety incident deleted successfully")
                            st.session_state[f'{base_key}_view'] = 'list'
                            st.rerun()
                    with confirm_col2:
                        if st.button("Cancel", key=f"cancel_delete_{base_key}"):
                            st.rerun()
        
        # Create form for editing or read-only view for viewing
        if is_edit_mode or is_new:
            with st.form(f"{base_key}_form"):
                # Basic Information Section
                def render_basic_info():
                    col1, col2 = st.columns(2)
                    with col1:
                        incident_id = st.text_input("Incident ID", value=item['incident_id'], disabled=not is_new)
                    with col2:
                        incident_type = st.selectbox("Incident Type", options=[
                            '', 'Near Miss', 'First Aid', 'Medical Treatment', 
                            'Lost Time Injury', 'Property Damage', 'Environmental'
                        ], index=['', 'Near Miss', 'First Aid', 'Medical Treatment', 
                                'Lost Time Injury', 'Property Damage', 'Environmental'].index(
                            item['incident_type'] if item['incident_type'] in ['', 'Near Miss', 'First Aid', 'Medical Treatment', 
                                                                              'Lost Time Injury', 'Property Damage', 'Environmental'] 
                            else '')
                        )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        incident_date = st.date_input(
                            "Incident Date", 
                            value=datetime.strptime(item['incident_date'], '%Y-%m-%d') if item['incident_date'] else datetime.now()
                        )
                    with col2:
                        incident_time = st.text_input("Incident Time (HH:MM)", value=item['incident_time'])
                    
                    location = st.text_input("Location", value=item['location'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        severity = st.selectbox("Severity", options=[
                            '', 'Low', 'Medium', 'High', 'Critical'
                        ], index=['', 'Low', 'Medium', 'High', 'Critical'].index(
                            item['severity'] if item['severity'] in ['', 'Low', 'Medium', 'High', 'Critical'] 
                            else '')
                        )
                    with col2:
                        status = st.selectbox("Status", options=[
                            'Open', 'Investigating', 'Resolved', 'Closed'
                        ], index=['Open', 'Investigating', 'Resolved', 'Closed'].index(
                            item['status'] if item['status'] in ['Open', 'Investigating', 'Resolved', 'Closed'] 
                            else 'Open')
                        )
                    
                    description = st.text_area("Description", value=item['description'], height=100)
                    
                    return incident_id, incident_type, incident_date, incident_time, location, severity, status, description
                
                incident_id, incident_type, incident_date, incident_time, location, severity, status, description = render_crud_fieldset("Incident Information", render_basic_info)
                
                # People Section
                def render_people_info():
                    reported_by = st.text_input("Reported By", value=item['reported_by'])
                    
                    # Witnesses
                    witnesses_str = ", ".join(item.get('witnesses', []))
                    witnesses = st.text_input("Witnesses (comma separated)", value=witnesses_str)
                    
                    # Injured persons
                    injured_persons_str = ", ".join(item.get('injured_persons', []))
                    injured_persons = st.text_input("Injured Persons (comma separated)", value=injured_persons_str)
                    
                    return reported_by, witnesses, injured_persons
                
                reported_by, witnesses, injured_persons = render_crud_fieldset("People Involved", render_people_info)
                
                # Investigation Section
                def render_investigation_info():
                    root_cause = st.text_area("Root Cause", value=item.get('root_cause', ''), height=100)
                    
                    # Corrective actions
                    st.subheader("Corrective Actions")
                    
                    corrective_actions = []
                    existing_actions = item.get('corrective_actions', [])
                    
                    for i, action in enumerate(existing_actions):
                        st.markdown(f"##### Action {i+1}")
                        col1, col2 = st.columns(2)
                        with col1:
                            action_text = st.text_input("Action", value=action['action'], key=f"action_text_{i}")
                        with col2:
                            assigned_to = st.text_input("Assigned To", value=action['assigned_to'], key=f"assigned_to_{i}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            due_date = st.date_input("Due Date", 
                                value=datetime.strptime(action['due_date'], '%Y-%m-%d') if action.get('due_date') else datetime.now(),
                                key=f"due_date_{i}")
                        with col2:
                            action_status = st.selectbox("Status", 
                                options=['Pending', 'In Progress', 'Complete'], 
                                index=['Pending', 'In Progress', 'Complete'].index(action.get('status', 'Pending')),
                                key=f"action_status_{i}")
                        
                        corrective_actions.append({
                            'action': action_text,
                            'assigned_to': assigned_to,
                            'due_date': due_date.strftime('%Y-%m-%d'),
                            'status': action_status
                        })
                    
                    # Add new action button
                    if st.checkbox("Add New Corrective Action", key=f"add_new_action"):
                        st.markdown(f"##### New Action")
                        col1, col2 = st.columns(2)
                        with col1:
                            new_action_text = st.text_input("Action", key=f"new_action_text")
                        with col2:
                            new_assigned_to = st.text_input("Assigned To", key=f"new_assigned_to")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            new_due_date = st.date_input("Due Date", value=datetime.now() + timedelta(days=7), key=f"new_due_date")
                        with col2:
                            new_action_status = st.selectbox("Status", 
                                options=['Pending', 'In Progress', 'Complete'], 
                                index=0,
                                key=f"new_action_status")
                        
                        if st.button("Add Action", key=f"confirm_add_action"):
                            corrective_actions.append({
                                'action': new_action_text,
                                'assigned_to': new_assigned_to,
                                'due_date': new_due_date.strftime('%Y-%m-%d'),
                                'status': new_action_status
                            })
                    
                    # Show closed date if status is Closed
                    if status == 'Closed':
                        closed_date = st.date_input(
                            "Closed Date", 
                            value=datetime.strptime(item['closed_date'], '%Y-%m-%d') if item.get('closed_date') else datetime.now()
                        )
                    else:
                        closed_date = None
                    
                    return root_cause, corrective_actions, closed_date
                
                root_cause, corrective_actions, closed_date = render_crud_fieldset("Investigation & Resolution", render_investigation_info)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Incident",
                    cancel_label="Cancel",
                    delete_label="Delete Incident",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Parse witnesses and injured persons from comma-separated strings
                    witnesses_list = [name.strip() for name in witnesses.split(',')] if witnesses else []
                    witnesses_list = [name for name in witnesses_list if name]  # Remove empty names
                    
                    injured_persons_list = [name.strip() for name in injured_persons.split(',')] if injured_persons else []
                    injured_persons_list = [name for name in injured_persons_list if name]  # Remove empty names
                    
                    # Update item with form values
                    updated_item = {
                        'incident_id': incident_id,
                        'incident_date': incident_date.strftime('%Y-%m-%d'),
                        'incident_time': incident_time,
                        'location': location,
                        'incident_type': incident_type,
                        'severity': severity,
                        'status': status,
                        'description': description,
                        'reported_by': reported_by,
                        'witnesses': witnesses_list,
                        'injured_persons': injured_persons_list,
                        'root_cause': root_cause,
                        'corrective_actions': corrective_actions,
                        'closed_date': closed_date.strftime('%Y-%m-%d') if closed_date else None,
                        'attachments': item.get('attachments', [])
                    }
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Safety incident saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['incident_id'])
                    st.success("Safety incident deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            # Incident Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Incident Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Incident ID:** {item['incident_id']}")
            with col2:
                st.markdown(f"**Incident Type:** {item['incident_type']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Date:** {item['incident_date']}")
            with col2:
                st.markdown(f"**Time:** {item['incident_time']}")
            
            st.markdown(f"**Location:** {item['location']}")
            
            col1, col2 = st.columns(2)
            with col1:
                # Show severity with colored badge
                severity_class = self._get_severity_class(item['severity'])
                severity_html = f"""
                <div style="display: flex; align-items: center; background: transparent;">
                    <span class='crud-status crud-status-{severity_class}' style="outline: none; box-shadow: none; border: none;">{item['severity']}</span>
                </div>
                """
                st.markdown("**Severity:**")
                st.markdown(severity_html, unsafe_allow_html=True)
            with col2:
                # Show status with colored badge
                status_class = self._get_status_class(item['status'])
                status_html = f"""
                <div style="display: flex; align-items: center; background: transparent;">
                    <span class='crud-status crud-status-{status_class}' style="outline: none; box-shadow: none; border: none;">{item['status']}</span>
                </div>
                """
                st.markdown("**Status:**")
                st.markdown(status_html, unsafe_allow_html=True)
            
            if item.get('description'):
                st.markdown(f"**Description:**")
                st.markdown(f"```{item['description']}```")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # People Involved Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("People Involved")
            
            st.markdown(f"**Reported By:** {item['reported_by']}")
            
            if item.get('witnesses'):
                st.markdown(f"**Witnesses:** {', '.join(item['witnesses'])}")
            else:
                st.markdown(f"**Witnesses:** None")
            
            if item.get('injured_persons'):
                st.markdown(f"**Injured Persons:** {', '.join(item['injured_persons'])}")
            else:
                st.markdown(f"**Injured Persons:** None")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Investigation Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Investigation & Resolution")
            
            if item.get('root_cause'):
                st.markdown(f"**Root Cause:**")
                st.markdown(f"```{item['root_cause']}```")
            else:
                st.markdown(f"**Root Cause:** Not yet determined")
            
            # Corrective Actions
            st.markdown("#### Corrective Actions")
            
            if not item.get('corrective_actions'):
                st.info("No corrective actions have been specified for this incident.")
            else:
                for i, action in enumerate(item['corrective_actions']):
                    action_status = action.get('status', 'Pending')
                    action_status_class = {
                        'Pending': 'secondary',
                        'In Progress': 'info',
                        'Complete': 'success'
                    }.get(action_status, 'secondary')
                    
                    st.markdown(f"""
                    <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px;">
                        <div><strong>Action {i+1}:</strong> {action['action']}</div>
                        <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                            <div>Assigned to: {action['assigned_to']}</div>
                            <div>Due: {action['due_date']}</div>
                            <div>Status: <span class='crud-status crud-status-{action_status_class}'>{action_status}</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            if item.get('closed_date'):
                st.markdown(f"**Closed Date:** {item['closed_date']}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Attachments Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Attachments")
            
            if not item.get('attachments'):
                st.info("No attachments for this incident.")
                
                # Add attachment button
                if st.button("➕ Add Attachment", key=f"add_attachment_{base_key}"):
                    st.session_state[f'{base_key}_add_attachment'] = True
                    
                if st.session_state.get(f'{base_key}_add_attachment', False):
                    with st.form(f"attachment_form_{base_key}"):
                        file_name = st.text_input("File Name")
                        file_type = st.selectbox("File Type", options=["PDF", "DOC", "JPG", "PNG", "Other"])
                        file_description = st.text_input("Description")
                        
                        attachment_actions = st.columns([1, 1])
                        with attachment_actions[0]:
                            save_attachment = st.form_submit_button("Save Attachment")
                        with attachment_actions[1]:
                            cancel_attachment = st.form_submit_button("Cancel")
                        
                        if save_attachment and file_name:
                            # Add attachment to the item
                            new_attachment = {
                                'name': file_name,
                                'type': file_type,
                                'description': file_description,
                                'date_added': datetime.now().strftime('%Y-%m-%d'),
                                'added_by': "Current User"
                            }
                            
                            attachments = item.get('attachments', [])
                            attachments.append(new_attachment)
                            
                            # Update item with new attachment
                            item['attachments'] = attachments
                            self._save_item(item)
                            
                            st.success("Attachment added successfully")
                            st.session_state[f'{base_key}_add_attachment'] = False
                            st.rerun()
                        
                        if cancel_attachment:
                            st.session_state[f'{base_key}_add_attachment'] = False
                            st.rerun()
            else:
                # Display attachments
                for i, attachment in enumerate(item.get('attachments', [])):
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    with col1:
                        st.markdown(f"**{attachment['name']}**")
                    with col2:
                        st.markdown(f"Type: {attachment['type']}")
                    with col3:
                        st.markdown(f"Added: {attachment['date_added']}")
                    with col4:
                        if st.button("📄 View", key=f"view_attachment_{i}_{base_key}"):
                            st.info(f"Viewing {attachment['name']} (Demo Mode)")
                    
                    if attachment.get('description'):
                        st.markdown(f"_{attachment['description']}_")
                    
                    if i < len(item.get('attachments', [])) - 1:
                        st.markdown("---")
                
                # Add attachment button
                if st.button("➕ Add Attachment", key=f"add_attachment_{base_key}"):
                    st.session_state[f'{base_key}_add_attachment'] = True
                    
                if st.session_state.get(f'{base_key}_add_attachment', False):
                    with st.form(f"attachment_form_{base_key}"):
                        file_name = st.text_input("File Name")
                        file_type = st.selectbox("File Type", options=["PDF", "DOC", "JPG", "PNG", "Other"])
                        file_description = st.text_input("Description")
                        
                        attachment_actions = st.columns([1, 1])
                        with attachment_actions[0]:
                            save_attachment = st.form_submit_button("Save Attachment")
                        with attachment_actions[1]:
                            cancel_attachment = st.form_submit_button("Cancel")
                        
                        if save_attachment and file_name:
                            # Add attachment to the item
                            new_attachment = {
                                'name': file_name,
                                'type': file_type,
                                'description': file_description,
                                'date_added': datetime.now().strftime('%Y-%m-%d'),
                                'added_by': "Current User"
                            }
                            
                            attachments = item.get('attachments', [])
                            attachments.append(new_attachment)
                            
                            # Update item with new attachment
                            item['attachments'] = attachments
                            self._save_item(item)
                            
                            st.success("Attachment added successfully")
                            st.session_state[f'{base_key}_add_attachment'] = False
                            st.rerun()
                        
                        if cancel_attachment:
                            st.session_state[f'{base_key}_add_attachment'] = False
                            st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        end_crud_detail_container()