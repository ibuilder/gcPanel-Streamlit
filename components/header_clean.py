"""
Clean Header Component for gcPanel.

This module provides a streamlined header with project title, logo, and navigation.
"""

import streamlit as st
from app_config import MENU_OPTIONS, MENU_MAP, PROJECT_INFO

def render_header():
    """Render the clean header component."""
    
    # Use the simpler approach with direct Streamlit components
    # This will ensure the layout works consistently
    with st.container():
        cols = st.columns([1, 3, 1])
        
        # Left column - Logo
        with cols[0]:
            st.image("gcpanel.png", width=80)
        
        # Middle column - Project Info
        with cols[1]:
            st.markdown(f"### {PROJECT_INFO['name']}")
            st.markdown(f"{PROJECT_INFO['value']} • {PROJECT_INFO['size']} • {PROJECT_INFO['floors']}")
        
        # Right column - Navigation
        with cols[2]:
            st.markdown("Navigation")
            selected_menu = st.selectbox(
                "Select Module",
                options=MENU_OPTIONS,
                index=MENU_OPTIONS.index("📊 Dashboard") if "current_menu" not in st.session_state else MENU_OPTIONS.index([opt for opt in MENU_OPTIONS if MENU_MAP[opt] == st.session_state.current_menu][0]),
                label_visibility="collapsed"
            )
            
            # Update current menu when selection changes
            if selected_menu:
                new_menu = MENU_MAP[selected_menu]
                if st.session_state.get("current_menu") != new_menu:
                    st.session_state["current_menu"] = new_menu
                    st.rerun()