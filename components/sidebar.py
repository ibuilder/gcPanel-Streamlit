import streamlit as st
from utils.module_loader import upload_module

def render_sidebar():
    """Render the application sidebar"""
    with st.sidebar:
        # Add Material Icons Link
        st.markdown("""
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        """, unsafe_allow_html=True)
        
        # Logo and title area
        st.markdown("""
        <div class="d-flex align-items-center p-3 mb-3 border-bottom">
            <div class="d-flex align-items-center justify-content-center rounded" 
                 style="width: 40px; height: 40px; margin-right: 15px; background-color: #1e3a8a;">
                <span class="material-icons" style="font-size: 24px; color: white;">construction</span>
            </div>
            <div>
                <h1 class="m-0 p-0" style="font-size: 22px; font-weight: 600; color: #1e3a8a;">gcPanel</h1>
                <p class="m-0 p-0" style="font-size: 12px; color: #64748b;">Construction Management</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # If we have current project, show project info at the top
        if 'current_project' in st.session_state:
            # Current project info card
            st.markdown(f"""
            <div style="margin-bottom: 20px; padding: 10px; border-radius: 4px; background-color: #e0f2fe; border-left: 4px solid #1e3a8a;">
                <div style="font-weight: 600; color: #1e3a8a;">{st.session_state.current_project}</div>
                <div style="font-size: 12px; color: #64748b;">Active Project</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Style for hiding buttons but keeping their functionality
        st.markdown("""
        <style>
        /* Hide button visually but maintain functionality */
        div[data-testid="element-container"] button.invisible-button {
            background-color: transparent;
            border: none;
            padding: 0;
            width: 1px;
            height: 1px;
            position: absolute;
            top: 0;
            left: 0;
            opacity: 0;
            pointer-events: none;
        }
        </style>
        """, unsafe_allow_html=True)
                    
        # Modern navigation with clean icons
        # Initialize menu if it doesn't exist
        if 'menu' not in st.session_state:
            st.session_state.menu = "Dashboard"
            
        # Main navigation items - single project focused
        nav_items = [
            {"id": "Dashboard", "icon": "dashboard", "label": "Dashboard"},
            {"id": "Project Information", "icon": "apartment", "label": "Project Information"},
            {"id": "Engineering", "icon": "engineering", "label": "Engineering"},
            {"id": "Field Operations", "icon": "construction", "label": "Field Operations"},
            {"id": "Safety", "icon": "health_and_safety", "label": "Safety"},
            {"id": "Contracts", "icon": "description", "label": "Contracts"},
            {"id": "Cost Management", "icon": "attach_money", "label": "Cost Management"},
            {"id": "BIM", "icon": "view_in_ar", "label": "BIM"},
            {"id": "Closeout", "icon": "task_alt", "label": "Closeout"},
            {"id": "Settings", "icon": "settings", "label": "Settings"}
        ]
        
        # Create navigation list
        st.markdown('<ul class="nav-list">', unsafe_allow_html=True)
        
        for item in nav_items:
            is_active = st.session_state.menu == item["id"]
            active_class = "active" if is_active else ""
            
            # Create the nav item with icon and label
            st.markdown(f"""
            <li>
                <div class="nav-item {active_class}" id="nav-{item['id']}">
                    <span class="nav-icon material-icons">{item['icon']}</span>
                    <span>{item['label']}</span>
                </div>
            </li>
            """, unsafe_allow_html=True)
            
            # Hidden button for handling navigation
            if st.button(item["label"], key=f"nav_btn_{item['id']}", help=f"Navigate to {item['label']}"):
                st.session_state.menu = item["id"]
                # Reset any module-specific state when changing menus
                if 'current_view' in st.session_state:
                    st.session_state.current_view = "list"
                st.rerun()
        
        # Add separator before settings/profile options
        st.markdown('<li><hr style="margin: 1rem 0; opacity: 0.2;"></li>', unsafe_allow_html=True)
        
        # Add Profile item
        profile_active = st.session_state.menu == "Profile"
        st.markdown(f"""
        <li>
            <div class="nav-item {profile_active}" id="nav-Profile">
                <span class="nav-icon material-icons">person</span>
                <span>Profile</span>
            </div>
        </li>
        """, unsafe_allow_html=True)
        
        if st.button("Profile", key="nav_btn_Profile", help="View your profile"):
            st.session_state.menu = "Profile"
            st.rerun()
        
        # Close the navigation list
        st.markdown('</ul>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Project selection at the bottom
        st.markdown('<h6 style="font-size: 0.85rem; color: #64748b; font-weight: 600; margin: 1rem 0 0.5rem 0;">PROJECT SELECTION</h6>', unsafe_allow_html=True)
        
        # List of projects - would normally come from a database
        projects = ["Highland Tower Development", "Riverfront Mall Renovation", "Metro Station Expansion"]
        
        # Project selector with clean styling
        selected_project = st.selectbox(
            "Select Project",
            projects,
            index=0 if 'current_project' not in st.session_state else projects.index(st.session_state.current_project),
            key="project_selector"
        )
        
        # Load project button
        if st.button("Switch Project", key="load_project_btn") or 'current_project' not in st.session_state:
            st.session_state.current_project = selected_project
            st.rerun()
            
        # Help and documentation
        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
        with st.expander("Help & Documentation"):
            st.markdown("[User Manual](#)")
            st.markdown("[API Documentation](#)")
            st.markdown("[Report Issue](#)")
        
        # Display version info
        st.caption("gcPanel v1.0.0")
        st.caption("© 2025 gcPanel Team")
