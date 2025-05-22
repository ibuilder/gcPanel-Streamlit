"""
CRUD Template Module for gcPanel

This module provides a standardized template for implementing CRUD (Create, Read, Update, Delete)
operations across all modules in the application. It ensures consistent styling and behavior.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json

from assets.crud_styler import (
    apply_crud_styles,
    render_crud_list_container,
    end_crud_list_container,
    render_crud_detail_container,
    end_crud_detail_container,
    render_form_actions,
    render_status_badge,
    render_crud_fieldset
)

class CrudModule:
    """
    A base class for implementing standardized CRUD functionality.
    
    This class provides common CRUD operations and UI rendering that can be
    inherited by specific modules to ensure consistent styling and behavior.
    """
    
    def __init__(self, 
                 module_name, 
                 data_file_path,
                 id_field='id',
                 list_columns=None,
                 default_sort_field=None,
                 default_sort_direction='asc',
                 status_field=None,
                 filter_options=None):
        """
        Initialize the CRUD module with configuration.
        
        Args:
            module_name (str): Name of the module for UI display and session state keys
            data_file_path (str): Path to the JSON data file
            id_field (str): Name of the field that acts as the primary key
            list_columns (list): List of columns to display in the list view
            default_sort_field (str): Default field to sort by
            default_sort_direction (str): Default sort direction ('asc' or 'desc')
            status_field (str): Name of the status field for filtering
            filter_options (list): Options for status filter dropdown
        """
        self.module_name = module_name
        self.data_file_path = data_file_path
        self.id_field = id_field
        self.list_columns = list_columns or []
        self.default_sort_field = default_sort_field or id_field
        self.default_sort_direction = default_sort_direction
        self.status_field = status_field
        self.filter_options = filter_options or []
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(data_file_path), exist_ok=True)
        
        # Initialize session state for this module
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state variables for this module."""
        base_key = self._get_state_key_prefix()
        
        # Initialize view state if not present
        if f'{base_key}_view' not in st.session_state:
            st.session_state[f'{base_key}_view'] = 'list'
        
        # Initialize sort state
        if f'{base_key}_sort_col' not in st.session_state:
            st.session_state[f'{base_key}_sort_col'] = self.default_sort_field
        
        if f'{base_key}_sort_direction' not in st.session_state:
            st.session_state[f'{base_key}_sort_direction'] = self.default_sort_direction
        
        # Initialize filter state
        if f'{base_key}_filter' not in st.session_state:
            st.session_state[f'{base_key}_filter'] = 'All'
        
        # Initialize search state
        if f'{base_key}_search' not in st.session_state:
            st.session_state[f'{base_key}_search'] = ''
    
    def _get_state_key_prefix(self):
        """Get the prefix used for session state keys for this module."""
        return self.module_name.lower().replace(' ', '_')
    
    def _get_items(self):
        """Get all items from the data file."""
        if not os.path.exists(self.data_file_path):
            # File doesn't exist, return empty list
            return []
        
        try:
            with open(self.data_file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Error reading file, return empty list
            return []
    
    def _save_items(self, items):
        """Save items to the data file."""
        with open(self.data_file_path, 'w') as f:
            json.dump(items, f, indent=2)
    
    def _get_item_by_id(self, item_id):
        """Get a specific item by ID."""
        items = self._get_items()
        for item in items:
            if str(item.get(self.id_field)) == str(item_id):
                return item
        return None
    
    def _save_item(self, item):
        """Save or update an item."""
        items = self._get_items()
        
        # Check if this is an existing item
        for i, existing_item in enumerate(items):
            if str(existing_item.get(self.id_field)) == str(item.get(self.id_field)):
                items[i] = item
                self._save_items(items)
                return item
        
        # This is a new item
        items.append(item)
        self._save_items(items)
        return item
    
    def _delete_item(self, item_id):
        """Delete an item by ID."""
        items = self._get_items()
        items = [item for item in items if str(item.get(self.id_field)) != str(item_id)]
        self._save_items(items)
    
    def _filter_items(self, items):
        """Apply filtering to items based on current filter and search settings."""
        base_key = self._get_state_key_prefix()
        
        # Apply search filter
        search = st.session_state.get(f'{base_key}_search', '').lower()
        if search:
            filtered_items = []
            for item in items:
                # Search in all string fields
                for key, value in item.items():
                    if isinstance(value, str) and search in value.lower():
                        filtered_items.append(item)
                        break
            items = filtered_items
        
        # Apply status filter
        status_filter = st.session_state.get(f'{base_key}_filter', 'All')
        if status_filter != 'All' and self.status_field:
            items = [item for item in items if item.get(self.status_field) == status_filter]
        
        return items
    
    def _sort_items(self, items):
        """Sort items based on current sort settings."""
        base_key = self._get_state_key_prefix()
        
        # Get sort column and direction
        sort_col = st.session_state.get(f'{base_key}_sort_col', self.default_sort_field)
        sort_direction = st.session_state.get(f'{base_key}_sort_direction', self.default_sort_direction)
        
        # Define a key function that handles different data types
        def sort_key(item):
            value = item.get(sort_col)
            
            # Handle different data types for sorting
            if value is None:
                # None values should sort last
                if sort_direction == 'asc':
                    return (True, None)  # Will sort after all non-None values
                else:
                    return (False, None)  # Will sort before all non-None values
            
            # For dates in string format (YYYY-MM-DD)
            if isinstance(value, str) and len(value) == 10 and value[4] == '-' and value[7] == '-':
                try:
                    return (False, datetime.strptime(value, '%Y-%m-%d'))
                except ValueError:
                    pass
            
            # For normal values
            return (False, value)
        
        # Sort the items
        sorted_items = sorted(items, key=sort_key, reverse=(sort_direction == 'desc'))
        
        return sorted_items
    
    def return_to_list_view(self):
        """Return to the list view by clearing detail view session state."""
        base_key = self._get_state_key_prefix()
        if f"{base_key}_show_detail" in st.session_state:
            del st.session_state[f"{base_key}_show_detail"]
        if f"{base_key}_selected_item" in st.session_state:
            del st.session_state[f"{base_key}_selected_item"]
        if f"{base_key}_is_new" in st.session_state:
            del st.session_state[f"{base_key}_is_new"]
        st.rerun()
    
    def render_list_view(self):
        """Render the list view with standardized CRUD styling."""
        # Apply CRUD styles
        apply_crud_styles()
        
        # Get items with filtering and sorting
        items = self._get_items()
        filtered_items = self._filter_items(items)
        sorted_items = self._sort_items(filtered_items)
        
        # Render the list container
        base_key = self._get_state_key_prefix()
        
        filter_field = None
        if self.status_field and self.filter_options:
            filter_field = {
                'label': f'Filter by {self.status_field.capitalize()}',
                'options': ['All'] + self.filter_options,
                'default': 'All'
            }
        
        list_actions = render_crud_list_container(
            title=self.module_name,
            add_button=True,
            search_field=True,
            filter_field=filter_field
        )
        
        # Store search and filter values in session state
        st.session_state[f'{base_key}_search'] = list_actions['search_value']
        if filter_field:
            st.session_state[f'{base_key}_filter'] = list_actions['filter_value']
        
        # Check if add button was clicked
        if list_actions['add_clicked']:
            st.session_state[f'{base_key}_view'] = 'new'
            st.rerun()
        
        # Create a table to display items
        if sorted_items:
            # Create column headers with sorting buttons
            cols = st.columns(len(self.list_columns) + 1)  # +1 for actions column
            
            for i, col_name in enumerate(self.list_columns):
                with cols[i]:
                    # Display field name as the header, with sort indicators
                    sort_col = st.session_state.get(f'{base_key}_sort_col')
                    sort_direction = st.session_state.get(f'{base_key}_sort_direction')
                    
                    field_name = col_name
                    display_name = field_name.capitalize().replace('_', ' ')
                    
                    # Add sort indicator
                    if sort_col == field_name:
                        sort_indicator = '↑' if sort_direction == 'asc' else '↓'
                        sort_label = f"{display_name} {sort_indicator}"
                    else:
                        sort_label = f"{display_name} ⇅"
                    
                    # Sort button
                    if st.button(sort_label, key=f"sort_{base_key}_{field_name}"):
                        # Toggle sort direction if clicking on the same column
                        if sort_col == field_name:
                            new_direction = 'desc' if sort_direction == 'asc' else 'asc'
                            st.session_state[f'{base_key}_sort_direction'] = new_direction
                        else:
                            st.session_state[f'{base_key}_sort_col'] = field_name
                            st.session_state[f'{base_key}_sort_direction'] = 'asc'
                        st.rerun()
            
            with cols[-1]:
                st.write("Actions")
            
            # Display each row with action buttons
            for item in sorted_items:
                row_cols = st.columns(len(self.list_columns) + 1)
                
                # Display each column
                for i, field_name in enumerate(self.list_columns):
                    with row_cols[i]:
                        value = item.get(field_name, '')
                        
                        # Special handling for status fields
                        if field_name == self.status_field:
                            status_html = f"""
                            <div style="display: flex; align-items: center; justify-content: center; background: transparent; border: none; outline: none; box-shadow: none;">
                                <span class='crud-status crud-status-{self._get_status_class(value)}' style="outline: none; box-shadow: none; border: none;">{value}</span>
                            </div>
                            """
                            st.markdown(status_html, unsafe_allow_html=True)
                        else:
                            st.write(value)
                
                # Add action buttons
                with row_cols[-1]:
                    view_col, edit_col = st.columns(2)
                    with view_col:
                        item_id = item.get(self.id_field, f"unknown_{hash(str(item))}")
                        if st.button("👁️", key=f"view_{item_id}", help="View details"):
                            st.session_state[f'{base_key}_selected_id'] = item[self.id_field]
                            st.session_state[f'{base_key}_view'] = 'detail'
                            st.session_state[f'{base_key}_edit_mode'] = False
                            st.rerun()
                    with edit_col:
                        if st.button("✏️", key=f"edit_{item[self.id_field]}", help="Edit"):
                            st.session_state[f'{base_key}_selected_id'] = item[self.id_field]
                            st.session_state[f'{base_key}_view'] = 'detail'
                            st.session_state[f'{base_key}_edit_mode'] = True
                            st.rerun()
        else:
            st.info(f"No {self.module_name.lower()} found. Add a new one using the button above.")
        
        end_crud_list_container()
    
    def render_detail_view(self):
        """
        Render the detail view for creating, viewing, or editing an item.
        
        This is a generic implementation that should be overridden by subclasses
        to provide specific form fields and validation for each module.
        """
        # Apply CRUD styles
        apply_crud_styles()
        
        base_key = self._get_state_key_prefix()
        
        # Get view mode
        is_new = st.session_state.get(f'{base_key}_view') == 'new'
        is_edit_mode = st.session_state.get(f'{base_key}_edit_mode', False)
        
        # Get item data
        if is_new:
            item = self._create_new_item_template()
            detail_title = f"New {self.module_name.rstrip('s')}"
        else:
            item_id = st.session_state.get(f'{base_key}_selected_id')
            item = self._get_item_by_id(item_id)
            if not item:
                st.error(f"Item with ID {item_id} not found")
                return
            detail_title = f"{item.get('title', item.get('name', item.get(self.id_field, 'Item')))}"
        
        # Render the detail container
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
                    st.warning(f"Are you sure you want to delete this {self.module_name.rstrip('s')}?")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("Yes, Delete", type="secondary", key="confirm_delete"):
                            self._delete_item(item[self.id_field])
                            st.success(f"{self.module_name.rstrip('s')} deleted successfully")
                            st.session_state[f'{base_key}_view'] = 'list'
                            st.rerun()
                    with confirm_col2:
                        if st.button("Cancel", key="cancel_delete"):
                            st.rerun()
        
        # Create form for editing or read-only view for viewing
        if is_edit_mode or is_new:
            # This should be implemented by subclasses
            st.warning("The detail form is not implemented for this module.")
            
            # Example form (to be replaced by subclass implementation)
            with st.form("item_form"):
                st.text_input("ID", value=item.get(self.id_field, ''), disabled=not is_new)
                st.text_input("Title", value=item.get('title', ''))
                st.text_area("Description", value=item.get('description', ''))
                
                # Form actions
                form_actions = render_form_actions(
                    save_label="Save",
                    cancel_label="Cancel",
                    delete_label="Delete",
                    show_delete=not is_new
                )
                
                if form_actions['save_clicked']:
                    st.success(f"{self.module_name.rstrip('s')} saved successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['cancel_clicked']:
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
                
                if form_actions['delete_clicked']:
                    self._delete_item(item[self.id_field])
                    st.success(f"{self.module_name.rstrip('s')} deleted successfully")
                    st.session_state[f'{base_key}_view'] = 'list'
                    st.rerun()
        else:
            # Read-only view (to be replaced by subclass implementation)
            st.warning("The detail view is not implemented for this module.")
            
            for field, value in item.items():
                st.write(f"**{field.capitalize().replace('_', ' ')}:** {value}")
        
        end_crud_detail_container()
    
    def _create_new_item_template(self):
        """Create a template for a new item with default values."""
        # This should be overridden by subclasses
        return {
            self.id_field: self._generate_new_id(),
            'created_date': datetime.now().strftime('%Y-%m-%d')
        }
    
    def _generate_new_id(self):
        """Generate a new unique ID for a new item."""
        items = self._get_items()
        
        # If no items exist yet, start with ID 1
        if not items:
            return "1"
        
        # Find the highest numerical ID and increment
        max_id = 0
        for item in items:
            item_id = item.get(self.id_field)
            if isinstance(item_id, (int, str)) and str(item_id).isdigit():
                max_id = max(max_id, int(item_id))
        
        return str(max_id + 1)
    
    def _get_status_class(self, status):
        """Get the CSS class for a status value."""
        if not status:
            return "info"
            
        status_map = {
            'Active': 'info',
            'Pending': 'warning',
            'In Progress': 'info',
            'Completed': 'success',
            'On Hold': 'warning',
            'Cancelled': 'danger',
            'Approved': 'success',
            'Rejected': 'danger',
            'Open': 'info',
            'Closed': 'success',
            'High': 'danger',
            'Medium': 'warning',
            'Low': 'info'
        }
        
        return status_map.get(status, "info")
    
    def render(self):
        """Render the appropriate view based on the current state."""
        base_key = self._get_state_key_prefix()
        current_view = st.session_state.get(f'{base_key}_view', 'list')
        
        if current_view == 'list':
            self.render_list_view()
        elif current_view in ['detail', 'new']:
            self.render_detail_view()
        else:
            st.error(f"Unknown view: {current_view}")
            st.session_state[f'{base_key}_view'] = 'list'
            st.rerun()