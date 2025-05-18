"""
UI Manager for gcPanel.

This module provides utility functions for managing UI components,
loading resources, and handling themes.
"""

import streamlit as st
import os

def load_css_file(file_path):
    """
    Load a CSS file and apply it to the Streamlit app.
    
    Args:
        file_path (str): Path to the CSS file
    """
    try:
        with open(file_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading CSS file {file_path}: {e}")

def load_external_resources():
    """
    Load all external resources needed for the application.
    
    This includes CSS, JavaScript, fonts, and other resources.
    """
    # Load CSS files
    css_files = [
        "static/css/main.css", 
        "static/css/notifications.css",
        "static/css/enhanced-theme.css",
        "static/css/optimized-ui.css",
        "static/css/console-fix.css",
        "static/css/buttons-fix.css",
        "static/css/action-buttons.css",
        "static/css/action-bar.css",
        "static/css/notification_styles.css",
        "static/css/clean-header.css"
    ]
    
    for css_file in css_files:
        load_css_file(css_file)
    
    # Load Material Icons
    st.markdown(
        '<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">',
        unsafe_allow_html=True
    )
    
    # Load JavaScript
    try:
        with open("static/js/notification_handler.js", "r") as f:
            st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading JavaScript: {e}")

def load_html_component(file_path):
    """
    Load an HTML component from a file.
    
    Args:
        file_path (str): Path to the HTML file
        
    Returns:
        str: The HTML content as a string
    """
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        st.error(f"Error loading HTML component {file_path}: {e}")
        return ""

def render_notification_button():
    """Render the notification button component."""
    html_content = load_html_component("static/html/notification_button.html")
    st.markdown(html_content, unsafe_allow_html=True)
    
    # Use a hidden button that will be triggered by JavaScript
    return st.button("Notifications", key="show_notifications_btn")

def set_page_config():
    """Set page configuration for the Streamlit app."""
    st.set_page_config(
        page_title="gcPanel Construction Dashboard",
        page_icon="gcpanel.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )