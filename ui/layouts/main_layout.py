"""
Main Layout for gcPanel
Clean main application layout with navigation and content areas
"""

import streamlit as st

def render_main_layout(nav_manager, module_registry):
    """Render the main application layout with sidebar navigation and content"""
    
    # Render sidebar navigation
    nav_manager.render_sidebar_navigation(module_registry)
    
    # Main content area
    render_main_content_area(module_registry)

def render_main_content_area(module_registry):
    """Render the main content area based on current menu selection"""
    
    # Header with project info
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #1e40af, #3b82f6); padding: 1rem; border-radius: 8px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0;">🏗️ {st.session_state.project_name}</h1>
        <p style="color: #e2e8f0; margin: 0; font-size: 1.1rem;">
            Welcome back, {st.session_state.username} | {st.session_state.current_menu}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render selected module
    current_module = st.session_state.get("current_menu", "Dashboard")
    module_registry.render_module(current_module)