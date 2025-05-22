"""
Clean Header Component for gcPanel.

This module provides a streamlined header with project title, logo, and navigation.
"""

import streamlit as st
from app_config import MENU_OPTIONS, MENU_MAP, PROJECT_INFO

def render_header():
    """Render the clean header component."""
    
    # Add minimal CSS for styling
    st.markdown("""
    <style>
    /* Add a subtle border at the bottom of the header */
    .header-container {
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
    }
    
    /* Remove extra padding from the logo button */
    .stButton button {
        padding: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create the header container with a CSS class
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    
    # Use Streamlit column layout
    cols = st.columns([1, 3, 1])
    
    # Left column - Logo with tower crane icon
    with cols[0]:
        # Create a simple 2-column layout for the logo
        logo_cols = st.columns([1, 3])
        
        # Tower crane icon
        with logo_cols[0]:
            st.markdown('<div style="font-size: 26px; color: #0099ff;">🏗️</div>', unsafe_allow_html=True)
        
        # gcPanel text
        with logo_cols[1]:
            st.markdown(
                '<span style="font-size: 28px; font-weight: 800; letter-spacing: -0.5px;">'
                '<span style="color: #0099ff;">gc</span><span style="color: #333333;">Panel</span>'
                '</span>', 
                unsafe_allow_html=True
            )
        
        # Hidden button for dashboard navigation - use Streamlit's built-in button
        st.button(
            "Home", 
            key="logo_dashboard_button", 
            help="Return to Dashboard",
            type="secondary",
            on_click=lambda: st.session_state.update({"current_menu": "Dashboard"})
        )
    
    # Middle column - Project Info
    with cols[1]:
        # Project name - using Streamlit's text formatting
        st.subheader(PROJECT_INFO["name"])
        
        # Project details
        details = f"{PROJECT_INFO['value']} • {PROJECT_INFO['size']} • {PROJECT_INFO['floors']}"
        st.caption(details)
    
    # Right column - Navigation with icons
    with cols[2]:
        # Navigation label
        st.caption("Navigation")
        
        # Default selection based on current menu
        default_index = MENU_OPTIONS.index("📊 Dashboard")
        if "current_menu" in st.session_state:
            try:
                # Find the menu option that maps to the current menu
                matching_options = [opt for opt in MENU_OPTIONS if MENU_MAP[opt] == st.session_state.current_menu]
                if matching_options:
                    default_index = MENU_OPTIONS.index(matching_options[0])
            except (ValueError, IndexError):
                # If there's an error, fall back to Dashboard
                pass
        
        # Create the navigation dropdown
        selected_menu = st.selectbox(
            "Select Module",
            options=MENU_OPTIONS,
            index=default_index,
            label_visibility="collapsed",
            format_func=lambda x: x  # Keep the icons
        )
        
        # Handle navigation changes
        if selected_menu:
            new_menu = MENU_MAP[selected_menu]
            if st.session_state.get("current_menu") != new_menu:
                st.session_state["current_menu"] = new_menu
                st.rerun()
    
    # Close the header container
    st.markdown('</div>', unsafe_allow_html=True)