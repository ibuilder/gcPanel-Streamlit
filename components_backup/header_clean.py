"""
Clean Header Component for gcPanel.

This module provides a streamlined header with project title, logo, and navigation.
Following modular design principles with separate styles and templates.
"""

import streamlit as st
import os
from app_config import MENU_OPTIONS, MENU_MAP, PROJECT_INFO
from utils.search_manager import SearchManager

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
    
    /* Search bar styling */
    .search-container {
        margin-top: 5px;
    }
    .search-container .stTextInput input {
        border-radius: 20px;
        padding-left: 15px;
        border: 1px solid #ddd;
    }
    .search-container .stTextInput input:focus {
        border-color: #0099ff;
        box-shadow: 0 0 0 1px rgba(0, 153, 255, 0.5);
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
    
    # Use Streamlit column layout with adjusted ratios to accommodate search
    cols = st.columns([1, 2, 2, 1])
    
    # Left column - Home button
    with cols[0]:
        # Empty space where logo used to be
        st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
        
        # Home navigation button
        st.button(
            "Home", 
            key="logo_dashboard_button", 
            help="Return to Dashboard",
            type="secondary",
            on_click=lambda: st.session_state.update({"current_menu": "Dashboard"})
        )
    
    # Middle-left column - Project Info
    with cols[1]:
        # Project name - using Streamlit's text formatting
        st.subheader(PROJECT_INFO["name"])
        
        # Project details
        details = f"{PROJECT_INFO['value']} • {PROJECT_INFO['size']} • {PROJECT_INFO['floors']}"
        st.caption(details)
    
    # Middle-right column - Search
    with cols[2]:
        # Search container
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        # Initialize search system if needed
        if "show_search_results" not in st.session_state:
            st.session_state.show_search_results = False
            
        # Add search input
        search_query = st.text_input(
            "Global Search",
            placeholder="🔍 Search across all modules...",
            key="header_search_input",
            label_visibility="collapsed",
            value=st.session_state.get("global_search_query", "")
        )
        
        # Update session state with current query
        if search_query != st.session_state.get("global_search_query", ""):
            st.session_state.global_search_query = search_query
            
            # Toggle search results display when search is performed
            if search_query:
                st.session_state.show_search_results = True
            else:
                st.session_state.show_search_results = False
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Right column - Navigation with icons
    with cols[3]:
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
    
    # Handle search results display
    if st.session_state.get("show_search_results", False) and st.session_state.get("global_search_query", ""):
        # Add a container for search results
        search_results_container = st.container()
        
        with search_results_container:
            st.markdown("""
            <style>
            .search-results {
                border: 1px solid #eee;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 20px;
                background-color: white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }
            </style>
            <div class="search-results">
            """, unsafe_allow_html=True)
            
            # Perform the search using the search manager
            with st.spinner("Searching..."):
                results = SearchManager.perform_global_search(st.session_state.global_search_query)
            
            # Display close button for search results
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"### Search Results for: '{st.session_state.global_search_query}'")
            with col2:
                if st.button("❌ Close", key="close_search_results"):
                    st.session_state.show_search_results = False
                    st.rerun()
            
            # Render search results
            SearchManager.render_search_results(results)
            
            st.markdown("</div>", unsafe_allow_html=True)