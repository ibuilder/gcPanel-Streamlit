"""
Resource loader utility for gcPanel.

This module provides functions for loading external resources such as
CSS, JavaScript, and HTML files.
"""

import streamlit as st
import os

def load_css_file(css_file_path):
    """
    Load and apply a CSS file.
    
    Args:
        css_file_path (str): Path to the CSS file
    """
    try:
        with open(css_file_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Could not find CSS file: {css_file_path}")

def load_multiple_css_files(css_files):
    """
    Load and apply multiple CSS files.
    
    Args:
        css_files (list): List of paths to CSS files
    """
    for css_file in css_files:
        load_css_file(css_file)

def load_js_file(js_file_path):
    """
    Load and execute a JavaScript file.
    
    Args:
        js_file_path (str): Path to the JavaScript file
    """
    try:
        with open(js_file_path, "r") as f:
            st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Could not find JavaScript file: {js_file_path}")

def load_html_file(html_file_path):
    """
    Load and render an HTML file.
    
    Args:
        html_file_path (str): Path to the HTML file
        
    Returns:
        str: The HTML content
    """
    try:
        with open(html_file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Could not find HTML file: {html_file_path}")
        return ""
        
def load_and_render_html(html_file_path):
    """
    Load and render an HTML file using st.markdown.
    
    Args:
        html_file_path (str): Path to the HTML file
    """
    html_content = load_html_file(html_file_path)
    if html_content:
        st.markdown(html_content, unsafe_allow_html=True)