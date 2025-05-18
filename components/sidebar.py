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
        
        # Basic navigation with direct buttons
        if st.button("Dashboard", key="dashboard_btn", use_container_width=True):
            st.session_state.menu = "dashboard"
            st.rerun()
            
        if st.button("Project Information", key="project_info_btn", use_container_width=True):
            st.session_state.menu = "project_information"
            st.rerun()
            
        if st.button("Schedule", key="schedule_btn", use_container_width=True):
            st.session_state.menu = "scheduling"
            st.rerun()
            
        if st.button("Safety", key="safety_btn", use_container_width=True):
            st.session_state.menu = "safety"
            st.rerun()
            
        if st.button("Contracts", key="contracts_btn", use_container_width=True):
            st.session_state.menu = "contracts"
            st.rerun()
            
        if st.button("Cost Management", key="cost_mgmt_btn", use_container_width=True):
            st.session_state.menu = "cost_management"
            st.rerun()
            
        if st.button("Engineering", key="engineering_btn", use_container_width=True):
            st.session_state.menu = "engineering"
            st.rerun()
            
        if st.button("Field Operations", key="field_ops_btn", use_container_width=True):
            st.session_state.menu = "field_operations"
            st.rerun()
            
        if st.button("Documents", key="documents_btn", use_container_width=True):
            st.session_state.menu = "documents"
            st.rerun()
            
        if st.button("BIM Viewer", key="bim_viewer_btn", use_container_width=True):
            st.session_state.menu = "bim_viewer"
            st.rerun()
            
        if st.button("Roadmap", key="roadmap_btn", use_container_width=True):
            st.session_state.menu = "roadmap"
            st.rerun()
            
        if st.button("Closeout", key="closeout_btn", use_container_width=True):
            st.session_state.menu = "closeout"
            st.rerun()
            
        if st.button("Settings", key="settings_btn", use_container_width=True):
            st.session_state.menu = "settings"
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