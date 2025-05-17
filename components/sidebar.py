"""
Sidebar navigation component for the gcPanel Construction Management Dashboard.

This module provides the navigation sidebar with project selection.
"""

import streamlit as st
from assets.styles import get_icon_svg

def navigate_to(menu_item):
    """
    Navigate to a menu item.
    
    Args:
        menu_item: The menu item to navigate to
    """
    st.session_state.menu = menu_item
    
    # Clear any sub-state depending on navigation
    if menu_item == "Dashboard":
        if "selected_project_id" in st.session_state:
            del st.session_state.selected_project_id
    
    # Force rerender
    st.rerun()

def render_sidebar():
    """
    Render the sidebar navigation.
    """
    with st.sidebar:
        # Application title and logo
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="font-size: 1.5rem; font-weight: 600; color: #3e79f7; margin-left: 0.5rem;">
                    🏗️ gcPanel
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # User info
        st.markdown(
            """
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem; 
                       background-color: rgba(62, 121, 247, 0.05); padding: 0.7rem; 
                       border-radius: 6px;">
                <div style="width: 40px; height: 40px; border-radius: 50%; 
                           background-color: #3e79f7; color: white; display: flex; 
                           justify-content: center; align-items: center; 
                           font-weight: 600; margin-right: 0.5rem;">
                    A
                </div>
                <div>
                    <div style="font-weight: 500;">Admin User</div>
                    <div style="font-size: 0.8rem; color: #6c757d;">Role: Administrator</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Navigation
        st.markdown("<div style='font-size: 0.8rem; text-transform: uppercase; color: #6c757d; margin-bottom: 0.5rem;'>Navigation</div>", unsafe_allow_html=True)
        
        # Menu items
        menu_items = [
            {"label": "Dashboard", "icon": "dashboard"},
            {"label": "Project Information", "icon": "apartment"},
            {"label": "Documents", "icon": "description"},
            {"label": "BIM", "icon": "view_in_ar"},
            {"label": "Engineering", "icon": "engineering"},
            {"label": "Field Operations", "icon": "construction"},
            {"label": "Safety", "icon": "health_and_safety"},
            {"label": "Contracts", "icon": "handshake"},
            {"label": "Cost Management", "icon": "paid"},
            {"label": "Closeout", "icon": "task_alt"},
            {"label": "Settings", "icon": "settings"}
        ]
        
        for item in menu_items:
            is_active = st.session_state.menu == item["label"]
            active_class = "active" if is_active else ""
            
            st.markdown(
                f"""
                <div class="nav-item {active_class}" 
                     onclick="parent.postMessage({{key: 'nav_to', value: '{item["label"]}'}}, '*')">
                    <span class="nav-icon material-icons">{item["icon"]}</span>
                    {item["label"]}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Handle navigation clicks
            if f"nav_to_{item['label']}" not in st.session_state:
                st.session_state[f"nav_to_{item['label']}"] = False
                
            # JavaScript to handle navigation
            st.markdown(
                """
                <script>
                window.addEventListener('message', function(e) {
                    if (e.data.key === 'nav_to') {
                        const data = {
                            nav_to: e.data.value
                        };
                        
                        // Send data to Streamlit
                        window.parent.postMessage({
                            type: 'streamlit:setComponentValue',
                            value: data
                        }, '*');
                    }
                });
                </script>
                """,
                unsafe_allow_html=True
            )
        
        # Project selection
        st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.8rem; text-transform: uppercase; color: #6c757d; margin-bottom: 0.5rem;'>Current Project</div>", unsafe_allow_html=True)
        
        # Show current project with icon
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; padding: 0.7rem; 
                      background-color: rgba(62, 121, 247, 0.05); border-radius: 6px;">
                <span class="material-icons" style="margin-right: 0.5rem; color: #3e79f7;">apartment</span>
                <div style="font-weight: 500; color: #2c3e50;">{st.session_state.current_project}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Version info
        st.markdown(
            """
            <div style="position: fixed; bottom: 0; left: 0; width: 100%; 
                      padding: 0.5rem 1rem; font-size: 0.7rem; color: #6c757d; 
                      background-color: rgba(255, 255, 255, 0.7); text-align: center;">
                gcPanel v1.0.0 © 2025
            </div>
            """,
            unsafe_allow_html=True
        )