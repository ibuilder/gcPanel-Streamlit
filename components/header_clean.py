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
        # Professional logo and project name with improved styling
        st.markdown("""
        <div style="display: flex; align-items: center; padding: 12px 0; background: linear-gradient(to right, #f8f9fa, #ffffff); 
                    border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="margin-right: 20px; cursor: pointer; transition: transform 0.2s ease;" 
                 onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'logo_clicked', value: true}, '*')"
                 onmouseover="this.style.transform='scale(1.02)'" 
                 onmouseout="this.style.transform='scale(1)'">
                <span style="font-size: 24px; font-weight: 700; letter-spacing: 0.3px; background: linear-gradient(45deg, #2c3e50, #4a6572); 
                             -webkit-background-clip: text; -webkit-text-fill-color: transparent; padding: 4px 10px;">
                    gc<span style="font-weight: 600;">Panel</span>
                </span>
            </div>
            <div style="border-left: 3px solid #4a6572; padding-left: 15px;">
                <div style="font-size: 12px; color: #4a6572; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500;">Project</div>
                <div style="font-size: 16px; font-weight: 600; color: #2c3e50;">Highland Tower Development</div>
                <div style="font-size: 12px; color: #64748b;">$45.5M • 168,500 sq ft • 15 Stories</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Handle logo click
        if st.session_state.get("logo_clicked", False):
            st.session_state.logo_clicked = False
            st.session_state.current_menu = "Dashboard"
            st.rerun()
    
    # No middle column in the new layout - removed to fix LSP error

    with col3:
        # Enhanced more prominent dropdown with improved styling and organization
        # Format options to include icons and grouped categories
        formatted_options = [f"{menu_options[k]['icon']} {menu_options[k]['label']}" for k in menu_options.keys()]
        
        # Create a mapping from formatted options back to keys
        option_to_key = {f"{menu_options[k]['icon']} {menu_options[k]['label']}": k for k in menu_options.keys()}
        
        # Find current menu's formatted option
        current_formatted = f"{menu_options[current_menu]['icon']} {menu_options[current_menu]['label']}"
        
        # Add a sleek, professional header for the navigation
        st.markdown("""
        <div style="text-align: center; padding: 8px 0; margin-top: 5px; 
                    background: linear-gradient(to right, #2c3e50, #4a6572); 
                    border-radius: 4px 4px 0 0; border: none;">
            <span style="font-size: 14px; color: #ffffff; font-weight: 500; letter-spacing: 0.5px; 
                   text-transform: uppercase;">
               Navigation
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Add custom CSS to improve dropdown appearance with more professional styling
        st.markdown("""
        <style>
        div[data-baseweb="select"] {
            border-radius: 0 0 4px 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            transition: all 0.2s ease;
            border: 1px solid #dfe1e5;
            background-color: #ffffff;
        }
        div[data-baseweb="select"]:hover {
            box-shadow: 0 2px 6px rgba(0,0,0,0.12);
        }
        div[data-baseweb="select"] > div {
            font-weight: 500;
            padding: 12px 16px;
            font-size: 15px;
            color: #333333;
        }
        div[data-baseweb="select"] svg {
            color: #4a6572 !important;
            width: 20px;
            height: 20px;
        }
        div[data-baseweb="menu"] {
            max-height: 450px !important;
            overflow-y: auto;
            border-radius: 4px;
            box-shadow: 0 3px 14px rgba(0,0,0,0.12);
            border: 1px solid #dfe1e5;
        }
        div[data-baseweb="menu"] ul {
            padding: 4px 0;
        }
        div[data-baseweb="menu"] li {
            padding: 10px 16px !important;
            font-size: 14px;
        }
        div[data-baseweb="menu"] li:hover {
            background-color: #f5f7fa !important;
        }
        
        /* Make logo and header more professional */
        .company-logo {
            filter: drop-shadow(0 1px 2px rgba(0,0,0,0.1));
        }
        </style>
        """, unsafe_allow_html=True)
        
        # More prominent dropdown
        selected_formatted = st.selectbox(
            "Navigation",
            options=formatted_options,
            index=formatted_options.index(current_formatted),
            key="header_nav_dropdown",
            label_visibility="collapsed"
        )
        
        # Convert selected formatted option back to key
        selected = option_to_key[selected_formatted]
        
        # Update session state if menu changed
        if selected != current_menu:
            st.session_state.current_menu = selected
            st.rerun()
    
    # Display a divider
    st.divider()
    
    # Breadcrumb and notification row
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