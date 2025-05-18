"""
Professional header component for gcPanel.

A clean, modern header implemented with pure Python Streamlit components.
"""

import streamlit as st

def render_header():
    """
    Render a simple, clean header using only Streamlit components.
    """
    # Menu options for dropdown
    menu_options = {
        "Dashboard": "Dashboard",
        "Project Information": "Project Information",
        "Schedule": "Schedule",
        "Safety": "Safety",
        "Contracts": "Contracts",
        "Cost Management": "Cost Management",
        "Engineering": "Engineering",
        "Field Operations": "Field Operations",
        "Documents": "Documents",
        "BIM Viewer": "BIM",
        "Closeout": "Closeout",
        "Settings": "Settings"
    }
    
    # Get currently selected menu value from session state
    current_menu = st.session_state.get("current_menu", "Dashboard")
    
    # Create the header layout using columns
    header_col1, header_col2, header_col3 = st.columns([1, 2, 1])
    
    # Project info (left column)
    with header_col1:
        st.caption("Project")
        st.write("**Highland Tower Development**")
    
    # Logo in center
    with header_col2:
        st.markdown("<div style='text-align: center; font-size: 24px; font-weight: 700;'>gc<span style='color: #3b82f6;'>Panel</span></div>", unsafe_allow_html=True)
    
    # Menu dropdown in right column
    with header_col3:
        selected = st.selectbox(
            "Navigation",
            options=list(menu_options.keys()),
            index=list(menu_options.keys()).index(current_menu),
            key="header_nav_dropdown"
        )
        
        # Update session state if menu changed
        if selected != current_menu:
            st.session_state.current_menu = selected
            st.rerun()
    
    # Breadcrumb navigation and notification
    nav_col1, nav_col2 = st.columns([5, 1])
    
    with nav_col1:
        # Simple breadcrumb
        st.write(f"[Home](#) > {current_menu}")
    
    with nav_col2:
        # Notification bell (simplified)
        st.markdown("<div style='text-align: right;'>🔔 <sup style='background-color: #ef4444; color: white; border-radius: 50%; padding: 2px 6px; font-size: 10px;'>3</sup></div>", unsafe_allow_html=True)
    
    # Main title
    st.header(current_menu)