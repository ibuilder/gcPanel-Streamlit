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
    
    # Apply required CSS
    st.markdown("""
    <style>
        /* Remove all extra space and padding */
        .block-container {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Hide the Streamlit selectbox but keep it functional */
        div.row-widget.stSelectbox {
            position: absolute !important;
            right: 20px !important;
            top: 30px !important;
            width: 250px !important;
            opacity: 0 !important;
            z-index: 1000 !important;
            height: 40px !important;
        }
        
        /* Custom styling for the header container */
        .simple-header-container {
            padding: 20px;
            background-color: white;
            position: relative;
            border-bottom: 1px solid #e5e7eb;
            height: 60px;
        }
        
        /* Project section styling */
        .project-section {
            position: absolute;
            left: 20px;
            top: 20px;
        }
        
        .project-label {
            font-size: 12px;
            color: #6b7280;
            margin-bottom: 4px;
            font-weight: 500;
        }
        
        .project-name {
            font-size: 16px;
            color: #374151;
            font-weight: 600;
        }
        
        /* Logo styling in center */
        .logo-section {
            position: absolute;
            left: 50%;
            top: 30px;
            transform: translateX(-50%);
            text-align: center;
        }
        
        .gc-logo {
            font-size: 24px;
            font-weight: 700;
            color: #374151;
        }
        
        .panel-highlight {
            color: #3b82f6;
        }
        
        /* Menu selector styling */
        .menu-selector {
            position: absolute;
            right: 20px;
            top: 20px;
            background-color: #f0f7ff;
            border-radius: 6px;
            padding: 8px 16px;
            display: flex;
            align-items: center;
            cursor: pointer;
        }
        
        .menu-icon {
            margin-right: 8px;
            color: #3b82f6;
        }
        
        .menu-label {
            color: #3b82f6;
            font-weight: 500;
            font-size: 15px;
            margin-right: 8px;
        }
        
        .dropdown-arrow {
            color: #6b7280;
            font-size: 10px;
        }
        
        /* Bottom navbar styling */
        .bottom-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background-color: #f9fafb;
            border-bottom: 1px solid #e5e7eb;
        }
        
        /* Breadcrumbs styling */
        .breadcrumbs {
            display: flex;
            align-items: center;
        }
        
        .breadcrumb-home {
            color: #3b82f6;
            text-decoration: none;
            font-size: 14px;
        }
        
        .breadcrumb-separator {
            margin: 0 8px;
            color: #9ca3af;
        }
        
        .breadcrumb-current {
            color: #374151;
            font-weight: 500;
            font-size: 14px;
        }
        
        /* Notification bell styling */
        .notification-area {
            position: relative;
        }
        
        .notification-bell {
            font-size: 20px;
            color: #6b7280;
            cursor: pointer;
        }
        
        .notification-count {
            position: absolute;
            top: -8px;
            right: -8px;
            background-color: #ef4444;
            color: white;
            border-radius: 50%;
            width: 18px;
            height: 18px;
            font-size: 11px;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header with all components
    st.markdown(f"""
    <div class="simple-header-container">
        <div class="project-section">
            <div class="project-label">Project</div>
            <div class="project-name">Highland Tower Development</div>
        </div>
        
        <div class="logo-section">
            <div class="gc-logo">gc<span class="panel-highlight">Panel</span></div>
        </div>
        
        <div class="menu-selector">
            <span class="menu-icon">📊</span>
            <span class="menu-label">{current_menu}</span>
            <span class="dropdown-arrow">▼</span>
        </div>
    </div>
    
    <div class="bottom-navbar">
        <div class="breadcrumbs">
            <a href="#" class="breadcrumb-home">Home</a>
            <span class="breadcrumb-separator">›</span>
            <span class="breadcrumb-current">{current_menu}</span>
        </div>
        <div class="notification-area">
            <span class="notification-bell">🔔</span>
            <span class="notification-count">3</span>
        </div>
    </div>
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