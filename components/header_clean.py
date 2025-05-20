"""
Professional header component for gcPanel.

A clean, modern header implemented with pure Python Streamlit components.
All CSS styling has been moved to static/css/header_styles.css for better
maintainability and performance.
"""

import streamlit as st
from utils.style_manager import load_css

def render_header():
    """
    Render a clean, modern header using only Streamlit components.
    All styling is now loaded from the external CSS file.
    """
    # Load CSS styling from external file
    load_css("header_styles.css")
    
    # Add a container class for the header - now using updated CSS class
    st.markdown('<div class="gc-header-container">', unsafe_allow_html=True)
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
    
    # Check if we're on mobile based on screen width (using JavaScript)
    st.markdown("""
    <script>
    // Add a class to the body based on screen width
    if (window.innerWidth <= 768) {
        document.body.classList.add('is-mobile');
    } else {
        document.body.classList.remove('is-mobile');
    }
    </script>
    """, unsafe_allow_html=True)
    
    # More readable column layout with better proportions
    col1, col3 = st.columns([6, 4], gap="small")
    
    with col1:
        # Use Streamlit's native components instead of HTML with event handlers
        logo_col, info_col = st.columns([1, 3])
        
        with logo_col:
            # Logo with styling from CSS
            if st.button("🏗️ gcPanel", key="logo_button", use_container_width=True, 
                      help="Return to dashboard"):
                st.session_state.logo_clicked = True
                st.rerun()
                
        with info_col:
            # Project info with consistent styling from CSS file
            st.markdown("""
            <div class="gc-project-info">
                <div class="gc-project-label">Project</div>
                <div class="gc-project-title">Highland Tower Development</div>
                <div class="gc-project-stats">$45.5M • 168,500 sq ft • 15 Stories</div>
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
    
    # Content area is now styled through CSS classes
    st.markdown('<div class="gc-content-container">', unsafe_allow_html=True)
    
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