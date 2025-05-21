"""
Custom styles for the Safety module in gcPanel.

This module provides enhanced styling for the Safety Management module,
with improved header appearance and layout.
"""

import streamlit as st

def apply_safety_styles():
    """Apply custom styles to improve the Safety Management layout."""
    # First, load the dedicated CSS file for removing header buttons
    with open('assets/remove_header_buttons.css', 'r') as f:
        remove_buttons_css = f.read()
    
    st.markdown(f"<style>{remove_buttons_css}</style>", unsafe_allow_html=True)
    
    # Apply the regular safety styles
    st.markdown("""
    <style>
    /* Remove extra whitespace above headers */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Enhance header appearance */
    h1, h2, h3, h4, h5, h6 {
        margin-top: 0.2rem !important;
        margin-bottom: 1rem !important;
        font-weight: 600 !important;
        color: #1a73e8 !important;
    }
    
    h1 {
        font-size: 1.8rem !important;
        border-bottom: 1px solid rgba(49, 51, 63, 0.1);
        padding-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 1.5rem !important;
    }
    
    h3 {
        font-size: 1.3rem !important;
    }
    
    /* Improved container styling */
    div.stTabs [data-baseweb="tab-panel"] {
        padding-top: 0.5rem !important;
    }
    
    /* Remove button margin-bottom */
    button {
        margin-bottom: 0 !important;
    }
    
    /* Style action buttons container */
    .stButton button {
        font-size: 0.85rem !important;
        padding: 2px 10px !important;
    }
    
    /* Improved form styling */
    .stForm > div:first-child {
        border: none !important;
        padding: 0 !important;
    }
    
    /* Better table styling */
    div[data-testid="stDataFrame"] {
        margin-bottom: 1rem !important;
    }
    
    /* Remove bottom space under select boxes */
    div[data-baseweb="select"] {
        margin-bottom: 0 !important;
    }
    
    /* Remove bottom buttons or unnecessary elements below header */
    div.stHeader + div.stButton,
    div.stHeader + div.row-widget.stButton,
    div.stHeader + div div.stButton,
    div.stHeader ~ div.stButton,
    div.stMarkdown + div.stButton,
    /* Target specific button patterns that appear after headers */
    div.stHeader ~ div.row-widget.stButton,
    div.stHeader + div.element-container div.stButton {
        display: none !important;
    }
    
    /* Create professional card appearance for list items */
    .safety-card {
        background-color: white;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        transition: all 0.3s cubic-bezier(.25,.8,.25,1);
    }
    
    .safety-card:hover {
        box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
    }
    </style>
    """, unsafe_allow_html=True)