"""
Module Registry for gcPanel
Centralized module loading and management with standardized interface
"""

import streamlit as st
import importlib
from typing import Dict, Callable, Optional

class ModuleRegistry:
    """Manages module registration and loading with standardized interface"""
    
    def __init__(self):
        self.modules = {}
        self.module_mapping = self._define_module_mapping()
        self._register_all_modules()
    
    def _define_module_mapping(self) -> Dict[str, dict]:
        """Define all available modules with their metadata"""
        return {
            "Dashboard": {
                "path": "gcpanel_core_focused",
                "function": "render_dashboard",
                "category": "core",
                "description": "Main project dashboard with KPIs"
            },
            "PreConstruction": {
                "path": "gcpanel_core_focused", 
                "function": "render_preconstruction",
                "category": "core",
                "description": "Pre-construction planning and design"
            },
            "Engineering": {
                "path": "gcpanel_core_focused",
                "function": "render_engineering", 
                "category": "core",
                "description": "Engineering drawings and specifications"
            },
            "Field Operations": {
                "path": "gcpanel_core_focused",
                "function": "render_field_operations",
                "category": "core", 
                "description": "Daily field operations management"
            },
            "Safety": {
                "path": "modules.safety",
                "function": "render",
                "fallback_path": "gcpanel_core_focused",
                "fallback_function": "render_safety",
                "category": "core",
                "description": "Safety management and incident tracking"
            },
            "Contracts": {
                "path": "modules.contracts",
                "function": "render",
                "fallback_path": "gcpanel_core_focused", 
                "fallback_function": "render_contracts",
                "category": "core",
                "description": "Contract management and change orders"
            },
            "Cost Management": {
                "path": "gcpanel_core_focused",
                "function": "render_cost_management",
                "category": "core",
                "description": "Cost tracking and budget management"
            },
            "BIM": {
                "path": "modules.bim",
                "function": "render_bim",
                "fallback_path": "gcpanel_core_focused",
                "fallback_function": "render_bim", 
                "category": "core",
                "description": "3D modeling and clash detection"
            },
            "Closeout": {
                "path": "modules.closeout",
                "function": "render",
                "fallback_path": "gcpanel_core_focused",
                "fallback_function": "render_closeout",
                "category": "core", 
                "description": "Project closeout and handover"
            },
            "Analytics": {
                "path": "gcpanel_core_focused",
                "function": "render_analytics",
                "category": "specialized",
                "description": "Advanced analytics and reporting"
            },
            "Documents": {
                "path": "gcpanel_core_focused", 
                "function": "render_documents",
                "category": "specialized",
                "description": "Document management system"
            },
            "Scheduling": {
                "path": "modules.scheduling",
                "function": "render_scheduling",
                "fallback_path": "gcpanel_core_focused",
                "fallback_function": "render_scheduling",
                "category": "specialized",
                "description": "Project scheduling and timeline management"
            },
            "AIA G702/G703 Billing": {
                "path": "modules.cost_management.aia_billing",
                "function": "render_aia_billing",
                "fallback_path": "gcpanel_core_focused", 
                "fallback_function": "render_aia_billing",
                "category": "specialized",
                "description": "AIA standard billing and payment applications"
            },
            "Prime Contract": {
                "path": "gcpanel_core_focused",
                "function": "render_prime_contract",
                "category": "specialized",
                "description": "Prime contract management"
            },
            "Change Orders": {
                "path": "gcpanel_core_focused",
                "function": "render_change_orders", 
                "category": "specialized",
                "description": "Change order processing and tracking"
            },
            "Recent Reports": {
                "path": "gcpanel_core_focused",
                "function": "render_recent_reports",
                "category": "field",
                "description": "Recent field reports and updates"
            },
            "Daily Reports": {
                "path": "gcpanel_core_focused",
                "function": "render_daily_reports",
                "category": "field",
                "description": "Daily construction reports"
            },
            "Quality Control": {
                "path": "gcpanel_core_focused",
                "function": "render_quality_control",
                "category": "field", 
                "description": "Quality control and inspections"
            },
            "Material Management": {
                "path": "gcpanel_core_focused",
                "function": "render_material_management",
                "category": "field",
                "description": "Material tracking and inventory"
            },
            "AI Assistant": {
                "path": "gcpanel_core_focused",
                "function": "render_ai_assistant",
                "category": "ai",
                "description": "AI-powered construction assistant"
            },
            "Mobile Companion": {
                "path": "gcpanel_core_focused", 
                "function": "render_mobile_companion",
                "category": "ai",
                "description": "Mobile companion application"
            }
        }
    
    def _register_all_modules(self):
        """Register all modules with error handling"""
        for module_name, config in self.module_mapping.items():
            self.modules[module_name] = self._load_module_function(config)
    
    def _load_module_function(self, config: dict) -> Optional[Callable]:
        """Load a module function with fallback support"""
        # Try primary path first
        try:
            module = importlib.import_module(config["path"])
            return getattr(module, config["function"])
        except (ImportError, AttributeError):
            # Try fallback if available
            if "fallback_path" in config and "fallback_function" in config:
                try:
                    module = importlib.import_module(config["fallback_path"])
                    return getattr(module, config["fallback_function"])
                except (ImportError, AttributeError):
                    pass
        
        # Return error function if all fails
        return self._create_error_function(config)
    
    def _create_error_function(self, config: dict) -> Callable:
        """Create an error display function for failed modules"""
        def error_function():
            st.error(f"Module '{config.get('description', 'Unknown')}' could not be loaded")
            st.info("Please check module configuration and try again.")
            
            with st.expander("Technical Details"):
                st.code(f"""
                Primary Path: {config.get('path', 'Unknown')}
                Function: {config.get('function', 'Unknown')}
                Fallback Path: {config.get('fallback_path', 'None')}
                Fallback Function: {config.get('fallback_function', 'None')}
                """)
        
        return error_function
    
    def render_module(self, module_name: str):
        """Render a specific module with loading state"""
        if module_name not in self.modules:
            st.error(f"Module '{module_name}' not found")
            return
        
        # Show loading state
        with st.spinner(f"Loading {module_name}..."):
            try:
                # Execute the module function
                self.modules[module_name]()
            except Exception as e:
                st.error(f"Error rendering {module_name}: {str(e)}")
                with st.expander("Error Details"):
                    st.exception(e)
    
    def get_modules_by_category(self, category: str) -> Dict[str, dict]:
        """Get all modules in a specific category"""
        return {
            name: config for name, config in self.module_mapping.items()
            if config.get("category") == category
        }
    
    def get_all_categories(self) -> list:
        """Get all available module categories"""
        categories = set()
        for config in self.module_mapping.values():
            categories.add(config.get("category", "unknown"))
        return sorted(list(categories))
    
    def is_module_available(self, module_name: str) -> bool:
        """Check if a module is available and functional"""
        return module_name in self.modules and self.modules[module_name] is not None