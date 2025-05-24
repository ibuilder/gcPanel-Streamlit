"""
Login page for gcPanel with clean interface.

This module provides a clean login page for Highland Tower Development.
"""

import streamlit as st
from login_form import render_login_form

def login_page():
    """Render the clean login page."""
    
    # Apply aggressive container removal for completely clean interface
    st.markdown("""
    <style>
    /* ELIMINATE ALL Streamlit default containers */
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e13 0%, #121721 100%);
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Remove EVERY default Streamlit element */
    header {display: none !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    
    /* Target specific container classes that create extra divs */
    .css-1rs6os {display: none !important;}
    .css-17ziqus {display: none !important;}
    .css-12oz5g7 {display: none !important;}
    .css-1y4p8pa {display: none !important;}
    .css-91z34k {display: none !important;}
    .css-1wrcr25 {display: none !important;}
    .css-ue6h4q {display: none !important;}
    .css-18e3th9 {display: none !important;}
    .css-1d391kg {display: none !important;}
    .css-k1vhr4 {display: none !important;}
    .css-1avcm0n {display: none !important;}
    
    /* Remove element containers and spacing */
    .element-container {
        margin: 0 !important; 
        padding: 0 !important;
        border: none !important;
    }
    
    .stMarkdown {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Force minimal spacing */
    .block-container > div {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    div[data-testid="element-container"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Clean layout */
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