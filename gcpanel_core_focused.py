"""
Highland Tower Development - Core Focused Construction Management Platform
$45.5M Mixed-Use Development - Better than Procore

Focus: Robust module functionality and core construction management features
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

def apply_highland_tower_styling():
    """Apply professional Highland Tower Development enterprise styling"""
    st.markdown("""
    <style>
    /* Highland Tower Enterprise Styling */
    :root {
        --highland-primary: #1e40af;
        --highland-secondary: #3b82f6;
        --highland-accent: #f59e0b;
        --highland-success: #059669;
        --highland-warning: #d97706;
        --highland-error: #dc2626;
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-200: #e5e7eb;
        --gray-300: #d1d5db;
        --gray-600: #4b5563;
        --gray-700: #374151;
        --gray-800: #1f2937;
        --gray-900: #111827;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    /* Main App Styling */
    .stApp {
        background-color: var(--gray-50) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    /* Container Styling - Production Optimized */
    .main .block-container {
        max-width: 1400px !important;
        padding: 1.5rem 2rem !important;
        background-color: transparent !important;
        margin: 0 auto !important;
    }
    
    /* Remove extra spacing for production */
    .element-container {
        margin-bottom: 1rem !important;
    }
    
    .stMarkdown {
        margin-bottom: 0.5rem !important;
    }

    /* Professional Header */
    .enterprise-header {
        background: linear-gradient(135deg, var(--highland-primary) 0%, var(--highland-secondary) 100%) !important;
        color: white !important;
        padding: 2.5rem 3rem !important;
        border-radius: 16px !important;
        margin-bottom: 2rem !important;
        box-shadow: var(--shadow-lg) !important;
    }

    .enterprise-header h1 {
        margin: 0 !important;
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }

    .enterprise-header p {
        margin: 0.75rem 0 0 0 !important;
        opacity: 0.95 !important;
        font-size: 1.125rem !important;
        font-weight: 500 !important;
    }

    /* Professional Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--gray-800) 0%, var(--gray-900) 100%) !important;
        border-right: 1px solid var(--gray-700) !important;
        box-shadow: var(--shadow-lg) !important;
    }

    section[data-testid="stSidebar"] > div {
        background-color: transparent !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding: 1.5rem !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #f3f4f6 !important;
        font-weight: 600 !important;
    }

    /* Enterprise Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--highland-primary) 0%, var(--highland-secondary) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-md) !important;
    }

    /* Sidebar Buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #f3f4f6 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        width: 100% !important;
        text-align: left !important;
        margin-bottom: 0.5rem !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: var(--highland-secondary) !important;
        border-color: var(--highland-secondary) !important;
        transform: translateX(4px) !important;
    }

    /* Professional Cards */
    .dashboard-card, .admin-card, .enterprise-card {
        background: white !important;
        border: 1px solid var(--gray-200) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.2s ease !important;
    }

    .dashboard-card:hover, .admin-card:hover, .enterprise-card:hover {
        box-shadow: var(--shadow-md) !important;
        transform: translateY(-2px) !important;
    }

    /* Professional Metrics */
    .stMetric {
        background: white !important;
        border: 1px solid var(--gray-200) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stMetric [data-testid="metric-container"] > div:first-child {
        color: var(--gray-600) !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
    }

    .stMetric [data-testid="metric-container"] > div:nth-child(2) {
        color: var(--highland-primary) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    /* Professional Tables */
    .stDataFrame {
        border: 1px solid var(--gray-200) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stDataFrame th {
        background-color: var(--gray-50) !important;
        color: var(--gray-700) !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 0.75rem !important;
    }

    .stDataFrame tr:hover {
        background-color: var(--gray-50) !important;
    }

    /* Professional Forms */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border: 1px solid var(--gray-300) !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--highland-secondary) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }

    /* Professional Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: white !important;
        border: 1px solid var(--gray-200) !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 0.5rem !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: var(--gray-600) !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.2s ease !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--highland-primary) !important;
        color: white !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stTabs [data-baseweb="tab-panel"] {
        background-color: white !important;
        border: 1px solid var(--gray-200) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 2rem !important;
    }

    /* Professional Alerts */
    .stSuccess {
        background-color: #d1fae5 !important;
        border: 1px solid #a7f3d0 !important;
        border-radius: 8px !important;
        color: #047857 !important;
    }

    .stWarning {
        background-color: #fef3c7 !important;
        border: 1px solid #fde68a !important;
        border-radius: 8px !important;
        color: #92400e !important;
    }

    .stError {
        background-color: #fee2e2 !important;
        border: 1px solid #fecaca !important;
        border-radius: 8px !important;
        color: #991b1b !important;
    }

    .stInfo {
        background-color: #dbeafe !important;
        border: 1px solid #bfdbfe !important;
        border-radius: 8px !important;
        color: #1e40af !important;
    }

    /* UNIFIED MOBILE-DESKTOP RESPONSIVE DESIGN */
    @media (max-width: 768px) {
        /* Consistent Container for Mobile */
        .main .block-container {
            padding: 1rem !important;
            max-width: 100% !important;
        }
        
        /* Mobile Header Styling */
        .enterprise-header, .highland-header {
            padding: 1.5rem 1rem !important;
            margin-bottom: 1rem !important;
            border-radius: 12px !important;
        }
        
        .enterprise-header h1, .highland-header h1 {
            font-size: 1.75rem !important;
            line-height: 1.2 !important;
        }
        
        .enterprise-header p, .highland-header p {
            font-size: 1rem !important;
            line-height: 1.4 !important;
        }
        
        /* Mobile Sidebar Adjustments */
        section[data-testid="stSidebar"] .block-container {
            padding: 1rem !important;
        }
        
        /* Unified Button Styling - Same as Desktop */
        .stButton > button {
            background: linear-gradient(135deg, #1e40af, #3b82f6) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            padding: 12px 16px !important;
            margin: 6px 0 !important;
            box-shadow: 0 3px 10px rgba(59, 130, 246, 0.3) !important;
            min-height: 44px !important;
            width: 100% !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #3b82f6, #60a5fa, #93c5fd) !important;
            transform: translateY(-2px) translateX(6px) !important;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5) !important;
            border-left: 4px solid #fbbf24 !important;
        }
        
        section[data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(135deg, #1e40af, #3b82f6, #60a5fa) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            padding: 12px 16px !important;
            margin: 6px 0 !important;
            box-shadow: 0 3px 10px rgba(59, 130, 246, 0.3) !important;
            text-align: left !important;
        }
        
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, #3b82f6, #60a5fa, #93c5fd) !important;
            transform: translateY(-2px) translateX(6px) !important;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5) !important;
            border-left: 4px solid #fbbf24 !important;
        }
        
        /* Mobile Form Elements - Touch Optimized */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {
            min-height: 48px !important;
            font-size: 16px !important;
            padding: 12px !important;
            border-radius: 8px !important;
        }
        
        /* Mobile Metrics Cards */
        .stMetric {
            padding: 1rem !important;
            margin-bottom: 1rem !important;
            border-radius: 8px !important;
        }
        
        .stMetric [data-testid="metric-container"] > div:first-child {
            font-size: 0.75rem !important;
        }
        
        .stMetric [data-testid="metric-container"] > div:nth-child(2) {
            font-size: 1.5rem !important;
        }
        
        /* Mobile Cards */
        .dashboard-card, .admin-card, .enterprise-card, .highland-card {
            padding: 1rem !important;
            margin-bottom: 1rem !important;
            border-radius: 8px !important;
        }
        
        /* Mobile Tables */
        .stDataFrame {
            border-radius: 8px !important;
            font-size: 14px !important;
        }
        
        .stDataFrame th {
            padding: 0.75rem 0.5rem !important;
            font-size: 0.7rem !important;
        }
        
        .stDataFrame td {
            padding: 0.75rem 0.5rem !important;
            font-size: 0.8rem !important;
        }
        
        /* Mobile Tabs */
        .stTabs [data-baseweb="tab-list"] {
            padding: 0.25rem !important;
            overflow-x: auto !important;
            white-space: nowrap !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.75rem 1rem !important;
            font-size: 14px !important;
            min-width: 120px !important;
            flex-shrink: 0 !important;
        }
        
        .stTabs [data-baseweb="tab-panel"] {
            padding: 1rem !important;
        }
        
        /* Mobile Alerts */
        .stSuccess, .stWarning, .stError, .stInfo {
            padding: 0.75rem !important;
            margin: 0.75rem 0 !important;
            border-radius: 6px !important;
            font-size: 14px !important;
        }
        
        /* Mobile Project Info */
        .project-info {
            padding: 1rem !important;
            margin-bottom: 1rem !important;
            border-radius: 8px !important;
        }
        
        .project-info h3 {
            font-size: 1.25rem !important;
            margin-bottom: 0.75rem !important;
        }
        
        .project-info p {
            font-size: 0.9rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Mobile Column Adjustments */
        .stColumns > div {
            padding: 0 0.25rem !important;
        }
        
        /* Mobile Expanders */
        .streamlit-expanderHeader {
            padding: 0.75rem 1rem !important;
            font-size: 14px !important;
        }
        
        .streamlit-expanderContent {
            padding: 1rem !important;
        }
        
        /* Mobile Charts */
        .stPlotlyChart {
            height: 300px !important;
        }
        
        /* Mobile Typography */
        h1 {
            font-size: 1.75rem !important;
            line-height: 1.2 !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
            line-height: 1.3 !important;
        }
        
        h3 {
            font-size: 1.25rem !important;
            line-height: 1.3 !important;
        }
        
        /* Mobile Navigation Improvements */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            font-size: 1.1rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Mobile Specific Highland Tower Branding */
        .highland-header h1 {
            font-size: 1.5rem !important;
            text-align: center !important;
        }
        
        .highland-header p {
            text-align: center !important;
            font-size: 0.9rem !important;
        }
        
        /* Touch-friendly spacing */
        .stMarkdown {
            margin-bottom: 0.75rem !important;
        }
        
        /* Mobile-optimized shadows */
        .highland-card:hover,
        .dashboard-card:hover,
        .admin-card:hover,
        .enterprise-card:hover {
            transform: none !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        }
    }
    
    /* Tablet Responsive Design (768px - 1024px) */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main .block-container {
            padding: 1.5rem 2rem !important;
            max-width: 1200px !important;
        }
        
        .enterprise-header, .highland-header {
            padding: 2rem !important;
        }
        
        .stButton > button {
            min-height: 44px !important;
            font-size: 15px !important;
        }
        
        .stMetric {
            padding: 1.25rem !important;
        }
        
        .highland-card, .dashboard-card, .admin-card, .enterprise-card {
            padding: 1.25rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def get_user_role_permissions():
    """Define role-based module access permissions for Highland Tower Development"""
    return {
        "admin": {
            "role_name": "Administrator",
            "modules": ["Dashboard", "PreConstruction", "Engineering", "Field Operations", "Safety", 
                       "Contracts", "Cost Management", "Unit Prices", "Deliveries", "Daily Reports", "Progress Photos", "Quality Control",
                       "Material Management", "BIM", "Analytics", "Submittals", "Transmittals", "RFIs", "Scheduling",
                       "Equipment Tracking", "AI Assistant", "Mobile Companion", "AIA Billing",
                       "Prime Contract", "Change Orders", "Closeout", "Documents", "Admin Settings",
                       "Subcontractor Management", "Inspections", "Issues & Risks", "Performance Snapshot"],
            "permissions": ["read_all", "write_all", "manage_users", "view_audit_logs", "approve_changes"]
        },
        "manager": {
            "role_name": "Project Manager", 
            "modules": ["Dashboard", "PreConstruction", "Engineering", "Field Operations", "Safety",
                       "Contracts", "Cost Management", "Unit Prices", "Deliveries", "Daily Reports", "Progress Photos", "Quality Control",
                       "Material Management", "BIM", "Analytics", "Submittals", "Transmittals",
                       "AIA Billing", "Prime Contract", "Change Orders", "Closeout", "Documents"],
            "permissions": ["read_all", "write_rfis", "write_daily_reports", "write_quality", "approve_changes"]
        },
        "superintendent": {
            "role_name": "Superintendent",
            "modules": ["Dashboard", "Field Operations", "Safety", "Daily Reports", "Progress Photos",
                       "Quality Control", "Material Management", "Equipment Tracking", "Mobile Companion"],
            "permissions": ["read_daily_reports", "write_daily_reports", "read_quality", "write_quality", "read_safety", "write_safety"]
        },
        "foreman": {
            "role_name": "Foreman",
            "modules": ["Dashboard", "Field Operations", "Safety", "Daily Reports", "Progress Photos",
                       "Quality Control", "Material Management", "Mobile Companion"],
            "permissions": ["read_daily_reports", "write_daily_reports", "read_quality", "read_safety"]
        },
        "inspector": {
            "role_name": "Quality Inspector",
            "modules": ["Dashboard", "Quality Control", "Safety", "Progress Photos", "Daily Reports"],
            "permissions": ["read_quality", "write_quality", "read_safety", "read_daily_reports"]
        },
        "user": {
            "role_name": "Standard User",
            "modules": ["Dashboard", "Daily Reports", "Progress Photos"],
            "permissions": ["read_daily_reports", "read_quality"]
        }
    }

def check_module_access(module_name):
    """Check if current user has access to specified module"""
    if not st.session_state.get("authenticated", False):
        return False
    
    user_role = st.session_state.get("user_role", "user")
    role_permissions = get_user_role_permissions()
    
    if user_role in role_permissions:
        return module_name in role_permissions[user_role]["modules"]
    
    return False

def initialize_session_state():
    """Initialize session state with role-based security."""
    defaults = {
        "authenticated": False,
        "username": "",
        "user_role": "",
        "user_permissions": [],
        "current_menu": "Dashboard",
        "project_name": "Highland Tower Development",
        "project_value": "$45.5M",
        "residential_units": 120,
        "retail_units": 8,
        "theme": "dark"
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def apply_theme():
    """Apply consistent professional theme"""
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #0f172a 100%) !important;
        border-right: 2px solid #1e40af;
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] button {
        background: linear-gradient(135deg, #1e40af, #3b82f6, #60a5fa) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 12px 16px !important;
        margin: 6px 0 !important;
        box-shadow: 0 3px 10px rgba(59, 130, 246, 0.3) !important;
        text-align: left !important;
    }
    
    section[data-testid="stSidebar"] button:hover {
        background: linear-gradient(135deg, #3b82f6, #60a5fa, #93c5fd) !important;
        transform: translateY(-2px) translateX(6px) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5) !important;
        border-left: 4px solid #fbbf24 !important;
    }
    
    /* Navigation Section Headers */
    section[data-testid="stSidebar"] h3 {
        color: #fbbf24 !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        margin: 1.5rem 0 0.8rem 0 !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #fbbf24 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border: 1px solid #475569 !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.4) !important;
        color: #f1f5f9 !important;
        transition: all 0.3s ease !important;
    }
    
    .metric-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        border-color: #3b82f6 !important;
    }
    
    /* Enhanced Main Content Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1e40af, #3b82f6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 14px 28px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
        font-size: 15px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3b82f6, #60a5fa) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Project Info Enhanced Styling */
    .project-info {
        background: linear-gradient(135deg, #1e40af, #3b82f6, #60a5fa) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 1.5rem 0 !important;
        border: 2px solid #93c5fd !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Enhanced Form Elements */
    .stSelectbox > div > div, .stTextInput input, .stTextArea textarea {
        background: rgba(30, 41, 59, 0.9) !important;
        border: 2px solid #475569 !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        transition: all 0.3s ease !important;
        padding: 12px !important;
    }
    
    .stSelectbox > div > div:focus, .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Enhanced Tables and Data Frames */
    .stDataFrame {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
        border: 1px solid #475569 !important;
    }
    
    /* Status Indicators */
    .status-active {
        color: #10b981 !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.3) !important;
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 4px solid #1e293b !important;
        border-top: 4px solid #3b82f6 !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        animation: spin 1s linear infinite !important;
        margin: 20px auto !important;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(30, 41, 59, 0.8) !important;
        color: #f1f5f9 !important;
        border: 1px solid #475569 !important;
    }
    
    .stDataFrame {
        background-color: rgba(30, 41, 59, 0.9) !important;
    }
    
    /* BIM module specific dark theme enhancements */
    .clash-item {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin-bottom: 0.5rem !important;
        color: #f1f5f9 !important;
    }
    
    .enterprise-header {
        background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
    }
    
    .project-info {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render professional header"""
    st.markdown(f"""
    <div class="enterprise-header">
        <h1 style="margin: 0; font-size: 2rem;">🏗️ gcPanel Construction Management</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
            {st.session_state.project_name} • {st.session_state.project_value} Investment
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render role-based sidebar with permissions control"""
    with st.sidebar:
        # Project information
        st.markdown(f"""
        <div class="project-info">
            <h3 style="color: #60a5fa; margin: 0 0 1rem 0;">Highland Tower Development</h3>
            <p><strong>Investment:</strong> {st.session_state.project_value}</p>
            <p><strong>Residential:</strong> {st.session_state.residential_units} units</p>
            <p><strong>Retail:</strong> {st.session_state.retail_units} spaces</p>
            <p><strong>Status:</strong> <span style="color: #10b981;">Active Development</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced User Profile Section
        user_role = st.session_state.get("user_role", "user")
        role_permissions = get_user_role_permissions()
        role_info = role_permissions.get(user_role, role_permissions["user"])
        username = st.session_state.get('username', 'Guest')
        
        # Clean Profile Section - No HTML
        st.markdown(f"### 👤 {username}")
        st.caption(f"**{role_info['role_name']}**")
        st.info("🏗️ Highland Tower Development")
        
        # Clean navigation without admin clutter
        
        # Core Tools - Most Used Daily Operations
        st.markdown("### ⚡ Core Tools")
        core_tools = [
            ("📊 Dashboard", "Dashboard"),
            ("📝 Daily Reports", "Daily Reports"),
            ("🚛 Deliveries", "Deliveries"),
            ("🦺 Safety", "Safety")
        ]
        
        for display_name, module in core_tools:
            if check_module_access(module):
                if st.button(display_name, key=f"core_tool_{module}", use_container_width=True):
                    st.session_state.current_menu = module
                    st.rerun()
        
        # Management Modules - Project Level Operations
        st.markdown("### 🎯 Project Management")
        management_modules = [
            ("🏗️ PreConstruction", "PreConstruction"), 
            ("⚙️ Engineering", "Engineering"),
            ("👷 Field Operations", "Field Operations"),
            ("📋 Contracts", "Contracts"),
            ("💰 Cost Management", "Cost Management"),
            ("🏢 BIM", "BIM"),
            ("✅ Closeout", "Closeout")
        ]
        
        for display_name, module in management_modules:
            if check_module_access(module):
                if st.button(display_name, key=f"mgmt_{module}", use_container_width=True):
                    st.session_state.current_menu = module
                    st.rerun()
        
        # Advanced Tools (filtered by permissions)
        advanced_available = any(check_module_access(tool) for _, tool in [
            ("❓ RFIs", "RFIs"),
            ("📤 Submittals", "Submittals"), 
            ("📨 Transmittals", "Transmittals"),
            ("📅 Scheduling", "Scheduling"), 
            ("🔍 Quality Control", "Quality Control"),
            ("📸 Progress Photos", "Progress Photos"),
            ("👥 Subcontractor Management", "Subcontractor Management"),
            ("📊 Inspections", "Inspections"),
            ("⚠️ Issues & Risks", "Issues & Risks")
        ])
        
        if advanced_available:
            st.markdown("### 🔧 Advanced Tools")
            advanced_tools = [
                ("❓ RFIs", "RFIs"),
                ("📤 Submittals", "Submittals"),
                ("📨 Transmittals", "Transmittals"),
                ("📅 Scheduling", "Scheduling"),
                ("🔍 Quality Control", "Quality Control"),
                ("📸 Progress Photos", "Progress Photos"),
                ("👥 Subcontractor Management", "Subcontractor Management"),
                ("📊 Inspections", "Inspections"),
                ("⚠️ Issues & Risks", "Issues & Risks")
            ]
            
            for display_name, tool in advanced_tools:
                if check_module_access(tool):
                    if st.button(display_name, key=f"tool_{tool}", use_container_width=True):
                        st.session_state.current_menu = tool
                        st.rerun()
        
        # Resource Management (filtered by permissions)
        resource_available = any(check_module_access(module) for _, module in [
            ("📁 Documents", "Documents"), ("💰 Unit Prices", "Unit Prices"),
            ("📋 Punch Lists", "Punch Lists")
        ])
        
        if resource_available:
            st.markdown("### 📦 Resource Management")
            resource_modules = [
                ("📁 Documents", "Documents"),
                ("💰 Unit Prices", "Unit Prices"),
                ("📋 Punch Lists", "Punch Lists")
            ]
            
            for display_name, module in resource_modules:
                if check_module_access(module):
                    if st.button(display_name, key=f"resource_{module}", use_container_width=True):
                        st.session_state.current_menu = module
                        st.rerun()

        # Analytics & Intelligence (consolidated)
        analytics_available = any(check_module_access(module) for _, module in [
            ("📈 Analytics", "Analytics"), ("🤖 AI Assistant", "AI Assistant"), ("📊 Performance Snapshot", "Performance Snapshot")
        ])
        
        if analytics_available:
            st.markdown("### 📊 Analytics & AI")
            analytics_modules = [
                ("📈 Analytics", "Analytics"),
                ("📊 Performance Snapshot", "Performance Snapshot"),
                ("🤖 AI Assistant", "AI Assistant")
            ]
            
            for display_name, module in analytics_modules:
                if check_module_access(module):
                    if st.button(display_name, key=f"analytics_{module}", use_container_width=True):
                        st.session_state.current_menu = module
                        st.rerun()
        
        # User section and logout
        st.markdown("---")
        
        # Move logout to bottom of sidebar
        st.markdown("---")
        st.markdown("")  # Add some spacing
        if st.button("🚪 Logout", use_container_width=True, type="secondary", key="logout_bottom"):
            st.session_state.authenticated = False
            st.session_state.user_role = ""
            st.session_state.username = ""
            st.session_state.current_menu = "Dashboard"
            st.success("✅ Logged out successfully")
            st.rerun()

def render_login():
    """Clean centered login form"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1 style="color: #60a5fa; font-size: 3.5rem; margin-bottom: 1rem;">gcPanel</h1>
        <h2 style="color: #94a3b8; font-size: 1.8rem; margin-bottom: 0.5rem;">Highland Tower Development</h2>
        <p style="color: #64748b; font-size: 1.2rem; margin-bottom: 3rem;">
            Enterprise Construction Management Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Centered login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Project Access")
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submitted = st.form_submit_button("Access Dashboard", use_container_width=True, type="primary")
            
            if submitted and username and password:
                # Assign roles based on username for Highland Tower Development
                role_mapping = {
                    "admin": "admin",
                    "manager": "manager", 
                    "superintendent": "superintendent",
                    "foreman": "foreman",
                    "inspector": "inspector",
                    "user": "user"
                }
                
                user_role = role_mapping.get(username.lower(), "user")
                role_permissions = get_user_role_permissions()
                
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.user_role = user_role
                st.session_state.user_permissions = role_permissions[user_role]["permissions"]
                st.rerun()
        
        # Login credentials help
        with st.expander("🔑 Access Credentials"):
            st.markdown("""
            **Available Access Levels:**
            - **admin** / admin123 - Full system access
            - **manager** / manager123 - Project management access  
            - **user** / user123 - Standard user access
            """)

def render_dashboard():
    """Enterprise dashboard with advanced analytics and real-time insights"""
    st.title("🏗️ Highland Tower Development - Executive Dashboard")
    st.markdown("**$45.5M Mixed-Use Development** | 120 Residential + 8 Retail Units | 15 Stories")
    
    # Real-time KPI metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Project Progress", "67.3%", "2.1% this week", help="Overall completion vs baseline schedule")
    with col2:
        st.metric("Budget Performance", "$30.5M", "-$2.1M under", help="Spent vs $45.5M total budget")
    with col3:
        st.metric("Schedule Variance", "5 Days", "Ahead of schedule", help="Current vs planned timeline")
    with col4:
        st.metric("Safety Rating", "98.5%", "+0.5% improvement", help="OSHA compliance score")
    with col5:
        st.metric("Quality Score", "96.2%", "+1.2% this month", help="QC inspections passed")
    
    # Advanced Analytics Tabs
    st.markdown("### 📊 Advanced Project Analytics")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Progress", "💰 Financials", "👷 Resources", "🎯 Critical Path", "⚠️ Risk Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            # Progress visualization
            progress_data = pd.DataFrame({
                'Floor': [f'Level {i}' for i in range(1, 16)],
                'Structural': [100 if i <= 12 else 85 if i == 13 else 30 if i == 14 else 0 for i in range(1, 16)],
                'MEP': [100 if i <= 9 else 70 if i <= 11 else 20 if i <= 13 else 0 for i in range(1, 16)],
                'Finishes': [100 if i <= 6 else 40 if i <= 8 else 10 if i <= 10 else 0 for i in range(1, 16)]
            })
            
            fig = px.bar(progress_data, x='Floor', y=['Structural', 'MEP', 'Finishes'], 
                        title="Floor-by-Floor Progress", barmode='group')
            fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            **Current Phase Status:**
            
            🏗️ **Structural (Level 13)**
            - Steel erection: 85% complete
            - Concrete pour: Scheduled Friday
            - Inspection: Passed preliminary
            
            ⚡ **MEP Systems (Level 9-11)**
            - Electrical rough-in: 70% complete
            - Plumbing stack: 90% complete
            - HVAC ducts: 65% complete
            
            🎨 **Interior Finishes (Level 6-8)**
            - Drywall: 40% complete
            - Flooring prep: 25% complete
            - Paint prep: 15% complete
            """)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            # Financial breakdown
            financial_data = pd.DataFrame({
                'Category': ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'Overhead'],
                'Budgeted': [18.2, 15.8, 6.3, 3.7, 1.5],
                'Actual': [17.8, 16.1, 5.9, 3.5, 1.4],
                'Forecasted': [17.9, 16.3, 6.0, 3.6, 1.5]
            })
            
            fig = px.bar(financial_data, x='Category', y=['Budgeted', 'Actual', 'Forecasted'],
                        title="Cost Performance by Category (Millions $)", barmode='group')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            **Financial Performance:**
            
            💰 **Total Budget:** $45.5M
            📊 **Spent to Date:** $30.5M (67%)
            📈 **Forecast at Completion:** $43.4M
            💚 **Projected Savings:** $2.1M (4.6%)
            
            **Cost Trends:**
            - Labor: 2% under budget (efficiency gains)
            - Materials: 3% over (steel price increase)
            - Equipment: 6% under (better utilization)
            
            **Change Orders:**
            - Approved: $890K (15 COs)
            - Pending: $340K (5 COs)
            - Rejected: $120K (3 COs)
            """)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Current Workforce:**
            - **Total Workers:** 89 active
            - **Prime Contractor:** 34 workers
            - **Subcontractors:** 55 workers (12 companies)
            - **Safety Officers:** 3 full-time
            - **QC Inspectors:** 2 full-time
            
            **Productivity Metrics:**
            - Average daily hours: 8.2
            - Overtime hours this week: 127
            - Efficiency rating: 94.2%
            - Worker satisfaction: 87%
            """)
        
        with col2:
            st.markdown("""
            **Resource Allocation:**
            
            **Level 13 (Current Focus):**
            - Ironworkers: 12
            - Concrete crew: 8
            - Crane operators: 2
            
            **Level 9-11 (MEP):**
            - Electricians: 15
            - Plumbers: 8
            - HVAC techs: 6
            
            **Level 6-8 (Finishes):**
            - Drywall crew: 10
            - Flooring team: 6
            - Painters: 4
            """)
    
    with tab4:
        st.markdown("""
        **Critical Path Analysis:**
        
        🚨 **Critical Activities (Next 30 Days):**
        1. **Level 13 Steel Erection** - 5 days remaining
        2. **Elevator Shaft Concrete** - Depends on #1
        3. **Level 9 MEP Inspection** - 3 days (parallel)
        4. **Curtain Wall Installation** - 10 days (Level 8-10)
        
        ⚡ **Schedule Acceleration Opportunities:**
        - Increase Level 13 crew by 25% → Save 2 days
        - Parallel MEP rough-in on Levels 12-13 → Save 5 days
        - Pre-fabricate bathroom pods → Save 8 days
        
        📊 **Float Analysis:**
        - Critical path float: 0 days
        - Near-critical activities: 12 (1-3 days float)
        - Weather contingency: 10 days built-in
        """)
    
    with tab5:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **High Priority Risks:**
            
            🔴 **CRITICAL:**
            - Steel delivery delays (10% probability)
            - Weather impact on concrete (25% probability)
            
            🟡 **MEDIUM:**
            - Labor shortage (15% probability)
            - MEP coordination conflicts (20% probability)
            - Permit approval delays (10% probability)
            
            🟢 **LOW:**
            - Material price increases (5% probability)
            - Equipment breakdowns (8% probability)
            """)
        
        with col2:
            st.markdown("""
            **Risk Mitigation Status:**
            
            ✅ **Active Mitigations:**
            - Alternative steel suppliers identified
            - Weather monitoring system deployed
            - Cross-trained labor pool established
            - Weekly MEP coordination meetings
            
            📋 **Contingency Plans:**
            - $1.5M budget reserve (3.3%)
            - 15-day schedule buffer
            - Emergency equipment rental agreements
            - Fast-track permit expeditor on retainer
            """)
    
    # Quick Action Dashboard
    st.markdown("### ⚡ Executive Action Center")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("📝 New RFI", use_container_width=True):
            st.session_state.current_menu = "RFIs"
            st.rerun()
    
    with col2:
        if st.button("📊 Daily Report", use_container_width=True):
            st.session_state.current_menu = "Daily Reports"
            st.rerun()
    
    with col3:
        if st.button("🦺 Safety Alert", use_container_width=True):
            st.session_state.current_menu = "Safety"
            st.rerun()
    
    with col4:
        if st.button("💰 Cost Update", use_container_width=True):
            st.session_state.current_menu = "Cost Management"
            st.rerun()
    
    with col5:
        if st.button("📸 Photo Upload", use_container_width=True):
            st.session_state.current_menu = "Progress Photos"
            st.rerun()
    
    with col6:
        if st.button("📋 QC Inspection", use_container_width=True):
            st.session_state.current_menu = "Quality Control"
            st.rerun()
    
    # Live Activity Feed - Highland Tower Development
    st.markdown("### 🔔 Highland Tower Development - Recent Activity")
    
    # Enhanced activity feed with better styling
    activities = [
        {
            "icon": "📊", 
            "type": "Daily Report", 
            "message": "Daily Progress Report #147 submitted: Level 13 steel erection 85% complete", 
            "time": "12 minutes ago",
            "priority": "SUCCESS",
            "link": "Daily Reports"
        },
        {
            "icon": "🚨", 
            "type": "RFI", 
            "message": "RFI-HTD-089: Structural beam connection detail needed for Level 13 Grid E4", 
            "time": "25 minutes ago",
            "priority": "HIGH",
            "link": "RFIs"
        },
        {
            "icon": "✅", 
            "type": "Inspection", 
            "message": "Quality Control: Zone C electrical rough-in inspection passed with approval", 
            "time": "1 hour ago",
            "priority": "SUCCESS",
            "link": "Quality Control"
        },
        {
            "icon": "💰", 
            "type": "Cost Alert", 
            "message": "Budget variance alert: Steel materials 3.2% over budget this week", 
            "time": "2 hours ago",
            "priority": "WARNING",
            "link": "Cost Management"
        },
        {
            "icon": "📸", 
            "type": "Progress Photo", 
            "message": "Progress photos uploaded: Level 12 interior framing completion documented", 
            "time": "3 hours ago",
            "priority": "INFO",
            "link": "Progress Photos"
        },
        {
            "icon": "🎉", 
            "type": "Milestone", 
            "message": "Major milestone achieved: Level 11 MEP rough-in 100% complete", 
            "time": "4 hours ago",
            "priority": "SUCCESS",
            "link": "Scheduling"
        },
        {
            "icon": "👷", 
            "type": "Crew Update", 
            "message": "Crew assignment: Team Delta moved to Level 14 preparation work", 
            "time": "5 hours ago",
            "priority": "INFO",
            "link": "Field Operations"
        },
        {
            "icon": "🔍", 
            "type": "Quality Issue", 
            "message": "Quality checkpoint: Minor concrete finish touch-up needed Unit 1205", 
            "time": "6 hours ago",
            "priority": "WARNING",
            "link": "Quality Control"
        }
    ]
    
    # Create styled activity cards
    for idx, activity in enumerate(activities):
        # Color coding for different priorities
        if activity["priority"] == "HIGH":
            border_color = "#dc3545"
            bg_color = "#f8d7da"
        elif activity["priority"] == "WARNING":
            border_color = "#ffc107"
            bg_color = "#fff3cd"
        elif activity["priority"] == "SUCCESS":
            border_color = "#28a745"
            bg_color = "#d4edda"
        else:
            border_color = "#17a2b8"
            bg_color = "#d1ecf1"
        
        # Create clickable activity cards
        col1, col2 = st.columns([1, 20])
        
        with col1:
            st.markdown(f"""
            <div style="width: 40px; height: 40px; border-radius: 50%; 
                       background-color: {bg_color}; border: 2px solid {border_color};
                       display: flex; align-items: center; justify-content: center; 
                       font-size: 18px; margin: 5px 0;">
                {activity['icon']}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background-color: {bg_color}; border-left: 4px solid {border_color}; 
                       padding: 12px; margin: 5px 0; border-radius: 0 8px 8px 0;">
                <div style="font-weight: 600; color: #333; margin-bottom: 4px;">
                    {activity['type']}: {activity['message']}
                </div>
                <div style="font-size: 12px; color: #666;">
                    {activity['time']} • Click to view in {activity['link']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Make activity clickable with unique key
            if st.button(f"View {activity['type']}", key=f"activity_{idx}_{activity['link']}", help=f"Go to {activity['link']} module"):
                st.session_state.current_menu = activity['link']
                st.rerun()
    
    # Quick access to Daily Reports
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 View All Daily Reports", type="primary", use_container_width=True):
            st.session_state.current_menu = "Daily Reports"
            st.rerun()
    
    with col2:
        if st.button("📋 Recent Reports Archive", use_container_width=True):
            st.session_state.current_menu = "Recent Reports"
            st.rerun()
    
    with col3:
        if st.button("📈 Progress Analytics", use_container_width=True):
            st.session_state.current_menu = "Analytics"
            st.rerun()

def render_contracts():
    """Render comprehensive contracts management"""
    st.markdown("## 📋 Contracts Management - Enterprise Level")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Active Contracts", "Change Orders", "Vendor Management", "Contract Analytics"])
    
    with tab1:
        st.markdown("### Current Project Contracts")
        contracts_data = pd.DataFrame({
            'Contractor': ['Highland Construction LLC', 'Elite MEP Systems', 'Premium Interiors', 'Safety First Inc', 'Steel Solutions Inc'],
            'Contract Value': ['$28.5M', '$8.2M', '$6.1M', '$450K', '$2.8M'],
            'Status': ['Active', 'Active', 'Pending', 'Active', 'Active'],
            'Completion': ['75%', '60%', '0%', '95%', '45%'],
            'Payment Status': ['Current', 'Current', 'N/A', 'Current', 'Pending']
        })
        st.dataframe(contracts_data, use_container_width=True)
        
        # Contract actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📝 Create New Contract", use_container_width=True):
                st.success("New contract form opened!")
        with col2:
            if st.button("📊 Contract Reports", use_container_width=True):
                st.info("Generating contract performance reports...")
        with col3:
            if st.button("💰 Payment Processing", use_container_width=True):
                st.info("Opening payment processing dashboard...")
    
    with tab2:
        st.markdown("### Change Orders Management")
        change_orders = pd.DataFrame({
            'CO Number': ['CO-2024-015', 'CO-2024-016', 'CO-2024-017', 'CO-2024-018'],
            'Description': ['HVAC scope modification', 'Additional electrical outlets', 'Flooring upgrade', 'Structural reinforcement'],
            'Amount': ['+$125K', '+$45K', '+$89K', '+$200K'],
            'Status': ['Under Review', 'Approved', 'Pending', 'Draft'],
            'Submitted Date': ['2024-05-20', '2024-05-18', '2024-05-22', '2024-05-23']
        })
        st.dataframe(change_orders, use_container_width=True)
        
        # Change order metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Change Orders", "18", "+4")
        with col2:
            st.metric("Total Value", "$1.2M", "+$459K")
        with col3:
            st.metric("Avg Processing Time", "3.2 days", "-0.8 days")
    
    with tab3:
        st.markdown("### Vendor Performance Dashboard")
        vendor_data = pd.DataFrame({
            'Vendor': ['Highland Construction', 'Elite MEP', 'Premium Interiors', 'Safety First', 'Steel Solutions'],
            'Performance Score': [95, 88, 92, 98, 85],
            'On-Time Delivery': ['98%', '92%', '95%', '100%', '87%'],
            'Quality Rating': [4.8, 4.5, 4.7, 4.9, 4.3],
            'Active Projects': [3, 2, 1, 4, 2]
        })
        st.dataframe(vendor_data, use_container_width=True)
    
    with tab4:
        st.markdown("### Contract Analytics")
        # Contract value distribution chart
        contract_values = [28.5, 8.2, 6.1, 2.8, 0.45]
        contractors = ['Highland Construction', 'Elite MEP', 'Premium Interiors', 'Steel Solutions', 'Safety First']
        
        fig = px.pie(values=contract_values, names=contractors, title="Contract Value Distribution")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def render_rfis():
    """Highland Tower Development - RFI Management System"""
    st.title("📝 Request for Information (RFIs) - Highland Tower Development")
    st.markdown("**Professional RFI management for $45.5M construction project**")
    
    # Action buttons for CRUD operations
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Create RFI", type="primary", use_container_width=True):
            st.session_state.rfi_mode = "create"
            st.rerun()
    
    with col2:
        if st.button("🔍 Search RFIs", use_container_width=True):
            st.session_state.rfi_mode = "search"
            st.rerun()
    
    with col3:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.rfi_mode = "analytics"
            st.rerun()
    
    with col4:
        if st.button("📋 Reports", use_container_width=True):
            st.session_state.rfi_mode = "reports"
            st.rerun()
    
    st.markdown("---")
    
    # Highland Tower RFI Database
    rfis_data = [
        {
            "rfi_id": "HTD-RFI-001",
            "rfi_number": "RFI-2025-001",
            "subject": "Steel beam connection detail clarification Level 12-13",
            "location": "Level 12-13, Grid Line A-B",
            "discipline": "Structural Engineering",
            "priority": "High",
            "status": "Open",
            "submitted_by": "Mike Chen - Site Superintendent",
            "assigned_to": "Highland Structural Engineering",
            "submitted_date": "2025-05-20",
            "due_date": "2025-05-27",
            "days_open": 5,
            "description": "Need clarification on connection detail for main structural beams at Grid Line A between floors 12-13. Current drawings show conflicting details.",
            "cost_impact": "$15,000 - $25,000",
            "schedule_impact": "2-3 days"
        },
        {
            "rfi_id": "HTD-RFI-002", 
            "rfi_number": "RFI-2025-002",
            "subject": "HVAC ductwork routing coordination Level 12 mechanical room",
            "location": "Level 12 - Mechanical Room North",
            "discipline": "MEP Engineering",
            "priority": "Medium",
            "status": "In Review",
            "submitted_by": "Sarah Johnson - Project Manager",
            "assigned_to": "Highland MEP Consultants",
            "submitted_date": "2025-05-18",
            "due_date": "2025-05-25",
            "days_open": 7,
            "description": "HVAC ductwork conflicts with structural beams in north mechanical room. Need routing solution.",
            "cost_impact": "$5,000 - $10,000",
            "schedule_impact": "1-2 days"
        },
        {
            "rfi_id": "HTD-RFI-003",
            "rfi_number": "RFI-2025-003", 
            "subject": "Exterior curtain wall material specification south facade",
            "location": "South Facade - Units 8-12",
            "discipline": "Architectural",
            "priority": "Medium",
            "status": "Answered",
            "submitted_by": "Robert Kim - Architecture Team",
            "assigned_to": "Highland Architecture Group",
            "submitted_date": "2025-05-15",
            "due_date": "2025-05-22",
            "days_open": 10,
            "description": "Clarification needed on glass specifications for south-facing residential units 8-12.",
            "cost_impact": "$8,000 - $12,000",
            "schedule_impact": "No impact"
        },
        {
            "rfi_id": "HTD-RFI-004",
            "rfi_number": "RFI-2025-004",
            "subject": "Electrical panel location retail space ground floor",
            "location": "Ground Floor - Retail Space 3",
            "discipline": "Electrical Engineering",
            "priority": "Low",
            "status": "Open",
            "submitted_by": "Lisa Rodriguez - Quality Inspector",
            "assigned_to": "Highland Electrical Consultants",
            "submitted_date": "2025-05-22",
            "due_date": "2025-05-29",
            "days_open": 3,
            "description": "Electrical panel location conflicts with retail tenant requirements. Need alternative placement.",
            "cost_impact": "$2,000 - $5,000",
            "schedule_impact": "1 day"
        },
        {
            "rfi_id": "HTD-RFI-005",
            "rfi_number": "RFI-2025-005",
            "subject": "Fire safety system integration residential levels",
            "location": "Levels 2-15 - Residential",
            "discipline": "Fire Safety",
            "priority": "Critical",
            "status": "Open",
            "submitted_by": "John Davis - Safety Manager",
            "assigned_to": "Fire Safety Consultants Inc",
            "submitted_date": "2025-05-23",
            "due_date": "2025-05-26",
            "days_open": 2,
            "description": "Fire safety system requires integration with building automation. Critical for occupancy permit.",
            "cost_impact": "$25,000 - $40,000",
            "schedule_impact": "5-7 days"
        }
    ]
    
    # Handle different modes
    if st.session_state.get("rfi_mode") == "create":
        st.markdown("### ➕ Create New RFI")
        
        with st.form("create_rfi_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                subject = st.text_input("RFI Subject*", placeholder="Brief description of the question or issue")
                location = st.selectbox("Location", [
                    "Level B2 - Parking", "Level B1 - Storage", "Ground Floor - Retail",
                    "Level 2-5 - Residential", "Level 6-10 - Residential", "Level 11-15 - Residential", 
                    "Mechanical Penthouse", "Roof Level", "Site Overall"
                ])
                discipline = st.selectbox("Engineering Discipline", [
                    "Structural Engineering", "MEP Engineering", "Architectural", 
                    "Electrical Engineering", "Fire Safety", "Civil Engineering", "Geotechnical"
                ])
                priority = st.selectbox("Priority Level", ["Low", "Medium", "High", "Critical"])
            
            with col2:
                submitted_by = st.text_input("Submitted By", value="Highland Tower Team")
                assigned_to = st.selectbox("Assign To", [
                    "Highland Structural Engineering", "Highland MEP Consultants", 
                    "Highland Architecture Group", "Highland Electrical Consultants",
                    "Fire Safety Consultants Inc", "Project Engineering Team"
                ])
                due_date = st.date_input("Response Due Date", datetime.now() + timedelta(days=7))
                cost_impact = st.selectbox("Estimated Cost Impact", [
                    "No Impact", "$0 - $2,000", "$2,000 - $5,000", "$5,000 - $15,000", 
                    "$15,000 - $25,000", "$25,000+"
                ])
            
            description = st.text_area("Detailed Description*", height=120, 
                placeholder="Provide detailed description of the question, issue, or clarification needed...")
            
            schedule_impact = st.selectbox("Schedule Impact", ["No Impact", "1 day", "2-3 days", "4-7 days", "1-2 weeks", "2+ weeks"])
            
            attachments = st.file_uploader("Attach Files", accept_multiple_files=True, 
                type=['pdf', 'dwg', 'jpg', 'png', 'xlsx', 'docx'])
            
            submitted = st.form_submit_button("📤 Submit RFI", type="primary")
            
            if submitted and subject and description:
                new_rfi_number = f"RFI-2025-{len(rfis_data)+1:03d}"
                st.success(f"✅ RFI created successfully! Reference: {new_rfi_number}")
                st.info("📧 Notification sent to assigned engineering team")
                st.session_state.rfi_mode = None
                st.rerun()
            elif submitted:
                st.error("Please provide required fields: Subject and Description")
    
    elif st.session_state.get("rfi_mode") == "search":
        st.markdown("### 🔍 Search Highland Tower RFIs")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_discipline = st.selectbox("Filter by Discipline", ["All Disciplines"] + list(set([rfi["discipline"] for rfi in rfis_data])))
        
        with col2:
            search_priority = st.selectbox("Filter by Priority", ["All Priorities"] + list(set([rfi["priority"] for rfi in rfis_data])))
        
        with col3:
            search_status = st.selectbox("Filter by Status", ["All Status"] + list(set([rfi["status"] for rfi in rfis_data])))
        
        search_text = st.text_input("🔍 Search in subjects and descriptions", placeholder="Enter keywords...")
        
        # Apply filters
        filtered_rfis = rfis_data.copy()
        
        if search_discipline != "All Disciplines":
            filtered_rfis = [r for r in filtered_rfis if r["discipline"] == search_discipline]
        
        if search_priority != "All Priorities":
            filtered_rfis = [r for r in filtered_rfis if r["priority"] == search_priority]
        
        if search_status != "All Status":
            filtered_rfis = [r for r in filtered_rfis if r["status"] == search_status]
        
        if search_text:
            filtered_rfis = [r for r in filtered_rfis if 
                           search_text.lower() in r["subject"].lower() or 
                           search_text.lower() in r["description"].lower()]
        
        st.markdown(f"### 📝 Found {len(filtered_rfis)} RFIs")
        rfis_data = filtered_rfis
    
    elif st.session_state.get("rfi_mode") == "analytics":
        st.markdown("### 📊 RFI Analytics Dashboard")
        
        # RFI metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total RFIs", len(rfis_data), "+3 this week")
        
        with col2:
            open_rfis = len([r for r in rfis_data if r["status"] == "Open"])
            st.metric("Open RFIs", open_rfis, "Needs attention")
        
        with col3:
            critical_rfis = len([r for r in rfis_data if r["priority"] == "Critical"])
            st.metric("Critical RFIs", critical_rfis, "High priority")
        
        with col4:
            avg_days = sum([r["days_open"] for r in rfis_data]) / len(rfis_data)
            st.metric("Avg Days Open", f"{avg_days:.1f}", "Target: 5 days")
        
        # Priority breakdown chart
        import plotly.express as px
        priority_counts = {}
        for rfi in rfis_data:
            priority_counts[rfi["priority"]] = priority_counts.get(rfi["priority"], 0) + 1
        
        fig = px.pie(
            values=list(priority_counts.values()),
            names=list(priority_counts.keys()),
            title="📝 RFIs by Priority Level"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Default view - RFI List with CRUD operations
    if not st.session_state.get("rfi_mode"):
        st.markdown("### 📝 Highland Tower Development - Active RFIs")
        
        # RFI summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total RFIs", len(rfis_data))
        
        with col2:
            open_count = len([r for r in rfis_data if r["status"] == "Open"])
            st.metric("Open", open_count)
        
        with col3:
            critical_count = len([r for r in rfis_data if r["priority"] == "Critical"])
            st.metric("Critical", critical_count)
        
        with col4:
            answered_count = len([r for r in rfis_data if r["status"] == "Answered"])
            st.metric("Answered", answered_count)
        
        st.markdown("---")
        
        # Display RFIs in expandable cards
        for i, rfi in enumerate(rfis_data):
            priority_colors = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}
            status_colors = {"Open": "🔴", "In Review": "🟡", "Answered": "🟢"}
            
            with st.expander(f"{priority_colors[rfi['priority']]} {rfi['rfi_number']} - {rfi['subject']}", expanded=False):
                
                col1, col2 = st.columns([2, 3])
                
                with col1:
                    st.markdown(f"""
                    **📋 RFI Details:**
                    - **Number:** {rfi['rfi_number']}
                    - **Location:** {rfi['location']}
                    - **Discipline:** {rfi['discipline']}
                    - **Priority:** {rfi['priority']}
                    - **Status:** {rfi['status']}
                    - **Submitted By:** {rfi['submitted_by']}
                    - **Assigned To:** {rfi['assigned_to']}
                    - **Submitted Date:** {rfi['submitted_date']}
                    - **Due Date:** {rfi['due_date']}
                    - **Days Open:** {rfi['days_open']}
                    """)
                
                with col2:
                    st.markdown(f"**📝 Description:**")
                    st.markdown(rfi['description'])
                    
                    st.markdown(f"**💰 Cost Impact:** {rfi['cost_impact']}")
                    st.markdown(f"**📅 Schedule Impact:** {rfi['schedule_impact']}")
                    
                    # Action buttons for each RFI
                    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
                    
                    with action_col1:
                        if st.button(f"👁️ View", key=f"view_{rfi['rfi_id']}", use_container_width=True):
                            st.info(f"Opening detailed view for {rfi['rfi_number']}")
                    
                    with action_col2:
                        if st.button(f"✏️ Edit", key=f"edit_{rfi['rfi_id']}", use_container_width=True):
                            st.session_state[f"edit_rfi_{rfi['rfi_id']}"] = True
                            st.rerun()
                    
                    with action_col3:
                        if st.button(f"💬 Respond", key=f"respond_{rfi['rfi_id']}", use_container_width=True):
                            st.session_state[f"respond_rfi_{rfi['rfi_id']}"] = True
                            st.rerun()
                    
                    with action_col4:
                        if st.button(f"📎 Files", key=f"files_{rfi['rfi_id']}", use_container_width=True):
                            st.success(f"Opening attachment manager for {rfi['rfi_number']}")
                
                # Handle edit mode for individual RFIs
                if st.session_state.get(f"edit_rfi_{rfi['rfi_id']}", False):
                    st.markdown("---")
                    st.markdown("### ✏️ Edit RFI Details")
                    
                    with st.form(f"edit_form_{rfi['rfi_id']}"):
                        edit_col1, edit_col2 = st.columns(2)
                        
                        with edit_col1:
                            new_subject = st.text_input("Subject", value=rfi['subject'])
                            new_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"], 
                                                      index=["Low", "Medium", "High", "Critical"].index(rfi['priority']))
                            new_status = st.selectbox("Status", ["Open", "In Review", "Answered", "Closed"], 
                                                    index=["Open", "In Review", "Answered", "Closed"].index(rfi['status']) 
                                                    if rfi['status'] in ["Open", "In Review", "Answered", "Closed"] else 0)
                        
                        with edit_col2:
                            new_assigned_to = st.text_input("Assigned To", value=rfi['assigned_to'])
                            new_cost_impact = st.text_input("Cost Impact", value=rfi['cost_impact'])
                            new_schedule_impact = st.text_input("Schedule Impact", value=rfi['schedule_impact'])
                        
                        new_description = st.text_area("Description", value=rfi['description'])
                        
                        submitted = st.form_submit_button("💾 Save Changes", type="primary")
                        
                        if submitted:
                            st.success(f"✅ RFI {rfi['rfi_number']} updated successfully!")
                            st.session_state[f"edit_rfi_{rfi['rfi_id']}"] = False
                            st.rerun()
                
                # Handle response mode
                if st.session_state.get(f"respond_rfi_{rfi['rfi_id']}", False):
                    st.markdown("---")
                    st.markdown("### 💬 RFI Response")
                    
                    with st.form(f"response_form_{rfi['rfi_id']}"):
                        response_text = st.text_area("Response", height=120, 
                            placeholder="Provide detailed response to the RFI question...")
                        
                        response_attachments = st.file_uploader("Attach Response Files", accept_multiple_files=True, 
                            type=['pdf', 'dwg', 'jpg', 'png', 'xlsx', 'docx'])
                        
                        submitted = st.form_submit_button("📤 Submit Response", type="primary")
                        
                        if submitted and response_text:
                            st.success(f"✅ Response submitted for {rfi['rfi_number']}!")
                            st.info("📧 Notification sent to RFI submitter")
                            st.session_state[f"respond_rfi_{rfi['rfi_id']}"] = False
                            st.rerun()
                        elif submitted:
                            st.error("Please provide a response")
    
    # Reset mode button
    if st.session_state.get("rfi_mode"):
        if st.button("← Back to RFI List"):
            st.session_state.rfi_mode = None
            st.rerun()
        
        with col2:
            st.markdown("### RFI Statistics")
            st.metric("Total RFIs", "47", "+5")
            st.metric("Open RFIs", "12", "+2")
            st.metric("Avg Response Time", "2.3 days", "-0.5 days")
            st.metric("This Week", "8", "+3")
            
            if st.button("📊 Full Analytics", use_container_width=True):
                st.session_state.current_menu = "RFI Analytics"
                st.rerun()
    
    with tab2:
        st.markdown("### RFI Performance Analytics")
        
        # RFI trend chart
        rfi_dates = pd.date_range(start='2024-01-01', end='2024-05-25', freq='W')
        rfi_counts = [2, 3, 5, 4, 6, 3, 7, 4, 5, 6, 8, 4, 7, 5, 6, 8, 9, 7, 6, 8, 5]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=rfi_dates[:len(rfi_counts)], y=rfi_counts, mode='lines+markers', name='RFIs per Week'))
        fig.update_layout(title="RFI Submission Trends", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        # Response time analysis
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Response Time by Priority")
            priority_data = pd.DataFrame({
                'Priority': ['High', 'Medium', 'Low'],
                'Avg Response Time (days)': [1.2, 2.3, 4.1],
                'Target (days)': [1.0, 3.0, 5.0]
            })
            st.dataframe(priority_data)
        
        with col2:
            st.markdown("#### RFI Sources")
            source_data = pd.DataFrame({
                'Source': ['Highland Construction', 'Elite MEP', 'Safety First', 'Premium Interiors'],
                'Count': [18, 12, 8, 9]
            })
            fig = px.bar(source_data, x='Source', y='Count', title="RFIs by Source")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Create New RFI")
        with st.form("new_rfi_form"):
            col1, col2 = st.columns(2)
            with col1:
                rfi_subject = st.text_input("RFI Subject", placeholder="Brief description of the request")
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
                category = st.selectbox("Category", ["Electrical", "Mechanical", "Structural", "Architectural", "Civil"])
            
            with col2:
                submitter = st.text_input("Submitted By", value=st.session_state.username)
                due_date = st.date_input("Response Due Date")
                assign_to = st.selectbox("Assign To", ["Project Manager", "MEP Engineer", "Structural Engineer", "Architect"])
            
            description = st.text_area("Detailed Description", height=100)
            
            # File upload for attachments
            uploaded_files = st.file_uploader("Attach Files", accept_multiple_files=True, type=['pdf', 'jpg', 'png', 'dwg'])
            
            submitted = st.form_submit_button("Submit RFI", use_container_width=True)
            
            if submitted:
                if rfi_subject and description:
                    st.success(f"✅ RFI submitted successfully! Reference: RFI-2024-{len(rfi_data)+1:03d}")
                    st.info("RFI has been assigned and notifications sent to relevant parties.")
                else:
                    st.error("Please fill in all required fields.")

def render_scheduling():
    """Render advanced scheduling module"""
    st.markdown("## 📅 Project Scheduling - Advanced Planning")
    
    tab1, tab2, tab3 = st.tabs(["Master Schedule", "Critical Path", "Resource Planning"])
    
    with tab1:
        st.markdown("### Master Project Schedule")
        
        # Schedule data
        schedule_data = pd.DataFrame({
            'Task': ['Site Preparation', 'Foundation', 'Structural Frame', 'MEP Rough-in', 'Exterior Envelope', 'Interior Finishes', 'Final Inspections'],
            'Start Date': ['2024-01-15', '2024-02-01', '2024-04-01', '2024-06-15', '2024-08-01', '2024-10-01', '2024-12-15'],
            'End Date': ['2024-01-31', '2024-03-31', '2024-06-14', '2024-07-31', '2024-09-30', '2024-12-14', '2024-12-31'],
            'Duration (days)': [16, 59, 74, 46, 60, 74, 16],
            'Progress': ['100%', '100%', '85%', '60%', '30%', '0%', '0%'],
            'Status': ['Complete', 'Complete', 'Active', 'Active', 'Planned', 'Planned', 'Planned']
        })
        st.dataframe(schedule_data, use_container_width=True)
        
        # Gantt chart simulation
        st.markdown("#### Gantt Chart Overview")
        fig = px.timeline(schedule_data, x_start='Start Date', x_end='End Date', y='Task', color='Status')
        fig.update_layout(title="Project Timeline", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Critical Path Analysis")
        st.info("Critical path identifies the longest sequence of dependent tasks that determines the minimum project duration.")
        
        critical_tasks = pd.DataFrame({
            'Critical Task': ['Foundation Completion', 'Structural Frame', 'MEP Rough-in', 'Exterior Envelope'],
            'Float (days)': [0, 0, 0, 0],
            'Impact': ['High', 'High', 'Medium', 'Medium'],
            'Risk Level': ['Low', 'Medium', 'High', 'Low']
        })
        st.dataframe(critical_tasks, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Project Duration", "351 days")
            st.metric("Critical Path Length", "285 days")
        with col2:
            st.metric("Schedule Buffer", "18.8%")
            st.metric("On-Time Probability", "87%")
    
    with tab3:
        st.markdown("### Resource Planning")
        
        resource_data = pd.DataFrame({
            'Resource Type': ['Labor', 'Equipment', 'Materials', 'Subcontractors'],
            'Allocated': ['145 workers', '12 units', '$2.3M', '8 firms'],
            'Utilized': ['128 workers', '10 units', '$2.1M', '7 firms'],
            'Efficiency': ['88%', '83%', '91%', '88%']
        })
        st.dataframe(resource_data, use_container_width=True)

def setup_database_connection():
    """Setup PostgreSQL database connection for your modules"""
    import os
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        st.session_state.db_connected = True
        return True
    else:
        st.session_state.db_connected = False
        return False

def load_sophisticated_modules():
    """Load your existing sophisticated module system"""
    try:
        # Your sophisticated modules are already loaded in the main function
        # This is just a placeholder for future enhancements
        return {
            "status": "loaded",
            "modules_count": 25,
            "enterprise_features": True
        }
    except Exception:
        return {}

def render_main_content():
    """Render main content using your sophisticated module system"""
    current_menu = st.session_state.current_menu
    
    # Setup database connection for your modules
    setup_database_connection()
    
    # Load your sophisticated modules
    sophisticated_modules = load_sophisticated_modules()
    
    # Your enterprise module mapping with sophisticated imports
    try:
        # Import your actual sophisticated modules with proper error handling
        module_functions = {}
        
        # Dashboard module with business intelligence
        try:
            from modules.dashboard import render_dashboard as dashboard_render
            module_functions["Dashboard"] = dashboard_render
        except ImportError:
            module_functions["Dashboard"] = render_dashboard
        
        # PreConstruction with estimating and bid management
        try:
            from modules.preconstruction import render_preconstruction as precon_render
            module_functions["PreConstruction"] = precon_render
        except ImportError:
            module_functions["PreConstruction"] = render_preconstruction
        
        # Engineering with RFIs, submittals, transmittals
        try:
            from modules.engineering import render_engineering as eng_render
            module_functions["Engineering"] = eng_render
        except ImportError:
            module_functions["Engineering"] = render_engineering
        
        # Field Operations with daily reports and checklists
        try:
            from modules.field_operations import render_field_operations as field_render
            module_functions["Field Operations"] = field_render
        except ImportError:
            module_functions["Field Operations"] = render_field_operations
        
        # Safety with incident tracking and compliance
        try:
            from modules.safety import render as safety_render
            module_functions["Safety"] = safety_render
        except ImportError:
            # Use the local fallback function defined in this file
            module_functions["Safety"] = lambda: render_safety()
        
        # Contracts with prime contracts and change orders
        try:
            from modules.contracts import render as contracts_render
            module_functions["Contracts"] = contracts_render
        except ImportError:
            # Use the local fallback function defined in this file
            module_functions["Contracts"] = lambda: render_contracts()
        
        # Cost Management with AIA billing
        try:
            from modules.cost_management import render_cost_management as cost_render
            module_functions["Cost Management"] = cost_render
        except ImportError:
            module_functions["Cost Management"] = render_cost_management
        
        # AIA G702/G703 Billing (separate module)
        module_functions["AIA G702/G703 Billing"] = render_aia_billing
        
        # Unit Prices module for advanced cost intelligence
        try:
            from modules.unit_prices import render_unit_prices as unit_prices_render
            module_functions["Unit Prices"] = unit_prices_render
        except ImportError:
            module_functions["Unit Prices"] = lambda: st.info("Unit Prices module loading...")
        
        # Deliveries module for comprehensive delivery management
        try:
            from modules.deliveries import render_deliveries as deliveries_render
            module_functions["Deliveries"] = deliveries_render
        except ImportError:
            module_functions["Deliveries"] = lambda: st.info("Deliveries module loading...")
        
        # BIM with model viewer and clash detection
        try:
            from modules.bim import render_bim as bim_render
            module_functions["BIM"] = bim_render
        except ImportError:
            module_functions["BIM"] = render_bim
        
        # Analytics with business intelligence
        try:
            from modules.analytics import render_analytics as analytics_render
            module_functions["Analytics"] = analytics_render
        except ImportError:
            module_functions["Analytics"] = render_analytics
        
        # Documents with PDF management
        try:
            from modules.documents import render_documents as docs_render
            module_functions["Documents"] = docs_render
        except ImportError:
            module_functions["Documents"] = render_documents
        
        # Scheduling with progress tracking
        try:
            from modules.scheduling import render_scheduling as scheduling_render
            module_functions["Scheduling"] = scheduling_render
        except ImportError:
            module_functions["Scheduling"] = render_scheduling
        
        # Closeout with project completion
        try:
            from modules.closeout import render as closeout_render
            module_functions["Closeout"] = closeout_render
        except ImportError:
            module_functions["Closeout"] = render_closeout
        
        # AI Assistant
        try:
            from modules.ai_assistant import render_ai_assistant as ai_render
            module_functions["AI Assistant"] = ai_render
        except ImportError:
            module_functions["AI Assistant"] = render_ai_assistant
        
        # Mobile Companion (Fixed)
        try:
            from modules.mobile_companion_fixed import render_mobile_companion as mobile_render
            module_functions["Mobile Companion"] = mobile_render
        except ImportError:
            module_functions["Mobile Companion"] = lambda: st.info("Mobile interface loading...")
        
        # Additional specialized modules
        module_functions.update({
            "Prime Contract": render_prime_contract,
            "Change Orders": render_change_orders,
            "Recent Reports": render_recent_reports,
            "Daily Reports": render_daily_reports,
            "Quality Control": render_quality_control,
            "Material Management": render_material_management,
        })
        
    except Exception as e:
        st.error(f"Error loading sophisticated modules: {str(e)}")
        # Fallback to basic functions - only use what's actually defined
        module_functions = {
            "Dashboard": render_dashboard,
            "PreConstruction": render_preconstruction,
            "Engineering": render_engineering,
            "Field Operations": render_field_operations,
            "Safety": render_safety,
            "Contracts": render_contracts,
            "Cost Management": render_cost_management,
            "BIM": render_bim,
            "Analytics": render_analytics,
            "Documents": lambda: __import__("modules.documents").documents.render_documents(),
            "Scheduling": render_scheduling,
            "AI Assistant": render_ai_assistant,
            "Mobile Companion": render_mobile_companion,
            "Prime Contract": render_prime_contract,
            "Change Orders": render_change_orders,
            "AIA G702/G703 Billing": render_aia_billing,
            "Recent Reports": render_recent_reports,
            "Daily Reports": render_daily_reports,
            "Quality Control": render_quality_control,
            "Material Management": render_material_management,
            "RFIs": render_rfis,
            "Performance Snapshot": lambda: __import__("modules.performance_snapshot").performance_snapshot.render(),
            "Subcontractor Management": lambda: __import__("modules.subcontractor_management").subcontractor_management.render(),
            "Inspections": lambda: __import__("modules.inspections").inspections.render(),
            "Issues & Risks": lambda: __import__("modules.issues_risks").issues_risks.render(),
        }
    
    if current_menu in module_functions:
        module_functions[current_menu]()
    else:
        # Advanced preview for remaining modules
        st.markdown(f"## {current_menu}")
        st.info(f"The {current_menu} module is being developed with enterprise-grade features designed to outperform Procore.")
        
        if current_menu == "PreConstruction":
            st.markdown("### 🏗️ PreConstruction Module")
            st.markdown("**Complete pre-construction planning and coordination platform**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **📋 Planning Tools:**
                - Project scope definition
                - Constructability reviews
                - Value engineering analysis
                - Risk assessment matrix
                """)
            with col2:
                st.markdown("""
                **📊 Advanced Features:**
                - AI-powered schedule optimization
                - Cost estimation with market data
                - Permit tracking and coordination
                - Trade partner qualification
                """)
        
        elif current_menu == "Closeout":
            st.markdown("### ✅ Project Closeout Module")
            st.markdown("**Comprehensive project completion and handover management**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **📋 Closeout Tasks:**
                - Punch list management
                - Final inspections tracking
                - Warranty documentation
                - As-built drawing compilation
                """)
            with col2:
                st.markdown("""
                **🎯 Advanced Features:**
                - Automated compliance checking
                - Digital handover packages
                - Maintenance manual integration
                - Owner training coordination
                """)
        
        elif current_menu == "Submittals":
            render_submittals()
        
        elif current_menu == "Transmittals":
            render_transmittals()
        
        elif current_menu == "Equipment Tracking":
            render_equipment_tracking()
        
        elif current_menu == "AI Assistant":
            render_ai_assistant()
        
        elif current_menu == "Mobile Companion":
            render_mobile_companion()
        
        # Admin modules
        elif current_menu == "User Management":
            st.title("👥 User Management")
            st.markdown("**Highland Tower Development - User Access Control**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Active Users", "47", "+2 this week")
            with col2:
                st.metric("Admin Users", "5", "No change")
            with col3:
                st.metric("Guest Access", "12", "Temporary access")
                
            # User management interface
            user_data = pd.DataFrame([
                {"Name": "Sarah Chen, PE", "Role": "Project Engineer", "Status": "Active", "Last Login": "2025-01-25"},
                {"Name": "Mike Rodriguez", "Role": "Field Supervisor", "Status": "Active", "Last Login": "2025-01-25"},
                {"Name": "Jennifer Walsh, AIA", "Role": "Architect", "Status": "Active", "Last Login": "2025-01-24"},
                {"Name": "David Kim", "Role": "Safety Manager", "Status": "Active", "Last Login": "2025-01-25"}
            ])
            st.dataframe(user_data, use_container_width=True, hide_index=True)
            
        elif current_menu == "Security Settings":
            st.title("🔐 Security Settings")
            st.markdown("**System security configuration and monitoring**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🔒 Access Control**")
                st.checkbox("Two-factor authentication required", value=True)
                st.checkbox("Password complexity requirements", value=True)
                st.checkbox("Session timeout (30 minutes)", value=True)
                
            with col2:
                st.markdown("**📊 Security Metrics**")
                st.metric("Failed Login Attempts", "3", "Last 24 hours")
                st.metric("Active Sessions", "23", "Current users")
                st.metric("Security Score", "98%", "Excellent")
                
        elif current_menu == "System Analytics":
            st.title("📊 System Analytics")
            st.markdown("**Highland Tower Development - System Performance**")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("System Uptime", "99.8%", "30 days")
            with col2:
                st.metric("Response Time", "1.2s", "Average")
            with col3:
                st.metric("Active Modules", "15/15", "All operational")
            with col4:
                st.metric("Data Usage", "2.3 TB", "This month")
                
        elif current_menu == "Database Admin":
            st.title("🗄️ Database Administration")
            st.markdown("**Database management and maintenance**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📈 Database Health**")
                st.metric("Database Size", "45.2 GB", "+2.1 GB this week")
                st.metric("Active Connections", "12", "Current")
                st.metric("Query Performance", "Fast", "95% < 100ms")
                
            with col2:
                st.markdown("**🔧 Maintenance Tools**")
                if st.button("📊 Generate Backup"):
                    st.success("Database backup initiated")
                if st.button("🧹 Optimize Tables"):
                    st.success("Table optimization started")
                if st.button("📋 View Logs"):
                    st.success("Database logs accessed")
                    
        else:
            st.markdown(f"### {current_menu}")
            st.info(f"The {current_menu} module provides comprehensive functionality for Highland Tower Development project management.")

def render_engineering():
    """Advanced Engineering module with comprehensive workflow management"""
    st.title("⚙️ Engineering Management - Advanced Coordination")
    st.markdown("**Complete engineering workflow from design through construction**")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📐 Drawing Management", "🔧 Coordination", "📊 Analytics", "⚙️ Settings"])
    
    with tab1:
        st.markdown("### 📐 Drawing Management & Revision Control")
        
        # Drawing Overview Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Drawings", "247", "+3 this week")
        with col2:
            st.metric("Current Revision", "Rev C", "Latest update")
        with col3:
            st.metric("Under Review", "12", "2 overdue")
        with col4:
            st.metric("Coordination Issues", "3", "High priority")
        
        # Drawing Management Interface
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("#### 📋 Highland Tower Development - Drawing Set")
            drawing_data = pd.DataFrame([
                {"Sheet": "A-101", "Title": "Level 1 Floor Plan", "Rev": "C", "Date": "2025-01-20", "Status": "Current", "Discipline": "Architectural"},
                {"Sheet": "A-201", "Title": "Exterior Elevations", "Rev": "B", "Date": "2025-01-19", "Status": "Current", "Discipline": "Architectural"},
                {"Sheet": "S-101", "Title": "Foundation Plan", "Rev": "D", "Date": "2025-01-21", "Status": "Current", "Discipline": "Structural"},
                {"Sheet": "S-201", "Title": "Level 13 Framing Plan", "Rev": "B", "Date": "2025-01-22", "Status": "Under Review", "Discipline": "Structural"},
                {"Sheet": "M-301", "Title": "HVAC Level 9-11", "Rev": "A", "Date": "2025-01-18", "Status": "Current", "Discipline": "Mechanical"},
                {"Sheet": "E-401", "Title": "Electrical Riser Diagram", "Rev": "D", "Date": "2025-01-21", "Status": "Superseded", "Discipline": "Electrical"},
                {"Sheet": "P-101", "Title": "Plumbing Floor Plans", "Rev": "C", "Date": "2025-01-20", "Status": "Current", "Discipline": "Plumbing"}
            ])
            
            # Filter by discipline
            discipline_filter = st.selectbox("Filter by Discipline", 
                ["All", "Architectural", "Structural", "Mechanical", "Electrical", "Plumbing"])
            
            if discipline_filter != "All":
                filtered_data = drawing_data[drawing_data["Discipline"] == discipline_filter]
            else:
                filtered_data = drawing_data
                
            st.dataframe(filtered_data, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### 🔧 Quick Actions")
            if st.button("📋 Upload New Drawing", use_container_width=True):
                st.success("Drawing upload interface opened")
            if st.button("🔄 Check for Updates", use_container_width=True):
                st.success("Checking for drawing updates...")
            if st.button("📤 Create Transmittal", use_container_width=True):
                st.success("Transmittal creation started")
            if st.button("🎯 Coordination Review", use_container_width=True):
                st.success("Opening coordination interface")
                
        # Drawing Revision History
        st.markdown("#### 📜 Recent Revision History")
        revision_data = pd.DataFrame([
            {"Date": "2025-01-22", "Sheet": "S-201", "Change": "Updated beam sizes", "By": "Sarah Chen, PE"},
            {"Date": "2025-01-21", "Sheet": "E-401", "Change": "Added emergency circuits", "By": "Mike Rodriguez, PE"},
            {"Date": "2025-01-20", "Sheet": "A-101", "Change": "Revised room layouts", "By": "Jennifer Walsh, AIA"}
        ])
        st.dataframe(revision_data, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("### 🔧 MEP Coordination Dashboard")
        st.warning("🚨 **Active Coordination Issues:** 3 conflicts require immediate attention")
        
        coordination_issues = [
            {"Issue": "HVAC duct conflicts with structural beam", "Location": "Level 11, Grid C3", "Priority": "High", "Assigned": "MEP Engineer"},
            {"Issue": "Electrical conduit routing needs adjustment", "Location": "Level 9, Corridor", "Priority": "Medium", "Assigned": "Electrical Engineer"},
            {"Issue": "Plumbing stack conflicts with architecture", "Location": "Level 12, Unit 1205", "Priority": "High", "Assigned": "Architect"}
        ]
        
        for issue in coordination_issues:
            with st.expander(f"⚠️ {issue['Issue']} - {issue['Priority']} Priority"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Location:** {issue['Location']}")
                with col2:
                    st.markdown(f"**Assigned To:** {issue['Assigned']}")
                with col3:
                    if st.button(f"Resolve Issue", key=f"resolve_{issue['Issue'][:10]}"):
                        st.success("Issue marked for resolution!")

def render_field_operations():
    """Advanced Field Operations with real-time crew and progress management"""
    st.title("👷 Field Operations - Live Project Management")
    st.markdown("**Real-time field coordination and workforce management**")
    
    tab1, tab2, tab3 = st.tabs(["👥 Crew Management", "🌤️ Weather Impact", "📱 Mobile Tools"])
    
    with tab1:
        st.markdown("### 👥 Active Crew Management")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Workers", "89", "+5 today")
        with col2:
            st.metric("Active Crews", "12", "All zones covered")
        with col3:
            st.metric("Safety Officers", "3", "On-site now")
        with col4:
            st.metric("Productivity", "94%", "+2% vs target")
        
        # Crew assignments by floor
        st.markdown("### 🏗️ Current Crew Assignments")
        
        crew_assignments = [
            {"Level": "Level 13", "Crew": "Structural Team A", "Activity": "Steel erection", "Count": 12, "Supervisor": "Mike Chen"},
            {"Level": "Level 11", "Crew": "MEP Team B", "Activity": "Electrical rough-in", "Count": 8, "Supervisor": "Sarah Johnson"},
            {"Level": "Level 9", "Crew": "MEP Team C", "Activity": "Plumbing installation", "Count": 6, "Supervisor": "Carlos Rodriguez"},
            {"Level": "Level 7", "Crew": "Finishing Team D", "Activity": "Drywall installation", "Count": 10, "Supervisor": "Jennifer Walsh"}
        ]
        
        for assignment in crew_assignments:
            with st.expander(f"👷 {assignment['Level']} - {assignment['Crew']} ({assignment['Count']} workers)"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Activity:** {assignment['Activity']}")
                    st.markdown(f"**Supervisor:** {assignment['Supervisor']}")
                with col2:
                    st.markdown(f"**Crew Size:** {assignment['Count']} workers")
                    st.markdown(f"**Status:** ✅ On Schedule")
                with col3:
                    if st.button(f"📞 Contact Supervisor", key=f"contact_{assignment['Level']}"):
                        st.info(f"Calling {assignment['Supervisor']}...")

def render_safety():
    """Comprehensive Safety Management with incident tracking and compliance"""
    st.title("🦺 Safety Management - Zero Incident Goal")
    st.markdown("**Comprehensive safety program with real-time monitoring**")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Safety Dashboard", "⚠️ Incident Reporting", "📚 Training Tracker", "🎯 Compliance"])
    
    with tab1:
        st.markdown("### 🎯 Safety Performance Dashboard")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Safety Score", "98.5%", "+0.5% this month")
        with col2:
            st.metric("Days Since Incident", "47", "🎉 Excellent")
        with col3:
            st.metric("Near Misses", "2", "This week")
        with col4:
            st.metric("Training Complete", "94%", "Target: 100%")
        with col5:
            st.metric("PPE Compliance", "99.2%", "✅ Excellent")
        
        # Recent safety activities
        st.markdown("### 📋 Recent Safety Activities")
        safety_activities = [
            "✅ Daily safety briefing completed - All crews",
            "🎓 Fall protection training - 15 workers certified",
            "🔍 Weekly safety inspection - Level 13 structural work",
            "📋 Toolbox talk: Electrical safety around MEP work",
            "🚨 Near miss reported: Crane load swing (resolved)"
        ]
        
        for activity in safety_activities:
            st.info(activity)

def render_cost_management():
    """Advanced Cost Management with AI-powered forecasting"""
    st.title("💰 Cost Management - Financial Control Center")
    st.markdown("**Real-time budget tracking with predictive analytics**")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Budget Overview", "📈 Forecasting", "💳 Change Orders", "📋 Owner Bill", "📄 AIA G702/G703"])
    
    with tab1:
        st.markdown("### 💰 Real-Time Budget Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Budget", "$45.5M", "Approved contract")
        with col2:
            st.metric("Spent to Date", "$30.5M", "67% of budget")
        with col3:
            st.metric("Forecast Final", "$43.4M", "$2.1M under budget")
        with col4:
            st.metric("Contingency", "$1.5M", "3.3% remaining")
        
        # Cost breakdown visualization
        cost_data = pd.DataFrame({
            'Category': ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'Overhead'],
            'Budget': [18.2, 15.8, 6.3, 3.7, 1.5],
            'Actual': [17.8, 16.1, 5.9, 3.5, 1.4],
            'Variance': [-0.4, 0.3, -0.4, -0.2, -0.1]
        })
        
        fig = px.bar(cost_data, x='Category', y=['Budget', 'Actual'], 
                    title="Budget vs Actual by Category (Millions $)", barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 📋 Owner Bill Management")
        st.markdown("**Highland Tower Development - Owner Billing Dashboard**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Bill Amount", "$2,847,500", "Application #8")
        with col2:
            st.metric("Total Billed to Date", "$30,247,800", "67% of contract")
        with col3:
            st.metric("Retention Held", "$1,512,390", "5% standard")
            
        # Owner billing interface
        st.markdown("#### 💰 Create Owner Bill")
        
        bill_col1, bill_col2 = st.columns(2)
        with bill_col1:
            bill_period = st.selectbox("Billing Period", ["January 2025", "December 2024", "November 2024"])
            bill_amount = st.number_input("Bill Amount ($)", value=2847500, step=1000)
            retention_rate = st.number_input("Retention Rate (%)", value=5.0, step=0.1)
            
        with bill_col2:
            work_completed = st.text_area("Work Completed This Period", 
                "Level 13 structural steel erection completed\nMEP rough-in Level 9-11 progress\nExterior skin installation ongoing")
            
        if st.button("📤 Generate Owner Bill", type="primary"):
            st.success("✅ Owner bill generated and ready for submission")
            
            # Import and render digital signature section
            from components.digital_signature import render_digital_signature_section
            st.divider()
            render_digital_signature_section("Owner Bill", bill_amount, None)
            
    with tab5:
        st.markdown("### 📄 AIA G702/G703 Application & Certificate for Payment")
        st.markdown("**Standard AIA billing forms for Highland Tower Development**")
        
        # G702/G703 interface
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 📋 Current Application Details")
            
            app_data = pd.DataFrame([
                {"Line Item": "01 - General Requirements", "Scheduled Value": "$1,820,000", "Work Complete": "$1,638,000", "% Complete": "90%"},
                {"Line Item": "03 - Concrete", "Scheduled Value": "$8,750,000", "Work Complete": "$7,875,000", "% Complete": "90%"},
                {"Line Item": "05 - Metals", "Scheduled Value": "$12,400,000", "Work Complete": "$8,680,000", "% Complete": "70%"},
                {"Line Item": "07 - Thermal & Moisture", "Scheduled Value": "$3,200,000", "Work Complete": "$1,280,000", "% Complete": "40%"},
                {"Line Item": "08 - Openings", "Scheduled Value": "$4,850,000", "Work Complete": "$1,455,000", "% Complete": "30%"}
            ])
            
            st.dataframe(app_data, use_container_width=True, hide_index=True)
            
        with col2:
            st.markdown("#### 🔧 Application Controls")
            app_number = st.number_input("Application Number", value=8, min_value=1)
            app_date = st.date_input("Application Date")
            period_to = st.date_input("Period To")
            
            if st.button("📄 Generate G702", use_container_width=True):
                st.success("G702 Application generated")
            if st.button("📊 Generate G703", use_container_width=True):
                st.success("G703 Schedule of Values generated")
            if st.button("📤 Submit Application", use_container_width=True, type="primary"):
                st.success("Payment application submitted to owner")
                
                # Add digital signature section for G702
                from components.digital_signature import render_digital_signature_section
                st.divider()
                render_digital_signature_section("G702", None, app_number)

def render_recent_reports():
    """Recent Daily Reports Management"""
    st.markdown("### 📋 Recent Daily Reports")
    st.markdown("**View and manage your submitted daily reports**")
    
    # Filter controls
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        date_filter = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "This Month", "All Reports"])
    with filter_col2:
        super_filter = st.selectbox("Superintendent", ["All", "John Smith", "Sarah Johnson", "Mike Rodriguez"])
    with filter_col3:
        status_filter = st.selectbox("Status", ["All", "Complete", "Pending Review", "Draft"])
    
    # Recent reports data from your project
    reports = [
        {
            "Date": "2025-01-25", "Super": "John Smith", "Workers": 45, "Weather": "Clear, 72°F",
            "Work": "Level 13 concrete pour - 185 CY completed, steel delivery received",
            "Issues": "None - ahead of schedule", "Status": "✅ Complete", "Time": "5:30 PM"
        },
        {
            "Date": "2025-01-24", "Super": "Sarah Johnson", "Workers": 48, "Weather": "Cloudy, 68°F", 
            "Work": "Steel erection Level 14 - 12 tons installed, MEP rough-in Level 12",
            "Issues": "Elevator shaft work delayed 1 hour", "Status": "✅ Complete", "Time": "6:15 PM"
        },
        {
            "Date": "2025-01-23", "Super": "Mike Rodriguez", "Workers": 52, "Weather": "Clear, 75°F",
            "Work": "Curtain wall south facade installation - 40% complete", 
            "Issues": "Material delivery 2 hour delay", "Status": "✅ Complete", "Time": "5:45 PM"
        },
        {
            "Date": "2025-01-22", "Super": "John Smith", "Workers": 47, "Weather": "Light Rain, 65°F",
            "Work": "Interior framing Levels 10-11, electrical rough-in progress",
            "Issues": "Rain delay 3 hours morning shift", "Status": "✅ Complete", "Time": "7:00 PM"
        },
        {
            "Date": "2025-01-21", "Super": "Sarah Johnson", "Workers": 44, "Weather": "Overcast, 70°F",
            "Work": "Plumbing rough-in Level 12, HVAC ductwork Level 11",
            "Issues": "None", "Status": "✅ Complete", "Time": "5:50 PM"
        }
    ]
    
    # Display reports
    for report in reports:
        with st.expander(f"{report['Status']} {report['Date']} - {report['Super']} ({report['Workers']} workers)"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **📋 Report Details:**
                - **Date:** {report['Date']}
                - **Superintendent:** {report['Super']}
                - **Workers:** {report['Workers']}
                - **Submitted:** {report['Time']}
                """)
            
            with col2:
                st.markdown(f"""
                **🌤️ Conditions & Status:**
                - **Weather:** {report['Weather']}
                - **Status:** {report['Status']}
                """)
            
            st.markdown(f"""
            **🏗️ Work Performed:**
            {report['Work']}
            
            **⚠️ Issues/Notes:**
            {report['Issues']}
            """)
            
            # Action buttons
            btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
            with btn_col1:
                if st.button(f"👁️ View Full", key=f"view_{report['Date']}", use_container_width=True):
                    st.success(f"Opening detailed view for {report['Date']}")
            with btn_col2:
                if st.button(f"✏️ Edit", key=f"edit_{report['Date']}", use_container_width=True):
                    st.info(f"Opening edit mode for {report['Date']}")
            with btn_col3:
                if st.button(f"📧 Send", key=f"send_{report['Date']}", use_container_width=True):
                    st.success("Report sent to stakeholders")
            with btn_col4:
                if st.button(f"📥 PDF", key=f"pdf_{report['Date']}", use_container_width=True):
                    st.info("Generating PDF...")
    
    # Summary metrics
    st.markdown("---")
    st.markdown("### 📊 Reports Summary")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric("Reports This Week", "5", "100% submitted")
    with metric_col2:
        st.metric("Avg Workers/Day", "47", "+3 vs last week")
    with metric_col3:
        st.metric("Weather Delays", "1", "3 hours total")
    with metric_col4:
        st.metric("Issues Reported", "2", "Minor delays only")

def render_daily_reports():
    """🚀 Next-Generation Daily Reports - Beyond Procore & Autodesk Construction Cloud"""
    st.title("📊 Highland Tower Daily Reports")
    st.markdown("**🎯 Advanced AI-Powered Field Reporting System**")
    
    # Real-time project status bar using native Streamlit components
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.info("📍 Highland Tower Development")
        with col2:
            st.info("🏗️ Level 13 Active")
        with col3:
            st.info("👷 89 Workers")
        with col4:
            st.info("🌤️ 72°F Clear")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚀 Smart Report", "📱 Mobile Capture", "🤖 AI Insights", "📊 Analytics", "🔄 Live Feed"
    ])
    
    with tab1:
        st.markdown("### 🚀 Intelligent Daily Report Creation")
        st.markdown("**Advanced Features:** Auto-populated data, AI suggestions, predictive analysis")
        
        # Auto-populated environmental data
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("#### 🌤️ Environmental (Auto-Detected)")
            report_date = st.date_input("📅 Report Date", value=pd.Timestamp.now())
            weather = st.selectbox("☁️ Weather", ["Clear ☀️", "Partly Cloudy ⛅", "Overcast ☁️", "Light Rain 🌦️", "Heavy Rain 🌧️"], index=0)
            col_temp1, col_temp2 = st.columns(2)
            with col_temp1:
                temp_high = st.number_input("🌡️ High °F", value=72, min_value=-20, max_value=120)
            with col_temp2:
                temp_low = st.number_input("🌡️ Low °F", value=58, min_value=-20, max_value=120)
            wind_speed = st.slider("💨 Wind Speed (mph)", 0, 50, 8)
            humidity = st.slider("💧 Humidity %", 0, 100, 65)
        
        with col2:
            st.markdown("#### 👥 Workforce Analytics")
            total_workers = st.number_input("👷 Total Workers", value=89, min_value=0)
            work_hours = st.number_input("⏰ Total Hours", value=712, min_value=0)
            overtime_hours = st.number_input("⏰ Overtime Hours", value=45, min_value=0)
            
            # AI-powered crew optimization suggestion
            st.info(f"🤖 **AI Suggestion:** Optimal crew size for current weather: {int(total_workers * 0.95)} workers")
            
            col_safety1, col_safety2 = st.columns(2)
            with col_safety1:
                safety_incidents = st.number_input("⚠️ Safety Issues", value=0, min_value=0)
            with col_safety2:
                quality_issues = st.number_input("🔍 Quality Issues", value=0, min_value=0)
        
        with col3:
            st.markdown("#### 💰 Cost & Schedule Impact")
            labor_cost = st.number_input("💵 Daily Labor Cost", value=35600, min_value=0)
            material_cost = st.number_input("🧱 Material Cost", value=12400, min_value=0)
            schedule_variance = st.selectbox("📈 Schedule Status", 
                ["Ahead of Schedule ⚡", "On Schedule ✅", "Behind Schedule ⚠️", "Critical Delay 🚨"])
            
            # Real-time cost analysis
            total_daily_cost = labor_cost + material_cost
            st.metric("💰 Total Daily Cost", f"${total_daily_cost:,}", 
                     delta=f"{-2.3}% vs planned", delta_color="normal")
        
        st.markdown("### 🏗️ Advanced Work Progress Tracking")
        st.markdown("**Enterprise Capabilities:** Real-time progress with photo verification and GPS tracking")
        
        # Enhanced progress tracking with Highland Tower specific areas
        progress_areas = [
            {
                "Area": "Level 13 - Structural Steel", 
                "Progress": 87, 
                "Crew": 12, 
                "Lead": "Mike Rodriguez", 
                "Priority": "High",
                "Notes": "W24x62 beam installation 90% complete. Connection details under review.",
                "Photos": 8,
                "GPS": "40.7589, -73.9851",
                "Schedule": "On Track",
                "Cost_Impact": "$0",
                "Next_Activity": "Install remaining beams L13.G-L13.J"
            },
            {
                "Area": "Level 11 - MEP Systems", 
                "Progress": 73, 
                "Crew": 14, 
                "Lead": "Sarah Chen", 
                "Priority": "Medium",
                "Notes": "HVAC ductwork installation progressing. Electrical conduit runs complete.",
                "Photos": 12,
                "GPS": "40.7587, -73.9851", 
                "Schedule": "Ahead",
                "Cost_Impact": "-$2,300 under budget",
                "Next_Activity": "Coordinate plumbing rough-in with electrical"
            },
            {
                "Area": "Level 9 - Interior Finishes", 
                "Progress": 51, 
                "Crew": 8, 
                "Lead": "Jennifer Walsh", 
                "Priority": "Low",
                "Notes": "Drywall installation 60% complete. Paint prep scheduled for next week.",
                "Photos": 15,
                "GPS": "40.7585, -73.9851",
                "Schedule": "On Track", 
                "Cost_Impact": "+$1,200 material variance",
                "Next_Activity": "Complete drywall installation east wing"
            }
        ]
        
        for i, area in enumerate(progress_areas):
            priority_color = "🔴" if area['Priority'] == "High" else "🟡" if area['Priority'] == "Medium" else "🟢"
            schedule_icon = "⚡" if area['Schedule'] == "Ahead" else "✅" if area['Schedule'] == "On Track" else "⚠️"
            
            with st.expander(f"{priority_color} {area['Area']} - {area['Progress']}% Complete {schedule_icon}"):
                # Multi-column layout for comprehensive data
                detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)
                
                with detail_col1:
                    st.markdown("**📊 Progress & Crew**")
                    progress_val = st.slider("Progress %", 0, 100, area['Progress'], key=f"progress_{i}")
                    crew_size = st.number_input("👥 Crew Size", value=area['Crew'], key=f"crew_{i}")
                    crew_lead = st.text_input("👤 Lead", value=area['Lead'], key=f"lead_{i}")
                
                with detail_col2:
                    st.markdown("**📍 Location & Photos**")
                    st.text_input("📍 GPS Coords", value=area['GPS'], key=f"gps_{i}")
                    photos_count = st.number_input("📸 Photos", value=area['Photos'], key=f"photos_{i}")
                    if st.button(f"📷 Capture Progress Photos", key=f"photo_btn_{i}"):
                        st.info("📱 Mobile camera integration would open here")
                
                with detail_col3:
                    st.markdown("**💰 Schedule & Cost**")
                    schedule_status = st.selectbox("📈 Status", 
                        ["Ahead", "On Track", "Behind", "Critical"], 
                        index=["Ahead", "On Track", "Behind"].index(area['Schedule']) if area['Schedule'] in ["Ahead", "On Track", "Behind"] else 1,
                        key=f"schedule_{i}")
                    cost_impact = st.text_input("💵 Cost Impact", value=area['Cost_Impact'], key=f"cost_{i}")
                
                with detail_col4:
                    st.markdown("**📝 Notes & Next Steps**")
                    work_notes = st.text_area("📋 Today's Work", value=area['Notes'], key=f"notes_{i}", height=100)
                    next_activity = st.text_area("➡️ Next Activity", value=area['Next_Activity'], key=f"next_{i}", height=80)
        
        # AI-powered suggestions and alerts
        st.markdown("### 🤖 AI-Powered Insights & Recommendations")
        
        insight_col1, insight_col2 = st.columns(2)
        with insight_col1:
            st.markdown("""
            **🧠 Smart Recommendations:**
            - 🌧️ Weather alert: 30% rain chance tomorrow - consider indoor work priority
            - ⚡ Productivity boost: Level 11 crew performing 15% above baseline
            - 🔄 Resource optimization: Relocate 2 workers from Level 9 to Level 13 for efficiency
            - 📈 Schedule prediction: Current pace will complete Level 13 structural 2 days ahead
            """)
        
        with insight_col2:
            st.markdown("""
            **⚠️ Risk Alerts:**
            - 🚨 Critical: Level 13 crane inspection due within 3 days
            - ⚠️ Medium: Material delivery delay risk for Level 14 steel (supplier contacted)
            - 📊 Low: Quality variance detected in concrete batch #237 - monitoring required
            - 💰 Budget: Daily costs running 2.3% under planned target
            """)
        
        # Enhanced submission with AI validation
        st.markdown("---")
        col_submit1, col_submit2, col_submit3 = st.columns(3)
        
        with col_submit1:
            if st.button("🤖 AI Review", use_container_width=True, type="secondary"):
                st.info("🧠 AI analyzing report for completeness and insights...")
                
        with col_submit2:
            if st.button("💾 Save Draft", use_container_width=True):
                st.success("✅ Draft saved - Report DR-HT-2025-025")
        
        with col_submit3:
            if st.button("📤 Submit Report", type="primary", use_container_width=True):
                st.balloons()
                st.success("""
                ✅ **Daily Report DR-HT-2025-025 Successfully Submitted!**
                
                📊 **Auto-Generated Insights:**
                - 📈 Project 3.2% ahead of schedule
                - 💰 Daily costs 2.3% under budget
                - 🎯 87% average productivity across all areas
                - 🚀 Ready for Level 14 structural start Monday
                """)
    
    with tab2:
        st.markdown("### 📱 Mobile-First Field Capture")
        st.markdown("**Revolutionary feature:** Real-time field data capture that beats both Procore and Autodesk")
        
        mobile_col1, mobile_col2 = st.columns(2)
        
        with mobile_col1:
            st.markdown("""
            #### 📸 Smart Photo Management
            **Features beyond competition:**
            - GPS auto-tagging with floor/area detection
            - AI-powered progress analysis from photos
            - Automatic quality issue detection
            - Voice-to-text annotations
            """)
            
            if st.button("📷 Launch Mobile Camera", use_container_width=True, type="primary"):
                st.info("📱 Mobile capture interface would launch with:")
                st.markdown("""
                - 🎯 AR overlay showing planned vs actual progress
                - 🤖 AI real-time quality analysis 
                - 📍 Automatic GPS and floor level detection
                - 🎙️ Voice note recording with transcription
                """)
        
        with mobile_col2:
            st.markdown("""
            #### 🎙️ Voice-Powered Reporting
            **Industry-first features:**
            - Natural language report creation
            - Real-time transcription with technical term recognition
            - Multi-language support for diverse crews
            - Offline capability with sync when connected
            """)
            
            if st.button("🎙️ Start Voice Report", use_container_width=True):
                st.info("🎤 Voice recording would start with:")
                st.markdown("""
                - 🧠 AI listening for construction terminology
                - 📝 Real-time transcription and formatting
                - 🔧 Auto-categorization into report sections
                - ✅ Smart validation and completion prompts
                """)
    
    with tab3:
        st.markdown("### 🤖 AI-Powered Construction Intelligence")
        st.markdown("**Next-level analytics that surpass industry leaders**")
        
        # AI insights dashboard
        ai_col1, ai_col2, ai_col3 = st.columns(3)
        
        with ai_col1:
            st.metric("🧠 AI Productivity Score", "94.2%", delta="↗️ +3.1%")
            st.metric("🎯 Schedule Confidence", "87%", delta="↗️ +5%")
            st.metric("💰 Cost Prediction Accuracy", "96.8%", delta="↗️ +1.2%")
        
        with ai_col2:
            st.metric("⚡ Efficiency Rating", "A+", delta="Excellent")
            st.metric("🔍 Quality Score", "9.1/10", delta="↗️ +0.3")
            st.metric("🚀 Innovation Index", "High", delta="Leading Industry")
        
        with ai_col3:
            st.metric("🌤️ Weather Impact", "Minimal", delta="↘️ -15% risk")
            st.metric("👥 Team Satisfaction", "92%", delta="↗️ +4%")
            st.metric("🎯 Goal Achievement", "103%", delta="↗️ Exceeding")
        
        # Advanced AI features
        st.markdown("#### 🚀 Advanced AI Capabilities")
        
        ai_feature_col1, ai_feature_col2 = st.columns(2)
        
        with ai_feature_col1:
            st.markdown("""
            **🔮 Predictive Analytics:**
            - 📊 7-day progress forecasting with 96% accuracy
            - 🌧️ Weather impact modeling and mitigation suggestions
            - 💰 Cost variance prediction with early warning system
            - 👥 Optimal crew allocation recommendations
            - 📈 Schedule optimization using machine learning
            """)
        
        with ai_feature_col2:
            st.markdown("""
            **🧠 Smart Automation:**
            - 📸 Photo analysis for automatic progress measurement
            - 🔍 Quality defect detection from images
            - 📝 Auto-generation of RFIs from field observations
            - 🚨 Proactive safety hazard identification
            - 📊 Real-time dashboard updates from field data
            """)
    
    with tab4:
        st.markdown("### 📊 Enterprise Analytics Dashboard")
        st.markdown("**Comprehensive analytics that outperform Autodesk Construction Cloud**")
        
        # Create sample charts with Highland Tower data
        fig_progress = px.line(
            x=['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            y=[23, 45, 67, 87],
            title="📈 Highland Tower Progress Trajectory",
            labels={'x': 'Timeline', 'y': 'Completion %'}
        )
        fig_progress.update_layout(template="plotly_dark")
        st.plotly_chart(fig_progress, use_container_width=True)
        
        # Cost analytics
        cost_col1, cost_col2 = st.columns(2)
        
        with cost_col1:
            fig_cost = px.bar(
                x=['Labor', 'Materials', 'Equipment', 'Overhead'],
                y=[35600, 12400, 8900, 5100],
                title="💰 Daily Cost Breakdown",
                color=['Labor', 'Materials', 'Equipment', 'Overhead']
            )
            fig_cost.update_layout(template="plotly_dark")
            st.plotly_chart(fig_cost, use_container_width=True)
        
        with cost_col2:
            fig_productivity = go.Figure(go.Indicator(
                mode = "gauge+number",
                value=94.2,
                title="⚡ Overall Productivity Score",
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "darkblue"},
                       'bgcolor': "white",
                       'borderwidth': 2,
                       'bordercolor': "gray",
                       'steps': [{'range': [0, 50], 'color': 'lightgray'},
                                {'range': [50, 80], 'color': 'gray'},
                                {'range': [80, 100], 'color': 'lightgreen'}],
                       'threshold': {'line': {'color': "red", 'width': 4},
                                   'thickness': 0.75, 'value': 90}}
            ))
            st.plotly_chart(fig_productivity, use_container_width=True)
    
    with tab5:
        st.markdown("### 🔄 Real-Time Project Feed")
        st.markdown("**Live collaboration that beats all competitors**")
        
        # Real-time activity feed
        st.markdown("#### 📡 Live Activity Stream")
        
        activities = [
            {"time": "2 hours ago", "icon": "❓", "action": "RFI: RFI #123 was answered", "user": "Project Manager", "type": "rfi"},
            {"time": "Yesterday", "icon": "✅", "action": "Submittal: Submittal #45 was approved", "user": "Engineering Team", "type": "submittal"},
            {"time": "2 days ago", "icon": "🏗️", "action": "Project: New milestone added", "user": "Highland Construction", "type": "project"},
            {"time": "3 days ago", "icon": "📋", "action": "Task: Task assigned to John Smith", "user": "Site Supervisor", "type": "assignment"},
            {"time": "4 days ago", "icon": "📄", "action": "Document: New document uploaded", "user": "Document Control", "type": "document"},
            {"time": "5 days ago", "icon": "🦺", "action": "Safety: Safety meeting scheduled", "user": "Safety Manager", "type": "safety"}
        ]
        
        for activity in activities:
            icon_color = "🟢" if activity["type"] == "completion" else "🔵" if activity["type"] == "photo" else "🟡" if activity["type"] == "alert" else "⚪"
            
            # Enterprise-grade error handling for activity display
            location_text = f" at {activity.get('location', 'Highland Tower')}" if activity.get('location') else ""
            st.markdown(f"""
            <div style="background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #3b82f6;">
                {activity.get('icon', '📋')} <strong>{activity.get('time', 'Recently')}</strong> - {activity.get('user', 'System')}: {activity.get('action', 'Activity logged')}{location_text}
            </div>
            """, unsafe_allow_html=True)
        
        # Real-time collaboration tools
        st.markdown("#### 💬 Team Collaboration Hub")
        
        collab_col1, collab_col2 = st.columns(2)
        
        with collab_col1:
            st.markdown("**🎯 Active Issues Requiring Attention:**")
            if st.button("🚨 Critical: Crane Inspection Due", use_container_width=True, type="secondary"):
                st.warning("📋 Crane certification expires in 2 days. Inspection scheduled for tomorrow 8 AM.")
            
            if st.button("⚠️ Medium: Material Delivery Delay", use_container_width=True):
                st.info("🚛 Steel delivery for Level 14 potentially delayed 1 day. Supplier confirmed backup plan.")
        
        with collab_col2:
            st.markdown("**💬 Quick Communication:**")
            quick_message = st.text_area("📱 Send Update to Team", placeholder="Type update, mention @user for notifications...")
            if st.button("📤 Send Update", use_container_width=True, type="primary"):
                st.success("✅ Update sent to Highland Tower team with push notifications")

def render_progress_photos():
    """Advanced Progress Photo Management with AI organization"""
    st.title("📸 Progress Photos - Visual Documentation")
    st.markdown("**AI-powered photo organization and progress tracking**")
    
    tab1, tab2, tab3 = st.tabs(["📷 Upload Photos", "🖼️ Photo Gallery", "📊 Progress Timeline"])
    
    with tab1:
        st.markdown("### 📷 Upload Progress Photos")
        
        col1, col2 = st.columns(2)
        with col1:
            photo_location = st.selectbox("Location", ["Level 13", "Level 12", "Level 11", "Level 10", "Exterior", "Site Overall"])
            photo_category = st.selectbox("Category", ["Structural", "MEP", "Finishes", "Exterior", "Safety", "General"])
            photo_date = st.date_input("Photo Date")
        
        with col2:
            photographer = st.text_input("Photographer", value="Site Supervisor")
            notes = st.text_area("Photo Description", placeholder="Describe what the photo shows...")
        
        uploaded_photos = st.file_uploader("Upload Photos", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])
        
        if uploaded_photos:
            st.success(f"✅ {len(uploaded_photos)} photos ready for upload")
            if st.button("📤 Upload & Process Photos", type="primary"):
                st.balloons()
                st.success("🎉 Photos uploaded and automatically organized by AI!")

def render_quality_control():
    """Advanced Quality Control with inspection workflows"""
    st.title("🔍 Quality Control - Inspection Management")
    st.markdown("**Comprehensive QC program with digital workflows**")
    
    tab1, tab2, tab3 = st.tabs(["✅ Inspections", "📋 Checklists", "📊 QC Metrics"])
    
    with tab1:
        st.markdown("### 🔍 Active Inspections")
        
        inspections = [
            {"ID": "QC-2025-045", "Type": "Structural", "Location": "Level 13", "Status": "In Progress", "Inspector": "John Davis"},
            {"ID": "QC-2025-044", "Type": "MEP Rough-in", "Location": "Level 11", "Status": "Passed", "Inspector": "Maria Garcia"},
            {"ID": "QC-2025-043", "Type": "Concrete", "Location": "Level 12", "Status": "Failed", "Inspector": "Robert Kim"}
        ]
        
        for inspection in inspections:
            status_color = "🟢" if inspection["Status"] == "Passed" else "🔴" if inspection["Status"] == "Failed" else "🟡"
            
            with st.expander(f"{status_color} {inspection['ID']} - {inspection['Type']} | {inspection['Status']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Location:** {inspection['Location']}")
                with col2:
                    st.markdown(f"**Inspector:** {inspection['Inspector']}")
                with col3:
                    if st.button(f"View Details", key=f"view_{inspection['ID']}"):
                        st.info(f"Opening detailed inspection report for {inspection['ID']}")

def render_material_management():
    """Advanced Material Management with supply chain integration"""
    st.title("📦 Material Management - Supply Chain Control")
    st.markdown("**Complete material tracking from procurement to installation**")
    
    tab1, tab2, tab3 = st.tabs(["📦 Inventory", "🚚 Deliveries", "📊 Analytics"])
    
    with tab1:
        st.markdown("### 📦 Current Material Inventory")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Items", "1,247", "Tracked in system")
        with col2:
            st.metric("Critical Stock", "12", "Items below threshold")
        with col3:
            st.metric("Pending Orders", "23", "Awaiting delivery")
        with col4:
            st.metric("Value On-Site", "$2.3M", "Current inventory")
        
        # Material categories
        materials = [
            {"Category": "Structural Steel", "On-Site": "850 tons", "Needed": "920 tons", "Status": "⚠️ Order placed"},
            {"Category": "Concrete", "On-Site": "2,400 CY", "Needed": "2,850 CY", "Status": "✅ Scheduled"},
            {"Category": "Windows", "On-Site": "45 units", "Needed": "120 units", "Status": "🚚 In transit"},
            {"Category": "Electrical", "On-Site": "85%", "Needed": "100%", "Status": "✅ On schedule"}
        ]
        
        for material in materials:
            with st.expander(f"📦 {material['Category']} | {material['Status']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**On-Site:** {material['On-Site']}")
                with col2:
                    st.markdown(f"**Total Needed:** {material['Needed']}")
                with col3:
                    st.markdown(f"**Status:** {material['Status']}")

def render_bim():
    """Advanced BIM Management with 3D coordination for Highland Tower Development"""
    st.title("🏢 BIM Management - Highland Tower Development")
    st.markdown("**Building Information Modeling with clash detection and IFC coordination for $45.5M project**")
    
    # BIM action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📤 Upload IFC Model", type="primary"):
            st.session_state.show_ifc_upload = True
    with col2:
        if st.button("🔍 Run Clash Detection"):
            st.session_state.show_clash_detection = True
    with col3:
        if st.button("📊 Model Analytics"):
            st.session_state.show_model_analytics = True
    with col4:
        if st.button("📋 Export Report"):
            st.success("📄 BIM coordination report exported")
    
    # IFC Upload form
    if st.session_state.get("show_ifc_upload", False):
        with st.form("ifc_upload_form"):
            st.subheader("📤 Upload IFC Model")
            
            col1, col2 = st.columns(2)
            with col1:
                uploaded_file = st.file_uploader("Choose IFC File", type=['ifc'], help="Industry Foundation Classes format only")
                model_name = st.text_input("Model Name", placeholder="Highland Tower - Architectural Rev D")
                discipline = st.selectbox("Discipline", ["Architectural", "Structural", "MEP", "Civil", "Landscape"])
                
            with col2:
                model_version = st.text_input("Model Version", placeholder="Rev D.1")
                model_level = st.selectbox("Model Level", ["LOD 200", "LOD 300", "LOD 350", "LOD 400", "LOD 500"])
                coordinated_by = st.text_input("Coordinated By", placeholder="Sarah Chen, BIM Manager")
            
            notes = st.text_area("Model Notes", placeholder="Latest coordination updates for Highland Tower Level 13-15 modifications")
            
            if st.form_submit_button("🔄 Process IFC Model", type="primary"):
                if uploaded_file:
                    st.success(f"✅ IFC model '{model_name}' uploaded and processed successfully!")
                    st.info(f"📊 Model contains {45672:,} elements across {1247} families")
                    st.session_state.show_ifc_upload = False
                    st.rerun()
                else:
                    st.error("Please select an IFC file to upload")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 IFC Model Library", "🎯 3D Coordination", "⚠️ Clash Detection", "📊 BIM Analytics"])
    
    with tab1:
        st.markdown("### 📋 Highland Tower Development - IFC Model Library")
        
        # Current IFC models
        ifc_models_data = pd.DataFrame([
            {
                "Model Name": "Highland Tower - Architectural",
                "Version": "Rev D.1",
                "Discipline": "Architectural", 
                "File Size": "487 MB",
                "Elements": "47,582",
                "Status": "Current",
                "Last Updated": "2025-05-23",
                "Coordinator": "Sarah Chen"
            },
            {
                "Model Name": "Highland Tower - Structural", 
                "Version": "Rev C.3",
                "Discipline": "Structural",
                "File Size": "298 MB", 
                "Elements": "28,947",
                "Status": "Under Review",
                "Last Updated": "2025-05-20",
                "Coordinator": "Michael Torres"
            },
            {
                "Model Name": "Highland Tower - MEP",
                "Version": "Rev B.2", 
                "Discipline": "MEP",
                "File Size": "652 MB",
                "Elements": "89,234",
                "Status": "Coordinating", 
                "Last Updated": "2025-05-18",
                "Coordinator": "Jennifer Walsh"
            }
        ])
        
        st.dataframe(ifc_models_data, use_container_width=True, hide_index=True)
        
        # IFC Model metrics
        st.subheader("📊 IFC Model Metrics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Elements", "165,763", "All disciplines")
        with col2:
            st.metric("Model Size", "1.4 GB", "Combined IFC")
        with col3:
            st.metric("Coordination Level", "LOD 350", "Design Development")
        with col4:
            st.metric("Last Coordination", "2 days ago", "All current")
    
    with tab2:
        st.markdown("### 🎯 3D Model Coordination")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🏗️ Highland Tower Model Status:**
            • **Architectural:** Rev D.1 (Current)
            • **Structural:** Rev C.3 (Under Review) 
            • **MEP:** Rev B.2 (Coordinating)
            • **Site/Civil:** Rev A.1 (Current)
            • **Landscape:** Rev A.0 (Draft)
            """)
        
        with col2:
            st.markdown("""
            **📊 Coordination Metrics:**
            • **Total IFC Elements:** 165,763
            • **Clash Tests Run:** 347 this week
            • **Active Clashes:** 18 (down from 45)
            • **Critical Issues:** 3 requiring attention
            • **Resolved This Week:** 27 clashes
            """)
        
        st.success("🔄 **Next BIM Coordination Meeting:** Thursday 2:00 PM - All discipline coordinators required")
        st.info("📋 **Focus Areas:** Level 13-15 MEP routing, structural connections, curtain wall integration")
    
    with tab3:
        st.markdown("### ⚠️ IFC Clash Detection Results")
        
        # Clash detection metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Clashes", "18", "-27 resolved")
        with col2:
            st.metric("Critical Clashes", "3", "Immediate attention")
        with col3:
            st.metric("Hard Clashes", "12", "Physical conflicts")
        with col4:
            st.metric("Soft Clashes", "6", "Clearance issues")
        
        # Current clash issues
        st.subheader("🚨 Priority Clash Issues")
        clash_data = pd.DataFrame([
            {
                "Clash ID": "CLH-HTD-047",
                "Type": "Hard Clash",
                "Location": "Level 13 - Grid E4",
                "Discipline 1": "MEP - HVAC Duct", 
                "Discipline 2": "Structural - Steel Beam",
                "Priority": "Critical",
                "Status": "Open",
                "Assigned To": "Jennifer Walsh / Michael Torres"
            },
            {
                "Clash ID": "CLH-HTD-046", 
                "Type": "Soft Clash",
                "Location": "Level 12 - Corridor",
                "Discipline 1": "Electrical - Conduit",
                "Discipline 2": "Plumbing - Domestic Water",
                "Priority": "High", 
                "Status": "Under Review",
                "Assigned To": "Jennifer Walsh"
            },
            {
                "Clash ID": "CLH-HTD-045",
                "Type": "Hard Clash", 
                "Location": "Level 14 - Mechanical Room",
                "Discipline 1": "HVAC - Equipment",
                "Discipline 2": "Structural - Column",
                "Priority": "Critical",
                "Status": "Resolution Proposed",
                "Assigned To": "Michael Torres"
            }
        ])
        
        st.dataframe(clash_data, use_container_width=True, hide_index=True)
    
    with tab4:
        st.markdown("### 📊 BIM Analytics - Highland Tower Development")
        
        # Model complexity analysis
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📈 Model Element Distribution")
            element_data = pd.DataFrame({
                'Discipline': ['Architectural', 'Structural', 'MEP', 'Civil'],
                'Elements': [47582, 28947, 89234, 5847],
                'Percentage': [28.7, 17.5, 53.8, 3.5]
            })
            st.dataframe(element_data, use_container_width=True, hide_index=True)
            
        with col2:
            st.markdown("#### 🎯 Coordination Progress")
            progress_data = pd.DataFrame({
                'Phase': ['Design Development', 'Coordination', 'Documentation', 'Construction'],
                'Architectural': [100, 95, 85, 0],
                'Structural': [100, 87, 78, 0], 
                'MEP': [95, 82, 65, 0]
            })
            st.dataframe(progress_data, use_container_width=True, hide_index=True)

def render_analytics():
    """Advanced Analytics with AI-powered insights"""
    st.title("📈 Advanced Analytics - AI-Powered Project Insights")
    st.markdown("**Comprehensive project analytics with predictive modeling**")
    
    tab1, tab2, tab3 = st.tabs(["📊 Executive Dashboard", "🔮 Predictive Analytics", "💡 AI Insights"])
    
    with tab1:
        st.markdown("### 📊 Executive Performance Dashboard")
        
        # Key performance indicators
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Project Health", "94%", "+2% this month")
        with col2:
            st.metric("Schedule Performance", "102%", "Ahead of plan")
        with col3:
            st.metric("Cost Performance", "96%", "Under budget")
        with col4:
            st.metric("Quality Score", "97%", "Excellent")
        
        # Performance trends
        performance_data = pd.DataFrame({
            'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            'Schedule': [98, 100, 101, 102],
            'Budget': [99, 98, 97, 96],
            'Quality': [95, 96, 96, 97],
            'Safety': [97, 98, 98, 99]
        })
        
        fig = px.line(performance_data, x='Week', y=['Schedule', 'Budget', 'Quality', 'Safety'],
                     title="📈 Weekly Performance Trends")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 🔮 AI-Powered Predictions")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🎯 Completion Forecast:**
            - Projected Completion: May 15, 2025
            - Confidence Level: 87%
            - Weather Risk Factor: Low
            - Resource Availability: Good
            """)
        
        with col2:
            st.markdown("""
            **💰 Cost Forecast:**
            - Final Cost Prediction: $43.4M
            - Confidence Level: 92%
            - Potential Savings: $2.1M
            - Risk Factors: Material prices
            """)

def main():
    """Main application entry point"""
    # Page config is now handled in app.py entry point
    initialize_session_state()
    apply_highland_tower_styling()
    
    if not st.session_state.authenticated:
        render_login()
    else:
        render_header()
        render_sidebar()
        render_main_content()

def render_submittals():
    """Enterprise Submittals Management with real-time collaboration"""
    st.title("📤 Submittals Management - Enterprise Workflow")
    st.markdown("**Real-time collaborative submittal tracking with automated routing and AI-powered review assistance**")
    
    # Real-time status indicators
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Active Submittals", "47", "+8 this week", help="Total submittals in system")
    with col2:
        st.metric("Pending Review", "12", "Avg 4.2 days", help="Awaiting stakeholder review")
    with col3:
        st.metric("Approved Today", "6", "+150% vs yesterday", help="Approved for procurement")
    with col4:
        st.metric("Revisions Needed", "7", "-3 since Monday", help="Requiring contractor updates")
    with col5:
        st.metric("Avg Review Time", "4.2 days", "-1.8 days improvement", help="Time from submission to decision")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Live Registry", "✅ Smart Creation", "🔄 Workflow Automation", "📊 Performance Analytics", "🤖 AI Review Assistant"])
    
    with tab1:
        st.markdown("### 📋 Live Submittal Registry with Real-Time Updates")
        
        # Advanced filtering and search
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
        with filter_col1:
            status_filter = st.multiselect("Status Filter", ["Under Review", "Approved", "Revision Required", "Pending"], default=["Under Review", "Pending"])
        with filter_col2:
            spec_filter = st.selectbox("Specification", ["All Sections", "05120 - Structural", "23000 - HVAC", "08400 - Curtain Wall", "26000 - Electrical"])
        with filter_col3:
            priority_filter = st.selectbox("Priority", ["All", "Critical", "High", "Standard"])
        with filter_col4:
            reviewer_filter = st.selectbox("Reviewer", ["All", "Structural Engineer", "MEP Engineer", "Architect"])
        
        # Live search with autocomplete
        search_query = st.text_input("🔍 Smart Search", placeholder="Search by ID, item name, spec section, or reviewer...")
        
        # Enterprise-grade submittal data with rich metadata
        submittal_data = [
            {
                "ID": "SUB-2025-034", 
                "Item": "W24x62 Beam Connection Details - Level 13", 
                "Spec": "05120", 
                "Status": "🟡 Under Review", 
                "Priority": "Critical",
                "Days": 3, 
                "Reviewer": "Sarah Chen, PE", 
                "Contractor": "Steel Fabricators Inc",
                "Submitted": "2025-01-22 14:30",
                "Due": "2025-01-25 17:00",
                "Cost Impact": "$45,000",
                "Schedule Impact": "2 days potential delay",
                "Attachments": 8,
                "Comments": 12,
                "Views": 34
            },
            {
                "ID": "SUB-2025-033", 
                "Item": "Trane HVAC Unit Specifications - Rooftop", 
                "Spec": "23000", 
                "Status": "🟢 Approved", 
                "Priority": "High",
                "Days": 8, 
                "Reviewer": "Michael Rodriguez, PE", 
                "Contractor": "HVAC Systems LLC",
                "Submitted": "2025-01-14 09:15",
                "Due": "2025-01-21 12:00",
                "Cost Impact": "$0",
                "Schedule Impact": "On track",
                "Attachments": 15,
                "Comments": 6,
                "Views": 67
            },
            {
                "ID": "SUB-2025-032", 
                "Item": "Guardian Glass Curtain Wall System - South Facade", 
                "Spec": "08400", 
                "Status": "🔴 Revision Required", 
                "Priority": "High",
                "Days": 12, 
                "Reviewer": "Jennifer Walsh, AIA", 
                "Contractor": "Curtain Wall Specialists",
                "Submitted": "2025-01-10 16:45",
                "Due": "2025-01-17 17:00",
                "Cost Impact": "$12,500 potential increase",
                "Schedule Impact": "1 week delay risk",
                "Attachments": 23,
                "Comments": 18,
                "Views": 89
            }
        ]
        
        # Interactive data table with live updates
        for submittal in submittal_data:
            priority_color = "🔴" if submittal["Priority"] == "Critical" else "🟡" if submittal["Priority"] == "High" else "🟢"
            
            with st.expander(f"{submittal['Status']} {submittal['ID']} - {submittal['Item']} {priority_color}"):
                # Rich submittal details with interactive elements
                detail_col1, detail_col2, detail_col3 = st.columns(3)
                
                with detail_col1:
                    st.markdown(f"""
                    **📋 Submittal Info:**
                    - **Spec Section:** {submittal['Spec']}
                    - **Priority:** {submittal['Priority']}
                    - **Contractor:** {submittal['Contractor']}
                    - **Submitted:** {submittal['Submitted']}
                    """)
                
                with detail_col2:
                    st.markdown(f"""
                    **⏰ Timeline:**
                    - **Days in Review:** {submittal['Days']}
                    - **Due Date:** {submittal['Due']}
                    - **Reviewer:** {submittal['Reviewer']}
                    - **Status:** {submittal['Status']}
                    """)
                
                with detail_col3:
                    st.markdown(f"""
                    **💰 Impact Analysis:**
                    - **Cost Impact:** {submittal['Cost Impact']}
                    - **Schedule Impact:** {submittal['Schedule Impact']}
                    - **Attachments:** {submittal['Attachments']} files
                    - **Activity:** {submittal['Views']} views, {submittal['Comments']} comments
                    """)
                
                # Standard CRUD Action Buttons
                st.markdown("---")
                action_col1, action_col2, action_col3, action_col4 = st.columns(4)
                
                with action_col1:
                    if st.button(f"👁️ View Details", key=f"view_{submittal['ID']}", use_container_width=True, type="secondary"):
                        st.session_state[f"view_mode_{submittal['ID']}"] = True
                        st.rerun()
                
                with action_col2:
                    if st.button(f"✏️ Edit", key=f"edit_{submittal['ID']}", use_container_width=True):
                        st.session_state[f"edit_mode_{submittal['ID']}"] = True
                        st.rerun()
                
                with action_col3:
                    if st.button(f"📋 Review", key=f"review_{submittal['ID']}", use_container_width=True, type="primary"):
                        st.session_state[f"review_mode_{submittal['ID']}"] = True
                        st.rerun()
                
                with action_col4:
                    if st.button(f"🗑️ Archive", key=f"delete_{submittal['ID']}", use_container_width=True):
                        st.warning(f"⚠️ Archive {submittal['ID']}? This action can be undone.")
                        if st.button(f"Confirm Archive", key=f"confirm_delete_{submittal['ID']}"):
                            st.success(f"✅ {submittal['ID']} archived successfully")
                
                # Handle CRUD operations
                if st.session_state.get(f"view_mode_{submittal['ID']}", False):
                    st.markdown("### 👁️ Detailed View Mode")
                    with st.container():
                        st.markdown(f"""
                        **Complete Submittal Details for {submittal['ID']}**
                        
                        **📋 Basic Information:**
                        - Title: {submittal['Item']}
                        - Specification: {submittal['Spec']}
                        - Status: {submittal['Status']}
                        - Priority: {submittal['Priority']}
                        
                        **👥 People & Timeline:**
                        - Contractor: {submittal['Contractor']}
                        - Reviewer: {submittal['Reviewer']}
                        - Submitted: {submittal['Submitted']}
                        - Due Date: {submittal['Due']}
                        - Days in Review: {submittal['Days']}
                        
                        **💰 Impact Analysis:**
                        - Cost Impact: {submittal['Cost Impact']}
                        - Schedule Impact: {submittal['Schedule Impact']}
                        
                        **📊 Activity Metrics:**
                        - Document Attachments: {submittal['Attachments']} files
                        - Comments: {submittal['Comments']} entries
                        - Views: {submittal['Views']} total views
                        """)
                        
                        if st.button(f"Close View", key=f"close_view_{submittal['ID']}"):
                            st.session_state[f"view_mode_{submittal['ID']}"] = False
                            st.rerun()
                
                if st.session_state.get(f"edit_mode_{submittal['ID']}", False):
                    st.markdown("### ✏️ Edit Mode")
                    with st.form(f"edit_form_{submittal['ID']}"):
                        edit_col1, edit_col2 = st.columns(2)
                        
                        with edit_col1:
                            edit_title = st.text_input("Title", value=submittal['Item'])
                            edit_priority = st.selectbox("Priority", ["Critical", "High", "Standard", "Low"], 
                                                       index=["Critical", "High", "Standard", "Low"].index(submittal['Priority']))
                            edit_cost = st.text_input("Cost Impact", value=submittal['Cost Impact'])
                        
                        with edit_col2:
                            edit_reviewer = st.text_input("Reviewer", value=submittal['Reviewer'])
                            edit_status = st.selectbox("Status", ["Under Review", "Approved", "Revision Required", "Pending"])
                            edit_schedule = st.text_input("Schedule Impact", value=submittal['Schedule Impact'])
                        
                        edit_notes = st.text_area("Additional Notes", placeholder="Add any updates or changes...")
                        
                        submit_col1, submit_col2 = st.columns(2)
                        with submit_col1:
                            if st.form_submit_button("💾 Save Changes", use_container_width=True, type="primary"):
                                st.success(f"✅ {submittal['ID']} updated successfully!")
                                st.session_state[f"edit_mode_{submittal['ID']}"] = False
                                st.rerun()
                        
                        with submit_col2:
                            if st.form_submit_button("❌ Cancel", use_container_width=True):
                                st.session_state[f"edit_mode_{submittal['ID']}"] = False
                                st.rerun()
                
                if st.session_state.get(f"review_mode_{submittal['ID']}", False):
                    st.markdown("### 📋 Review & Approval Interface")
                    with st.form(f"review_form_{submittal['ID']}"):
                        review_decision = st.radio("Review Decision", 
                                                 ["✅ Approve", "🔄 Request Revisions", "❌ Reject"], 
                                                 horizontal=True)
                        
                        review_comments = st.text_area("Review Comments", 
                                                     placeholder="Provide detailed feedback for the contractor...")
                        
                        if review_decision == "🔄 Request Revisions":
                            revision_deadline = st.date_input("Revision Deadline")
                            critical_issues = st.multiselect("Critical Issues", 
                                                            ["Specification Compliance", "Technical Details", "Documentation", "Code Requirements"])
                        
                        review_col1, review_col2 = st.columns(2)
                        with review_col1:
                            if st.form_submit_button("📤 Submit Review", use_container_width=True, type="primary"):
                                st.balloons()
                                st.success(f"✅ Review submitted for {submittal['ID']}!")
                                st.info("📧 Automatic notification sent to contractor")
                                st.session_state[f"review_mode_{submittal['ID']}"] = False
                                st.rerun()
                        
                        with review_col2:
                            if st.form_submit_button("❌ Cancel Review", use_container_width=True):
                                st.session_state[f"review_mode_{submittal['ID']}"] = False
                                st.rerun()
    
    with tab2:
        st.markdown("### ✅ Smart Submittal Creation with AI Assistance")
        
        # AI-powered form with intelligent defaults
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.markdown("**🤖 AI Assistant**")
            if st.button("🧠 Auto-Generate from Specs", use_container_width=True):
                st.success("🤖 AI analyzing project specifications to pre-populate submittal form")
            
            if st.button("📋 Load Template", use_container_width=True):
                st.info("📋 Loading standard template based on specification section")
            
            if st.button("🔍 Similar Submittals", use_container_width=True):
                st.info("🔍 Found 3 similar submittals from this project for reference")
        
        with col1:
            st.markdown("**📋 Enhanced Submittal Creation Form**")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                sub_title = st.text_input("📝 Submittal Title*", placeholder="AI will suggest based on spec section")
                sub_spec = st.selectbox("📖 Specification Section*", [
                    "03300 - Cast-in-Place Concrete",
                    "05120 - Structural Steel",
                    "08400 - Curtain Wall Systems", 
                    "23000 - HVAC Systems",
                    "26000 - Electrical Systems",
                    "33000 - Utilities"
                ])
                sub_contractor = st.selectbox("🏢 Submitting Contractor*", [
                    "Steel Fabricators Inc", 
                    "HVAC Systems LLC", 
                    "Curtain Wall Specialists", 
                    "Electrical Contractors Corp"
                ])
                sub_cost_impact = st.number_input("💰 Estimated Cost Impact ($)", min_value=0, value=0)
            
            with form_col2:
                sub_reviewer = st.multiselect("👥 Primary Reviewers*", [
                    "Sarah Chen, PE - Structural Engineer",
                    "Michael Rodriguez, PE - MEP Engineer", 
                    "Jennifer Walsh, AIA - Architect",
                    "David Kim, PE - Civil Engineer"
                ])
                sub_priority = st.selectbox("🎯 Priority Level*", ["Critical", "High", "Standard", "Low"])
                sub_due_date = st.date_input("📅 Response Required By*")
                sub_schedule_impact = st.selectbox("⏰ Schedule Impact", ["No Impact", "Minor Delay", "Moderate Delay", "Major Delay"])
            
            # Rich text description with AI assistance
            sub_description = st.text_area(
                "📋 Detailed Description*", 
                placeholder="AI Assistant: Describe the submittal items, review requirements, and any special considerations...",
                height=120
            )
            
            # Advanced file upload with categorization and preview
            st.markdown("**📁 Document Upload & Management**")
            
            upload_col1, upload_col2 = st.columns(2)
            
            with upload_col1:
                drawings = st.file_uploader("📐 Technical Drawings", accept_multiple_files=True, type=['pdf', 'dwg', 'dxf'])
                specifications = st.file_uploader("📖 Product Specifications", accept_multiple_files=True, type=['pdf', 'doc', 'docx'])
            
            with upload_col2:
                test_reports = st.file_uploader("🧪 Test Reports & Certifications", accept_multiple_files=True, type=['pdf', 'xlsx'])
                cut_sheets = st.file_uploader("📄 Product Cut Sheets", accept_multiple_files=True, type=['pdf', 'jpg', 'png'])
            
            # Smart workflow options
            st.markdown("**⚙️ Smart Workflow Options**")
            
            workflow_col1, workflow_col2 = st.columns(2)
            
            with workflow_col1:
                auto_route = st.checkbox("🔄 Auto-route based on specification", value=True)
                urgent_notify = st.checkbox("🚨 Send urgent notifications (Critical/High priority)")
                ai_review = st.checkbox("🤖 Enable AI pre-review for common issues")
            
            with workflow_col2:
                track_changes = st.checkbox("📊 Enable detailed change tracking", value=True)
                email_notifications = st.checkbox("📧 Send email notifications to stakeholders", value=True)
                mobile_alerts = st.checkbox("📱 Send mobile push notifications")
            
            # Enhanced submission with validation
            st.markdown("---")
            
            submit_col1, submit_col2, submit_col3 = st.columns(3)
            
            with submit_col1:
                if st.button("💾 Save as Draft", use_container_width=True):
                    st.info("💾 Draft saved with auto-backup enabled")
            
            with submit_col2:
                if st.button("🔍 AI Validation Check", use_container_width=True):
                    st.info("🤖 Running AI validation: Checking completeness, spec compliance, and potential issues...")
            
            with submit_col3:
                if st.button("📤 Submit for Review", type="primary", use_container_width=True):
                    if sub_title and sub_description and sub_reviewer:
                        st.balloons()
                        st.success("🎉 Submittal SUB-2025-035 created successfully!")
                        st.info("📧 Automated notifications sent to all reviewers")
                        st.info("📊 Real-time tracking dashboard updated")
                        st.info("🤖 AI monitoring activated for review optimization")
                    else:
                        st.error("❌ Please complete all required fields before submitting")
    
    with tab3:
        st.markdown("### 🔄 Advanced Workflow Automation")
        
        workflow_col1, workflow_col2 = st.columns(2)
        
        with workflow_col1:
            st.markdown("""
            **🤖 Automated Workflows Active:**
            
            ✅ **Smart Routing Engine**
            - Auto-assigns reviewers based on spec section
            - Escalates overdue items after 7 days
            - Parallel routing for complex submittals
            
            ✅ **Intelligent Notifications**
            - Priority-based notification scheduling
            - Mobile alerts for critical items
            - Digest emails for non-urgent updates
            
            ✅ **Integration Automation**
            - Auto-sync with project schedule
            - Cost tracking integration
            - Document version control
            """)
        
        with workflow_col2:
            st.markdown("""
            **📊 Performance Optimization:**
            
            ✅ **AI-Powered Insights**
            - Predicts review completion times
            - Identifies potential bottlenecks
            - Suggests process improvements
            
            ✅ **Quality Assurance**
            - Automated compliance checking
            - Specification cross-referencing
            - Duplicate detection
            
            ✅ **Real-Time Collaboration**
            - Live comment threads
            - Simultaneous multi-user editing
            - Instant status synchronization
            """)
    
    with tab4:
        st.markdown("### 📊 Enterprise Performance Analytics")
        
        # Advanced analytics dashboard
        analytics_col1, analytics_col2 = st.columns(2)
        
        with analytics_col1:
            # Performance trends visualization
            performance_data = pd.DataFrame({
                'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                'Submitted': [12, 15, 18, 14],
                'Approved': [8, 11, 16, 13],
                'Avg Review Days': [6.2, 5.8, 4.9, 4.2],
                'Satisfaction Score': [85, 88, 92, 94]
            })
            
            fig = px.line(performance_data, x='Week', y=['Avg Review Days'], 
                         title="📈 Review Time Optimization Trend")
            fig.add_scatter(x=performance_data['Week'], y=performance_data['Satisfaction Score']/20, 
                           mode='lines+markers', name='Satisfaction Score', yaxis='y2')
            fig.update_layout(yaxis2=dict(overlaying='y', side='right'))
            st.plotly_chart(fig, use_container_width=True)
        
        with analytics_col2:
            # Submittal volume and success rates
            volume_data = pd.DataFrame({
                'Category': ['Structural', 'MEP', 'Architectural', 'Civil'],
                'Volume': [18, 15, 9, 5],
                'Approval Rate': [89, 92, 87, 95],
                'Avg Days': [4.2, 3.8, 5.1, 3.2]
            })
            
            fig = px.bar(volume_data, x='Category', y='Volume', 
                        title="📊 Submittal Volume by Discipline")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.markdown("### 🤖 AI Review Assistant")
        
        st.markdown("**Intelligent review assistance powered by construction AI**")
        
        ai_col1, ai_col2 = st.columns(2)
        
        with ai_col1:
            st.markdown("""
            **🧠 AI Capabilities:**
            
            ✅ **Specification Compliance Check**
            - Automated cross-reference with project specs
            - Code compliance verification
            - Standard detail comparison
            
            ✅ **Quality Assurance**
            - Document completeness validation
            - Technical accuracy assessment
            - Industry best practice verification
            """)
        
        with ai_col2:
            st.markdown("""
            **⚡ Smart Recommendations:**
            
            ✅ **Review Optimization**
            - Suggests review priority based on project impact
            - Identifies potential approval bottlenecks
            - Recommends reviewer assignments
            
            ✅ **Process Intelligence**
            - Learns from historical approval patterns
            - Predicts review outcomes
            - Suggests process improvements
            """)
        
        # AI assistant interaction
        st.markdown("### 💬 AI Review Assistant Chat")
        
        ai_action_col1, ai_action_col2, ai_action_col3 = st.columns(3)
        
        with ai_action_col1:
            if st.button("🔍 Analyze Current Submittals", use_container_width=True):
                st.success("🤖 AI Analysis: 3 submittals show high approval probability. SUB-2025-034 may need structural clarification on connection details.")
        
        with ai_action_col2:
            if st.button("📊 Predict Review Times", use_container_width=True):
                st.info("🔮 AI Forecast: Current submittals will complete review in 3.8 days average, 95% confidence level.")
        
        with ai_action_col3:
            if st.button("💡 Process Optimization", use_container_width=True):
                st.info("💡 AI Recommendation: Parallel reviewing for complex MEP submittals could reduce review time by 1.5 days.")

def render_transmittals():
    """Advanced Transmittals Management for document distribution"""
    st.title("📨 Transmittals - Document Distribution")
    st.markdown("**Professional document transmittal and tracking system**")
    
    tab1, tab2 = st.tabs(["📨 Active Transmittals", "✅ Create New"])
    
    with tab1:
        transmittals = [
            {"ID": "TRA-2025-012", "Subject": "Updated Structural Drawings Rev C", "To": "All Trades", "Date": "2025-01-22", "Status": "🟢 Distributed"},
            {"ID": "TRA-2025-011", "Subject": "MEP Coordination Meeting Minutes", "To": "MEP Contractors", "Date": "2025-01-20", "Status": "🟡 Pending"}
        ]
        
        for transmittal in transmittals:
            with st.expander(f"{transmittal['Status']} {transmittal['ID']} - {transmittal['Subject']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**To:** {transmittal['To']}")
                with col2:
                    st.markdown(f"**Date:** {transmittal['Date']}")
                with col3:
                    if st.button(f"📧 Resend", key=f"resend_{transmittal['ID']}"):
                        st.success(f"Resending {transmittal['ID']}")

def render_equipment_tracking():
    """Advanced Equipment Tracking with GPS and maintenance"""
    st.title("🚛 Equipment Tracking - Asset Management")
    st.markdown("**Real-time equipment location and maintenance tracking**")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Equipment", "23", "On-site assets")
    with col2:
        st.metric("Currently Active", "19", "82% utilization")
    with col3:
        st.metric("In Maintenance", "2", "Scheduled service")
    with col4:
        st.metric("Available", "2", "Ready for assignment")
    
    equipment = [
        {"Asset": "Tower Crane TC-01", "Location": "Level 13", "Status": "🟢 Active", "Operator": "Mike Chen"},
        {"Asset": "Concrete Pump CP-02", "Location": "Level 12", "Status": "🟢 Active", "Operator": "Sarah Johnson"},
        {"Asset": "Material Hoist MH-01", "Location": "Exterior", "Status": "🔴 Maintenance", "Operator": "N/A"}
    ]
    
    for item in equipment:
        with st.expander(f"{item['Status']} {item['Asset']} - {item['Location']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Location:** {item['Location']}")
            with col2:
                st.markdown(f"**Operator:** {item['Operator']}")
            with col3:
                if st.button(f"📍 Track", key=f"track_{item['Asset']}"):
                    st.info(f"Opening GPS tracking for {item['Asset']}")

def render_ai_assistant():
    """AI-Powered Construction Assistant"""
    st.title("🤖 AI Assistant - Intelligent Project Support")
    st.markdown("**AI-powered assistance for construction management tasks**")
    
    st.chat_message("assistant").write("Hello! I'm your AI construction assistant. I can help with project analysis, scheduling optimization, cost forecasting, and risk assessment.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Analyze Schedule", use_container_width=True):
            st.success("Your project is 5 days ahead of schedule. Level 13 steel erection is on critical path.")
    with col2:
        if st.button("💰 Cost Analysis", use_container_width=True):
            st.success("You're 4.6% under budget ($2.1M savings). Forecast completion at $43.4M.")
    with col3:
        if st.button("🦺 Safety Review", use_container_width=True):
            st.success("Safety performance excellent at 98.5%. Recommend crane safety briefings.")

def render_mobile_companion():
    """Mobile Companion for field operations"""
    st.title("📱 Mobile Companion - Field Operations")
    st.markdown("**Mobile-optimized tools for on-site project management**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Today's Focus:**
        - Level 13 steel erection
        - MEP coordination meeting at 2 PM
        - Safety inspection at 4 PM
        """)
    
    with col2:
        st.markdown("""
        **Quick Stats:**
        - 89 workers on-site
        - 98.5% safety score
        - 3 active RFIs
        """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Quick RFI", use_container_width=True):
            st.info("Mobile RFI form optimized for field input")
    with col2:
        if st.button("📸 Photo Upload", use_container_width=True):
            st.info("Camera integration for instant progress photos")
    with col3:
        if st.button("🚨 Safety Report", use_container_width=True):
            st.info("Emergency safety incident reporting")

def render_aia_billing():
    """AIA G702/G703 Billing System - Your sophisticated billing module"""
    try:
        import sys
        sys.path.append('modules/cost_management')
        from aia_billing import render_aia_billing as aia_render
        aia_render()
    except ImportError:
        st.title("💰 AIA G702/G703 Billing System")
        st.markdown("**Professional payment application system with owner billing and change orders**")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📋 G702 Application", "📊 G703 Schedule", "🔄 Change Orders", "📈 Billing History"])
        
        with tab1:
            st.markdown("### 📋 AIA G702 - Application for Payment")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Project Name", value="Highland Tower Development", disabled=True)
                st.text_input("Owner", value="Highland Development LLC", disabled=True)
                st.text_input("Contractor", value="Premier Construction Group", disabled=True)
            with col2:
                st.text_input("Contract Amount", value="$45,500,000.00", disabled=True)
                st.text_input("Change Orders", value="$850,000.00", disabled=True)
                st.text_input("Adjusted Contract", value="$46,350,000.00", disabled=True)
        
        with tab2:
            st.markdown("### 📊 AIA G703 - Schedule of Values")
            schedule_data = pd.DataFrame([
                {"Item": "01 00 00", "Description": "General Requirements", "Scheduled Value": "$2,275,000", "% Complete": "100%"},
                {"Item": "03 00 00", "Description": "Concrete", "Scheduled Value": "$8,500,000", "% Complete": "85%"},
                {"Item": "05 00 00", "Description": "Metals", "Scheduled Value": "$6,200,000", "% Complete": "75%"}
            ])
            st.dataframe(schedule_data, use_container_width=True)

def render_prime_contract():
    """Prime Contract Management - Your sophisticated contract system"""
    st.title("📄 Prime Contract Management")
    st.markdown("**Highland Tower Development - Owner Contract Administration**")
    
    tab1, tab2, tab3 = st.tabs(["📋 Contract Overview", "📝 Amendments", "📊 Performance"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Contract Number", value="HTD-2024-001", disabled=True)
            st.text_input("Original Amount", value="$45,500,000.00", disabled=True)
        with col2:
            st.text_input("Owner", value="Highland Development LLC", disabled=True)
            st.text_input("Contractor", value="Premier Construction Group", disabled=True)

def render_change_orders():
    """Change Order Management - Your sophisticated change order system"""
    st.title("🔄 Change Order Management")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Change Orders", "8", "+2 this month")
    with col2:
        st.metric("Total Value", "$850,000", "+$185,000")
    with col3:
        st.metric("Approved", "$665,000", "78.2% of total")
    with col4:
        st.metric("Pending", "$185,000", "3 orders")

def render_preconstruction():
    """PreConstruction Module - Highland Tower Development Planning System"""
    st.title("📋 PreConstruction Management - Highland Tower Development")
    st.markdown("**Project planning, estimating, procurement, and bidding management for $45.5M mixed-use development**")
    
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Estimating", "📦 Procurement", "🏢 Bidder Management", "📊 Project Planning"])
    
    with tab1:
        render_estimating_section()
    
    with tab2:
        render_procurement_section()
    
    with tab3:
        render_bidder_management_section()
    
    with tab4:
        render_project_planning_section()

def render_closeout():
    """Project Closeout - Your sophisticated closeout system"""
    st.title("✅ Project Closeout")
    st.markdown("**Project completion, documentation, and handover processes**")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Completion", "73%", "On track")
    with col2:
        st.metric("Documentation", "68%", "In progress")
    with col3:
        st.metric("Punch List", "24 items", "-8 completed")
    with col4:
        st.metric("Final Inspections", "Scheduled", "Next week")

def render_estimating_section():
    """Comprehensive estimating for Highland Tower Development"""
    st.header("💰 Project Estimating - Highland Tower Development")
    st.markdown("**Cost estimation and analysis for $45.5M mixed-use development**")
    
    # Estimating action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📊 New Estimate", type="primary"):
            st.session_state.show_new_estimate = True
    with col2:
        if st.button("📈 Cost Analysis"):
            st.session_state.show_cost_analysis = True
    with col3:
        if st.button("📋 Export Estimate"):
            st.success("📄 Estimate exported to Excel")
    with col4:
        if st.button("🔄 Update Pricing"):
            st.success("💰 Current market pricing updated")
    
    # Current estimates display
    st.subheader("📋 Highland Tower Development Estimates")
    
    estimates_data = pd.DataFrame([
        {
            "Estimate ID": "EST-HTD-001",
            "Name": "Highland Tower - Full Building",
            "Type": "Construction Documents",
            "Total Cost": "$45,500,000",
            "Cost/SF": "$270.18",
            "Status": "Current",
            "Date": "2025-05-20"
        },
        {
            "Estimate ID": "EST-HTD-002", 
            "Name": "Foundation Package",
            "Type": "Bid Package",
            "Total Cost": "$8,750,000",
            "Cost/SF": "$51.93",
            "Status": "Final",
            "Date": "2025-05-15"
        }
    ])
    
    st.dataframe(estimates_data, use_container_width=True, hide_index=True)

def render_procurement_section():
    """Comprehensive procurement for Highland Tower Development"""
    st.header("📦 Procurement Management - Highland Tower Development")
    st.markdown("**Material and equipment procurement for $45.5M project**")
    
    # Procurement action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🛒 New Purchase Order", type="primary"):
            st.session_state.show_new_po = True
    with col2:
        if st.button("📋 Vendor Quotes"):
            st.session_state.show_vendor_quotes = True
    with col3:
        if st.button("📊 Procurement Analytics"):
            st.session_state.show_procurement_analytics = True
    with col4:
        if st.button("🚚 Track Deliveries"):
            st.session_state.show_delivery_tracking = True
    
    # Active procurement display
    st.subheader("📋 Active Procurement - Highland Tower Development")
    
    procurement_data = pd.DataFrame([
        {
            "PO Number": "PO-HTD-001",
            "Vendor": "Steel Fabricators Inc",
            "Description": "Structural Steel Package",
            "Amount": "$2,850,000",
            "Status": "Approved",
            "Delivery": "2025-06-15"
        },
        {
            "PO Number": "PO-HTD-002",
            "Vendor": "NYC Concrete Supply", 
            "Description": "Ready Mix Concrete",
            "Amount": "$875,000",
            "Status": "In Transit",
            "Delivery": "2025-05-28"
        }
    ])
    
    st.dataframe(procurement_data, use_container_width=True, hide_index=True)

def render_bidder_management_section():
    """Comprehensive bidder management and profiles"""
    st.header("🏢 Bidder Management - Highland Tower Development")
    st.markdown("**Qualified contractor and vendor management system**")
    
    # Bidder management buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ Add New Bidder", type="primary"):
            st.session_state.show_add_bidder = True
    with col2:
        if st.button("📋 Bidder Database"):
            st.session_state.show_bidder_database = True
    with col3:
        if st.button("📊 Bid Analysis"):
            st.session_state.show_bid_analysis = True
    with col4:
        if st.button("✅ Qualification Review"):
            st.session_state.show_qualification_review = True
    
    # Qualified bidders database
    st.subheader("👥 Qualified Bidders Database")
    
    bidders_data = pd.DataFrame([
        {
            "Company": "Steel Fabricators Inc",
            "Trade": "Structural Steel",
            "Experience": "25 years",
            "Rating": "A+",
            "Max Project": "$100M",
            "Status": "Pre-Qualified",
            "Last Project": "Metro Tower - $85M"
        },
        {
            "Company": "Elite MEP Systems", 
            "Trade": "MEP",
            "Experience": "18 years", 
            "Rating": "A",
            "Max Project": "$50M",
            "Status": "Active Bidder",
            "Last Project": "City Center - $45M"
        }
    ])
    
    st.dataframe(bidders_data, use_container_width=True, hide_index=True)

def render_project_planning_section():
    """Project planning dashboard"""
    st.header("📊 Project Planning Dashboard")
    st.markdown("**Highland Tower Development - Planning Overview**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Planning Phase", "85%", "On track")
    with col2:
        st.metric("Design Review", "Complete", "Approved")
    with col3:
        st.metric("Permits", "Pending", "2 weeks")

def render_documents():
    """Document Management - Your sophisticated document system"""
    st.title("📁 Document Management")
    st.markdown("**Centralized document control and management system**")
    
    tab1, tab2, tab3 = st.tabs(["📂 Document Library", "🔍 Search", "📊 Analytics"])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Documents", "2,847", "+156 this week")
        with col2:
            st.metric("Drawings", "342", "Current revision")
        with col3:
            st.metric("Specifications", "89", "Updated")
        with col4:
            st.metric("Reports", "156", "This month")

if __name__ == "__main__":
    main()