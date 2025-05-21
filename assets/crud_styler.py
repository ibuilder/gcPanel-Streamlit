"""
CRUD Styler Module for gcPanel

This module provides a consistent way to apply CRUD (Create, Read, Update, Delete)
styles across the application. It helps maintain a standardized look and feel
for all CRUD operations in different modules.
"""

import streamlit as st

def apply_crud_styles():
    """
    Apply standardized CRUD styles across the application.
    
    This function loads the CRUD styles CSS file and applies it to the application.
    It should be called before rendering any CRUD components.
    """
    # Load CRUD styles from CSS file
    with open('assets/crud_styles.css', 'r') as f:
        crud_styles = f.read()
    
    # Apply CRUD styles
    st.markdown(f"<style>{crud_styles}</style>", unsafe_allow_html=True)

def render_crud_list_container(title, add_button=True, search_field=True, filter_field=None):
    """
    Render a standardized CRUD list container with header and action buttons.
    
    Args:
        title (str): The title of the list container
        add_button (bool): Whether to show the add button
        search_field (bool): Whether to show the search field
        filter_field (dict, optional): Configuration for a filter dropdown
            {
                'label': 'Filter by',
                'options': ['Option 1', 'Option 2'],
                'default': 'All'
            }
    
    Returns:
        dict: A dictionary containing click/interaction states
    """
    st.markdown(f'<div class="crud-list-container">', unsafe_allow_html=True)
    
    # List header with title and actions
    st.markdown(f'<div class="crud-list-header">', unsafe_allow_html=True)
    st.markdown(f'<h3 class="crud-list-title">{title}</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action row with search and filters
    if search_field or filter_field:
        cols = st.columns([3, 1, 1] if filter_field else [3, 1])
        
        with cols[0]:
            search_input = st.text_input("Search", key=f"search_{title.lower().replace(' ', '_')}")
        
        if filter_field:
            with cols[1]:
                filter_value = st.selectbox(
                    filter_field.get('label', 'Filter by'),
                    options=filter_field.get('options', []),
                    index=filter_field.get('options', []).index(filter_field.get('default', 'All')) 
                    if filter_field.get('default') in filter_field.get('options', []) else 0
                )
        
        with cols[-1]:
            add_clicked = False
            if add_button:
                add_clicked = st.button(f"Add {title.rstrip('s')}", type="primary")
    else:
        add_clicked = False
        if add_button:
            add_col = st.columns([3, 1])
            with add_col[1]:
                add_clicked = st.button(f"Add {title.rstrip('s')}", type="primary")
    
    # Return interaction states
    result = {
        "add_clicked": add_clicked if 'add_clicked' in locals() else False,
        "search_value": search_input if 'search_input' in locals() else "",
        "filter_value": filter_value if 'filter_value' in locals() else None
    }
    
    return result

def end_crud_list_container():
    """Close the CRUD list container div tag."""
    st.markdown('</div>', unsafe_allow_html=True)

def render_crud_detail_container(title, is_new=False, back_button=True):
    """
    Render a standardized CRUD detail container with header and back button.
    
    Args:
        title (str): The title of the detail container
        is_new (bool): Whether this is a new item or existing item edit view
        back_button (bool): Whether to show the back button
        
    Returns:
        dict: A dictionary containing click/interaction states
    """
    st.markdown(f'<div class="crud-detail-container">', unsafe_allow_html=True)
    
    # Detail header with back button and title
    st.markdown(f'<div class="crud-detail-header">', unsafe_allow_html=True)
    
    action_prefix = "New" if is_new else "Edit"
    header_title = f"{action_prefix} {title}"
    
    back_clicked = False
    if back_button:
        cols = st.columns([1, 5])
        with cols[0]:
            back_clicked = st.button("← Back", key=f"back_{title.lower().replace(' ', '_')}")
        with cols[1]:
            st.markdown(f'<h3 class="crud-detail-title">{header_title}</h3>', unsafe_allow_html=True)
    else:
        st.markdown(f'<h3 class="crud-detail-title">{header_title}</h3>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Return interaction states
    result = {
        "back_clicked": back_clicked
    }
    
    return result

def end_crud_detail_container():
    """Close the CRUD detail container div tag."""
    st.markdown('</div>', unsafe_allow_html=True)

def render_form_actions(save_label="Save", cancel_label="Cancel", delete_label=None, show_delete=False):
    """
    Render standardized form action buttons.
    
    Args:
        save_label (str): Label for the save button
        cancel_label (str): Label for the cancel button
        delete_label (str): Label for the delete button (if shown)
        show_delete (bool): Whether to show the delete button
        
    Returns:
        dict: A dictionary containing button click states
    """
    st.markdown('<div class="crud-form-actions">', unsafe_allow_html=True)
    
    cols = st.columns([1, 1, 4] if show_delete else [1, 1, 5])
    
    with cols[0]:
        cancel_clicked = st.button(cancel_label, key=f"cancel_action")
    
    with cols[1]:
        save_clicked = st.button(save_label, key=f"save_action", type="primary")
    
    delete_clicked = False
    if show_delete and delete_label:
        with cols[2]:
            delete_clicked = st.button(delete_label, key=f"delete_action", type="secondary")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Return interaction states
    result = {
        "save_clicked": save_clicked,
        "cancel_clicked": cancel_clicked,
        "delete_clicked": delete_clicked
    }
    
    return result

def render_crud_table(data, columns, key_column, on_select=None, show_actions=True, action_column_width=80):
    """
    Render a standardized CRUD table with data.
    
    Args:
        data (list): List of dictionaries containing the data
        columns (list): List of column configurations
            [
                {
                    'field': 'id',
                    'header': 'ID',
                    'width': 100  # optional
                },
                ...
            ]
        key_column (str): The field name that serves as the unique identifier
        on_select (callable, optional): Callback function when a row is selected
        show_actions (bool): Whether to show action buttons in the table
        action_column_width (int): Width of the action column in pixels
        
    Returns:
        str: Selected row key if a row was selected, None otherwise
    """
    if not data:
        st.info("No data to display")
        return None
    
    # Calculate column widths
    total_defined_width = sum(col.get('width', 0) for col in columns if 'width' in col)
    remaining_cols = len([col for col in columns if 'width' not in col])
    
    if show_actions:
        total_defined_width += action_column_width
    
    available_width = 1000 - total_defined_width  # Assume 1000px total width
    default_width = available_width // max(1, remaining_cols) if remaining_cols > 0 else 0
    
    # Prepare HTML for table
    table_html = f"""
    <table class="crud-table" style="width: 100%">
        <thead>
            <tr>
    """
    
    # Add header row
    for col in columns:
        width = col.get('width', default_width)
        header = col.get('header', col.get('field', '').capitalize())
        table_html += f'<th style="width: {width}px">{header}</th>'
    
    # Add action column header if needed
    if show_actions:
        table_html += f'<th style="width: {action_column_width}px">Actions</th>'
    
    table_html += """
            </tr>
        </thead>
        <tbody>
    """
    
    # Add data rows
    for i, row in enumerate(data):
        row_key = row.get(key_column, i)
        
        # Create a unique key for row selection
        row_key_safe = str(row_key).replace(" ", "_").lower()
        
        # Add row
        table_html += f'<tr id="row-{row_key_safe}">'
        
        # Add cells
        for col in columns:
            field = col.get('field', '')
            formatter = col.get('formatter', lambda x: x)
            value = row.get(field, '')
            
            # Apply formatter if available
            displayed_value = formatter(value) if value is not None else ''
            
            table_html += f'<td>{displayed_value}</td>'
        
        # Add action column if needed
        if show_actions:
            table_html += f"""
            <td>
                <button class="crud-icon-button view-button" data-row-key="{row_key_safe}">👁️</button>
                <button class="crud-icon-button edit-button" data-row-key="{row_key_safe}">✏️</button>
            </td>
            """
        
        table_html += '</tr>'
    
    # Close table
    table_html += """
        </tbody>
    </table>
    """
    
    # Add JavaScript for interactivity
    js_code = f"""
    <script>
        // Function to handle row selection
        document.querySelectorAll('.crud-table tr[id^="row-"]').forEach(row => {{
            row.addEventListener('click', function() {{
                // Get the row key
                const rowKey = this.id.replace('row-', '');
                
                // Remove selection from all rows
                document.querySelectorAll('.crud-table tr').forEach(r => {{
                    r.classList.remove('selected');
                }});
                
                // Add selection to clicked row
                this.classList.add('selected');
                
                // Notify Streamlit of selection
                const data = {{
                    rowKey: rowKey,
                    action: 'select'
                }};
                
                // Use Streamlit's setComponentValue for communication
                if (window.parent.streamlitSendBackData) {{
                    window.parent.streamlitSendBackData({{
                        data: data,
                        dataType: 'json'
                    }});
                }}
            }});
        }});
        
        // Function to handle action button clicks
        document.querySelectorAll('.view-button, .edit-button').forEach(button => {{
            button.addEventListener('click', function(e) {{
                e.stopPropagation();  // Prevent row selection
                
                // Get the row key
                const rowKey = this.getAttribute('data-row-key');
                
                // Determine action type
                const action = this.classList.contains('view-button') ? 'view' : 'edit';
                
                // Notify Streamlit of action
                const data = {{
                    rowKey: rowKey,
                    action: action
                }};
                
                // Use Streamlit's setComponentValue for communication
                if (window.parent.streamlitSendBackData) {{
                    window.parent.streamlitSendBackData({{
                        data: data,
                        dataType: 'json'
                    }});
                }}
            }});
        }});
    </script>
    """
    
    # Render the table
    st.markdown(table_html + js_code, unsafe_allow_html=True)
    
    # For now, we'll return None since we can't easily capture click events 
    # from JavaScript in this implementation. In a real implementation,
    # we would use Streamlit components for proper communication.
    return None

def render_crud_fieldset(legend, content_func):
    """
    Render a fieldset for grouping related form fields.
    
    Args:
        legend (str): The fieldset legend/title
        content_func (callable): Function that renders the fieldset content
    """
    st.markdown(f'<fieldset class="crud-fieldset">', unsafe_allow_html=True)
    st.markdown(f'<legend class="crud-fieldset-legend">{legend}</legend>', unsafe_allow_html=True)
    
    # Call the content function to render the fieldset content
    content_func()
    
    st.markdown('</fieldset>', unsafe_allow_html=True)

def render_status_badge(status, status_map=None):
    """
    Render a status badge with appropriate styling.
    
    Args:
        status (str): The status value
        status_map (dict, optional): Mapping of status values to status types
            e.g. {'Approved': 'success', 'Pending': 'info', 'Rejected': 'danger'}
    
    Returns:
        str: HTML for the status badge
    """
    if status_map is None:
        status_map = {
            'Active': 'success',
            'Pending': 'info',
            'Completed': 'success',
            'In Progress': 'info',
            'On Hold': 'warning',
            'Cancelled': 'danger',
            'Approved': 'success',
            'Rejected': 'danger',
            'Open': 'info',
            'Closed': 'success'
        }
    
    status_type = status_map.get(status, 'info')
    
    badge_html = f'<span class="crud-status crud-status-{status_type}">{status}</span>'
    return badge_html

def apply_crud_formatter(value, formatter_type):
    """
    Apply a standard formatter to a value for display in tables.
    
    Args:
        value: The value to format
        formatter_type (str): The type of formatter to apply
            - 'date': Format as date (YYYY-MM-DD)
            - 'datetime': Format as datetime (YYYY-MM-DD HH:MM)
            - 'currency': Format as currency ($X,XXX.XX)
            - 'percent': Format as percentage (XX.X%)
            - 'status': Format as status badge
            - 'boolean': Format as Yes/No
    
    Returns:
        str: The formatted value as HTML if needed
    """
    if value is None:
        return ""
    
    if formatter_type == 'date':
        try:
            if isinstance(value, str):
                # Assume ISO format (YYYY-MM-DD)
                return value
            else:
                # Try to format as date
                return value.strftime('%Y-%m-%d')
        except:
            return str(value)
    
    elif formatter_type == 'datetime':
        try:
            if isinstance(value, str):
                # Assume ISO format
                return value
            else:
                # Try to format as datetime
                return value.strftime('%Y-%m-%d %H:%M')
        except:
            return str(value)
    
    elif formatter_type == 'currency':
        try:
            # Format as currency
            return f"${float(value):,.2f}"
        except:
            return str(value)
    
    elif formatter_type == 'percent':
        try:
            # Format as percentage
            return f"{float(value):.1f}%"
        except:
            return str(value)
    
    elif formatter_type == 'status':
        # Format as status badge
        return render_status_badge(value)
    
    elif formatter_type == 'boolean':
        # Format as Yes/No
        if isinstance(value, bool):
            return "Yes" if value else "No"
        elif value in [1, '1', 'true', 'True', 'yes', 'Yes']:
            return "Yes"
        elif value in [0, '0', 'false', 'False', 'no', 'No']:
            return "No"
        else:
            return str(value)
    
    else:
        # No formatting
        return str(value)