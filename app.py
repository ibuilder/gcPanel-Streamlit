"""
gcPanel Construction Management Dashboard

This is the main application file for the gcPanel Construction Management
Dashboard, a comprehensive project management tool for construction projects.
Featuring advanced modules for document management, BIM integration, and more.
"""

import streamlit as st
from utils.ui_manager import set_page_config
from app_manager import initialize_session_state, render_application

def local_css():
    """Apply custom CSS for theming"""
    # Load external CSS files
    css_files = [
        "static/css/main.css", 
        "static/css/notifications.css",
        "static/css/enhanced-theme.css",
        "static/css/optimized-ui.css",
        "static/css/console-fix.css",
        "static/css/buttons-fix.css",
        "static/css/action-buttons.css",
        "static/css/action-bar.css"
    ]
    
    for css_file in css_files:
        try:
            with open(css_file, "r") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading CSS file {css_file}: {e}")
    
    # Include Material Icons
    st.markdown("""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    # Include the Google Fonts for better typography
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    # Load JavaScript files
    js_files = [
        "static/js/notifications.js",
        "static/js/sidebar.js"
    ]
    
    for js_file in js_files:
        try:
            with open(js_file, "r") as f:
                st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading JavaScript file {js_file}: {e}")

def initialize_session_state():
    """Initialize session state variables."""
    if 'menu' not in st.session_state:
        st.session_state.menu = "Dashboard"
    
    if 'theme_color' not in st.session_state:
        st.session_state.theme_color = "#3e79f7"
    
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = "light"
    
    if 'current_project' not in st.session_state:
        st.session_state.current_project = "Highland Tower Development"
    
    if 'edit_project' not in st.session_state:
        st.session_state.edit_project = False

def main():
    """Main application entry point."""
    
    # Set page configuration with new favicon
    st.set_page_config(
        page_title="gcPanel Construction Dashboard",
        page_icon="static/images/favicon.svg",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    local_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Navigation is now handled by the sidebar component
    
    # Initialize database and authentication
    initialize_application()
    
    # Render the new header navigation instead of sidebar
    render_header_nav()
    
    # Main content area
    with st.container():
        # Get current menu selection
        current_menu = st.session_state.get("current_menu", "Dashboard")
        
        # Get breadcrumbs for current page
        breadcrumb_items = get_breadcrumbs_for_page(current_menu)
        
        # Create a header row with breadcrumbs and notification center
        header_col1, header_col2 = st.columns([7, 3])
        
        with header_col1:
            # Render breadcrumbs
            simple_breadcrumbs(breadcrumb_items)
        
        with header_col2:
            col_right_1, col_right_2 = st.columns([1, 1])
            
            with col_right_2:
                # Add notification center toggle button with styling
                st.markdown("""
                <style>
                    .notification-btn-container {
                        position: relative;
                        display: inline-block;
                        float: right;
                        margin-right: 10px;
                    }
                    .notification-btn {
                        background-color: #f8f9fa;
                        border: 1px solid #eef2f7;
                        border-radius: 6px;
                        padding: 8px 12px;
                        font-size: 14px;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        transition: all 0.2s ease;
                    }
                    .notification-btn:hover {
                        background-color: #eef2f7;
                    }
                    .notification-btn i {
                        font-size: 18px;
                        margin-right: 5px;
                    }
                    .notification-badge {
                        position: absolute;
                        top: -5px;
                        right: -5px;
                        background-color: #ff5b5b;
                        color: white;
                        border-radius: 50%;
                        width: 20px;
                        height: 20px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 12px;
                        font-weight: bold;
                        border: 2px solid white;
                    }
                </style>
                """, unsafe_allow_html=True)
                
                # Get the count of unread notifications
                unread_count = 0
                if "notifications" in st.session_state:
                    unread_count = sum(1 for n in st.session_state.get("notifications", []) if not n.get("read", False))
                
                # Notification button with badge
                badge_html = f'<div class="notification-badge">{unread_count}</div>' if unread_count > 0 else ''
                notification_btn_html = f"""
                <div class="notification-btn-container">
                    <button class="notification-btn" id="notification-btn" onclick="document.querySelector('[data-testid="stButton"] button').click();">
                        <i class="material-icons">notifications</i> Notifications
                    </button>
                    {badge_html}
                </div>
                <script>
                    // Wait for Streamlit to load
                    window.addEventListener('load', function() {{
                        // Get the notification button
                        const notificationBtn = document.getElementById('notification-btn');
                        
                        // Add click event listener
                        notificationBtn.addEventListener('click', function() {{
                            // Find the hidden Streamlit button and click it
                            const streamlitBtn = document.querySelector('[data-testid="stButton"] button');
                            if (streamlitBtn) {{
                                streamlitBtn.click();
                            }}
                        }});
                    }});
                </script>
                """
                st.markdown(notification_btn_html, unsafe_allow_html=True)
                
                # Hidden button that will be clicked by JavaScript
                show_notifications = st.button("Notifications", key="show_notifications_btn")
                
                # Hide the actual button with CSS
                st.markdown("""
                <style>
                    /* Only hide notification toggle button */
                    .stButton button[kind="secondary"] {
                        position: absolute;
                        width: 1px;
                        height: 1px;
                        padding: 0;
                        margin: -1px;
                        overflow: hidden;
                        clip: rect(0, 0, 0, 0);
                        white-space: nowrap;
                        border-width: 0;
                    }
                    
                    /* But make sure action buttons are visible */
                    .action-buttons-container .stButton button {
                        display: inline-flex !important;
                        visibility: visible !important;
                        position: relative !important;
                        width: auto !important;
                        height: auto !important;
                        padding: 0.5rem 1rem !important;
                        margin: 0 !important;
                        overflow: visible !important;
                        clip: auto !important;
                        white-space: nowrap !important;
                        border-width: 1px !important;
                    }
                </style>
                """, unsafe_allow_html=True)
                
                if show_notifications:
                    st.session_state.show_notification_center = not st.session_state.get("show_notification_center", False)
                    st.rerun()
            
            # Initialize notification center
            if st.session_state.get("show_notification_center", False):
                notification_center()
        
        # Define which pages should have Add/Edit buttons
        pages_with_actions = {
            "Project Information": "Information", 
            "Schedule": "Schedule Item",
            "Safety": "Safety Item",
            "Contracts": "Contract", 
            "Cost Management": "Cost Item",
            "Engineering": "Drawing",
            "Field Operations": "Field Item",
            "Documents": "Document",
            "Closeout": "Closeout Item"
        }
        
        # Add action bar if the current menu needs it
        if current_menu in pages_with_actions:
            page_type = pages_with_actions[current_menu]
            action_result = render_action_bar(page_type=page_type)
            
            # Store action results in session state if needed
            if action_result["add_clicked"] or action_result["edit_clicked"]:
                st.session_state[f"{current_menu.lower().replace(' ', '_')}_action"] = action_result
                st.rerun()
        
        # Render selected module
        if current_menu == "Dashboard":
            render_dashboard()
        elif current_menu == "Project Information":
            render_project_information()
        elif current_menu == "Engineering":
            render_engineering()
        elif current_menu == "Documents":
            render_documents()
        elif current_menu == "BIM":
            # Create tabs for different BIM viewer options
            bim_tab1, bim_tab2 = st.tabs(["Basic Viewer", "3D Viewer"])
            
            with bim_tab1:
                render_basic_bim_viewer()
            
            with bim_tab2:
                render_advanced_bim_viewer()
        elif current_menu == "Field Operations":
            render_field_operations()
        elif current_menu == "Safety":
            render_safety()
        elif current_menu == "Contracts":
            render_contracts()
        elif current_menu == "Cost Management":
            render_cost_management()
        elif current_menu == "Schedule":
            render_scheduling()
        # Roadmap functionality has been integrated into Schedule module
        elif current_menu == "Closeout":
            render_closeout()
        elif current_menu == "Settings":
            render_settings()
        else:
            st.error(f"Unknown menu: {current_menu}")
            
        # Render footer at the bottom of every page
        render_footer()

if __name__ == "__main__":
    main()