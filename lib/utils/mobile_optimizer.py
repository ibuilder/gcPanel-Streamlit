"""
Mobile Optimization Manager for Highland Tower Development

Provides responsive design and mobile-specific features for field teams.
"""

import streamlit as st
from typing import Dict, Any
import logging

class MobileOptimizer:
    """Manages mobile optimization and responsive design for field operations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def detect_device_type(self) -> str:
        """Detect device type for optimal layout."""
        # In production, this would use actual device detection
        return st.session_state.get("device_type", "desktop")
    
    def apply_mobile_styles(self):
        """Apply mobile-optimized CSS styles."""
        mobile_css = """
        <style>
        /* Mobile-first responsive design */
        @media (max-width: 768px) {
            .stApp > div:first-child {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
            
            /* Larger touch targets for field use */
            .stButton > button {
                min-height: 48px !important;
                font-size: 16px !important;
            }
            
            /* Better form spacing on mobile */
            .stSelectbox, .stTextInput, .stTextArea {
                margin-bottom: 1rem !important;
            }
            
            /* Mobile-friendly metrics */
            [data-testid="metric-container"] {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 12px;
                padding: 1rem;
                margin: 0.5rem 0;
            }
            
            /* Compact tables for mobile */
            .mobile-compact-table {
                font-size: 14px;
                overflow-x: auto;
            }
        }
        
        /* Enhanced touch targets */
        .mobile-action-btn {
            padding: 12px 20px;
            border-radius: 8px;
            margin: 5px;
            min-width: 120px;
        }
        
        /* Field-friendly colors (high contrast) */
        .field-priority-high {
            background-color: #ff4444 !important;
            color: white !important;
        }
        
        .field-priority-medium {
            background-color: #ffaa00 !important;
            color: white !important;
        }
        
        .field-priority-low {
            background-color: #00aa44 !important;
            color: white !important;
        }
        </style>
        """
        
        st.markdown(mobile_css, unsafe_allow_html=True)
    
    def render_mobile_navigation(self, current_module: str):
        """Render mobile-optimized navigation."""
        if self.detect_device_type() == "mobile":
            st.markdown("#### 🏗️ Highland Tower - Quick Access")
            
            # Essential modules for field teams
            mobile_modules = [
                {"name": "Daily Reports", "icon": "📝", "key": "daily_reports"},
                {"name": "RFIs", "icon": "❓", "key": "rfis"},
                {"name": "Safety", "icon": "⚠️", "key": "safety"},
                {"name": "Field Operations", "icon": "🚧", "key": "field_ops"}
            ]
            
            cols = st.columns(2)
            for i, module in enumerate(mobile_modules):
                with cols[i % 2]:
                    if st.button(
                        f"{module['icon']} {module['name']}", 
                        key=f"mobile_nav_{module['key']}",
                        use_container_width=True,
                        type="primary" if current_module == module['name'] else "secondary"
                    ):
                        st.session_state.current_module = module['name']
                        st.rerun()
    
    def create_mobile_widget(self, widget_type: str, **kwargs) -> Any:
        """Create mobile-optimized widgets."""
        if widget_type == "quick_metric":
            return self._create_mobile_metric(**kwargs)
        elif widget_type == "action_card":
            return self._create_mobile_action_card(**kwargs)
        elif widget_type == "status_badge":
            return self._create_mobile_status_badge(**kwargs)
    
    def _create_mobile_metric(self, title: str, value: str, delta: str = None, color: str = "blue"):
        """Create mobile-friendly metric display."""
        delta_html = f"<small style='color: #888;'>{delta}</small>" if delta else ""
        
        metric_html = f"""
        <div style='background: linear-gradient(135deg, {color}40 0%, {color}20 100%); 
                    border-left: 4px solid {color}; 
                    padding: 1rem; 
                    border-radius: 8px; 
                    margin: 0.5rem 0;'>
            <h3 style='margin: 0; color: {color}; font-size: 1.5rem;'>{value}</h3>
            <p style='margin: 0.25rem 0 0 0; font-weight: 500;'>{title}</p>
            {delta_html}
        </div>
        """
        
        return st.markdown(metric_html, unsafe_allow_html=True)
    
    def _create_mobile_action_card(self, title: str, description: str, action_text: str, priority: str = "medium"):
        """Create mobile-optimized action card."""
        priority_class = f"field-priority-{priority}"
        
        card_html = f"""
        <div class='{priority_class}' style='padding: 1rem; border-radius: 12px; margin: 1rem 0;'>
            <h4 style='margin: 0 0 0.5rem 0;'>{title}</h4>
            <p style='margin: 0 0 1rem 0; opacity: 0.9;'>{description}</p>
            <button style='background: rgba(255,255,255,0.2); 
                          border: 1px solid rgba(255,255,255,0.5); 
                          color: white; 
                          padding: 8px 16px; 
                          border-radius: 6px;'>{action_text}</button>
        </div>
        """
        
        return st.markdown(card_html, unsafe_allow_html=True)
    
    def _create_mobile_status_badge(self, status: str, count: int = None):
        """Create mobile-friendly status badge."""
        status_colors = {
            "urgent": "#ff4444",
            "pending": "#ffaa00", 
            "complete": "#00aa44",
            "review": "#4444ff"
        }
        
        color = status_colors.get(status.lower(), "#888888")
        count_text = f" ({count})" if count is not None else ""
        
        badge_html = f"""
        <span style='background: {color}; 
                    color: white; 
                    padding: 4px 12px; 
                    border-radius: 20px; 
                    font-size: 0.9rem; 
                    font-weight: 500;'>{status.title()}{count_text}</span>
        """
        
        return st.markdown(badge_html, unsafe_allow_html=True)
    
    def enable_offline_mode(self):
        """Enable offline capabilities for field use."""
        if "offline_data" not in st.session_state:
            st.session_state.offline_data = {}
        
        # Cache critical data for offline access
        st.session_state.offline_data.update({
            "last_sync": "2025-05-24 10:20:00",
            "cached_reports": [],
            "pending_uploads": []
        })
    
    def get_field_shortcuts(self) -> Dict[str, str]:
        """Get field team keyboard shortcuts."""
        return {
            "Ctrl+N": "New Daily Report",
            "Ctrl+R": "New RFI", 
            "Ctrl+S": "New Safety Report",
            "Ctrl+F": "Search",
            "Ctrl+U": "Upload Photo"
        }