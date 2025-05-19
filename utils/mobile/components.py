"""
Mobile-optimized UI components for gcPanel.

This module provides reusable mobile-friendly UI components
that are designed for optimal display on smaller screens.
"""

import streamlit as st

def load_mobile_styles():
    """Load custom CSS styles for mobile UI components."""
    with open("static/mobile/mobile_styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def mobile_card(icon, title, on_click_key=None):
    """
    Create a mobile-friendly card with an icon and title.
    
    Args:
        icon (str): Emoji or icon to display
        title (str): Card title
        on_click_key (str): Key for the hidden button that handles clicks
        
    Returns:
        bool: True if the card was clicked, False otherwise
    """
    # Create a container for the card
    container = st.container()
    
    # Add the card HTML with proper CSS classes
    with container:
        st.markdown(f"""
        <div class="mobile-card" onclick="document.getElementById('{on_click_key}').click()">
            <div class="mobile-card-icon">{icon}</div>
            <div class="mobile-card-title">{title}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Hidden button for handling clicks
        clicked = st.button(title, key=on_click_key)
    
    return clicked

def mobile_list_item(title, subtitle=None, icon=None, on_click_key=None):
    """
    Create a mobile-friendly list item.
    
    Args:
        title (str): Main title text
        subtitle (str, optional): Subtitle or description text
        icon (str, optional): Emoji or icon to show
        on_click_key (str, optional): Key for the click handler
        
    Returns:
        bool: True if the item was clicked, False otherwise
    """
    # Create a container for the list item
    container = st.container()
    
    # Add the list item HTML with proper CSS classes
    with container:
        subtitle_html = f'<div class="mobile-list-subtitle">{subtitle}</div>' if subtitle else ''
        icon_html = f'<div class="mobile-list-icon">{icon}</div>' if icon else ''
        
        st.markdown(f"""
        <div class="mobile-list-item" onclick="document.getElementById('{on_click_key}').click()">
            {icon_html}
            <div class="mobile-list-content">
                <div class="mobile-list-title">{title}</div>
                {subtitle_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Hidden button for handling clicks
        clicked = st.button(f"Select {title}", key=on_click_key)
    
    return clicked

def mobile_section(title, content_func):
    """
    Create a mobile-friendly section with a title and content.
    
    Args:
        title (str): Section title
        content_func (callable): Function that renders the section content
    """
    st.markdown(f'<div class="mobile-section-title">{title}</div>', unsafe_allow_html=True)
    content_func()