"""
Professional header component for gcPanel.

A clean, modern header implemented with pure Python Streamlit components.
"""

import streamlit as st

def render_header():
    """
    Render a simple, clean header using only Streamlit components.
    """
    # Apply a more balanced header layout with better visual hierarchy
    st.markdown("""
    <style>
    /* Clean header reset - more balanced approach */
    .main .block-container {
        padding-top: 0.5rem !important; /* Small padding for breathing room */
        max-width: 100% !important; /* Full width */
    }
    
    /* Hide Streamlit default header */
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Main app container */
    .stApp {
        background-color: #f8f9fa !important; /* Light gray background */
    }
    
    /* Improve container structure */
    .stElementContainer {
        margin-bottom: 0.5rem !important; /* Better spacing between elements */
    }
    
    /* Custom header area */
    .header-area {
        background-color: white !important;
        border-bottom: 1px solid #e9ecef !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        padding: 0.75rem 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Improve navigation controls */
    div[data-baseweb="select"] {
        background-color: white !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 4px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        transition: all 0.2s ease !important;
    }
    
    div[data-baseweb="select"]:hover {
        border-color: #adb5bd !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    /* Visual hierarchy for page content */
    h1, h2, h3 {
        margin-top: 0.5rem !important;
        margin-bottom: 1rem !important;
        color: #212529 !important;
    }
    
    /* Main content spacing */
    [data-testid="stVerticalBlock"] {
        padding: 0 1rem !important;
    }
    
    /* Breadcrumb style improvements */
    .breadcrumb-container {
        font-size: 0.85rem !important;
        margin-bottom: 0.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add a container class for the header
    st.markdown('<div class="header-area">', unsafe_allow_html=True)
    # Menu options for dropdown with icons
    menu_options = {
        "Dashboard": {"label": "Dashboard", "icon": "📊"},
        "Project Information": {"label": "Project Information", "icon": "📋"},
        "Schedule": {"label": "Schedule", "icon": "📅"},
        "Safety": {"label": "Safety", "icon": "⚠️"},
        "Contracts": {"label": "Contracts", "icon": "📝"},
        "Cost Management": {"label": "Cost Management", "icon": "💰"},
        "Analytics": {"label": "Analytics", "icon": "📈"},
        "Engineering": {"label": "Engineering", "icon": "🔧"},
        "Field Operations": {"label": "Field Operations", "icon": "🏗️"},
        "Documents": {"label": "Documents", "icon": "📄"},
        "BIM Viewer": {"label": "BIM", "icon": "🏢"},
        "Mobile Companion": {"label": "Mobile Companion", "icon": "📱"},
        "Closeout": {"label": "Closeout", "icon": "✅"},
        "Integrations": {"label": "Integrations", "icon": "🔄"},
        "Features Showcase": {"label": "Features Showcase", "icon": "✨"},
        "Settings": {"label": "Settings", "icon": "⚙️"}
    }
    
    # Get currently selected menu value from session state
    current_menu = st.session_state.get("current_menu", "Dashboard")
    
    # Check if we're on mobile based on screen width (using CSS media query and JavaScript)
    st.markdown("""
    <script>
    // Add a class to the body based on screen width
    if (window.innerWidth <= 768) {
        document.body.classList.add('is-mobile');
    } else {
        document.body.classList.remove('is-mobile');
    }
    </script>
    <style>
    /* Mobile-specific header styles */
    @media (max-width: 768px) {
        /* Stack header elements vertically on mobile */
        .mobile-stack {
            display: block !important;
        }
        
        /* Smaller project info on mobile */
        .project-info div {
            font-size: 90% !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Better layout for header content
    st.markdown("""
    <style>
    /* Cleaner header structure */
    .header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0;
    }
    
    /* Improve dropdown usability */
    div[data-baseweb="select"] {
        z-index: 100 !important;
        min-width: 200px !important;
    }
    
    /* Make navigation more prominent */
    label[data-baseweb="label"] {
        font-weight: 500 !important;
        color: #495057 !important;
    }
    
    /* Remove excess space between elements */
    .stColumn > div {
        margin-bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # More readable column layout with better proportions
    col1, col3 = st.columns([6, 4], gap="small")
    
    with col1:
        # Use Streamlit's native components instead of HTML with event handlers
        logo_col, info_col = st.columns([1, 3])
        
        with logo_col:
            # Make the logo bolder with custom styling
            st.markdown("""
            <style>
            .logo-button {
                font-weight: 800 !important;
                font-size: 18px !important;
                background: none !important;
                border: none !important;
                padding: 0.4rem !important;
                box-shadow: none !important;
                color: #2c3e50 !important;
            }
            .logo-button:hover {
                background-color: rgba(0,0,0,0.05) !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Bolder logo button
            if st.button("🏗️ gcPanel", key="logo_button", use_container_width=True, 
                      help="Return to dashboard"):
                st.session_state.logo_clicked = True
                st.rerun()
                
        with info_col:
            st.markdown("""
            <div class="project-info" style="border-left: 3px solid #4a6572; padding-left: 15px; margin-left: -15px;">
                <div style="font-size: 12px; color: #4a6572; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500;">Project</div>
                <div class="project-title" style="font-size: 16px; font-weight: 600; color: #2c3e50;">Highland Tower Development</div>
                <div class="project-details" style="font-size: 12px; color: #64748b;">$45.5M • 168,500 sq ft • 15 Stories</div>
            </div>
            
            <style>
            /* Mobile responsive project info */
            @media (max-width: 768px) {
                .project-info {
                    padding-left: 10px !important;
                    margin-left: -10px !important;
                }
                .project-title {
                    font-size: 14px !important;
                    white-space: nowrap !important;
                    overflow: hidden !important;
                    text-overflow: ellipsis !important;
                }
                .project-details {
                    font-size: 10px !important;
                }
            }
            </style>
            """, unsafe_allow_html=True)
        
        # Handle logo click
        if st.session_state.get("logo_clicked", False):
            st.session_state.logo_clicked = False
            st.session_state.current_menu = "Dashboard"
            st.rerun()
    
    # Two column layout for better spacing

    with col3:
        # Enhanced more prominent dropdown with improved styling and organization
        # Format options to include icons and grouped categories
        formatted_options = [f"{menu_options[k]['icon']} {menu_options[k]['label']}" for k in menu_options.keys()]
        
        # Create a mapping from formatted options back to keys
        option_to_key = {f"{menu_options[k]['icon']} {menu_options[k]['label']}": k for k in menu_options.keys()}
        
        # Find current menu's formatted option
        current_formatted = f"{menu_options[current_menu]['icon']} {menu_options[current_menu]['label']}"
        
        # Clean styling without extra spacers
        st.markdown("""
        <style>
        /* Align dropdown with the rest of the header */
        div.row-widget.stSelectbox {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Enhanced stylish dropdown menu
        st.markdown("""
        <style>
        /* Elegant Dropdown Styling */
        div[data-baseweb="select"] {
            border-radius: 0 0 4px 4px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            border: 1px solid #e0e7ee;
            border-top: none;
            background-color: #ffffff;
        }
        
        div[data-baseweb="select"]:hover {
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        div[data-baseweb="select"] > div {
            font-weight: 500;
            padding: 13px 16px;
            font-size: 14px;
            color: #1a2a6c;
            letter-spacing: 0.2px;
        }
        
        div[data-baseweb="select"] svg {
            color: #1a2a6c !important;
            width: 18px;
            height: 18px;
        }
        
        div[data-baseweb="menu"] {
            max-height: 450px !important;
            overflow-y: auto;
            border-radius: 6px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            border: 1px solid #e0e7ee;
        }
        
        div[data-baseweb="menu"] ul {
            padding: 6px 0;
        }
        
        div[data-baseweb="menu"] li {
            padding: 10px 16px !important;
            font-size: 14px;
            transition: all 0.2s ease;
        }
        
        div[data-baseweb="menu"] li:hover {
            background-color: #f0f7ff !important;
            transform: translateX(2px);
        }
        
        /* Add subtle dividers between menu items */
        div[data-baseweb="menu"] li:not(:last-child) {
            border-bottom: 1px solid #f5f5f8;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Enhanced navigation styling with vertical alignment fix
        st.markdown("""
        <style>
        /* Fix vertical alignment with the rest of the header - removed margin */
        div[data-baseweb="select"] {
            margin-top: 0 !important; /* Completely removed margin */
        }
        
        /* Remove label spacing above Navigation dropdown */
        label[data-baseweb="label"] {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
        }
        
        /* Reduce selectbox containers spacing */
        div.row-widget.stSelectbox {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Mobile responsive adjustments */
        @media (max-width: 768px) {
            /* Hide the label on mobile */
            label[data-baseweb="label"] {
                display: none !important;
            }
            
            /* Make dropdown take full width on mobile */
            div[data-baseweb="select"] {
                width: 100% !important;
                margin-top: 5px !important; /* Further reduced margin for mobile */
            }
            
            /* Larger touch target on mobile */
            div[data-baseweb="select"] > div {
                min-height: 44px !important;
                padding: 10px 14px !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Responsive dropdown
        selected_formatted = st.selectbox(
            "Navigation",  # Label for accessibility
            options=formatted_options,
            index=formatted_options.index(current_formatted),
            key="header_nav_dropdown",
            label_visibility="visible"  # Show the label on desktop, hidden on mobile via CSS
        )
        
        # Convert selected formatted option back to key
        selected = option_to_key[selected_formatted]
        
        # Update session state if menu changed
        if selected != current_menu:
            st.session_state.current_menu = selected
            st.rerun()
    
    # Close the header-area div
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add a more subtle divider
    st.markdown("""
    <style>
    .elegant-divider {
        display: none; /* Remove the divider - now using header-area border */
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add a content area container with better styling
    st.markdown("""
    <div style="padding: 0.5rem 1.5rem; background-color: white; border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-bottom: 1rem;">
    """, unsafe_allow_html=True)
    
    # Breadcrumb and notification row with better spacing and visual hierarchy
    brow_col1, brow_col2 = st.columns([9, 3])
    
    with brow_col1:
        # Show breadcrumb for the current page
        from components.simple_breadcrumbs import get_breadcrumbs_for_page, simple_breadcrumbs
        breadcrumb_items = get_breadcrumbs_for_page(current_menu)
        simple_breadcrumbs(breadcrumb_items)
    
    with brow_col2:
        # Create a styled notification button that includes the bell icon
        notification_style = """
        <style>
        div[data-testid="stButton"] > button {
            background-color: transparent;
            border: none;
            color: #6b7280;
            padding: 0;
            font-size: 1.2rem;
            position: relative;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: rgba(0,0,0,0.05);
            color: #3b82f6;
        }
        </style>
        """
        st.markdown(notification_style, unsafe_allow_html=True)
        
        # Use a pure Python approach for the notification button without HTML
        notification_col = st.container()
        notification_button = notification_col.button("🔔", key="notif_button", help="View notifications")
        
        # Add the notification badge using a separate element
        notification_col.markdown(
            """
            <div style="position: relative; top: -40px; left: 20px; z-index: 1000; width: 20px; height: 20px;">
                <span style="background-color: #ef4444; color: white; border-radius: 50%; font-size: 0.7rem; padding: 2px 5px;">3</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        if notification_button:
            st.session_state.show_notification_center = not st.session_state.get("show_notification_center", False)
            st.rerun()