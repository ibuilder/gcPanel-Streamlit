"""
Responsive layout utilities for mobile optimization.

This module provides utilities to create responsive layouts optimized for
mobile devices and smaller screens.
"""

import streamlit as st

def add_mobile_styles():
    """
    Add CSS styles for mobile optimization.
    
    This function injects CSS that makes the UI more mobile-friendly,
    with appropriate sizing, spacing, and touch targets.
    """
    mobile_styles = """
    <style>
        /* Base mobile responsive styles */
        @media (max-width: 768px) {
            /* Completely remove top spacing for mobile */
            .main .block-container {
                padding-top: 0 !important;
                margin-top: 0 !important;
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
            }
            
            /* Aggressively remove all space above header */
            header {
                display: none !important;
            }
            
            .stApp {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
            
            /* Fix header layout for mobile */
            div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
            }
            
            /* Mobile-optimized navigation */
            div[data-baseweb="select"] {
                margin-top: 0 !important;
                width: 100% !important;
            }
            
            /* Hide the "Navigation" label on mobile */
            div[data-baseweb="select"] > label {
                display: none !important;
            }
            
            /* Increase touch targets */
            .stButton > button {
                min-height: 44px !important;
                min-width: 44px !important;
            }
            
            /* Adjust heading sizes */
            h1 {
                font-size: 1.6rem !important;
            }
            
            h2 {
                font-size: 1.4rem !important;
            }
            
            h3 {
                font-size: 1.1rem !important;
            }
            
            /* Make inputs larger for touch */
            input, select, textarea {
                font-size: 16px !important; /* Prevents iOS zoom on focus */
            }
            
            /* Improve spacing in forms */
            div[data-testid="stForm"] {
                padding: 0.5rem !important;
            }
            
            /* Ensure tables can scroll horizontally */
            .stTable {
                overflow-x: auto !important;
            }
            
            /* Prevent images from overflowing */
            img {
                max-width: 100% !important;
                height: auto !important;
            }
            
            /* Compress project info on mobile */
            .project-info-text {
                font-size: 11px !important;
            }
        }
        
        /* Mobile card styles */
        .mobile-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .mobile-card:active {
            transform: scale(0.98);
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        
        .mobile-card-title {
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 5px;
        }
        
        .mobile-card-action {
            font-size: 0.9rem;
            color: #777;
            margin-bottom: 10px;
        }
        
        /* Mobile tabs styles */
        .mobile-tabs {
            display: flex;
            overflow-x: auto;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 5px;
            margin-bottom: 15px;
        }
        
        .mobile-tab {
            padding: 8px 16px;
            margin-right: 5px;
            white-space: nowrap;
            border-radius: 20px;
            background-color: #f5f5f5;
        }
        
        .mobile-tab.active {
            background-color: #3b82f6;
            color: white;
        }
        
        /* Mobile list item styles */
        .mobile-list-item {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .mobile-list-item-content {
            flex-grow: 1;
        }
        
        .mobile-list-item-title {
            font-weight: 500;
            margin-bottom: 3px;
        }
        
        .mobile-list-item-subtitle {
            font-size: 0.85rem;
            color: #666;
        }
        
        /* Mobile-friendly form styles */
        .mobile-form-field {
            margin-bottom: 20px;
        }
        
        .mobile-form-label {
            font-weight: 500;
            margin-bottom: 5px;
            display: block;
        }
        
        /* Bottom navigation styles */
        .mobile-bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            display: flex;
            justify-content: space-around;
            background-color: white;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
            padding: 10px 0;
            z-index: 1000;
        }
        
        .mobile-bottom-nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 0.8rem;
        }
        
        .mobile-bottom-nav-icon {
            font-size: 1.5rem;
            margin-bottom: 2px;
        }
        
        /* Mobile action buttons */
        .mobile-action-button {
            position: fixed;
            bottom: 70px;
            right: 20px;
            background-color: #3b82f6;
            color: white;
            border-radius: 50%;
            width: 56px;
            height: 56px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
        }
        
        .mobile-action-button:active {
            transform: scale(0.95);
        }
    </style>
    """
    
    st.markdown(mobile_styles, unsafe_allow_html=True)

def create_responsive_card(icon, title, action, button_text, button_key):
    """
    Create a mobile-friendly card with an action button.
    
    Args:
        icon (str): Emoji or icon to display
        title (str): Card title
        action (str): Description of the action
        button_text (str): Text for the action button
        button_key (str): Unique key for the button
        
    Returns:
        bool: True if the button was clicked, False otherwise
    """
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.markdown(f"""
        <div style="font-size: 2rem; display: flex; align-items: center; justify-content: center; 
                   height: 100%;">
            {icon}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="mobile-card-title">{title}</div>
        <div class="mobile-card-action">{action}</div>
        """, unsafe_allow_html=True)
        
        button_clicked = st.button(button_text, key=button_key)
    
    # Add separator
    st.markdown("<hr style='margin: 15px 0 20px 0; opacity: 0.2;'>", unsafe_allow_html=True)
    
    return button_clicked

def create_mobile_tab_layout(tab_items):
    """
    Create a mobile-friendly tab layout.
    
    Args:
        tab_items (list): List of dictionaries with 'icon', 'label', and 'content' keys
            
    Returns:
        int: Index of the selected tab
    """
    # Generate a unique key for this set of tabs
    import random
    tab_key = f"mobile_tabs_{random.randint(1000, 9999)}"
    
    # Initialize selected tab index if not present
    if f"{tab_key}_index" not in st.session_state:
        st.session_state[f"{tab_key}_index"] = 0
    
    # Create the mobile tab bar
    st.markdown(
        """
        <div class="mobile-tabs">
        """ +
        "".join([
            f"""
            <div class="mobile-tab {'active' if idx == st.session_state[f"{tab_key}_index"] else ''}" 
                 onclick="this.dispatchEvent(new CustomEvent('tab_click', {{bubbles: true, detail: {{index: {idx}}}}}))">
                {item['icon']} {item['label']}
            </div>
            """
            for idx, item in enumerate(tab_items)
        ]) +
        """
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Add JavaScript for click handling
    # Since Streamlit doesn't directly support JS interactivity,
    # we'll use buttons below the tabs for tab switching
    
    # Create hidden buttons for each tab
    cols = st.columns(len(tab_items))
    for idx, col in enumerate(cols):
        with col:
            if st.button(f"Tab {idx}", key=f"{tab_key}_{idx}"):
                st.session_state[f"{tab_key}_index"] = idx
                st.rerun()
    
    # Display the content of the selected tab
    selected_idx = st.session_state[f"{tab_key}_index"]
    st.markdown(tab_items[selected_idx]['content'])
    
    return selected_idx

def create_mobile_list_item(title, subtitle=None, trailing_icon=None, on_tap_key=None):
    """
    Create a mobile-friendly list item.
    
    Args:
        title (str): Main title text
        subtitle (str, optional): Subtitle or description text
        trailing_icon (str, optional): Icon to show on the right side
        on_tap_key (str, optional): Key for the clickable area
        
    Returns:
        bool: True if the item was tapped/clicked, False otherwise
    """
    # Create the list item container
    with st.container():
        col1, col2 = st.columns([5, 1])
        
        with col1:
            st.markdown(f"""
            <div class="mobile-list-item-title">{title}</div>
            {f'<div class="mobile-list-item-subtitle">{subtitle}</div>' if subtitle else ''}
            """, unsafe_allow_html=True)
        
        with col2:
            if trailing_icon:
                st.markdown(f"""
                <div style="text-align: right; font-size: 1.2rem;">{trailing_icon}</div>
                """, unsafe_allow_html=True)
        
        # Invisible button for click/tap handling
        clicked = False
        if on_tap_key:
            # Full-width invisible button overlay
            clicked = st.button("", key=on_tap_key)
    
    # Add separator
    st.markdown("<hr style='margin: 0; opacity: 0.2;'>", unsafe_allow_html=True)
    
    return clicked