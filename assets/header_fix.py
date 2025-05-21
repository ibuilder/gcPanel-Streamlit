"""
Header fixes for gcPanel.

This module applies CSS fixes to remove the white header box and improve the header styling.
"""

import streamlit as st

def apply_header_fixes():
    """Apply CSS fixes to improve header appearance and remove white box."""
    
    # Hide the default Streamlit header
    st.markdown("""
    <style>
    /* Hide default Streamlit header and footer */
    .stApp > header {
        display: none !important;
    }
    
    /* Fix top margin */
    .main .block-container {
        padding-top: 1rem;
    }
    
    /* Header container styling */
    .gc-header-container {
        margin-top: 0;
        padding: 0.5rem 1rem;
        background-color: #f8f9fa;
        border-bottom: 1px solid #e9ecef;
    }
    
    /* Fix navigation dropdown styling */
    .stSelectbox {
        margin-bottom: 0;
    }
    
    /* Project title styling */
    .gc-project-title {
        font-size: 1.25rem;
        font-weight: bold;
        margin: 0;
        color: #1a1a1a;
    }
    
    /* Project details styling */
    .gc-project-details {
        font-size: 0.85rem;
        color: #4b5563;
        margin: 0;
    }
    
    /* Logo styling */
    .gc-logo {
        display: flex;
        align-items: center;
    }
    
    /* Navigation title styling */
    .gc-nav-title {
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #4b5563;
    }
    </style>
    """, unsafe_allow_html=True)