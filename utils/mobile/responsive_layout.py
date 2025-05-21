"""
Responsive Layout Utils for gcPanel

This module provides utilities for making the application responsive and mobile-friendly.
"""

import streamlit as st
import base64
from pathlib import Path

def add_mobile_styles():
    """
    Add responsive mobile styles to improve the application on mobile devices.
    
    This includes adjustments for:
    - Touch targets (larger buttons, inputs)
    - Responsive layout adjustments
    - Better readability on small screens
    """
    # Mobile optimization CSS
    st.markdown("""
    <style>
        /* Base mobile optimizations */
        @media (max-width: 768px) {
            /* Make buttons and inputs larger for touch */
            button, input, select, textarea, .stButton button {
                min-height: 44px !important;
                font-size: 16px !important;
            }
            
            /* Improve readability on small screens */
            body, p, div {
                font-size: 16px !important;
            }
            
            h1 {
                font-size: 1.8rem !important;
            }
            
            h2 {
                font-size: 1.5rem !important;
            }
            
            h3 {
                font-size: 1.3rem !important;
            }
            
            /* Adjust column layout for mobile */
            div.row-widget.stHorizontal {
                flex-direction: column;
            }
            
            /* Make sure tables don't overflow */
            table {
                display: block;
                overflow-x: auto;
                white-space: nowrap;
            }
            
            /* Adjust sidebar for mobile */
            section[data-testid="stSidebar"] {
                width: 100% !important;
                min-width: 100% !important;
                max-width: 100% !important;
            }
            
            /* Improve cards on mobile */
            .card {
                margin: 0.5rem 0 !important;
                padding: 0.8rem !important;
            }
            
            /* Better spacing for form elements */
            .element-container {
                margin-bottom: 1rem !important;
            }
            
            /* Make notification content scrollable on small screens */
            .notification-content {
                max-height: 60vh;
                overflow-y: auto;
            }
        }
        
        /* Add viewport meta tag for proper mobile rendering */
        @media screen {
            body:before {
                content: '';
                display: block;
            }
        }
        
        /* Handle notches on iPhone X and newer */
        @supports (padding: max(0px)) {
            .main .block-container {
                padding-left: max(1rem, env(safe-area-inset-left));
                padding-right: max(1rem, env(safe-area-inset-right));
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Add viewport meta tag
    st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    """, unsafe_allow_html=True)
    
def create_responsive_card(title, content, icon=None, status=None, footer=None, on_click=None):
    """
    Create a responsive card component that works well on mobile and desktop.
    
    Args:
        title (str): Card title
        content (str): Card content text
        icon (str, optional): Icon name or path to icon image
        status (str, optional): Status text to show (e.g. "Complete", "In Progress")
        footer (str, optional): Footer text or HTML
        on_click (callable, optional): Function to call when card is clicked
        
    Returns:
        bool: True if card was clicked
    """
    # Generate a unique key for this card
    card_id = f"card_{hash(title + content)}"
    
    # Determine status color
    status_color = "#2196F3"  # Default blue
    if status:
        status = status.lower()
        if status in ["complete", "completed", "done", "approved"]:
            status_color = "#4CAF50"  # Green
        elif status in ["pending", "in progress", "reviewing"]:
            status_color = "#FF9800"  # Orange
        elif status in ["overdue", "late", "failed", "rejected"]:
            status_color = "#F44336"  # Red
    
    # Create card HTML
    card_html = f"""
    <div class="mobile-card" id="{card_id}" 
         style="background-color: white; border-radius: 8px; padding: 16px; 
                margin-bottom: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                border: 1px solid #e0e0e0; cursor: pointer;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <h3 style="margin: 0; font-size: 18px; color: #333;">{title}</h3>
            {f'<div style="background-color: {status_color}33; color: {status_color}; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">{status}</div>' if status else ''}
        </div>
        <p style="margin: 8px 0; color: #666; font-size: 14px;">{content}</p>
        {f'<div style="border-top: 1px solid #eee; margin-top: 12px; padding-top: 12px; font-size: 12px; color: #888;">{footer}</div>' if footer else ''}
    </div>
    
    <script>
        document.getElementById("{card_id}").addEventListener("click", function() {{
            // Send a message to Streamlit to trigger the Python callback
            window.parent.postMessage({{
                type: "streamlit:setComponentValue",
                value: "{card_id}",
            }}, "*");
        }});
    </script>
    """
    
    # Render the card
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Handle click event (this is a simplified approach without actual components)
    clicked = st.session_state.get(card_id, False)
    if clicked and on_click:
        on_click()
    
    return clicked

def create_mobile_list_item(title, subtitle=None, icon=None, trailing_icon=None, on_click=None):
    """
    Create a mobile-friendly list item component.
    
    Args:
        title (str): Primary text
        subtitle (str, optional): Secondary text shown below title
        icon (str, optional): Leading icon name or path
        trailing_icon (str, optional): Trailing icon name or path
        on_click (callable, optional): Function to call when item is clicked
        
    Returns:
        bool: True if item was clicked
    """
    item_id = f"item_{hash(title + (subtitle or ''))}"
    
    item_html = f"""
    <div class="mobile-list-item" id="{item_id}" 
         style="display: flex; padding: 12px 16px; border-bottom: 1px solid #eee; 
                align-items: center; cursor: pointer; background-color: white;">
        {f'<div style="margin-right: 16px; width: 24px; height: 24px;">{icon}</div>' if icon else ''}
        <div style="flex: 1; min-width: 0;">
            <div style="font-size: 16px; color: #333; margin-bottom: 2px;">{title}</div>
            {f'<div style="font-size: 14px; color: #666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{subtitle}</div>' if subtitle else ''}
        </div>
        {f'<div style="margin-left: 16px;">{trailing_icon}</div>' if trailing_icon else ''}
    </div>
    
    <script>
        document.getElementById("{item_id}").addEventListener("click", function() {{
            window.parent.postMessage({{
                type: "streamlit:setComponentValue",
                value: "{item_id}",
            }}, "*");
        }});
    </script>
    """
    
    st.markdown(item_html, unsafe_allow_html=True)
    
    clicked = st.session_state.get(item_id, False)
    if clicked and on_click:
        on_click()
    
    return clicked

def create_mobile_tab_layout(tabs, content_funcs):
    """
    Create a mobile-friendly tab layout.
    
    Args:
        tabs (list): List of tab titles
        content_funcs (list): List of functions to render content for each tab
    """
    if 'mobile_active_tab' not in st.session_state:
        st.session_state.mobile_active_tab = 0
    
    # Create tabs HTML
    tabs_html = '<div style="display: flex; overflow-x: auto; margin-bottom: 16px; background-color: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">'
    
    for i, tab in enumerate(tabs):
        active_class = "active" if i == st.session_state.mobile_active_tab else ""
        tabs_html += f"""
        <div class="mobile-tab {active_class}" 
             style="padding: 12px 16px; text-align: center; flex: 1; 
                    min-width: fit-content; cursor: pointer;
                    color: {'#1976D2' if i == st.session_state.mobile_active_tab else '#666'};
                    border-bottom: {f'2px solid #1976D2' if i == st.session_state.mobile_active_tab else '2px solid transparent'};"
             onclick="document.getElementById('mobile_tab_{i}').click();">
            {tab}
        </div>
        """
    
    tabs_html += '</div>'
    
    # Render tabs
    st.markdown(tabs_html, unsafe_allow_html=True)
    
    # Create invisible buttons for tab selection
    cols = st.columns(len(tabs))
    for i, col in enumerate(cols):
        with col:
            if st.button("", key=f"mobile_tab_{i}", help=f"Switch to {tabs[i]} tab"):
                st.session_state.mobile_active_tab = i
                st.rerun()
    
    # Render active tab content
    if 0 <= st.session_state.mobile_active_tab < len(content_funcs):
        content_funcs[st.session_state.mobile_active_tab]()