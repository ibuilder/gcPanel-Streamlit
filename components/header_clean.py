"""
Professional header component for gcPanel.

A clean, modern header implemented with pure Python Streamlit components.
"""

import streamlit as st

def render_header():
    """
    Render a header matching the design from the screenshot.
    """
    # Custom CSS to improve the header styling
    st.markdown("""
    <style>
        /* Remove extra padding from the top */
        .block-container {
            padding-top: 1rem !important;
        }
        
        /* Style for the notification badge */
        .notification-badge {
            background-color: #ef4444;
            color: white;
            border-radius: 50%;
            padding: 0.1rem 0.4rem;
            font-size: 0.7rem;
            position: relative;
            top: -0.5rem;
        }
        
        /* Divider styling */
        .header-divider {
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
            border-top: 1px solid #e5e7eb;
        }
        
        /* Active dropdown styling */
        div[data-baseweb="select"] {
            background-color: #f0f7ff;
            border-radius: 6px;
        }
        
        /* Project info styling */
        .project-caption {
            font-size: 0.8rem;
            color: #6b7280;
            margin-bottom: 0;
        }
        
        .project-name {
            font-weight: 600;
            margin-top: 0;
        }
        
        /* Logo styling */
        .gc-logo {
            font-size: 24px;
            font-weight: 700;
        }
        
        .panel-highlight {
            color: #3b82f6;
        }
    </style>
    """, unsafe_allow_html=True)
    
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
    
    # Top header row
    header_row1 = st.container()
    with header_row1:
        col1, col2, col3 = st.columns([1, 1, 1])
        
        # Project info (left)
        with col1:
            st.markdown('<p class="project-caption">Project</p>', unsafe_allow_html=True)
            st.markdown('<p class="project-name">Highland Tower Development</p>', unsafe_allow_html=True)
        
        # Logo (center)
        with col2:
            st.markdown('<div style="text-align: center;"><span class="gc-logo">gc<span class="panel-highlight">Panel</span></span></div>', unsafe_allow_html=True)
        
        # Navigation dropdown (right)
        with col3:
            selected = st.selectbox(
                "Navigation",
                options=list(menu_options.keys()),
                index=list(menu_options.keys()).index(current_menu),
                format_func=lambda x: "Dashboard" if x == "Dashboard" else x,
                label_visibility="collapsed",
                key="header_nav_dropdown"
            )
            
            # Update session state if menu changed
            if selected != current_menu:
                st.session_state.current_menu = selected
                st.rerun()
    
    # Horizontal divider
    st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)
    
    # Breadcrumb and notification row
    header_row2 = st.container()
    with header_row2:
        col1, col2 = st.columns([11, 1])
        
        # Breadcrumb navigation
        with col1:
            st.markdown(f'<a href="#" style="color: #3b82f6; text-decoration: none; font-size: 0.9rem;">Home</a> <span style="color: #6b7280; margin: 0 0.3rem;">></span> <span style="font-size: 0.9rem;">{current_menu}</span>', unsafe_allow_html=True)
        
        # Notification bell
        with col2:
            st.markdown('<div style="text-align: right;">🔔<span class="notification-badge">3</span></div>', unsafe_allow_html=True)
    
    # Main title (only render once, not duplicated)
    st.markdown(f"<h1 style='margin-top: 1rem; margin-bottom: 1rem; font-size: 1.8rem; font-weight: 700;'>{current_menu}</h1>", unsafe_allow_html=True)
    
    # Set a background color for the page (light gray)
    st.markdown("""
    <style>
        body {
            background-color: #f7f9fc;
        }
    </style>
    """, unsafe_allow_html=True)