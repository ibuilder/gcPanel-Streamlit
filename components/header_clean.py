"""
Professional header component for gcPanel.

A clean, modern header that matches the design specification
with project info, logo, and dropdown navigation.
"""

import streamlit as st

def render_header():
    """
    Render a simple, clean header exactly matching the design specification.
    """
    # Menu options without icons for selector
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
    
    # Apply required CSS - removed extra/improper selectors
    st.markdown("""
    <style>
        /* Base styles */
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        }
        
        /* Remove top padding */
        .block-container {
            padding-top: 0 !important;
        }
        
        /* Hide selectbox visually but keep it functional */
        div.row-widget.stSelectbox {
            position: absolute !important;
            right: 20px !important;
            top: 30px !important;
            width: 250px !important;
            opacity: 0 !important;
            z-index: 1000 !important;
            height: 40px !important;
        }
        
        /* Header wrapper */
        .header-wrapper {
            background-color: #fff;
            padding: 1rem 1.5rem;
            border-bottom: 1px solid #e5e7eb;
        }
        
        /* Project info - left side */
        .project-info {
            position: absolute;
            left: 20px;
            top: 20px;
        }
        
        .project-label {
            color: #6b7280;
            font-size: 12px;
            font-weight: 500;
        }
        
        .project-name {
            color: #111827;
            font-size: 16px;
            font-weight: 600;
        }
        
        /* Logo section - center */
        .logo-section {
            text-align: center;
            padding: 1rem 0;
        }
        
        .gc-logo {
            font-size: 24px;
            font-weight: 700;
        }
        
        .panel-highlight {
            color: #3b82f6;
        }
        
        /* Nav & breadcrumbs */
        .nav-area {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background-color: #f9fafb;
            padding: 0.75rem 1.5rem;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .home-link {
            color: #3b82f6;
            text-decoration: none;
            font-size: 14px;
        }
        
        /* Menu selector - right side */
        .menu-selector {
            position: absolute;
            right: 20px;
            top: 20px;
            background-color: #f0f7ff;
            border-radius: 6px;
            padding: 8px 14px;
            display: flex;
            align-items: center;
        }
        
        .menu-icon {
            color: #3b82f6;
            margin-right: 8px;
            font-size: 16px;
        }
        
        .menu-label {
            color: #3b82f6;
            font-weight: 500;
            margin-right: 8px;
        }
        
        .dropdown-arrow {
            color: #6b7280;
            font-size: 12px;
        }
        
        /* Notification bell */
        .notification-bell {
            position: relative;
            margin-left: auto;
        }
        
        .bell-icon {
            color: #6b7280;
            font-size: 20px;
            cursor: pointer;
        }
        
        .notification-badge {
            position: absolute;
            top: -8px;
            right: -8px;
            background-color: #ef4444;
            color: white;
            font-size: 11px;
            font-weight: bold;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Dashboard title */
        .dashboard-title {
            font-size: 2rem;
            font-weight: 700;
            color: #111827;
            margin: 1.5rem 0 1rem;
            padding-left: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header & navigation
    st.markdown(f"""
    <!-- Header with logo and navigation -->
    <div class="header-wrapper">
        <!-- Project info - left -->
        <div class="project-info">
            <div class="project-label">Project</div>
            <div class="project-name">Highland Tower Development</div>
        </div>
        
        <!-- Logo section - center -->
        <div class="logo-section">
            <div class="gc-logo">gc<span class="panel-highlight">Panel</span></div>
        </div>
        
        <!-- Menu selector - right -->
        <div class="menu-selector">
            <span class="menu-icon">📊</span>
            <span class="menu-label">{current_menu}</span>
            <span class="dropdown-arrow">▼</span>
        </div>
    </div>
    
    <!-- Navigation area with breadcrumbs -->
    <div class="nav-area">
        <a href="#" class="home-link">Home</a>
        
        <!-- Notification bell -->
        <div class="notification-bell">
            <span class="bell-icon">🔔</span>
            <span class="notification-badge">3</span>
        </div>
    </div>
    
    <!-- Main title -->
    <div class="dashboard-title">{current_menu}</div>
    """, unsafe_allow_html=True)
    
    # Dropdown selector (hidden but functional)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        selected = st.selectbox(
            "Navigation",
            options=list(menu_options.keys()),
            index=list(menu_options.keys()).index(current_menu),
            label_visibility="collapsed",
            key="header_nav_dropdown"
        )
        
        # Update session state if menu changed
        if selected != current_menu:
            st.session_state.current_menu = selected
            st.rerun()