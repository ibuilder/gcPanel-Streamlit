"""
Accessibility utilities for gcPanel.

This module provides functions for implementing accessibility features
in the application, including keyboard navigation, screen reader support,
and ARIA attributes.
"""

import streamlit as st
import html

def add_accessibility_css():
    """Add accessibility-related CSS to the Streamlit app."""
    css = """
    <style>
    /* Focus styles for better keyboard navigation */
    :focus {
        outline: 3px solid #3367D6 !important;
        outline-offset: 2px !important;
    }
    
    /* Skip to content link */
    .skip-to-content {
        position: absolute;
        top: -40px;
        left: 0;
        background: #3367D6;
        color: white;
        padding: 8px;
        z-index: 10000;
        transition: top 0.3s;
    }
    
    .skip-to-content:focus {
        top: 0;
    }
    
    /* High contrast mode support */
    @media (forced-colors: active) {
        .stButton button {
            border: 2px solid ButtonText !important;
        }
        
        a {
            text-decoration: underline !important;
        }
    }
    
    /* Increased color contrast */
    .low-contrast {
        color: #727272 !important;
    }
    
    .high-contrast {
        color: #424242 !important;
    }
    
    /* Improved button and input focus states */
    .stButton button:focus {
        box-shadow: 0 0 0 2px white, 0 0 0 4px #3367D6 !important;
    }
    
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus {
        box-shadow: 0 0 0 2px white, 0 0 0 4px #3367D6 !important;
    }
    
    /* Keyboard accessible menu */
    .keyboard-nav .menu-item:focus {
        background-color: rgba(51, 103, 214, 0.1) !important;
        box-shadow: 0 0 0 2px #3367D6 !important;
    }
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def add_skip_to_content_link():
    """Add a skip to content link for keyboard navigation."""
    html_code = """
    <a href="#main-content" class="skip-to-content">Skip to main content</a>
    <div id="main-content" tabindex="-1"></div>
    """
    
    st.markdown(html_code, unsafe_allow_html=True)

def add_keyboard_shortcuts_info():
    """Add information about keyboard shortcuts."""
    shortcuts = {
        "General Navigation": [
            {"key": "Tab", "description": "Move forward through interactive elements"},
            {"key": "Shift+Tab", "description": "Move backward through interactive elements"},
            {"key": "Enter", "description": "Activate buttons, links, or submit forms"},
            {"key": "Space", "description": "Toggle checkboxes or activate buttons"}
        ],
        "Menu Navigation": [
            {"key": "Alt+M", "description": "Focus on menu"},
            {"key": "Arrow Up/Down", "description": "Navigate menu items"},
            {"key": "Enter", "description": "Select menu item"}
        ],
        "Content Navigation": [
            {"key": "Alt+H", "description": "Go to home/dashboard"},
            {"key": "Alt+S", "description": "Open search"},
            {"key": "Alt+N", "description": "Go to notifications"}
        ]
    }
    
    with st.expander("Keyboard Shortcuts"):
        for category, items in shortcuts.items():
            st.subheader(category)
            
            for item in items:
                st.markdown(f"**{item['key']}**: {item['description']}")

def render_with_aria(component_type, content, label=None, description=None, key=None, **kwargs):
    """
    Render a component with proper ARIA attributes.
    
    Args:
        component_type: Type of component (text, button, checkbox, etc.)
        content: Content to display
        label: Accessible label for screen readers
        description: Accessible description
        key: Streamlit key for the component
        **kwargs: Additional arguments for the component
        
    Returns:
        The rendered component
    """
    if component_type == "button":
        button_html = f"""
        <button
            class="stButton"
            role="button"
            aria-label="{html.escape(label) if label else html.escape(content)}"
            {f'aria-describedby="{key}-desc"' if description else ''}
            id="{key}"
        >
            {html.escape(content)}
        </button>
        """
        
        if description:
            button_html += f'<div id="{key}-desc" class="sr-only">{html.escape(description)}</div>'
        
        return st.markdown(button_html, unsafe_allow_html=True)
    
    elif component_type == "checkbox":
        return st.checkbox(
            label=content,
            key=key,
            **kwargs
        )
    
    elif component_type == "text_input":
        return st.text_input(
            label=content,
            key=key,
            help=description,
            **kwargs
        )
    
    elif component_type == "select":
        return st.selectbox(
            label=content,
            key=key,
            help=description,
            **kwargs
        )
    
    elif component_type == "text":
        if label:
            st.markdown(f'<span aria-label="{html.escape(label)}">{html.escape(content)}</span>', unsafe_allow_html=True)
        else:
            st.markdown(content, unsafe_allow_html=False)
    
    else:
        # Default to standard Streamlit components
        return getattr(st, component_type)(content, **kwargs)

def create_accessible_table(headers, rows, caption=None):
    """
    Create an accessible HTML table.
    
    Args:
        headers: List of column headers
        rows: List of rows, each row is a list of cells
        caption: Optional table caption
        
    Returns:
        HTML for an accessible table
    """
    html_code = '<div class="table-container" role="region" aria-label="Data Table" tabindex="0">'
    html_code += '<table class="dataframe" role="table">'
    
    if caption:
        html_code += f'<caption>{html.escape(caption)}</caption>'
    
    # Add headers
    html_code += '<thead role="rowgroup">'
    html_code += '<tr role="row">'
    for header in headers:
        html_code += f'<th role="columnheader" scope="col">{html.escape(str(header))}</th>'
    html_code += '</tr>'
    html_code += '</thead>'
    
    # Add rows
    html_code += '<tbody role="rowgroup">'
    for row in rows:
        html_code += '<tr role="row">'
        for i, cell in enumerate(row):
            html_code += f'<td role="cell" data-label="{html.escape(str(headers[i]))}">{html.escape(str(cell))}</td>'
        html_code += '</tr>'
    html_code += '</tbody>'
    
    html_code += '</table>'
    html_code += '</div>'
    
    # Add CSS for responsive table
    html_code += """
    <style>
    .table-container {
        overflow-x: auto;
        margin-bottom: 1rem;
    }
    
    @media screen and (max-width: 600px) {
        .dataframe thead {
            display: none;
        }
        
        .dataframe tbody tr {
            display: block;
            margin-bottom: 0.5rem;
            border: 1px solid #e0e0e0;
        }
        
        .dataframe tbody tr td {
            display: block;
            text-align: right;
            padding: 0.5rem;
            position: relative;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .dataframe tbody tr td:before {
            content: attr(data-label);
            float: left;
            font-weight: bold;
        }
    }
    </style>
    """
    
    return html_code

def render_screenreader_only_text(text):
    """
    Render text that is only visible to screen readers.
    
    Args:
        text: Text content
    """
    st.markdown(f"""
    <style>
    .sr-only {{
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border-width: 0;
    }}
    </style>
    <div class="sr-only">{html.escape(text)}</div>
    """, unsafe_allow_html=True)

def initialize_accessibility():
    """Initialize accessibility features for the application."""
    # Add CSS
    add_accessibility_css()
    
    # Add skip to content link
    add_skip_to_content_link()
    
    # Add keyboard shortcut handler
    st.markdown("""
    <script>
    document.addEventListener('keydown', function(e) {
        // Alt+M for menu focus
        if (e.altKey && e.key === 'm') {
            const menu = document.querySelector('.sidebar .sidebar-content');
            if (menu) {
                menu.focus();
                e.preventDefault();
            }
        }
        
        // Alt+H for home
        if (e.altKey && e.key === 'h') {
            const homeLink = document.querySelector('a[href="/?page=dashboard"]');
            if (homeLink) {
                homeLink.click();
                e.preventDefault();
            }
        }
        
        // Alt+S for search
        if (e.altKey && e.key === 's') {
            const searchInput = document.querySelector('input[aria-label="Search"]');
            if (searchInput) {
                searchInput.focus();
                e.preventDefault();
            }
        }
        
        // Alt+N for notifications
        if (e.altKey && e.key === 'n') {
            const notifButton = document.querySelector('button.notification-btn');
            if (notifButton) {
                notifButton.click();
                e.preventDefault();
            }
        }
    });
    </script>
    """, unsafe_allow_html=True)