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
    
    # Header styling is now moved to external CSS file
    
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
    
    # Create a two-column layout for our header
    header_col1, header_col2 = st.columns([3, 1])
    
    # Left column with the logo and project info
    with header_col1:
        st.markdown("""
        <div class="header-left">
            <div class="gcpanel-logo">
                <img src="gcpanel.png" alt="gcPanel Logo">
            </div>
            <div class="project-info">
                <p class="project-info-label">Project</p>
                <p class="project-name">Highland Tower Development</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Right column with the navigation dropdown
    with header_col2:
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