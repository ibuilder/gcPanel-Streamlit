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
    # Load CSS files - using consolidated CSS with fallback to individual files
    if os.path.exists("static/css/consolidated.css"):
        css_files = ["static/css/consolidated.css"]
    else:
        # Fallback to individual CSS files
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
            "static/css/clean-header.css",
            "static/css/header-components.css",
            "static/css/breadcrumbs.css",
            "static/css/notification-center.css",
            "static/css/space-fix.css",
            "static/css/debug-fix.css",
            "static/css/emotion-cache-fix.css"
        ]
    
    for css_file in css_files:
        load_css_file(css_file)
    
    # Load Material Icons
    st.markdown(
        '<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">',
        unsafe_allow_html=True
    )
    
    # Load JavaScript - using consolidated JS with fallback to individual files
    try:
        if os.path.exists("static/js/consolidated.js"):
            with open("static/js/consolidated.js", "r") as f:
                st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)
        else:
            # Fallback to individual JS files
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
    """Render the notification button component with icon only."""
    # Add a custom icon-only notification button via HTML
    html_content = """
    <div class="notification-btn-container">
        <button id="notificationBellBtn" class="notification-btn">
            <i class="material-icons">notifications</i>
            <div class="notification-badge">3</div>
        </button>
    </div>
    
    <style>
    /* Hide the standard button completely */
    button[kind="secondary"][data-testid="baseButton-secondary"] {
        display: none !important;
    }
    
    /* Style for the icon button */
    .notification-btn-container {
        display: flex;
        justify-content: flex-end;
    }
    
    .notification-btn {
        background: none;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        position: relative;
        padding: 8px;
        border-radius: 50%;
        transition: background-color 0.2s ease;
    }
    
    .notification-btn:hover {
        background-color: rgba(0, 0, 0, 0.05);
    }
    
    .notification-btn .material-icons {
        font-size: 24px;
        color: #3e79f7;
    }
    
    .notification-badge {
        position: absolute;
        top: 0;
        right: 0;
        background-color: #ff5b5b;
        color: white;
        border-radius: 50%;
        width: 16px;
        height: 16px;
        font-size: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
    </style>
    
    <script>
    // Set up click handler for notification button
    document.addEventListener('DOMContentLoaded', function() {
        const bellBtn = document.getElementById('notificationBellBtn');
        if (bellBtn) {
            bellBtn.addEventListener('click', function() {
                // Find the hidden button and click it
                const hiddenBtn = document.querySelector('button[kind="secondary"][data-testid="baseButton-secondary"]');
                if (hiddenBtn) hiddenBtn.click();
            });
        }
    });
    </script>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)
    
    # Keep the original button for functionality, but it will be hidden by CSS
    return st.button("", key="show_notifications_btn")

def set_page_config():
    """Set page configuration for the Streamlit app."""
    st.set_page_config(
        page_title="gcPanel Construction Dashboard",
        page_icon="gcpanel.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )