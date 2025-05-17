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

# Reset demo mode flag
st.session_state.demo_mode = False

# Always refresh modules on startup to ensure they're properly loaded
st.session_state.modules = load_modules()

# Authentication check
if not st.session_state.authenticated:
    check_authentication()
else:
    # Render the application components
    render_header()
    
    # Main content area - streamlined layout
    with st.container():
        # Render sidebar (using Streamlit's built-in sidebar)
        with st.sidebar:
            render_sidebar()
        
        # Main content area with navigation and module content
        with st.container():
            # Improved navigation bar
            render_navigation()
            
            # Render the selected module content
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
                # Display dashboard homepage with enhanced components
                st.title("gcPanel Dashboard")
                
                # Import custom components
                from components.custom_elements import dashboard_card, progress_bar, info_box, status_pill
                
                # Material Icon link for icons
                st.markdown("""
                <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
                <style>
                    /* Dashboard specific styling */
                    .dashboard-header {
                        margin-bottom: 20px;
                    }
                    
                    .dashboard-section {
                        margin-bottom: 30px;
                    }
                    
                    /* Ensure images have consistent dimensions */
                    .dashboard-image {
                        width: 100%;
                        border-radius: 8px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }
                </style>
                """, unsafe_allow_html=True)
                
                # Dashboard header with project overview
                if 'current_project' in st.session_state:
                    st.markdown(f"""
                    <div class="dashboard-header">
                        <h2>Project Overview: {st.session_state.current_project}</h2>
                        <p style="color: #666;">Below is a summary of key metrics and recent activity for this project.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Top metrics row (4 cards in a row)
                cols = st.columns(4)
                
                with cols[0]:
                    dashboard_card("Active Projects", "5", "2 in planning phase", "domain", "#1e88e5")
                
                with cols[1]:
                    dashboard_card("Open RFIs", "12", "3 urgent", "help_outline", "#f44336")
                
                with cols[2]:
                    dashboard_card("Pending Submittals", "8", "5 overdue", "description", "#ff9800")
                
                with cols[3]:
                    dashboard_card("Budget Utilization", "$2.4M", "68% of total", "attach_money", "#43a047")
                
                # Project progress section
                st.markdown('<div class="dashboard-section"><h3>Project Progress</h3></div>', unsafe_allow_html=True)
                
                # Progress bars in two columns
                prog_col1, prog_col2 = st.columns(2)
                
                with prog_col1:
                    progress_bar(68, 100, "Budget Progress", "#1e88e5")
                    progress_bar(42, 100, "Schedule Completion", "#43a047")
                
                with prog_col2:
                    progress_bar(92, 100, "Quality Score", "#ff9800")
                    progress_bar(78, 100, "Documentation", "#9c27b0")
                
                # Recent activity and site photos
                activity_col, photo_col = st.columns([3, 2])
                
                with activity_col:
                    st.markdown('<div class="dashboard-section"><h3>Recent Activity</h3></div>', unsafe_allow_html=True)
                    
                    # Activity items with status pills
                    st.markdown('<div style="display: flex; justify-content: space-between; margin-bottom: 10px;">'
                                '<span>Submittal #102 - HVAC Equipment</span>', unsafe_allow_html=True)
                    status_pill("approved")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div style="display: flex; justify-content: space-between; margin-bottom: 10px;">'
                                '<span>RFI #45 - Foundation Details</span>', unsafe_allow_html=True)
                    status_pill("pending")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div style="display: flex; justify-content: space-between; margin-bottom: 10px;">'
                                '<span>Daily Report - May 16, 2025</span>', unsafe_allow_html=True)
                    status_pill("complete")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div style="display: flex; justify-content: space-between; margin-bottom: 10px;">'
                                '<span>Change Order #8 - Site Utilities</span>', unsafe_allow_html=True)
                    status_pill("revise")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Info box for announcements
                    info_box("The project team meeting is scheduled for May 20, 2025 at 10:00 AM. Please prepare your progress reports.", 
                            "info", True, "announcement")
                
                with photo_col:
                    st.markdown('<div class="dashboard-section"><h3>Site Photos</h3></div>', unsafe_allow_html=True)
                    
                    # Site photo with better styling
                    st.markdown("""
                    <img src="https://pixabay.com/get/g9f0f096f46d0d28520ae0a9a4b0d21826da014234b3817602a97ab8e49a66e97f590ed7492657c0a12df3ec17fb129eeb4afbeed9ab0173cd54afee551d2cf09_1280.jpg" 
                         class="dashboard-image" alt="Construction Site">
                    <p style="font-size: 12px; color: #666; text-align: center; margin-top: 5px;">
                        Latest site photo - May 16, 2025
                    </p>
                    """, unsafe_allow_html=True)
                
                # Welcome information at the bottom
                st.markdown('<div class="dashboard-section"><h3>Getting Started</h3></div>', unsafe_allow_html=True)
                
                info_box("""
                <p><strong>Welcome to gcPanel</strong> - your comprehensive construction management dashboard.</p>
                <p>Use the sidebar navigation to access different modules:</p>
                <ul>
                    <li><strong>Engineering:</strong> Manage RFIs, submittals, and document library</li>
                    <li><strong>Field:</strong> Daily reports and photo logs</li>
                    <li><strong>Cost:</strong> Budget tracking and change orders</li>
                    <li><strong>Contracts:</strong> Prime contract and subcontract management</li>
                </ul>
                <p>Select a module from the sidebar or use the quick access buttons to get started.</p>
                """, "success", False, "welcome")

    # Render footer
    render_footer()
