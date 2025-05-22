"""
Fixed Header Component for gcPanel.

This module provides a header component that is positioned correctly at the top of the page.
"""

import streamlit as st

def render_fixed_header():
    """
    Render a header that's correctly positioned at the top of the page.
    Uses direct HTML/CSS to ensure proper positioning.
    """
    
    # First, apply fixes to Streamlit's default margins and padding
    st.markdown("""
    <style>
    /* Remove all padding and margins from main container */
    .main .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
        max-width: 100% !important;
    }
    
    /* Fix default Streamlit header */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Fix breadcrumbs */
    .breadcrumb-container {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Ensure first element has no top margin */
    .element-container:first-child {
        margin-top: 0 !important;
    }
    
    /* Force vertical block spacing */
    [data-testid="stVerticalBlock"] > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Style for our custom navigation container */
    .nav-dropdown-container {
        width: 100%;
        text-align: right;
        padding-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create the first part of the header (logo and project info)
    st.markdown("""
    <div style="position:relative; top:0; left:0; right:0; z-index:999; background:#f8f9fa; padding:5px 10px; border-bottom:1px solid #e9ecef; margin:0;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div style="display:flex; align-items:center;">
                <div style="font-size:24px; color:#0099ff; margin-right:5px;">🏗️</div>
                <div>
                    <span style="font-weight:bold; color:#0099ff;">gc</span><span style="font-weight:bold; color:#333333;">Panel</span>
                </div>
            </div>
            <div style="text-align:center;">
                <div style="font-weight:bold; font-size:18px;">Highland Tower Development</div>
                <div style="font-size:12px; color:#666;">$45.5M • 168,500 sq ft • 15 stories above ground, 2 below</div>
            </div>
    """, unsafe_allow_html=True)
    
    # Create a column layout for the third part (navigation)
    col1, col2, col3 = st.columns([7, 1, 2])
    
    # In the third column, place the navigation dropdown
    with col3:
        current_menu = st.session_state.get("current_menu", "Dashboard")
        from app_config import MENU_OPTIONS
        
        selected_menu = st.selectbox(
            label="Navigation", # Adding a proper label for accessibility
            options=MENU_OPTIONS,
            index=MENU_OPTIONS.index(current_menu) if current_menu in MENU_OPTIONS else 0,
            key="nav_dropdown",
            label_visibility="collapsed"
        )
        
        # Update current menu if selection changed
        if selected_menu != current_menu:
            st.session_state.current_menu = selected_menu
            st.rerun()
    
    # Close the header div
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)