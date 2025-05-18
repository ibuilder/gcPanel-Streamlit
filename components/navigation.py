"""
Basic navigation component for the gcPanel Construction Management Dashboard.
"""

import streamlit as st

def render_navigation():
    """Render a simple navigation sidebar."""
    
    # Add logo and title
    st.sidebar.image("gcpanel.png", width=100)
    st.sidebar.title("gcPanel")
    
    # Project selection
    st.sidebar.markdown("### Project")
    st.sidebar.markdown("**Highland Tower Development**")
    
    # Navigation section
    st.sidebar.markdown("### Navigation")
    
    # Navigation items with icons
    nav_items = [
        ("Dashboard", "📊 Dashboard"),
        ("Project Information", "📋 Project Information"),
        ("Schedule", "📅 Schedule"),
        ("Safety", "⚠️ Safety"),
        ("Contracts", "📝 Contracts"),
        ("Cost Management", "💰 Cost Management"),
        ("Engineering", "🔧 Engineering"),
        ("Field Operations", "🚧 Field Operations"),
        ("Documents", "📄 Documents"),
        ("BIM", "🏢 BIM Viewer"),
        ("Closeout", "✅ Closeout"),
        ("Settings", "⚙️ Settings")
    ]
    
    # Create the navigation buttons
    for menu_key, label in nav_items:
        if st.sidebar.button(label, key=f"nav_{menu_key.lower().replace(' ', '_')}"):
            st.session_state.current_menu = menu_key
            st.rerun()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("© 2025 gcPanel")