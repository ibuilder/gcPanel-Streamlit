"""
Clean header component for gcPanel.

This component provides a fixed header with navigation positioned
exactly as required - in the white header area aligned to the right.
"""

import streamlit as st

def render_header():
    """
    Render a clean header with logo, project info, and right-aligned navigation.
    """
    # CSS is now loaded from external file in ui_manager.py
    
    # Menu options with icons
    menu_options = {
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
    
    # Create a container for the header
    with st.container():
        cols = st.columns([7, 3])
        
        # Logo and project info in first column
        with cols[0]:
            st.markdown("""
            <div class="header-logo-container">
                <div class="header-logo">
                    <img src="gcpanel.png" alt="gcPanel Logo">
                </div>
                <div class="header-project-info">
                    <p class="header-project-label">Project</p>
                    <p class="header-project-name">Highland Tower Development</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation dropdown in second column (right-aligned)
        with cols[1]:
            # Get currently selected menu value from session state
            current_menu = st.session_state.get("current_menu", "Dashboard")
            current_display_menu = next((k for k, v in menu_options.items() if v == current_menu), list(menu_options.keys())[0])
            
            # Create the dropdown with right alignment
            selected = st.selectbox(
                "Navigation",
                options=list(menu_options.keys()),
                index=list(menu_options.keys()).index(current_display_menu),
                label_visibility="collapsed",
                key="header_nav_dropdown"
            )
            
            # Update the session state when a new menu item is selected
            if menu_options[selected] != current_menu:
                st.session_state.current_menu = menu_options[selected]
                st.rerun()
    
    # Draw a separator line below the header
    st.markdown("""
    <div class="header-separator"></div>
    """, unsafe_allow_html=True)