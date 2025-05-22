"""
Submittal Packages Module for gcPanel

This module implements the Submittal Packages functionality for the Engineering section,
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

class SubmittalPackageModule(CrudModule):
    def __init__(self):
        """Initialize the Submittal Packages module with configuration."""
        super().__init__(
            module_name="Submittal Packages",
            data_file_path="data/engineering/submittal_packages.json",
            id_field="submittal_id",
            list_columns=["submittal_id", "title", "spec_section", "subcontractor", "status", "due_date"],
            default_sort_field="submittal_id",
            default_sort_direction="desc",
            status_field="status",
            filter_options=["Draft", "Submitted", "Approved", "Approved as Noted", "Revise and Resubmit", "Rejected"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        spec_sections = [
            "03 30 00 - Cast-in-Place Concrete", 
            "05 12 00 - Structural Steel Framing", 
            "07 21 00 - Thermal Insulation",
            "08 11 13 - Hollow Metal Doors and Frames", 
            "09 29 00 - Gypsum Board", 
            "22 40 00 - Plumbing Fixtures",
            "23 37 13 - Diffusers, Registers, and Grilles", 
            "26 51 00 - Interior Lighting", 
            "27 51 23 - Intercommunication System",
            "32 31 13 - Chain Link Fences and Gates"
        ]
        
        subcontractors = [
            "ABC Concrete", "Steel Solutions Inc.", "Insulation Masters", 
            "Door Systems Inc.", "Drywall Experts", "Plumbing Specialists",
            "HVAC Contractors", "Electrical Solutions", "Communications Group",
            "Fence and Gate Co."
        ]
        
        statuses = ["Draft", "Submitted", "Approved", "Approved as Noted", "Revise and Resubmit", "Rejected"]
        
        demo_items = []
        
        # Create sample submittal packages
        for i in range(1, 21):
            # Set dates
            created_date = datetime.now() - timedelta(days=random.randint(10, 90))
            due_date = created_date + timedelta(days=random.randint(14, 30))
            submitted_date = None
            reviewed_date = None
            
            # Determine status and set dates accordingly
            status = random.choice(statuses)
            if status != "Draft":
                submitted_date = created_date + timedelta(days=random.randint(3, 10))
                
                if status in ["Approved", "Approved as Noted", "Revise and Resubmit", "Rejected"]:
                    reviewed_date = submitted_date + timedelta(days=random.randint(3, 14))
            
            # Select spec section and subcontractor
            section_idx = (i - 1) % len(spec_sections)
            spec_section = spec_sections[section_idx]
            subcontractor = subcontractors[section_idx]
            
            # Create random revision number
            revision = 0 if random.random() < 0.7 else random.randint(1, 3)
            
            # Create the submittal package
            item = {
                'submittal_id': f'SUB-{i:03d}',
                'title': f'Submittal for {spec_section.split(" - ")[1]}',
                'spec_section': spec_section,
                'subcontractor': subcontractor,
                'description': f'Submittal package for {spec_section}',
                'status': status,
                'revision': revision,
                'created_date': created_date.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d'),
                'submitted_date': submitted_date.strftime('%Y-%m-%d') if submitted_date else None,
                'reviewed_date': reviewed_date.strftime('%Y-%m-%d') if reviewed_date else None,
                'reviewer': "Jane Doe" if reviewed_date else None,
                'review_comments': f"Sample review comments for {spec_section}" if reviewed_date else None,
                'attachments': [],
                'response_attachments': []
            }
            
            demo_items.append(item)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _create_new_item_template(self):
        """Create a template for a new submittal package with default values."""
        submittal_id = self._generate_new_id()
        
        # Set default dates
        today = datetime.now()
        due_date = today + timedelta(days=21)
        
        return {
            'submittal_id': f'SUB-{int(submittal_id):03d}',
            'title': '',
            'spec_section': '',
            'subcontractor': '',
            'description': '',
            'status': 'Draft',
            'revision': 0,
            'created_date': today.strftime('%Y-%m-%d'),
            'due_date': due_date.strftime('%Y-%m-%d'),
            'submitted_date': None,
            'reviewed_date': None,
            'reviewer': None,
            'review_comments': None,
            'attachments': [],
            'response_attachments': []
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for submittal packages."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            submittal_id = item.get('submittal_id', '')
            if submittal_id.startswith('SUB-'):
                try:
                    num = int(submittal_id.split('-')[1])
                    max_id = max(max_id, num)
                except:
                    pass
        
        return str(max_id + 1)
    
    def _get_status_class(self, status):
        """Get the status class for a given status value."""
        status_classes = {
            'Draft': 'secondary',
            'Submitted': 'info',
            'Approved': 'success',
            'Approved as Noted': 'primary',
            'Revise and Resubmit': 'warning',
            'Rejected': 'danger'
        }
        return status_classes.get(status, 'secondary')
    
    def render_detail_view(self):
        """Render the detail view for creating, viewing, or editing a submittal package."""
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = "New Submittal Package"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Submittal Package with ID {item_id} not found")
                return
            detail_title = f"{item.get('title', item.get('submittal_id', 'Submittal Package'))}"
        
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
                    st.warning("Are you sure you want to delete this submittal package?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key=f"confirm_delete_{base_key}"):
                            self._delete_item(item['submittal_id'])
                            st.success("Submittal package deleted successfully")
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
                        submittal_id = st.text_input("Submittal ID", value=item['submittal_id'], disabled=not is_new)
                    with col2:
                        title = st.text_input("Title", value=item['title'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        spec_section = st.text_input("Specification Section", value=item['spec_section'])
                    with col2:
                        subcontractor = st.text_input("Subcontractor", value=item['subcontractor'])
                    
                    description = st.text_area("Description", value=item['description'], height=100)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        status = st.selectbox("Status", options=[
                            'Draft', 'Submitted', 'Approved', 'Approved as Noted', 'Revise and Resubmit', 'Rejected'
                        ], index=['Draft', 'Submitted', 'Approved', 'Approved as Noted', 'Revise and Resubmit', 'Rejected'].index(
                            item['status'] if item['status'] in ['Draft', 'Submitted', 'Approved', 'Approved as Noted', 'Revise and Resubmit', 'Rejected'] 
                            else 'Draft')
                        )
                    with col2:
                        revision = st.number_input("Revision", 
                                               value=int(item['revision']) if item.get('revision') is not None else 0,
                                               min_value=0,
                                               step=1)
                
                render_crud_fieldset("Basic Information", render_basic_info)
                
                # Dates Section
                def render_dates():
                    col1, col2 = st.columns(2)
                    with col1:
                        created_date = st.date_input("Created Date", 
                            value=datetime.strptime(item['created_date'], '%Y-%m-%d') if item['created_date'] else datetime.now()
                        )
                    with col2:
                        due_date = st.date_input("Due Date", 
                            value=datetime.strptime(item['due_date'], '%Y-%m-%d') if item['due_date'] else (datetime.now() + timedelta(days=21))
                        )
                    
                    # Only show submitted date if status is not Draft
                    if status != 'Draft':
                        col1, col2 = st.columns(2)
                        with col1:
                            submitted_date = st.date_input("Submitted Date", 
                                value=datetime.strptime(item['submitted_date'], '%Y-%m-%d') if item.get('submitted_date') else datetime.now()
                            )
                    else:
                        submitted_date = None
                    
                    # Only show review fields if status is not Draft or Submitted
                    if status not in ['Draft', 'Submitted']:
                        col1, col2 = st.columns(2)
                        with col1:
                            reviewed_date = st.date_input("Reviewed Date", 
                                value=datetime.strptime(item['reviewed_date'], '%Y-%m-%d') if item.get('reviewed_date') else datetime.now()
                            )
                        with col2:
                            reviewer = st.text_input("Reviewer", value=item.get('reviewer', ''))
                        
                        review_comments = st.text_area("Review Comments", value=item.get('review_comments', ''), height=100)
                    else:
                        reviewed_date = None
                        reviewer = None
                        review_comments = None
                
                render_crud_fieldset("Dates and Review", render_dates)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Submittal Package",
                    cancel_label="Cancel",
                    delete_label="Delete Submittal Package",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Update item with form values
                    updated_item = {
                        'submittal_id': submittal_id,
                        'title': title,
                        'spec_section': spec_section,
                        'subcontractor': subcontractor,
                        'description': description,
                        'status': status,
                        'revision': int(revision),
                        'created_date': created_date.strftime('%Y-%m-%d'),
                        'due_date': due_date.strftime('%Y-%m-%d'),
                        'submitted_date': submitted_date.strftime('%Y-%m-%d') if submitted_date else None,
                        'reviewed_date': reviewed_date.strftime('%Y-%m-%d') if reviewed_date else None,
                        'reviewer': reviewer,
                        'review_comments': review_comments,
                        'attachments': item.get('attachments', []),
                        'response_attachments': item.get('response_attachments', [])
                    }
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Submittal package saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['submittal_id'])
                    st.success("Submittal package deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            # Basic Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Basic Information")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Submittal ID:** {item['submittal_id']}")
            with col2:
                st.markdown(f"**Title:** {item['title']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Specification Section:** {item['spec_section']}")
            with col2:
                st.markdown(f"**Subcontractor:** {item['subcontractor']}")
            
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
                st.markdown(f"**Revision:** {item['revision']}")
            
            if item.get('description'):
                st.markdown(f"**Description:**")
                st.markdown(f"```{item['description']}```")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Dates and Review Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Dates and Review")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Created Date:** {item['created_date']}")
            with col2:
                st.markdown(f"**Due Date:** {item['due_date']}")
            
            if item.get('submitted_date'):
                st.markdown(f"**Submitted Date:** {item['submitted_date']}")
            
            if item.get('reviewed_date'):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Reviewed Date:** {item['reviewed_date']}")
                with col2:
                    st.markdown(f"**Reviewer:** {item.get('reviewer', 'Unknown')}")
                
                if item.get('review_comments'):
                    st.markdown(f"**Review Comments:**")
                    st.markdown(f"```{item['review_comments']}```")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Attachments Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Attachments")
            
            if not item.get('attachments'):
                st.info("No attachments uploaded.")
                
                # Add attachment button
                if st.button("➕ Add Attachment", key=f"add_attachment_{base_key}"):
                    st.session_state[f'{base_key}_add_attachment'] = True
                    
                if st.session_state.get(f'{base_key}_add_attachment', False):
                    with st.form(f"attachment_form_{base_key}"):
                        file_name = st.text_input("File Name")
                        file_type = st.selectbox("File Type", options=["PDF", "DWG", "XLS", "DOC", "Other"])
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
                attachments = item.get('attachments', [])
                for i, attachment in enumerate(attachments):
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
                    
                    if i < len(attachments) - 1:
                        st.markdown("---")
                
                # Add attachment button
                if st.button("➕ Add Attachment", key=f"add_attachment_{base_key}"):
                    st.session_state[f'{base_key}_add_attachment'] = True
                    
                if st.session_state.get(f'{base_key}_add_attachment', False):
                    with st.form(f"attachment_form_{base_key}"):
                        file_name = st.text_input("File Name")
                        file_type = st.selectbox("File Type", options=["PDF", "DWG", "XLS", "DOC", "Other"])
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
            
            # Response Attachments Section (if status indicates reviewed)
            if item['status'] in ['Approved', 'Approved as Noted', 'Revise and Resubmit', 'Rejected']:
                st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
                st.subheader("Response Attachments")
                
                if not item.get('response_attachments'):
                    st.info("No response attachments uploaded.")
                    
                    # Add response attachment button
                    if st.button("➕ Add Response", key=f"add_response_{base_key}"):
                        st.session_state[f'{base_key}_add_response'] = True
                        
                    if st.session_state.get(f'{base_key}_add_response', False):
                        with st.form(f"response_form_{base_key}"):
                            file_name = st.text_input("File Name")
                            file_type = st.selectbox("File Type", options=["PDF", "DWG", "XLS", "DOC", "Other"])
                            file_description = st.text_input("Description")
                            
                            response_actions = st.columns([1, 1])
                            with response_actions[0]:
                                save_response = st.form_submit_button("Save Response")
                            with response_actions[1]:
                                cancel_response = st.form_submit_button("Cancel")
                            
                            if save_response and file_name:
                                # Add response to the item
                                new_response = {
                                    'name': file_name,
                                    'type': file_type,
                                    'description': file_description,
                                    'date_added': datetime.now().strftime('%Y-%m-%d'),
                                    'added_by': "Current User"
                                }
                                
                                responses = item.get('response_attachments', [])
                                responses.append(new_response)
                                
                                # Update item with new response
                                item['response_attachments'] = responses
                                self._save_item(item)
                                
                                st.success("Response attachment added successfully")
                                st.session_state[f'{base_key}_add_response'] = False
                                st.rerun()
                            
                            if cancel_response:
                                st.session_state[f'{base_key}_add_response'] = False
                                st.rerun()
                else:
                    # Display response attachments
                    responses = item.get('response_attachments', [])
                    for i, response in enumerate(responses):
                        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                        with col1:
                            st.markdown(f"**{response['name']}**")
                        with col2:
                            st.markdown(f"Type: {response['type']}")
                        with col3:
                            st.markdown(f"Added: {response['date_added']}")
                        with col4:
                            if st.button("📄 View", key=f"view_response_{i}_{base_key}"):
                                st.info(f"Viewing {response['name']} (Demo Mode)")
                        
                        if response.get('description'):
                            st.markdown(f"_{response['description']}_")
                        
                        if i < len(responses) - 1:
                            st.markdown("---")
                    
                    # Add response attachment button
                    if st.button("➕ Add Response", key=f"add_response_{base_key}"):
                        st.session_state[f'{base_key}_add_response'] = True
                        
                    if st.session_state.get(f'{base_key}_add_response', False):
                        with st.form(f"response_form_{base_key}"):
                            file_name = st.text_input("File Name")
                            file_type = st.selectbox("File Type", options=["PDF", "DWG", "XLS", "DOC", "Other"])
                            file_description = st.text_input("Description")
                            
                            response_actions = st.columns([1, 1])
                            with response_actions[0]:
                                save_response = st.form_submit_button("Save Response")
                            with response_actions[1]:
                                cancel_response = st.form_submit_button("Cancel")
                            
                            if save_response and file_name:
                                # Add response to the item
                                new_response = {
                                    'name': file_name,
                                    'type': file_type,
                                    'description': file_description,
                                    'date_added': datetime.now().strftime('%Y-%m-%d'),
                                    'added_by': "Current User"
                                }
                                
                                responses = item.get('response_attachments', [])
                                responses.append(new_response)
                                
                                # Update item with new response
                                item['response_attachments'] = responses
                                self._save_item(item)
                                
                                st.success("Response attachment added successfully")
                                st.session_state[f'{base_key}_add_response'] = False
                                st.rerun()
                            
                            if cancel_response:
                                st.session_state[f'{base_key}_add_response'] = False
                                st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        end_crud_detail_container()

def render():
    """Render the Submittal Packages module."""
    st.title("Submittal Packages")
    
    # Create and render the Submittal Packages module
    submittal_packages = SubmittalPackageModule()
    submittal_packages.render()