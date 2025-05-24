"""
Complete Full Dark Theme for Highland Tower Development Dashboard

Ultra-comprehensive dark mode that transforms every single element.
"""

import streamlit as st

def apply_complete_dark_theme():
    """Apply complete full dark theme - every element will be dark."""
    
    complete_dark_css = """
    <style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Complete Dark Theme Variables */
    :root {
        --bg-primary: #0a0e13;
        --bg-secondary: #121721;
        --bg-tertiary: #1a1f2e;
        --bg-surface: #1e2533;
        --bg-card: #242b3d;
        --bg-input: #2a3441;
        --border-primary: #364253;
        --border-secondary: #4a5568;
        --text-primary: #ffffff;
        --text-secondary: #e2e8f0;
        --text-muted: #a0aec0;
        --accent-blue: #4299e1;
        --accent-green: #48bb78;
        --accent-orange: #ed8936;
        --accent-red: #f56565;
        --shadow-dark: 0 4px 6px rgba(0, 0, 0, 0.7);
    }
    
    /* FORCE DARK ON EVERYTHING */
    *, *:before, *:after {
        color: var(--text-primary) !important;
    }
    
    /* Force Dark on Navigation and Toolbar */
    .stToolbar, [data-testid="stToolbar"],
    .stHeader, [data-testid="stHeader"],
    header[data-testid="stHeader"],
    .main-header, .toolbar {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border-bottom: 1px solid var(--border-primary) !important;
    }
    
    /* Logout Button and Navigation Buttons */
    .stButton > button[kind="secondary"],
    button[data-testid="baseButton-secondary"],
    .stButton button,
    [data-testid="stButton"] button {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-primary) !important;
    }
    
    /* Force All Charts and Graphs Dark - Enhanced */
    .js-plotly-plot, .plotly, .plotly-graph-div,
    .user-select-none, .svg-container,
    .stPlotlyChart, [data-testid="stPlotlyChart"] {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
    }
    
    /* Plotly Chart Background and Text - Complete Coverage */
    .js-plotly-plot .plotly .main-svg,
    .js-plotly-plot .bg, .plot-container,
    .modebar, .modebar-container, .modebar-group,
    .plotly .gtitle, .plotly .xtitle, .plotly .ytitle,
    .plotly text, .plotly .tick text {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        fill: var(--text-primary) !important;
    }
    
    /* Streamlit Navigation and Header - Enhanced Dark */
    .main .block-container, 
    [data-testid="stSidebar"], 
    [data-testid="stSidebarNav"],
    .css-1d391kg, .css-12oz5g7,
    header[data-testid="stHeader"] {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }
    
    /* All Navigation Elements Dark */
    nav, .stSelectbox, .stTabs,
    .streamlit-container .main,
    .stApp > header, .stToolbar {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border-color: var(--border-primary) !important;
    }
    
    /* Force Logout and Action Buttons Dark */
    button[kind="secondary"], button[kind="primary"],
    .stButton button, .stDownloadButton button,
    [data-testid="baseButton-secondary"],
    [data-testid="baseButton-primary"] {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-primary) !important;
        padding: 0.75rem 1.25rem !important;
        margin: 0.5rem !important;
    }
    
    /* Root Elements - Complete Dark */
    html, body {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Streamlit App Container - Force Dark */
    .stApp, [data-testid="stApp"] {
        background-color: var(--bg-primary) !important;
        background-image: none !important;
        color: var(--text-primary) !important;
    }
    
    /* Main Content Areas - Force Dark */
    .main, [data-testid="stMain"] {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    /* App View Container - Force Dark */
    [data-testid="stAppViewContainer"] {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Block Container - Full Width Dark */
    .block-container, [data-testid="stMain"] .block-container {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        max-width: 100% !important;
        padding: 2rem !important;
    }
    
    /* ALL Text Elements - Force White Text */
    h1, h2, h3, h4, h5, h6, p, span, div, label, 
    .stMarkdown, .stText, .stTitle, .stSubheader,
    [data-testid="stMarkdownContainer"],
    [data-testid="stText"] {
        color: var(--text-primary) !important;
        background-color: transparent !important;
    }
    
    /* Headers with Better Contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Metrics - Complete Dark Redesign */
    [data-testid="metric-container"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: var(--shadow-dark) !important;
    }
    
    [data-testid="metric-container"] label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--accent-blue) !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }
    
    /* Buttons - Complete Dark Style with Better Padding */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue), #3182ce) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        margin: 0.5rem 0 !important;
        font-weight: 500 !important;
        box-shadow: var(--shadow-dark) !important;
        transition: all 0.3s ease !important;
        min-height: 44px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3182ce, #2c5aa0) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Container Spacing and Padding Improvements */
    .stContainer, [data-testid="stVerticalBlock"] {
        padding: 1rem 1.5rem !important;
        margin: 0.5rem 0 !important;
    }
    
    .stColumns, [data-testid="stColumns"] {
        gap: 1.5rem !important;
        padding: 0 0.75rem !important;
    }
    
    .stColumn, [data-testid="stColumn"] {
        padding: 0 0.75rem !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Card-style containers with proper spacing */
    .element-container, [data-testid="element-container"] {
        padding: 1rem !important;
        margin: 1rem 0 !important;
        background-color: var(--bg-card) !important;
        border-radius: 8px !important;
        border: 1px solid var(--border-primary) !important;
    }
    
    /* Content blocks with breathing room */
    .stMarkdown, [data-testid="stMarkdown"] {
        padding: 0.5rem 1rem !important;
        margin: 0.75rem 0 !important;
    }
    
    /* Form element containers */
    .stTextInput, .stSelectbox, .stTextArea, .stNumberInput {
        margin: 0.75rem 0 !important;
        padding: 0.25rem 0 !important;
    }
    
    /* Form Elements - Complete Dark */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        background-color: var(--bg-input) !important;
        border: 1px solid var(--border-primary) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Selectbox Dropdown - Dark */
    .stSelectbox [data-baseweb="select"] {
        background-color: var(--bg-input) !important;
        border-color: var(--border-primary) !important;
    }
    
    .stSelectbox [data-baseweb="select"] span {
        color: var(--text-primary) !important;
    }
    
    /* Tabs - Complete Dark */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--bg-card) !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: var(--text-muted) !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--accent-blue) !important;
        color: #ffffff !important;
    }
    
    /* Expanders - Dark */
    .streamlit-expanderHeader {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: 8px !important;
    }
    
    .streamlit-expanderContent {
        background-color: var(--bg-surface) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-primary) !important;
        border-top: none !important;
    }
    
    /* Data Tables - Complete Dark */
    .stDataFrame, [data-testid="stDataFrame"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    .stDataFrame table {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
    }
    
    .stDataFrame th {
        background-color: var(--bg-surface) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        border-bottom: 1px solid var(--border-primary) !important;
    }
    
    .stDataFrame td {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border-bottom: 1px solid var(--border-primary) !important;
    }
    
    /* Columns - Dark Background */
    [data-testid="column"] {
        background-color: transparent !important;
        color: var(--text-primary) !important;
    }
    
    /* Containers - Dark */
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    .element-container {
        background-color: transparent !important;
        color: var(--text-primary) !important;
    }
    
    /* Charts and Plots - Dark Background */
    .js-plotly-plot, .plotly {
        background-color: var(--bg-card) !important;
        border-radius: 8px !important;
    }
    
    /* Progress Bars - Dark */
    .stProgress > div {
        background-color: var(--border-primary) !important;
        border-radius: 4px !important;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--accent-green), var(--accent-blue)) !important;
        border-radius: 4px !important;
    }
    
    /* Alerts and Messages - Dark */
    .stAlert {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-primary) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
    }
    
    .stSuccess {
        background-color: rgba(72, 187, 120, 0.1) !important;
        border-color: var(--accent-green) !important;
        color: var(--accent-green) !important;
    }
    
    .stError {
        background-color: rgba(245, 101, 101, 0.1) !important;
        border-color: var(--accent-red) !important;
        color: var(--accent-red) !important;
    }
    
    .stWarning {
        background-color: rgba(237, 137, 54, 0.1) !important;
        border-color: var(--accent-orange) !important;
        color: var(--accent-orange) !important;
    }
    
    .stInfo {
        background-color: rgba(66, 153, 225, 0.1) !important;
        border-color: var(--accent-blue) !important;
        color: var(--accent-blue) !important;
    }
    
    /* Checkboxes and Radio - Dark */
    .stCheckbox, .stRadio {
        color: var(--text-primary) !important;
    }
    
    /* File Uploader - Dark */
    .stFileUploader {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }
    
    /* Sidebar (if any) - Complete Dark */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border-right: 1px solid var(--border-primary) !important;
    }
    
    /* Custom Dashboard Cards */
    .dashboard-card {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-primary) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: var(--shadow-dark) !important;
        color: var(--text-primary) !important;
    }
    
    /* Highland Tower Status Badges */
    .status-pill {
        padding: 0.25rem 0.75rem !important;
        border-radius: 20px !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
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
    
    /* Counter Values for Metrics */
    .counter-value {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: var(--accent-blue) !important;
        line-height: 1 !important;
    }
    
    .counter-label {
        font-size: 0.9rem !important;
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
    }
    
    /* COMPLETELY ELIMINATE SIDEBAR AND STREAMLIT ELEMENTS */
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden !important;
        display: none !important;
    }
    
    [data-testid="stToolbar"] {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* AGGRESSIVE SIDEBAR REMOVAL */
    [data-testid="stSidebar"],
    .css-1d391kg,
    .css-1lcbmhc,
    .css-17eq0hr,
    section[data-testid="stSidebar"],
    .st-emotion-cache-1d391kg,
    .st-emotion-cache-1lcbmhc,
    .st-emotion-cache-17eq0hr,
    [data-testid="collapsedControl"],
    button[kind="headerNoPadding"],
    .stSidebar {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        min-width: 0 !important;
        max-width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Force Main Content to Full Width */
    .main .block-container {
        margin-left: 0 !important;
        padding-left: 2rem !important;
    }
    
    .stApp > div:first-child {
        margin-left: 0 !important;
    }
    
    /* Mobile Responsive Dark */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem !important;
        }
        
        .dashboard-card {
            padding: 1rem !important;
        }
    }
    
    /* Scrollbars - Dark */
    ::-webkit-scrollbar {
        width: 8px !important;
        background: var(--bg-primary) !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-primary) !important;
        border-radius: 4px !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-blue) !important;
    }
    
    /* Force Dark on Remaining Elements */
    [data-testid="stMarkdown"] > div,
    .stMarkdown > div,
    .element-container > div {
        background-color: transparent !important;
        color: var(--text-primary) !important;
    }
    
    /* Theme Toggle Indicator */
    .dark-theme-indicator {
        position: fixed !important;
        top: 1rem !important;
        right: 1rem !important;
        background: var(--bg-card) !important;
        color: var(--accent-blue) !important;
        padding: 0.5rem 1rem !important;
        border-radius: 20px !important;
        font-size: 0.8rem !important;
        border: 1px solid var(--border-primary) !important;
        z-index: 1000 !important;
    }
    </style>
    """
    
    st.markdown(complete_dark_css, unsafe_allow_html=True)

def add_dark_theme_indicator():
    """Add dark theme indicator."""
    st.markdown("""
    <div class="dark-theme-indicator">
        🌙 Highland Tower - Full Dark Mode
    </div>
    """, unsafe_allow_html=True)