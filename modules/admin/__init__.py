"""
Admin Module for gcPanel

This module provides administrative functionality that is only accessible to admin users.
It includes:
- Feature Showcase
- Digital Signatures
- Standardized CRUD Styling Demo
"""

import streamlit as st
from modules.features_showcase import render_features_showcase
from modules.digital_signatures import render_digital_signatures
from modules.crud_demo import render_crud_demo

def check_admin_access():
    """Check if the current user has admin access."""
    # In a production environment, this would check against user roles in a database
    # For this demo, we'll just use a session state variable
    if 'user_role' not in st.session_state:
        st.session_state.user_role = 'admin'  # Default to admin for demo purposes
    
    return st.session_state.user_role == 'admin'

def render():
    """Render the Admin module."""
    st.title("Admin Panel")
    
    # Check admin access
    if not check_admin_access():
        st.error("You do not have permission to access this section. Please contact your administrator.")
        return
    
    # Create tabs for different admin features
    tab1, tab2, tab3 = st.tabs(["Feature Showcase", "Digital Signatures", "CRUD Styling Demo"])
    
    with tab1:
        render_features_showcase()
    
    with tab2:
        render_digital_signatures()
    
    with tab3:
        render_crud_demo()