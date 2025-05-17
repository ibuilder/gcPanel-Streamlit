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
        
        # Logo and title area with professional styling
        st.markdown("""
        <div style="display: flex; align-items: center; padding: 10px 0 20px 0; margin-bottom: 10px; border-bottom: 1px solid var(--divider-color);">
            <div style="display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; 
                      background-color: var(--primary-color); border-radius: 8px; margin-right: 15px;">
                <span class="material-icons" style="font-size: 24px; color: white;">construction</span>
            </div>
            <div>
                <h1 style="margin: 0; padding: 0; color: var(--text-primary); font-size: 22px; font-weight: 600;">gcPanel</h1>
                <p style="margin: 0; padding: 0; color: var(--text-secondary); font-size: 12px;">Construction Management</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Project Selection with modern styling
        st.markdown("""
        <div style="background-color: rgba(255,255,255,0.05); padding: 16px; border-radius: 12px; margin-bottom: 20px; 
                  border: 1px solid var(--divider-color); box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <span class="material-icons" style="color: var(--primary-color); margin-right: 8px; font-size: 20px;">apartment</span>
                <span style="font-weight: 500; color: var(--text-primary); font-size: 16px;">Project Selection</span>
            </div>
        """, unsafe_allow_html=True)
        
        # List of projects - would normally come from a database
        projects = ["Highland Tower Development", "Riverfront Mall Renovation", "Metro Station Expansion"]
        
        # Project selector with better styling
        selected_project = st.selectbox(
            "Select Project",
            projects,
            index=0 if 'current_project' not in st.session_state else projects.index(st.session_state.current_project),
            key="project_selector",
            label_visibility="collapsed"
        )
        
        # Load project button with better styling
        col1, col2 = st.columns([3, 1])
        with col2:
            # Use primary button style
            if st.button("Load", key="load_project_btn", type="primary") or 'current_project' not in st.session_state:
                st.session_state.current_project = selected_project
                st.rerun()
                
        # Close the project card container
        st.markdown('</div>', unsafe_allow_html=True)
        
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
            
            # Create a modern nav item for the category
            st.markdown(f"""
            <div class="sidebar-nav-item {('active' if is_current_category else '')}" id="category-{category_name}">
                <span class="material-icons">{category_info['icon']}</span>
                <span style="flex: 1;">{category_info['display_name']}</span>
                <span class="material-icons">{'expand_less' if is_current_category else 'expand_more'}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Hidden button for category click handling
            if st.button(
                "",
                key=f"category_btn_{category_name}",
                help=f"Toggle {category_info['display_name']}"
            ):
                # Toggle the category
                if is_current_category:
                    # Already open, do nothing
                    pass
                else:
                    # Open this category
                    st.session_state.current_section = category_name
                    # Select the first module by default
                    st.session_state.current_module = category_info['modules'][0]['name']
                    st.session_state.current_view = "list"
                    st.rerun()
            
            # Display the modules for this category
            if is_current_category:
                st.markdown(f"""
                <div style="margin-left: 10px; margin-bottom: 10px;" id="modules-{category_name}">
                """, unsafe_allow_html=True)
                
                for module in category_info['modules']:
                    is_current_module = (is_current_category and 
                                         module['name'] == st.session_state.get('current_module'))
                    
                    # Modern module button with proper styling
                    st.markdown(f"""
                    <div class="sidebar-nav-item {('active' if is_current_module else '')}"
                        style="margin-left: 15px;" id="module-{category_name}-{module['name']}">
                        <span class="material-icons" style="font-size: 18px;">{module['icon']}</span>
                        <span style="flex: 1;">{module['display_name']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Hidden button for functional behavior
                    if st.button(
                        "",
                        key=f"module_btn_{category_name}_{module['name']}",
                        help=f"Open {module['display_name']}"
                    ):
                        st.session_state.current_section = category_name
                        st.session_state.current_module = module['name'] 
                        st.session_state.current_view = "list"
                        st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Category toggle button with proper text
            button_container = st.container()
            button_container.markdown('<div style="height: 0; visibility: hidden;">.</div>', unsafe_allow_html=True)
            if button_container.button(category_info['display_name'], key=f"category_toggle_{category_name}"):
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
        
        # End of sidebar - clean margin at the bottom
        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Help and documentation
        with st.expander("Help & Documentation"):
            st.markdown("[User Manual](#)")
            st.markdown("[API Documentation](#)")
            st.markdown("[Report Issue](#)")
        
        # Display version info
        st.caption("gcPanel v1.0.0")
        st.caption("© 2023 gcPanel Team")
