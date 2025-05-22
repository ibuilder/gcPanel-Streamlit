"""
Clean Header Component for gcPanel.

This module provides a streamlined header with project title, logo, and navigation.
"""

import streamlit as st
from app_config import MENU_OPTIONS, MENU_MAP, PROJECT_INFO

def render_header():
    """Render the clean header component."""
    
    # Add some custom CSS for professional header styling
    st.markdown("""
    <style>
    .header-container {
        padding: 1rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .project-title {
        font-size: 18px;
        font-weight: 600;
        margin: 0;
        color: #333;
    }
    .project-details {
        font-size: 14px;
        color: #666;
        margin: 0;
    }
    .stButton button {
        border: none;
        background: none;
        padding: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Use the simpler approach with direct Streamlit components
    # This will ensure the layout works consistently
    with st.container():
        cols = st.columns([1, 3, 1])
        
        # Left column - Logo with tower crane icon (clickable)
        with cols[0]:
            # Create a logo with tower crane to the left of gcPanel text
            st.markdown("""
            <div style="display: flex; align-items: center; cursor: pointer;" onclick="window.location.href='/?view=Dashboard'">
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 24px; color: #0099ff; margin-right: 6px;">🏗️</div>
                    <div>
                        <span style="font-size: 24px; font-weight: 600; letter-spacing: -0.5px;">
                            <span style="color: #2c3e50;">gc</span><span style="color: #0099ff;">Panel</span>
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Hidden button for dashboard navigation
            if st.button("Dashboard", key="logo_dashboard_button", help="Return to Dashboard", type="secondary"):
                st.session_state["current_menu"] = "Dashboard"
                st.rerun()
        
        # Middle column - Project Info (smaller project name)
        with cols[1]:
            st.markdown(f'<p class="project-title">{PROJECT_INFO["name"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="project-details">{PROJECT_INFO["value"]} • {PROJECT_INFO["size"]} • {PROJECT_INFO["floors"]}</p>', unsafe_allow_html=True)
        
        # Right column - Navigation with icons
        with cols[2]:
            st.markdown('<p style="font-size:13px; color:#666; margin-bottom:5px;">Navigation</p>', unsafe_allow_html=True)
            
            # Force label visibility to be visible to ensure icons show up
            selected_menu = st.selectbox(
                "Select Module",
                options=MENU_OPTIONS,
                index=MENU_OPTIONS.index("📊 Dashboard") if "current_menu" not in st.session_state else MENU_OPTIONS.index([opt for opt in MENU_OPTIONS if MENU_MAP[opt] == st.session_state.current_menu][0]),
                label_visibility="collapsed",
                format_func=lambda x: x  # This ensures the icons display correctly
            )
            
            # Update current menu when selection changes
            if selected_menu:
                new_menu = MENU_MAP[selected_menu]
                if st.session_state.get("current_menu") != new_menu:
                    st.session_state["current_menu"] = new_menu
                    st.rerun()