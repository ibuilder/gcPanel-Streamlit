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
    # Add custom CSS to improve button appearance and spacing
    st.markdown("""
    <style>
    .stButton > button {
        min-width: 120px;
        margin-right: 10px;
        margin-bottom: 10px;
        height: 42px;
        padding: 0px 15px;
        border-radius: 5px;
        font-weight: 500;
    }
    .action-button-container {
        display: flex;
        justify-content: flex-end;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create container with more space for buttons
    col1, col2 = st.columns([4, 3])
    
    with col2:
        # Container for action buttons
        st.markdown('<div class="action-button-container">', unsafe_allow_html=True)
        
        # Track button clicks
        results = {
            'add_clicked': False,
            'edit_clicked': False,
            'delete_clicked': False
        }
        
        # Calculate how many buttons to display for proper layout
        button_count = sum([show_add, show_edit, show_delete])
        
        # Create a row of buttons with proper spacing
        button_cols = st.columns(button_count)
        
        col_index = 0
        
        if show_add:
            with button_cols[col_index]:
                add_label = f"Add {page_type}"
                if st.button(f"➕ Add", key=f"add_{page_type.lower()}_btn", help=add_label):
                    results['add_clicked'] = True
            col_index += 1
                
        if show_edit:
            with button_cols[col_index]:
                edit_label = f"Edit {page_type}"
                if st.button(f"✏️ Edit", key=f"edit_{page_type.lower()}_btn", help=edit_label):
                    results['edit_clicked'] = True
            col_index += 1
                
        if show_delete:
            with button_cols[col_index]:
                delete_label = f"Delete {page_type}"
                if st.button(f"🗑️ Delete", key=f"delete_{page_type.lower()}_btn", help=delete_label):
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
    # Apply consistent styling with other action buttons
    st.markdown("""
    <style>
    .stButton > button {
        min-width: 120px;
        height: 42px;
        padding: 0px 15px;
        border-radius: 5px;
        font-weight: 500;
    }
    .add-button-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 15px;
        padding-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a container for better positioning
    col1, col2 = st.columns([5, 2])
    
    with col2:
        st.markdown('<div class="add-button-container">', unsafe_allow_html=True)
        
        # Create a more accessible button with tooltip
        add_label = f"Add {page_type}"
        clicked = st.button(
            f"➕ Add", 
            key=f"add_{page_type.lower()}{key_suffix}_btn",
            help=add_label  # Add tooltip with full context
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    return clicked