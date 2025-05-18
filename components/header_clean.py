"""
Professional header component for gcPanel.

A clean, modern header that matches the design specification
with project info, logo, and dropdown navigation.
"""

import streamlit as st

def render_header():
    """
    Render the professionally-designed header for gcPanel.
    """
    # Menu options with icons for selector
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
    
    # Get menu icon map
    menu_icons = {
        "Dashboard": "📊",
        "Project Information": "📋",
        "Schedule": "📅", 
        "Safety": "⚠️",
        "Contracts": "📝",
        "Cost Management": "💰",
        "Engineering": "🔧",
        "Field Operations": "🚧",
        "Documents": "📄",
        "BIM": "🏢",
        "Closeout": "✅",
        "Settings": "⚙️"
    }
    
    # Apply styles for fixed header
    st.markdown("""
    <style>
        /* Remove extra space at the top */
        .block-container {
            padding-top: 0 !important;
        }
        
        /* Hide selectbox visually but keep it functional */
        div.row-widget.stSelectbox {
            position: absolute;
            right: 20px;
            top: 28px;
            width: 250px;
            opacity: 0;
            z-index: 10;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main Header HTML with embedded styles
    header_html = f"""
    <style>
        /* Header Styling */
        .gc-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 25px;
            background-color: white;
            border-bottom: 1px solid #eaeaea;
        }}
        
        /* Left Section - Project Info */
        .left-section {{
            flex: 1;
        }}
        
        .project-label {{
            font-size: 12px;
            color: #6c757d;
            margin-bottom: 3px;
            font-weight: 500;
        }}
        
        .project-name {{
            font-size: 16px;
            color: #343a40;
            font-weight: 600;
        }}
        
        /* Center Section - Logo */
        .center-section {{
            flex: 1;
            display: flex;
            justify-content: center;
        }}
        
        .gc-logo {{
            font-size: 24px;
            font-weight: 700;
            color: #343a40;
        }}
        
        .panel-part {{
            color: #3b82f6;
        }}
        
        /* Right Section - Menu */
        .right-section {{
            flex: 1;
            display: flex;
            justify-content: flex-end;
        }}
        
        .menu-selector {{
            display: flex;
            align-items: center;
            background-color: #f0f7ff;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            color: #3b82f6;
        }}
        
        .menu-icon {{
            margin-right: 8px;
        }}
        
        .menu-label {{
            font-weight: 500;
            font-size: 15px;
        }}
        
        .dropdown-arrow {{
            margin-left: 8px;
            font-size: 10px;
            color: #6c757d;
        }}
        
        /* Subheader Styling */
        .subheader {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 25px;
            background-color: #f8f9fa;
            border-bottom: 1px solid #eaeaea;
        }}
        
        /* Breadcrumbs */
        .breadcrumbs {{
            display: flex;
            align-items: center;
        }}
        
        .breadcrumb-link {{
            color: #6c757d;
            text-decoration: none;
            font-size: 14px;
        }}
        
        .breadcrumb-separator {{
            margin: 0 8px;
            color: #adb5bd;
        }}
        
        .breadcrumb-current {{
            color: #343a40;
            font-weight: 500;
            font-size: 14px;
        }}
        
        /* Notification Bell */
        .notification-bell {{
            position: relative;
        }}
        
        .bell-icon {{
            font-size: 20px;
            color: #6c757d;
            cursor: pointer;
        }}
        
        .notification-count {{
            position: absolute;
            top: -8px;
            right: -8px;
            background-color: #dc3545;
            color: white;
            font-size: 11px;
            font-weight: bold;
            border-radius: 50%;
            width: 18px;
            height: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
    </style>
    
    <header class="gc-header">
        <div class="left-section">
            <div class="project-label">Project</div>
            <div class="project-name">Highland Tower Development</div>
        </div>
        
        <div class="center-section">
            <div class="gc-logo">gc<span class="panel-part">Panel</span></div>
        </div>
        
        <div class="right-section">
            <div class="menu-selector">
                <span class="menu-icon">{menu_icons.get(current_menu, "")}</span>
                <span class="menu-label">{current_menu}</span>
                <span class="dropdown-arrow">▼</span>
            </div>
        </div>
    </header>
    
    <div class="subheader">
        <div class="breadcrumbs">
            <a href="#" class="breadcrumb-link">Home</a>
            <span class="breadcrumb-separator">›</span>
            <span class="breadcrumb-current">{current_menu}</span>
        </div>
        <div class="notification-bell">
            <i class="bell-icon">🔔</i>
            <span class="notification-count">3</span>
        </div>
    </div>
    """
    
    # Render the header
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Dropdown selector (hidden but functional)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        selected = st.selectbox(
            label="Navigation",
            options=list(menu_options.keys()),
            index=list(menu_options.keys()).index(current_menu),
            label_visibility="collapsed",
            key="header_nav_dropdown"
        )
        
        # Update the session state when a new menu item is selected
        if selected != current_menu:
            st.session_state.current_menu = selected
            st.rerun()