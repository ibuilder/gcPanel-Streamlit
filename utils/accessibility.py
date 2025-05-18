"""
Accessibility utilities for gcPanel.

This module provides helpers to ensure WCAG 2.1 compliance
and better accessibility for all users.
"""

import streamlit as st

def initialize_accessibility():
    """Initialize accessibility settings in session state."""
    if "high_contrast" not in st.session_state:
        st.session_state.high_contrast = False
    
    if "large_text" not in st.session_state:
        st.session_state.large_text = False
    
    if "reduce_motion" not in st.session_state:
        st.session_state.reduce_motion = False

def apply_accessibility_styles():
    """Apply accessibility styles based on user preferences."""
    # Build CSS for accessibility
    css = """
    <style>
    """
    
    # High contrast mode
    if st.session_state.get("high_contrast", False):
        css += """
        body {
            color: #FFFFFF !important;
            background-color: #000000 !important;
        }
        
        a, button, .stButton button {
            color: #FFFF00 !important;
            border-color: #FFFF00 !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF !important;
        }
        
        .dashboard-card {
            background-color: #222222 !important;
            border: 2px solid #FFFFFF !important;
        }
        """
    
    # Large text mode
    if st.session_state.get("large_text", False):
        css += """
        body {
            font-size: 125% !important;
        }
        
        p, div, span, li {
            font-size: 1.2rem !important;
            line-height: 1.5 !important;
        }
        
        h1 { font-size: 2.4rem !important; }
        h2 { font-size: 2.0rem !important; }
        h3 { font-size: 1.8rem !important; }
        h4 { font-size: 1.6rem !important; }
        h5 { font-size: 1.4rem !important; }
        h6 { font-size: 1.2rem !important; }
        
        button, .stButton button {
            font-size: 1.2rem !important;
            padding: 0.6rem 1.2rem !important;
        }
        
        .stSelectbox, .stTextInput input {
            font-size: 1.2rem !important;
            height: auto !important;
            padding: 0.5rem !important;
        }
        """
    
    # Reduce motion
    if st.session_state.get("reduce_motion", False):
        css += """
        * {
            animation: none !important;
            transition: none !important;
        }
        """
    
    css += """
    </style>
    """
    
    # Apply the CSS if any accessibility options are enabled
    if (st.session_state.get("high_contrast", False) or 
        st.session_state.get("large_text", False) or 
        st.session_state.get("reduce_motion", False)):
        st.markdown(css, unsafe_allow_html=True)

def render_accessibility_settings():
    """Render accessibility settings controls."""
    st.header("Accessibility Settings")
    
    initialize_accessibility()
    
    st.markdown("""
    These settings help make the application more accessible to users with different needs.
    Changes will apply immediately and be saved for your next visit.
    """)
    
    # High contrast mode
    high_contrast = st.checkbox(
        "High Contrast Mode",
        value=st.session_state.get("high_contrast", False),
        help="Increases contrast for better visibility"
    )
    
    # Large text mode
    large_text = st.checkbox(
        "Large Text Mode",
        value=st.session_state.get("large_text", False),
        help="Increases text size for better readability"
    )
    
    # Reduce motion
    reduce_motion = st.checkbox(
        "Reduce Motion",
        value=st.session_state.get("reduce_motion", False),
        help="Reduces animations and motion effects"
    )
    
    # Update session state if settings changed
    if high_contrast != st.session_state.get("high_contrast", False):
        st.session_state.high_contrast = high_contrast
        st.rerun()
        
    if large_text != st.session_state.get("large_text", False):
        st.session_state.large_text = large_text
        st.rerun()
        
    if reduce_motion != st.session_state.get("reduce_motion", False):
        st.session_state.reduce_motion = reduce_motion
        st.rerun()

def set_page_metadata(title, description):
    """
    Set page metadata for better screen reader and SEO support.
    
    Args:
        title: Page title
        description: Page description
    """
    # This is a bit of a hack as Streamlit doesn't directly support meta tags
    meta_html = f"""
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <script>
        document.title = "{title}";
    </script>
    """
    st.markdown(meta_html, unsafe_allow_html=True)

def accessibility_hints():
    """Generate accessibility hints for screen readers."""
    # These hints are hidden visually but available to screen readers
    sr_hints = """
    <div class="sr-only" style="position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border-width: 0;">
        <p>Navigation tip: Use tab key to navigate through interactive elements.</p>
        <p>This application supports keyboard navigation.</p>
        <p>To access accessibility settings, press Alt+A or navigate to the settings page.</p>
    </div>
    """
    st.markdown(sr_hints, unsafe_allow_html=True)

def create_skip_link():
    """Create a skip navigation link for keyboard users."""
    skip_link = """
    <style>
    .skip-link {
        position: absolute;
        top: -40px;
        left: 0;
        background: #3367D6;
        color: white;
        padding: 8px;
        z-index: 100;
        transition: top 0.3s;
    }
    
    .skip-link:focus {
        top: 0;
    }
    </style>
    
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <div id="main-content"></div>
    """
    st.markdown(skip_link, unsafe_allow_html=True)