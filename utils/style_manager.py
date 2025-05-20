"""
Style Manager for gcPanel

Centralized CSS management for the application.
Allows loading CSS files from the static/css directory.
"""

import streamlit as st
import os

def load_css(css_filename):
    """
    Load CSS from static/css directory
    
    Args:
        css_filename: The name of the CSS file (e.g., "main.css")
    """
    css_path = os.path.join("static", "css", css_filename)
    
    # Check if file exists
    if not os.path.exists(css_path):
        print(f"Warning: CSS file not found: {css_path}")
        return
        
    # Read CSS file
    with open(css_path, "r") as f:
        css_content = f.read()
    
    # Inject CSS
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

def load_multiple_css(css_filenames):
    """
    Load multiple CSS files from static/css directory
    
    Args:
        css_filenames: List of CSS filenames to load
    """
    for filename in css_filenames:
        load_css(filename)