"""
Simplified sidebar navigation component for the gcPanel Construction Management Dashboard.
"""

import streamlit as st

def render_sidebar():
    """Render the simplified sidebar navigation."""
    
    with st.sidebar:
        # Add logo and title
        st.image("gcpanel.png", width=50)
        st.title("gcPanel")
        
        # Project selection
        st.markdown("### Project")
        project_name = "Highland Tower Development"
        st.markdown(f"**{project_name}**")
        
        # Navigation
        st.markdown("### Navigation")
        
        # Create a dictionary of navigation items with display labels and icons
        nav_items = {
            "Dashboard": "📊 Dashboard",
            "Project Information": "📋 Project Information",
            "Schedule": "📅 Schedule",
            "Safety": "⚠️ Safety",
            "Contracts": "📝 Contracts",
            "Cost Management": "💰 Cost Management",
            "Engineering": "🔧 Engineering",
            "Field Operations": "🚧 Field Operations",
            "Documents": "📄 Documents",
            "BIM": "🏢 BIM Viewer",
            "Closeout": "✅ Closeout",
            "Settings": "⚙️ Settings"
        }
        
        # Create navigation buttons with icons
        for menu_key, display_label in nav_items.items():
            if st.button(f"{display_label}", key=f"nav_{menu_key.lower().replace(' ', '_')}"):
                st.session_state.current_menu = menu_key
                st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("© 2025 gcPanel")