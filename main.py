"""
gcPanel - Highland Tower Development
Enterprise Construction Management Platform
Entry Point - Clean & Minimal
"""

import streamlit as st
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.app_state import AppStateManager
from core.theme_manager import ThemeManager
from core.navigation import NavigationManager
from core.module_registry import ModuleRegistry

def render_login_page():
    """Clean login page"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #60a5fa; font-size: 3rem; margin-bottom: 0.5rem;">gcPanel</h1>
        <h2 style="color: #94a3b8; font-size: 1.5rem; margin-bottom: 2rem;">Highland Tower Development</h2>
        <p style="color: #64748b; font-size: 1.1rem;">Enterprise Construction Management Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Project Access")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_button = st.form_submit_button("Access Project Dashboard", use_container_width=True)
            
            if login_button:
                state_manager = AppStateManager()
                if state_manager.authenticate_user(username, password):
                    st.success("✅ Access granted! Loading project dashboard...")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
        
        with st.expander("Login Information"):
            st.markdown("**Available Access:** admin/admin123, manager/manager123, user/user123")

def render_main_layout(nav_manager, module_registry):
    """Main application layout"""
    nav_manager.render_sidebar_navigation(module_registry)
    
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #1e40af, #3b82f6); padding: 1rem; border-radius: 8px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0;">🏗️ {st.session_state.project_name}</h1>
        <p style="color: #e2e8f0; margin: 0; font-size: 1.1rem;">
            Welcome back, {st.session_state.username} | {st.session_state.current_menu}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    current_module = st.session_state.get("current_menu", "Dashboard")
    module_registry.render_module(current_module)

def main():
    """Main application entry point - keeping it under 50 lines"""
    state_manager = AppStateManager()
    theme_manager = ThemeManager()
    nav_manager = NavigationManager()
    module_registry = ModuleRegistry()
    
    state_manager.initialize()
    theme_manager.apply_current_theme()
    
    if not st.session_state.authenticated:
        render_login_page()
        return
    
    render_main_layout(nav_manager, module_registry)

if __name__ == "__main__":
    main()