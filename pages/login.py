"""
Login page for gcPanel with clean interface.

This module provides a clean login page for Highland Tower Development.
"""

import streamlit as st
from login_form import render_login_form

def login_page():
    """Render the clean login page."""
    
    # Apply dark theme styles
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0a0e13 0%, #121721 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #0a0e13 0%, #121721 100%);
    }
    
    /* Hide default elements */
    header {display: none !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    
    /* Full width layout */
    .appview-container .main .block-container {
        max-width: 100% !important;
        padding: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Clean Highland Tower Development header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="font-size: 2.2rem; margin: 0; color: #ffffff;">
            🏗️ gcPanel - Highland Tower Development
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Render the clean login form
    render_login_form()