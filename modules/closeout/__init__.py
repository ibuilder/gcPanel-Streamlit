"""
Closeout Module for gcPanel

This module provides project closeout functionality for the construction management dashboard,
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

class CloseoutItemModule(CrudModule):
    def __init__(self):
        """Initialize the Closeout Items module with configuration."""
        super().__init__(
            module_name="Closeout Items",
            data_file_path="data/closeout/closeout_items.json",
            id_field="item_id",
            list_columns=["item_id", "category", "title", "responsible_party", "due_date", "status"],
            default_sort_field="due_date",
            default_sort_direction="asc",
            status_field="status",
            filter_options=["Not Started", "In Progress", "Submitted", "Approved", "Complete", "Overdue"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        categories = [
            "Operation & Maintenance Manuals", 
            "Warranties", 
            "As-Built Drawings", 
            "Certificates",
            "Training", 
            "Owner Turnover", 
            "Final Inspections", 
            "Final Payment",
            "Certificate of Occupancy", 
            "Final Cleaning"
        ]
        
        responsible_parties = [
            "General Contractor", 
            "Subcontractor", 
            "Owner", 
            "Architect",
            "MEP Engineer", 
            "Building Department", 
            "Fire Marshal"
        ]
        
        statuses = ["Not Started", "In Progress", "Submitted", "Approved", "Complete", "Overdue"]
        
        demo_items = []
        
        # Create sample closeout items
        for i in range(1, 31):
            category = random.choice(categories)
            
            # Set dates based on realistic timeframes
            created_date = datetime.now() - timedelta(days=random.randint(30, 90))
            due_date = created_date + timedelta(days=random.randint(14, 60))
            
            # Determine completion percentage and status
            completion_pct = 0
            status = "Not Started"
            completed_date = None
            
            # Set random status based on due date
            if due_date < datetime.now():
                # Past due date
                random_val = random.random()
                if random_val < 0.3:
                    status = "Overdue"
                    completion_pct = random.randint(0, 90)
                else:
                    status = random.choice(["Approved", "Complete"])
                    completion_pct = 100
                    completed_date = due_date - timedelta(days=random.randint(1, 10))
            else:
                # Not yet due
                random_val = random.random()
                if random_val < 0.2:
                    status = "Not Started"
                    completion_pct = 0
                elif random_val < 0.5:
                    status = "In Progress"
                    completion_pct = random.randint(10, 75)
                elif random_val < 0.8:
                    status = "Submitted"
                    completion_pct = random.randint(80, 95)
                else:
                    status = random.choice(["Approved", "Complete"])
                    completion_pct = 100
                    completed_date = datetime.now() - timedelta(days=random.randint(1, 10))
            
            # Generate item based on category
            if category == "Operation & Maintenance Manuals":
                title = f"O&M Manual - {random.choice(['HVAC', 'Electrical', 'Plumbing', 'Fire Protection', 'Elevator'])}"
                description = f"Submit complete O&M manual for {title.split(' - ')[1]} systems"
                responsible_party = random.choice(["Subcontractor", "General Contractor"])
            elif category == "Warranties":
                title = f"Warranty - {random.choice(['Roofing', 'Windows', 'HVAC Equipment', 'Elevator', 'Flooring'])}"
                description = f"Submit manufacturer and installer warranties for {title.split(' - ')[1]}"
                responsible_party = "Subcontractor"
            elif category == "As-Built Drawings":
                title = f"As-Built - {random.choice(['Architectural', 'Structural', 'Mechanical', 'Electrical', 'Plumbing'])}"
                description = f"Submit complete as-built drawings for {title.split(' - ')[1]}"
                responsible_party = random.choice(["Architect", "Subcontractor", "MEP Engineer"])
            elif category == "Certificates":
                title = f"Certificate - {random.choice(['Fire Alarm', 'Elevator', 'Sprinkler System', 'Backflow', 'Pressure Test'])}"
                description = f"Obtain certificate for {title.split(' - ')[1]}"
                responsible_party = random.choice(["Subcontractor", "Building Department", "Fire Marshal"])
            elif category == "Training":
                title = f"Training - {random.choice(['HVAC Controls', 'Security System', 'Fire Alarm', 'Irrigation System', 'Lighting Controls'])}"
                description = f"Conduct owner training for {title.split(' - ')[1]}"
                responsible_party = "Subcontractor"
            elif category == "Owner Turnover":
                title = f"Turnover - {random.choice(['Keys', 'Access Cards', 'Attic Stock', 'Spare Parts', 'Extra Materials'])}"
                description = f"Provide {title.split(' - ')[1]} to owner"
                responsible_party = "General Contractor"
            elif category == "Final Inspections":
                title = f"Final Inspection - {random.choice(['Building', 'Electrical', 'Plumbing', 'Mechanical', 'Fire'])}"
                description = f"Schedule and pass final {title.split(' - ')[1]} inspection"
                responsible_party = random.choice(["General Contractor", "Building Department", "Fire Marshal"])
            elif category == "Final Payment":
                title = f"Final Payment - {random.choice(['Owner', 'Subcontractor', 'Vendor'])}"
                description = f"Process final payment to {title.split(' - ')[1]}"
                responsible_party = random.choice(["General Contractor", "Owner"])
            elif category == "Certificate of Occupancy":
                title = f"Certificate of Occupancy - {random.choice(['Temporary', 'Final', 'Partial'])}"
                description = f"Obtain {title.split(' - ')[1]} certificate of occupancy"
                responsible_party = random.choice(["General Contractor", "Building Department"])
            else:  # Final Cleaning
                title = f"Final Cleaning - {random.choice(['Interior', 'Exterior', 'Windows', 'Floors', 'Complete Building'])}"
                description = f"Complete {title.split(' - ')[1]} final cleaning"
                responsible_party = random.choice(["General Contractor", "Subcontractor"])
            
            # Create the closeout item
            item = {
                'item_id': f'CLO-{i:03d}',
                'category': category,
                'title': title,
                'description': description,
                'responsible_party': responsible_party,
                'created_date': created_date.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d'),
                'status': status,
                'completion_pct': completion_pct,
                'completed_date': completed_date.strftime('%Y-%m-%d') if completed_date else None,
                'notes': "" if random.random() < 0.7 else f"Follow up with {responsible_party} to ensure timely completion.",
                'attachments': []
            }
            
            demo_items.append(item)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _create_new_item_template(self):
        """Create a template for a new closeout item with default values."""
        item_id = self._generate_new_id()
        
        # Set default dates
        today = datetime.now()
        due_date = today + timedelta(days=30)
        
        return {
            'item_id': f'CLO-{int(item_id):03d}',
            'category': '',
            'title': '',
            'description': '',
            'responsible_party': '',
            'created_date': today.strftime('%Y-%m-%d'),
            'due_date': due_date.strftime('%Y-%m-%d'),
            'status': 'Not Started',
            'completion_pct': 0,
            'completed_date': None,
            'notes': '',
            'attachments': []
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for closeout items."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            item_id = item.get('item_id', '')
            if item_id.startswith('CLO-'):
                try:
                    num = int(item_id.split('-')[1])
                    max_id = max(max_id, num)
                except:
                    pass
        
        return str(max_id + 1)
    
    def _get_status_class(self, status):
        """Get the status class for a given status value."""
        status_classes = {
            'Not Started': 'secondary',
            'In Progress': 'info',
            'Submitted': 'primary',
            'Approved': 'success',
            'Complete': 'success',
            'Overdue': 'danger'
        }
        return status_classes.get(status, 'secondary')
    
    def render_detail_view(self):
        """Render the detail view for creating, viewing, or editing a closeout item."""
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = "New Closeout Item"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Closeout Item with ID {item_id} not found")
                return
            detail_title = f"{item.get('title', item.get('item_id', 'Closeout Item'))}"
        
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
                    st.info("This would generate a PDF version of the closeout item in a production environment.")
            with col3:
                if st.button("🗑️ Delete", type="secondary", key=f"delete_{base_key}_action"):
                    st.warning("Are you sure you want to delete this closeout item?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key=f"confirm_delete_{base_key}"):
                            self._delete_item(item['item_id'])
                            st.success("Closeout item deleted successfully")
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
                        item_id = st.text_input("Item ID", value=item['item_id'], disabled=not is_new)
                    with col2:
                        title = st.text_input("Title", value=item['title'])
                    
                    category = st.selectbox("Category", options=[
                        '', 'Operation & Maintenance Manuals', 'Warranties', 'As-Built Drawings', 
                        'Certificates', 'Training', 'Owner Turnover', 'Final Inspections', 
                        'Final Payment', 'Certificate of Occupancy', 'Final Cleaning'
                    ], index=['', 'Operation & Maintenance Manuals', 'Warranties', 'As-Built Drawings', 
                              'Certificates', 'Training', 'Owner Turnover', 'Final Inspections', 
                              'Final Payment', 'Certificate of Occupancy', 'Final Cleaning'].index(
                        item['category'] if item['category'] in ['', 'Operation & Maintenance Manuals', 'Warranties', 'As-Built Drawings', 
                                                               'Certificates', 'Training', 'Owner Turnover', 'Final Inspections', 
                                                               'Final Payment', 'Certificate of Occupancy', 'Final Cleaning'] 
                        else '')
                    )
                    
                    description = st.text_area("Description", value=item['description'], height=100)
                    
                    responsible_party = st.selectbox("Responsible Party", options=[
                        '', 'General Contractor', 'Subcontractor', 'Owner', 'Architect',
                        'MEP Engineer', 'Building Department', 'Fire Marshal'
                    ], index=['', 'General Contractor', 'Subcontractor', 'Owner', 'Architect',
                              'MEP Engineer', 'Building Department', 'Fire Marshal'].index(
                        item['responsible_party'] if item['responsible_party'] in ['', 'General Contractor', 'Subcontractor', 'Owner', 'Architect',
                                                                                 'MEP Engineer', 'Building Department', 'Fire Marshal'] 
                        else '')
                    )
                
                render_crud_fieldset("Basic Information", render_basic_info)
                
                # Status Section
                def render_status():
                    col1, col2 = st.columns(2)
                    with col1:
                        created_date = st.date_input(
                            "Created Date", 
                            value=datetime.strptime(item['created_date'], '%Y-%m-%d') if item['created_date'] else datetime.now()
                        )
                    with col2:
                        due_date = st.date_input(
                            "Due Date", 
                            value=datetime.strptime(item['due_date'], '%Y-%m-%d') if item['due_date'] else (datetime.now() + timedelta(days=30))
                        )
                    
                    status = st.selectbox("Status", options=[
                        'Not Started', 'In Progress', 'Submitted', 'Approved', 'Complete', 'Overdue'
                    ], index=['Not Started', 'In Progress', 'Submitted', 'Approved', 'Complete', 'Overdue'].index(
                        item['status'] if item['status'] in ['Not Started', 'In Progress', 'Submitted', 'Approved', 'Complete', 'Overdue'] 
                        else 'Not Started')
                    )
                    
                    completion_pct = st.slider("Completion Percentage", 
                                           min_value=0, 
                                           max_value=100, 
                                           value=int(item['completion_pct']) if item.get('completion_pct') is not None else 0,
                                           step=5)
                    
                    # Only show completed date if status is Complete or Approved
                    if status in ['Complete', 'Approved']:
                        completed_date = st.date_input(
                            "Completed Date", 
                            value=datetime.strptime(item['completed_date'], '%Y-%m-%d') if item.get('completed_date') else datetime.now()
                        )
                    else:
                        completed_date = None
                    
                    notes = st.text_area("Notes", value=item.get('notes', ''), height=100)
                    
                    return created_date, due_date, status, completion_pct, completed_date, notes
                
                created_date, due_date, status, completion_pct, completed_date, notes = render_crud_fieldset("Status", render_status)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Closeout Item",
                    cancel_label="Cancel",
                    delete_label="Delete Closeout Item",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Update item with form values
                    updated_item = {
                        'item_id': item_id,
                        'category': category,
                        'title': title,
                        'description': description,
                        'responsible_party': responsible_party,
                        'created_date': created_date.strftime('%Y-%m-%d'),
                        'due_date': due_date.strftime('%Y-%m-%d'),
                        'status': status,
                        'completion_pct': completion_pct,
                        'completed_date': completed_date.strftime('%Y-%m-%d') if completed_date else None,
                        'notes': notes,
                        'attachments': item.get('attachments', [])
                    }
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Closeout item saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['item_id'])
                    st.success("Closeout item deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            # Basic Information Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Basic Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Item ID:** {item['item_id']}")
            with col2:
                st.markdown(f"**Title:** {item['title']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Category:** {item['category']}")
            with col2:
                st.markdown(f"**Responsible Party:** {item['responsible_party']}")
            
            if item.get('description'):
                st.markdown(f"**Description:**")
                st.markdown(f"```{item['description']}```")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Status Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Status")
            
            # Show status with colored badge
            status_html = f"""
            <div style="display: flex; align-items: center; background: transparent;">
                <span class='crud-status crud-status-{self._get_status_class(item['status'])}' style="outline: none; box-shadow: none; border: none;">{item['status']}</span>
            </div>
            """
            st.markdown("**Status:**")
            st.markdown(status_html, unsafe_allow_html=True)
            
            # Show completion percentage as progress bar
            st.markdown(f"**Completion Percentage:** {item['completion_pct']}%")
            st.progress(float(item['completion_pct'])/100)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Created Date:** {item['created_date']}")
            with col2:
                st.markdown(f"**Due Date:** {item['due_date']}")
            
            if item.get('completed_date'):
                st.markdown(f"**Completed Date:** {item['completed_date']}")
            
            if item.get('notes'):
                st.markdown(f"**Notes:**")
                st.markdown(f"```{item['notes']}```")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Attachments Section
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Attachments")
            
            if not item.get('attachments'):
                st.info("No attachments for this closeout item.")
                
                # Add attachment button
                if st.button("➕ Add Attachment", key=f"add_attachment_{base_key}"):
                    st.session_state[f'{base_key}_add_attachment'] = True
                    
                if st.session_state.get(f'{base_key}_add_attachment', False):
                    with st.form(f"attachment_form_{base_key}"):
                        file_name = st.text_input("File Name")
                        file_type = st.selectbox("File Type", options=["PDF", "DOC", "XLS", "JPG", "PNG", "Other"])
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
                        file_type = st.selectbox("File Type", options=["PDF", "DOC", "XLS", "JPG", "PNG", "Other"])
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

    def render_dashboard(self):
        """Render the Closeout Dashboard."""
        items = self._get_items()
        
        if not items:
            st.info("No closeout items found.")
            return
        
        st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
        st.subheader("Closeout Status Overview")
        
        # Calculate statistics
        total_items = len(items)
        complete_items = sum(1 for item in items if item['status'] in ['Complete', 'Approved'])
        in_progress_items = sum(1 for item in items if item['status'] in ['In Progress', 'Submitted'])
        not_started_items = sum(1 for item in items if item['status'] == 'Not Started')
        overdue_items = sum(1 for item in items if item['status'] == 'Overdue')
        
        # Calculate overall completion percentage
        overall_completion = sum(int(item['completion_pct']) for item in items) / total_items if total_items > 0 else 0
        
        # Status metrics in 4 columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Complete", f"{complete_items} / {total_items}", f"{(complete_items/total_items*100):.1f}%")
        with col2:
            st.metric("In Progress", in_progress_items)
        with col3:
            st.metric("Not Started", not_started_items)
        with col4:
            st.metric("Overdue", overdue_items, delta="-", delta_color="inverse" if overdue_items > 0 else "normal")
        
        # Overall progress
        st.markdown("### Overall Completion")
        st.progress(overall_completion / 100)
        st.markdown(f"**{overall_completion:.1f}%** Complete")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Items by category
        category_counts = {}
        for item in items:
            category = item['category']
            if category not in category_counts:
                category_counts[category] = {
                    'total': 0,
                    'complete': 0,
                    'in_progress': 0,
                    'not_started': 0,
                    'overdue': 0
                }
            
            category_counts[category]['total'] += 1
            
            if item['status'] in ['Complete', 'Approved']:
                category_counts[category]['complete'] += 1
            elif item['status'] in ['In Progress', 'Submitted']:
                category_counts[category]['in_progress'] += 1
            elif item['status'] == 'Not Started':
                category_counts[category]['not_started'] += 1
            elif item['status'] == 'Overdue':
                category_counts[category]['overdue'] += 1
        
        # Sort categories by completion percentage
        sorted_categories = sorted(
            category_counts.items(),
            key=lambda x: x[1]['complete'] / x[1]['total'] if x[1]['total'] > 0 else 0,
            reverse=True
        )
        
        # Display category progress
        st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
        st.subheader("Completion by Category")
        
        for category, counts in sorted_categories:
            completion_pct = counts['complete'] / counts['total'] * 100 if counts['total'] > 0 else 0
            
            st.markdown(f"**{category}** ({counts['complete']} of {counts['total']} complete)")
            
            # Progress bar and status counts as small text
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(completion_pct / 100)
            with col2:
                st.markdown(f"""
                <small>
                Complete: {counts['complete']}<br>
                In Progress: {counts['in_progress']}<br>
                Not Started: {counts['not_started']}<br>
                Overdue: {counts['overdue']}
                </small>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Items due soon (within next 14 days)
        upcoming_items = []
        today = datetime.now().date()
        
        for item in items:
            if item['status'] not in ['Complete', 'Approved']:
                due_date = datetime.strptime(item['due_date'], '%Y-%m-%d').date()
                days_until_due = (due_date - today).days
                
                if 0 <= days_until_due <= 14:
                    upcoming_items.append({
                        'item_id': item['item_id'],
                        'title': item['title'],
                        'days_until_due': days_until_due,
                        'responsible_party': item['responsible_party'],
                        'status': item['status'],
                        'completion_pct': item['completion_pct']
                    })
        
        # Sort by days until due
        upcoming_items.sort(key=lambda x: x['days_until_due'])
        
        if upcoming_items:
            st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.subheader("Items Due Soon")
            
            for item in upcoming_items:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{item['title']}** ({item['item_id']})")
                    st.markdown(f"Responsible: {item['responsible_party']}")
                with col2:
                    days_text = "Today" if item['days_until_due'] == 0 else f"{item['days_until_due']} days"
                    st.markdown(f"**Due:** {days_text}")
                    
                    # Status badge
                    status_class = self._get_status_class(item['status'])
                    st.markdown(f"""
                    <span class='crud-status crud-status-{status_class}' 
                          style="outline: none; box-shadow: none; border: none;">{item['status']}</span>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"**{item['completion_pct']}%**")
                    st.progress(float(item['completion_pct'])/100)
                
                st.markdown("---")
            
            st.markdown("</div>", unsafe_allow_html=True)

def render():
    """Render the Closeout module."""
    st.title("Project Closeout")
    
    # Create tabs for different closeout functions
    tab1, tab2 = st.tabs(["Closeout Dashboard", "Closeout Items"])
    
    # Closeout Dashboard Tab
    with tab1:
        closeout_items = CloseoutItemModule()
        closeout_items.render_dashboard()
    
    # Closeout Items Tab
    with tab2:
        closeout_items = CloseoutItemModule()
        closeout_items.render()