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
    # CSS for the action bar
    st.markdown("""
    <div class="action-bar">
    """, unsafe_allow_html=True)
    
    # Setup columns for buttons
    cols = st.columns([6, 1, 1, 1])
    
    # Initialize result tracking
    result = {
        "add_clicked": False,
        "edit_clicked": False,
        "delete_clicked": False
    }
    
    # Add button
    if show_add:
        with cols[1]:
            add_label = f"Add {page_type}"
            add_clicked = st.button(f"➕ {add_label}", key=f"add_{page_type.lower().replace(' ', '_')}")
            if add_clicked:
                result["add_clicked"] = True
    
    # Edit button
    if show_edit:
        with cols[2]:
            edit_label = f"Edit {page_type}"
            edit_clicked = st.button(f"✏️ {edit_label}", key=f"edit_{page_type.lower().replace(' ', '_')}")
            if edit_clicked:
                result["edit_clicked"] = True
    
    # Delete button
    if show_delete:
        with cols[3]:
            delete_label = f"Delete {page_type}"
            delete_clicked = st.button(f"🗑️ {delete_label}", key=f"delete_{page_type.lower().replace(' ', '_')}")
            if delete_clicked:
                result["delete_clicked"] = True
    
    # Close the action bar container
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)
    
    return result