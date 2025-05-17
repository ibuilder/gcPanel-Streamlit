import streamlit as st

def apply_styles():
    """Apply custom styles to the application"""
    
    # Try to load custom CSS file first
    try:
        with open('assets/custom.css', 'r') as f:
            custom_css = f.read()
            st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)
    except Exception:
        # Fall back to inline styles if file isn't available
        st.markdown("""
        <style>
            /* Main color variables */
            :root {
                --primary-color: #1e88e5;
                --secondary-color: #43a047;
                --accent-color: #ff9800;
                --background-color: #f5f7fa;
                --sidebar-bg: #2c3e50;
                --sidebar-text: #ecf0f1;
                --card-bg: white;
                --text-color: #333;
                --border-color: #e0e0e0;
                --success-color: #4caf50;
                --warning-color: #ff9800;
                --danger-color: #f44336;
                --info-color: #2196f3;
            }
            
            /* Main container styles */
            .main .block-container {
                padding-top: 1rem;
                padding-bottom: 1rem;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            /* Sidebar styling - enhanced for construction dashboard */
            section[data-testid="stSidebar"] {
                background-color: var(--sidebar-bg);
                border-right: 1px solid var(--border-color);
            }
            
            section[data-testid="stSidebar"] .block-container {
                padding-top: 2rem;
            }
            
            /* Make sidebar text white */
            section[data-testid="stSidebar"] h1, 
            section[data-testid="stSidebar"] h2, 
            section[data-testid="stSidebar"] h3,
            section[data-testid="stSidebar"] .stSubheader,
            section[data-testid="stSidebar"] p {
                color: var(--sidebar-text) !important;
            }
            
            section[data-testid="stSidebar"] button {
                border: none;
                border-radius: 0;
                text-align: left;
                padding: 0.5rem 1rem;
                margin: 0.2rem 0;
                transition: background-color 0.3s;
                color: var(--sidebar-text);
                width: 100%;
            }
            
            section[data-testid="stSidebar"] button:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            
            /* Sidebar divider */
            section[data-testid="stSidebar"] hr {
                margin: 1rem 0;
                border-color: rgba(255, 255, 255, 0.1);
            }
            
            /* Sidebar expander styling */
            section[data-testid="stSidebar"] [data-testid="stExpander"] {
                border: none;
                background-color: rgba(255, 255, 255, 0.05);
                margin-bottom: 0.5rem;
            }
            
            section[data-testid="stSidebar"] [data-testid="stExpander"] summary {
                padding: 0.5rem 1rem;
                color: var(--sidebar-text);
                font-weight: 500;
            }
            
            /* Header styles */
            header {
                background-color: transparent !important;
                border-bottom: 1px solid var(--border-color);
            }
            
            /* Footer styles */
            footer {
                border-top: 1px solid var(--border-color);
                padding-top: 1rem;
                margin-top: 2rem;
                text-align: center;
                color: #666;
                font-size: 0.8rem;
            }
            
            /* Improve spacing in forms */
            .stForm {
                background-color: var(--card-bg);
                padding: 1.5rem;
                border-radius: 8px;
                border: none;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 1rem;
            }
            
            /* Improve button styling */
            .stButton button {
                border-radius: 4px;
                font-weight: 500;
                padding: 0.5rem 1rem;
                transition: all 0.3s;
            }
            
            .stButton button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            
            /* Add some spacing to metrics */
            [data-testid="stMetric"] {
                background-color: var(--card-bg);
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            [data-testid="stMetricLabel"] {
                font-weight: 500;
            }
            
            [data-testid="stMetricValue"] {
                font-size: 2rem;
                font-weight: 700;
                color: var(--primary-color);
            }
            
            /* Style dataframes */
            .stDataFrame {
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            .stDataFrame th {
                background-color: #f5f7fa;
                font-weight: 600;
                padding: 10px 15px;
            }
            
            .stDataFrame td {
                border: 1px solid var(--border-color);
                padding: 8px 12px;
            }
            
            /* Improve tabs styling */
            .stTabs [data-baseweb="tab-list"] {
                gap: 1rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: 3rem;
                white-space: nowrap;
                padding: 0 1rem;
                border: 1px solid #e9ecef;
                border-radius: 0.25rem 0.25rem 0 0;
                font-weight: 500;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: var(--primary-color);
                color: white;
                border-bottom: none;
            }
            
            /* Section headers */
            .section-header {
                position: relative;
                margin-bottom: 1.5rem;
                padding-bottom: 0.5rem;
            }
            
            .section-header::after {
                content: '';
                position: absolute;
                left: 0;
                bottom: 0;
                height: 3px;
                width: 50px;
                background-color: var(--primary-color);
            }
            
            /* Status badges */
            .status-badge {
                display: inline-block;
                padding: 0.25rem 0.5rem;
                border-radius: 12px;
                font-size: 0.8rem;
                font-weight: 500;
            }
            
            .status-badge.approved {
                background-color: rgba(76, 175, 80, 0.2);
                color: #2e7d32;
            }
            
            .status-badge.pending {
                background-color: rgba(33, 150, 243, 0.2);
                color: #1565c0;
            }
            
            .status-badge.rejected {
                background-color: rgba(244, 67, 54, 0.2);
                color: #c62828;
            }
            
            .status-badge.revise {
                background-color: rgba(255, 152, 0, 0.2);
                color: #ef6c00;
            }
        </style>
        """, unsafe_allow_html=True)

def apply_theme():
    """Apply theme settings (alternative to config.toml)"""
    # This function is provided as an alternative to using config.toml
    # It can be called at the start of the app if config.toml is not used
    
    st.set_page_config(
        page_title="gcPanel - Construction Management Dashboard",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def get_icon_svg(icon_name):
    """Get an SVG icon from Feather Icons
    
    Args:
        icon_name (str): Name of the Feather icon
        
    Returns:
        str: SVG markup for the icon
    """
    # This is a simplified version - in a real app, you would use a proper icon library
    # or fetch from a CDN
    
    icons = {
        "building": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-home"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>',
        "clipboard": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-clipboard"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>',
        "users": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-users"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>',
        "file-text": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-file-text"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>',
        "settings": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-settings"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>',
        "bar-chart-2": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-bar-chart-2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>'
    }
    
    return icons.get(icon_name, '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-file"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path><polyline points="13 2 13 9 20 9"></polyline></svg>')
