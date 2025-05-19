"""
Action Bar Component for gcPanel

This component provides a consistent action bar with Add/Edit buttons
for various pages in the gcPanel application.
"""

import streamlit as st

def render_action_bar(page_type="Item", show_add=True, show_edit=True, show_delete=False):
    """
    Render an action bar with Add/Edit/Delete buttons.
    
    Args:
        page_type (str): The type of item to add/edit (e.g., "Contract", "Document")
        show_add (bool): Whether to show the Add button
        show_edit (bool): Whether to show the Edit button
        show_delete (bool): Whether to show the Delete button
        
    Returns:
        dict: Dictionary containing button click states (add_clicked, edit_clicked, delete_clicked)
    """
    # CSS for the action bar with improved button styling
    st.markdown("""
    <style>
    .stButton > button {
        min-width: 120px;
        height: 42px;
        margin-right: 10px;
        margin-bottom: 10px;
        padding: 0px 15px;
        border-radius: 5px;
        font-weight: 500;
    }
    .action-bar {
        display: flex;
        justify-content: flex-end;
        padding: 10px 0;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(49, 51, 63, 0.2);
    }
    </style>
    <div class="action-bar">
    """, unsafe_allow_html=True)
    
    # Calculate how many buttons to show
    visible_buttons = sum([show_add, show_edit, show_delete])
    
    # Setup columns with appropriate spacing
    # Giving more space to the content area and proper spacing for buttons
    cols = []
    if visible_buttons > 0:
        cols = st.columns([5] + [1] * visible_buttons)
    else:
        cols = [st.container()]  # Just a placeholder if no buttons
    
    # Initialize result tracking
    result = {
        "add_clicked": False,
        "edit_clicked": False,
        "delete_clicked": False
    }
    
    col_index = 1  # Start from the second column (after the content space)
    
    # Add button
    if show_add:
        with cols[col_index]:
            add_label = f"Add {page_type}"
            add_clicked = st.button(
                add_label, 
                key=f"add_{page_type.lower().replace(' ', '_')}",
                help=f"Create a new {page_type.lower()}"
            )
            if add_clicked:
                result["add_clicked"] = True
        col_index += 1
    
    # Edit button
    if show_edit:
        with cols[col_index]:
            edit_label = f"Edit {page_type}"
            edit_clicked = st.button(
                edit_label, 
                key=f"edit_{page_type.lower().replace(' ', '_')}",
                help=f"Modify selected {page_type.lower()}"
            )
            if edit_clicked:
                result["edit_clicked"] = True
        col_index += 1
    
    # Delete button
    if show_delete:
        with cols[col_index]:
            delete_label = f"Delete {page_type}"
            delete_clicked = st.button(
                delete_label,
                key=f"delete_{page_type.lower().replace(' ', '_')}",
                help=f"Remove selected {page_type.lower()}"
            )
            if delete_clicked:
                result["delete_clicked"] = True
    
    # Close the action bar container
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)
    
    return result