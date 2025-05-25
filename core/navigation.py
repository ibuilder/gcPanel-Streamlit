"""
Navigation hierarchy and module management for gcPanel
Centralized navigation structure with proper module loading
"""

import streamlit as st
from typing import Dict, List, Tuple, Callable

class NavigationManager:
    """Manages the navigation hierarchy and module loading"""
    
    def __init__(self):
        self.navigation_structure = self._define_navigation_structure()
        self.module_loaders = self._define_module_loaders()
    
    def _define_navigation_structure(self) -> Dict[str, List[Tuple[str, str]]]:
        """Define the hierarchical navigation structure"""
        return {
            "core_management": [
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
            "specialized_modules": [
                ("📊 Analytics", "Analytics"),
                ("📁 Documents", "Documents"),
                ("📅 Scheduling", "Scheduling"),
                ("💳 AIA G702/G703 Billing", "AIA G702/G703 Billing"),
                ("📋 Prime Contract", "Prime Contract"),
                ("🔄 Change Orders", "Change Orders")
            ],
            "field_operations": [
                ("📝 Recent Reports", "Recent Reports"),
                ("📋 Daily Reports", "Daily Reports"),
                ("🔍 Quality Control", "Quality Control"),
                ("📦 Material Management", "Material Management")
            ],
            "ai_systems": [
                ("🤖 AI Assistant", "AI Assistant"),
                ("📱 Mobile Companion", "Mobile Companion")
            ]
        }
    
    def _define_module_loaders(self) -> Dict[str, Callable]:
        """Define module loading functions with proper imports"""
        loaders = {}
        
        # Core Management Modules
        try:
            from modules.dashboard import render_dashboard
            loaders["Dashboard"] = render_dashboard
        except ImportError:
            from gcpanel_core_focused import render_dashboard
            loaders["Dashboard"] = render_dashboard
        
        try:
            from modules.preconstruction import render_preconstruction
            loaders["PreConstruction"] = render_preconstruction
        except ImportError:
            from gcpanel_core_focused import render_preconstruction
            loaders["PreConstruction"] = render_preconstruction
        
        try:
            from modules.engineering import render_engineering
            loaders["Engineering"] = render_engineering
        except ImportError:
            from gcpanel_core_focused import render_engineering
            loaders["Engineering"] = render_engineering
        
        try:
            from modules.field_operations import render_field_operations
            loaders["Field Operations"] = render_field_operations
        except ImportError:
            from gcpanel_core_focused import render_field_operations
            loaders["Field Operations"] = render_field_operations
        
        try:
            from modules.safety import render as safety_render
            loaders["Safety"] = safety_render
        except ImportError:
            from gcpanel_core_focused import render_safety
            loaders["Safety"] = render_safety
        
        try:
            from modules.contracts import render as contracts_render
            loaders["Contracts"] = contracts_render
        except ImportError:
            from gcpanel_core_focused import render_contracts
            loaders["Contracts"] = render_contracts
        
        try:
            from modules.cost_management import render_cost_management
            loaders["Cost Management"] = render_cost_management
        except ImportError:
            from gcpanel_core_focused import render_cost_management
            loaders["Cost Management"] = render_cost_management
        
        try:
            from modules.bim import render_bim
            loaders["BIM"] = render_bim
        except ImportError:
            from gcpanel_core_focused import render_bim
            loaders["BIM"] = render_bim
        
        try:
            from modules.closeout import render as closeout_render
            loaders["Closeout"] = closeout_render
        except ImportError:
            from gcpanel_core_focused import render_closeout
            loaders["Closeout"] = render_closeout
        
        # Specialized Modules
        try:
            from modules.analytics import render_analytics
            loaders["Analytics"] = render_analytics
        except ImportError:
            from gcpanel_core_focused import render_analytics
            loaders["Analytics"] = render_analytics
        
        try:
            from modules.documents import render_documents
            loaders["Documents"] = render_documents
        except ImportError:
            from gcpanel_core_focused import render_documents
            loaders["Documents"] = render_documents
        
        try:
            from modules.scheduling import render_scheduling
            loaders["Scheduling"] = render_scheduling
        except ImportError:
            from gcpanel_core_focused import render_scheduling
            loaders["Scheduling"] = render_scheduling
        
        try:
            from modules.cost_management.aia_billing import render_aia_billing
            loaders["AIA G702/G703 Billing"] = render_aia_billing
        except ImportError:
            from gcpanel_core_focused import render_aia_billing
            loaders["AIA G702/G703 Billing"] = render_aia_billing
        
        # Additional modules
        from gcpanel_core_focused import (
            render_prime_contract, render_change_orders, render_recent_reports,
            render_daily_reports, render_quality_control, render_material_management,
            render_ai_assistant, render_mobile_companion
        )
        
        loaders.update({
            "Prime Contract": render_prime_contract,
            "Change Orders": render_change_orders,
            "Recent Reports": render_recent_reports,
            "Daily Reports": render_daily_reports,
            "Quality Control": render_quality_control,
            "Material Management": render_material_management,
            "AI Assistant": render_ai_assistant,
            "Mobile Companion": render_mobile_companion
        })
        
        return loaders
    
    def render_navigation_section(self, section_name: str, section_modules: List[Tuple[str, str]]):
        """Render a section of navigation with grouped modules"""
        st.markdown(f"### {section_name.replace('_', ' ').title()}")
        
        for display_name, module_key in section_modules:
            if st.button(display_name, key=f"nav_{module_key}", use_container_width=True):
                st.session_state.current_menu = module_key
                st.rerun()
    
    def render_sidebar_navigation(self):
        """Render the complete modular sidebar navigation"""
        with st.sidebar:
            # Project overview section
            st.markdown(f"""
            <div class="project-info">
                <h3 style="color: #60a5fa; margin: 0 0 1rem 0;">Project Overview</h3>
                <p><strong>Investment:</strong> {st.session_state.project_value}</p>
                <p><strong>Residential:</strong> {st.session_state.residential_units} units</p>
                <p><strong>Retail:</strong> {st.session_state.retail_units} spaces</p>
                <p><strong>Status:</strong> <span style="color: #10b981;">Active Development</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Core Management Modules
            self.render_navigation_section("🎯 Core Management", 
                                         self.navigation_structure["core_management"])
            
            # Specialized Modules
            self.render_navigation_section("📊 Specialized Systems", 
                                         self.navigation_structure["specialized_modules"])
            
            # Field Operations
            self.render_navigation_section("👷 Field Operations", 
                                         self.navigation_structure["field_operations"])
            
            # AI Systems
            self.render_navigation_section("🤖 AI Systems", 
                                         self.navigation_structure["ai_systems"])
            
            # Theme toggle
            st.markdown("---")
            current_theme = "🌙 Dark Mode" if st.session_state.theme == "light" else "☀️ Light Mode"
            if st.button(current_theme, use_container_width=True):
                st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
                st.rerun()
    
    def load_module(self, module_key: str):
        """Load and execute the specified module"""
        if module_key in self.module_loaders:
            try:
                self.module_loaders[module_key]()
            except Exception as e:
                st.error(f"Error loading module {module_key}: {str(e)}")
                st.info("Please check module configuration and try again.")
        else:
            st.error(f"Module {module_key} not found in navigation structure")
            st.info("Available modules: " + ", ".join(self.module_loaders.keys()))