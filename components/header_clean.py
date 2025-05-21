"""
Clean Header Component for gcPanel.

This module provides a streamlined header with project title, logo, and navigation.
"""

import streamlit as st
from app_config import MENU_OPTIONS, MENU_MAP, PROJECT_INFO

def render_header():
    """Render the clean header component."""
    
    with st.container():
        # Add logo and project info in the header
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            # Logo
            st.image("gcpanel.png", width=100)
            
        with col2:
            # Project information
            st.markdown(f"""
            <div class='project-info'>
                <h2>{PROJECT_INFO['name']}</h2>
                <p>{PROJECT_INFO['value']} • {PROJECT_INFO['size']} • {PROJECT_INFO['floors']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            # Navigation
            st.write("Navigation")
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
    
    # Optional: Breadcrumbs can be added here if needed