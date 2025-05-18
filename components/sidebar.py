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
        
        # Create the navigation HTML with data attributes for JavaScript interaction
        nav_items_html = """
        <ul class="nav-list">
            <li class="nav-item" data-module="dashboard">
                <i class="material-icons">dashboard</i>
                Dashboard
            </li>
            <li class="nav-item" data-module="project_information">
                <i class="material-icons">info</i>
                Project Information
            </li>
            <li class="nav-item" data-module="scheduling">
                <i class="material-icons">event</i>
                Schedule
            </li>
            <li class="nav-item" data-module="safety">
                <i class="material-icons">health_and_safety</i>
                Safety
            </li>
            <li class="nav-item" data-module="contracts">
                <i class="material-icons">description</i>
                Contracts
            </li>
            <li class="nav-item" data-module="cost_management">
                <i class="material-icons">payments</i>
                Cost Management
            </li>
            <li class="nav-item" data-module="engineering">
                <i class="material-icons">engineering</i>
                Engineering
            </li>
            <li class="nav-item" data-module="field_operations">
                <i class="material-icons">construction</i>
                Field Operations
            </li>
            <li class="nav-item" data-module="documents">
                <i class="material-icons">folder</i>
                Documents
            </li>
            <li class="nav-item" data-module="roadmap">
                <i class="material-icons">map</i>
                Roadmap
            </li>
            <li class="nav-item" data-module="closeout">
                <i class="material-icons">task_alt</i>
                Closeout
            </li>
            <li class="nav-item" data-module="settings">
                <i class="material-icons">settings</i>
                Settings
            </li>
        </ul>
        """
        
        st.markdown(nav_items_html, unsafe_allow_html=True)
        
        # Hidden buttons for each navigation item (for Streamlit state management)
        # These will be clicked by JavaScript
        with st.container():
            st.write("")  # Spacer
            cols = st.columns(3)
            
            # Add buttons (hidden with display:none in CSS)
            with cols[0]:
                dashboard_clicked = st.button(
                    "Dashboard",
                    key="btn_dashboard",
                    help="Go to Dashboard",
                    use_container_width=True
                )
            
            with cols[1]:
                project_info_clicked = st.button(
                    "Project Info",
                    key="btn_project_information",
                    help="Go to Project Information",
                    use_container_width=True
                )
                
            with cols[2]:
                scheduling_clicked = st.button(
                    "Schedule",
                    key="btn_scheduling",
                    help="Go to Schedule",
                    use_container_width=True
                )
                
            with cols[0]:
                safety_clicked = st.button(
                    "Safety",
                    key="btn_safety",
                    help="Go to Safety",
                    use_container_width=True
                )
                
            with cols[1]:
                contracts_clicked = st.button(
                    "Contracts",
                    key="btn_contracts",
                    help="Go to Contracts",
                    use_container_width=True
                )
                
            with cols[2]:
                cost_mgmt_clicked = st.button(
                    "Cost Management",
                    key="btn_cost_management",
                    help="Go to Cost Management",
                    use_container_width=True
                )
                
            with cols[0]:
                engineering_clicked = st.button(
                    "Engineering",
                    key="btn_engineering",
                    help="Go to Engineering",
                    use_container_width=True
                )
                
            with cols[1]:
                field_ops_clicked = st.button(
                    "Field Operations",
                    key="btn_field_operations",
                    help="Go to Field Operations",
                    use_container_width=True
                )
                
            with cols[2]:
                documents_clicked = st.button(
                    "Documents",
                    key="btn_documents",
                    help="Go to Documents",
                    use_container_width=True
                )
                
            with cols[0]:
                roadmap_clicked = st.button(
                    "Roadmap",
                    key="btn_roadmap",
                    help="Go to Roadmap",
                    use_container_width=True
                )
                
            with cols[1]:
                closeout_clicked = st.button(
                    "Closeout",
                    key="btn_closeout",
                    help="Go to Closeout",
                    use_container_width=True
                )
                
            with cols[2]:
                settings_clicked = st.button(
                    "Settings",
                    key="btn_settings",
                    help="Go to Settings",
                    use_container_width=True
                )
        
        # Hide these buttons with CSS
        st.markdown("""
        <style>
            div[data-testid="column"] button {
                display: none;
            }
            
            /* Add styles to ensure navigation items are visible */
            .nav-list {
                list-style: none;
                padding-left: 0;
                margin-top: 1rem;
            }
            
            .nav-item {
                padding: 0.8rem 1rem;
                margin-bottom: 0.5rem;
                display: flex;
                align-items: center;
                cursor: pointer;
                color: #6c757d;
                border-radius: 6px;
                transition: all 0.15s ease;
                font-size: 0.95rem;
                user-select: none;
            }
            
            .nav-item:hover {
                background-color: rgba(62, 121, 247, 0.08);
                color: #3e79f7;
            }
            
            .nav-item.active {
                background-color: rgba(62, 121, 247, 0.15);
                color: #3e79f7;
                font-weight: 500;
            }
            
            .nav-item i {
                margin-right: 0.75rem;
                font-size: 1.25rem;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Add JavaScript for navigation highlighting
        st.markdown("""
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Find active module from URL or other state
                const currentPath = window.location.pathname;
                const urlParams = new URLSearchParams(window.location.search);
                let activeModule = urlParams.get('module') || 'dashboard';
                
                // Highlight the active navigation item
                const navItems = document.querySelectorAll('.nav-item');
                navItems.forEach(item => {
                    const module = item.getAttribute('data-module');
                    if (module === activeModule) {
                        item.classList.add('active');
                    }
                    
                    // Add click event to each item
                    item.addEventListener('click', function() {
                        // Reset all items
                        navItems.forEach(i => i.classList.remove('active'));
                        
                        // Mark this one as active
                        item.classList.add('active');
                        
                        // Find the matching hidden button and click it
                        const buttonId = `btn_${module}`;
                        const button = document.querySelector(`button[key="${buttonId}"]`);
                        if (button) {
                            button.click();
                        }
                    });
                });
            });
        </script>
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