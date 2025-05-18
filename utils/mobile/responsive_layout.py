"""
Mobile Responsive Layout Utilities for gcPanel.

This module provides utilities to create responsive layouts
that work well on mobile devices and tablets.
"""

import streamlit as st
import platform

def is_mobile_device():
    """
    Detect if the current device is likely a mobile device.
    
    This is a best-effort detection based on session state information.
    For more accurate detection, a JavaScript-based approach would be needed.
    
    Returns:
        bool: True if the device appears to be mobile, False otherwise
    """
    # Store the detected device type in session state
    if "device_type" not in st.session_state:
        # Check if we can identify a common mobile dimension
        # Default to desktop if we can't determine
        st.session_state.device_type = "desktop"
    
    return st.session_state.device_type == "mobile"

def set_mobile_device_detection():
    """
    Set up device detection using CSS and JavaScript.
    
    This function injects CSS and JavaScript to better detect mobile devices
    and adjust the layout accordingly.
    """
    # Add a placeholder for JavaScript to detect device and update session state
    st.markdown("""
    <script>
        // This is a placeholder for actual device detection
        // In production, this would use more sophisticated detection methods
        const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
        if (isMobile) {
            // This is where we would set a cookie or localStorage value
            // that the server side could read on subsequent requests
            console.log("Mobile device detected");
        }
    </script>
    """, unsafe_allow_html=True)

def create_responsive_columns(ratios=None, num_columns=2, mobile_stack=True):
    """
    Create responsive columns that stack on mobile devices.
    
    Args:
        ratios (list): List of column width ratios, e.g. [2, 1] for 2/3 and 1/3
        num_columns (int): Number of equal-width columns if ratios not provided
        mobile_stack (bool): Whether to stack columns on mobile devices
        
    Returns:
        list: List of column objects
    """
    # Detect if we're on a mobile device
    mobile = is_mobile_device()
    
    # If we should stack on mobile, return a single column
    if mobile and mobile_stack:
        return [st.container()]
    
    # Otherwise create columns based on ratios or equal widths
    if ratios:
        return st.columns(ratios)
    else:
        return st.columns(num_columns)

def add_mobile_styles():
    """
    Add CSS styles for better mobile display.
    
    This injects CSS that improves the display on mobile devices.
    """
    mobile_css = """
    <style>
        /* Responsive styles for mobile devices */
        @media (max-width: 768px) {
            /* Adjust page margins */
            .main .block-container {
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
                padding-top: 0.5rem !important;
            }
            
            /* Make buttons more touch-friendly */
            .stButton button {
                min-height: 3rem;
            }
            
            /* Adjust font sizes for readability */
            h1 {
                font-size: 1.8rem !important;
            }
            
            h2 {
                font-size: 1.4rem !important;
            }
            
            h3 {
                font-size: 1.2rem !important;
            }
            
            p, li, div {
                font-size: 0.95rem !important;
            }
            
            /* Make selectbox and multiselect more touch-friendly */
            .stSelectbox, .stMultiselect {
                min-height: 2.5rem;
            }
            
            /* Adjust datepicker for touch */
            .stDateInput {
                min-height: 2.5rem;
            }
            
            /* Make cards more compact */
            .element-container {
                margin-bottom: 0.5rem;
            }
        }
    </style>
    """
    
    st.markdown(mobile_css, unsafe_allow_html=True)

def create_mobile_friendly_menu(menu_items, icon_name="menu"):
    """
    Create a mobile-friendly hamburger menu.
    
    Args:
        menu_items (dict): Dictionary of menu item labels and functions
        icon_name (str): Name of the icon to use for the menu button
        
    Returns:
        str: Selected menu item
    """
    # On mobile, use a compact dropdown menu
    if is_mobile_device():
        return st.selectbox("", options=list(menu_items.keys()), label_visibility="collapsed")
    else:
        # On desktop, use horizontal buttons
        cols = st.columns(len(menu_items))
        selected = None
        
        for i, (label, _) in enumerate(menu_items.items()):
            with cols[i]:
                if st.button(label):
                    selected = label
        
        return selected

def create_responsive_card(title, content, image_path=None, action_buttons=None):
    """
    Create a responsive card component that works well on mobile.
    
    Args:
        title (str): Card title
        content (str): Card content
        image_path (str): Path to image (optional)
        action_buttons (list): List of button labels and callbacks
        
    Returns:
        None
    """
    # Create card container
    card = st.container()
    
    with card:
        # Card styling
        st.markdown("""
        <style>
        .card-container {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 1rem;
            margin-bottom: 1rem;
            background-color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .card-title {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .card-content {
            margin-bottom: 1rem;
        }
        
        @media (max-width: 768px) {
            .card-container {
                padding: 0.75rem;
            }
            
            .card-title {
                font-size: 1.1rem;
            }
        }
        </style>
        
        <div class="card-container">
            <div class="card-title">{title}</div>
            <div class="card-content">{content}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Image display if provided
        if image_path:
            st.image(image_path)
        
        # Action buttons
        if action_buttons:
            cols = create_responsive_columns(num_columns=len(action_buttons), mobile_stack=False)
            
            for i, (label, callback) in enumerate(action_buttons):
                with cols[i]:
                    if st.button(label, key=f"card_button_{title}_{label}"):
                        callback()

def init_mobile_optimization():
    """Initialize mobile optimization features."""
    # Add mobile styles
    add_mobile_styles()
    
    # Set up device detection
    set_mobile_device_detection()
    
    # Set a flag in session state for mobile optimization
    if "mobile_optimized" not in st.session_state:
        st.session_state.mobile_optimized = True