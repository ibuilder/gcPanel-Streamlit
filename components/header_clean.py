"""
Clean header component for gcPanel.

This component provides a fixed header with navigation positioned
exactly as required - in the white header area aligned to the right.
"""

import streamlit as st

def render_header():
    """
    Render a professional header with centered logo, project info, and navigation.
    """
    # CSS is now loaded from external file in ui_manager.py
    
    # Menu options with icons
    menu_options = {
        "📊 Dashboard": "Dashboard", 
        "📋 Project Information": "Project Information",
        "📅 Schedule": "Schedule",
        "⚠️ Safety": "Safety",
        "📝 Contracts": "Contracts", 
        "💰 Cost Management": "Cost Management",
        "🔧 Engineering": "Engineering",
        "🚧 Field Operations": "Field Operations",
        "📄 Documents": "Documents",
        "🏢 BIM Viewer": "BIM",
        "✅ Closeout": "Closeout",
        "⚙️ Settings": "Settings"
    }
    
    # Get currently selected menu value from session state
    current_menu = st.session_state.get("current_menu", "Dashboard")
    
    # Get icon for current menu
    current_icon = ""
    for k, v in menu_options.items():
        if v == current_menu:
            current_icon = k.split(" ")[0]
            break
    
    # Create main header container
    st.markdown("""
    <div class="pro-header-container">
        <div class="pro-header-left">
            <div class="pro-project-label">Project</div>
            <div class="pro-project-name">Highland Tower Development</div>
        </div>
        
        <div class="pro-header-center">
            <div class="pro-logo">gc<span class="pro-logo-highlight">Panel</span></div>
        </div>
        
        <div class="pro-header-right">
            <div class="pro-menu-selected">
                <span class="pro-menu-icon">{}</span>
                <span class="pro-menu-text">{}</span>
                <span class="pro-menu-arrow">▼</span>
            </div>
        </div>
    </div>
    """.format(current_icon, current_menu), unsafe_allow_html=True)
    
    # Navigation dropdown (hidden but functional)
    # Add a CSS class to help target this specific dropdown
    st.markdown("""
    <style>
    /* Target this specific dropdown */
    div[data-testid="stSelectbox"]:has(select#header_nav_dropdown) {
        position: absolute !important;
        opacity: 0 !important;
        width: 200px !important;
        height: 50px !important;
        z-index: 5 !important;
        right: 24px !important;
        top: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 3])
    with col3:
        selected = st.selectbox(
            "Navigation",
            options=list(menu_options.keys()),
            index=list(menu_options.values()).index(current_menu),
            label_visibility="collapsed",
            key="header_nav_dropdown",
        )
        
        # Update the session state when a new menu item is selected
        if menu_options[selected] != current_menu:
            st.session_state.current_menu = menu_options[selected]
            st.rerun()
    
    # Secondary navigation bar with breadcrumbs
    st.markdown(f"""
    <div class="pro-secondary-nav">
        <div class="pro-breadcrumbs">
            <a href="#" class="pro-breadcrumb-item">Home</a>
            <span class="pro-breadcrumb-separator">›</span>
            <span class="pro-breadcrumb-current">{current_menu}</span>
        </div>
        <div class="pro-notification-area">
            <span class="pro-notification-icon">🔔</span>
            <span class="pro-notification-badge">3</span>
        </div>
    </div>
    """, unsafe_allow_html=True)