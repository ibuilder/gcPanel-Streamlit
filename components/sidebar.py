"""
Sidebar navigation component for the gcPanel Construction Management Dashboard.

This module provides a responsive sidebar with navigation options to
different modules in the application.
"""

import streamlit as st
from streamlit_elements import elements, mui
import os

def render_sidebar():
    """Render the sidebar navigation."""
    
    with st.sidebar:
        # Logo and title
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("gcpanel.png", width=50)
        with col2:
            st.markdown("## gcPanel", unsafe_allow_html=True)
        
        # Project selection
        st.markdown("### Project")
        project_name = "Highland Tower Development"
        st.markdown(f"**{project_name}**")
        
        # Navigation items
        st.markdown("### Navigation")
        
        # Define navigation items with icons
        nav_items = [
            {"label": "Dashboard", "icon": "dashboard"},
            {"label": "Project Information", "icon": "info"},
            {"label": "Schedule", "icon": "event"},
            {"label": "Safety", "icon": "health_and_safety"},
            {"label": "Contracts", "icon": "description"},
            {"label": "Cost Management", "icon": "payments"},
            {"label": "Engineering", "icon": "engineering"},
            {"label": "Field Operations", "icon": "construction"},
            {"label": "Documents", "icon": "folder"},
            {"label": "BIM Viewer", "icon": "view_in_ar"},
            {"label": "Roadmap", "icon": "map"},
            {"label": "Closeout", "icon": "task_alt"},
            {"label": "Settings", "icon": "settings"}
        ]
        
        # Create navigation buttons with icons
        for item in nav_items:
            label = item["label"]
            icon = item["icon"]
            key = f"nav_{label.lower().replace(' ', '_')}"
            
            # Create navigation button
            if st.button(f":{icon}: {label}", key=key, use_container_width=True):
                # Convert button label to menu item name
                if label == "Dashboard":
                    st.session_state.menu = "dashboard"
                elif label == "Project Information":
                    st.session_state.menu = "project_information"
                elif label == "Schedule":
                    st.session_state.menu = "scheduling"
                elif label == "Safety":
                    st.session_state.menu = "safety"
                elif label == "Contracts":
                    st.session_state.menu = "contracts"
                elif label == "Cost Management":
                    st.session_state.menu = "cost_management"
                elif label == "Engineering":
                    st.session_state.menu = "engineering"
                elif label == "Field Operations":
                    st.session_state.menu = "field_operations"
                elif label == "Documents":
                    st.session_state.menu = "documents"
                elif label == "BIM Viewer":
                    st.session_state.menu = "bim_viewer"
                elif label == "Roadmap":
                    st.session_state.menu = "roadmap"
                elif label == "Closeout":
                    st.session_state.menu = "closeout"
                elif label == "Settings":
                    st.session_state.menu = "settings"
                
                # Rerun the app to update the UI
                st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("© 2025 gcPanel", help="Made with ❤️ by the gcPanel team")

def handle_navigation():
    """Handle navigation events from the sidebar."""
    # Change the module based on the clicked button
    if st.session_state.get("btn_dashboard", False):
        st.session_state.menu = "dashboard"
    elif st.session_state.get("btn_project_information", False):
        st.session_state.menu = "project_information"
    elif st.session_state.get("btn_scheduling", False):
        st.session_state.menu = "scheduling"
    elif st.session_state.get("btn_safety", False):
        st.session_state.menu = "safety"
    elif st.session_state.get("btn_contracts", False):
        st.session_state.menu = "contracts"
    elif st.session_state.get("btn_cost_management", False):
        st.session_state.menu = "cost_management"
    elif st.session_state.get("btn_engineering", False):
        st.session_state.menu = "engineering"
    elif st.session_state.get("btn_field_operations", False):
        st.session_state.menu = "field_operations"
    elif st.session_state.get("btn_documents", False):
        st.session_state.menu = "documents"
    elif st.session_state.get("btn_roadmap", False):
        st.session_state.menu = "roadmap"
    elif st.session_state.get("btn_closeout", False):
        st.session_state.menu = "closeout"
    elif st.session_state.get("btn_settings", False):
        st.session_state.menu = "settings"