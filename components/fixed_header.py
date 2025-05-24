"""
Fixed Header Component for gcPanel.

This module provides a header component that is positioned correctly at the top of the page.
"""

import streamlit as st
from app_config import MENU_OPTIONS, MENU_MAP, PROJECT_INFO

def render_fixed_header():
    """
    Render a header that's correctly positioned at the top of the page.
    Uses direct HTML/CSS to ensure proper positioning.
    """
    
    # First, apply fixes to Streamlit's default margins and padding
    st.markdown("""
    <style>
    /* Remove all padding and margins from main container */
    .main .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
        max-width: 100% !important;
    }
    
    /* Fix default Streamlit header */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Fix breadcrumbs */
    .breadcrumb-container {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Ensure first element has no top margin */
    .element-container:first-child {
        margin-top: 0 !important;
    }
    
    /* Force vertical block spacing */
    [data-testid="stVerticalBlock"] > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Style for our custom navigation container */
    .nav-dropdown-container {
        width: 100%;
        text-align: right;
        padding-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add more CSS to remove spacing
    st.markdown("""
    <style>
    /* Move everything to top of page */
    .main .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Remove space under header and above breadcrumbs */
    .breadcrumb-container {
        margin-top: 0 !important;
        padding-top: 0 !important;
        margin-bottom: 0.25rem !important;
    }
    
    /* Remove padding from columns */
    div[data-testid="column"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Remove padding from select box */
    div[data-testid="stSelectbox"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Remove top padding for all elements */
    .stVerticalBlock {
        gap: 0rem !important;
    }
    
    /* Compact header layout */
    .header-row {
        margin: 0 !important;
        padding: 5px 0 !important;
    }
    
    /* Remove element container padding */
    .element-container {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Make sure all blocks start from the top */
    div[data-testid="stVerticalBlock"] > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a four-column layout for the header with no padding
    header_col1, header_col2, header_col3, header_col4 = st.columns([1, 2, 1, 0.5])
    
    # Column 1: Enhanced Logo with animation
    with header_col1:
        st.markdown("""
        <div style="display:flex; align-items:center; padding:0; margin:0;" class="logo-container">
            <div style="font-size:24px; color:#f59e0b; margin-right:8px; transition: transform 0.3s ease;" class="logo-icon">🏗️</div>
            <div style="font-family: 'Inter', sans-serif;">
                <span style="font-weight:700; color:#1e293b; font-size:18px;">gc</span><span style="font-weight:700; color:#3b82f6; font-size:18px;">Panel</span>
                <div style="font-size:10px; color:#64748b; line-height:1;">Construction Management</div>
            </div>
        </div>
        <style>
        .logo-container:hover .logo-icon {
            transform: rotate(15deg) scale(1.1);
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Column 2: Project Info (centered)
    with header_col2:
        st.markdown("""
        <div style="text-align:center; padding:0; margin:0;">
            <div style="font-weight:bold; font-size:18px; line-height:1.2;">Highland Tower Development</div>
            <div style="font-size:12px; color:#666; line-height:1.2;">$45.5M • 168,500 sq ft • 15 stories above ground, 2 below</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Column 3: Navigation dropdown
    with header_col3:
        current_menu = st.session_state.get("current_menu", "Dashboard")
        
        # Find current menu option with icon
        current_menu_option = "📊 Dashboard"
        for option in MENU_OPTIONS:
            if MENU_MAP[option] == current_menu:
                current_menu_option = option
                break
        
        selected_menu = st.selectbox(
            label="Navigation",
            options=MENU_OPTIONS,
            index=MENU_OPTIONS.index(current_menu_option),
            key="nav_dropdown",
            label_visibility="collapsed"
        )
        
        # Update current menu if selection changed
        if selected_menu != current_menu_option:
            new_menu = MENU_MAP[selected_menu]
            st.session_state.current_menu = new_menu
            st.rerun()
    
    # Column 4: User menu and logout
    with header_col4:
        user = st.session_state.get("user", {})
        user_name = user.get("full_name", "User")
        
        # Create a simple logout button
        if st.button("🚪 Logout", key="logout_btn", help=f"Logout {user_name}"):
            # Clear authentication
            st.session_state.authenticated = False
            if "user" in st.session_state:
                del st.session_state.user
            if "token" in st.session_state:
                del st.session_state.token
            st.rerun()
    
    # Add a horizontal line below the header
    st.markdown("""
    <hr style="height:1px; margin:0; padding:0; border:none; background-color:#e9ecef;">
    """, unsafe_allow_html=True)