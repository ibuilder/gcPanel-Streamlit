"""
Simple and efficient sidebar component for the gcPanel Construction Management Dashboard.
"""

import streamlit as st

def render_sidebar():
    """Render a simplified, efficient sidebar navigation."""
    
    with st.sidebar:
        # Logo and header
        st.image("gcpanel.png", width=50)
        st.title("gcPanel")
        
        # Project name
        st.markdown("### Project")
        st.markdown("**Highland Tower Development**")
        
        # Navigation section
        st.markdown("### Navigation")
        
        # Simple navigation menu using radio buttons for efficiency
        current = st.session_state.get("current_menu", "Dashboard")
        
        selected = st.radio(
            "Navigation",
            ["📊 Dashboard", "📋 Project Information", "📅 Schedule", 
             "⚠️ Safety", "📝 Contracts", "💰 Cost Management", 
             "🔧 Engineering", "🚧 Field Operations", "📄 Documents", 
             "🏢 BIM Viewer", "✅ Closeout", "⚙️ Settings"],
            index=["Dashboard", "Project Information", "Schedule", 
                  "Safety", "Contracts", "Cost Management", 
                  "Engineering", "Field Operations", "Documents", 
                  "BIM", "Closeout", "Settings"].index(current),
            label_visibility="collapsed"
        )
        
        # Map selection back to menu key
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
        
        # Update session state if selection changed
        menu_key = menu_map[selected]
        if menu_key != current:
            st.session_state.current_menu = menu_key
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("© 2025 gcPanel")