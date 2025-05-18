"""
Action buttons component for page headers.

This module provides reusable action buttons (Add, Edit, Delete) 
to be displayed at the top of pages.
"""

import streamlit as st

def render_action_buttons(page_type, show_add=True, show_edit=True, show_delete=False):
    """
    Render action buttons (Add, Edit, Delete) for a page header.
    
    Args:
        page_type (str): The type of page/module (e.g., "Contract", "RFI", "Submittal")
        show_add (bool): Whether to show the Add button
        show_edit (bool): Whether to show the Edit button
        show_delete (bool): Whether to show the Delete button
    
    Returns:
        dict: Dictionary with keys 'add_clicked', 'edit_clicked', 'delete_clicked'
    """
    # Create container for buttons
    col1, col2 = st.columns([6, 1])
    
    with col2:
        # Container for action buttons
        st.markdown('<div class="action-buttons-container">', unsafe_allow_html=True)
        
        # Track button clicks
        results = {
            'add_clicked': False,
            'edit_clicked': False,
            'delete_clicked': False
        }
        
        if show_add:
            add_label = f"Add {page_type}"
            if st.button(f"➕ {add_label}", key=f"add_{page_type.lower()}_btn"):
                results['add_clicked'] = True
                
        if show_edit:
            edit_label = f"Edit {page_type}"
            if st.button(f"✏️ {edit_label}", key=f"edit_{page_type.lower()}_btn"):
                results['edit_clicked'] = True
                
        if show_delete:
            delete_label = f"Delete {page_type}"
            if st.button(f"🗑️ {delete_label}", key=f"delete_{page_type.lower()}_btn"):
                results['delete_clicked'] = True
                
        st.markdown('</div>', unsafe_allow_html=True)
        
    return results


def render_add_button(page_type, key_suffix=""):
    """
    Render only an Add button for a page header.
    
    Args:
        page_type (str): The type of page/module (e.g., "Contract", "RFI", "Submittal")
        key_suffix (str): Optional suffix for the button key to avoid duplicate keys
    
    Returns:
        bool: True if button was clicked, False otherwise
    """
    # Container for action button
    st.markdown("""
    <style>
    .add-button-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="add-button-container">', unsafe_allow_html=True)
    
    add_label = f"Add {page_type}"
    clicked = st.button(f"➕ {add_label}", key=f"add_{page_type.lower()}{key_suffix}_btn")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return clicked