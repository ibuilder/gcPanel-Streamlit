"""
Professional Dark Theme for Highland Tower Development Dashboard

Modern dark theme optimized for construction project management with:
- Reduced eye strain for long work sessions
- High contrast for field visibility
- Professional construction industry aesthetics
- Full feature parity with light theme
"""

import streamlit as st

def apply_dark_theme_styles():
    """Apply comprehensive full dark theme styling for Highland Tower Development."""
    
    dark_theme_css = """
    <style>
    /* Import Google Fonts for professional typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    
    /* Root Variables for Complete Dark Theme */
    :root {
        --primary-bg: #0a0e13;
        --secondary-bg: #151a23;
        --card-bg: #1e2533;
        --accent-bg: #252d3a;
        --surface-bg: #2a3441;
        --border-color: #364253;
        --border-light: #4a5568;
        --text-primary: #f7fafc;
        --text-secondary: #e2e8f0;
        --text-muted: #a0aec0;
        --text-disabled: #718096;
        --accent-blue: #63b3ed;
        --accent-green: #68d391;
        --accent-orange: #fbb040;
        --accent-red: #fc8181;
        --accent-purple: #b794f6;
        --accent-yellow: #faf089;
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.6);
        --gradient-primary: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        --gradient-accent: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
    }
    
    /* Complete Dark Base Application */
    html, body, [data-testid="stAppViewContainer"] {
        background: var(--primary-bg) !important;
        color: var(--text-primary) !important;
    }
    
    .stApp {
        background: var(--primary-bg) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Hide ALL Streamlit Branding and Elements */
    #MainMenu, footer, header, .stDeployButton, .stDecoration {
        visibility: hidden !important;
        display: none !important;
    }
    
    [data-testid="stToolbar"] {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* Force Dark Background Everywhere */
    .main, [data-testid="stMain"], [data-testid="stAppViewContainer"] > .main {
        background: var(--primary-bg) !important;
        color: var(--text-primary) !important;
    }
    
    /* Full Width Dark Container */
    .main .block-container, [data-testid="stMain"] .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 1rem !important;
        background: var(--primary-bg) !important;
        color: var(--text-primary) !important;
    }
    
    /* Force Dark on All Containers */
    [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"], .element-container {
        background: transparent !important;
        color: var(--text-primary) !important;
    }
    
    /* Dark Cards and Containers */
    .dashboard-card {
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: var(--shadow) !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
    }
    
    .dashboard-card:hover {
        box-shadow: var(--shadow-lg) !important;
        border-color: var(--accent-blue) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Complete Dark Text and Headers */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: var(--text-primary) !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600 !important;
    }
    
    .stMarkdown, .stMarkdown > div, .stText {
        color: var(--text-primary) !important;
        background: transparent !important;
    }
    
    /* Force Dark on ALL Text Elements */
    [data-testid="stMarkdownContainer"], 
    [data-testid="stText"],
    .stMarkdown p,
    .stMarkdown div,
    .stMarkdown span {
        color: var(--text-primary) !important;
        background: transparent !important;
    }
    
    /* Dark Title Elements */
    [data-testid="stHeader"] h1,
    [data-testid="stSubheader"] h2,
    .stTitle {
        color: var(--text-primary) !important;
        background: transparent !important;
    }
    
    /* Dark Metrics Cards */
    [data-testid="metric-container"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        box-shadow: var(--shadow) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="metric-container"]:hover {
        border-color: var(--accent-blue) !important;
        transform: translateY(-2px) !important;
    }
    
    [data-testid="metric-container"] label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }
    
    [data-testid="metric-container"] .metric-value {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }
    
    /* Dark Theme Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue) 0%, #3182ce 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3182ce 0%, #2c5aa0 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    /* Secondary Buttons */
    .stButton > button[kind="secondary"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: var(--accent-bg) !important;
        border-color: var(--accent-blue) !important;
    }
    
    /* Dark Form Elements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1) !important;
    }
    
    /* Dark Expanders */
    .streamlit-expanderHeader {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }
    
    .streamlit-expanderContent {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }
    
    /* Dark Sidebar (if needed) */
    .css-1d391kg {
        background-color: var(--secondary-bg) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    
    /* Dark Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--card-bg) !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: var(--text-secondary) !important;
        border-radius: 6px !important;
        padding: 0.75rem 1rem !important;
        margin: 0 0.25rem !important;
        font-weight: 500 !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--accent-blue) !important;
        color: white !important;
    }
    
    /* Dark Tables */
    .stDataFrame {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    .stDataFrame table {
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
    }
    
    .stDataFrame th {
        background-color: var(--accent-bg) !important;
        color: var(--text-primary) !important;
        border-bottom: 1px solid var(--border-color) !important;
    }
    
    /* Progress Bars */
    .stProgress > div > div {
        background-color: var(--border-color) !important;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent-green) 0%, var(--accent-blue) 100%) !important;
    }
    
    /* Charts and Visualizations */
    .js-plotly-plot {
        background-color: var(--card-bg) !important;
        border-radius: 8px !important;
    }
    
    /* Custom Status Badges for Dark Theme */
    .status-pill {
        padding: 0.25rem 0.75rem !important;
        border-radius: 20px !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    .status-active {
        background-color: rgba(72, 187, 120, 0.2) !important;
        color: var(--accent-green) !important;
        border: 1px solid var(--accent-green) !important;
    }
    
    .status-pending {
        background-color: rgba(237, 137, 54, 0.2) !important;
        color: var(--accent-orange) !important;
        border: 1px solid var(--accent-orange) !important;
    }
    
    .status-overdue {
        background-color: rgba(245, 101, 101, 0.2) !important;
        color: var(--accent-red) !important;
        border: 1px solid var(--accent-red) !important;
    }
    
    /* Highland Tower Specific Styling */
    .project-header {
        background: linear-gradient(135deg, var(--card-bg) 0%, var(--accent-bg) 100%) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        margin-bottom: 2rem !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .project-header::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 4px !important;
        background: linear-gradient(90deg, var(--accent-blue) 0%, var(--accent-green) 50%, var(--accent-purple) 100%) !important;
    }
    
    /* Counter Values */
    .counter-value {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: var(--accent-blue) !important;
        line-height: 1 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .counter-label {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    /* Activity Feed Styling */
    .activity-item {
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin-bottom: 0.75rem !important;
        transition: all 0.3s ease !important;
    }
    
    .activity-item:hover {
        border-color: var(--accent-blue) !important;
        transform: translateX(4px) !important;
    }
    
    /* Mobile Responsive Dark Theme */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        .dashboard-card {
            padding: 1rem !important;
        }
        
        .counter-value {
            font-size: 2rem !important;
        }
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--primary-bg) !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color) !important;
        border-radius: 4px !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-blue) !important;
    }
    
    /* Fix for Light Elements in Dark Theme */
    .stAlert {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    /* Theme Toggle Indicator */
    .theme-indicator {
        position: fixed !important;
        top: 1rem !important;
        right: 1rem !important;
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 20px !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.8rem !important;
        color: var(--text-secondary) !important;
        z-index: 1000 !important;
    }
    </style>
    """
    
    st.markdown(dark_theme_css, unsafe_allow_html=True)

def create_dark_status_badge(status: str, text: str):
    """Create dark theme status badge."""
    status_colors = {
        "active": {"bg": "rgba(72, 187, 120, 0.2)", "color": "#48bb78", "border": "#48bb78"},
        "pending": {"bg": "rgba(237, 137, 54, 0.2)", "color": "#ed8936", "border": "#ed8936"},
        "overdue": {"bg": "rgba(245, 101, 101, 0.2)", "color": "#f56565", "border": "#f56565"},
        "completed": {"bg": "rgba(72, 187, 120, 0.2)", "color": "#48bb78", "border": "#48bb78"},
        "review": {"bg": "rgba(66, 153, 225, 0.2)", "color": "#4299e1", "border": "#4299e1"}
    }
    
    colors = status_colors.get(status.lower(), status_colors["pending"])
    
    badge_html = f"""
    <span style='
        background: {colors["bg"]};
        color: {colors["color"]};
        border: 1px solid {colors["border"]};
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    '>{text}</span>
    """
    
    return st.markdown(badge_html, unsafe_allow_html=True)

def create_dark_metric_card(title: str, value: str, change: str = None, icon: str = "📊", color: str = "#4299e1"):
    """Create dark theme metric card."""
    change_html = ""
    if change:
        change_color = "#48bb78" if not change.startswith("-") else "#f56565"
        change_html = f"<div style='color: {change_color}; font-size: 0.9rem; margin-top: 0.5rem;'>{change}</div>"
    
    card_html = f"""
    <div style='
        background: #242b3d;
        border: 1px solid #3a4553;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    '>
        <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
            <span style='font-size: 1.5rem; margin-right: 0.75rem;'>{icon}</span>
            <div style='color: #a0aec0; font-size: 0.9rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;'>{title}</div>
        </div>
        <div style='font-size: 2.5rem; font-weight: 700; color: {color}; line-height: 1;'>{value}</div>
        {change_html}
    </div>
    """
    
    return st.markdown(card_html, unsafe_allow_html=True)

def add_dark_theme_toggle():
    """Add theme toggle indicator."""
    st.markdown("""
    <div class="theme-indicator">
        🌙 Dark Mode Active
    </div>
    """, unsafe_allow_html=True)