"""
Centralized Project Configuration for gcPanel
Manages project information that updates across the entire platform
"""

import streamlit as st
from typing import Dict, Any
import json
import os

class ProjectConfig:
    """Centralized project configuration management"""
    
    def __init__(self):
        self.config_file = "lib/config/project_settings.json"
        self._load_config()
    
    def _load_config(self):
        """Load project configuration from file or set defaults"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self._set_default_config()
        except Exception:
            self._set_default_config()
    
    def _set_default_config(self):
        """Set default project configuration with Matthew M. Emma as project manager"""
        self.config = {
            "project_name": "Highland Tower Development",
            "project_manager": "Matthew M. Emma",
            "project_value": "$45.5M",
            "project_type": "Mixed-Use Development",
            "project_location": "Downtown Core",
            "project_start_date": "2024-01-15",
            "project_end_date": "2025-12-31",
            "company_name": "gcPanel Construction Management",
            "project_description": "45-story mixed-use tower with retail, office, and residential units",
            "client_name": "Highland Development Group",
            "architect": "Thompson & Associates",
            "general_contractor": "Elite Construction Corp",
            "project_progress": 78.5,
            "spi": 1.05,
            "projected_savings": "$700K"
        }
        self._save_config()
    
    def _save_config(self):
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            st.error(f"Error saving project configuration: {e}")
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value and save"""
        self.config[key] = value
        self._save_config()
        # Update session state to trigger rerun
        if f"config_{key}" in st.session_state:
            st.session_state[f"config_{key}"] = value
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values"""
        return self.config.copy()
    
    def update_multiple(self, updates: Dict[str, Any]):
        """Update multiple configuration values"""
        self.config.update(updates)
        self._save_config()
        # Update session state
        for key, value in updates.items():
            if f"config_{key}" in st.session_state:
                st.session_state[f"config_{key}"] = value
    
    def get_project_header(self) -> str:
        """Get formatted project header for pages"""
        return f"{self.get('project_name')} - {self.get('project_type')}"
    
    def get_project_subtitle(self, module_name: str) -> str:
        """Get formatted project subtitle for specific modules"""
        manager = self.get('project_manager')
        value = self.get('project_value')
        return f"Project Manager: {manager} | Value: {value} | {module_name}"

# Global instance
project_config = ProjectConfig()

def get_project_config():
    """Get the global project configuration instance"""
    return project_config