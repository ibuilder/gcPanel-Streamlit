"""
Simple and effective sidebar component for the gcPanel Construction Management Dashboard.
"""

import streamlit as st

def render_sidebar():
    """Render a simple but effective sidebar navigation."""
    
    with st.sidebar:
        # Logo and header
        st.image("gcpanel.png", width=50)
        st.title("gcPanel")
        
        # Project name
        st.markdown("### Project")
        st.markdown("**Highland Tower Development**")
        
        # Navigation section
        st.markdown("### Navigation")
        
        # Style the navigation menu items
        st.markdown("""
        <style>
        div.row-widget.stButton > button {
            width: 100%;
            text-align: left;
            border: none;
            background-color: transparent;
            font-weight: normal;
            margin: 0px;
            padding: 5px 10px;
            border-radius: 3px;
        }
        div.row-widget.stButton > button:hover {
            background-color: rgba(151, 166, 195, 0.15);
        }
        </style>
        """, unsafe_allow_html=True)
        
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
        
        # Create navigation buttons for each item
        for menu_key, label in nav_items:
            if st.button(label, key=f"nav_{menu_key.lower().replace(' ', '_')}"):
                st.session_state.current_menu = menu_key
                st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("© 2025 gcPanel")