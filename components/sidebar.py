import streamlit as st
from utils.module_loader import upload_module

def render_sidebar():
    """Render the application sidebar"""
    with st.sidebar:
        # Logo and title area
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown('<div style="display: flex; justify-content: center; align-items: center; height: 50px;"><span style="font-size: 30px; color: #ffffff;">🏗️</span></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<h1 style="margin: 0; padding: 0; color: #ffffff; font-size: 24px;">gcPanel</h1>', unsafe_allow_html=True)
            st.markdown('<p style="margin: 0; padding: 0; color: #cccccc; font-size: 12px;">Construction Management</p>', unsafe_allow_html=True)
        
        st.markdown('<hr style="margin: 0.5rem 0; border-color: rgba(255,255,255,0.1);">', unsafe_allow_html=True)
        
        # Project selection
        st.markdown('<h3 style="color: #ffffff; font-size: 16px; margin-top: 1rem;">Project Selection</h3>', unsafe_allow_html=True)
        
        # In a real application, we would fetch projects from the database
        # For demonstration, we'll use a static list
        projects = ["Highland Tower Development", "Riverfront Mall Renovation", "Metro Station Expansion"]
        selected_project = st.selectbox(
            "Select Project",
            projects,
            index=0 if 'current_project' not in st.session_state else projects.index(st.session_state.current_project),
            key="project_selector"
        )
        
        # Select button with improved styling
        if st.button("Load Project", key="load_project_btn") or 'current_project' not in st.session_state:
            st.session_state.current_project = selected_project
            st.rerun()
            
        # Project quick info
        if 'current_project' in st.session_state:
            st.markdown(f"""
            <div style="background-color: rgba(255,255,255,0.05); padding: 8px; border-radius: 4px; margin-top: 10px;">
                <p style="color: #ffffff; margin: 0; font-weight: bold;">{st.session_state.current_project}</p>
                <p style="color: #cccccc; margin: 0; font-size: 12px;">Status: Active</p>
                <p style="color: #cccccc; margin: 0; font-size: 12px;">Completion: 42%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Module navigation
        st.markdown('<h3 style="color: #ffffff; font-size: 16px; margin-top: 0.5rem;">Modules</h3>', unsafe_allow_html=True)
        
        # Icons for the modules (feather icons SVG codes)
        icons = {
            'building': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>',
            'clipboard': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>',
            'hard-hat': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"></path><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"></path><path d="M4 15v-3a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v3"></path></svg>',
            'shield': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
            'file-text': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>',
            'dollar-sign': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>',
            '3d-model': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2"></polygon><line x1="12" y1="22" x2="12" y2="15.5"></line><polyline points="22 8.5 12 15.5 2 8.5"></polyline></svg>',
            'check-circle': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
            'database': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg>',
            'settings': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>',
            'bar-chart-2': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>',
            'package': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"></line><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>',
            'users': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>',
            'help-circle': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
            'upload': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>',
            'folder': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>'
        }
        
        # Define default modules to show in sidebar
        default_modules = {
            'preconstruction': {
                'display_name': 'Preconstruction',
                'icon': 'building',
                'modules': [
                    {'name': 'bid_packages', 'display_name': 'Bid Packages', 'icon': 'package'},
                    {'name': 'qualified_bidders', 'display_name': 'Qualified Bidders', 'icon': 'users'}
                ]
            },
            'engineering': {
                'display_name': 'Engineering',
                'icon': 'clipboard',
                'modules': [
                    {'name': 'rfi', 'display_name': 'RFIs', 'icon': 'help-circle'},
                    {'name': 'submittals', 'display_name': 'Submittals', 'icon': 'upload'},
                    {'name': 'file_explorer', 'display_name': 'Document Library', 'icon': 'folder'}
                ]
            },
            'field': {
                'display_name': 'Field',
                'icon': 'hard-hat',
                'modules': [
                    {'name': 'daily_reports', 'display_name': 'Daily Reports', 'icon': 'clipboard'},
                    {'name': 'photo_log', 'display_name': 'Photo Log', 'icon': 'camera'}
                ]
            },
            'safety': {
                'display_name': 'Safety',
                'icon': 'shield',
                'modules': [
                    {'name': 'observations', 'display_name': 'Safety Observations', 'icon': 'eye'},
                    {'name': 'incidents', 'display_name': 'Incident Reports', 'icon': 'alert-triangle'}
                ]
            },
            'contracts': {
                'display_name': 'Contracts',
                'icon': 'file-text',
                'modules': [
                    {'name': 'prime_contract', 'display_name': 'Prime Contract', 'icon': 'file-text'},
                    {'name': 'subcontracts', 'display_name': 'Subcontracts', 'icon': 'file-minus'}
                ]
            },
            'cost': {
                'display_name': 'Cost',
                'icon': 'dollar-sign',
                'modules': [
                    {'name': 'budget', 'display_name': 'Budget', 'icon': 'dollar-sign'},
                    {'name': 'change_orders', 'display_name': 'Change Orders', 'icon': 'git-branch'}
                ]
            }
        }
        
        # Try to get modules from session state, fall back to default modules
        modules = st.session_state.get('modules', default_modules)
        if not modules:
            modules = default_modules
        
        # Display sections as expanders with icons
        for section_name, section_info in modules.items():
            section_icon = icons.get(section_info['icon'], '')
            is_current = st.session_state.get('current_section') == section_name
            
            expander_label = f"{section_icon} {section_info['display_name']}"
            
            # Create a styled expander header
            if is_current:
                expander_style = "background-color: rgba(30, 136, 229, 0.2); border-left: 3px solid #1e88e5;"
            else:
                expander_style = "background-color: rgba(255, 255, 255, 0.05);"
                
            with st.expander(section_info['display_name'], expanded=is_current):
                # Display modules as buttons
                for module in section_info['modules']:
                    module_icon = icons.get(module['icon'], '')
                    is_current_module = is_current and st.session_state.get('current_module') == module['name']
                    
                    # Style the button based on whether it's the active module
                    if is_current_module:
                        button_style = "color: #1e88e5; font-weight: bold;"
                        prefix = "• "
                    else:
                        button_style = "color: #ffffff;"
                        prefix = ""
                        
                    # Create a styled button using markdown
                    module_html = f"""
                    <div style="cursor: pointer; padding: 4px 10px; margin: 2px 0; border-radius: 4px; {button_style}" 
                         id="module_{section_name}_{module['name']}_btn">
                        {module_icon} {prefix}{module['display_name']}
                    </div>
                    """
                    
                    # Use a container for the clickable area
                    module_container = st.container()
                    module_container.markdown(module_html, unsafe_allow_html=True)
                    
                    # Handle click with a small empty button
                    if st.button("", key=f"module_{section_name}_{module['name']}", 
                                  help=f"Open {module['display_name']}",
                                  style={"display": "none"}):  # Hidden button
                        st.session_state.current_section = section_name
                        st.session_state.current_module = module['name']
                        st.session_state.current_view = "list"  # Default to list view
                        st.rerun()
        
        st.markdown("---")
        
        # Administrator tools
        if st.session_state.get('user_role') == 'administrator':
            st.subheader("Administrator Tools")
            
            # Module upload
            with st.expander("Upload Module"):
                uploaded_file = st.file_uploader("Select Module ZIP file", type="zip")
                
                if uploaded_file is not None and st.button("Install Module"):
                    success, message = upload_module(uploaded_file)
                    if success:
                        st.success(message)
                        # Reload modules
                        st.session_state.modules = None
                        st.rerun()
                    else:
                        st.error(message)
            
            # User management (link to module)
            if st.button("User Management"):
                st.session_state.current_section = "settings"
                st.session_state.current_module = "user_management"
                st.session_state.current_view = "list"
                st.rerun()
            
            # Database settings (link to module)
            if st.button("Database Settings"):
                st.session_state.current_section = "settings"
                st.session_state.current_module = "database_settings"
                st.session_state.current_view = "list"
                st.rerun()
        
        st.markdown("---")
        
        # Help and documentation
        with st.expander("Help & Documentation"):
            st.markdown("[User Manual](#)")
            st.markdown("[API Documentation](#)")
            st.markdown("[Report Issue](#)")
        
        # Display version info
        st.caption("gcPanel v1.0.0")
        st.caption("© 2023 gcPanel Team")
