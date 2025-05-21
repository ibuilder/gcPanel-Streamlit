"""
Container styling improvements for gcPanel.

This module provides consistent spacing and padding for content containers
across the application to ensure proper readability and visual hierarchy.
"""

import streamlit as st

def apply_container_styles():
    """
    Apply improved container styles with better spacing.
    
    This addresses the issue of text being too close to container edges
    and provides consistent padding across the application.
    """
    # Apply global container styles with better padding and spacing
    st.markdown("""
    <style>
    /* Improve spacing for text and content */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
    
    /* Add proper padding to containers */
    div.stMarkdown {
        padding: 0.5rem 0.75rem;
    }
    
    /* More balanced container padding */
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 1rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Improve header spacing */
    .stApp header {
        margin-top: 0;
        padding-top: 0.5rem;
    }
    
    /* Restore proper spacing in Streamlit containers */
    .stApp {
        margin-top: 0;
        padding-top: 0.5rem;
    }
    
    /* Ensure consistent sidebar spacing */
    section[data-testid="stSidebar"] {
        padding-top: 1rem !important;
    }
    
    /* Card-style containers with proper padding */
    .content-card {
        background: white;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        border: 1px solid rgba(49, 51, 63, 0.1);
    }
    
    /* Data container with better spacing */
    .data-container {
        padding: 1.25rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        border: 1px solid rgba(49, 51, 63, 0.1);
        background: #f8f9fa;
    }
    
    /* Section headers with proper spacing */
    .section-header {
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(49, 51, 63, 0.1);
        font-weight: 600;
    }
    
    /* Adjust spacing for DataFrames */
    .dataframe-container .stDataFrame {
        padding: 1rem;
    }
    
    /* Fix for tight spacing in tables */
    .stTable {
        padding: 0.5rem;
    }
    
    /* Better button spacing */
    .stButton > button {
        margin: 0.5rem 0;
    }
    
    /* Input fields with better padding */
    .stTextInput > div > div {
        padding: 0.25rem 0.75rem;
    }
    
    /* Select boxes with more padding */
    .stSelectbox > div > div {
        padding: 0.25rem 0;
    }
    
    /* Better layout for forms */
    form div.stButton > button {
        margin-top: 1.5rem;
    }
    
    /* Header elements with better margins */
    h1, h2, h3, h4, h5 {
        margin-top: 1rem;
        margin-bottom: 0.75rem;
        font-weight: 600;
    }
    
    /* Improve readability of paragraphs */
    p {
        margin-bottom: 0.75rem;
        line-height: 1.6;
    }
    
    /* List items with better spacing */
    li {
        margin-bottom: 0.25rem;
    }
    </style>
    """, unsafe_allow_html=True)

def card_container(title=None):
    """
    Create a card-style container with proper spacing and padding.
    
    Args:
        title (str, optional): Title for the card container
    """
    if title:
        st.markdown(f"<h3 class='section-header'>{title}</h3>", unsafe_allow_html=True)
    
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    # Return the container for content to be placed inside
    container = st.container()
    st.markdown("</div>", unsafe_allow_html=True)
    
    return container

def data_container(title=None):
    """
    Create a data display container with proper spacing.
    
    Args:
        title (str, optional): Title for the data container
    """
    if title:
        st.markdown(f"<h4>{title}</h4>", unsafe_allow_html=True)
    
    st.markdown("<div class='data-container'>", unsafe_allow_html=True)
    # Return the container for data to be placed inside
    container = st.container()
    st.markdown("</div>", unsafe_allow_html=True)
    
    return container

def section_header(title):
    """
    Create a section header with proper spacing and styling.
    
    Args:
        title (str): Title for the section
    """
    st.markdown(f"<h3 class='section-header'>{title}</h3>", unsafe_allow_html=True)