"""
Header navigation component for the gcPanel application.

This component provides a horizontal header with logo, project info,
and navigation controls, replacing the traditional sidebar.
"""

import streamlit as st

def render_header_nav():
    """
    Render the main application header with navigation elements.
    
    This creates a horizontal header with:
    - Logo and project info on the left
    - Navigation dropdown and notifications on the right
    """
    
    # Create the header container
    with st.container():
        # Apply custom CSS for header styling
        st.markdown("""
        <style>
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background-color: white;
            border-bottom: 1px solid #DADCE0;
            margin: 0 0 1rem 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        /* Fix for Streamlit's extra space */
        .block-container {
            padding-top: 0 !important;
        }
        
        .header-left {
            display: flex;
            align-items: center;
        }
        
        .header-right {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .project-info {
            margin-left: 20px;
            border-left: 1px solid #DADCE0;
            padding-left: 20px;
        }
        
        .project-info h3 {
            margin: 0;
            font-size: 16px;
            font-weight: 600;
            color: #5F6368;
        }
        
        .project-info p {
            margin: 0;
            font-size: 14px;
            color: #3367D6;
            font-weight: 500;
        }
        
        .notification-btn-container {
            position: relative;
            display: inline-block;
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
        
        /* Override Streamlit's default selectbox styling */
        div[data-testid="stSelectbox"] {
            margin-bottom: 0 !important;
        }
        
        div[data-testid="stImage"] img {
            display: block;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create the header HTML
        header_html = """
        <div class="header-container">
            <div class="header-left">
                <div class="logo">
                    <img src="static/images/gcpanel-logo.svg" alt="gcPanel Logo" width="180">
                </div>
                <div class="project-info">
                    <h3>Project</h3>
                    <p>Highland Tower Development</p>
                </div>
            </div>
            <div class="header-right">
                <!-- Navigation will be inserted by Streamlit -->
                <div id="nav-placeholder"></div>
            </div>
        </div>
        
        <script>
            // Wait for Streamlit to load
            window.addEventListener('load', function() {
                // Move the navigation selectbox into the header
                const navElement = document.querySelector('div[data-testid="stSelectbox"]');
                const navPlaceholder = document.getElementById('nav-placeholder');
                if (navElement && navPlaceholder) {
                    navPlaceholder.appendChild(navElement);
                }
            });
        </script>
        """
        
        # Render the header
        st.markdown(header_html, unsafe_allow_html=True)
        
        # Create a hidden container for the navigation selectbox
        # It will be moved to the header via JavaScript
        with st.container():
            # Simple navigation using a selectbox
            menu_options = [
                "📊 Dashboard", 
                "📋 Project Information",
                "📅 Schedule",
                "⚠️ Safety",
                "📝 Contracts", 
                "💰 Cost Management",
                "🔧 Engineering",
                "🚧 Field Operations",
                "📄 Documents",
                "🏢 BIM Viewer",
                "✅ Closeout",
                "⚙️ Settings"
            ]
            
            # Mapping from display name to internal name
            menu_map = {
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
            current_display_menu = next((k for k, v in menu_map.items() if v == st.session_state.get("current_menu", "Dashboard")), menu_options[0])
            
            # Create the navigation dropdown
            selected = st.selectbox(
                "Select Module",
                menu_options,
                index=menu_options.index(current_display_menu),
                label_visibility="collapsed"
            )
            
            # Update state based on selection
            current_menu = menu_map[selected]
            if current_menu != st.session_state.get("current_menu"):
                st.session_state.current_menu = current_menu
                st.rerun()
        
        # Hidden button for notification center
        show_notifications = st.button("Notifications", key="header_notifications_btn")
        
        # Hide the actual button with CSS
        st.markdown("""
        <style>
            [data-testid="stButton"] {
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
        </style>
        """, unsafe_allow_html=True)
        
        # Handle notification click
        if show_notifications:
            st.session_state.show_notification_center = not st.session_state.get("show_notification_center", False)
            st.rerun()