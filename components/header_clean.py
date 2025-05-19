"""
Professional header component for gcPanel.

A clean, modern header implemented with pure Python Streamlit components.
"""

import streamlit as st

def render_header():
    """
    Render a simple, clean header using only Streamlit components.
    """
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
    
    # Create a balanced two-column layout for the header with more space for the dropdown
    col1, col3 = st.columns([5, 5])
    
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
            <div style="border-left: 3px solid #4a6572; padding-left: 15px; margin-left: -15px;">
                <div style="font-size: 12px; color: #4a6572; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500;">Project</div>
                <div style="font-size: 16px; font-weight: 600; color: #2c3e50;">Highland Tower Development</div>
                <div style="font-size: 12px; color: #64748b;">$45.5M • 168,500 sq ft • 15 Stories</div>
            </div>
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
        
        # Clean dropdown showing current selection
        selected_formatted = st.selectbox(
            "Navigation",  # Label for accessibility
            options=formatted_options,
            index=formatted_options.index(current_formatted),
            key="header_nav_dropdown",
            label_visibility="visible"  # Show the label
        )
        
        # Convert selected formatted option back to key
        selected = option_to_key[selected_formatted]
        
        # Update session state if menu changed
        if selected != current_menu:
            st.session_state.current_menu = selected
            st.rerun()
    
    # Display a subtle, elegant divider
    st.markdown("""
    <style>
    .elegant-divider {
        height: 1px;
        background: linear-gradient(to right, rgba(220,220,220,0.1), rgba(220,220,220,0.7), rgba(220,220,220,0.1));
        margin: 10px 0 12px 0;
    }
    </style>
    <div class="elegant-divider"></div>
    """, unsafe_allow_html=True)
    
    # Breadcrumb and notification row with better spacing
    brow_col1, brow_col2 = st.columns([11, 1])
    
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