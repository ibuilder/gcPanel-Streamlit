"""
Responsive UI utilities for gcPanel.

This module provides utilities for creating responsive UI components that work well
on both desktop and mobile devices. It includes:

- Responsive layout adjustments
- Touch-friendly UI components
- Media queries for different screen sizes
- Device detection and adaptation
"""

import streamlit as st
import platform
import re
from typing import List, Dict, Any, Tuple, Optional, Union

def apply_responsive_styles():
    """
    Apply global responsive styling for better mobile experience.
    
    This adds CSS that improves the mobile experience with:
    - Better button sizes for touch
    - Improved form controls
    - Proper spacing and margins
    - Text size adjustments
    """
    st.markdown(
        """
        <style>
        /* Global Responsive Adjustments */
        @media (max-width: 768px) {
            /* Make text slightly larger on mobile */
            .stMarkdown p {
                font-size: 1.05rem;
            }
            
            /* Make buttons more touch-friendly */
            .stButton button {
                min-height: 2.5rem;
                padding: 0.5rem 1rem !important;
                margin: 0.5rem 0 !important;
            }
            
            /* Make form inputs taller */
            .stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input {
                height: 2.5rem;
                font-size: 1rem;
            }
            
            /* More space between form elements */
            .stForm > div > div {
                margin-bottom: 1rem;
            }
            
            /* Reduce padding in containers */
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1rem;
            }
            
            /* Make tables horizontally scrollable */
            .stTable {
                overflow-x: auto;
            }
            
            /* Make tab text larger */
            button[data-baseweb="tab"] {
                font-size: 0.95rem !important;
            }
            
            /* Make selectbox dropdowns more touch-friendly */
            .stSelectbox div[data-baseweb="select"] > div {
                min-height: 2.5rem;
            }
            
            /* Make multiselect dropdowns more touch-friendly */
            .stMultiSelect div[data-baseweb="select"] > div {
                min-height: 2.5rem;
            }
            
            /* Dashboard metrics */
            [data-testid="metric-container"] {
                width: 100%;
            }
            
            /* Charts and visualizations */
            [data-testid="stArrowVegaLiteChart"] > div {
                width: 100% !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def detect_mobile():
    """
    Detect if the current device is a mobile device.
    
    Uses browser user agent string if available, otherwise makes a reasonable guess
    based on session state parameters.
    
    Returns:
        bool: True if the user is on a mobile device, False otherwise
    """
    # This is our best guess in Streamlit
    screen_width = st.session_state.get("_screen_width", 1200)
    return screen_width < 768

def create_responsive_columns(count_desktop: int = 3, count_mobile: int = 1):
    """
    Create columns that adapt to screen size.
    
    Args:
        count_desktop (int): Number of columns on desktop
        count_mobile (int): Number of columns on mobile
        
    Returns:
        list: List of column objects
    """
    is_mobile = detect_mobile()
    column_count = count_mobile if is_mobile else count_desktop
    return st.columns(column_count)

def responsive_container(mobile_padding: bool = True):
    """
    Create a container with responsive behavior.
    
    Args:
        mobile_padding (bool): Whether to add extra padding on mobile
        
    Returns:
        container: A streamlit container with responsive behavior
    """
    container = st.container()
    
    is_mobile = detect_mobile()
    if is_mobile and mobile_padding:
        with container:
            st.markdown(
                """
                <style>
                div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stVerticalBlock"]) {
                    padding-left: 0.5rem;
                    padding-right: 0.5rem;
                }
                </style>
                """, 
                unsafe_allow_html=True
            )
    
    return container

def responsive_grid(items: List[Dict[str, Any]], 
                    cols_desktop: int = 3, 
                    cols_mobile: int = 1,
                    render_func=None):
    """
    Create a responsive grid layout.
    
    Args:
        items (List[Dict]): List of items to display
        cols_desktop (int): Number of columns on desktop
        cols_mobile (int): Number of columns on mobile
        render_func (function): Function to render each item
        
    Returns:
        None: Renders the grid directly
    """
    is_mobile = detect_mobile()
    cols_count = cols_mobile if is_mobile else cols_desktop
    
    # Create a grid layout
    if not items:
        st.info("No items to display")
        return
    
    # Create columns
    cols = st.columns(cols_count)
    
    # Distribute items across columns
    for i, item in enumerate(items):
        with cols[i % cols_count]:
            if render_func:
                render_func(item)
            else:
                st.write(item)

def responsive_table(df, height=None):
    """
    Display a table that works well on both desktop and mobile.
    
    Args:
        df: Pandas DataFrame to display
        height (int, optional): Height of the table
        
    Returns:
        None: Renders the table directly
    """
    is_mobile = detect_mobile()
    
    # Add special styling for mobile
    if is_mobile:
        st.markdown(
            """
            <style>
            .responsive-table {
                overflow-x: auto;
                font-size: 0.85rem;
            }
            .responsive-table table {
                width: 100%;
                min-width: 400px;
            }
            </style>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown('<div class="responsive-table">', unsafe_allow_html=True)
        st.dataframe(df, height=height, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.dataframe(df, height=height, use_container_width=True)

def touch_friendly_button(label, key=None, type="primary", help=None):
    """
    Create a button that's easier to tap on touch devices.
    
    Args:
        label (str): Button label
        key (str, optional): Unique key for the button
        type (str): Button type (primary, secondary)
        help (str, optional): Help text
        
    Returns:
        bool: True if button was clicked, False otherwise
    """
    is_mobile = detect_mobile()
    
    if is_mobile:
        st.markdown(
            f"""
            <style>
            [data-testid="stButton"] > button {{
                height: 3rem;
                padding: 0.75rem 1.5rem;
                font-size: 1.05rem;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    return st.button(label, key=key, type=type, help=help)

def touch_friendly_form_field(field_type, label, key=None, **kwargs):
    """
    Create a form field that's easier to use on touch devices.
    
    Args:
        field_type (str): Type of field (text_input, number_input, etc.)
        label (str): Field label
        key (str, optional): Unique key for the field
        **kwargs: Additional arguments to pass to the field function
        
    Returns:
        Any: The value of the form field
    """
    is_mobile = detect_mobile()
    
    if is_mobile:
        st.markdown(
            f"""
            <style>
            [data-testid="stTextInput"] input,
            [data-testid="stNumberInput"] input,
            [data-testid="stDateInput"] input,
            div[data-baseweb="select"] > div {{
                min-height: 2.75rem;
                font-size: 1.05rem;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    field_func = getattr(st, field_type)
    return field_func(label=label, key=key, **kwargs)

def responsive_dashboard_metrics(metrics: List[Dict[str, Any]]):
    """
    Display dashboard metrics in a responsive layout.
    
    Args:
        metrics (List[Dict]): List of metrics with keys:
            - label: Metric label
            - value: Metric value
            - delta: Metric delta (optional)
            - delta_color: Color for delta (optional)
            
    Returns:
        None: Renders the metrics directly
    """
    is_mobile = detect_mobile()
    
    # Determine column count based on device
    if is_mobile:
        if len(metrics) <= 2:
            col_count = len(metrics)
        else:
            col_count = 2
    else:
        if len(metrics) <= 5:
            col_count = len(metrics)
        else:
            col_count = 4
    
    cols = st.columns(col_count)
    
    for i, metric in enumerate(metrics):
        with cols[i % col_count]:
            delta = metric.get("delta")
            delta_color = metric.get("delta_color", "normal")
            
            if delta:
                st.metric(
                    label=metric["label"],
                    value=metric["value"],
                    delta=delta,
                    delta_color=delta_color
                )
            else:
                st.metric(
                    label=metric["label"],
                    value=metric["value"]
                )
                
def responsive_area(desktop_content_func, mobile_content_func=None):
    """
    Render different content based on the device type.
    
    Args:
        desktop_content_func (callable): Function to render desktop content
        mobile_content_func (callable, optional): Function to render mobile content
                                                If None, uses desktop_content_func
    
    Returns:
        None: Renders the content directly
    """
    is_mobile = detect_mobile()
    
    if is_mobile and mobile_content_func:
        mobile_content_func()
    else:
        desktop_content_func()

def add_touch_scrolling_to_charts():
    """
    Add touch-friendly scrolling behavior to charts and tables.
    
    This adds touch-scrolling capability to horizontal scrollable elements,
    which is especially useful for tables and charts on mobile devices.
    """
    st.markdown(
        """
        <style>
        /* Enable touch scrolling for tables and charts */
        .stTable, [data-testid="stArrowVegaLiteChart"] {
            -webkit-overflow-scrolling: touch;
        }
        
        /* Make scrollbars more visible on mobile */
        @media (max-width: 768px) {
            /* Track */
            ::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }
            
            /* Handle */
            ::-webkit-scrollbar-thumb {
                background: rgba(0,0,0,0.3);
                border-radius: 3px;
            }
            
            /* Handle on hover */
            ::-webkit-scrollbar-thumb:hover {
                background: rgba(0,0,0,0.5);
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def apply_all_responsive_styles():
    """Apply all responsive styles and enhancements."""
    apply_responsive_styles()
    add_touch_scrolling_to_charts()
    
    # Add screen size detection script
    st.markdown(
        """
        <script>
        // Send screen dimensions to Streamlit
        const updateScreenSize = () => {
            const width = window.innerWidth;
            const height = window.innerHeight;
            const data = {
                width: width,
                height: height,
                isMobile: width < 768,
                isTablet: width >= 768 && width < 1024,
                isDesktop: width >= 1024
            };
            
            window.parent.postMessage({
                type: "streamlit:setComponentValue",
                value: data
            }, "*");
        };
        
        // Update on resize
        window.addEventListener('resize', updateScreenSize);
        
        // Initial update
        updateScreenSize();
        </script>
        """,
        unsafe_allow_html=True
    )