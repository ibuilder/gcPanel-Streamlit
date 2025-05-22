"""
Simple breadcrumbs component for gcPanel.

This module provides a simplified breadcrumb navigation component.
"""

import streamlit as st
from app_config import MENU_MAP

def simple_breadcrumbs(current_page, previous_pages=None):
    """
    Display simple breadcrumb navigation component.
    
    Args:
        current_page (str): Current page name
        previous_pages (list, optional): List of previous pages in the navigation hierarchy
    """
    # Create the breadcrumb HTML
    breadcrumb_html = """
    <div class="breadcrumb-container">
        <div class="breadcrumbs">
    """
    
    # Add Home link
    breadcrumb_html += """<span class="breadcrumb-item"><a href="javascript:void(0);" onclick="homeClick()">Home</a></span>"""
    
    # If current_page is not Dashboard or Home, add it with separator
    if current_page != "Dashboard" and current_page != "Home" and current_page != "📊 Dashboard":
        breadcrumb_html += f"""<span class="breadcrumb-separator">›</span>
        <span class="breadcrumb-item breadcrumb-active">{current_page}</span>"""
    
    # Close breadcrumb container
    breadcrumb_html += """
        </div>
    </div>
    """
    
    # Add JavaScript for Home button
    breadcrumb_html += """
    <script>
    function homeClick() {
        window.parent.postMessage({
            type: "streamlit:setComponentValue",
            value: {"current_menu": "Dashboard"}
        }, "*");
    }
    </script>
    """
    
    # Add CSS for breadcrumbs
    breadcrumb_html += """
    <style>
    .breadcrumb-container {
        margin-bottom: 1rem;
    }
    .breadcrumbs {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        padding: 0.5rem 0;
    }
    .breadcrumb-item {
        font-size: 0.9rem;
    }
    .breadcrumb-item a {
        color: #4b5563;
        text-decoration: none;
    }
    .breadcrumb-item a:hover {
        color: #1a1a1a;
        text-decoration: underline;
    }
    .breadcrumb-separator {
        margin: 0 0.5rem;
        color: #9ca3af;
    }
    .breadcrumb-active {
        color: #1a1a1a;
        font-weight: 600;
    }
    </style>
    """
    
    # Render breadcrumbs
    st.markdown(breadcrumb_html, unsafe_allow_html=True)

def get_breadcrumbs_for_page(page):
    """
    Get breadcrumb hierarchy for a specific page.
    
    Args:
        page (str): Page name
        
    Returns:
        list: The current page name only - no longer using hierarchies
    """
    # For Dashboard or Home, don't show any breadcrumbs
    if page == "Dashboard" or page == "Home":
        return []
    
    # For all other pages, just return the page name - no hierarchy
    return [page]