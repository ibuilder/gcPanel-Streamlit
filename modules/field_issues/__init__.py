"""
Field Issues Module for gcPanel

This module manages field issues using the standardized CRUD template.
"""

import streamlit as st
from datetime import datetime, timedelta
import random
import os

from modules.crud_template import CrudModule
from assets.crud_styler import render_form_actions, render_crud_fieldset, apply_crud_styles

# Define the Field Issues CRUD module
class FieldIssuesModule(CrudModule):
    def __init__(self):
        """Initialize the Field Issues module with configuration."""
        super().__init__(
            module_name="Field Issues",
            data_file_path="data/field_issues/issues.json",
            id_field="issue_id",
            list_columns=["issue_id", "title", "location", "priority", "status", "assigned_to", "due_date"],
            default_sort_field="due_date",
            default_sort_direction="asc",
            status_field="status",
            filter_options=["Open", "In Progress", "On Hold", "Resolved", "Closed"]
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        # Initialize demo data if it doesn't exist
        if not os.path.exists(self.data_file_path) or len(self._get_items()) == 0:
            self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize sample data if none exists."""
        statuses = ['Open', 'In Progress', 'On Hold', 'Resolved', 'Closed']
        priorities = ['High', 'Medium', 'Low']
        locations = ['2nd Floor - North Wing', '5th Floor - Mechanical Room', 'Basement - Electrical Room', 
                    'Roof Access', 'Lobby', 'Parking Garage - Level P1', 'Elevator Shaft #2']
        assignees = ['John Smith', 'Maria Garcia', 'Tom Wilson', 'Jessica Lee', 'Raj Patel']
        
        demo_items = []
        for i in range(1, 11):
            created_date = datetime.now() - timedelta(days=random.randint(1, 30))
            due_date = created_date + timedelta(days=random.randint(3, 15))
            
            item = {
                'issue_id': f'FI-{i:04d}',
                'title': f'Field Issue {i}',
                'description': f'This is a sample field issue #{i} with description about a construction problem.',
                'status': random.choice(statuses),
                'priority': random.choice(priorities),
                'location': random.choice(locations),
                'assigned_to': random.choice(assignees),
                'created_date': created_date.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d'),
                'reported_by': random.choice(assignees),
                'related_documents': [],
                'comments': []
            }
            demo_items.append(item)
        
        # Save demo data
        self._save_items(demo_items)
    
    def _create_new_item_template(self):
        """Create a template for a new field issue with default values."""
        issue_id = self._generate_new_id()
        return {
            'issue_id': f'FI-{int(issue_id):04d}',
            'title': '',
            'description': '',
            'status': 'Open',
            'priority': 'Medium',
            'location': '',
            'assigned_to': '',
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'due_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'reported_by': '',
            'related_documents': [],
            'comments': []
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for a field issue."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            issue_id = item.get('issue_id', '')
            if issue_id.startswith('FI-'):
                try:
                    num = int(issue_id.split('-')[1])
                    max_id = max(max_id, num)
                except:
                    pass
        
        return str(max_id + 1)
    
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
            detail_title = f"{item.get('title', item.get('issue_id', 'Issue'))}"
        
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
                if st.button("✏️ Edit", type="primary"):
                    st.session_state[f'{base_key}_edit_mode'] = True
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", type="secondary"):
                    st.warning("Are you sure you want to delete this Field Issue?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key="confirm_delete"):
                            self._delete_item(item['issue_id'])
                            st.success("Field Issue deleted successfully")
                            st.session_state[f'{base_key}_view'] = 'list'
                            st.rerun()
                    with confirm_col2:
                        if st.button("Cancel", key="cancel_delete"):
                            st.rerun()
        
        # Create form for editing or read-only view for viewing
        if is_edit_mode or is_new:
            with st.form("field_issue_form"):
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
                        reported_by = st.text_input("Reported By", value=item['reported_by'])
                
                render_crud_fieldset("Basic Information", render_basic_info)
                
                # Status and Priority Section
                def render_status_priority():
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        status = st.selectbox("Status", 
                            options=['Open', 'In Progress', 'On Hold', 'Resolved', 'Closed'],
                            index=['Open', 'In Progress', 'On Hold', 'Resolved', 'Closed'].index(item['status'])
                        )
                    with col2:
                        priority = st.selectbox("Priority",
                            options=['High', 'Medium', 'Low'],
                            index=['High', 'Medium', 'Low'].index(item['priority'])
                        )
                    with col3:
                        assigned_to = st.text_input("Assigned To", value=item['assigned_to'])
                
                render_crud_fieldset("Status and Priority", render_status_priority)
                
                # Dates Section
                def render_dates():
                    col1, col2 = st.columns(2)
                    with col1:
                        created_date = st.date_input("Created Date", 
                            value=datetime.strptime(item['created_date'], '%Y-%m-%d') if item['created_date'] else datetime.now(),
                            disabled=not is_new
                        )
                    with col2:
                        due_date = st.date_input("Due Date",
                            value=datetime.strptime(item['due_date'], '%Y-%m-%d') if item['due_date'] else (datetime.now() + timedelta(days=7))
                        )
                
                render_crud_fieldset("Dates", render_dates)
                
                # Form Actions
                form_actions = render_form_actions(
                    save_label="Save Issue",
                    cancel_label="Cancel",
                    delete_label="Delete Issue",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    # Update item with form values
                    updated_item = {
                        'issue_id': issue_id,
                        'title': title,
                        'description': description,
                        'status': status,
                        'priority': priority,
                        'location': location,
                        'assigned_to': assigned_to,
                        'created_date': created_date.strftime('%Y-%m-%d'),
                        'due_date': due_date.strftime('%Y-%m-%d'),
                        'reported_by': reported_by,
                        'related_documents': item.get('related_documents', []),
                        'comments': item.get('comments', [])
                    }
                    
                    # Save the updated item
                    self._save_item(updated_item)
                    
                    # Show success message and return to list view
                    st.success("Field Issue saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked'] and not is_new:
                    self._delete_item(item['issue_id'])
                    st.success("Field Issue deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view
            st.subheader("Basic Information")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Issue ID:** {item['issue_id']}")
            with col2:
                st.markdown(f"**Title:** {item['title']}")
            
            st.markdown(f"**Description:**")
            st.markdown(f"```{item['description']}```")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Location:** {item['location']}")
            with col2:
                st.markdown(f"**Reported By:** {item['reported_by']}")
            
            st.subheader("Status and Priority")
            col1, col2, col3 = st.columns(3)
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
                    <span class='crud-status crud-status-{self._get_status_class(item['priority'])}' style="outline: none; box-shadow: none; border: none;">{item['priority']}</span>
                </div>
                """
                st.markdown("**Priority:**")
                st.markdown(priority_html, unsafe_allow_html=True)
            with col3:
                st.markdown(f"**Assigned To:** {item['assigned_to']}")
            
            st.subheader("Dates")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Created Date:** {item['created_date']}")
            with col2:
                st.markdown(f"**Due Date:** {item['due_date']}")
            
            # Show comments if they exist
            if item.get('comments'):
                st.subheader("Comments")
                for i, comment in enumerate(item['comments']):
                    st.markdown(f"**{comment.get('author', 'Unknown')}** on {comment.get('date', 'Unknown date')}:")
                    st.markdown(f"> {comment.get('text', '')}")
                    if i < len(item['comments']) - 1:
                        st.markdown("---")
            
            # Show related documents if they exist
            if item.get('related_documents'):
                st.subheader("Related Documents")
                for doc in item['related_documents']:
                    st.markdown(f"- [{doc.get('name', 'Document')}]({doc.get('url', '#')})")
        
        end_crud_detail_container()

# Function to render the module
def render():
    """Render the Field Issues module."""
    st.title("Field Issues")
    
    # Create and render the Field Issues module
    field_issues = FieldIssuesModule()
    field_issues.render()