"""
Ultra-simple sidebar component for the gcPanel Construction Management Dashboard.
"""

import streamlit as st

def render_sidebar():
    """Render an ultra-simple sidebar navigation."""
    
    with st.sidebar:
        # Logo and header
        st.image("gcpanel.png", width=50)
        st.title("gcPanel")
        
        # Project name
        st.markdown("### Project")
        st.markdown("**Highland Tower Development**")
        
        # Navigation section
        st.markdown("### Navigation")
        
        # Simple navigation using native Streamlit selectbox
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
        
        # Use a few simple Streamlit components
        for menu_key, label in nav_items.items():
            if st.button(label, key=f"nav_{menu_key.lower().replace(' ', '_')}"):
                st.session_state.current_menu = menu_key
                st.rerun()
                
        # Footer
        st.markdown("---")
        st.markdown("© 2025 gcPanel")