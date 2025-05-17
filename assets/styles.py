import streamlit as st

def apply_styles():
    """Apply custom styles to the application"""
    
    # Inline styles for a more professional and modern look
    st.markdown("""
    <style>
        /* Modern color scheme for construction management */
        :root {
            --primary-color: #1976d2;
            --primary-light: #4791db;
            --primary-dark: #115293;
            --secondary-color: #388e3c;
            --secondary-light: #5eae60;
            --secondary-dark: #1b5e20;
            --accent-color: #f57c00;
            --accent-light: #ff9e40;
            --accent-dark: #bb4d00;
            --background-color: #121212;
            --surface-color: #1e1e1e;
            --error-color: #d32f2f;
            --warning-color: #ffa000;
            --info-color: #0288d1;
            --success-color: #388e3c;
            
            /* Text colors */
            --text-primary: rgba(255, 255, 255, 0.87);
            --text-secondary: rgba(255, 255, 255, 0.6);
            --text-disabled: rgba(255, 255, 255, 0.38);
            
            /* UI elements */
            --card-bg: #2d2d2d;
            --sidebar-bg: #1a1a1a;
            --sidebar-text: rgba(255, 255, 255, 0.87);
            --border-color: rgba(255, 255, 255, 0.12);
            --divider-color: rgba(255, 255, 255, 0.12);
            --shadow-color: rgba(0, 0, 0, 0.5);
            
            /* Status colors */
            --status-approved: #4caf50;
            --status-pending: #2196f3;
            --status-rejected: #f44336;
            --status-revise: #ff9800;
        }
        
        /* Core app layout improvements */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }
        
        /* Make everything dark by default */
        .stApp {
            background-color: var(--background-color);
            color: var(--text-primary);
        }
                
        /* Modernize header and make it sticky */
        header {
            position: sticky;
            top: 0;
            z-index: 999;
            background-color: var(--background-color) !important;
            border-bottom: 1px solid var(--divider-color);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        
        /* Hide Streamlit branding */
        #MainMenu, footer, header .decoration {
            display: none !important;
        }
        
        /* Professional sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--divider-color);
        }
        
        section[data-testid="stSidebar"] .block-container {
            padding-top: 1rem;
        }
        
        /* Navigation elements in sidebar */
        .sidebar-nav-item {
            display: flex;
            align-items: center;
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 5px;
            transition: all 0.2s ease;
            cursor: pointer;
            color: var(--sidebar-text);
            text-decoration: none;
        }
        
        .sidebar-nav-item:hover {
            background-color: rgba(255, 255, 255, 0.08);
        }
        
        .sidebar-nav-item.active {
            background-color: var(--primary-color);
            color: white;
        }
        
        .sidebar-nav-item .material-icons {
            margin-right: 10px;
            font-size: 20px;
        }
        
        /* Modern card design */
        .card {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px var(--shadow-color);
            border: 1px solid var(--divider-color);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px var(--shadow-color);
        }
        
        .card-header {
            border-bottom: 1px solid var(--divider-color);
            padding-bottom: 12px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .card-title {
            font-size: 18px;
            font-weight: 500;
            color: var(--text-primary);
            margin: 0;
        }
        
        .card-subtitle {
            color: var(--text-secondary);
            margin-top: 4px;
            font-size: 14px;
        }
        
        /* Dashboard metric cards */
        .metric-card {
            background: linear-gradient(135deg, var(--card-bg) 0%, rgba(45, 45, 45, 0.8) 100%);
            border-radius: 12px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 4px 12px var(--shadow-color);
            position: relative;
            overflow: hidden;
            border: 1px solid var(--divider-color);
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 5px;
            height: 100%;
            background-color: var(--primary-color);
        }
        
        .metric-card.secondary::before {
            background-color: var(--secondary-color);
        }
        
        .metric-card.accent::before {
            background-color: var(--accent-color);
        }
        
        .metric-card.info::before {
            background-color: var(--info-color);
        }
        
        .metric-value {
            font-size: 26px;
            font-weight: 700;
            margin: 8px 0;
            color: var(--text-primary);
        }
        
        .metric-label {
            color: var(--text-secondary);
            font-size: 14px;
            margin-bottom: 4px;
        }
        
        .metric-subtext {
            color: var(--text-secondary);
            font-size: 12px;
            display: flex;
            align-items: center;
        }
        
        /* Modern buttons */
        .stButton button {
            border-radius: 6px;
            font-weight: 500;
            padding: 8px 16px;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            border: none;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        
        /* Primary action button */
        .primary-button {
            background-color: var(--primary-color) !important;
            color: white !important;
        }
        
        /* Secondary action button */
        .secondary-button {
            background-color: transparent !important;
            border: 1px solid var(--primary-color) !important;
            color: var(--primary-color) !important;
        }
        
        /* Status pills/badges with modern design */
        .status-pill {
            display: inline-flex;
            align-items: center;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 12px;
            font-weight: 500;
            text-transform: uppercase;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .status-pill-icon {
            margin-right: 6px;
            font-size: 14px;
        }
        
        .status-approved {
            background-color: rgba(76, 175, 80, 0.15);
            color: var(--status-approved);
            border: 1px solid rgba(76, 175, 80, 0.3);
        }
        
        .status-pending {
            background-color: rgba(33, 150, 243, 0.15);
            color: var(--status-pending);
            border: 1px solid rgba(33, 150, 243, 0.3);
        }
        
        .status-rejected {
            background-color: rgba(244, 67, 54, 0.15);
            color: var(--status-rejected);
            border: 1px solid rgba(244, 67, 54, 0.3);
        }
        
        .status-revise {
            background-color: rgba(255, 152, 0, 0.15);
            color: var(--status-revise);
            border: 1px solid rgba(255, 152, 0, 0.3);
        }
        
        /* Modern data tables */
        .styled-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 10px var(--shadow-color);
            margin: 16px 0;
        }
        
        .styled-table thead tr {
            background-color: rgba(25, 118, 210, 0.1);
            text-align: left;
            font-weight: 500;
        }
        
        .styled-table th {
            padding: 12px 15px;
            border-bottom: 1px solid var(--divider-color);
            color: var(--primary-color);
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .styled-table td {
            padding: 10px 15px;
            border-bottom: 1px solid var(--divider-color);
            font-size: 14px;
        }
        
        .styled-table tbody tr {
            transition: all 0.2s ease;
        }
        
        .styled-table tbody tr:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
        
        .styled-table tbody tr:last-of-type td {
            border-bottom: none;
        }
        
        /* Progress bar styling */
        .modern-progress-container {
            width: 100%;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            height: 10px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .modern-progress-bar {
            height: 100%;
            border-radius: 8px;
            background: linear-gradient(90deg, var(--primary-color) 0%, var(--primary-light) 100%);
            transition: width 0.5s ease;
        }
        
        .modern-progress-bar.success {
            background: linear-gradient(90deg, var(--success-color) 0%, var(--secondary-light) 100%);
        }
        
        .modern-progress-bar.warning {
            background: linear-gradient(90deg, var(--warning-color) 0%, var(--accent-light) 100%);
        }
        
        .modern-progress-bar.danger {
            background: linear-gradient(90deg, var(--error-color) 0%, #f44336 100%);
        }
        
        /* Activity feed styling */
        .activity-feed {
            margin: 20px 0;
        }
        
        .activity-item {
            display: flex;
            margin-bottom: 16px;
            position: relative;
        }
        
        .activity-icon {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background-color: rgba(25, 118, 210, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            color: var(--primary-color);
        }
        
        .activity-content {
            flex: 1;
            background-color: rgba(255, 255, 255, 0.05);
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid var(--divider-color);
        }
        
        .activity-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        
        .activity-title {
            font-weight: 500;
            color: var(--text-primary);
        }
        
        .activity-time {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .activity-description {
            color: var(--text-secondary);
            font-size: 14px;
        }
        
        /* Breadcrumb navigation */
        .breadcrumb {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            font-size: 14px;
        }
        
        .breadcrumb-item {
            display: flex;
            align-items: center;
        }
        
        .breadcrumb-item:not(:last-child)::after {
            content: '›';
            margin: 0 8px;
            color: var(--text-secondary);
        }
        
        .breadcrumb-item a {
            color: var(--primary-color);
            text-decoration: none;
            transition: all 0.2s ease;
        }
        
        .breadcrumb-item a:hover {
            color: var(--primary-light);
            text-decoration: underline;
        }
        
        .breadcrumb-item:last-child {
            color: var(--text-secondary);
        }
        
        /* Styles for data inputs in dark mode */
        input, textarea, select, 
        .stTextInput > div[data-baseweb="base-input"] > div > input,
        .stTextArea > div[data-baseweb="textarea"] > textarea,
        .stSelectbox div[role="combobox"] input {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid var(--divider-color) !important;
            border-radius: 6px !important;
            color: var(--text-primary) !important;
            padding: 10px 14px !important;
            transition: all 0.2s ease;
        }
        
        /* Fix for select boxes */
        .stSelectbox div[data-baseweb="select"] {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-radius: 6px !important;
        }
        
        .stSelectbox div[role="listbox"] {
            background-color: var(--card-bg) !important;
            border: 1px solid var(--divider-color) !important;
        }
        
        .stSelectbox div[role="option"] {
            color: var(--text-primary) !important;
        }
        
        .stSelectbox div[role="option"]:hover {
            background-color: rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Button styles for dark theme */
        .stButton > button {
            background-color: rgba(255, 255, 255, 0.08) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--divider-color) !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton > button:hover {
            background-color: rgba(255, 255, 255, 0.12) !important;
            border-color: var(--primary-color) !important;
        }
        
        /* Primary buttons */
        .stButton > [kind="primary"] {
            background-color: var(--primary-color) !important;
            color: white !important;
            border: none !important;
        }
        
        .stButton > [kind="primary"]:hover {
            background-color: var(--primary-light) !important;
            box-shadow: 0 2px 8px rgba(25, 118, 210, 0.4) !important;
        }
        
        /* Focus states */
        input:focus, textarea:focus, select:focus, 
        .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 1px var(--primary-color) !important;
        }
        
        /* For light theme */
        .light-mode {
            /* Inverse color scheme */
            --background-color: #f5f5f5;
            --surface-color: #ffffff;
            --card-bg: #ffffff;
            --sidebar-bg: #1976d2;
            --text-primary: rgba(0, 0, 0, 0.87);
            --text-secondary: rgba(0, 0, 0, 0.6);
            --text-disabled: rgba(0, 0, 0, 0.38);
            --divider-color: rgba(0, 0, 0, 0.12);
            --shadow-color: rgba(0, 0, 0, 0.2);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Add Material Design Icons
    st.markdown("""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    # Apply theme-specific styling
    if st.session_state.get('theme', 'dark') == 'light':
        st.markdown("""
        <style>
            /* Light theme overrides */
            :root {
                --primary-color: #1976d2;
                --primary-light: #4791db;
                --primary-dark: #115293;
                --secondary-color: #388e3c;
                --secondary-light: #5eae60;
                --secondary-dark: #1b5e20;
                --accent-color: #f57c00;
                --accent-light: #ff9e40;
                --accent-dark: #bb4d00;
                
                /* Light theme specific colors */
                --background-color: #ffffff;
                --surface-color: #f5f5f5;
                --card-bg: #ffffff;
                --sidebar-bg: #f0f0f0;
                --error-color: #d32f2f;
                --warning-color: #ffa000;
                --info-color: #0288d1;
                --success-color: #388e3c;
                
                /* Text colors for light theme */
                --text-primary: rgba(0, 0, 0, 0.87);
                --text-secondary: rgba(0, 0, 0, 0.6);
                --text-disabled: rgba(0, 0, 0, 0.38);
                --sidebar-text: rgba(0, 0, 0, 0.87);
                
                /* UI elements for light theme */
                --border-color: rgba(0, 0, 0, 0.12);
                --divider-color: rgba(0, 0, 0, 0.12);
                --shadow-color: rgba(0, 0, 0, 0.1);
            }
            
            /* Sidebar specific overrides for light theme */
            section[data-testid="stSidebar"] {
                background-color: var(--sidebar-bg);
                border-right: 1px solid var(--divider-color);
            }
            
            /* Override the active states for better visibility in light mode */
            .sidebar-nav-item.active {
                background-color: var(--primary-color);
                color: white !important;
            }
            
            .sidebar-nav-item:not(.active) {
                color: var(--text-primary);
            }
            
            /* Make status pills more visible in light mode */
            .status-pill {
                border: 1px solid rgba(0, 0, 0, 0.1);
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
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
