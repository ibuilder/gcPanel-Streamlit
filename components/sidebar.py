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
        
        # Project Selection
        project_col1, project_col2 = st.columns([3, 1])
        
        with project_col1:
            # In a real application, we would fetch projects from the database
            # For demonstration, we'll use a static list
            projects = ["Highland Tower Development", "Riverfront Mall Renovation", "Metro Station Expansion"]
            selected_project = st.selectbox(
                "Select Project",
                projects,
                index=0 if 'current_project' not in st.session_state else projects.index(st.session_state.current_project),
                key="project_selector",
                label_visibility="collapsed"
            )
        
        with project_col2:
            # Select button with improved styling - aligned with the dropdown
            if st.button("Load", key="load_project_btn") or 'current_project' not in st.session_state:
                st.session_state.current_project = selected_project
                st.rerun()
                
        # Project quick info with status indicators
        if 'current_project' in st.session_state:
            # Add some project metrics for quick reference
            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                st.markdown("""
                <div style="text-align: center; background-color: rgba(30, 136, 229, 0.1); padding: 8px; border-radius: 4px;">
                    <div style="font-size: 18px; font-weight: bold; color: #1e88e5;">42%</div>
                    <div style="font-size: 11px; color: #cccccc;">Complete</div>
                </div>
                """, unsafe_allow_html=True)
                
            with metrics_col2:
                st.markdown("""
                <div style="text-align: center; background-color: rgba(76, 175, 80, 0.1); padding: 8px; border-radius: 4px;">
                    <div style="font-size: 18px; font-weight: bold; color: #43a047;">$2.4M</div>
                    <div style="font-size: 11px; color: #cccccc;">Budget</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<hr style="margin: 0.5rem 0; border-color: rgba(255,255,255,0.1);">', unsafe_allow_html=True)
        
        # Module quick navigation
        st.markdown('<h3 style="color: #ffffff; font-size: 16px; margin-top: 0.5rem;">Quick Navigation</h3>', unsafe_allow_html=True)
        
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
            'folder': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>',
            'eye': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>',
            'camera': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>',
            'alert-triangle': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
            'file-minus': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="9" y1="15" x2="15" y2="15"></line></svg>',
            'home': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>',
            'git-branch': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="3" x2="6" y2="15"></line><circle cx="18" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle><path d="M18 9a9 9 0 0 1-9 9"></path></svg>'
        }

        # Create quick access buttons - uses flex layout for better organization
        st.markdown("""
        <div style="display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 10px;">
        """, unsafe_allow_html=True)
        
        # Most commonly used modules
        quick_access_modules = [
            {'section': 'engineering', 'module': 'submittals', 'icon': 'upload', 'label': 'Submittals'},
            {'section': 'engineering', 'module': 'rfi', 'icon': 'help-circle', 'label': 'RFIs'},
            {'section': 'field', 'module': 'daily_reports', 'icon': 'clipboard', 'label': 'Daily Reports'},
            {'section': 'cost', 'module': 'budget', 'icon': 'dollar-sign', 'label': 'Budget'}
        ]
        
        for i, module in enumerate(quick_access_modules):
            is_active = (st.session_state.get('current_section') == module['section'] and 
                         st.session_state.get('current_module') == module['module'])
            
            # Determine button style based on active state
            button_bg = "rgba(30, 136, 229, 0.2)" if is_active else "rgba(255, 255, 255, 0.05)"
            button_border = "1px solid #1e88e5" if is_active else "1px solid rgba(255, 255, 255, 0.1)"
            button_color = "#1e88e5" if is_active else "#ffffff"
            icon = icons.get(module['icon'], '')
            
            st.markdown(f"""
            <button id="quick_access_{i}" style="background-color: {button_bg}; border: {button_border}; border-radius: 4px; 
                    color: {button_color}; padding: 8px 12px; cursor: pointer; min-width: calc(50% - 5px); display: flex; 
                    align-items: center; justify-content: center; gap: 5px;">
                {icon} {module['label']}
            </button>
            """, unsafe_allow_html=True)
            
            # Hidden button to handle click
            col1, col2 = st.columns([1, 1])
            with col1 if i % 2 == 0 else col2:
                if st.button("", key=f"quick_{module['section']}_{module['module']}"):
                    st.session_state.current_section = module['section']
                    st.session_state.current_module = module['module']
                    st.session_state.current_view = "list"
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # List of modules by categories (direct selection without expanders)
        st.markdown('<h3 style="color: #ffffff; font-size: 16px; margin-top: 1rem;">All Modules</h3>', unsafe_allow_html=True)
        
        # Define categories with their modules
        module_categories = {
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
            'cost': {
                'display_name': 'Cost',
                'icon': 'dollar-sign',
                'modules': [
                    {'name': 'budget', 'display_name': 'Budget', 'icon': 'dollar-sign'},
                    {'name': 'change_orders', 'display_name': 'Change Orders', 'icon': 'git-branch'}
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
            'preconstruction': {
                'display_name': 'Preconstruction',
                'icon': 'building',
                'modules': [
                    {'name': 'bid_packages', 'display_name': 'Bid Packages', 'icon': 'package'},
                    {'name': 'qualified_bidders', 'display_name': 'Qualified Bidders', 'icon': 'users'}
                ]
            },
            'safety': {
                'display_name': 'Safety',
                'icon': 'shield',
                'modules': [
                    {'name': 'observations', 'display_name': 'Safety Observations', 'icon': 'eye'},
                    {'name': 'incidents', 'display_name': 'Incident Reports', 'icon': 'alert-triangle'}
                ]
            }
        }
        
        # Display each category with its modules
        for category_name, category_info in module_categories.items():
            # Category header with icon
            category_icon = icons.get(category_info['icon'], '')
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-top: 15px; margin-bottom: 5px; padding-bottom: 3px; border-bottom: 1px solid rgba(255,255,255,0.1);">
                {category_icon} <span style="margin-left: 5px; font-weight: 600; color: #ffffff;">{category_info['display_name']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Create columns for the modules (2 per row)
            modules_list = category_info['modules']
            rows = [modules_list[i:i+2] for i in range(0, len(modules_list), 2)]
            
            for row in rows:
                cols = st.columns(len(row))
                for i, module in enumerate(row):
                    with cols[i]:
                        module_icon = icons.get(module['icon'], '')
                        is_current = (category_name == st.session_state.get('current_section') and 
                                     module['name'] == st.session_state.get('current_module'))
                        
                        # Style based on current selection
                        bg_color = "rgba(30, 136, 229, 0.2)" if is_current else "rgba(255, 255, 255, 0.05)"
                        border = "1px solid #1e88e5" if is_current else "none"
                        
                        # Create module card
                        st.markdown(f"""
                        <div style="background-color: {bg_color}; border: {border}; border-radius: 4px; padding: 8px; 
                                cursor: pointer; margin-bottom: 5px;" id="module_card_{category_name}_{module['name']}">
                            <div style="display: flex; align-items: center;">
                                {module_icon} <span style="margin-left: 5px; color: #ffffff;">{module['display_name']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Hidden button for the click functionality
                        if st.button("", key=f"module_{category_name}_{module['name']}"):
                            st.session_state.current_section = category_name
                            st.session_state.current_module = module['name']
                            st.session_state.current_view = "list"
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
