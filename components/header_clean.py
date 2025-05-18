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
    # Hide default Streamlit elements and remove all top spacing
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        margin-top: -80px !important;
    }
    div.appview-container {
        margin-top: -80px !important;
    }
    section[data-testid="stSidebar"] {
        margin-top: -80px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
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
            <div style="display: flex; align-items: center;">
                <div style="margin-right: 20px;">
                    <img src="gcpanel.png" alt="gcPanel Logo" style="max-height: 40px; width: auto;">
                </div>
                <div style="border-left: 1px solid #DADCE0; padding-left: 20px;">
                    <p style="margin: 0; font-size: 14px; font-weight: 600; color: #5F6368;">Project</p>
                    <p style="margin: 0; font-size: 16px; color: #3367D6; font-weight: 600;">Highland Tower Development</p>
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
    <div style="height: 1px; background-color: #DADCE0; margin: 0 -1rem; box-shadow: 0 2px 5px rgba(0,0,0,0.05);"></div>
    """, unsafe_allow_html=True)