"""
Page header component for the gcPanel application.

This component provides a consistent header for all pages,
including title, breadcrumbs, and action buttons.
"""

import streamlit as st

def render_page_header(title, add_button=True, edit_button=True, delete_button=False):
    """
    Render a consistent page header with action buttons.
    
    Args:
        title (str): The page title
        add_button (bool): Whether to show an Add button
        edit_button (bool): Whether to show an Edit button
        delete_button (bool): Whether to show a Delete button
    
    Returns:
        dict: Dictionary with keys 'add_clicked', 'edit_clicked', 'delete_clicked'
    """
    # Create container for the page header
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; 
                margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid #eef2f7;">
        <h1 style="font-size: 24px; margin: 0; color: #2c3e50;">{title}</h1>
        <div class="action-buttons-container">
    """, unsafe_allow_html=True)
    
    # Create columns for buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Initialize result dictionary
    results = {
        'add_clicked': False,
        'edit_clicked': False,
        'delete_clicked': False
    }
    
    # Add button
    if add_button:
        with col1:
            add_clicked = st.button("➕ Add", key=f"add_{title.lower().replace(' ', '_')}")
            if add_clicked:
                results['add_clicked'] = True
    
    # Edit button
    if edit_button:
        with col2:
            edit_clicked = st.button("✏️ Edit", key=f"edit_{title.lower().replace(' ', '_')}")
            if edit_clicked:
                results['edit_clicked'] = True
    
    # Delete button
    if delete_button:
        with col3:
            delete_clicked = st.button("🗑️ Delete", key=f"delete_{title.lower().replace(' ', '_')}")
            if delete_clicked:
                results['delete_clicked'] = True
    
    # Close the container
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    return results