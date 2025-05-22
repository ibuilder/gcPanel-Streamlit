"""
Clean Header Component for gcPanel.

This module provides a streamlined header with project title, logo, and navigation.
Following modular design principles with separate styles and templates.
"""

import streamlit as st
import os
from app_config import MENU_OPTIONS, MENU_MAP, PROJECT_INFO

def get_css():
    """Return CSS for header styling."""
    return """
    /* Header styling for gcPanel */
    
    /* Add a subtle border at the bottom of the header and ensure it's at the top */
    .header-container {
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        position: relative;
        top: 0;
        margin-top: 0;
        padding-top: 0.5rem;
    }
    
    /* Crane icon styling */
    .crane-icon {
        font-size: 26px;
        color: #0099ff;
    }
    
    /* Logo text styling */
    .logo-text {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    /* Blue gc text */
    .gc-text {
        color: #0099ff;
    }
    
    /* Panel text */
    .panel-text {
        color: #333333;
    }
    
    /* Navigation label */
    .nav-label {
        font-size: 13px;
        color: #666;
        margin-bottom: 5px;
    }
    
    /* Remove extra padding from the logo button */
    .stButton button {
        padding: 0;
    }
    """

def get_header_container_html():
    """Return HTML for header container."""
    return """<div class="header-container"><!-- Header content --></div>"""

def get_logo_html():
    """Return HTML for logo."""
    return """
    <div class="header-logo">
        <div class="crane-icon">🏗️</div>
        <div class="logo-text">
            <span class="gc-text">gc</span><span class="panel-text">Panel</span>
        </div>
    </div>
    """

def render_header():
    """Render the clean header component using modular styles and templates."""
    
    # Apply CSS styling from the function
    st.markdown(f"<style>{get_css()}</style>", unsafe_allow_html=True)
    
    # Start the header container
    st.markdown(get_header_container_html(), unsafe_allow_html=True)
    
    # Use Streamlit column layout
    cols = st.columns([1, 3, 1])
    
    # Left column - Logo with tower crane icon
    with cols[0]:
        # Create a simple 2-column layout for the logo
        logo_cols = st.columns([1, 3])
        
        # Add logo components
        with logo_cols[0]:
            st.markdown('<div class="crane-icon">🏗️</div>', unsafe_allow_html=True)
        
        with logo_cols[1]:
            st.markdown(
                '<span class="logo-text">'
                '<span class="gc-text">gc</span><span class="panel-text">Panel</span>'
                '</span>', 
                unsafe_allow_html=True
            )
        
        # Home navigation button
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
        st.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)
        
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