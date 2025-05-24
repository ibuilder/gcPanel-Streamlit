"""
Login page for gcPanel with clean interface.

This module provides a clean login page for Highland Tower Development.
"""

import streamlit as st
from login_form import render_login_form

def login_page():
    """Render the clean login page."""
    
    # Apply clean dark theme and remove ALL extra containers
    st.markdown("""
    <style>
    /* Remove ALL unnecessary containers and elements */
    .main .block-container {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e13 0%, #121721 100%);
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Hide ALL default Streamlit elements */
    header {display: none !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    .css-1rs6os {display: none !important;}
    .css-17ziqus {display: none !important;}
    
    /* Remove extra spacing and containers */
    .element-container {margin: 0 !important; padding: 0 !important;}
    .stMarkdown {margin: 0 !important;}
    
    /* Clean full width layout */
    .appview-container .main .block-container {
        max-width: 100% !important;
        padding: 1rem !important;
        margin: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Simple clean header
    st.markdown("# 🏗️ gcPanel - Highland Tower Development", unsafe_allow_html=True)
    
    # Render the clean login form
    render_login_form()