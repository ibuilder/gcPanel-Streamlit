"""
Field Issues Module for gcPanel

This module implements the Field Issues functionality for the Field Operations section,
using the standardized CRUD template for consistent styling and behavior.
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

class FieldIssueModule(CrudModule):
    def __init__(self):
        """Initialize the Field Issues module with configuration."""
        super().__init__(
            module_name="Field Issues",
            data_file_path="data/field_operations/field_issues.json",
            id_field="issue_id",
            list_columns=["issue_id", "title", "location", "priority", "status", "due_date"],
            default_sort_field="due_date",
            default_sort_direction="asc",
            status_field="status",
            filter_options=["Open", "In Progress", "Resolved", "Closed", "Pending Review"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        locations = [
            "Level 1 - East Wing", "Level 2 - North Corridor", "Level 3 - South Wing", 
            "Level 4 - Mechanical Room", "Level 5 - Unit 502", "Basement - Parking",
            "Roof - HVAC Units", "Exterior - West Facade", "Lobby - Main Entrance",
            "Site - North Excavation"
        ]
        
        titles = [
            "Water leak in ceiling", "Incorrect electrical outlet placement", 
            "Drywall damage during installation", "Misaligned door frame",
            "Missing fire stop", "Damaged flooring material", "Incorrect paint color",
            "Insufficient backing for handrail", "MEP coordination issue",
            "Exterior drainage issue", "Concrete crack in foundation"
        ]
        
        priorities = ["Low", "Medium", "High", "Critical"]
        statuses = ["Open", "In Progress", "Resolved", "Closed", "Pending Review"]
        
        assignees = ["John Smith", "Jane Doe", "Bob Johnson", "Alice Williams", "Mike Brown"]
        reporters = ["David Wilson", "Sarah Davis", "Robert Miller", "Emily Clark", "Mark Taylor"]
        
        demo_items = []
        
        # Create sample field issues
        for i in range(1, 21):
            # Set dates
            created_date = datetime.now() - timedelta(days=random.randint(1, 30))
            due_date = created_date + timedelta(days=random.randint(3, 14))
            
            # Determine status and set resolution date accordingly
            status = random.choice(statuses)
            resolution_date = None
            resolution_notes = None
            
            if status in ["Resolved", "Closed"]:
                resolution_date = created_date + timedelta(days=random.randint(1, 10))
                resolution_notes = f"Issue was resolved by {random.choice(assignees)}. {random.choice(['Required material replacement.', 'Repaired damaged area.', 'Reinstalled correctly.', 'Coordinated with subcontractor.'])}"
            
            # Create the issue
            issue = {
                'issue_id': f'ISS-{i:03d}',
                'title': random.choice(titles),
                'description': f"Detailed description of the issue #{i}. This explains what was found and what needs to be corrected.",
                'location': random.choice(locations),
                'priority': random.choice(priorities),
                'status': status,
                'created_date': created_date.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d'),
                'reported_by': random.choice(reporters),
                'assigned_to': random.choice(assignees),
                'resolution_date': resolution_date.strftime('%Y-%m-%d') if resolution_date else None,
                'resolution_notes': resolution_notes,
                'photos': [],
                'related_documents': []
            }
            
            demo_items.append(issue)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _create_new_item_template(self):
        """Create a template for a new field issue with default values."""
        issue_id = self._generate_new_id()
        
        # Set default dates
        today = datetime.now()
        due_date = today + timedelta(days=7)
        
        return {
            'issue_id': f'ISS-{int(issue_id):03d}',
            'title': '',
            'description': '',
            'location': '',
            'priority': 'Medium',
            'status': 'Open',
            'created_date': today.strftime('%Y-%m-%d'),
            'due_date': due_date.strftime('%Y-%m-%d'),
            'reported_by': '',
            'assigned_to': '',
            'resolution_date': None,
            'resolution_notes': None,
            'photos': [],
            'related_documents': []
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for field issues."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            issue_id = item.get('issue_id', '')
            if issue_id.startswith('ISS-'):
                try:
                    num = int(issue_id.split('-')[1])
                    max_id = max(max_id, num)
                except:
                    pass
        
        return str(max_id + 1)
    
    def _get_status_class(self, status):
        """Get the status class for a given status value."""
        status_classes = {
            'Open': 'warning',
            'In Progress': 'info',
            'Resolved': 'success',
            'Closed': 'secondary',
            'Pending Review': 'primary'
        }
        return status_classes.get(status, 'secondary')
    
    def _get_priority_class(self, priority):
        """Get the priority class for a given priority value."""
        priority_classes = {
            'Low': 'secondary',
            'Medium': 'info',
            'High': 'warning',
            'Critical': 'danger'
        }
        return priority_classes.get(priority, 'secondary')
    
    def render_detail_view(self):
        """Render the detail view for creating, viewing, or editing a field issue."""
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = "New Field Issue"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Field Issue with ID {item_id} not found")
                return
            detail_title = f"{item.get('title', item.get('issue_id', 'Field Issue'))}"
        
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
            col1, col2, col3 = st.columns([1, 1, 6])
            with col1:
                if st.button("✏️ Edit", type="primary", key=f"edit_{base_key}_action"):
                    st.session_state[f'{base_key}_edit_mode'] = True
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", type="secondary", key=f"delete_{base_key}_action"):
                    st.warning("Are you sure you want to delete this field issue?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key=f"confirm_delete_{base_key}"):
                            self._delete_item(item['issue_id'])
                            st.success("Field issue deleted successfully")
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
                        issue_id = st.text_input("Issue ID", value=item['issue_id'], disabled=not is_new)
                    with col2:
                        title = st.text_input("Title", value=item['title'])
                    
                    description = st.text_area("Description", value=item['description'], height=100)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        location = st.text_input("Location", value=item['location'])
                    with col2:
                        priority = st.selectbox("Priority", options=[
                            'Low', 'Medium', 'High', 'Critical'
                        ], index=['Low', 'Medium', 'High', 'Critical'].index(
                            item['priority'] if item['priority'] in ['Low', 'Medium', 'High', 'Critical'] 
                            else 'Medium')
                        )
                    
                    status = st.selectbox("Status", options=[
                        'Open', 'In Progress', 'Resolved', 'Closed', 'Pending Review'
                    ], index=['Open', 'In Progress', 'Resolved', 'Closed', 'Pending Review'].index(
                        item['status'] if item['status'] in ['Open', 'In Progress', 'Resolved', 'Closed', 'Pending Review'] 
                        else 'Open')
                    )
                
                render_crud_fieldset("Basic Information", render_basic_info)
                
                # Assignment Section
                def render_assignment():
                    col1, col2 = st.columns(2)
                    with col1:
                        created_date = st.date_input(
                            "Created Date", 
                            value=datetime.strptime(item['created_date'], '%Y-%m-%d') if item['created_date'] else datetime.now()
                        )
                    with col2:
                        due_date = st.date_input(
                            "Due Date", 
                            value=datetime.strptime(item['due_date'], '%Y-%m-%d') if item['due_date'] else (datetime.now() + timedelta(days=7))
                        )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        reported_by = st.text_input("Reported By", value=item['reported_by'])
                    with col2:
                        assigned_to = st.text_input("Assigned To", value=item['assigned_to'])
                
                render_crud_fieldset("Assignment", render_assignment)
                
                # Resolution Section (if status is Resolved or Closed)
                def render_resolution():
                    show_resolution = status in ['Resolved', 'Closed']
                    
                    if show_resolution:
                        resolution_date = st.date_input(
                            "Resolution Date", 
                            value=datetime.strptime(item['resolution_date'], '%Y-%m-%d') if item.get('resolution_date') else datetime.now()
                        )
                        
                        resolution_notes = st.text_area(
                            "Resolution Notes", 
                            value=item.get('resolution_notes', ''),
                            height=100
                        )
                    else:
                        resolution_date = None
                        resolution_notes = None
                        
                        st.info("Resolution details will be available when the issue status is set to 'Resolved' or 'Closed'.")
                    
                    return resolution_date, resolution_notes, show_resolution
                
                resolution_date, resolution_notes, show_resolution = render_crud_fieldset("Resolution", render_resolution)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Field Issue",
                    cancel_label="Cancel",
                    delete_label="Delete Field Issue",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Update item with form values
                    updated_item = {
                        'issue_id': issue_id,
                        'title': title,
                        'description': description,
                        'location': location,
                        'priority': priority,
                        'status': status,
                        'created_date': created_date.strftime('%Y-%m-%d'),
                        'due_date': due_date.strftime('%Y-%m-%d'),
                        'reported_by': reported_by,
                        'assigned_to': assigned_to,
                        'resolution_date': resolution_date.strftime('%Y-%m-%d') if resolution_date and show_resolution else None,
                        'resolution_notes': resolution_notes if show_resolution else None,
                        'photos': item.get('photos', []),
                        'related_documents': item.get('related_documents', [])
                    }
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Field issue saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['issue_id'])
                    st.success("Field issue deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            # Basic Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Basic Information")
            
            # Issue ID and Title
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Issue ID:** {item['issue_id']}")
            with col2:
                st.markdown(f"**Title:** {item['title']}")
            
            # Status and Priority with styling
            col1, col2 = st.columns(2)
            with col1:
                status_html = f"""
                <div style="display: flex; align-items: center; background: transparent;">
                    <span class='crud-status crud-status-{self._get_status_class(item['status'])}' style="outline: none; box-shadow: none; border: none;">{item['status']}</span>
                </div>
                """
                st.markdown("**Status:**")
                st.markdown(status_html, unsafe_allow_html=True)
            
            with col2:
                priority_html = f"""
                <div style="display: flex; align-items: center; background: transparent;">
                    <span class='crud-status crud-status-{self._get_priority_class(item['priority'])}' style="outline: none; box-shadow: none; border: none;">{item['priority']}</span>
                </div>
                """
                st.markdown("**Priority:**")
                st.markdown(priority_html, unsafe_allow_html=True)
            
            # Location
            st.markdown(f"**Location:** {item['location']}")
            
            # Description
            if item.get('description'):
                st.markdown(f"**Description:**")
                st.markdown(f"```{item['description']}```")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Assignment Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Assignment")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Created Date:** {item['created_date']}")
            with col2:
                st.markdown(f"**Due Date:** {item['due_date']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Reported By:** {item['reported_by']}")
            with col2:
                st.markdown(f"**Assigned To:** {item['assigned_to']}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Resolution Section (if resolved or closed)
            if item['status'] in ['Resolved', 'Closed'] and (item.get('resolution_date') or item.get('resolution_notes')):
                st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
                st.subheader("Resolution")
                
                if item.get('resolution_date'):
                    st.markdown(f"**Resolution Date:** {item['resolution_date']}")
                
                if item.get('resolution_notes'):
                    st.markdown(f"**Resolution Notes:**")
                    st.markdown(f"```{item['resolution_notes']}```")
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Photos Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Photos")
            
            if not item.get('photos'):
                st.info("No photos attached to this issue.")
                
                # Add photo button
                if st.button("➕ Add Photo", key=f"add_photo_{base_key}"):
                    st.session_state[f'{base_key}_add_photo'] = True
                    
                if st.session_state.get(f'{base_key}_add_photo', False):
                    with st.form(f"photo_form_{base_key}"):
                        photo_title = st.text_input("Photo Title")
                        photo_description = st.text_input("Description")
                        
                        photo_actions = st.columns([1, 1])
                        with photo_actions[0]:
                            save_photo = st.form_submit_button("Save Photo")
                        with photo_actions[1]:
                            cancel_photo = st.form_submit_button("Cancel")
                        
                        if save_photo and photo_title:
                            # Add photo to the item
                            new_photo = {
                                'title': photo_title,
                                'description': photo_description,
                                'date_added': datetime.now().strftime('%Y-%m-%d'),
                                'added_by': "Current User"
                            }
                            
                            photos = item.get('photos', [])
                            photos.append(new_photo)
                            
                            # Update item with new photo
                            item['photos'] = photos
                            self._save_item(item)
                            
                            st.success("Photo added successfully")
                            st.session_state[f'{base_key}_add_photo'] = False
                            st.rerun()
                        
                        if cancel_photo:
                            st.session_state[f'{base_key}_add_photo'] = False
                            st.rerun()
            else:
                # Display photos
                photos = item.get('photos', [])
                photo_cols = st.columns(min(len(photos), 3))
                
                for i, photo in enumerate(photos):
                    with photo_cols[i % len(photo_cols)]:
                        st.markdown(f"**{photo['title']}**")
                        st.image("https://via.placeholder.com/300x200.png?text=Issue+Photo", caption=photo['description'])
                        st.markdown(f"Added: {photo['date_added']} by {photo['added_by']}")
                
                # Add photo button
                if st.button("➕ Add Photo", key=f"add_photo_{base_key}"):
                    st.session_state[f'{base_key}_add_photo'] = True
                    
                if st.session_state.get(f'{base_key}_add_photo', False):
                    with st.form(f"photo_form_{base_key}"):
                        photo_title = st.text_input("Photo Title")
                        photo_description = st.text_input("Description")
                        
                        photo_actions = st.columns([1, 1])
                        with photo_actions[0]:
                            save_photo = st.form_submit_button("Save Photo")
                        with photo_actions[1]:
                            cancel_photo = st.form_submit_button("Cancel")
                        
                        if save_photo and photo_title:
                            # Add photo to the item
                            new_photo = {
                                'title': photo_title,
                                'description': photo_description,
                                'date_added': datetime.now().strftime('%Y-%m-%d'),
                                'added_by': "Current User"
                            }
                            
                            photos = item.get('photos', [])
                            photos.append(new_photo)
                            
                            # Update item with new photo
                            item['photos'] = photos
                            self._save_item(item)
                            
                            st.success("Photo added successfully")
                            st.session_state[f'{base_key}_add_photo'] = False
                            st.rerun()
                        
                        if cancel_photo:
                            st.session_state[f'{base_key}_add_photo'] = False
                            st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Related Documents Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Related Documents")
            
            if not item.get('related_documents'):
                st.info("No related documents attached to this issue.")
                
                # Add document button
                if st.button("➕ Add Document", key=f"add_doc_{base_key}"):
                    st.session_state[f'{base_key}_add_doc'] = True
                    
                if st.session_state.get(f'{base_key}_add_doc', False):
                    with st.form(f"doc_form_{base_key}"):
                        doc_title = st.text_input("Document Title")
                        doc_type = st.selectbox("Document Type", options=["Drawing", "Specification", "RFI", "Submittal", "Other"])
                        doc_reference = st.text_input("Reference Number")
                        
                        doc_actions = st.columns([1, 1])
                        with doc_actions[0]:
                            save_doc = st.form_submit_button("Save Document")
                        with doc_actions[1]:
                            cancel_doc = st.form_submit_button("Cancel")
                        
                        if save_doc and doc_title:
                            # Add document to the item
                            new_doc = {
                                'title': doc_title,
                                'type': doc_type,
                                'reference': doc_reference,
                                'date_added': datetime.now().strftime('%Y-%m-%d'),
                                'added_by': "Current User"
                            }
                            
                            docs = item.get('related_documents', [])
                            docs.append(new_doc)
                            
                            # Update item with new document
                            item['related_documents'] = docs
                            self._save_item(item)
                            
                            st.success("Document added successfully")
                            st.session_state[f'{base_key}_add_doc'] = False
                            st.rerun()
                        
                        if cancel_doc:
                            st.session_state[f'{base_key}_add_doc'] = False
                            st.rerun()
            else:
                # Display documents
                docs = item.get('related_documents', [])
                for i, doc in enumerate(docs):
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.markdown(f"**{doc['title']}**")
                    with col2:
                        st.markdown(f"Type: {doc['type']} | Ref: {doc['reference']}")
                    with col3:
                        if st.button("📄 View", key=f"view_doc_{i}_{base_key}"):
                            st.info(f"Viewing {doc['title']} (Demo Mode)")
                    
                    if i < len(docs) - 1:
                        st.markdown("---")
                
                # Add document button
                if st.button("➕ Add Document", key=f"add_doc_{base_key}"):
                    st.session_state[f'{base_key}_add_doc'] = True
                    
                if st.session_state.get(f'{base_key}_add_doc', False):
                    with st.form(f"doc_form_{base_key}"):
                        doc_title = st.text_input("Document Title")
                        doc_type = st.selectbox("Document Type", options=["Drawing", "Specification", "RFI", "Submittal", "Other"])
                        doc_reference = st.text_input("Reference Number")
                        
                        doc_actions = st.columns([1, 1])
                        with doc_actions[0]:
                            save_doc = st.form_submit_button("Save Document")
                        with doc_actions[1]:
                            cancel_doc = st.form_submit_button("Cancel")
                        
                        if save_doc and doc_title:
                            # Add document to the item
                            new_doc = {
                                'title': doc_title,
                                'type': doc_type,
                                'reference': doc_reference,
                                'date_added': datetime.now().strftime('%Y-%m-%d'),
                                'added_by': "Current User"
                            }
                            
                            docs = item.get('related_documents', [])
                            docs.append(new_doc)
                            
                            # Update item with new document
                            item['related_documents'] = docs
                            self._save_item(item)
                            
                            st.success("Document added successfully")
                            st.session_state[f'{base_key}_add_doc'] = False
                            st.rerun()
                        
                        if cancel_doc:
                            st.session_state[f'{base_key}_add_doc'] = False
                            st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        end_crud_detail_container()

def render():
    """Render the Field Issues module."""
    st.title("Field Issues")
    
    # Create and render the Field Issues module
    field_issues = FieldIssueModule()
    field_issues.render()