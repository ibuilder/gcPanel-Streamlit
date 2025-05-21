"""
CRUD Demo Module for gcPanel

This module demonstrates the standardized CRUD (Create, Read, Update, Delete)
styles and components for consistent UI across all modules.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import json
import os

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

# Sample data for demonstration
DEMO_DATA_FILE = 'data/crud_demo/demo_items.json'

# Ensure data directory exists
os.makedirs(os.path.dirname(DEMO_DATA_FILE), exist_ok=True)

def initialize_demo_data():
    """Initialize demo data if it doesn't exist."""
    if os.path.exists(DEMO_DATA_FILE):
        return
    
    # Create sample data
    statuses = ['Active', 'Pending', 'Completed', 'On Hold']
    types = ['Project', 'Task', 'Meeting', 'Milestone']
    
    demo_items = []
    for i in range(1, 11):
        created_date = datetime.now() - timedelta(days=random.randint(1, 30))
        due_date = created_date + timedelta(days=random.randint(5, 45))
        
        item = {
            'id': f'ITEM-{i:03d}',
            'title': f'Demo Item {i}',
            'description': f'This is a demonstration item #{i} with various fields to showcase CRUD styling.',
            'status': random.choice(statuses),
            'type': random.choice(types),
            'priority': random.randint(1, 5),
            'assigned_to': f'User {random.randint(1, 5)}',
            'created_date': created_date.strftime('%Y-%m-%d'),
            'due_date': due_date.strftime('%Y-%m-%d'),
            'cost': round(random.uniform(100, 10000), 2),
            'completed': random.choice([True, False])
        }
        demo_items.append(item)
    
    # Save data
    with open(DEMO_DATA_FILE, 'w') as f:
        json.dump(demo_items, f, indent=2)

def get_demo_items():
    """Get all demo items from the data file."""
    if not os.path.exists(DEMO_DATA_FILE):
        initialize_demo_data()
    
    with open(DEMO_DATA_FILE, 'r') as f:
        return json.load(f)

def save_demo_items(items):
    """Save demo items to the data file."""
    with open(DEMO_DATA_FILE, 'w') as f:
        json.dump(items, f, indent=2)

def get_item_by_id(item_id):
    """Get a specific item by ID."""
    items = get_demo_items()
    for item in items:
        if item['id'] == item_id:
            return item
    return None

def save_item(item):
    """Save or update an item."""
    items = get_demo_items()
    
    # Check if this is an existing item
    for i, existing_item in enumerate(items):
        if existing_item['id'] == item['id']:
            items[i] = item
            save_demo_items(items)
            return item
    
    # This is a new item
    items.append(item)
    save_demo_items(items)
    return item

def delete_item(item_id):
    """Delete an item by ID."""
    items = get_demo_items()
    items = [item for item in items if item['id'] != item_id]
    save_demo_items(items)

def render_demo_list():
    """Render the demo list view with our standardized CRUD styles."""
    # Get demo items
    items = get_demo_items()
    
    # Apply filter and search if provided
    search = st.session_state.get('crud_demo_search', '')
    status_filter = st.session_state.get('crud_demo_filter', 'All')
    
    if search:
        search = search.lower()
        items = [
            item for item in items 
            if search in item['title'].lower() or 
               search in item['description'].lower() or
               search in item['id'].lower()
        ]
    
    if status_filter != 'All':
        items = [item for item in items if item['status'] == status_filter]
    
    # Render the list container
    list_actions = render_crud_list_container(
        title="Demo Items",
        add_button=True,
        search_field=True,
        filter_field={
            'label': 'Status',
            'options': ['All', 'Active', 'Pending', 'Completed', 'On Hold'],
            'default': 'All'
        }
    )
    
    # Store search and filter values in session state
    st.session_state['crud_demo_search'] = list_actions['search_value']
    st.session_state['crud_demo_filter'] = list_actions['filter_value']
    
    # Check if add button was clicked
    if list_actions['add_clicked']:
        st.session_state['crud_demo_view'] = 'new'
        st.rerun()
    
    # Create a table to display items
    if items:
        # Convert to DataFrame for easier display
        df = pd.DataFrame(items)
        
        # Select columns to display
        display_df = df[['id', 'title', 'status', 'type', 'priority', 'due_date', 'assigned_to']]
        
        # Apply custom formatting for status column
        def status_formatter(status):
            return f"<span class='crud-status crud-status-{get_status_class(status)}'>{status}</span>"
            
        # Apply formatting to each row manually
        formatted_status = []
        for status in display_df['status']:
            formatted_status.append(status_formatter(status))
        display_df['status'] = formatted_status
        
        # Create an enhanced table with sorting, filtering, and action buttons
        st.subheader("Items List")
        
        # Add column headers with sorting buttons
        sort_col = st.session_state.get('crud_demo_sort_col', 'id')
        sort_direction = st.session_state.get('crud_demo_sort_direction', 'asc')
        
        # Sort the dataframe based on the selected column and direction
        # Convert the dataframe to list of dictionaries for easier manual sorting
        display_list = display_df.to_dict(orient='records')
        
        # Sort the list manually to avoid pandas issues
        if sort_col == 'priority':
            # Numeric sorting for priority
            display_list = sorted(display_list, 
                                 key=lambda x: int(x[sort_col]), 
                                 reverse=(sort_direction == 'desc'))
        else:
            # String sorting for other columns
            display_list = sorted(display_list, 
                                 key=lambda x: str(x[sort_col]), 
                                 reverse=(sort_direction == 'desc'))
            
        # Convert back to dataframe
        display_df = pd.DataFrame(display_list)
        
        # Create column headers with sorting buttons
        cols = st.columns(len(display_df.columns) + 1)  # +1 for actions column
        
        for i, col_name in enumerate(display_df.columns):
            with cols[i]:
                # Create a sort button for each column
                sort_label = f"{col_name} {'↑' if sort_col == col_name and sort_direction == 'asc' else '↓' if sort_col == col_name and sort_direction == 'desc' else '⇅'}"
                if st.button(sort_label, key=f"sort_{col_name}"):
                    # Toggle sort direction if clicking on the same column
                    if sort_col == col_name:
                        st.session_state['crud_demo_sort_direction'] = 'desc' if sort_direction == 'asc' else 'asc'
                    else:
                        st.session_state['crud_demo_sort_col'] = col_name
                        st.session_state['crud_demo_sort_direction'] = 'asc'
                    st.rerun()
        
        with cols[-1]:
            st.write("Actions")
        
        # Display the sorted data with action buttons for each row
        for _, row in display_df.iterrows():
            item_id = row['id']
            cols = st.columns(len(row) + 1)  # +1 for actions column
            
            # Display the row data
            for i, (col_name, value) in enumerate(row.items()):
                with cols[i]:
                    # For status column, display with HTML formatting
                    if col_name == 'status':
                        status_html = f"""
                        <div style="display: flex; align-items: center; justify-content: center;">
                            <span class='crud-status crud-status-{get_status_class(value)}' style="outline: none; box-shadow: none;">{value}</span>
                        </div>
                        """
                        st.markdown(status_html, unsafe_allow_html=True)
                    else:
                        st.write(value)
            
            # Add action buttons
            with cols[-1]:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👁️", key=f"view_{item_id}", help="View item details"):
                        st.session_state['crud_demo_selected_id'] = item_id
                        st.session_state['crud_demo_view'] = 'detail'
                        st.session_state['crud_demo_edit_mode'] = False
                        st.rerun()
                with col2:
                    if st.button("✏️", key=f"edit_{item_id}", help="Edit this item"):
                        st.session_state['crud_demo_selected_id'] = item_id
                        st.session_state['crud_demo_view'] = 'detail'
                        st.session_state['crud_demo_edit_mode'] = True
                        st.rerun()
        
        # Add a filter section
        st.subheader("Advanced Filters")
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            # Filter by type
            type_filter = st.multiselect(
                "Filter by Type",
                options=list(set(item['type'] for item in items)),
                default=[]
            )
            if type_filter:
                st.session_state['crud_demo_type_filter'] = type_filter
            
        with filter_col2:
            # Filter by priority
            priority_filter = st.multiselect(
                "Filter by Priority",
                options=list(range(1, 6)),
                default=[]
            )
            if priority_filter:
                st.session_state['crud_demo_priority_filter'] = priority_filter
                
        with filter_col3:
            # Reset filters button
            if st.button("Reset Filters"):
                if 'crud_demo_type_filter' in st.session_state:
                    del st.session_state['crud_demo_type_filter']
                if 'crud_demo_priority_filter' in st.session_state:
                    del st.session_state['crud_demo_priority_filter']
                if 'crud_demo_search' in st.session_state:
                    st.session_state['crud_demo_search'] = ''
                if 'crud_demo_filter' in st.session_state:
                    st.session_state['crud_demo_filter'] = 'All'
                st.rerun()
    else:
        st.info("No items found. Create a new item using the Add button above.")
    
    end_crud_list_container()

def render_demo_detail():
    """Render the detail view for a selected item."""
    item_id = st.session_state.get('crud_demo_selected_id')
    is_new = st.session_state.get('crud_demo_view') == 'new'
    is_edit_mode = st.session_state.get('crud_demo_edit_mode', is_new)
    
    # Get item data or initialize a new one
    if is_new:
        item = {
            'id': generate_new_id(),
            'title': '',
            'description': '',
            'status': 'Pending',
            'type': 'Task',
            'priority': 3,
            'assigned_to': '',
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'due_date': (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'),
            'cost': 0.0,
            'completed': False
        }
        detail_title = "New Item"
    else:
        item = get_item_by_id(item_id)
        if not item:
            st.error(f"Item with ID {item_id} not found")
            return
        detail_title = item['title']
    
    # Render the detail container with appropriate title based on mode
    mode_prefix = "New" if is_new else "Edit" if is_edit_mode else "View"
    container_title = f"{mode_prefix}: {detail_title}"
    
    detail_actions = render_crud_detail_container(
        title=container_title,
        is_new=is_new,
        back_button=True
    )
    
    # Check if back button was clicked
    if detail_actions['back_clicked']:
        st.session_state['crud_demo_view'] = 'list'
        st.rerun()
    
    # Display top action buttons for view mode
    if not is_new and not is_edit_mode:
        col1, col2, col3 = st.columns([1, 1, 6])
        with col1:
            if st.button("✏️ Edit", type="primary"):
                st.session_state['crud_demo_edit_mode'] = True
                st.rerun()
        with col2:
            if st.button("🗑️ Delete", type="secondary"):
                st.warning("Are you sure you want to delete this item?")
                confirm_col1, confirm_col2 = st.columns(2)
                with confirm_col1:
                    if st.button("Yes, Delete", type="secondary", key="confirm_delete"):
                        delete_item(item_id)
                        st.success(f"Item {item_id} deleted successfully")
                        st.session_state['crud_demo_view'] = 'list'
                        st.rerun()
                with confirm_col2:
                    if st.button("Cancel", key="cancel_delete"):
                        st.rerun()
    
    # Create a form for editing or viewing the item
    if is_edit_mode or is_new:
        # Edit mode - show the form
        with st.form("item_form"):
            # Basic Information
            st.markdown('<div class="crud-section-header">Basic Information</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title", value=item['title'])
                
            with col2:
                item_id = st.text_input("ID", value=item['id'], disabled=not is_new)
            
            description = st.text_area("Description", value=item['description'], height=100)
            
            # Details
            st.markdown('<div class="crud-section-header">Details</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                status = st.selectbox("Status", 
                    options=['Active', 'Pending', 'Completed', 'On Hold'],
                    index=['Active', 'Pending', 'Completed', 'On Hold'].index(item['status'])
                )
                
            with col2:
                item_type = st.selectbox("Type", 
                    options=['Project', 'Task', 'Meeting', 'Milestone'],
                    index=['Project', 'Task', 'Meeting', 'Milestone'].index(item['type'])
                )
                
            with col3:
                priority = st.slider("Priority", 1, 5, item['priority'])
            
            # Dates and Assignment
            st.markdown('<div class="crud-section-header">Scheduling</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                created_date = st.date_input("Created Date", 
                    value=datetime.strptime(item['created_date'], '%Y-%m-%d') if item['created_date'] else datetime.now()
                )
                
            with col2:
                due_date = st.date_input("Due Date", 
                    value=datetime.strptime(item['due_date'], '%Y-%m-%d') if item['due_date'] else datetime.now() + timedelta(days=14)
                )
                
            with col3:
                assigned_to = st.selectbox("Assigned To", 
                    options=['', 'User 1', 'User 2', 'User 3', 'User 4', 'User 5'],
                    index=['', 'User 1', 'User 2', 'User 3', 'User 4', 'User 5'].index(item['assigned_to']) if item['assigned_to'] in ['', 'User 1', 'User 2', 'User 3', 'User 4', 'User 5'] else 0
                )
            
            # Additional Information
            st.markdown('<div class="crud-section-header">Additional Information</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                cost = st.number_input("Cost ($)", value=float(item['cost']), min_value=0.0, format="%.2f")
                
            with col2:
                completed = st.checkbox("Completed", value=item['completed'])
            
            # Form submission buttons with clear styling
            st.markdown('<div class="crud-form-actions">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                cancel = st.form_submit_button("Cancel")
            with col2:
                submit = st.form_submit_button("Save")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle form submission
        if submit:
            # Update item data
            updated_item = {
                'id': item_id,
                'title': title,
                'description': description,
                'status': status,
                'type': item_type,
                'priority': priority,
                'assigned_to': assigned_to,
                'created_date': created_date.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d'),
                'cost': cost,
                'completed': completed
            }
            
            # Save the item
            save_item(updated_item)
            
            # Show success message
            st.success(f"Item {item_id} saved successfully")
            
            # Return to list view after short delay
            if is_new:
                st.session_state['crud_demo_view'] = 'list'
            else:
                st.session_state['crud_demo_edit_mode'] = False
            st.rerun()
        
        if cancel:
            # Return to list view if new, or view mode if editing
            if is_new:
                st.session_state['crud_demo_view'] = 'list'
            else:
                st.session_state['crud_demo_edit_mode'] = False
            st.rerun()
            
    else:
        # View mode - display formatted data in read-only format
        # Basic Information
        st.markdown('<div class="crud-section-header">Basic Information</div>', unsafe_allow_html=True)
        
        st.markdown(f"**ID:** {item['id']}")
        st.markdown(f"**Title:** {item['title']}")
        
        st.markdown('<div class="crud-label">Description</div>', unsafe_allow_html=True)
        st.markdown(f"""<div class="crud-value-box">
            {item['description'] if item['description'] else 'No description provided.'}
        </div>""", unsafe_allow_html=True)
        
        # Details
        st.markdown('<div class="crud-section-header">Details</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Status:**")
            st.markdown(f"<span class='crud-status crud-status-{get_status_class(item['status'])}'>{item['status']}</span>", unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"**Type:** {item['type']}")
            
        with col3:
            st.markdown(f"**Priority:** {item['priority']}/5")
        
        # Dates and Assignment
        st.markdown('<div class="crud-section-header">Scheduling</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Created Date:** {item['created_date']}")
            
        with col2:
            st.markdown(f"**Due Date:** {item['due_date']}")
            
        with col3:
            st.markdown(f"**Assigned To:** {item['assigned_to'] if item['assigned_to'] else 'Unassigned'}")
        
        # Additional Information
        st.markdown('<div class="crud-section-header">Additional Information</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Cost:** ${item['cost']:.2f}")
            
        with col2:
            st.markdown(f"**Completed:** {'Yes' if item['completed'] else 'No'}")
    
    end_crud_detail_container()

def get_status_class(status):
    """Get the CSS class for a status value."""
    status_map = {
        'Active': 'info',
        'Pending': 'warning',
        'Completed': 'success',
        'On Hold': 'danger'
    }
    return status_map.get(status, 'info')

def generate_new_id():
    """Generate a new unique ID."""
    items = get_demo_items()
    existing_ids = [item['id'] for item in items]
    
    # Find the highest number and increment
    max_num = 0
    for item_id in existing_ids:
        if item_id.startswith('ITEM-'):
            try:
                num = int(item_id.split('-')[1])
                max_num = max(max_num, num)
            except:
                pass
    
    return f'ITEM-{max_num + 1:03d}'

def render_crud_demo():
    """Main entry point for the CRUD demo module."""
    st.title("Standardized CRUD Styling Demo")
    
    # Apply CRUD styles
    apply_crud_styles()
    
    # Initialize data
    initialize_demo_data()
    
    # Initialize session state for view management
    if 'crud_demo_view' not in st.session_state:
        st.session_state['crud_demo_view'] = 'list'
    
    # Render appropriate view
    if st.session_state['crud_demo_view'] == 'list':
        render_demo_list()
    elif st.session_state['crud_demo_view'] in ['detail', 'new']:
        render_demo_detail()
    else:
        st.error(f"Unknown view: {st.session_state['crud_demo_view']}")