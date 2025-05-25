"""
Clean Navigation System for gcPanel
Simplified, efficient navigation with module category grouping
"""

import streamlit as st
from typing import Dict, List, Tuple

class NavigationManager:
    """Clean navigation manager with category-based module grouping"""
    
    def __init__(self):
        self.navigation_structure = self._define_navigation_structure()
    
    def _define_navigation_structure(self) -> Dict[str, List[Tuple[str, str]]]:
        """Define clean navigation hierarchy"""
        return {
            "core": [
                ("📊 Dashboard", "Dashboard"),
                ("🏗️ PreConstruction", "PreConstruction"), 
                ("⚙️ Engineering", "Engineering"),
                ("👷 Field Operations", "Field Operations"),
                ("🦺 Safety", "Safety"),
                ("📋 Contracts", "Contracts"),
                ("💰 Cost Management", "Cost Management"),
                ("🏢 BIM", "BIM"),
                ("✅ Closeout", "Closeout")
            ],
            "specialized": [
                ("📊 Analytics", "Analytics"),
                ("📁 Documents", "Documents"),
                ("📅 Scheduling", "Scheduling"),
                ("💳 AIA G702/G703 Billing", "AIA G702/G703 Billing"),
                ("📋 Prime Contract", "Prime Contract"),
                ("🔄 Change Orders", "Change Orders")
            ],
            "field": [
                ("📝 Recent Reports", "Recent Reports"),
                ("📋 Daily Reports", "Daily Reports"),
                ("🔍 Quality Control", "Quality Control"),
                ("📦 Material Management", "Material Management")
            ],
            "ai": [
                ("🤖 AI Assistant", "AI Assistant"),
                ("📱 Mobile Companion", "Mobile Companion")
            ]
        }
    
    def render_sidebar_navigation(self, module_registry):
        """Render clean sidebar navigation with project info"""
        with st.sidebar:
            # Project info header
            project_info = st.session_state
            st.markdown(f"""
            <div class="project-info">
                <h3 style="color: #60a5fa; margin: 0 0 1rem 0;">Highland Tower Development</h3>
                <p><strong>Investment:</strong> {project_info.get('project_value', '$45.5M')}</p>
                <p><strong>Residential:</strong> {project_info.get('residential_units', 120)} units</p>
                <p><strong>Retail:</strong> {project_info.get('retail_units', 8)} spaces</p>
                <p><strong>Status:</strong> <span class="status-active">Active Development</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Render navigation sections
            self._render_nav_section("🎯 Core Management", "core", module_registry)
            self._render_nav_section("📊 Specialized Systems", "specialized", module_registry)
            self._render_nav_section("👷 Field Operations", "field", module_registry)
            self._render_nav_section("🤖 AI Systems", "ai", module_registry)
            
            # Theme toggle
            st.markdown("---")
            from core.theme_manager import ThemeManager
            theme_manager = ThemeManager()
            if st.button(theme_manager.get_theme_button_text(), use_container_width=True):
                theme_manager.toggle_theme()
    
    def _render_nav_section(self, section_title: str, category: str, module_registry):
        """Render a navigation section"""
        st.markdown(f"### {section_title}")
        
        if category in self.navigation_structure:
            for display_name, module_key in self.navigation_structure[category]:
                if st.button(display_name, key=f"nav_{module_key}", use_container_width=True):
                    st.session_state.current_menu = module_key
                    st.rerun()