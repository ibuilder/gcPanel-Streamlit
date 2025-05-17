import streamlit as st
import os
import importlib
from components.header import render_header
from components.navigation import render_navigation
from components.sidebar import render_sidebar
from components.footer import render_footer
from utils.auth import check_authentication, initialize_auth
from utils.database import initialize_db
from utils.module_loader import load_modules
from assets.styles import apply_styles

# App configuration
st.set_page_config(
    page_title="gcPanel - Construction Management Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles
apply_styles()

# Initialize authentication
initialize_auth()

# Initialize database connection
initialize_db()

# Initialize session state variables if they don't exist
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'current_section' not in st.session_state:
    st.session_state.current_section = None
if 'current_module' not in st.session_state:
    st.session_state.current_module = None
if 'current_view' not in st.session_state:
    st.session_state.current_view = "list"  # Default view (list, view, form)
if 'modules' not in st.session_state:
    st.session_state.modules = load_modules()

# Authentication check
if not st.session_state.authenticated:
    check_authentication()
else:
    # Render the application components
    render_header()
    
    # Main container for the app
    with st.container():
        # Two-column layout: sidebar and main content
        col1, col2 = st.columns([1, 5])
        
        with col1:
            render_sidebar()
        
        with col2:
            # Navigation bar
            render_navigation()
            
            # Render the selected module
            if st.session_state.current_section and st.session_state.current_module:
                try:
                    module_path = f"modules.{st.session_state.current_section}.{st.session_state.current_module}"
                    module = importlib.import_module(module_path)
                    
                    if st.session_state.current_view == "list":
                        module.render_list()
                    elif st.session_state.current_view == "view":
                        module.render_view()
                    elif st.session_state.current_view == "form":
                        module.render_form()
                    else:
                        st.error("Invalid view selected")
                except ModuleNotFoundError:
                    st.error(f"Module {module_path} not found")
                except Exception as e:
                    st.error(f"Error loading module: {str(e)}")
            else:
                # Display dashboard homepage
                st.title("gcPanel - Construction Management Dashboard")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.image("https://pixabay.com/get/gba48db1250efd35c9dffd0db152d0ebc3f28f4c90bb444aedf8c8d35ed6483d95bb97cefd51fa783369788c90562bb037d3745554751db92e1d14ef5ec963950_1280.jpg", 
                             caption="Construction Management", use_column_width=True)
                    
                    st.subheader("Recent Activity")
                    st.info("Welcome to gcPanel, your comprehensive construction management dashboard.")
                    
                    # Display some stats
                    st.metric(label="Active Projects", value="5")
                    st.metric(label="Open RFIs", value="12")
                    st.metric(label="Pending Submittals", value="8")
                
                with col2:
                    st.image("https://pixabay.com/get/g9f0f096f46d0d28520ae0a9a4b0d21826da014234b3817602a97ab8e49a66e97f590ed7492657c0a12df3ec17fb129eeb4afbeed9ab0173cd54afee551d2cf09_1280.jpg", 
                             caption="Construction Site", use_column_width=True)
                    
                    st.subheader("System Statistics")
                    st.info("Select a module from the sidebar to get started.")
                    
                    # Display some metrics
                    st.metric(label="Budget Progress", value="68%")
                    st.metric(label="Schedule Completion", value="42%")
                    st.metric(label="Quality Score", value="92%")
                
                st.subheader("Welcome to gcPanel")
                st.write("""
                This construction management dashboard provides a comprehensive set of tools to manage your construction projects.
                Use the sidebar to navigate through different modules organized by sections.
                """)

    # Render footer
    render_footer()
