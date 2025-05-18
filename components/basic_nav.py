"""
Extremely basic navigation component without any fancy styling.
"""

import streamlit as st

def render_nav():
    """Render the most basic possible navigation."""
    
    st.sidebar.title("Navigation")
    
    # Simple navigation menu
    menu_options = [
        "Dashboard", 
        "Project Information",
        "Engineering", 
        "Documents", 
        "BIM",
        "Field Operations",
        "Safety",
        "Contracts", 
        "Cost Management",
        "Schedule",
        "Closeout",
        "Settings"
    ]
    
    # Simple selectbox for navigation
    menu = st.sidebar.selectbox(
        "Select Module",
        menu_options,
        index=menu_options.index(st.session_state.get("current_menu", "Dashboard"))
    )
    
    # Update session state on change
    if menu != st.session_state.get("current_menu", "Dashboard"):
        st.session_state.current_menu = menu
        st.rerun()