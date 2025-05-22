"""
Engineering Module for gcPanel

This module provides engineering management functionality for the construction management dashboard,
with a focus on Submittal Packages and Transmittals using the standardized CRUD styling.
"""

import streamlit as st
from modules.engineering.submittal_packages import render as render_submittal_packages
from modules.engineering.transmittals import render as render_transmittals

def render():
    """Render the Engineering module."""
    st.title("Engineering")
    
    # Create tabs for different engineering functions
    tab1, tab2 = st.tabs(["Submittal Packages", "Transmittals"])
    
    # Submittal Packages Tab
    with tab1:
        render_submittal_packages()
    
    # Transmittals Tab
    with tab2:
        render_transmittals()