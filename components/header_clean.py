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
    
    # Create a three-column layout for the header
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # Project info (left aligned)
        st.caption("Project")
        st.write("Highland Tower Development")
    
    with col2:
        # Center the logo
        st.markdown("""
        <div style="text-align: center; padding-top: 10px;">
            <span style="font-size: 24px; font-weight: 700;">
                gc<span style="color: #3b82f6;">Panel</span>
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Right aligned dropdown
        st.markdown("""
        <div style="text-align: right; padding-bottom: 5px;">
            <span style="font-size: 14px; color: #6b7280;">Navigation</span>
        </div>
        """, unsafe_allow_html=True)
        
        selected = st.selectbox(
            "Navigation",
            options=list(menu_options.keys()),
            index=list(menu_options.keys()).index(current_menu),
            key="header_nav_dropdown",
            label_visibility="collapsed"
        )
        
        # Update session state if menu changed
        if selected != current_menu:
            st.session_state.current_menu = selected
            st.rerun()
    
    # Display a divider
    st.divider()
    
    # Breadcrumb row
    # Nothing here because breadcrumbs are handled in app_manager.py