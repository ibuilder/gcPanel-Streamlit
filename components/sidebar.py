import streamlit as st
from utils.module_loader import upload_module

def render_sidebar():
    """Render the application sidebar"""
    with st.sidebar:
        # Load custom CSS
        try:
            with open('assets/custom.css', 'r') as f:
                custom_css = f.read()
                st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)
        except Exception:
            pass
            
        # Add Material Icons Link
        st.markdown("""
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        """, unsafe_allow_html=True)
        
        # Logo and title area with improved styling
        st.markdown("""
        <div style="display: flex; align-items: center; padding: 10px 0 20px 0;">
            <div style="font-size: 32px; margin-right: 10px;">🏗️</div>
            <div>
                <h1 style="margin: 0; padding: 0; color: #ffffff; font-size: 24px;">gcPanel</h1>
                <p style="margin: 0; padding: 0; color: #cccccc; font-size: 12px;">Construction Management</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Project Selection with better styling
        st.markdown('<div class="sidebar-section-title">Project Selection</div>', unsafe_allow_html=True)
        
        # Project selector - using two columns for better layout
        col1, col2 = st.columns([4, 1])
        
        # List of projects - would normally come from a database
        projects = ["Highland Tower Development", "Riverfront Mall Renovation", "Metro Station Expansion"]
        
        with col1:
            selected_project = st.selectbox(
                "Select Project",
                projects,
                index=0 if 'current_project' not in st.session_state else projects.index(st.session_state.current_project),
                key="project_selector",
                label_visibility="collapsed"
            )
        
        with col2:
            # CSS for load button styling
            st.markdown("""
            <style>
            div[data-testid="element-container"]:has(button#load_project_btn) {
                height: 38px !important;
                display: flex;
                align-items: center;
            }
            
            div[data-testid="element-container"]:has(button#load_project_btn) button {
                height: 38px !important;
                width: 100%;
                padding: 0 !important;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            </style>
            """, unsafe_allow_html=True)
            
            if st.button("Load", key="load_project_btn") or 'current_project' not in st.session_state:
                st.session_state.current_project = selected_project
                st.rerun()
        
        # Project Quick Metrics Grid
        if 'current_project' in st.session_state:
            # Current project info card
            st.markdown(f"""
            <div style="background-color: rgba(30, 136, 229, 0.1); padding: 10px; border-radius: 4px; 
                     margin-bottom: 15px; border-left: 3px solid #1e88e5;">
                <div style="font-weight: 600; color: white;">{st.session_state.current_project}</div>
                <div style="color: #aaa; font-size: 12px;">Active Project</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Project statistics in a 2-column grid
            proj_col1, proj_col2 = st.columns(2)
            with proj_col1:
                # Completion percentage
                st.markdown("""
                <div class="project-metric">
                    <div class="project-metric-title">Completion</div>
                    <div class="project-metric-value" style="color: #1e88e5;">42%</div>
                </div>
                
                <div class="project-metric">
                    <div class="project-metric-title">RFIs</div>
                    <div class="project-metric-value" style="color: #ff9800;">12</div>
                </div>
                """, unsafe_allow_html=True)
                
            with proj_col2:
                # Budget metrics
                st.markdown("""
                <div class="project-metric">
                    <div class="project-metric-title">Budget</div>
                    <div class="project-metric-value" style="color: #43a047;">$2.4M</div>
                </div>
                
                <div class="project-metric">
                    <div class="project-metric-title">Submittals</div>
                    <div class="project-metric-value" style="color: #9c27b0;">8</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Module quick navigation
        st.markdown('<div class="sidebar-section-title">Quick Access</div>', unsafe_allow_html=True)
        
        # Material icons styling for better visuals
        st.markdown("""
        <style>
        /* Fix button styling */
        div[data-testid="element-container"] button {
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
        
        # Create a grid of quick access buttons
        # Most commonly used modules
        quick_access_modules = [
            {'section': 'engineering', 'module': 'submittals', 'icon': 'upload', 'label': 'Submittals'},
            {'section': 'engineering', 'module': 'rfi', 'icon': 'help_outline', 'label': 'RFIs'},
            {'section': 'field', 'module': 'daily_reports', 'icon': 'description', 'label': 'Daily Reports'},
            {'section': 'cost', 'module': 'budget', 'icon': 'attach_money', 'label': 'Budget'}
        ]
        
        # Create 2x2 grid
        quick_col1, quick_col2 = st.columns(2)
        
        for i, module in enumerate(quick_access_modules):
            is_active = (st.session_state.get('current_section') == module['section'] and 
                         st.session_state.get('current_module') == module['module'])
            
            col = quick_col1 if i % 2 == 0 else quick_col2
            
            with col:
                # Define styling based on active state
                active_class = "active" if is_active else ""
                
                # Create the button with material icons
                st.markdown(f"""
                <div class="quick-access-btn {active_class}" id="quick-access-{i}">
                    <span class="material-icons">{module['icon']}</span>
                    <div>{module['label']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Hidden button that triggers the navigation
                if st.button("", key=f"quick_btn_{module['section']}_{module['name']}"):
                    st.session_state.current_section = module['section']
                    st.session_state.current_module = module['module']
                    st.session_state.current_view = "list"
                    st.rerun()
                    
        # Modules organized by category
        st.markdown('<div class="sidebar-section-title">Modules</div>', unsafe_allow_html=True)
        
        # Define categories with their modules
        module_categories = {
            'engineering': {
                'display_name': 'Engineering',
                'icon': 'engineering',
                'modules': [
                    {'name': 'rfi', 'display_name': 'RFIs', 'icon': 'help_outline'},
                    {'name': 'submittals', 'display_name': 'Submittals', 'icon': 'upload'},
                    {'name': 'file_explorer', 'display_name': 'Document Library', 'icon': 'folder'}
                ]
            },
            'field': {
                'display_name': 'Field',
                'icon': 'construction',
                'modules': [
                    {'name': 'daily_reports', 'display_name': 'Daily Reports', 'icon': 'description'},
                    {'name': 'photo_log', 'display_name': 'Photo Log', 'icon': 'photo_camera'}
                ]
            },
            'cost': {
                'display_name': 'Cost',
                'icon': 'attach_money',
                'modules': [
                    {'name': 'budget', 'display_name': 'Budget', 'icon': 'account_balance_wallet'},
                    {'name': 'change_orders', 'display_name': 'Change Orders', 'icon': 'swap_horiz'}
                ]
            },
            'contracts': {
                'display_name': 'Contracts',
                'icon': 'description',
                'modules': [
                    {'name': 'prime_contract', 'display_name': 'Prime Contract', 'icon': 'gavel'},
                    {'name': 'subcontracts', 'display_name': 'Subcontracts', 'icon': 'groups'}
                ]
            },
            'preconstruction': {
                'display_name': 'Preconstruction',
                'icon': 'domain',
                'modules': [
                    {'name': 'bid_packages', 'display_name': 'Bid Packages', 'icon': 'inventory_2'},
                    {'name': 'qualified_bidders', 'display_name': 'Qualified Bidders', 'icon': 'people'}
                ]
            },
            'safety': {
                'display_name': 'Safety',
                'icon': 'health_and_safety',
                'modules': [
                    {'name': 'observations', 'display_name': 'Safety Observations', 'icon': 'visibility'},
                    {'name': 'incidents', 'display_name': 'Incident Reports', 'icon': 'warning'}
                ]
            }
        }
        
        # Create an accordion for the modules
        for category_name, category_info in module_categories.items():
            is_current_category = category_name == st.session_state.get('current_section')
            
            # Create the category header
            st.markdown(f"""
            <div class="module-category" style="margin-bottom: 5px; cursor: pointer;" id="category-{category_name}">
                <div style="display: flex; align-items: center; justify-content: space-between; 
                         padding: 8px; border-radius: 4px; background-color: {'rgba(30, 136, 229, 0.2)' if is_current_category else 'rgba(255, 255, 255, 0.05)'};">
                    <div style="display: flex; align-items: center;">
                        <span class="material-icons" style="margin-right: 8px;">{category_info['icon']}</span>
                        <span style="font-weight: 500;">{category_info['display_name']}</span>
                    </div>
                    <span class="material-icons">{'expand_less' if is_current_category else 'expand_more'}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display the modules for this category
            if is_current_category:
                st.markdown(f"""
                <div style="margin-left: 10px; margin-bottom: 10px;" id="modules-{category_name}">
                """, unsafe_allow_html=True)
                
                for module in category_info['modules']:
                    is_current_module = (is_current_category and 
                                         module['name'] == st.session_state.get('current_module'))
                    
                    # Module item with material icon
                    st.markdown(f"""
                    <div class="module-card {('active' if is_current_module else '')}" 
                         id="module-{category_name}-{module['name']}">
                        <span class="material-icons module-card-icon">{module['icon']}</span>
                        {module['display_name']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Hidden button for navigation
                    if st.button("", key=f"module_btn_{category_name}_{module['name']}"):
                        st.session_state.current_section = category_name
                        st.session_state.current_module = module['name'] 
                        st.session_state.current_view = "list"
                        st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Category toggle button
            if st.button("", key=f"category_toggle_{category_name}"):
                if is_current_category:
                    # Already open, do nothing (let the module buttons work)
                    pass
                else:
                    # Open this category
                    st.session_state.current_section = category_name
                    # Select the first module by default
                    st.session_state.current_module = category_info['modules'][0]['name']
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
