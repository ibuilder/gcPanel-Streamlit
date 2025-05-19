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
    
    # Create a more balanced three-column layout for the header with extra space for menu
    col1, col2, col3 = st.columns([4, 4, 3])
    
    with col1:
        # Enhanced logo and project name with improved spacing and shadow for better visibility
        st.markdown("""
        <div style="display: flex; align-items: center; padding: 10px 0;">
            <div style="margin-right: 18px; cursor: pointer; transition: transform 0.2s ease;" 
                 onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'logo_clicked', value: true}, '*')"
                 onmouseover="this.style.transform='scale(1.05)'" 
                 onmouseout="this.style.transform='scale(1)'">
                <span style="font-size: 26px; font-weight: 700; text-shadow: 0px 1px 2px rgba(0,0,0,0.1);">
                    🏗️ gc<span style="color: #3b82f6;">Panel</span>
                </span>
            </div>
            <div style="border-left: 3px solid #3b82f6; padding-left: 15px;">
                <div style="font-size: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">Project</div>
                <div style="font-size: 16px; font-weight: 600; color: #1f2937;">Highland Tower Development</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Handle logo click
        if st.session_state.get("logo_clicked", False):
            st.session_state.logo_clicked = False
            st.session_state.current_menu = "Dashboard"
            st.rerun()
    
    # Middle column for quick access buttons
    with col2:
        # Use Streamlit native components for quick access instead of HTML
        st.markdown("""
        <style>
        .quick-nav {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 10px;
        }
        .quick-nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 65px;
            text-decoration: none;
            color: #4b5563;
            transition: all 0.2s ease;
        }
        .quick-nav-item:hover {
            transform: translateY(-2px);
        }
        .quick-nav-icon {
            font-size: 22px;
            margin-bottom: 5px;
        }
        .quick-nav-label {
            font-size: 11px;
            text-align: center;
            color: #4b5563;
        }
        </style>
        <div class="quick-nav">
            <div class="quick-nav-item" id="quicknav_dashboard">
                <div class="quick-nav-icon">📊</div>
                <div class="quick-nav-label">Dashboard</div>
            </div>
            <div class="quick-nav-item" id="quicknav_docs">
                <div class="quick-nav-icon">📄</div>
                <div class="quick-nav-label">Documents</div>
            </div>
            <div class="quick-nav-item" id="quicknav_schedule">
                <div class="quick-nav-icon">📅</div>
                <div class="quick-nav-label">Schedule</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add actual buttons for proper interaction
        quick_nav_cols = st.columns(3)
        with quick_nav_cols[0]:
            if st.button("Dashboard", key="btn_dashboard", use_container_width=True, 
                          help="Go to Dashboard", type="secondary"):
                st.session_state.current_menu = "Dashboard"
                st.rerun()
        
        with quick_nav_cols[1]:
            if st.button("Documents", key="btn_docs", use_container_width=True, 
                          help="Go to Documents", type="secondary"):
                st.session_state.current_menu = "Documents"
                st.rerun()
                
        with quick_nav_cols[2]:
            if st.button("Schedule", key="btn_schedule", use_container_width=True, 
                          help="Go to Schedule", type="secondary"):
                st.session_state.current_menu = "Schedule"
                st.rerun()

        # Handle quick navigation clicks
        for quicknav in ['dashboard', 'docs', 'schedule']:
            if st.session_state.get(f"quicknav_{quicknav}", False):
                st.session_state[f"quicknav_{quicknav}"] = False
                if quicknav == 'dashboard':
                    st.session_state.current_menu = "Dashboard"
                elif quicknav == 'docs':
                    st.session_state.current_menu = "Documents"
                elif quicknav == 'schedule':
                    st.session_state.current_menu = "Schedule"
                st.rerun()

    with col3:
        # Enhanced right-aligned dropdown with improved styling and organization
        # Format options to include icons and grouped categories
        formatted_options = [f"{menu_options[k]['icon']} {menu_options[k]['label']}" for k in menu_options.keys()]
        
        # Create a mapping from formatted options back to keys
        option_to_key = {f"{menu_options[k]['icon']} {menu_options[k]['label']}": k for k in menu_options.keys()}
        
        # Find current menu's formatted option
        current_formatted = f"{menu_options[current_menu]['icon']} {menu_options[current_menu]['label']}"
        
        st.markdown("""
        <div style="text-align: right; padding-bottom: 5px; margin-top: 5px;">
            <span style="font-size: 14px; color: #6b7280; font-weight: 500; letter-spacing: 0.5px;">NAVIGATION</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Add custom CSS to improve dropdown appearance
        st.markdown("""
        <style>
        div[data-baseweb="select"] {
            border-radius: 8px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }
        div[data-baseweb="select"]:hover {
            box-shadow: 0 2px 5px rgba(0,0,0,0.15);
        }
        div[data-baseweb="select"] > div {
            font-weight: 500;
            padding: 5px 8px;
        }
        </style>
        """, unsafe_allow_html=True)
        
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