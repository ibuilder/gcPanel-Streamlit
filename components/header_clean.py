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
        
        /* Remove section margins */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* Main container styling */
        .main-container {
            background-color: #f5f7fa;
            padding: 20px;
            border-radius: 5px;
            margin: 0 auto;
            max-width: 100%;
        }
        
        /* Header styling */
        .header-container {
            background-color: white;
            border-radius: 5px;
            padding: 15px 20px;
            margin-bottom: 15px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            position: relative;
        }
        
        /* Code display section */
        .code-display {
            background-color: #f5f7fa;
            border-radius: 5px;
            padding: 15px 20px;
            margin-bottom: 15px;
            font-family: monospace;
            font-size: 14px;
            color: #374151;
            border: 1px solid #e5e7eb;
        }
        
        .code-line {
            margin-bottom: 5px;
            white-space: pre;
        }
        
        /* Navigation row */
        .nav-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
        }
        
        .nav-left {
            display: flex;
            align-items: center;
        }
        
        .home-link {
            font-size: 15px;
            color: #3b82f6;
            text-decoration: none;
            margin-right: 10px;
        }
        
        /* Dashboard title section */
        .dashboard-title {
            font-size: 28px;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 20px;
        }
        
        /* Logo styling */
        .logo-section {
            padding: 5px 10px;
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
            background-color: #f0f7ff;
            border-radius: 6px;
            padding: 8px 16px;
            display: flex;
            align-items: center;
            cursor: pointer;
            margin-left: 10px;
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
        
        /* Notification bell styling */
        .notification-area {
            position: relative;
            margin-left: auto;
            margin-right: 10px;
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
        
        /* Dropdown menu */
        .dropdown {
            position: absolute;
            right: 20px;
            background-color: white;
            display: flex;
            align-items: center;
            border-radius: 5px;
            padding: 5px 10px;
        }
        
        .dropdown-text {
            font-size: 16px;
            font-weight: 500;
            margin-right: 5px;
        }
        
        .dropdown-icon {
            font-size: 16px;
            color: #6b7280;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Render the header based on the HTML code shown in the screenshot
    st.markdown(f"""
    <div class="main-container">
        <div class="header-container">
            <div class="code-display">
                <div class="code-line">&lt;div class="logo-section"&gt;</div>
                <div class="code-line">    &lt;div class="gc-logo"&gt;gc&lt;span class="panel-highlight"&gt;Panel&lt;/span&gt;&lt;/div&gt;</div>
                <div class="code-line">&lt;/div&gt;</div>
                <div class="code-line"></div>
                <div class="code-line">&lt;div class="menu-selector"&gt;</div>
                <div class="code-line">    &lt;span class="menu-icon"&gt;📊&lt;/span&gt;</div>
                <div class="code-line">    &lt;span class="menu-label"&gt;Dashboard&lt;/span&gt;</div>
                <div class="code-line">    &lt;span class="dropdown-arrow"&gt;▼&lt;/span&gt;</div>
                <div class="code-line">&lt;/div&gt;</div>
            </div>
            
            <div class="nav-row">
                <div class="nav-left">
                    <a href="#" class="home-link">Home</a>
                </div>
                
                <div class="dropdown">
                    <span class="dropdown-text">Dashboard</span>
                    <span class="dropdown-icon">▼</span>
                </div>
                
                <div class="notification-area">
                    <span class="notification-bell">🔔</span>
                    <span class="notification-count">3</span>
                </div>
            </div>
        </div>
        
        <div class="dashboard-title">Dashboard</div>
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