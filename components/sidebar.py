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
        st.image("generated-icon.png", width=50)
        st.title("gcPanel")
        
        # Project selection
        st.markdown("### Project")
        project_name = "Highland Tower Development"
        st.markdown(f"**{project_name}**")
        
        # If needed, add a project dropdown here for multi-project support
        
        # Navigation items
        st.markdown("### Navigation")
        
        # Direct Streamlit approach for navigation
        st.button("Dashboard", key="btn_dashboard", use_container_width=True)
        st.button("Project Information", key="btn_project_information", use_container_width=True) 
        st.button("Schedule", key="btn_scheduling", use_container_width=True)
        st.button("Safety", key="btn_safety", use_container_width=True)
        st.button("Contracts", key="btn_contracts", use_container_width=True)
        st.button("Cost Management", key="btn_cost_management", use_container_width=True)
        st.button("Engineering", key="btn_engineering", use_container_width=True)
        st.button("Field Operations", key="btn_field_operations", use_container_width=True)
        st.button("Documents", key="btn_documents", use_container_width=True)
        st.button("BIM Viewer", key="btn_bim_viewer", use_container_width=True)
        st.button("Roadmap", key="btn_roadmap", use_container_width=True)
        st.button("Closeout", key="btn_closeout", use_container_width=True)
        st.button("Settings", key="btn_settings", use_container_width=True)
        
        # Apply custom styling for sidebar buttons
        st.markdown("""
        <style>
            /* Style sidebar buttons to look like a navigation menu */
            [data-testid="baseButton-secondary"] {
                background-color: transparent !important;
                border: none !important;
                text-align: left !important;
                font-weight: normal !important;
                padding: 0.8rem 1rem !important;
                margin-bottom: 0.3rem !important;
                color: #6c757d !important;
                border-radius: 6px !important;
                transition: all 0.15s ease !important;
            }
            
            [data-testid="baseButton-secondary"]:hover {
                background-color: rgba(62, 121, 247, 0.08) !important;
                color: #3e79f7 !important;
            }
            
            /* Highlight the active navigation item */
            .active-nav-item {
                background-color: rgba(62, 121, 247, 0.15) !important;
                color: #3e79f7 !important;
                font-weight: 500 !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
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