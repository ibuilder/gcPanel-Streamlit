"""
Modular Header Component for gcPanel

This component provides a modular navigation header that works
with the new module loader system for better independence.
"""

import streamlit as st
from modules.module_loader import get_modules_by_category


def render_header(modules, current_module):
    """
    Render the application header with navigation menu.
    
    Args:
        modules (dict): Dictionary of available modules
        current_module (str): The currently selected module
    """
    # Apply header styling
    st.markdown("""
    <style>
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid #f0f0f0;
    }
    .header-logo {
        display: flex;
        align-items: center;
    }
    .header-logo img {
        height: 40px;
        margin-right: 10px;
    }
    .header-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
    }
    .header-project {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
    }
    .header-actions {
        display: flex;
        align-items: center;
    }
    .nav-container {
        margin-bottom: 20px;
    }
    .nav-button {
        text-align: left;
        padding: 8px 16px;
        margin-bottom: 5px;
        transition: all 0.2s ease;
        border-radius: 4px;
    }
    .nav-button:hover {
        background-color: #f5f5f5;
    }
    .nav-button.active {
        background-color: #e6f0fd;
        color: #1a73e8;
        font-weight: 500;
    }
    .nav-category {
        font-size: 0.8rem;
        font-weight: 600;
        color: #666;
        margin: 15px 0 5px 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
    """,
                unsafe_allow_html=True)

    # Header layout
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            # Logo and title
            st.markdown("""
                <div class="header-logo">
                    <img src="https://raw.githubusercontent.com/streamlit/streamlit/develop/app/client/static/favicon.png" alt="gcPanel Logo">
                    <div>
                        <div class="header-project">Highland Tower Development</div><div class="header-title">gcPanel</div>
                    </div>
                </div>
                """,
                        unsafe_allow_html=True)

        with col3:
            # User menu and notifications
            st.markdown("""
                <div class="header-actions">
                    <span class="material-icons" style="cursor: pointer; margin-right: 15px; color: #666;">
                        notifications
                    </span>
                    <span class="material-icons" style="cursor: pointer; color: #666;">
                        account_circle
                    </span>
                </div>
                """,
                        unsafe_allow_html=True)

    # Navigation sidebar
    with st.sidebar:
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)

        # Get modules organized by category
        categories = get_modules_by_category()

        # Sort categories to ensure Main is first
        sorted_categories = sorted(categories.items(),
                                   key=lambda x: 0 if x[0] == "Main" else 1)

        # Render navigation items by category
        for category, module_list in sorted_categories:
            # Show category header except for Main category
            if category != "Main":
                st.markdown(f'<div class="nav-category">{category}</div>',
                            unsafe_allow_html=True)

            # Create navigation buttons for each module in this category
            for module in module_list:
                module_id = module["id"]
                module_name = module["name"]

                # Determine if this is the active module
                is_active = module_id == current_module
                active_class = "active" if is_active else ""

                # Create clickable navigation item
                if st.markdown(f"""
                    <div class="nav-button {active_class}" 
                         onclick="handleNavClick('{module_id}')" 
                         data-module="{module_id}">
                        {module_name}
                    </div>
                    """,
                               unsafe_allow_html=True):
                    # This is fallback behavior if the JS click doesn't work
                    st.session_state.current_module = module_id
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # Add JavaScript for navigation click handling
        st.markdown("""
            <script>
            function handleNavClick(moduleId) {
                // Send a message to update the current_module in session state
                window.parent.postMessage({
                    type: "streamlit:setSessionState",
                    key: "current_module",
                    value: moduleId
                }, "*");
                
                // Force page refresh
                setTimeout(() => {
                    window.parent.postMessage({
                        type: "streamlit:forceRerun"
                    }, "*");
                }, 100);
            }
            
            // Add click event listeners to nav buttons using proper event handling
            document.addEventListener("DOMContentLoaded", function() {
                const navButtons = document.querySelectorAll(".nav-button");
                navButtons.forEach(function(button) {
                    button.addEventListener("click", function(e) {
                        const moduleId = this.getAttribute("data-module");
                        if (moduleId) {
                            handleNavClick(moduleId);
                        }
                    });
                });
            });
            </script>
            """,
                    unsafe_allow_html=True)
