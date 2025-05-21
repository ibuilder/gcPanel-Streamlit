"""
Shared State Manager for gcPanel

This module provides centralized management of application-wide state
to ensure consistent behavior across modular components.
"""

import streamlit as st

def initialize_base_session_state():
    """
    Initialize core application session state that's shared across all modules.
    """
    base_state = {
        "current_module": "dashboard",    # Default module ID to display
        "is_mobile_view": False,          # Mobile view toggle
        "show_notification_center": False, # Notification center toggle
        "theme": "light",                 # Theme (light/dark) setting
        "user": {                         # User information
            "name": "Admin User",
            "role": "admin",
            "email": "admin@example.com",
            "authenticated": True
        },
        "project": {                      # Current project information
            "name": "Highland Tower Development",
            "id": "HTD-2025",
            "value": 45500000.00,
            "location": "101 Main Street, Metropolis",
            "start_date": "2025-01-15",
            "completion_date": "2027-07-01"
        }
    }
    
    # Only set values that aren't already in session state
    for key, value in base_state.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_project_info():
    """
    Get the current project information.
    
    Returns:
        dict: Current project information
    """
    if "project" not in st.session_state:
        initialize_base_session_state()
    
    return st.session_state.project

def get_user_info():
    """
    Get the current user information.
    
    Returns:
        dict: Current user information
    """
    if "user" not in st.session_state:
        initialize_base_session_state()
    
    return st.session_state.user

def is_user_authenticated():
    """
    Check if the current user is authenticated.
    
    Returns:
        bool: True if authenticated, False otherwise
    """
    user_info = get_user_info()
    return user_info.get("authenticated", False)

def require_authentication(callback=None):
    """
    Require user authentication to proceed.
    
    Args:
        callback: Optional function to call if authentication fails
        
    Returns:
        bool: True if user is authenticated, False otherwise
    """
    if not is_user_authenticated():
        if callback:
            callback()
        return False
    return True