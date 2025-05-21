"""
Clean Header Component for gcPanel.

This module provides a streamlined header with project title, logo, and navigation.
"""

import streamlit as st
from app_config import MENU_OPTIONS, MENU_MAP, PROJECT_INFO

def render_header():
    """Render the clean header component."""
    
    # Add custom CSS for the header
    st.markdown("""
    <style>
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0.5rem;
        background-color: #f8f9fa;
        border-bottom: 1px solid #e9ecef;
        margin-bottom: 1.5rem;
    }
    .logo-section {
        display: flex;
        align-items: center;
    }
    .logo-section img {
        height: 40px;
        margin-right: 0.5rem;
    }
    .project-info {
        flex-grow: 1;
        text-align: center;
    }
    .project-info h2 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
    }
    .project-info p {
        margin: 0;
        font-size: 0.9rem;
        color: #6b7280;
    }
    .nav-section {
        min-width: 150px;
    }
    .stSelectbox {
        margin-bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create the header HTML structure
    header_html = f"""
    <div class="header-container">
        <div class="logo-section">
            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAAB3RJTUUH5AoSEwgTQeHRlwAADJpJREFUaN7FmXmQXVWdxz/n3Pt2evn7dSetdBIISQhLQhaJYJRdR4bSKBnHqRJxA4W4MFUWLkgxDuioVVqMiIrWOFhYjMsiIopsFgFGyBJCSEL29HT6dfrt97737pn743W/7oQ0SYeZmq+q69577j2/8/19l9/v/M5tMcYYfgc2sXELjuPA4KBwzqFPPY0d6QVPQBQa7Dj07GfZB9/FXrCAUIDnCUj/nPeVl5u01R8rLxUGLAsi8fgzz2FZ1jnfL19+OdddN48rlt/D5m9/F4rD0PUa5I6DpyERh9bLoG01NPVA/iC8shE+8Qka2tvP+M6zWvm8Aphh2bR0dcEb2zHGgIDWgucaTCRCPJmktW0RS1csp72tFtsSNm7cRCwaWd2+YP78+ppalFInzfvw5hfIv/dzKB6DzJsw1A/DNRDPwugQtHTC/GXQsBD2vQTPPwMXr4aaOFZNlOG9B/jYP36RWFUVEYv...
        </div>
        <div class="project-info">
            <h2>{PROJECT_INFO['name']}</h2>
            <p>{PROJECT_INFO['value']} • {PROJECT_INFO['size']} • {PROJECT_INFO['floors']}</p>
        </div>
        <div class="nav-section">
            <p style="margin-bottom: 0.2rem; font-size: 0.8rem; color: #6b7280;">Navigation</p>
        </div>
    </div>
    """
    
    # Render the custom header
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Add the navigation dropdown after the custom HTML
    # Use columns to position it correctly on the right side
    col1, col2, col3 = st.columns([4, 1, 1])
    
    with col3:
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