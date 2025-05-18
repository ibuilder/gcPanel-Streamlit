"""
Header navigation component with fixed positioning for the gcPanel application.

This component provides a horizontal header with logo, project info,
and navigation controls in the exact positions requested.
"""

import streamlit as st

def render_header_nav():
    """
    Render the main application header with navigation elements.
    
    This creates a horizontal header with:
    - Logo and project info on the left
    - Navigation dropdown on the right
    """
    
    # Apply custom CSS for header styling
    st.markdown("""
    <style>
    /* Header container */
    .header-wrapper {
        position: relative;
        background-color: white;
        margin-bottom: 2rem;
        border-bottom: 1px solid #DADCE0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Logo and project info */
    .gcpanel-logo {
        display: inline-block;
        vertical-align: middle;
        padding: 10px;
    }
    
    .project-info {
        display: inline-block;
        vertical-align: middle;
        margin-left: 20px;
        border-left: 1px solid #DADCE0;
        padding-left: 20px;
    }
    
    .project-info-label {
        margin: 0;
        font-size: 14px;
        font-weight: 600;
        color: #5F6368;
    }
    
    .project-name {
        margin: 0;
        font-size: 16px;
        color: #3367D6;
        font-weight: 600;
    }
    
    /* Fix for Streamlit's extra space */
    .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
        max-width: 100% !important;
    }
    
    /* Remove extra padding from the main area */
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-bottom: 1rem !important;
        margin-top: 0 !important;
    }
    
    /* Fix top margin in stApp */
    [data-testid="stAppViewContainer"] > div:first-child {
        margin-top: 0 !important;
    }
    
    [data-testid="stVerticalBlock"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Position the navigation dropdown in the top right */
    .nav-dropdown-container {
        position: absolute;
        top: 15px;
        right: 20px;
        width: 200px;
    }
    
    /* Hide the label for the dropdown */
    .nav-dropdown-container label {
        display: none;
    }
    
    /* Styling for the dropdown */
    .nav-dropdown-container div[data-baseweb="select"] {
        background-color: #f5f7fa;
        border-radius: 6px;
        border: 1px solid #e1e4e8;
        transition: all 0.2s;
    }
    
    .nav-dropdown-container div[data-baseweb="select"]:hover {
        border-color: #3367D6;
        box-shadow: 0 0 0 1px rgba(51, 103, 214, 0.5);
    }
    
    /* Dropdown list styling */
    div[role="listbox"] {
        border-radius: 6px;
        border: 1px solid #e1e4e8;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    
    div[role="option"] {
        padding: 8px 12px;
        transition: background-color 0.2s;
    }
    
    div[role="option"]:hover {
        background-color: rgba(51, 103, 214, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Menu options
    menu_options = [
        "📊 Dashboard", 
        "📋 Project Information",
        "📅 Schedule",
        "⚠️ Safety",
        "📝 Contracts", 
        "💰 Cost Management",
        "🔧 Engineering",
        "🚧 Field Operations",
        "📄 Documents",
        "🏢 BIM Viewer",
        "✅ Closeout",
        "⚙️ Settings"
    ]
    
    # Mapping from display name to internal name
    menu_map = {
        "📊 Dashboard": "Dashboard", 
        "📋 Project Information": "Project Information",
        "📅 Schedule": "Schedule",
        "⚠️ Safety": "Safety",
        "📝 Contracts": "Contracts", 
        "💰 Cost Management": "Cost Management",
        "🔧 Engineering": "Engineering",
        "🚧 Field Operations": "Field Operations",
        "📄 Documents": "Documents",
        "🏢 BIM Viewer": "BIM",
        "✅ Closeout": "Closeout",
        "⚙️ Settings": "Settings"
    }
    
    # Create the header with logo and project info
    st.markdown("""
    <div class="header-wrapper">
        <div class="gcpanel-logo">
            <img src="static/images/gcpanel-logo.svg" alt="gcPanel Logo" width="150">
        </div>
        <div class="project-info">
            <p class="project-info-label">Project</p>
            <p class="project-name">Highland Tower Development</p>
        </div>
        <div class="nav-dropdown-container" id="nav-dropdown-container"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a container for the navigation dropdown
    with st.container():
        # Apply CSS to position the dropdown container in the right spot
        st.markdown("""
        <style>
        /* Move this specific dropdown to the target location */
        [data-testid="stSelectbox"] {
            position: absolute;
            top: 15px;
            right: 20px;
            width: 200px;
            z-index: 1000;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Get currently selected menu value from session state
        current_display_menu = next((k for k, v in menu_map.items() if v == st.session_state.get("current_menu", "Dashboard")), menu_options[0])
        
        # Create the navigation dropdown
        selected = st.selectbox(
            "Select Module",
            menu_options,
            index=menu_options.index(current_display_menu),
            label_visibility="collapsed",
            key="main_nav_dropdown"
        )
        
        # Update state based on selection
        current_menu = menu_map[selected]
        if current_menu != st.session_state.get("current_menu"):
            st.session_state.current_menu = current_menu
            st.rerun()