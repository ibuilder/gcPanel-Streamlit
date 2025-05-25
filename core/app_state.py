"""
Application State Management for gcPanel
Centralized session state handling with professional defaults
"""

import streamlit as st

class AppStateManager:
    """Manages application session state with enterprise defaults"""
    
    def __init__(self):
        self.default_state = {
            "authenticated": False,
            "username": "",
            "user_role": "user",
            "current_menu": "Dashboard",
            "project_name": "Highland Tower Development",
            "project_value": "$45.5M",
            "residential_units": 120,
            "retail_units": 8,
            "floors_above": 15,
            "floors_below": 2,
            "theme": "dark",
            "loading": False,
            "notifications": [],
            "last_activity": None
        }
    
    def initialize(self):
        """Initialize session state with default values"""
        for key, value in self.default_state.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user with enterprise credentials"""
        # Enterprise authentication logic
        valid_credentials = {
            "admin": "admin123",
            "manager": "manager123", 
            "user": "user123"
        }
        
        if username in valid_credentials and valid_credentials[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.user_role = username
            return True
        return False
    
    def logout(self):
        """Secure logout process"""
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.user_role = "user"
        st.session_state.current_menu = "Dashboard"
    
    def set_loading(self, is_loading: bool):
        """Control loading state"""
        st.session_state.loading = is_loading
    
    def add_notification(self, message: str, type: str = "info"):
        """Add notification to queue"""
        if "notifications" not in st.session_state:
            st.session_state.notifications = []
        
        st.session_state.notifications.append({
            "message": message,
            "type": type,
            "timestamp": st.session_state.get("last_activity")
        })
    
    def get_project_info(self) -> dict:
        """Get project information for display"""
        return {
            "name": st.session_state.project_name,
            "value": st.session_state.project_value,
            "residential_units": st.session_state.residential_units,
            "retail_units": st.session_state.retail_units,
            "floors_above": st.session_state.floors_above,
            "floors_below": st.session_state.floors_below
        }