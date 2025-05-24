"""
Base Module Interface for Highland Tower Development Dashboard

This module provides a standardized interface that all modules must implement
to ensure consistency across the application.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import streamlit as st
from datetime import datetime

class BaseModule(ABC):
    """
    Base class for all Highland Tower Development modules.
    
    This ensures all modules have consistent structure and functionality.
    """
    
    def __init__(self, module_name: str, module_icon: str):
        self.module_name = module_name
        self.module_icon = module_icon
        self.module_id = module_name.lower().replace(" ", "_")
        
    @abstractmethod
    def render(self) -> None:
        """Main render method for the module."""
        pass
    
    @abstractmethod
    def get_module_config(self) -> Dict[str, Any]:
        """Return module configuration."""
        pass
    
    def render_header(self, title: Optional[str] = None) -> None:
        """Render standardized module header."""
        display_title = title if title is not None else f"{self.module_icon} {self.module_name}"
        st.title(display_title)
        
    def render_metrics(self, metrics: List[Dict[str, Any]]) -> None:
        """Render standardized metrics row."""
        if not metrics:
            return
            
        cols = st.columns(len(metrics))
        for i, metric in enumerate(metrics):
            with cols[i]:
                st.metric(
                    metric["label"],
                    metric["value"],
                    metric.get("delta", None)
                )
    
    def render_quick_actions(self, actions: List[Dict[str, Any]]) -> None:
        """Render standardized quick action buttons."""
        if not actions:
            return
            
        st.markdown("#### Quick Actions")
        cols = st.columns(len(actions))
        
        for i, action in enumerate(actions):
            with cols[i]:
                if st.button(
                    action["label"],
                    type=action.get("type", "secondary"),
                    use_container_width=True,
                    key=f"{self.module_id}_{action['key']}"
                ):
                    if action.get("callback"):
                        action["callback"]()
                    else:
                        st.success(action.get("message", "Action completed!"))
    
    def render_data_table(self, data: List[Dict[str, Any]], columns: List[str]) -> None:
        """Render standardized data table."""
        if not data:
            st.info(f"No {self.module_name.lower()} data available.")
            return
            
        for item in data:
            with st.container():
                st.markdown("---")
                self._render_data_item(item, columns)
    
    def _render_data_item(self, item: Dict[str, Any], columns: List[str]) -> None:
        """Render individual data item."""
        cols = st.columns(len(columns))
        
        for i, column in enumerate(columns):
            with cols[i]:
                if column in item:
                    value = item[column]
                    if isinstance(value, str) and len(value) > 50:
                        st.markdown(f"**{column}**: {value[:50]}...")
                    else:
                        st.markdown(f"**{column}**: {value}")
    
    def log_action(self, action: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Log user actions for audit trail."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "module": self.module_name,
            "action": action,
            "user": st.session_state.get("current_user", {}).get("name", "Unknown"),
            "details": details if details is not None else {}
        }
        
        # Store in session state for now (will be moved to database)
        if "audit_log" not in st.session_state:
            st.session_state.audit_log = []
        st.session_state.audit_log.append(log_entry)
    
    def get_search_data(self) -> List[Dict[str, Any]]:
        """Return searchable data for global search functionality."""
        return []
    
    def handle_bulk_operations(self, operation: str, items: List[str]) -> bool:
        """Handle bulk operations on multiple items."""
        return False
    
    def get_notifications(self) -> List[Dict[str, Any]]:
        """Get module-specific notifications."""
        return []