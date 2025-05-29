"""
Style manager utility for gcPanel.

This module provides functions to load CSS styles and other resources
for the gcPanel application.
"""

import streamlit as st
import os

def load_css(css_file_name):
    """
    Load CSS from a file in the static/css directory.
    
    Args:
        css_file_name: Name of the CSS file to load
    """
    # Check if the file exists
    css_path = f"static/css/{css_file_name}"
    if not os.path.exists(css_path):
        st.warning(f"CSS file not found: {css_path}")
        return
    
    # Read the CSS file
    with open(css_path, "r") as f:
        css = f.read()
    
    # Inject the CSS
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def load_js(js_file_name):
    """
    Load JavaScript from a file in the static/js directory.
    
    Args:
        js_file_name: Name of the JavaScript file to load
    """
    # Check if the file exists
    js_path = f"static/js/{js_file_name}"
    if not os.path.exists(js_path):
        st.warning(f"JavaScript file not found: {js_path}")
        return
    
    # Read the JavaScript file
    with open(js_path, "r") as f:
        js = f.read()
    
    # Inject the JavaScript
    st.markdown(f"<script>{js}</script>", unsafe_allow_html=True)