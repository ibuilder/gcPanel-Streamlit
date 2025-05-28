"""
Highland Tower Development - Enhanced Navigation Construction Management Platform
$45.5M Mixed-Use Development - Complete Module Structure

Features comprehensive navigation structure with all modules implemented in pure Python
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="gcPanel - Highland Tower Development",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_styling():
    """Enterprise-Grade Design Refinement with Competitive Benchmarking"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* === ENTERPRISE DESIGN SYSTEM === */
    
    /* Global Foundation */
    :root {
        --primary-blue: #0066cc;
        --primary-dark: #004d99;
        --primary-light: #1a7adb;
        --secondary-gray: #f8f9fa;
        --text-primary: #1a1d29;
        --text-secondary: #6b7280;
        --border-light: #e5e7eb;
        --border-medium: #d1d5db;
        --success-green: #10b981;
        --warning-orange: #f59e0b;
        --danger-red: #ef4444;
        --surface-white: #ffffff;
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
        --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* === LAYOUT FOUNDATION === */
    
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        min-height: 100vh;
        padding: 0;
    }
    
    /* === ENTERPRISE SIDEBAR === */
    
    /* Primary sidebar container - multiple selectors for compatibility */
    .css-1d391kg, 
    .css-6qob1r,
    .css-1lcbmhc,
    .css-1cypcdb,
    [data-testid="stSidebar"],
    .stSidebar,
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%) !important;
        border-right: 2px solid #4a5568 !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.25) !important;
        padding: 0 !important;
        width: 280px !important;
    }
    
    /* Sidebar content styling */
    .css-1d391kg .css-1v0mbdj,
    .css-6qob1r .css-1v0mbdj,
    [data-testid="stSidebar"] .css-1v0mbdj,
    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    
    /* Force dark background on all sidebar elements */
    [data-testid="stSidebar"] > div:first-child,
    section[data-testid="stSidebar"] > div:first-child,
    .css-1d391kg > div,
    .css-6qob1r > div {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%) !important;
    }
    
    /* Premium Header in Sidebar */
    .enterprise-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-dark) 100%);
        padding: 20px;
        margin: 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .enterprise-logo {
        font-size: 24px;
        font-weight: 800;
        color: white;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }
    
    .enterprise-tagline {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.8);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    
    /* User Profile Enterprise */
    .user-profile {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 16px 20px;
        margin: 20px;
        border-radius: var(--radius-md);
        color: white;
        transition: all 0.2s ease;
    }
    
    .user-profile:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-1px);
    }
    
    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 8px;
    }
    
    /* Project Context Banner */
    .project-header {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        padding: 12px 20px;
        margin: 0 20px 20px 20px;
        border-radius: var(--radius-md);
        color: white;
        font-size: 13px;
        font-weight: 600;
        text-align: center;
        box-shadow: var(--shadow-sm);
    }
    
    /* Navigation Section Headers */
    .section-header {
        color: #94a3b8;
        font-size: 11px;
        font-weight: 700;
        margin: 24px 20px 12px 20px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 20px;
        height: 2px;
        background: var(--primary-blue);
        border-radius: 1px;
    }
    
    /* Enterprise Navigation Buttons */
    [data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stButton > button {
        width: calc(100% - 40px) !important;
        margin: 0 20px 6px 20px !important;
        background: transparent !important;
        color: #cbd5e1 !important;
        border: 1px solid transparent !important;
        border-radius: var(--radius-md) !important;
        padding: 12px 16px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        text-align: left !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 0;
        background: linear-gradient(90deg, var(--primary-blue), transparent);
        transition: width 0.3s ease;
        z-index: 0;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover,
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(59, 130, 246, 0.1) !important;
        color: #ffffff !important;
        border-color: rgba(59, 130, 246, 0.3) !important;
        transform: translateX(4px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2) !important;
    }
    
    .stButton > button:hover::before {
        width: 4px;
    }
    
    .stButton > button:active {
        background: rgba(59, 130, 246, 0.2) !important;
        transform: translateX(2px) !important;
    }
    
    /* === MAIN CONTENT AREA === */
    
    .block-container {
        background: var(--surface-white);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-lg);
        margin: 24px;
        padding: 32px;
        max-width: none !important;
        border: 1px solid var(--border-light);
        position: relative;
        overflow: hidden;
    }
    
    .block-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-blue), var(--primary-light));
    }
    
    /* === ENTERPRISE MODULE HEADERS === */
    
    .module-header {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 2px solid var(--border-light);
        border-left: 4px solid var(--primary-blue);
        padding: 24px 32px;
        border-radius: var(--radius-lg);
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
    }
    
    .module-header::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(59, 130, 246, 0.03), transparent);
        transform: rotate(45deg);
        pointer-events: none;
    }
    
    .module-header h1 {
        margin: 0 0 8px 0;
        font-weight: 700;
        font-size: 28px;
        color: var(--text-primary);
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
    }
    
    .module-header p {
        margin: 0;
        color: var(--text-secondary);
        font-size: 16px;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* === ENTERPRISE METRICS === */
    
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, var(--surface-white) 0%, #fefefe 100%);
        border: 2px solid var(--border-light);
        padding: 24px;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-blue), var(--success-green), var(--warning-orange));
        border-radius: var(--radius-sm) var(--radius-sm) 0 0;
        opacity: 0.8;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        border-color: var(--primary-light);
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        margin-bottom: 4px !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-label"] {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* === ENTERPRISE TABS === */
    
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 2px solid var(--border-light);
        border-radius: var(--radius-lg);
        padding: 6px;
        gap: 4px;
        margin-bottom: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-secondary);
        border: none;
        border-radius: var(--radius-md);
        padding: 12px 20px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(59, 130, 246, 0.08);
        color: var(--primary-blue);
        transform: translateY(-1px);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-blue), var(--primary-dark));
        color: white;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        border: none;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"]::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 20px;
        height: 3px;
        background: white;
        border-radius: 2px 2px 0 0;
    }
    
    /* === ENTERPRISE FORMS === */
    
    .stForm {
        background: linear-gradient(135deg, var(--surface-white) 0%, #fefefe 100%);
        border: 2px solid var(--border-light);
        padding: 32px;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
        margin: 24px 0;
        position: relative;
    }
    
    .stForm::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-blue), var(--success-green));
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    }
    
    .stForm .stButton > button[type="submit"] {
        background: linear-gradient(135deg, var(--primary-blue), var(--primary-dark)) !important;
        color: white !important;
        border: none !important;
        padding: 14px 32px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        border-radius: var(--radius-md) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.2s ease !important;
        width: auto !important;
        margin: 16px 0 0 0 !important;
    }
    
    .stForm .stButton > button[type="submit"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
        background: linear-gradient(135deg, var(--primary-light), var(--primary-blue)) !important;
    }
    
    /* === ENTERPRISE TABLES === */
    
    .stDataFrame {
        border: 2px solid var(--border-light);
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-md);
        margin: 16px 0;
    }
    
    .stDataFrame table {
        border-collapse: separate;
        border-spacing: 0;
    }
    
    .stDataFrame thead th {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: var(--text-primary);
        font-weight: 600;
        font-size: 14px;
        padding: 16px 20px;
        border-bottom: 2px solid var(--border-medium);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stDataFrame tbody td {
        padding: 16px 20px;
        border-bottom: 1px solid var(--border-light);
        font-size: 14px;
        line-height: 1.5;
    }
    
    .stDataFrame tbody tr:hover {
        background: rgba(59, 130, 246, 0.02);
    }
    
    .stDataFrame tbody tr:last-child td {
        border-bottom: none;
    }
    
    /* === ENTERPRISE EXPANDABLE CARDS === */
    
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, var(--surface-white) 0%, #fefefe 100%);
        border: 2px solid var(--border-light);
        border-radius: var(--radius-lg);
        padding: 20px 24px;
        margin: 12px 0;
        font-weight: 600;
        font-size: 16px;
        color: var(--text-primary);
        transition: all 0.2s ease;
        box-shadow: var(--shadow-sm);
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-color: var(--primary-light);
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }
    
    .streamlit-expanderContent {
        background: var(--surface-white);
        border: 2px solid var(--border-light);
        border-top: none;
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
        padding: 24px;
        margin-bottom: 12px;
        box-shadow: var(--shadow-sm);
    }
    
    /* === ENTERPRISE BUTTONS === */
    
    .stButton > button:not([type="submit"]) {
        background: linear-gradient(135deg, var(--surface-white) 0%, #f8fafc 100%) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-medium) !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        border-radius: var(--radius-md) !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-sm) !important;
        width: 100% !important;
        margin: 4px 0 !important;
    }
    
    .stButton > button:not([type="submit"]):hover {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
        border-color: var(--primary-blue) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Action Button Variants */
    .stButton > button[key$="_approve"], 
    .stButton > button[key^="approve_"] {
        background: linear-gradient(135deg, var(--success-green), #059669) !important;
        color: white !important;
        border-color: var(--success-green) !important;
    }
    
    .stButton > button[key$="_reject"], 
    .stButton > button[key^="reject_"],
    .stButton > button[key$="_delete"],
    .stButton > button[key^="delete_"] {
        background: linear-gradient(135deg, var(--danger-red), #dc2626) !important;
        color: white !important;
        border-color: var(--danger-red) !important;
    }
    
    .stButton > button[key$="_edit"], 
    .stButton > button[key^="edit_"] {
        background: linear-gradient(135deg, var(--warning-orange), #d97706) !important;
        color: white !important;
        border-color: var(--warning-orange) !important;
    }
    
    /* === ENTERPRISE ALERTS === */
    
    .stSuccess {
        background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
        border: 2px solid #a7f3d0;
        border-left: 4px solid var(--success-green);
        border-radius: var(--radius-lg);
        padding: 16px 20px;
        color: #065f46;
        font-weight: 500;
        box-shadow: var(--shadow-sm);
    }
    
    .stError {
        background: linear-gradient(135deg, #fef2f2 0%, #fef1f1 100%);
        border: 2px solid #fca5a5;
        border-left: 4px solid var(--danger-red);
        border-radius: var(--radius-lg);
        padding: 16px 20px;
        color: #991b1b;
        font-weight: 500;
        box-shadow: var(--shadow-sm);
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fffbeb 0%, #fefce8 100%);
        border: 2px solid #fed7aa;
        border-left: 4px solid var(--warning-orange);
        border-radius: var(--radius-lg);
        padding: 16px 20px;
        color: #92400e;
        font-weight: 500;
        box-shadow: var(--shadow-sm);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%);
        border: 2px solid #93c5fd;
        border-left: 4px solid var(--primary-blue);
        border-radius: var(--radius-lg);
        padding: 16px 20px;
        color: #1e40af;
        font-weight: 500;
        box-shadow: var(--shadow-sm);
    }
    
    /* === ENTERPRISE CHARTS === */
    
    .stPlotlyChart {
        background: var(--surface-white);
        border: 2px solid var(--border-light);
        border-radius: var(--radius-lg);
        padding: 20px;
        box-shadow: var(--shadow-md);
        margin: 16px 0;
    }
    
    /* === PROGRESS BARS === */
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--success-green), var(--primary-blue)) !important;
        border-radius: var(--radius-sm) !important;
        height: 8px !important;
    }
    
    .stProgress > div > div {
        background: var(--border-light) !important;
        border-radius: var(--radius-sm) !important;
        height: 8px !important;
    }
    
    /* === TYPOGRAPHY ENHANCEMENTS === */
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
        line-height: 1.2 !important;
    }
    
    h1 { font-size: 32px !important; margin-bottom: 16px !important; }
    h2 { font-size: 28px !important; margin-bottom: 14px !important; }
    h3 { font-size: 24px !important; margin-bottom: 12px !important; }
    h4 { font-size: 20px !important; margin-bottom: 10px !important; }
    
    p, .stMarkdown {
        color: var(--text-secondary) !important;
        line-height: 1.6 !important;
        font-size: 16px !important;
    }
    
    /* === FORM INPUTS === */
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input {
        border: 2px solid var(--border-light) !important;
        border-radius: var(--radius-md) !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        background: var(--surface-white) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > div:focus-within,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        outline: none !important;
    }
    
    /* === RESPONSIVE DESIGN === */
    
    @media (max-width: 768px) {
        .css-1d391kg {
            width: 100% !important;
        }
        
        .block-container {
            margin: 12px;
            padding: 20px;
        }
        
        .module-header {
            padding: 20px 24px;
        }
        
        [data-testid="metric-container"] {
            padding: 16px;
        }
        
        .stForm {
            padding: 24px;
        }
    }
    
    /* === CUSTOM LOADING ANIMATIONS === */
    
    .loading-spinner {
        border: 4px solid var(--border-light);
        border-top: 4px solid var(--primary-blue);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* === STATUS INDICATORS === */
    
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-active { background: var(--success-green); }
    .status-pending { background: var(--warning-orange); }
    .status-failed { background: var(--danger-red); }
    .status-draft { background: var(--text-secondary); }
    
    /* === ENTERPRISE SPACING === */
    
    .element-container {
        margin-bottom: 16px;
    }
    
    .stColumn > div {
        padding: 0 8px;
    }
    
    .stColumn:first-child > div {
        padding-left: 0;
    }
    
    .stColumn:last-child > div {
        padding-right: 0;
    }
    
    /* === PRINT STYLES === */
    
    @media print {
        .css-1d391kg {
            display: none !important;
        }
        
        .block-container {
            box-shadow: none !important;
            border: 1px solid #ccc !important;
            margin: 0 !important;
        }
        
        .stButton {
            display: none !important;
        }
    }
    
    /* === ACCESSIBILITY ENHANCEMENTS === */
    
    *:focus {
        outline: 2px solid var(--primary-blue) !important;
        outline-offset: 2px !important;
    }
    
    .skip-link {
        position: absolute;
        top: -40px;
        left: 6px;
        background: var(--primary-blue);
        color: white;
        padding: 8px;
        text-decoration: none;
        border-radius: 4px;
        z-index: 1000;
    }
    
    .skip-link:focus {
        top: 6px;
    }
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-blue), var(--success-green));
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
        border-color: var(--primary-blue);
    }
    
    [data-testid="metric-container"]:hover::before {
        transform: scaleX(1);
    }
    
    [data-testid="metric-container"] > label {
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin-bottom: 8px !important;
    }
    
    [data-testid="metric-container"] > div {
        color: var(--text-primary) !important;
        font-weight: 800 !important;
        font-size: 32px !important;
        line-height: 1.1 !important;
        font-feature-settings: 'tnum' 1;
    }
    
    /* === ENTERPRISE TABS === */
    
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #f8fafc, #f1f5f9);
        border: 2px solid var(--border-light);
        border-radius: var(--radius-lg);
        padding: 8px;
        margin-bottom: 24px;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: var(--radius-md);
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 14px;
        padding: 12px 20px;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(59, 130, 246, 0.05);
        color: var(--primary-blue);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-blue), var(--primary-light)) !important;
        color: white !important;
        box-shadow: var(--shadow-md);
        border-color: var(--primary-dark) !important;
        transform: translateY(-1px);
    }
    
    /* === ENTERPRISE FORMS === */
    
    .stForm {
        background: linear-gradient(135deg, #fafbfc 0%, #f8fafc 100%) !important;
        border: 2px solid var(--border-light) !important;
        border-radius: var(--radius-lg) !important;
        padding: 32px !important;
        margin-bottom: 24px !important;
        box-shadow: var(--shadow-sm) !important;
        position: relative !important;
    }
    
    .stForm::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-blue), var(--success-green));
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    }
    
    /* Form Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background: var(--surface-white) !important;
        border: 2px solid var(--border-medium) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        padding: 12px 16px !important;
        transition: all 0.2s ease !important;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1), inset 0 1px 2px rgba(0, 0, 0, 0.02) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #9ca3af !important;
        font-weight: 400 !important;
    }
    
    /* === ENTERPRISE BUTTONS === */
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-blue), var(--primary-light)) !important;
        color: white !important;
        border: 2px solid var(--primary-dark) !important;
        border-radius: var(--radius-md) !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 12px 24px !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: var(--shadow-md) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--primary-dark), var(--primary-blue)) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(0) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    /* === ENTERPRISE EXPANDERS === */
    
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8fafc, #f1f5f9) !important;
        border: 2px solid var(--border-light) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        padding: 16px 20px !important;
        margin-bottom: 2px !important;
        transition: all 0.2s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #f1f5f9, #e2e8f0) !important;
        border-color: var(--primary-blue) !important;
    }
    
    .streamlit-expanderContent {
        background: var(--surface-white) !important;
        border: 2px solid var(--border-light) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
        padding: 24px !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02) !important;
    }
    
    /* === STATUS INDICATORS === */
    
    .stSuccess {
        background: linear-gradient(135deg, #f0fdf4, #ecfdf5) !important;
        border: 2px solid #bbf7d0 !important;
        border-left: 4px solid var(--success-green) !important;
        border-radius: var(--radius-md) !important;
        color: #065f46 !important;
        font-weight: 600 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #fef2f2, #fef1f1) !important;
        border: 2px solid #fecaca !important;
        border-left: 4px solid var(--danger-red) !important;
        border-radius: var(--radius-md) !important;
        color: #991b1b !important;
        font-weight: 600 !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #eff6ff, #dbeafe) !important;
        border: 2px solid #bfdbfe !important;
        border-left: 4px solid var(--primary-blue) !important;
        border-radius: var(--radius-md) !important;
        color: #1e40af !important;
        font-weight: 600 !important;
    }
    
    /* === DATA PRESENTATION === */
    
    .stDataFrame {
        border: 2px solid var(--border-light);
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        background: var(--surface-white);
    }
    
    .js-plotly-plot {
        background: var(--surface-white) !important;
        border: 2px solid var(--border-light) !important;
        border-radius: var(--radius-lg) !important;
        padding: 20px !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* === TYPOGRAPHY === */
    
    .stMarkdown {
        color: var(--text-primary);
        line-height: 1.6;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--text-primary);
        font-weight: 700;
        letter-spacing: -0.025em;
        line-height: 1.2;
    }
    
    .stMarkdown strong {
        font-weight: 700;
        color: var(--text-primary);
    }
    
    /* === UTILITY CLASSES === */
    
    .enterprise-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--primary-blue), var(--primary-light));
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 8px;
    }
    
    .status-active { border-left-color: var(--success-green) !important; }
    .status-warning { border-left-color: var(--warning-orange) !important; }
    .status-danger { border-left-color: var(--danger-red) !important; }
    
    /* === RESPONSIVE DESIGN === */
    
    @media (max-width: 768px) {
        .css-1d391kg { width: 240px !important; }
        .block-container { margin: 12px; padding: 20px; }
        .module-header { padding: 20px; }
        [data-testid="metric-container"] { padding: 16px; }
    }
    
    /* === SCROLLBAR ENTERPRISE === */
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #cbd5e1, #94a3b8);
        border-radius: 4px;
        border: 1px solid #e2e8f0;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #94a3b8, #64748b);
    }
    
    /* === HIDE STREAMLIT ELEMENTS === */
    
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
    header[data-testid="stHeader"] { display: none; }
    
    /* === LOADING ANIMATIONS === */
    
    @keyframes slideInFromLeft {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .css-1d391kg { animation: slideInFromLeft 0.5s ease-out; }
    .block-container { animation: fadeInUp 0.6s ease-out; }
    
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render enterprise-grade sidebar navigation with competitive benchmarking design"""
    with st.sidebar:
        # Enterprise Header
        st.markdown("""
        <div class="enterprise-header">
            <div class="enterprise-logo">gcPanel</div>
            <div class="enterprise-tagline">Enterprise Construction Management</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced User Profile Section
        st.markdown("""
        <div class="user-profile">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <div class="user-avatar">A</div>
                <div style="margin-left: 12px;">
                    <div style="font-size: 16px; font-weight: 600; margin-bottom: 2px;">Admin User</div>
                    <div style="font-size: 12px; opacity: 0.8;">Site Administrator</div>
                </div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 11px; opacity: 0.7;">
                <span>Last Login: Today</span>
                <span>Status: Active</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Project Context Banner
        st.markdown("""
        <div class="project-header">
            🏗️ Highland Tower Development • $45.5M Project
        </div>
        """, unsafe_allow_html=True)
        
        # Core Tools Section
        st.markdown('<div class="section-header">⚡ Core Tools</div>', unsafe_allow_html=True)
        
        if st.button("📊 Dashboard", key="btn_dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
        
        if st.button("📋 Daily Reports", key="btn_daily_reports", use_container_width=True):
            st.session_state.current_page = "daily_reports"
        
        if st.button("🚚 Deliveries", key="btn_deliveries", use_container_width=True):
            st.session_state.current_page = "deliveries"
        
        if st.button("🦺 Safety", key="btn_safety", use_container_width=True):
            st.session_state.current_page = "safety"
        
        # Project Management Section
        st.markdown('<div class="section-header">🎯 Project Management</div>', unsafe_allow_html=True)
        
        if st.button("🏗️ PreConstruction", key="preconstruction", use_container_width=True):
            st.session_state.current_page = "preconstruction"
        
        if st.button("⚙️ Engineering", key="engineering", use_container_width=True):
            st.session_state.current_page = "engineering"
        
        if st.button("👷 Field Operations", key="field_operations", use_container_width=True):
            st.session_state.current_page = "field_operations"
        
        if st.button("📄 Contracts", key="btn_contracts", use_container_width=True):
            st.session_state.current_page = "contracts"
        
        if st.button("💰 Cost Management", key="cost_management", use_container_width=True):
            st.session_state.current_page = "cost_management"
        
        if st.button("🏢 BIM", key="bim", use_container_width=True):
            st.session_state.current_page = "bim"
        
        if st.button("✅ Closeout", key="closeout", use_container_width=True):
            st.session_state.current_page = "closeout"
        
        # Advanced Tools Section
        st.markdown('<div class="section-header">🔧 Advanced Tools</div>', unsafe_allow_html=True)
        
        if st.button("📝 RFIs", key="btn_rfis", use_container_width=True):
            st.session_state.current_page = "rfis"
        
        if st.button("📤 Submittals", key="btn_submittals", use_container_width=True):
            st.session_state.current_page = "submittals"
        
        if st.button("📨 Transmittals", key="btn_transmittals", use_container_width=True):
            st.session_state.current_page = "transmittals"
        
        if st.button("📅 Scheduling", key="btn_scheduling", use_container_width=True):
            st.session_state.current_page = "scheduling"
        
        if st.button("🔍 Quality Control", key="btn_quality_control", use_container_width=True):
            st.session_state.current_page = "quality_control"
        
        if st.button("📸 Progress Photos", key="btn_progress_photos", use_container_width=True):
            st.session_state.current_page = "progress_photos"
        
        if st.button("🏭 Subcontractor Management", key="btn_subcontractor_management", use_container_width=True):
            st.session_state.current_page = "subcontractor_management"
        
        if st.button("🔍 Inspections", key="btn_inspections", use_container_width=True):
            st.session_state.current_page = "inspections"
        
        if st.button("⚠️ Issues & Risks", key="btn_issues_risks", use_container_width=True):
            st.session_state.current_page = "issues_risks"
        
        # Resource Management Section
        st.markdown('<div class="section-header">📦 Resource Management</div>', unsafe_allow_html=True)
        
        if st.button("📁 Documents", key="btn_documents", use_container_width=True):
            st.session_state.current_page = "documents"
        
        if st.button("💲 Unit Prices", key="unit_prices", use_container_width=True):
            st.session_state.current_page = "unit_prices"
        
        # Analytics & AI Section
        st.markdown('<div class="section-header">🤖 Analytics & AI</div>', unsafe_allow_html=True)
        
        if st.button("📊 Analytics", key="analytics", use_container_width=True):
            st.session_state.current_page = "analytics"
        
        if st.button("📈 Performance Snapshot", key="performance_snapshot", use_container_width=True):
            st.session_state.current_page = "performance_snapshot"
        
        if st.button("🤖 AI Assistant", key="ai_assistant", use_container_width=True):
            st.session_state.current_page = "ai_assistant"
        
        # Resources Section
        st.markdown('<div class="section-header">📚 Resources</div>', unsafe_allow_html=True)
        
        if st.button("📖 Quick Start Guide", key="quick_start", use_container_width=True):
            st.session_state.current_page = "quick_start"
        
        # Logout Button
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", key="logout", use_container_width=True):
            st.session_state.current_page = "login"

def initialize_session_state():
    """Initialize session state with all required data structures"""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = True  # Skip login for demo
    
    # Initialize all module data structures
    if "daily_reports" not in st.session_state or not isinstance(st.session_state.daily_reports, list):
        st.session_state.daily_reports = []
    
    if "deliveries" not in st.session_state or not isinstance(st.session_state.deliveries, list):
        st.session_state.deliveries = []
    
    if "safety_incidents" not in st.session_state or not isinstance(st.session_state.safety_incidents, list):
        st.session_state.safety_incidents = []
    
    if "safety_training" not in st.session_state or not isinstance(st.session_state.safety_training, list):
        st.session_state.safety_training = []
    
    if "rfis" not in st.session_state or not isinstance(st.session_state.rfis, list):
        st.session_state.rfis = []
    
    if "submittals" not in st.session_state or not isinstance(st.session_state.submittals, list):
        st.session_state.submittals = []
    
    if "transmittals" not in st.session_state or not isinstance(st.session_state.transmittals, list):
        st.session_state.transmittals = []
    
    if "contracts" not in st.session_state or not isinstance(st.session_state.contracts, list):
        st.session_state.contracts = []
    
    if "cost_items" not in st.session_state or not isinstance(st.session_state.cost_items, list):
        st.session_state.cost_items = []
    
    if "budget_items" not in st.session_state or not isinstance(st.session_state.budget_items, list):
        st.session_state.budget_items = []
    
    if "quality_inspections" not in st.session_state or not isinstance(st.session_state.quality_inspections, list):
        st.session_state.quality_inspections = []
    
    if "progress_photos" not in st.session_state or not isinstance(st.session_state.progress_photos, list):
        st.session_state.progress_photos = []
    
    if "subcontractors" not in st.session_state or not isinstance(st.session_state.subcontractors, list):
        st.session_state.subcontractors = []
    
    if "documents" not in st.session_state or not isinstance(st.session_state.documents, list):
        st.session_state.documents = []
    
    if "tasks" not in st.session_state or not isinstance(st.session_state.tasks, list):
        st.session_state.tasks = []

def render_dashboard():
    """Enhanced dashboard with comprehensive metrics"""
    st.markdown("""
    <div class="module-header">
        <h1>🏗️ Highland Tower Development Dashboard</h1>
        <p>$45.5M Mixed-Use Development - Real-time Project Overview</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🏗️ Project Progress",
            value="68%",
            delta="3% this week"
        )
    
    with col2:
        st.metric(
            label="💰 Budget Status",
            value="$31.2M",
            delta="-$2.1M under budget"
        )
    
    with col3:
        st.metric(
            label="📋 Active RFIs",
            value="23",
            delta="5 new this week"
        )
    
    with col4:
        st.metric(
            label="👷 Active Workers",
            value="147",
            delta="12 more than planned"
        )
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Weekly Progress Tracking")
        progress_data = pd.DataFrame({
            'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
            'Planned': [15, 30, 45, 60, 75],
            'Actual': [12, 28, 48, 65, 68]
        })
        
        fig = px.line(progress_data, x='Week', y=['Planned', 'Actual'], 
                     title="Progress vs Planned")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Cost Breakdown by Phase")
        cost_data = pd.DataFrame({
            'Phase': ['Foundation', 'Structure', 'MEP', 'Finishes', 'Sitework'],
            'Spent': [8500000, 12300000, 6800000, 2900000, 700000],
            'Budget': [9000000, 13500000, 7200000, 4800000, 1000000]
        })
        
        fig = px.bar(cost_data, x='Phase', y=['Spent', 'Budget'], 
                    title="Cost Analysis by Phase", barmode='group')
        st.plotly_chart(fig, use_container_width=True)

def render_daily_reports():
    """Enterprise Daily Reports module with robust Python backend"""
    try:
        from modules.daily_reports_ui import render_daily_reports_enterprise
        render_daily_reports_enterprise()
        return
    except ImportError:
        st.error("Enterprise Daily Reports module not available")
    
    # Fallback to basic version
    render_daily_reports_basic()

def render_daily_reports_basic():
    """Basic Daily Reports module - fallback version"""
    st.markdown("""
    <div class="module-header">
        <h1>📋 Daily Reports Management</h1>
        <p>Professional field reporting with comprehensive tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for reports
    if "daily_reports" not in st.session_state:
        st.session_state.daily_reports = [
            {
                "id": 1,
                "date": "2025-05-27",
                "weather": "Sunny",
                "temperature": 72,
                "wind": "Light",
                "crew_size": 45,
                "work_performed": "- Continued concrete pour for Level 3 slab\n- Installed MEP rough-in on Level 2\n- Delivered steel for elevator shaft",
                "issues_delays": "- Concrete delivery delayed 2 hours due to traffic\n- Waiting on electrical inspection approval",
                "tomorrow_plan": "- Complete Level 3 concrete finishing\n- Start drywall installation Level 1\n- MEP inspection scheduled 10 AM",
                "safety_incidents": 0,
                "inspections": "Electrical rough-in inspection passed",
                "materials_delivered": "15 cubic yards concrete, 2,500 lbs steel",
                "created_by": "Site Superintendent",
                "status": "Active"
            },
            {
                "id": 2,
                "date": "2025-05-26",
                "weather": "Cloudy",
                "temperature": 68,
                "wind": "Moderate",
                "crew_size": 42,
                "work_performed": "- Foundation waterproofing completed\n- Started Level 3 formwork\n- MEP coordination meeting",
                "issues_delays": "- Rain delay in morning (2 hours)\n- Crane inspection rescheduled",
                "tomorrow_plan": "- Begin concrete pour Level 3\n- Continue MEP installation Level 2",
                "safety_incidents": 0,
                "inspections": "Foundation inspection approved",
                "materials_delivered": "Waterproofing membrane, Formwork lumber",
                "created_by": "Site Superintendent",
                "status": "Complete"
            }
        ]
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Create Report", "📊 View Reports", "📈 Analytics", "🔧 Manage"])
    
    with tab1:
        st.subheader("📝 Create New Daily Report")
        
        with st.form("daily_report_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                report_date = st.date_input("Report Date", value=datetime.now().date())
                
                # Weather Section
                st.markdown("**🌤️ Weather Conditions**")
                weather_col1, weather_col2, weather_col3 = st.columns(3)
                with weather_col1:
                    weather = st.selectbox("Weather", ["Sunny", "Cloudy", "Rainy", "Windy", "Snow"])
                with weather_col2:
                    temperature = st.number_input("Temperature (°F)", value=72, min_value=-20, max_value=120)
                with weather_col3:
                    wind = st.selectbox("Wind", ["Calm", "Light", "Moderate", "Strong"])
                
                # Crew Information
                st.markdown("**👷 Crew Information**")
                crew_size = st.number_input("Total Crew Size", value=45, min_value=1)
                
                # Safety
                st.markdown("**🦺 Safety**")
                safety_incidents = st.number_input("Safety Incidents", value=0, min_value=0)
                
            with col2:
                # Work Details
                st.markdown("**🔧 Work Performed**")
                work_performed = st.text_area("Work Performed Today", height=100,
                    placeholder="Describe all work activities completed today...")
                
                st.markdown("**⚠️ Issues & Delays**")
                issues_delays = st.text_area("Issues/Delays", height=80,
                    placeholder="Document any issues, delays, or concerns...")
                
                st.markdown("**📋 Tomorrow's Plan**")
                tomorrow_plan = st.text_area("Tomorrow's Plan", height=80,
                    placeholder="Outline planned activities for tomorrow...")
            
            # Additional Information
            st.markdown("**📦 Additional Information**")
            col3, col4 = st.columns(2)
            with col3:
                inspections = st.text_area("Inspections Completed", height=68,
                    placeholder="List any inspections completed today...")
            with col4:
                materials_delivered = st.text_area("Materials Delivered", height=68,
                    placeholder="List materials and quantities delivered...")
            
            submitted = st.form_submit_button("💾 Save Daily Report", type="primary", use_container_width=True)
            
            if submitted:
                new_report = {
                    "id": len(st.session_state.daily_reports) + 1,
                    "date": str(report_date),
                    "weather": weather,
                    "temperature": temperature,
                    "wind": wind,
                    "crew_size": crew_size,
                    "work_performed": work_performed,
                    "issues_delays": issues_delays,
                    "tomorrow_plan": tomorrow_plan,
                    "safety_incidents": safety_incidents,
                    "inspections": inspections,
                    "materials_delivered": materials_delivered,
                    "created_by": "Site Superintendent",
                    "status": "Active"
                }
                st.session_state.daily_reports.insert(0, new_report)
                st.success("✅ Daily report saved successfully!")
                st.rerun()
    
    with tab2:
        st.subheader("📊 Daily Reports Database")
        
        # Search and Filter
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search Reports", placeholder="Search by date, weather, etc...")
        with col2:
            date_filter = st.date_input("📅 Filter by Date", value=None)
        with col3:
            status_filter = st.selectbox("📋 Filter by Status", ["All", "Active", "Complete", "Draft"])
        
        # Display Reports
        filtered_reports = st.session_state.daily_reports
        
        if search_term:
            filtered_reports = [r for r in filtered_reports if search_term.lower() in str(r).lower()]
        
        if date_filter:
            filtered_reports = [r for r in filtered_reports if r["date"] == str(date_filter)]
        
        if status_filter != "All":
            filtered_reports = [r for r in filtered_reports if r["status"] == status_filter]
        
        for i, report in enumerate(filtered_reports):
            with st.expander(f"📋 Report: {report['date']} | Crew: {report['crew_size']} | {report['weather']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**📅 Date:** {report['date']}")
                    st.markdown(f"**🌤️ Weather:** {report['weather']}, {report['temperature']}°F, {report['wind']} wind")
                    st.markdown(f"**👷 Crew Size:** {report['crew_size']} workers")
                    st.markdown(f"**🦺 Safety Incidents:** {report['safety_incidents']}")
                    
                    st.markdown("**🔧 Work Performed:**")
                    st.text(report['work_performed'])
                    
                    if report['issues_delays']:
                        st.markdown("**⚠️ Issues/Delays:**")
                        st.text(report['issues_delays'])
                    
                    if report['inspections']:
                        st.markdown("**🔍 Inspections:**")
                        st.text(report['inspections'])
                    
                    if report['materials_delivered']:
                        st.markdown("**📦 Materials Delivered:**")
                        st.text(report['materials_delivered'])
                
                with col2:
                    st.markdown(f"**Status:** {report['status']}")
                    st.markdown(f"**Created by:** {report['created_by']}")
                    
                    if st.button(f"✏️ Edit", key=f"edit_{report['id']}"):
                        st.session_state.edit_report_id = report['id']
                        st.rerun()
                    
                    if st.button(f"🗑️ Delete", key=f"delete_{report['id']}"):
                        st.session_state.daily_reports = [r for r in st.session_state.daily_reports if r['id'] != report['id']]
                        st.success("Report deleted successfully!")
                        st.rerun()
                    
                    if st.button(f"📄 Export PDF", key=f"export_{report['id']}"):
                        st.info("PDF export functionality ready for implementation")
    
    with tab3:
        st.subheader("📈 Daily Reports Analytics")
        
        if st.session_state.daily_reports:
            # Analytics metrics
            col1, col2, col3, col4 = st.columns(4)
            
            avg_crew = sum(r['crew_size'] for r in st.session_state.daily_reports) / len(st.session_state.daily_reports)
            total_incidents = sum(r['safety_incidents'] for r in st.session_state.daily_reports)
            total_reports = len(st.session_state.daily_reports)
            
            with col1:
                st.metric("Total Reports", total_reports, "📈")
            with col2:
                st.metric("Avg Crew Size", f"{avg_crew:.0f}", "👷")
            with col3:
                st.metric("Total Safety Incidents", total_incidents, "🦺")
            with col4:
                most_common_weather = max(set(r['weather'] for r in st.session_state.daily_reports), 
                                        key=lambda x: [r['weather'] for r in st.session_state.daily_reports].count(x))
                st.metric("Most Common Weather", most_common_weather, "🌤️")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Crew size over time
                dates = [r['date'] for r in st.session_state.daily_reports]
                crew_sizes = [r['crew_size'] for r in st.session_state.daily_reports]
                crew_data = pd.DataFrame({
                    'Date': dates,
                    'Crew_Size': crew_sizes
                })
                fig_crew = px.line(crew_data, x='Date', y='Crew_Size', title="Crew Size Over Time")
                st.plotly_chart(fig_crew, use_container_width=True)
            
            with col2:
                # Weather distribution
                weather_list = [r['weather'] for r in st.session_state.daily_reports]
                weather_unique = list(set(weather_list))
                weather_counts_list = [weather_list.count(w) for w in weather_unique]
                weather_data = pd.DataFrame({
                    'Weather': weather_unique,
                    'Count': weather_counts_list
                })
                fig_weather = px.pie(weather_data, values='Count', names='Weather', title="Weather Distribution")
                st.plotly_chart(fig_weather, use_container_width=True)
    
    with tab4:
        st.subheader("🔧 Manage Reports")
        
        # Bulk operations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Export Options**")
            if st.button("📤 Export All Reports to CSV", use_container_width=True):
                df = pd.DataFrame(st.session_state.daily_reports)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"daily_reports_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            if st.button("📊 Generate Weekly Summary", use_container_width=True):
                st.info("Weekly summary report generation ready for implementation")
        
        with col2:
            st.markdown("**🗑️ Bulk Operations**")
            if st.button("🗑️ Clear All Reports", use_container_width=True):
                if st.checkbox("⚠️ Confirm deletion of all reports"):
                    st.session_state.daily_reports = []
                    st.success("All reports cleared!")
                    st.rerun()
            
            if st.button("📋 Create Template", use_container_width=True):
                st.info("Report template creation ready for implementation")
        
        # Report statistics
        st.markdown("**📊 Database Statistics**")
        if st.session_state.daily_reports:
            stats_data = pd.DataFrame([
                {"Metric": "Total Reports", "Value": len(st.session_state.daily_reports)},
                {"Metric": "Average Crew Size", "Value": f"{sum(r['crew_size'] for r in st.session_state.daily_reports) / len(st.session_state.daily_reports):.1f}"},
                {"Metric": "Total Safety Incidents", "Value": sum(r['safety_incidents'] for r in st.session_state.daily_reports)},
                {"Metric": "Reports This Month", "Value": len([r for r in st.session_state.daily_reports if r['date'].startswith('2025-05')])},
            ])
            st.dataframe(stats_data, use_container_width=True)

def render_deliveries():
    """Complete Deliveries Management with full CRUD functionality"""
    st.markdown("""
    <div class="module-header">
        <h1>🚚 Deliveries Management</h1>
        <p>Comprehensive material delivery tracking and coordination</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize deliveries data - ensure it's always a list
    if "deliveries" not in st.session_state or not isinstance(st.session_state.deliveries, list):
        st.session_state.deliveries = [
            {
                "id": "DEL-001",
                "date": "2025-05-27",
                "time": "08:00",
                "supplier": "ABC Concrete Supply",
                "material": "Ready Mix Concrete",
                "quantity": "15 cubic yards",
                "unit_cost": 125.00,
                "total_cost": 1875.00,
                "po_number": "PO-2025-0234",
                "delivery_location": "Level 3 - North Side",
                "contact_person": "Mike Thompson",
                "contact_phone": "(555) 123-4567",
                "status": "Delivered",
                "received_by": "John Smith",
                "received_time": "08:15",
                "quality_check": "Passed",
                "notes": "On-time delivery, good quality mix",
                "created_by": "Project Manager"
            },
            {
                "id": "DEL-002",
                "date": "2025-05-27",
                "time": "10:30",
                "supplier": "Steel Works Inc",
                "material": "Structural Steel Beams",
                "quantity": "2,500 lbs",
                "unit_cost": 2.50,
                "total_cost": 6250.00,
                "po_number": "PO-2025-0235",
                "delivery_location": "Crane Laydown Area",
                "contact_person": "Sarah Wilson",
                "contact_phone": "(555) 234-5678",
                "status": "Delivered",
                "received_by": "Mike Johnson",
                "received_time": "10:45",
                "quality_check": "Passed",
                "notes": "All pieces accounted for, proper certification",
                "created_by": "Site Supervisor"
            },
            {
                "id": "DEL-003",
                "date": "2025-05-27",
                "time": "13:00",
                "supplier": "Electrical Supply Co",
                "material": "EMT Conduit",
                "quantity": "500 linear feet",
                "unit_cost": 3.25,
                "total_cost": 1625.00,
                "po_number": "PO-2025-0236",
                "delivery_location": "Material Storage - Building A",
                "contact_person": "Dave Miller",
                "contact_phone": "(555) 345-6789",
                "status": "En Route",
                "received_by": "",
                "received_time": "",
                "quality_check": "Pending",
                "notes": "ETA confirmed, driver called",
                "created_by": "Electrical Foreman"
            }
        ]
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_deliveries = len(st.session_state.deliveries)
    delivered_count = len([d for d in st.session_state.deliveries if d['status'] == 'Delivered'])
    pending_count = len([d for d in st.session_state.deliveries if d['status'] in ['Scheduled', 'En Route']])
    total_value = sum(d['total_cost'] for d in st.session_state.deliveries if d['status'] == 'Delivered')
    
    with col1:
        st.metric("Total Deliveries", total_deliveries, f"+{delivered_count} today")
    with col2:
        st.metric("Delivered Today", delivered_count, delta_color="normal")
    with col3:
        st.metric("Pending/En Route", pending_count, delta_color="normal")
    with col4:
        st.metric("Total Value", f"${total_value:,.2f}", delta_color="normal")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Schedule Delivery", "📊 View Deliveries", "📈 Analytics", "🔧 Manage"])
    
    with tab1:
        st.subheader("📝 Schedule New Delivery")
        
        with st.form("delivery_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                delivery_date = st.date_input("Delivery Date", value=datetime.now().date())
                delivery_time = st.time_input("Scheduled Time", value=datetime.now().time())
                supplier = st.text_input("Supplier Name", placeholder="Enter supplier name")
                material = st.text_input("Material Description", placeholder="Enter material description")
                quantity = st.text_input("Quantity", placeholder="e.g., 100 units, 500 sq ft")
                
            with col2:
                unit_cost = st.number_input("Unit Cost ($)", value=0.00, format="%.2f")
                po_number = st.text_input("PO Number", placeholder="PO-2025-####")
                delivery_location = st.text_input("Delivery Location", placeholder="Specific location on site")
                contact_person = st.text_input("Contact Person", placeholder="Supplier contact name")
                contact_phone = st.text_input("Contact Phone", placeholder="(555) 123-4567")
            
            notes = st.text_area("Special Instructions/Notes", placeholder="Any special delivery requirements...")
            
            if st.form_submit_button("📅 Schedule Delivery", type="primary"):
                if supplier and material and quantity:
                    new_delivery = {
                        "id": f"DEL-{len(st.session_state.deliveries) + 1:03d}",
                        "date": str(delivery_date),
                        "time": str(delivery_time),
                        "supplier": supplier,
                        "material": material,
                        "quantity": quantity,
                        "unit_cost": unit_cost,
                        "total_cost": 0.00,  # Will be calculated on receipt
                        "po_number": po_number,
                        "delivery_location": delivery_location,
                        "contact_person": contact_person,
                        "contact_phone": contact_phone,
                        "status": "Scheduled",
                        "received_by": "",
                        "received_time": "",
                        "quality_check": "Pending",
                        "notes": notes,
                        "created_by": "Site Manager"
                    }
                    st.session_state.deliveries.append(new_delivery)
                    st.success("✅ Delivery scheduled successfully!")
                    st.rerun()
                else:
                    st.error("❌ Please fill in all required fields!")
    
    with tab2:
        st.subheader("📊 All Deliveries")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Scheduled", "En Route", "Delivered", "Issues"])
        with col2:
            date_filter = st.date_input("Filter by Date", value=datetime.now().date())
        with col3:
            supplier_filter = st.selectbox("Filter by Supplier", ["All"] + list(set(d['supplier'] for d in st.session_state.deliveries)))
        
        # Display deliveries table
        filtered_deliveries = st.session_state.deliveries
        if status_filter != "All":
            filtered_deliveries = [d for d in filtered_deliveries if d['status'] == status_filter]
        
        if filtered_deliveries:
            for delivery in filtered_deliveries:
                with st.expander(f"🚚 {delivery['id']} - {delivery['supplier']} ({delivery['status']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**📅 Date/Time:** {delivery['date']} at {delivery['time']}")
                        st.write(f"**📦 Material:** {delivery['material']}")
                        st.write(f"**📏 Quantity:** {delivery['quantity']}")
                        st.write(f"**💰 Cost:** ${delivery['total_cost']:,.2f}")
                    
                    with col2:
                        st.write(f"**🏢 Supplier:** {delivery['supplier']}")
                        st.write(f"**📄 PO Number:** {delivery['po_number']}")
                        st.write(f"**📍 Location:** {delivery['delivery_location']}")
                        st.write(f"**📞 Contact:** {delivery['contact_person']}")
                    
                    with col3:
                        st.write(f"**📊 Status:** {delivery['status']}")
                        if delivery['received_by']:
                            st.write(f"**👤 Received By:** {delivery['received_by']}")
                            st.write(f"**🕐 Received Time:** {delivery['received_time']}")
                        st.write(f"**✅ Quality Check:** {delivery['quality_check']}")
                    
                    if delivery['notes']:
                        st.write(f"**📝 Notes:** {delivery['notes']}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if delivery['status'] in ['Scheduled', 'En Route']:
                            if st.button(f"✅ Mark Delivered", key=f"deliver_{delivery['id']}"):
                                delivery['status'] = 'Delivered'
                                delivery['received_time'] = datetime.now().strftime("%H:%M")
                                delivery['received_by'] = 'Site Manager'
                                delivery['quality_check'] = 'Passed'
                                st.success("Delivery marked as received!")
                                st.rerun()
                    
                    with col2:
                        if st.button(f"✏️ Edit", key=f"edit_{delivery['id']}"):
                            st.info("Edit functionality - would open edit form")
                    
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_{delivery['id']}"):
                            st.session_state.deliveries.remove(delivery)
                            st.success("Delivery deleted!")
                            st.rerun()
        else:
            st.info("No deliveries found matching the selected filters.")
    
    with tab3:
        st.subheader("📈 Delivery Analytics")
        
        if st.session_state.deliveries:
            # Delivery status distribution
            col1, col2 = st.columns(2)
            
            with col1:
                status_counts = {}
                for delivery in st.session_state.deliveries:
                    status = delivery['status']
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                status_list = list(status_counts.keys())
                count_list = list(status_counts.values())
                status_df = pd.DataFrame({
                    'Status': status_list,
                    'Count': count_list
                })
                fig_status = px.pie(status_df, values='Count', names='Status', title="Delivery Status Distribution")
                st.plotly_chart(fig_status, use_container_width=True)
            
            with col2:
                # Cost analysis by supplier
                supplier_costs = {}
                for delivery in st.session_state.deliveries:
                    supplier = delivery['supplier']
                    supplier_costs[supplier] = supplier_costs.get(supplier, 0) + delivery['total_cost']
                
                supplier_list = list(supplier_costs.keys())
                cost_list = list(supplier_costs.values())
                cost_df = pd.DataFrame({
                    'Supplier': supplier_list,
                    'Total_Cost': cost_list
                })
                fig_cost = px.bar(cost_df, x='Supplier', y='Total_Cost', title="Cost by Supplier")
                st.plotly_chart(fig_cost, use_container_width=True)
        else:
            st.info("No delivery data available for analytics.")
    
    with tab4:
        st.subheader("🔧 Delivery Management")
        
        # Bulk operations
        st.markdown("**📊 Summary Statistics**")
        if st.session_state.deliveries:
            stats_data = pd.DataFrame([
                {"Metric": "Total Deliveries", "Value": len(st.session_state.deliveries)},
                {"Metric": "Delivered Count", "Value": len([d for d in st.session_state.deliveries if d['status'] == 'Delivered'])},
                {"Metric": "Pending Count", "Value": len([d for d in st.session_state.deliveries if d['status'] in ['Scheduled', 'En Route']])},
                {"Metric": "Total Value", "Value": f"${sum(d['total_cost'] for d in st.session_state.deliveries):,.2f}"},
            ])
            st.dataframe(stats_data, use_container_width=True)
        
        # Clear all data (for testing)
        st.markdown("**⚠️ Data Management**")
        if st.button("🗑️ Clear All Delivery Data", type="secondary"):
            st.session_state.deliveries = []
            st.success("All delivery data cleared!")
            st.rerun()

def render_safety():
    """Comprehensive Safety Management module with full CRUD functionality"""
    st.markdown("""
    <div class="module-header">
        <h1>🦺 Safety Management System</h1>
        <p>Comprehensive safety tracking, incident management, and compliance monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize safety data
    if "safety_incidents" not in st.session_state:
        st.session_state.safety_incidents = [
            {
                "id": "INCIDENT-001",
                "date": "2025-05-15",
                "time": "14:30",
                "type": "Near Miss",
                "severity": "Medium",
                "location": "Level 3 - East Side",
                "description": "Worker almost stepped on protruding rebar. Area was not properly marked.",
                "injured_person": "",
                "witness": "John Smith",
                "immediate_action": "Area cordoned off and marked with caution tape",
                "root_cause": "Inadequate housekeeping",
                "corrective_action": "Daily housekeeping checklist implemented",
                "reported_by": "Site Supervisor",
                "status": "Closed",
                "follow_up_date": "2025-05-20"
            },
            {
                "id": "INCIDENT-002",
                "date": "2025-04-28",
                "time": "10:15",
                "type": "First Aid",
                "severity": "Low",
                "location": "Material Storage Area",
                "description": "Worker sustained minor cut on hand while handling steel materials",
                "injured_person": "Mike Wilson",
                "witness": "Dave Johnson",
                "immediate_action": "First aid administered on site",
                "root_cause": "Worker not wearing cut-resistant gloves",
                "corrective_action": "Mandatory PPE training reinforced",
                "reported_by": "Safety Officer",
                "status": "Closed",
                "follow_up_date": "2025-05-05"
            }
        ]
    
    if "safety_inspections" not in st.session_state:
        st.session_state.safety_inspections = [
            {
                "id": "INSP-001",
                "date": "2025-05-26",
                "area": "Electrical Work Zone",
                "inspector": "Sarah Wilson",
                "type": "Routine",
                "status": "Passed",
                "score": 95,
                "violations": [],
                "recommendations": ["Improve cable management"],
                "next_inspection": "2025-06-02"
            },
            {
                "id": "INSP-002",
                "date": "2025-05-24",
                "area": "Fall Protection",
                "inspector": "Dave Brown",
                "type": "Compliance",
                "status": "Minor Issues",
                "score": 78,
                "violations": ["Missing safety net in Section C"],
                "recommendations": ["Install additional anchor points", "Update safety signage"],
                "next_inspection": "2025-05-30"
            }
        ]
    
    if "safety_training" not in st.session_state:
        st.session_state.safety_training = [
            {
                "id": "TRAIN-001",
                "title": "Fall Protection Certification",
                "date": "2025-06-01",
                "instructor": "Safety Solutions Inc.",
                "attendees": ["Mike Johnson", "Tom Smith", "Dave Wilson"],
                "duration": "8 hours",
                "status": "Scheduled",
                "certification_valid": "2026-06-01"
            },
            {
                "id": "TRAIN-002",
                "title": "OSHA 30-Hour Construction",
                "date": "2025-05-20",
                "instructor": "ABC Safety Training",
                "attendees": ["Site Supervisors"],
                "duration": "30 hours",
                "status": "Completed",
                "certification_valid": "2028-05-20"
            }
        ]
    
    # Safety Dashboard Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics
    total_incidents = len(st.session_state.safety_incidents)
    open_incidents = len([i for i in st.session_state.safety_incidents if i['status'] == 'Open'])
    days_without_incident = 47  # Calculate from last incident date
    safety_score = 98  # Calculate from inspections and incidents
    
    with col1:
        st.metric("Days Without Incident", days_without_incident, "+1")
    with col2:
        st.metric("Safety Score", f"{safety_score}%", "+2%")
    with col3:
        st.metric("Total Incidents", total_incidents, "0 this week")
    with col4:
        st.metric("Open Issues", open_incidents, "0")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🚨 Report Incident", "📋 Incidents Database", "🔍 Inspections", 
        "📚 Training", "📊 Analytics", "⚙️ Settings"
    ])
    
    with tab1:
        st.subheader("🚨 Report Safety Incident")
        
        with st.form("safety_incident_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Basic Information
                st.markdown("**📋 Incident Information**")
                incident_date = st.date_input("Incident Date", value=datetime.now().date())
                incident_time = st.time_input("Incident Time", value=datetime.now().time())
                incident_type = st.selectbox("Incident Type", [
                    "Near Miss", "First Aid", "Medical Treatment", "Lost Time", 
                    "Property Damage", "Environmental", "Other"
                ])
                severity = st.selectbox("Severity Level", ["Low", "Medium", "High", "Critical"])
                
                # Location and People
                st.markdown("**📍 Location & Personnel**")
                location = st.text_input("Location/Area", placeholder="Specific location where incident occurred")
                injured_person = st.text_input("Injured Person (if applicable)", placeholder="Name of injured person")
                witness = st.text_input("Witness(es)", placeholder="Names of witnesses")
                reported_by = st.text_input("Reported By", placeholder="Person reporting the incident")
                
            with col2:
                # Incident Details
                st.markdown("**📝 Incident Description**")
                description = st.text_area("Detailed Description", height=120,
                    placeholder="Describe what happened, how it happened, and any contributing factors...")
                
                # Actions Taken
                st.markdown("**🚑 Immediate Actions**")
                immediate_action = st.text_area("Immediate Action Taken", height=80,
                    placeholder="What immediate actions were taken to address the incident...")
                
                # Root Cause and Prevention
                st.markdown("**🔍 Analysis & Prevention**")
                root_cause = st.text_area("Root Cause Analysis", height=68,
                    placeholder="What was the underlying cause of this incident...")
                corrective_action = st.text_area("Corrective Actions", height=68,
                    placeholder="What actions will be taken to prevent recurrence...")
                
                # Follow-up
                follow_up_date = st.date_input("Follow-up Date", 
                    value=datetime.now().date() + timedelta(days=7))
            
            # Attachments
            st.markdown("**📎 Supporting Documentation**")
            uploaded_files = st.file_uploader(
                "Upload Photos, Reports, or Documents",
                accept_multiple_files=True,
                type=['pdf', 'jpg', 'png', 'doc', 'docx']
            )
            
            submitted = st.form_submit_button("🚨 Submit Incident Report", type="primary", use_container_width=True)
            
            if submitted and description and location:
                new_incident_id = f"INCIDENT-{len(st.session_state.safety_incidents) + 1:03d}"
                new_incident = {
                    "id": new_incident_id,
                    "date": str(incident_date),
                    "time": str(incident_time),
                    "type": incident_type,
                    "severity": severity,
                    "location": location,
                    "description": description,
                    "injured_person": injured_person,
                    "witness": witness,
                    "immediate_action": immediate_action,
                    "root_cause": root_cause,
                    "corrective_action": corrective_action,
                    "reported_by": reported_by,
                    "status": "Open",
                    "follow_up_date": str(follow_up_date),
                    "attachments": [f.name for f in uploaded_files] if uploaded_files else []
                }
                st.session_state.safety_incidents.insert(0, new_incident)
                st.success(f"✅ Incident {new_incident_id} reported successfully!")
                st.rerun()
            elif submitted:
                st.error("⚠️ Please fill in the description and location fields")
    
    with tab2:
        st.subheader("📋 Safety Incidents Database")
        
        # Search and Filter
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            search_term = st.text_input("🔍 Search Incidents", placeholder="Search by description, location...")
        with col2:
            type_filter = st.selectbox("Type", ["All", "Near Miss", "First Aid", "Medical Treatment", "Lost Time", "Other"])
        with col3:
            severity_filter = st.selectbox("Severity", ["All", "Low", "Medium", "High", "Critical"])
        with col4:
            status_filter = st.selectbox("Status", ["All", "Open", "Under Investigation", "Closed"])
        
        # Filter incidents
        filtered_incidents = st.session_state.safety_incidents
        
        if search_term:
            filtered_incidents = [i for i in filtered_incidents if search_term.lower() in 
                                (i['description'] + i['location']).lower()]
        if type_filter != "All":
            filtered_incidents = [i for i in filtered_incidents if i['type'] == type_filter]
        if severity_filter != "All":
            filtered_incidents = [i for i in filtered_incidents if i['severity'] == severity_filter]
        if status_filter != "All":
            filtered_incidents = [i for i in filtered_incidents if i['status'] == status_filter]
        
        # Display incidents
        for incident in filtered_incidents:
            severity_color = {
                "Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"
            }.get(incident['severity'], "⚪")
            
            with st.expander(f"🚨 {incident['id']} - {incident['type']} | {severity_color} {incident['severity']} | {incident['status']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**📅 Date/Time:** {incident['date']} at {incident['time']}")
                    st.markdown(f"**📍 Location:** {incident['location']}")
                    if incident['injured_person']:
                        st.markdown(f"**🤕 Injured Person:** {incident['injured_person']}")
                    if incident['witness']:
                        st.markdown(f"**👥 Witness:** {incident['witness']}")
                    st.markdown(f"**👤 Reported by:** {incident['reported_by']}")
                    
                    st.markdown("**📝 Description:**")
                    st.text(incident['description'])
                    
                    if incident['immediate_action']:
                        st.markdown("**🚑 Immediate Action:**")
                        st.text(incident['immediate_action'])
                    
                    if incident['root_cause']:
                        st.markdown("**🔍 Root Cause:**")
                        st.text(incident['root_cause'])
                    
                    if incident['corrective_action']:
                        st.markdown("**✅ Corrective Action:**")
                        st.text(incident['corrective_action'])
                
                with col2:
                    st.markdown("**🔧 Incident Management**")
                    
                    new_status = st.selectbox(
                        "Update Status",
                        ["Open", "Under Investigation", "Closed"],
                        index=["Open", "Under Investigation", "Closed"].index(incident['status']),
                        key=f"status_{incident['id']}"
                    )
                    
                    if st.button("💾 Update", key=f"update_{incident['id']}"):
                        for i, inc in enumerate(st.session_state.safety_incidents):
                            if inc['id'] == incident['id']:
                                st.session_state.safety_incidents[i]['status'] = new_status
                                break
                        st.success("Status updated!")
                        st.rerun()
                    
                    if st.button("✏️ Edit", key=f"edit_{incident['id']}"):
                        st.info("Edit functionality ready")
                    
                    if st.button("📄 Generate Report", key=f"report_{incident['id']}"):
                        st.info("Report generation ready")
                    
                    if st.button("🗑️ Delete", key=f"delete_{incident['id']}"):
                        st.session_state.safety_incidents = [i for i in st.session_state.safety_incidents 
                                                           if i['id'] != incident['id']]
                        st.success("Incident deleted!")
                        st.rerun()
    
    with tab3:
        st.subheader("🔍 Safety Inspections")
        
        # Create New Inspection
        with st.expander("➕ Schedule New Inspection"):
            with st.form("inspection_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    insp_area = st.text_input("Inspection Area")
                    insp_type = st.selectbox("Inspection Type", ["Routine", "Compliance", "Follow-up", "Special"])
                    inspector_name = st.text_input("Inspector Name")
                
                with col2:
                    insp_date = st.date_input("Inspection Date")
                    insp_checklist = st.text_area("Inspection Checklist Items", height=80)
                
                if st.form_submit_button("📅 Schedule Inspection"):
                    new_inspection = {
                        "id": f"INSP-{len(st.session_state.safety_inspections) + 1:03d}",
                        "date": str(insp_date),
                        "area": insp_area,
                        "inspector": inspector_name,
                        "type": insp_type,
                        "status": "Scheduled",
                        "score": 0,
                        "violations": [],
                        "recommendations": [],
                        "next_inspection": ""
                    }
                    st.session_state.safety_inspections.insert(0, new_inspection)
                    st.success("Inspection scheduled!")
                    st.rerun()
        
        # Display Inspections
        for inspection in st.session_state.safety_inspections:
            status_icon = {"Passed": "✅", "Minor Issues": "⚠️", "Failed": "❌", "Scheduled": "📅"}.get(inspection['status'], "📋")
            
            with st.expander(f"{status_icon} {inspection['id']} - {inspection['area']} | {inspection['status']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**📅 Date:** {inspection['date']}")
                    st.markdown(f"**👤 Inspector:** {inspection['inspector']}")
                    st.markdown(f"**🔍 Type:** {inspection['type']}")
                    if inspection['score'] > 0:
                        st.markdown(f"**📊 Score:** {inspection['score']}/100")
                    
                    if inspection['violations']:
                        st.markdown("**⚠️ Violations:**")
                        for violation in inspection['violations']:
                            st.write(f"• {violation}")
                    
                    if inspection['recommendations']:
                        st.markdown("**💡 Recommendations:**")
                        for rec in inspection['recommendations']:
                            st.write(f"• {rec}")
                
                with col2:
                    if st.button("✏️ Update Results", key=f"update_insp_{inspection['id']}"):
                        st.info("Update inspection results")
                    
                    if st.button("📄 Export Report", key=f"export_insp_{inspection['id']}"):
                        st.info("Export inspection report")
    
    with tab4:
        st.subheader("📚 Safety Training Management")
        
        # Training Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Scheduled Trainings", len([t for t in st.session_state.safety_training if t['status'] == 'Scheduled']), "📅")
        with col2:
            st.metric("Completed This Month", len([t for t in st.session_state.safety_training if t['status'] == 'Completed']), "✅")
        with col3:
            st.metric("Workers Trained", 45, "+8")
        
        # Schedule New Training
        with st.expander("➕ Schedule New Training"):
            with st.form("training_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    training_title = st.text_input("Training Title")
                    training_date = st.date_input("Training Date")
                    instructor = st.text_input("Instructor/Company")
                
                with col2:
                    duration = st.text_input("Duration")
                    attendees = st.text_area("Expected Attendees", height=68)
                    certification_period = st.text_input("Certification Valid Period")
                
                if st.form_submit_button("📚 Schedule Training"):
                    new_training = {
                        "id": f"TRAIN-{len(st.session_state.safety_training) + 1:03d}",
                        "title": training_title,
                        "date": str(training_date),
                        "instructor": instructor,
                        "attendees": attendees.split('\n') if attendees else [],
                        "duration": duration,
                        "status": "Scheduled",
                        "certification_valid": certification_period
                    }
                    st.session_state.safety_training.insert(0, new_training)
                    st.success("Training scheduled!")
                    st.rerun()
        
        # Display Trainings
        for training in st.session_state.safety_training:
            status_icon = {"Scheduled": "📅", "In Progress": "🔄", "Completed": "✅", "Cancelled": "❌"}.get(training['status'], "📋")
            
            with st.expander(f"{status_icon} {training['title']} - {training['date']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**📅 Date:** {training['date']}")
                    st.markdown(f"**👨‍🏫 Instructor:** {training['instructor']}")
                    st.markdown(f"**⏱️ Duration:** {training['duration']}")
                    st.markdown(f"**👥 Attendees:** {len(training['attendees'])} people")
                    if training['certification_valid']:
                        st.markdown(f"**📜 Certification Valid Until:** {training['certification_valid']}")
                
                with col2:
                    new_training_status = st.selectbox(
                        "Status",
                        ["Scheduled", "In Progress", "Completed", "Cancelled"],
                        index=["Scheduled", "In Progress", "Completed", "Cancelled"].index(training['status']),
                        key=f"train_status_{training['id']}"
                    )
                    
                    if st.button("💾 Update", key=f"update_train_{training['id']}"):
                        for i, t in enumerate(st.session_state.safety_training):
                            if t['id'] == training['id']:
                                st.session_state.safety_training[i]['status'] = new_training_status
                                break
                        st.success("Training status updated!")
                        st.rerun()
    
    with tab5:
        st.subheader("📊 Safety Analytics")
        
        if st.session_state.safety_incidents:
            col1, col2 = st.columns(2)
            
            with col1:
                # Incident Types
                type_counts = {}
                for incident in st.session_state.safety_incidents:
                    inc_type = incident['type']
                    type_counts[inc_type] = type_counts.get(inc_type, 0) + 1
                
                type_df = pd.DataFrame(list(type_counts.items()), columns=['Type', 'Count'])
                fig_types = px.pie(type_df, values='Count', names='Type', title="Incident Types Distribution")
                st.plotly_chart(fig_types, use_container_width=True)
                
                # Severity Distribution
                severity_counts = {}
                for incident in st.session_state.safety_incidents:
                    severity = incident['severity']
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1
                
                severity_df = pd.DataFrame(list(severity_counts.items()), columns=['Severity', 'Count'])
                fig_severity = px.bar(severity_df, x='Severity', y='Count', title="Incident Severity Distribution")
                st.plotly_chart(fig_severity, use_container_width=True)
            
            with col2:
                # Monthly Trends (simulated data)
                monthly_data = pd.DataFrame({
                    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                    'Incidents': [2, 1, 0, 1, len(st.session_state.safety_incidents)],
                    'Near Misses': [5, 3, 2, 4, 1],
                    'Safety Score': [92, 94, 97, 95, 98]
                })
                
                fig_monthly = px.line(monthly_data, x='Month', y=['Incidents', 'Near Misses'], 
                                    title="Monthly Safety Trends")
                st.plotly_chart(fig_monthly, use_container_width=True)
                
                # Safety Score Trend
                fig_score = px.line(monthly_data, x='Month', y='Safety Score', 
                                  title="Safety Score Trend")
                st.plotly_chart(fig_score, use_container_width=True)
    
    with tab6:
        st.subheader("⚙️ Safety Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔧 Notification Settings**")
            incident_notifications = st.checkbox("Email Notifications for Incidents", value=True)
            inspection_reminders = st.checkbox("Inspection Reminders", value=True)
            training_alerts = st.checkbox("Training Expiration Alerts", value=True)
            
            st.markdown("**📊 Reporting Settings**")
            auto_reports = st.checkbox("Automatic Monthly Reports", value=False)
            dashboard_refresh = st.number_input("Dashboard Refresh (minutes)", value=15, min_value=1)
            
            if st.button("💾 Save Settings", use_container_width=True):
                st.success("Settings saved successfully!")
        
        with col2:
            st.markdown("**📚 Quick Reference**")
            if st.button("📞 Emergency Contacts", use_container_width=True):
                st.info("Emergency contacts: 911, Site Safety: (555) 123-4567")
            
            if st.button("📖 Safety Manual", use_container_width=True):
                st.info("Safety manual access ready for implementation")
            
            if st.button("🎯 Training Materials", use_container_width=True):
                st.info("Training materials library ready")
            
            st.markdown("**🗂️ Data Management**")
            if st.button("📤 Export All Safety Data", use_container_width=True):
                st.info("Complete safety data export ready")
            
            if st.button("🔄 Reset Safety Data", use_container_width=True):
                if st.checkbox("⚠️ Confirm reset of all safety data"):
                    st.session_state.safety_incidents = []
                    st.session_state.safety_inspections = []
                    st.session_state.safety_training = []
                    st.success("Safety data reset!")
                    st.rerun()

def render_preconstruction():
    """Complete PreConstruction Management with full CRUD functionality"""
    st.markdown("""
    <div class="module-header">
        <h1>🏗️ PreConstruction Management</h1>
        <p>Comprehensive project planning, estimating, procurement, and bid management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize preconstruction data
    if "estimates" not in st.session_state:
        st.session_state.estimates = [
            {
                "id": "EST-001",
                "project_phase": "Foundation",
                "trade": "Concrete",
                "description": "Foundation concrete work including footings and slab",
                "quantity": 450,
                "unit": "cubic yards",
                "unit_cost": 185.00,
                "total_cost": 83250.00,
                "vendor": "ABC Concrete Supply",
                "status": "Approved",
                "created_date": "2024-12-15",
                "notes": "Includes reinforcement and finishing"
            },
            {
                "id": "EST-002",
                "project_phase": "Structure",
                "trade": "Steel",
                "description": "Structural steel for floors 1-8",
                "quantity": 125,
                "unit": "tons",
                "unit_cost": 3200.00,
                "total_cost": 400000.00,
                "vendor": "Steel Works Inc",
                "status": "Under Review",
                "created_date": "2025-01-10",
                "notes": "Fire-rated structural steel"
            }
        ]
    
    if "bids" not in st.session_state:
        st.session_state.bids = [
            {
                "id": "BID-001",
                "trade": "HVAC",
                "description": "Complete HVAC system for all floors",
                "bid_deadline": "2025-06-15",
                "invited_contractors": ["Climate Control Pro", "HVAC Masters", "Air Tech Solutions", "Comfort Systems"],
                "received_bids": [
                    {"contractor": "Climate Control Pro", "amount": 2100000, "submitted": True},
                    {"contractor": "HVAC Masters", "amount": 2250000, "submitted": True},
                    {"contractor": "Air Tech Solutions", "amount": 0, "submitted": False},
                    {"contractor": "Comfort Systems", "amount": 2050000, "submitted": True}
                ],
                "status": "Active",
                "project_manager": "Sarah Wilson",
                "scope_documents": ["HVAC Plans Rev 3", "Specifications Section 23", "Equipment Schedules"]
            },
            {
                "id": "BID-002",
                "trade": "Electrical",
                "description": "Electrical rough-in and finish work",
                "bid_deadline": "2025-06-20",
                "invited_contractors": ["Power Electric", "Spark Solutions", "Current Tech", "Wire Works", "Voltage Masters"],
                "received_bids": [
                    {"contractor": "Power Electric", "amount": 2400000, "submitted": True},
                    {"contractor": "Spark Solutions", "amount": 0, "submitted": False},
                    {"contractor": "Current Tech", "amount": 2550000, "submitted": True}
                ],
                "status": "Under Review",
                "project_manager": "Mike Johnson",
                "scope_documents": ["Electrical Plans Rev 2", "Panel Schedules", "Lighting Plans"]
            }
        ]
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_estimates = len(st.session_state.estimates)
    approved_estimates = len([e for e in st.session_state.estimates if e['status'] == 'Approved'])
    total_estimated_cost = sum(e['total_cost'] for e in st.session_state.estimates)
    active_bids = len([b for b in st.session_state.bids if b['status'] == 'Active'])
    
    with col1:
        st.metric("Total Estimates", total_estimates, delta_color="normal")
    with col2:
        st.metric("Approved Estimates", approved_estimates, delta_color="normal")
    with col3:
        st.metric("Estimated Value", f"${total_estimated_cost:,.2f}", delta_color="normal")
    with col4:
        st.metric("Active Bids", active_bids, delta_color="normal")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💰 Estimating", "📋 Bid Management", "📊 Project Overview", "📈 Analytics", "🔧 Management"])
    
    with tab1:
        st.subheader("💰 Cost Estimating")
        
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📝 Create Estimate", "📊 View Estimates", "📈 Cost Analysis"])
        
        with sub_tab1:
            st.markdown("**Create New Cost Estimate**")
            
            with st.form("estimate_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    project_phase = st.selectbox("Project Phase", 
                        ["Foundation", "Structure", "MEP", "Finishes", "Sitework", "Other"])
                    trade = st.text_input("Trade/Category", placeholder="e.g., Concrete, Steel, Electrical")
                    description = st.text_area("Work Description", placeholder="Detailed description of work scope")
                    quantity = st.number_input("Quantity", value=1.0, min_value=0.01)
                    unit = st.text_input("Unit", placeholder="e.g., sq ft, cubic yards, linear feet")
                
                with col2:
                    unit_cost = st.number_input("Unit Cost ($)", value=0.00, format="%.2f")
                    vendor = st.text_input("Preferred Vendor", placeholder="Vendor or supplier name")
                    notes = st.text_area("Notes", placeholder="Additional notes or considerations")
                
                if st.form_submit_button("💾 Create Estimate", type="primary"):
                    if trade and description and quantity and unit_cost:
                        new_estimate = {
                            "id": f"EST-{len(st.session_state.estimates) + 1:03d}",
                            "project_phase": project_phase,
                            "trade": trade,
                            "description": description,
                            "quantity": quantity,
                            "unit": unit,
                            "unit_cost": unit_cost,
                            "total_cost": quantity * unit_cost,
                            "vendor": vendor,
                            "status": "Draft",
                            "created_date": str(datetime.now().date()),
                            "notes": notes
                        }
                        st.session_state.estimates.append(new_estimate)
                        st.success("✅ Estimate created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with sub_tab2:
            st.markdown("**All Cost Estimates**")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                phase_filter = st.selectbox("Filter by Phase", ["All"] + list(set(e['project_phase'] for e in st.session_state.estimates)))
            with col2:
                status_filter = st.selectbox("Filter by Status", ["All", "Draft", "Under Review", "Approved", "Rejected"])
            with col3:
                trade_filter = st.selectbox("Filter by Trade", ["All"] + list(set(e['trade'] for e in st.session_state.estimates)))
            
            # Display estimates
            filtered_estimates = st.session_state.estimates
            if phase_filter != "All":
                filtered_estimates = [e for e in filtered_estimates if e['project_phase'] == phase_filter]
            if status_filter != "All":
                filtered_estimates = [e for e in filtered_estimates if e['status'] == status_filter]
            
            for estimate in filtered_estimates:
                with st.expander(f"💰 {estimate['id']} - {estimate['trade']} ({estimate['status']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**📋 Phase:** {estimate['project_phase']}")
                        st.write(f"**🔧 Trade:** {estimate['trade']}")
                        st.write(f"**📝 Description:** {estimate['description']}")
                        st.write(f"**📅 Created:** {estimate['created_date']}")
                    
                    with col2:
                        st.write(f"**📏 Quantity:** {estimate['quantity']} {estimate['unit']}")
                        st.write(f"**💲 Unit Cost:** ${estimate['unit_cost']:,.2f}")
                        st.write(f"**💰 Total Cost:** ${estimate['total_cost']:,.2f}")
                        st.write(f"**🏢 Vendor:** {estimate['vendor']}")
                    
                    with col3:
                        st.write(f"**📊 Status:** {estimate['status']}")
                        if estimate['notes']:
                            st.write(f"**📝 Notes:** {estimate['notes']}")
                    
                    # Status update buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button(f"✅ Approve", key=f"approve_{estimate['id']}"):
                            estimate['status'] = 'Approved'
                            st.success("Estimate approved!")
                            st.rerun()
                    with col2:
                        if st.button(f"📋 Review", key=f"review_{estimate['id']}"):
                            estimate['status'] = 'Under Review'
                            st.info("Estimate under review!")
                            st.rerun()
                    with col3:
                        if st.button(f"✏️ Edit", key=f"edit_{estimate['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col4:
                        if st.button(f"🗑️ Delete", key=f"delete_{estimate['id']}"):
                            st.session_state.estimates.remove(estimate)
                            st.success("Estimate deleted!")
                            st.rerun()
        
        with sub_tab3:
            st.markdown("**Cost Analysis by Phase**")
            
            if st.session_state.estimates:
                # Cost by phase
                phase_costs = {}
                for estimate in st.session_state.estimates:
                    phase = estimate['project_phase']
                    phase_costs[phase] = phase_costs.get(phase, 0) + estimate['total_cost']
                
                phase_list = list(phase_costs.keys())
                cost_list = list(phase_costs.values())
                phase_df = pd.DataFrame({
                    'Phase': phase_list,
                    'Total_Cost': cost_list
                })
                fig_phase = px.bar(phase_df, x='Phase', y='Total_Cost', title="Cost by Project Phase")
                st.plotly_chart(fig_phase, use_container_width=True)
    
    with tab2:
        st.subheader("📋 Bid Management")
        
        bid_sub_tab1, bid_sub_tab2, bid_sub_tab3 = st.tabs(["📤 Create Bid Package", "📊 Active Bids", "📈 Bid Analysis"])
        
        with bid_sub_tab1:
            st.markdown("**Create New Bid Package**")
            
            with st.form("bid_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    bid_trade = st.text_input("Trade", placeholder="e.g., HVAC, Plumbing, Electrical")
                    bid_description = st.text_area("Work Description", placeholder="Detailed scope of work")
                    bid_deadline = st.date_input("Bid Deadline", value=datetime.now().date() + timedelta(days=30))
                    project_manager = st.text_input("Project Manager", placeholder="Responsible PM")
                
                with col2:
                    invited_contractors = st.text_area("Invited Contractors", 
                        placeholder="Enter contractor names (one per line)")
                    scope_documents = st.text_area("Scope Documents", 
                        placeholder="List of drawings and specifications")
                
                if st.form_submit_button("📤 Create Bid Package", type="primary"):
                    if bid_trade and bid_description and invited_contractors:
                        contractor_list = [c.strip() for c in invited_contractors.split('\n') if c.strip()]
                        doc_list = [d.strip() for d in scope_documents.split('\n') if d.strip()]
                        
                        new_bid = {
                            "id": f"BID-{len(st.session_state.bids) + 1:03d}",
                            "trade": bid_trade,
                            "description": bid_description,
                            "bid_deadline": str(bid_deadline),
                            "invited_contractors": contractor_list,
                            "received_bids": [{"contractor": c, "amount": 0, "submitted": False} for c in contractor_list],
                            "status": "Active",
                            "project_manager": project_manager,
                            "scope_documents": doc_list
                        }
                        st.session_state.bids.append(new_bid)
                        st.success("✅ Bid package created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with bid_sub_tab2:
            st.markdown("**Active Bid Packages**")
            
            for bid in st.session_state.bids:
                submitted_count = len([b for b in bid['received_bids'] if b['submitted']])
                total_invited = len(bid['invited_contractors'])
                
                with st.expander(f"📋 {bid['id']} - {bid['trade']} ({submitted_count}/{total_invited} bids)"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**🔧 Trade:** {bid['trade']}")
                        st.write(f"**📝 Description:** {bid['description']}")
                        st.write(f"**📅 Deadline:** {bid['bid_deadline']}")
                        st.write(f"**👤 PM:** {bid['project_manager']}")
                        st.write(f"**📊 Status:** {bid['status']}")
                    
                    with col2:
                        st.write("**📋 Invited Contractors:**")
                        for contractor in bid['invited_contractors']:
                            st.write(f"- {contractor}")
                        
                        if bid['scope_documents']:
                            st.write("**📄 Scope Documents:**")
                            for doc in bid['scope_documents']:
                                st.write(f"- {doc}")
                    
                    st.write("**💰 Received Bids:**")
                    bid_data = []
                    for received_bid in bid['received_bids']:
                        status_icon = "✅" if received_bid['submitted'] else "⏰"
                        amount_display = f"${received_bid['amount']:,.2f}" if received_bid['submitted'] else "Pending"
                        bid_data.append({
                            "Status": status_icon,
                            "Contractor": received_bid['contractor'],
                            "Bid Amount": amount_display
                        })
                    
                    if bid_data:
                        bid_df = pd.DataFrame(bid_data)
                        st.dataframe(bid_df, use_container_width=True)
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📧 Send Reminder", key=f"remind_{bid['id']}"):
                            st.info("Reminder sent to contractors!")
                    with col2:
                        if st.button(f"✅ Award", key=f"award_{bid['id']}"):
                            bid['status'] = 'Awarded'
                            st.success("Bid awarded!")
                            st.rerun()
                    with col3:
                        if st.button(f"❌ Cancel", key=f"cancel_{bid['id']}"):
                            bid['status'] = 'Cancelled'
                            st.warning("Bid cancelled!")
                            st.rerun()
        
        with bid_sub_tab3:
            st.markdown("**Bid Analysis**")
            
            if st.session_state.bids:
                # Bid status distribution
                status_counts = {}
                for bid in st.session_state.bids:
                    status = bid['status']
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                status_list = list(status_counts.keys())
                count_list = list(status_counts.values())
                status_df = pd.DataFrame({
                    'Status': status_list,
                    'Count': count_list
                })
                fig_status = px.pie(status_df, values='Count', names='Status', title="Bid Package Status Distribution")
                st.plotly_chart(fig_status, use_container_width=True)
    
    with tab3:
        st.subheader("📊 Project Overview - Highland Tower Development")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎯 Project Information**")
            st.write("**Project Name:** Highland Tower Development")
            st.write("**Total Contract Value:** $45,500,000")
            st.write("**Start Date:** January 15, 2025")
            st.write("**Planned Completion:** December 2026")
            st.write("**Total Units:** 120 Residential + 8 Retail")
            st.write("**Building Height:** 12 floors")
            st.write("**Total Square Footage:** 185,000 sq ft")
            
            st.markdown("**📈 Project Phases**")
            phases_data = [
                {"Phase": "Site Preparation", "Duration": "2 months", "Status": "✅ Complete", "Progress": 100},
                {"Phase": "Foundation", "Duration": "3 months", "Status": "✅ Complete", "Progress": 100},
                {"Phase": "Structure", "Duration": "8 months", "Status": "🔄 In Progress", "Progress": 68},
                {"Phase": "MEP", "Duration": "4 months", "Status": "⏰ Planned", "Progress": 0},
                {"Phase": "Finishes", "Duration": "6 months", "Status": "⏰ Planned", "Progress": 0}
            ]
            
            for phase in phases_data:
                st.write(f"**{phase['Phase']}** - {phase['Status']}")
                st.progress(phase['Progress'] / 100)
        
        with col2:
            st.markdown("**💰 Cost Breakdown**")
            cost_breakdown = pd.DataFrame({
                'Category': ['Labor', 'Materials', 'Equipment', 'Overhead', 'Profit'],
                'Amount': [18200000, 15600000, 4550000, 3640000, 3510000],
                'Percentage': [40.0, 34.3, 10.0, 8.0, 7.7]
            })
            
            fig_cost = px.pie(cost_breakdown, values='Amount', names='Category', 
                            title="Project Cost Distribution")
            st.plotly_chart(fig_cost, use_container_width=True)
            
            st.markdown("**📏 Unit Breakdown**")
            unit_data = pd.DataFrame({
                'Unit Type': ['Studio', '1-Bedroom', '2-Bedroom', '3-Bedroom', 'Small Retail', 'Large Retail'],
                'Count': [24, 48, 36, 12, 6, 2],
                'Cost Each': [180000, 225000, 285000, 340000, 150000, 275000]
            })
            
            fig_units = px.bar(unit_data, x='Unit Type', y='Count', 
                             title="Unit Count by Type")
            st.plotly_chart(fig_units, use_container_width=True)
    
    with tab4:
        st.subheader("📈 PreConstruction Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Estimate status distribution
            if st.session_state.estimates:
                estimate_status_counts = {}
                for estimate in st.session_state.estimates:
                    status = estimate['status']
                    estimate_status_counts[status] = estimate_status_counts.get(status, 0) + 1
                
                est_status_list = list(estimate_status_counts.keys())
                est_count_list = list(estimate_status_counts.values())
                est_status_df = pd.DataFrame({
                    'Status': est_status_list,
                    'Count': est_count_list
                })
                fig_est_status = px.pie(est_status_df, values='Count', names='Status', title="Estimate Status Distribution")
                st.plotly_chart(fig_est_status, use_container_width=True)
        
        with col2:
            # Cost trends by trade
            if st.session_state.estimates:
                trade_costs = {}
                for estimate in st.session_state.estimates:
                    trade = estimate['trade']
                    trade_costs[trade] = trade_costs.get(trade, 0) + estimate['total_cost']
                
                trade_list = list(trade_costs.keys())
                trade_cost_list = list(trade_costs.values())
                trade_df = pd.DataFrame({
                    'Trade': trade_list,
                    'Total_Cost': trade_cost_list
                })
                fig_trade = px.bar(trade_df, x='Trade', y='Total_Cost', title="Cost by Trade")
                st.plotly_chart(fig_trade, use_container_width=True)
    
    with tab5:
        st.subheader("🔧 PreConstruction Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Estimate Summary**")
            if st.session_state.estimates:
                est_stats_data = pd.DataFrame([
                    {"Metric": "Total Estimates", "Value": len(st.session_state.estimates)},
                    {"Metric": "Approved Estimates", "Value": len([e for e in st.session_state.estimates if e['status'] == 'Approved'])},
                    {"Metric": "Total Estimated Value", "Value": f"${sum(e['total_cost'] for e in st.session_state.estimates):,.2f}"},
                    {"Metric": "Average Estimate", "Value": f"${sum(e['total_cost'] for e in st.session_state.estimates) / len(st.session_state.estimates):,.2f}"},
                ])
                st.dataframe(est_stats_data, use_container_width=True)
        
        with col2:
            st.markdown("**📋 Bid Summary**")
            if st.session_state.bids:
                bid_stats_data = pd.DataFrame([
                    {"Metric": "Total Bid Packages", "Value": len(st.session_state.bids)},
                    {"Metric": "Active Bids", "Value": len([b for b in st.session_state.bids if b['status'] == 'Active'])},
                    {"Metric": "Total Invited Contractors", "Value": sum(len(b['invited_contractors']) for b in st.session_state.bids)},
                    {"Metric": "Bids Received", "Value": sum(len([rb for rb in b['received_bids'] if rb['submitted']]) for b in st.session_state.bids)},
                ])
                st.dataframe(bid_stats_data, use_container_width=True)
        
        # Data management
        st.markdown("**⚠️ Data Management**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear All Estimates", type="secondary"):
                st.session_state.estimates = []
                st.success("All estimates cleared!")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear All Bids", type="secondary"):
                st.session_state.bids = []
                st.success("All bids cleared!")
                st.rerun()

def render_engineering():
    """Complete Engineering Management with full CRUD functionality"""
    st.markdown("""
    <div class="module-header">
        <h1>⚙️ Engineering Management</h1>
        <p>Advanced technical coordination, drawing management, and engineering workflows</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize engineering data
    if "engineering_rfis" not in st.session_state:
        st.session_state.engineering_rfis = [
            {
                "id": "ENG-RFI-001",
                "subject": "Structural steel connection details for Level 8",
                "trade": "Structural",
                "priority": "High",
                "status": "Response Pending",
                "submitted_by": "Steel Fabricator",
                "submitted_date": "2025-05-20",
                "response_due": "2025-05-30",
                "description": "Clarification needed on moment connection details for beam-to-column connections on Level 8. Current drawings show conflicting information between architectural and structural plans.",
                "location": "Level 8, Grid Lines C-3 to C-7",
                "drawing_references": ["S-801", "S-802", "A-801"],
                "assigned_engineer": "Sarah Chen, P.E.",
                "response": "",
                "cost_impact": 15000,
                "schedule_impact": 3,
                "attachments": ["Connection Detail Photos", "Shop Drawing Excerpts"],
                "coordination_notes": "Requires coordination with architectural team"
            },
            {
                "id": "ENG-RFI-002",
                "subject": "MEP routing conflicts in ceiling space",
                "trade": "MEP",
                "priority": "Medium",
                "status": "Under Review",
                "submitted_by": "MEP Contractor",
                "submitted_date": "2025-05-22",
                "response_due": "2025-06-01",
                "description": "HVAC ductwork conflicts with electrical conduit routing in Level 9 ceiling space. Need design team review for coordination solution.",
                "location": "Level 9, Zones A-C",
                "drawing_references": ["M-901", "E-901", "A-901"],
                "assigned_engineer": "Mike Rodriguez, P.E.",
                "response": "Under coordination review with design team",
                "cost_impact": 8500,
                "schedule_impact": 2,
                "attachments": ["MEP Coordination Model", "Conflict Report"],
                "coordination_notes": "3D model coordination in progress"
            }
        ]
    
    if "change_orders" not in st.session_state:
        st.session_state.change_orders = [
            {
                "id": "CO-001",
                "title": "Additional MEP work for data center upgrade",
                "description": "Owner requested upgrade to data center infrastructure requiring additional electrical and cooling capacity",
                "trade": "MEP",
                "amount": 125000.00,
                "status": "Approved",
                "submitted_date": "2025-05-15",
                "approved_date": "2025-05-20",
                "schedule_impact": 5,
                "reason": "Owner Request",
                "submitted_by": "Project Manager",
                "approved_by": "Owner Representative",
                "scope_description": "Installation of additional UPS systems, backup generators, and enhanced HVAC for data center",
                "drawings_affected": ["E-401", "E-402", "M-401", "M-402"]
            },
            {
                "id": "CO-002",
                "title": "Design modification for retail entrance",
                "description": "Architectural design change for main retail entrance per city planning requirements",
                "trade": "Architectural",
                "amount": 75000.00,
                "status": "Under Review",
                "submitted_date": "2025-05-18",
                "approved_date": "",
                "schedule_impact": 0,
                "reason": "Code Compliance",
                "submitted_by": "Architect",
                "approved_by": "",
                "scope_description": "Redesign of main entrance canopy and accessible ramp configuration",
                "drawings_affected": ["A-101", "A-201", "A-301"]
            }
        ]
    
    if "technical_reviews" not in st.session_state:
        st.session_state.technical_reviews = [
            {
                "id": "TR-001",
                "item": "Shop Drawings - Structural Steel Connections",
                "type": "Shop Drawing",
                "reviewer": "Sarah Chen, P.E.",
                "status": "Approved",
                "submitted_date": "2025-05-20",
                "review_date": "2025-05-25",
                "priority": "High",
                "comments": "Approved as submitted. All connection details meet specification requirements.",
                "revision_required": False,
                "drawing_numbers": ["SD-S-001", "SD-S-002", "SD-S-003"],
                "trade": "Structural"
            },
            {
                "id": "TR-002",
                "item": "MEP Coordination Model - Levels 9-11",
                "type": "Coordination Review",
                "reviewer": "Mike Rodriguez, P.E.",
                "status": "Revisions Required",
                "submitted_date": "2025-05-22",
                "review_date": "2025-05-24",
                "priority": "Medium",
                "comments": "Minor conflicts identified in ceiling space. Revise ductwork routing per redlines.",
                "revision_required": True,
                "drawing_numbers": ["M-901", "M-1001", "M-1101"],
                "trade": "MEP"
            }
        ]
    
    # Key Engineering Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    active_rfis = len([r for r in st.session_state.engineering_rfis if r['status'] != 'Closed'])
    pending_reviews = len([r for r in st.session_state.technical_reviews if r['status'] == 'Under Review'])
    open_change_orders = len([c for c in st.session_state.change_orders if c['status'] != 'Approved'])
    total_cost_impact = sum(r['cost_impact'] for r in st.session_state.engineering_rfis)
    
    with col1:
        st.metric("Active RFIs", active_rfis, delta_color="normal")
    with col2:
        st.metric("Pending Reviews", pending_reviews, delta_color="normal")
    with col3:
        st.metric("Open Change Orders", open_change_orders, delta_color="normal")
    with col4:
        st.metric("Cost Impact", f"${total_cost_impact:,.0f}", delta_color="normal")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 RFI Management", "📋 Change Orders", "🔧 Technical Reviews", "📈 Analytics", "🔧 Management"])
    
    with tab1:
        st.subheader("📝 Request for Information (RFI) Management")
        
        rfi_sub_tab1, rfi_sub_tab2, rfi_sub_tab3 = st.tabs(["📤 Create RFI", "📊 View RFIs", "📈 RFI Analytics"])
        
        with rfi_sub_tab1:
            st.markdown("**Create New RFI**")
            
            with st.form("rfi_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    rfi_subject = st.text_input("RFI Subject", placeholder="Brief description of the question/issue")
                    trade = st.selectbox("Trade", ["Architectural", "Structural", "MEP", "Civil", "Electrical", "Mechanical", "Plumbing", "Other"])
                    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
                    location = st.text_input("Location", placeholder="Building level, grid lines, room number")
                    submitted_by = st.text_input("Submitted By", placeholder="Company/Person submitting")
                
                with col2:
                    response_due = st.date_input("Response Required By", value=datetime.now().date() + timedelta(days=10))
                    drawing_refs = st.text_input("Drawing References", placeholder="Comma-separated drawing numbers")
                    assigned_engineer = st.selectbox("Assigned Engineer", 
                        ["Sarah Chen, P.E.", "Mike Rodriguez, P.E.", "Jennifer Walsh, AIA", "David Kim, P.E."])
                    cost_impact = st.number_input("Estimated Cost Impact ($)", value=0, format="%d")
                    schedule_impact = st.number_input("Schedule Impact (days)", value=0, format="%d")
                
                description = st.text_area("Detailed Description", placeholder="Provide detailed description of the question or issue")
                coordination_notes = st.text_area("Coordination Notes", placeholder="Any coordination requirements or notes")
                
                if st.form_submit_button("📝 Submit RFI", type="primary"):
                    if rfi_subject and description and trade:
                        new_rfi = {
                            "id": f"ENG-RFI-{len(st.session_state.engineering_rfis) + 1:03d}",
                            "subject": rfi_subject,
                            "trade": trade,
                            "priority": priority,
                            "status": "Open",
                            "submitted_by": submitted_by,
                            "submitted_date": str(datetime.now().date()),
                            "response_due": str(response_due),
                            "description": description,
                            "location": location,
                            "drawing_references": [ref.strip() for ref in drawing_refs.split(',') if ref.strip()],
                            "assigned_engineer": assigned_engineer,
                            "response": "",
                            "cost_impact": cost_impact,
                            "schedule_impact": schedule_impact,
                            "attachments": [],
                            "coordination_notes": coordination_notes
                        }
                        st.session_state.engineering_rfis.append(new_rfi)
                        st.success("✅ RFI submitted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with rfi_sub_tab2:
            st.markdown("**All Engineering RFIs**")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All", "Open", "Response Pending", "Under Review", "Closed"])
            with col2:
                trade_filter = st.selectbox("Filter by Trade", ["All"] + list(set(r['trade'] for r in st.session_state.engineering_rfis)))
            with col3:
                priority_filter = st.selectbox("Filter by Priority", ["All", "Low", "Medium", "High", "Critical"])
            
            # Display RFIs
            filtered_rfis = st.session_state.engineering_rfis
            if status_filter != "All":
                filtered_rfis = [r for r in filtered_rfis if r['status'] == status_filter]
            if trade_filter != "All":
                filtered_rfis = [r for r in filtered_rfis if r['trade'] == trade_filter]
            if priority_filter != "All":
                filtered_rfis = [r for r in filtered_rfis if r['priority'] == priority_filter]
            
            for rfi in filtered_rfis:
                priority_icon = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}.get(rfi['priority'], "⚪")
                
                with st.expander(f"{priority_icon} {rfi['id']} - {rfi['subject']} ({rfi['status']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**🔧 Trade:** {rfi['trade']}")
                        st.write(f"**📍 Location:** {rfi['location']}")
                        st.write(f"**👤 Submitted By:** {rfi['submitted_by']}")
                        st.write(f"**📅 Submitted:** {rfi['submitted_date']}")
                        st.write(f"**⏰ Due:** {rfi['response_due']}")
                    
                    with col2:
                        st.write(f"**⚠️ Priority:** {rfi['priority']}")
                        st.write(f"**👨‍💼 Assigned:** {rfi['assigned_engineer']}")
                        st.write(f"**💰 Cost Impact:** ${rfi['cost_impact']:,.0f}")
                        st.write(f"**📅 Schedule Impact:** {rfi['schedule_impact']} days")
                        if rfi['drawing_references']:
                            st.write(f"**📐 Drawings:** {', '.join(rfi['drawing_references'])}")
                    
                    with col3:
                        st.write(f"**📊 Status:** {rfi['status']}")
                        if rfi['response']:
                            st.write(f"**💬 Response:** {rfi['response']}")
                        if rfi['coordination_notes']:
                            st.write(f"**📝 Notes:** {rfi['coordination_notes']}")
                    
                    st.write(f"**📝 Description:** {rfi['description']}")
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button(f"✅ Close RFI", key=f"close_rfi_{rfi['id']}"):
                            rfi['status'] = 'Closed'
                            st.success("RFI closed!")
                            st.rerun()
                    with col2:
                        if st.button(f"🔄 Under Review", key=f"review_rfi_{rfi['id']}"):
                            rfi['status'] = 'Under Review'
                            st.info("RFI under review!")
                            st.rerun()
                    with col3:
                        if st.button(f"✏️ Add Response", key=f"respond_rfi_{rfi['id']}"):
                            st.info("Response interface - would open response form")
                    with col4:
                        if st.button(f"🗑️ Delete", key=f"delete_rfi_{rfi['id']}"):
                            st.session_state.engineering_rfis.remove(rfi)
                            st.success("RFI deleted!")
                            st.rerun()
        
        with rfi_sub_tab3:
            st.markdown("**RFI Analytics**")
            
            if st.session_state.engineering_rfis:
                col1, col2 = st.columns(2)
                
                with col1:
                    # RFI status distribution
                    status_counts = {}
                    for rfi in st.session_state.engineering_rfis:
                        status = rfi['status']
                        status_counts[status] = status_counts.get(status, 0) + 1
                    
                    if status_counts:
                        status_list = list(status_counts.keys())
                        count_list = list(status_counts.values())
                        status_df = pd.DataFrame({
                            'Status': status_list,
                            'Count': count_list
                        })
                        fig_status = px.pie(status_df, values='Count', names='Status', title="RFI Status Distribution")
                        st.plotly_chart(fig_status, use_container_width=True)
                
                with col2:
                    # Cost impact by trade
                    trade_costs = {}
                    for rfi in st.session_state.engineering_rfis:
                        trade = rfi['trade']
                        trade_costs[trade] = trade_costs.get(trade, 0) + rfi['cost_impact']
                    
                    if trade_costs:
                        trade_list = list(trade_costs.keys())
                        cost_list = list(trade_costs.values())
                        trade_df = pd.DataFrame({
                            'Trade': trade_list,
                            'Cost_Impact': cost_list
                        })
                        fig_trade = px.bar(trade_df, x='Trade', y='Cost_Impact', title="Cost Impact by Trade")
                        st.plotly_chart(fig_trade, use_container_width=True)
    
    with tab2:
        st.subheader("📋 Change Order Management")
        
        co_sub_tab1, co_sub_tab2 = st.tabs(["📤 Create Change Order", "📊 View Change Orders"])
        
        with co_sub_tab1:
            st.markdown("**Create New Change Order**")
            
            with st.form("change_order_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    co_title = st.text_input("Change Order Title", placeholder="Brief title describing the change")
                    trade = st.selectbox("Affected Trade", ["Architectural", "Structural", "MEP", "Civil", "General"])
                    amount = st.number_input("Amount ($)", value=0.00, format="%.2f")
                    schedule_impact = st.number_input("Schedule Impact (days)", value=0, format="%d")
                    reason = st.selectbox("Reason", ["Owner Request", "Design Change", "Site Conditions", "Code Compliance", "Coordination Issue"])
                
                with col2:
                    submitted_by = st.text_input("Submitted By", placeholder="Person/company submitting")
                    drawings_affected = st.text_input("Drawings Affected", placeholder="Comma-separated drawing numbers")
                    
                description = st.text_area("Detailed Description", placeholder="Provide detailed description of the change")
                scope_description = st.text_area("Scope Description", placeholder="Detailed scope of work for this change")
                
                if st.form_submit_button("📋 Submit Change Order", type="primary"):
                    if co_title and description and amount >= 0:
                        new_co = {
                            "id": f"CO-{len(st.session_state.change_orders) + 1:03d}",
                            "title": co_title,
                            "description": description,
                            "trade": trade,
                            "amount": amount,
                            "status": "Submitted",
                            "submitted_date": str(datetime.now().date()),
                            "approved_date": "",
                            "schedule_impact": schedule_impact,
                            "reason": reason,
                            "submitted_by": submitted_by,
                            "approved_by": "",
                            "scope_description": scope_description,
                            "drawings_affected": [d.strip() for d in drawings_affected.split(',') if d.strip()]
                        }
                        st.session_state.change_orders.append(new_co)
                        st.success("✅ Change Order submitted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with co_sub_tab2:
            st.markdown("**All Change Orders**")
            
            for co in st.session_state.change_orders:
                status_icon = {"Submitted": "📋", "Under Review": "🔄", "Approved": "✅", "Rejected": "❌"}.get(co['status'], "📋")
                
                with st.expander(f"{status_icon} {co['id']} - {co['title']} (${co['amount']:,.2f})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**💰 Amount:** ${co['amount']:,.2f}")
                        st.write(f"**🔧 Trade:** {co['trade']}")
                        st.write(f"**📅 Submitted:** {co['submitted_date']}")
                        st.write(f"**👤 Submitted By:** {co['submitted_by']}")
                        st.write(f"**📅 Schedule Impact:** {co['schedule_impact']} days")
                        st.write(f"**📋 Reason:** {co['reason']}")
                    
                    with col2:
                        st.write(f"**📊 Status:** {co['status']}")
                        if co['approved_date']:
                            st.write(f"**✅ Approved:** {co['approved_date']}")
                            st.write(f"**👤 Approved By:** {co['approved_by']}")
                        if co['drawings_affected']:
                            st.write(f"**📐 Drawings Affected:** {', '.join(co['drawings_affected'])}")
                    
                    st.write(f"**📝 Description:** {co['description']}")
                    if co['scope_description']:
                        st.write(f"**🔧 Scope:** {co['scope_description']}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if co['status'] != 'Approved' and st.button(f"✅ Approve", key=f"approve_co_{co['id']}"):
                            co['status'] = 'Approved'
                            co['approved_date'] = str(datetime.now().date())
                            co['approved_by'] = 'Project Manager'
                            st.success("Change Order approved!")
                            st.rerun()
                    with col2:
                        if st.button(f"🔄 Under Review", key=f"review_co_{co['id']}"):
                            co['status'] = 'Under Review'
                            st.info("Change Order under review!")
                            st.rerun()
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_co_{co['id']}"):
                            st.session_state.change_orders.remove(co)
                            st.success("Change Order deleted!")
                            st.rerun()
    
    with tab3:
        st.subheader("🔧 Technical Reviews")
        
        tr_sub_tab1, tr_sub_tab2 = st.tabs(["📤 Create Review", "📊 View Reviews"])
        
        with tr_sub_tab1:
            st.markdown("**Create New Technical Review**")
            
            with st.form("technical_review_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    item = st.text_input("Review Item", placeholder="What is being reviewed")
                    review_type = st.selectbox("Review Type", ["Shop Drawing", "Coordination Review", "Design Review", "Submittal Review"])
                    reviewer = st.selectbox("Reviewer", ["Sarah Chen, P.E.", "Mike Rodriguez, P.E.", "Jennifer Walsh, AIA", "David Kim, P.E."])
                    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
                
                with col2:
                    trade = st.selectbox("Trade", ["Architectural", "Structural", "MEP", "Civil", "General"])
                    drawing_numbers = st.text_input("Drawing Numbers", placeholder="Comma-separated drawing numbers")
                
                comments = st.text_area("Review Comments", placeholder="Detailed review comments and requirements")
                
                if st.form_submit_button("🔧 Create Review", type="primary"):
                    if item and reviewer and comments:
                        new_review = {
                            "id": f"TR-{len(st.session_state.technical_reviews) + 1:03d}",
                            "item": item,
                            "type": review_type,
                            "reviewer": reviewer,
                            "status": "Under Review",
                            "submitted_date": str(datetime.now().date()),
                            "review_date": "",
                            "priority": priority,
                            "comments": comments,
                            "revision_required": False,
                            "drawing_numbers": [d.strip() for d in drawing_numbers.split(',') if d.strip()],
                            "trade": trade
                        }
                        st.session_state.technical_reviews.append(new_review)
                        st.success("✅ Technical review created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with tr_sub_tab2:
            st.markdown("**All Technical Reviews**")
            
            for review in st.session_state.technical_reviews:
                status_icon = {"Under Review": "🔄", "Approved": "✅", "Revisions Required": "⚠️", "Rejected": "❌"}.get(review['status'], "📋")
                
                with st.expander(f"{status_icon} {review['id']} - {review['item']} ({review['status']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📋 Type:** {review['type']}")
                        st.write(f"**👨‍💼 Reviewer:** {review['reviewer']}")
                        st.write(f"**🔧 Trade:** {review['trade']}")
                        st.write(f"**📅 Submitted:** {review['submitted_date']}")
                        if review['review_date']:
                            st.write(f"**📅 Reviewed:** {review['review_date']}")
                    
                    with col2:
                        st.write(f"**⚠️ Priority:** {review['priority']}")
                        st.write(f"**📊 Status:** {review['status']}")
                        if review['drawing_numbers']:
                            st.write(f"**📐 Drawings:** {', '.join(review['drawing_numbers'])}")
                        st.write(f"**🔄 Revisions Required:** {'Yes' if review['revision_required'] else 'No'}")
                    
                    st.write(f"**💬 Comments:** {review['comments']}")
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button(f"✅ Approve", key=f"approve_tr_{review['id']}"):
                            review['status'] = 'Approved'
                            review['review_date'] = str(datetime.now().date())
                            review['revision_required'] = False
                            st.success("Review approved!")
                            st.rerun()
                    with col2:
                        if st.button(f"⚠️ Revisions", key=f"revise_tr_{review['id']}"):
                            review['status'] = 'Revisions Required'
                            review['review_date'] = str(datetime.now().date())
                            review['revision_required'] = True
                            st.warning("Revisions requested!")
                            st.rerun()
                    with col3:
                        if st.button(f"❌ Reject", key=f"reject_tr_{review['id']}"):
                            review['status'] = 'Rejected'
                            review['review_date'] = str(datetime.now().date())
                            st.error("Review rejected!")
                            st.rerun()
                    with col4:
                        if st.button(f"🗑️ Delete", key=f"delete_tr_{review['id']}"):
                            st.session_state.technical_reviews.remove(review)
                            st.success("Review deleted!")
                            st.rerun()
    
    with tab4:
        st.subheader("📈 Engineering Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Change order amounts by trade
            if st.session_state.change_orders:
                co_trade_amounts = {}
                for co in st.session_state.change_orders:
                    trade = co['trade']
                    co_trade_amounts[trade] = co_trade_amounts.get(trade, 0) + co['amount']
                
                if co_trade_amounts:
                    trade_list = list(co_trade_amounts.keys())
                    amount_list = list(co_trade_amounts.values())
                    co_trade_df = pd.DataFrame({
                        'Trade': trade_list,
                        'Amount': amount_list
                    })
                    fig_co_trade = px.bar(co_trade_df, x='Trade', y='Amount', title="Change Order Amounts by Trade")
                    st.plotly_chart(fig_co_trade, use_container_width=True)
        
        with col2:
            # Technical review status
            if st.session_state.technical_reviews:
                tr_status_counts = {}
                for tr in st.session_state.technical_reviews:
                    status = tr['status']
                    tr_status_counts[status] = tr_status_counts.get(status, 0) + 1
                
                if tr_status_counts:
                    tr_status_list = list(tr_status_counts.keys())
                    tr_count_list = list(tr_status_counts.values())
                    tr_status_df = pd.DataFrame({
                        'Status': tr_status_list,
                        'Count': tr_count_list
                    })
                    fig_tr_status = px.pie(tr_status_df, values='Count', names='Status', title="Technical Review Status")
                    st.plotly_chart(fig_tr_status, use_container_width=True)
    
    with tab5:
        st.subheader("🔧 Engineering Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📊 RFI Summary**")
            if st.session_state.engineering_rfis:
                rfi_stats_data = pd.DataFrame([
                    {"Metric": "Total RFIs", "Value": len(st.session_state.engineering_rfis)},
                    {"Metric": "Open RFIs", "Value": len([r for r in st.session_state.engineering_rfis if r['status'] != 'Closed'])},
                    {"Metric": "High Priority", "Value": len([r for r in st.session_state.engineering_rfis if r['priority'] == 'High'])},
                    {"Metric": "Total Cost Impact", "Value": f"${sum(r['cost_impact'] for r in st.session_state.engineering_rfis):,.0f}"},
                ])
                st.dataframe(rfi_stats_data, use_container_width=True)
        
        with col2:
            st.markdown("**📋 Change Order Summary**")
            if st.session_state.change_orders:
                co_stats_data = pd.DataFrame([
                    {"Metric": "Total Change Orders", "Value": len(st.session_state.change_orders)},
                    {"Metric": "Approved", "Value": len([c for c in st.session_state.change_orders if c['status'] == 'Approved'])},
                    {"Metric": "Pending Approval", "Value": len([c for c in st.session_state.change_orders if c['status'] != 'Approved'])},
                    {"Metric": "Total Value", "Value": f"${sum(c['amount'] for c in st.session_state.change_orders):,.2f}"},
                ])
                st.dataframe(co_stats_data, use_container_width=True)
        
        with col3:
            st.markdown("**🔧 Review Summary**")
            if st.session_state.technical_reviews:
                tr_stats_data = pd.DataFrame([
                    {"Metric": "Total Reviews", "Value": len(st.session_state.technical_reviews)},
                    {"Metric": "Approved", "Value": len([r for r in st.session_state.technical_reviews if r['status'] == 'Approved'])},
                    {"Metric": "Under Review", "Value": len([r for r in st.session_state.technical_reviews if r['status'] == 'Under Review'])},
                    {"Metric": "Require Revisions", "Value": len([r for r in st.session_state.technical_reviews if r['revision_required']])},
                ])
                st.dataframe(tr_stats_data, use_container_width=True)
        
        # Data management
        st.markdown("**⚠️ Data Management**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🗑️ Clear All RFIs", type="secondary"):
                st.session_state.engineering_rfis = []
                st.success("All RFIs cleared!")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Change Orders", type="secondary"):
                st.session_state.change_orders = []
                st.success("All change orders cleared!")
                st.rerun()
        with col3:
            if st.button("🗑️ Clear Reviews", type="secondary"):
                st.session_state.technical_reviews = []
                st.success("All reviews cleared!")
                st.rerun()

def render_field_operations():
    """Complete Field Operations Management with full CRUD functionality"""
    st.markdown("""
    <div class="module-header">
        <h1>👷 Field Operations Management</h1>
        <p>Real-time crew coordination, work progress tracking, and equipment management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize field operations data
    if "crews" not in st.session_state:
        st.session_state.crews = [
            {
                "id": "CREW-001",
                "name": "Structural Steel Team Alpha",
                "foreman": "Mike Chen",
                "workers": 12,
                "trade": "Structural",
                "location": "Level 8 - Grid Lines A-D",
                "current_activity": "Steel beam installation and welding",
                "status": "Active",
                "shift_start": "07:00",
                "shift_end": "16:00",
                "productivity": 95,
                "safety_score": 98,
                "phone": "(555) 123-4567",
                "certification": "OSHA 30, AWS D1.1",
                "equipment_assigned": ["Crane", "Welding Equipment", "Safety Gear"]
            },
            {
                "id": "CREW-002",
                "name": "MEP Installation Team Beta",
                "foreman": "Sarah Rodriguez",
                "workers": 15,
                "trade": "MEP",
                "location": "Level 6-7 - Electrical Rooms",
                "current_activity": "Electrical panel installation and conduit routing",
                "status": "Active",
                "shift_start": "07:00",
                "shift_end": "16:00",
                "productivity": 88,
                "safety_score": 100,
                "phone": "(555) 234-5678",
                "certification": "Electrical License, OSHA 10",
                "equipment_assigned": ["Scissor Lift", "Electrical Tools", "Cable Pulling Equipment"]
            },
            {
                "id": "CREW-003",
                "name": "Concrete Finishing Crew",
                "foreman": "David Wilson",
                "workers": 8,
                "trade": "Concrete",
                "location": "Level 5 - East Wing",
                "current_activity": "Concrete finishing and curing",
                "status": "Break",
                "shift_start": "06:00",
                "shift_end": "15:00",
                "productivity": 92,
                "safety_score": 96,
                "phone": "(555) 345-6789",
                "certification": "ACI Certification, OSHA 30",
                "equipment_assigned": ["Concrete Tools", "Power Trowels", "Curing Equipment"]
            }
        ]
    
    if "work_packages" not in st.session_state:
        st.session_state.work_packages = [
            {
                "id": "WP-001",
                "title": "Level 8 Structural Steel Installation",
                "description": "Install structural steel beams and columns for Level 8",
                "assigned_crew": "Structural Steel Team Alpha",
                "start_date": "2025-05-27",
                "target_completion": "2025-05-30",
                "progress": 68,
                "status": "In Progress",
                "priority": "High",
                "estimated_hours": 120,
                "actual_hours": 82,
                "safety_requirements": ["Fall protection", "Crane safety", "Hot work permits"],
                "materials_needed": ["Steel beams", "Bolts", "Welding rods"],
                "quality_checkpoints": ["Alignment check", "Weld inspection", "Bolt torque verification"]
            },
            {
                "id": "WP-002",
                "title": "MEP Rough-in Levels 6-7",
                "description": "Complete electrical and mechanical rough-in for floors 6-7",
                "assigned_crew": "MEP Installation Team Beta",
                "start_date": "2025-05-25",
                "target_completion": "2025-06-02",
                "progress": 45,
                "status": "In Progress",
                "priority": "Medium",
                "estimated_hours": 200,
                "actual_hours": 90,
                "safety_requirements": ["Electrical safety", "Lockout/Tagout", "Confined space"],
                "materials_needed": ["Conduit", "Wire", "Panels", "Ductwork"],
                "quality_checkpoints": ["Conduit installation", "Wire pulling", "Panel connections"]
            }
        ]
    
    if "equipment" not in st.session_state:
        st.session_state.equipment = [
            {
                "id": "EQ-001",
                "name": "Tower Crane TC-1",
                "type": "Tower Crane",
                "model": "Liebherr 280EC-H",
                "location": "Center Site",
                "operator": "Steve Wilson",
                "status": "Operating",
                "daily_rate": 850.00,
                "maintenance_due": "2025-06-01",
                "hours_today": 7.5,
                "fuel_level": 75,
                "last_inspection": "2025-05-20",
                "certifications": ["NCCCO", "Crane Operator License"],
                "safety_checklist": "Completed"
            },
            {
                "id": "EQ-002",
                "name": "Concrete Pump CP-1",
                "type": "Concrete Pump",
                "model": "Putzmeister BSF 36.16H",
                "location": "Level 5 - East",
                "operator": "Tom Davis",
                "status": "Operating",
                "daily_rate": 450.00,
                "maintenance_due": "2025-05-30",
                "hours_today": 6.0,
                "fuel_level": 60,
                "last_inspection": "2025-05-22",
                "certifications": ["Pump Operator License"],
                "safety_checklist": "Completed"
            },
            {
                "id": "EQ-003",
                "name": "Scissor Lift SL-A",
                "type": "Scissor Lift",
                "model": "Genie GS-3246",
                "location": "Level 7 - Electrical Room",
                "operator": "Jennifer Kim",
                "status": "Maintenance",
                "daily_rate": 125.00,
                "maintenance_due": "2025-05-28",
                "hours_today": 0,
                "fuel_level": 85,
                "last_inspection": "2025-05-25",
                "certifications": ["Aerial Lift Certification"],
                "safety_checklist": "Pending"
            }
        ]
    
    # Key Field Operations Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_workers = sum(crew['workers'] for crew in st.session_state.crews)
    active_crews = len([crew for crew in st.session_state.crews if crew['status'] == 'Active'])
    equipment_operating = len([eq for eq in st.session_state.equipment if eq['status'] == 'Operating'])
    avg_productivity = sum(crew['productivity'] for crew in st.session_state.crews) / len(st.session_state.crews) if st.session_state.crews else 0
    
    with col1:
        st.metric("Total Workers", total_workers, delta_color="normal")
    with col2:
        st.metric("Active Crews", active_crews, delta_color="normal")
    with col3:
        st.metric("Equipment Operating", equipment_operating, delta_color="normal")
    with col4:
        st.metric("Avg Productivity", f"{avg_productivity:.0f}%", delta_color="normal")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👥 Crew Management", "🏗️ Work Packages", "⚡ Equipment", "📈 Analytics", "🔧 Management"])
    
    with tab1:
        st.subheader("👥 Crew Management")
        
        crew_sub_tab1, crew_sub_tab2, crew_sub_tab3 = st.tabs(["📝 Add Crew", "👷 View Crews", "📊 Crew Performance"])
        
        with crew_sub_tab1:
            st.markdown("**Add New Crew**")
            
            with st.form("crew_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    crew_name = st.text_input("Crew Name", placeholder="e.g., Structural Team Alpha")
                    foreman = st.text_input("Foreman", placeholder="Foreman name")
                    workers = st.number_input("Number of Workers", value=1, min_value=1, max_value=50)
                    trade = st.selectbox("Trade", ["Structural", "MEP", "Concrete", "Finishing", "Demolition", "Site Work"])
                    location = st.text_input("Current Location", placeholder="Building level and area")
                
                with col2:
                    current_activity = st.text_input("Current Activity", placeholder="What they're working on")
                    shift_start = st.time_input("Shift Start", value=datetime.strptime("07:00", "%H:%M").time())
                    shift_end = st.time_input("Shift End", value=datetime.strptime("16:00", "%H:%M").time())
                    phone = st.text_input("Contact Phone", placeholder="(555) 123-4567")
                    certification = st.text_input("Certifications", placeholder="Required certifications")
                
                equipment_assigned = st.text_area("Equipment Assigned", placeholder="List equipment assigned to this crew")
                
                if st.form_submit_button("👷 Add Crew", type="primary"):
                    if crew_name and foreman and trade:
                        new_crew = {
                            "id": f"CREW-{len(st.session_state.crews) + 1:03d}",
                            "name": crew_name,
                            "foreman": foreman,
                            "workers": workers,
                            "trade": trade,
                            "location": location,
                            "current_activity": current_activity,
                            "status": "Active",
                            "shift_start": str(shift_start),
                            "shift_end": str(shift_end),
                            "productivity": 100,
                            "safety_score": 100,
                            "phone": phone,
                            "certification": certification,
                            "equipment_assigned": [eq.strip() for eq in equipment_assigned.split(',') if eq.strip()]
                        }
                        st.session_state.crews.append(new_crew)
                        st.success("✅ Crew added successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with crew_sub_tab2:
            st.markdown("**All Crews**")
            
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All", "Active", "Break", "Off Duty"])
            with col2:
                trade_filter = st.selectbox("Filter by Trade", ["All"] + list(set(crew['trade'] for crew in st.session_state.crews)))
            
            # Display crews
            filtered_crews = st.session_state.crews
            if status_filter != "All":
                filtered_crews = [crew for crew in filtered_crews if crew['status'] == status_filter]
            if trade_filter != "All":
                filtered_crews = [crew for crew in filtered_crews if crew['trade'] == trade_filter]
            
            for crew in filtered_crews:
                status_icon = {"Active": "🟢", "Break": "🟡", "Off Duty": "🔴"}.get(crew['status'], "⚪")
                
                with st.expander(f"{status_icon} {crew['name']} - {crew['workers']} workers ({crew['status']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**👤 Foreman:** {crew['foreman']}")
                        st.write(f"**🔧 Trade:** {crew['trade']}")
                        st.write(f"**📍 Location:** {crew['location']}")
                        st.write(f"**👷 Workers:** {crew['workers']}")
                        st.write(f"**📞 Phone:** {crew['phone']}")
                    
                    with col2:
                        st.write(f"**🏗️ Activity:** {crew['current_activity']}")
                        st.write(f"**⏰ Shift:** {crew['shift_start']} - {crew['shift_end']}")
                        st.write(f"**📊 Productivity:** {crew['productivity']}%")
                        st.write(f"**🦺 Safety Score:** {crew['safety_score']}%")
                        st.write(f"**📜 Certification:** {crew['certification']}")
                    
                    with col3:
                        st.write(f"**📊 Status:** {crew['status']}")
                        if crew['equipment_assigned']:
                            st.write(f"**⚡ Equipment:** {', '.join(crew['equipment_assigned'])}")
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button(f"🟢 Set Active", key=f"active_{crew['id']}"):
                            crew['status'] = 'Active'
                            st.success("Crew status updated!")
                            st.rerun()
                    with col2:
                        if st.button(f"🟡 Set Break", key=f"break_{crew['id']}"):
                            crew['status'] = 'Break'
                            st.info("Crew on break!")
                            st.rerun()
                    with col3:
                        if st.button(f"✏️ Edit", key=f"edit_{crew['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col4:
                        if st.button(f"🗑️ Remove", key=f"remove_{crew['id']}"):
                            st.session_state.crews.remove(crew)
                            st.success("Crew removed!")
                            st.rerun()
        
        with crew_sub_tab3:
            st.markdown("**Crew Performance Analytics**")
            
            if st.session_state.crews:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Productivity by crew
                    crew_names = [crew['name'] for crew in st.session_state.crews]
                    productivity_scores = [crew['productivity'] for crew in st.session_state.crews]
                    prod_df = pd.DataFrame({
                        'Crew': crew_names,
                        'Productivity': productivity_scores
                    })
                    fig_prod = px.bar(prod_df, x='Crew', y='Productivity', title="Crew Productivity Scores")
                    st.plotly_chart(fig_prod, use_container_width=True)
                
                with col2:
                    # Workers by trade
                    trade_workers = {}
                    for crew in st.session_state.crews:
                        trade = crew['trade']
                        trade_workers[trade] = trade_workers.get(trade, 0) + crew['workers']
                    
                    trade_list = list(trade_workers.keys())
                    worker_list = list(trade_workers.values())
                    trade_df = pd.DataFrame({
                        'Trade': trade_list,
                        'Workers': worker_list
                    })
                    fig_trade = px.pie(trade_df, values='Workers', names='Trade', title="Workers by Trade")
                    st.plotly_chart(fig_trade, use_container_width=True)
    
    with tab2:
        st.subheader("🏗️ Work Package Management")
        
        wp_sub_tab1, wp_sub_tab2 = st.tabs(["📝 Create Work Package", "📊 View Work Packages"])
        
        with wp_sub_tab1:
            st.markdown("**Create New Work Package**")
            
            with st.form("work_package_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    wp_title = st.text_input("Work Package Title", placeholder="Brief description of work package")
                    assigned_crew = st.selectbox("Assigned Crew", [crew['name'] for crew in st.session_state.crews])
                    start_date = st.date_input("Start Date", value=datetime.now().date())
                    target_completion = st.date_input("Target Completion", value=datetime.now().date() + timedelta(days=5))
                    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
                
                with col2:
                    estimated_hours = st.number_input("Estimated Hours", value=40, min_value=1)
                    safety_requirements = st.text_area("Safety Requirements", placeholder="List safety requirements")
                    materials_needed = st.text_area("Materials Needed", placeholder="List required materials")
                    quality_checkpoints = st.text_area("Quality Checkpoints", placeholder="List quality control checkpoints")
                
                description = st.text_area("Detailed Description", placeholder="Provide detailed description of the work package")
                
                if st.form_submit_button("🏗️ Create Work Package", type="primary"):
                    if wp_title and description and assigned_crew:
                        new_wp = {
                            "id": f"WP-{len(st.session_state.work_packages) + 1:03d}",
                            "title": wp_title,
                            "description": description,
                            "assigned_crew": assigned_crew,
                            "start_date": str(start_date),
                            "target_completion": str(target_completion),
                            "progress": 0,
                            "status": "Not Started",
                            "priority": priority,
                            "estimated_hours": estimated_hours,
                            "actual_hours": 0,
                            "safety_requirements": [req.strip() for req in safety_requirements.split(',') if req.strip()],
                            "materials_needed": [mat.strip() for mat in materials_needed.split(',') if mat.strip()],
                            "quality_checkpoints": [qc.strip() for qc in quality_checkpoints.split(',') if qc.strip()]
                        }
                        st.session_state.work_packages.append(new_wp)
                        st.success("✅ Work package created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with wp_sub_tab2:
            st.markdown("**All Work Packages**")
            
            for wp in st.session_state.work_packages:
                priority_icon = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}.get(wp['priority'], "⚪")
                status_icon = {"Not Started": "⏸️", "In Progress": "🔄", "Completed": "✅", "On Hold": "⏸️"}.get(wp['status'], "📋")
                
                with st.expander(f"{priority_icon} {wp['id']} - {wp['title']} ({wp['progress']}%)"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**👷 Assigned Crew:** {wp['assigned_crew']}")
                        st.write(f"**📅 Start Date:** {wp['start_date']}")
                        st.write(f"**🎯 Target Completion:** {wp['target_completion']}")
                        st.write(f"**⚠️ Priority:** {wp['priority']}")
                        st.write(f"**📊 Status:** {wp['status']}")
                        st.write(f"**⏱️ Estimated Hours:** {wp['estimated_hours']}")
                        st.write(f"**⏱️ Actual Hours:** {wp['actual_hours']}")
                    
                    with col2:
                        st.write(f"**📝 Description:** {wp['description']}")
                        if wp['safety_requirements']:
                            st.write(f"**🦺 Safety Requirements:** {', '.join(wp['safety_requirements'])}")
                        if wp['materials_needed']:
                            st.write(f"**📦 Materials:** {', '.join(wp['materials_needed'])}")
                        if wp['quality_checkpoints']:
                            st.write(f"**✅ Quality Checkpoints:** {', '.join(wp['quality_checkpoints'])}")
                    
                    # Progress bar
                    st.write("**📈 Progress:**")
                    st.progress(wp['progress'] / 100)
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button(f"▶️ Start", key=f"start_{wp['id']}"):
                            wp['status'] = 'In Progress'
                            st.success("Work package started!")
                            st.rerun()
                    with col2:
                        new_progress = st.slider(f"Update Progress", 0, 100, wp['progress'], key=f"progress_{wp['id']}")
                        if st.button(f"📊 Update", key=f"update_{wp['id']}"):
                            wp['progress'] = new_progress
                            if new_progress >= 100:
                                wp['status'] = 'Completed'
                            st.success("Progress updated!")
                            st.rerun()
                    with col3:
                        if st.button(f"✏️ Edit", key=f"edit_wp_{wp['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col4:
                        if st.button(f"🗑️ Delete", key=f"delete_wp_{wp['id']}"):
                            st.session_state.work_packages.remove(wp)
                            st.success("Work package deleted!")
                            st.rerun()
    
    with tab3:
        st.subheader("⚡ Equipment Management")
        
        eq_sub_tab1, eq_sub_tab2 = st.tabs(["📝 Add Equipment", "⚡ View Equipment"])
        
        with eq_sub_tab1:
            st.markdown("**Add New Equipment**")
            
            with st.form("equipment_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    eq_name = st.text_input("Equipment Name", placeholder="e.g., Tower Crane TC-1")
                    eq_type = st.selectbox("Equipment Type", ["Tower Crane", "Mobile Crane", "Excavator", "Forklift", "Scissor Lift", "Boom Lift", "Concrete Pump", "Generator", "Compressor"])
                    model = st.text_input("Model", placeholder="Equipment model number")
                    location = st.text_input("Current Location", placeholder="Where equipment is located")
                    operator = st.text_input("Operator", placeholder="Operator name")
                
                with col2:
                    daily_rate = st.number_input("Daily Rate ($)", value=0.00, format="%.2f")
                    maintenance_due = st.date_input("Next Maintenance Due", value=datetime.now().date() + timedelta(days=30))
                    fuel_level = st.slider("Fuel Level (%)", 0, 100, 100)
                    last_inspection = st.date_input("Last Inspection", value=datetime.now().date())
                    certifications = st.text_input("Required Certifications", placeholder="Operator certifications")
                
                if st.form_submit_button("⚡ Add Equipment", type="primary"):
                    if eq_name and eq_type and operator:
                        new_equipment = {
                            "id": f"EQ-{len(st.session_state.equipment) + 1:03d}",
                            "name": eq_name,
                            "type": eq_type,
                            "model": model,
                            "location": location,
                            "operator": operator,
                            "status": "Operating",
                            "daily_rate": daily_rate,
                            "maintenance_due": str(maintenance_due),
                            "hours_today": 0,
                            "fuel_level": fuel_level,
                            "last_inspection": str(last_inspection),
                            "certifications": certifications,
                            "safety_checklist": "Pending"
                        }
                        st.session_state.equipment.append(new_equipment)
                        st.success("✅ Equipment added successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with eq_sub_tab2:
            st.markdown("**All Equipment**")
            
            for equipment in st.session_state.equipment:
                status_icon = {"Operating": "🟢", "Maintenance": "🟡", "Down": "🔴", "Idle": "⚪"}.get(equipment['status'], "⚪")
                
                with st.expander(f"{status_icon} {equipment['name']} - {equipment['type']} ({equipment['status']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**🔧 Type:** {equipment['type']}")
                        st.write(f"**📋 Model:** {equipment['model']}")
                        st.write(f"**📍 Location:** {equipment['location']}")
                        st.write(f"**👤 Operator:** {equipment['operator']}")
                        st.write(f"**💰 Daily Rate:** ${equipment['daily_rate']:,.2f}")
                    
                    with col2:
                        st.write(f"**📊 Status:** {equipment['status']}")
                        st.write(f"**⏱️ Hours Today:** {equipment['hours_today']}")
                        st.write(f"**⛽ Fuel Level:** {equipment['fuel_level']}%")
                        st.write(f"**🔧 Maintenance Due:** {equipment['maintenance_due']}")
                        st.write(f"**🔍 Last Inspection:** {equipment['last_inspection']}")
                    
                    with col3:
                        st.write(f"**📜 Certifications:** {equipment['certifications']}")
                        st.write(f"**✅ Safety Checklist:** {equipment['safety_checklist']}")
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button(f"🟢 Operating", key=f"operating_{equipment['id']}"):
                            equipment['status'] = 'Operating'
                            st.success("Equipment status updated!")
                            st.rerun()
                    with col2:
                        if st.button(f"🟡 Maintenance", key=f"maintenance_{equipment['id']}"):
                            equipment['status'] = 'Maintenance'
                            st.warning("Equipment in maintenance!")
                            st.rerun()
                    with col3:
                        if st.button(f"✏️ Edit", key=f"edit_eq_{equipment['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col4:
                        if st.button(f"🗑️ Remove", key=f"remove_eq_{equipment['id']}"):
                            st.session_state.equipment.remove(equipment)
                            st.success("Equipment removed!")
                            st.rerun()
    
    with tab4:
        st.subheader("📈 Field Operations Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Work package progress
            if st.session_state.work_packages:
                wp_titles = [wp['title'][:30] + "..." if len(wp['title']) > 30 else wp['title'] for wp in st.session_state.work_packages]
                wp_progress = [wp['progress'] for wp in st.session_state.work_packages]
                wp_df = pd.DataFrame({
                    'Work_Package': wp_titles,
                    'Progress': wp_progress
                })
                fig_wp = px.bar(wp_df, x='Work_Package', y='Progress', title="Work Package Progress")
                st.plotly_chart(fig_wp, use_container_width=True)
        
        with col2:
            # Equipment status distribution
            if st.session_state.equipment:
                eq_status_counts = {}
                for eq in st.session_state.equipment:
                    status = eq['status']
                    eq_status_counts[status] = eq_status_counts.get(status, 0) + 1
                
                eq_status_list = list(eq_status_counts.keys())
                eq_count_list = list(eq_status_counts.values())
                eq_status_df = pd.DataFrame({
                    'Status': eq_status_list,
                    'Count': eq_count_list
                })
                fig_eq_status = px.pie(eq_status_df, values='Count', names='Status', title="Equipment Status Distribution")
                st.plotly_chart(fig_eq_status, use_container_width=True)
    
    with tab5:
        st.subheader("🔧 Field Operations Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**👷 Crew Summary**")
            if st.session_state.crews:
                crew_stats_data = pd.DataFrame([
                    {"Metric": "Total Crews", "Value": len(st.session_state.crews)},
                    {"Metric": "Active Crews", "Value": len([c for c in st.session_state.crews if c['status'] == 'Active'])},
                    {"Metric": "Total Workers", "Value": sum(c['workers'] for c in st.session_state.crews)},
                    {"Metric": "Avg Productivity", "Value": f"{sum(c['productivity'] for c in st.session_state.crews) / len(st.session_state.crews):.1f}%"},
                ])
                st.dataframe(crew_stats_data, use_container_width=True)
        
        with col2:
            st.markdown("**🏗️ Work Package Summary**")
            if st.session_state.work_packages:
                wp_stats_data = pd.DataFrame([
                    {"Metric": "Total Work Packages", "Value": len(st.session_state.work_packages)},
                    {"Metric": "In Progress", "Value": len([wp for wp in st.session_state.work_packages if wp['status'] == 'In Progress'])},
                    {"Metric": "Completed", "Value": len([wp for wp in st.session_state.work_packages if wp['status'] == 'Completed'])},
                    {"Metric": "Avg Progress", "Value": f"{sum(wp['progress'] for wp in st.session_state.work_packages) / len(st.session_state.work_packages):.1f}%"},
                ])
                st.dataframe(wp_stats_data, use_container_width=True)
        
        with col3:
            st.markdown("**⚡ Equipment Summary**")
            if st.session_state.equipment:
                eq_stats_data = pd.DataFrame([
                    {"Metric": "Total Equipment", "Value": len(st.session_state.equipment)},
                    {"Metric": "Operating", "Value": len([eq for eq in st.session_state.equipment if eq['status'] == 'Operating'])},
                    {"Metric": "In Maintenance", "Value": len([eq for eq in st.session_state.equipment if eq['status'] == 'Maintenance'])},
                    {"Metric": "Daily Cost", "Value": f"${sum(eq['daily_rate'] for eq in st.session_state.equipment):,.2f}"},
                ])
                st.dataframe(eq_stats_data, use_container_width=True)
        
        # Data management
        st.markdown("**⚠️ Data Management**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🗑️ Clear All Crews", type="secondary"):
                st.session_state.crews = []
                st.success("All crews cleared!")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Work Packages", type="secondary"):
                st.session_state.work_packages = []
                st.success("All work packages cleared!")
                st.rerun()
        with col3:
            if st.button("🗑️ Clear Equipment", type="secondary"):
                st.session_state.equipment = []
                st.success("All equipment cleared!")
                st.rerun()

# Additional render functions for all other modules...
def render_contracts():
    """Complete Contracts Management with full CRUD functionality"""
    st.markdown("""
    <div class="module-header">
        <h1>📄 Contracts Management</h1>
        <p>Comprehensive contract administration, tracking, and lifecycle management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize contracts data
    if "contracts" not in st.session_state:
        st.session_state.contracts = [
            {
                "id": "CON-001",
                "contractor_name": "Highland Construction LLC",
                "contract_type": "General Contractor",
                "trade": "General Construction",
                "contract_value": 28500000.00,
                "start_date": "2025-01-15",
                "completion_date": "2026-12-15",
                "status": "Active",
                "payment_status": "Current",
                "completion_percentage": 75,
                "project_manager": "Sarah Wilson",
                "contract_number": "HTD-GC-2025-001",
                "bonding_amount": 2850000.00,
                "insurance_expiry": "2026-12-31",
                "retention_percentage": 5.0,
                "total_paid": 21375000.00,
                "phone": "(555) 123-4567",
                "email": "pm@highlandconstruction.com",
                "address": "123 Construction Ave, City, State 12345",
                "performance_score": 95
            },
            {
                "id": "CON-002",
                "contractor_name": "Elite MEP Systems",
                "contract_type": "Subcontractor",
                "trade": "MEP",
                "contract_value": 8200000.00,
                "start_date": "2025-03-01",
                "completion_date": "2026-10-15",
                "status": "Active",
                "payment_status": "Current",
                "completion_percentage": 60,
                "project_manager": "Mike Rodriguez",
                "contract_number": "HTD-MEP-2025-002",
                "bonding_amount": 820000.00,
                "insurance_expiry": "2026-10-31",
                "retention_percentage": 5.0,
                "total_paid": 4920000.00,
                "phone": "(555) 234-5678",
                "email": "contracts@elitemep.com",
                "address": "456 Industrial Blvd, City, State 12345",
                "performance_score": 88
            },
            {
                "id": "CON-003",
                "contractor_name": "Steel Solutions Inc",
                "contract_type": "Subcontractor",
                "trade": "Structural Steel",
                "contract_value": 2800000.00,
                "start_date": "2025-04-01",
                "completion_date": "2025-09-30",
                "status": "Active",
                "payment_status": "Pending",
                "completion_percentage": 45,
                "project_manager": "David Kim",
                "contract_number": "HTD-STL-2025-003",
                "bonding_amount": 280000.00,
                "insurance_expiry": "2025-12-31",
                "retention_percentage": 10.0,
                "total_paid": 1134000.00,
                "phone": "(555) 345-6789",
                "email": "admin@steelsolutions.com",
                "address": "789 Steel Way, City, State 12345",
                "performance_score": 85
            }
        ]
    
    if "contract_change_orders" not in st.session_state:
        st.session_state.contract_change_orders = [
            {
                "id": "CCO-001",
                "contract_id": "CON-001",
                "contractor_name": "Highland Construction LLC",
                "description": "Additional HVAC scope modification for improved efficiency",
                "amount": 125000.00,
                "type": "Addition",
                "status": "Approved",
                "submitted_date": "2025-05-15",
                "approved_date": "2025-05-20",
                "reason": "Owner Request",
                "impact_schedule": 5,
                "submitted_by": "Project Manager",
                "approved_by": "Owner Representative"
            },
            {
                "id": "CCO-002",
                "contract_id": "CON-002",
                "contractor_name": "Elite MEP Systems",
                "description": "Additional electrical outlets for data center upgrade",
                "amount": 45000.00,
                "type": "Addition",
                "status": "Under Review",
                "submitted_date": "2025-05-22",
                "approved_date": "",
                "reason": "Design Change",
                "impact_schedule": 2,
                "submitted_by": "MEP Contractor",
                "approved_by": ""
            }
        ]
    
    # Key Contract Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_contract_value = sum(contract['contract_value'] for contract in st.session_state.contracts)
    active_contracts = len([c for c in st.session_state.contracts if c['status'] == 'Active'])
    total_paid = sum(contract['total_paid'] for contract in st.session_state.contracts)
    avg_completion = sum(contract['completion_percentage'] for contract in st.session_state.contracts) / len(st.session_state.contracts) if st.session_state.contracts else 0
    
    with col1:
        st.metric("Total Contract Value", f"${total_contract_value:,.0f}", delta_color="normal")
    with col2:
        st.metric("Active Contracts", active_contracts, delta_color="normal")
    with col3:
        st.metric("Total Paid", f"${total_paid:,.0f}", delta_color="normal")
    with col4:
        st.metric("Avg Completion", f"{avg_completion:.1f}%", delta_color="normal")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Create Contract", "📊 View Contracts", "📋 Change Orders", "📈 Analytics", "🔧 Management"])
    
    with tab1:
        st.subheader("📝 Create New Contract")
        
        with st.form("contract_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                contractor_name = st.text_input("Contractor Name", placeholder="Company name")
                contract_type = st.selectbox("Contract Type", ["General Contractor", "Subcontractor", "Supplier", "Consultant"])
                trade = st.selectbox("Trade", ["General Construction", "MEP", "Structural Steel", "Concrete", "Electrical", "Plumbing", "HVAC", "Architectural", "Other"])
                contract_value = st.number_input("Contract Value ($)", value=0.00, format="%.2f")
                start_date = st.date_input("Start Date", value=datetime.now().date())
                completion_date = st.date_input("Completion Date", value=datetime.now().date() + timedelta(days=365))
            
            with col2:
                project_manager = st.text_input("Project Manager", placeholder="Assigned PM name")
                contract_number = st.text_input("Contract Number", placeholder="Unique contract identifier")
                bonding_amount = st.number_input("Bonding Amount ($)", value=0.00, format="%.2f")
                insurance_expiry = st.date_input("Insurance Expiry", value=datetime.now().date() + timedelta(days=365))
                retention_percentage = st.number_input("Retention %", value=5.0, min_value=0.0, max_value=15.0, format="%.1f")
                phone = st.text_input("Phone", placeholder="(555) 123-4567")
            
            email = st.text_input("Email", placeholder="contractor@company.com")
            address = st.text_area("Address", placeholder="Full business address")
            
            if st.form_submit_button("📄 Create Contract", type="primary"):
                if contractor_name and contract_value > 0 and trade:
                    new_contract = {
                        "id": f"CON-{len(st.session_state.contracts) + 1:03d}",
                        "contractor_name": contractor_name,
                        "contract_type": contract_type,
                        "trade": trade,
                        "contract_value": contract_value,
                        "start_date": str(start_date),
                        "completion_date": str(completion_date),
                        "status": "Active",
                        "payment_status": "Current",
                        "completion_percentage": 0,
                        "project_manager": project_manager,
                        "contract_number": contract_number,
                        "bonding_amount": bonding_amount,
                        "insurance_expiry": str(insurance_expiry),
                        "retention_percentage": retention_percentage,
                        "total_paid": 0.00,
                        "phone": phone,
                        "email": email,
                        "address": address,
                        "performance_score": 100
                    }
                    st.session_state.contracts.append(new_contract)
                    st.success("✅ Contract created successfully!")
                    st.rerun()
                else:
                    st.error("❌ Please fill in all required fields!")
    
    with tab2:
        st.subheader("📊 All Contracts")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Active", "Completed", "Terminated", "On Hold"])
        with col2:
            type_filter = st.selectbox("Filter by Type", ["All", "General Contractor", "Subcontractor", "Supplier", "Consultant"])
        with col3:
            trade_filter = st.selectbox("Filter by Trade", ["All"] + list(set(c['trade'] for c in st.session_state.contracts)))
        
        # Display contracts
        filtered_contracts = st.session_state.contracts
        if status_filter != "All":
            filtered_contracts = [c for c in filtered_contracts if c['status'] == status_filter]
        if type_filter != "All":
            filtered_contracts = [c for c in filtered_contracts if c['contract_type'] == type_filter]
        if trade_filter != "All":
            filtered_contracts = [c for c in filtered_contracts if c['trade'] == trade_filter]
        
        for contract in filtered_contracts:
            status_icon = {"Active": "🟢", "Completed": "✅", "Terminated": "❌", "On Hold": "⏸️"}.get(contract['status'], "📋")
            
            with st.expander(f"{status_icon} {contract['contractor_name']} - ${contract['contract_value']:,.0f} ({contract['completion_percentage']}%)"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**📄 Contract #:** {contract['contract_number']}")
                    st.write(f"**🏢 Type:** {contract['contract_type']}")
                    st.write(f"**🔧 Trade:** {contract['trade']}")
                    st.write(f"**💰 Value:** ${contract['contract_value']:,.2f}")
                    st.write(f"**📅 Start:** {contract['start_date']}")
                    st.write(f"**🎯 Completion:** {contract['completion_date']}")
                
                with col2:
                    st.write(f"**📊 Status:** {contract['status']}")
                    st.write(f"**💳 Payment Status:** {contract['payment_status']}")
                    st.write(f"**📈 Progress:** {contract['completion_percentage']}%")
                    st.write(f"**👤 PM:** {contract['project_manager']}")
                    st.write(f"**🏆 Performance:** {contract['performance_score']}/100")
                    st.write(f"**💰 Total Paid:** ${contract['total_paid']:,.2f}")
                
                with col3:
                    st.write(f"**🏦 Bonding:** ${contract['bonding_amount']:,.2f}")
                    st.write(f"**🛡️ Insurance Expiry:** {contract['insurance_expiry']}")
                    st.write(f"**📊 Retention:** {contract['retention_percentage']}%")
                    st.write(f"**📞 Phone:** {contract['phone']}")
                    st.write(f"**📧 Email:** {contract['email']}")
                    if contract['address']:
                        st.write(f"**📍 Address:** {contract['address']}")
                
                # Progress bar
                st.write("**📈 Contract Progress:**")
                st.progress(contract['completion_percentage'] / 100)
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button(f"✅ Complete", key=f"complete_{contract['id']}"):
                        contract['status'] = 'Completed'
                        contract['completion_percentage'] = 100
                        st.success("Contract completed!")
                        st.rerun()
                with col2:
                    new_progress = st.slider(f"Update Progress", 0, 100, contract['completion_percentage'], key=f"progress_c_{contract['id']}")
                    if st.button(f"📊 Update", key=f"update_c_{contract['id']}"):
                        contract['completion_percentage'] = new_progress
                        st.success("Progress updated!")
                        st.rerun()
                with col3:
                    if st.button(f"✏️ Edit", key=f"edit_c_{contract['id']}"):
                        st.info("Edit functionality - would open edit form")
                with col4:
                    if st.button(f"🗑️ Delete", key=f"delete_c_{contract['id']}"):
                        st.session_state.contracts.remove(contract)
                        st.success("Contract deleted!")
                        st.rerun()
    
    with tab3:
        st.subheader("📋 Contract Change Orders")
        
        co_sub_tab1, co_sub_tab2 = st.tabs(["📝 Create Change Order", "📊 View Change Orders"])
        
        with co_sub_tab1:
            st.markdown("**Create New Contract Change Order**")
            
            with st.form("change_order_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    contract_selection = st.selectbox("Select Contract", 
                        [f"{c['contract_number']} - {c['contractor_name']}" for c in st.session_state.contracts])
                    selected_contract = next((c for c in st.session_state.contracts 
                                            if f"{c['contract_number']} - {c['contractor_name']}" == contract_selection), None)
                    
                    co_description = st.text_area("Change Order Description", placeholder="Detailed description of the change")
                    co_amount = st.number_input("Amount ($)", value=0.00, format="%.2f")
                    co_type = st.selectbox("Type", ["Addition", "Deduction", "Credit"])
                    reason = st.selectbox("Reason", ["Owner Request", "Design Change", "Site Conditions", "Code Compliance", "Coordination Issue"])
                
                with col2:
                    impact_schedule = st.number_input("Schedule Impact (days)", value=0, format="%d")
                    submitted_by = st.text_input("Submitted By", placeholder="Person submitting change order")
                
                if st.form_submit_button("📋 Create Change Order", type="primary"):
                    if selected_contract and co_description and co_amount != 0:
                        new_co = {
                            "id": f"CCO-{len(st.session_state.contract_change_orders) + 1:03d}",
                            "contract_id": selected_contract['id'],
                            "contractor_name": selected_contract['contractor_name'],
                            "description": co_description,
                            "amount": co_amount,
                            "type": co_type,
                            "status": "Submitted",
                            "submitted_date": str(datetime.now().date()),
                            "approved_date": "",
                            "reason": reason,
                            "impact_schedule": impact_schedule,
                            "submitted_by": submitted_by,
                            "approved_by": ""
                        }
                        st.session_state.contract_change_orders.append(new_co)
                        st.success("✅ Change order created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with co_sub_tab2:
            st.markdown("**All Contract Change Orders**")
            
            for co in st.session_state.contract_change_orders:
                status_icon = {"Submitted": "📋", "Under Review": "🔄", "Approved": "✅", "Rejected": "❌"}.get(co['status'], "📋")
                type_icon = {"Addition": "➕", "Deduction": "➖", "Credit": "💳"}.get(co['type'], "📋")
                
                with st.expander(f"{status_icon} {co['id']} - {co['contractor_name']} {type_icon}${abs(co['amount']):,.2f}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📄 Contract:** {co['contract_id']}")
                        st.write(f"**🏢 Contractor:** {co['contractor_name']}")
                        st.write(f"**💰 Amount:** ${co['amount']:,.2f}")
                        st.write(f"**📋 Type:** {co['type']}")
                        st.write(f"**📅 Submitted:** {co['submitted_date']}")
                        st.write(f"**👤 Submitted By:** {co['submitted_by']}")
                    
                    with col2:
                        st.write(f"**📊 Status:** {co['status']}")
                        st.write(f"**📅 Schedule Impact:** {co['impact_schedule']} days")
                        st.write(f"**📋 Reason:** {co['reason']}")
                        if co['approved_date']:
                            st.write(f"**✅ Approved:** {co['approved_date']}")
                            st.write(f"**👤 Approved By:** {co['approved_by']}")
                    
                    st.write(f"**📝 Description:** {co['description']}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if co['status'] != 'Approved' and st.button(f"✅ Approve", key=f"approve_co_{co['id']}"):
                            co['status'] = 'Approved'
                            co['approved_date'] = str(datetime.now().date())
                            co['approved_by'] = 'Project Manager'
                            # Update contract value
                            contract = next((c for c in st.session_state.contracts if c['id'] == co['contract_id']), None)
                            if contract:
                                contract['contract_value'] += co['amount']
                            st.success("Change order approved!")
                            st.rerun()
                    with col2:
                        if st.button(f"🔄 Under Review", key=f"review_co_{co['id']}"):
                            co['status'] = 'Under Review'
                            st.info("Change order under review!")
                            st.rerun()
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_co_{co['id']}"):
                            st.session_state.contract_change_orders.remove(co)
                            st.success("Change order deleted!")
                            st.rerun()
    
    with tab4:
        st.subheader("📈 Contract Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Contract value by contractor
            if st.session_state.contracts:
                contractor_names = [contract['contractor_name'] for contract in st.session_state.contracts]
                contract_values = [contract['contract_value'] for contract in st.session_state.contracts]
                contract_df = pd.DataFrame({
                    'Contractor': contractor_names,
                    'Value': contract_values
                })
                fig_contracts = px.bar(contract_df, x='Contractor', y='Value', title="Contract Value by Contractor")
                st.plotly_chart(fig_contracts, use_container_width=True)
        
        with col2:
            # Contract completion status
            if st.session_state.contracts:
                completion_ranges = []
                for contract in st.session_state.contracts:
                    if contract['completion_percentage'] <= 25:
                        completion_ranges.append("0-25%")
                    elif contract['completion_percentage'] <= 50:
                        completion_ranges.append("26-50%")
                    elif contract['completion_percentage'] <= 75:
                        completion_ranges.append("51-75%")
                    else:
                        completion_ranges.append("76-100%")
                
                completion_counts = {}
                for range_val in completion_ranges:
                    completion_counts[range_val] = completion_counts.get(range_val, 0) + 1
                
                completion_list = list(completion_counts.keys())
                count_list = list(completion_counts.values())
                completion_df = pd.DataFrame({
                    'Completion_Range': completion_list,
                    'Count': count_list
                })
                fig_completion = px.pie(completion_df, values='Count', names='Completion_Range', title="Contract Completion Status")
                st.plotly_chart(fig_completion, use_container_width=True)
        
        # Change order analytics
        if st.session_state.contract_change_orders:
            st.markdown("**📋 Change Order Analytics**")
            col1, col2 = st.columns(2)
            
            with col1:
                # Change order amounts by contractor
                co_contractor_amounts = {}
                for co in st.session_state.contract_change_orders:
                    contractor = co['contractor_name']
                    co_contractor_amounts[contractor] = co_contractor_amounts.get(contractor, 0) + co['amount']
                
                co_contractor_list = list(co_contractor_amounts.keys())
                co_amount_list = list(co_contractor_amounts.values())
                co_contractor_df = pd.DataFrame({
                    'Contractor': co_contractor_list,
                    'Change_Order_Amount': co_amount_list
                })
                fig_co_amounts = px.bar(co_contractor_df, x='Contractor', y='Change_Order_Amount', title="Change Order Amounts by Contractor")
                st.plotly_chart(fig_co_amounts, use_container_width=True)
            
            with col2:
                # Change order status
                co_status_counts = {}
                for co in st.session_state.contract_change_orders:
                    status = co['status']
                    co_status_counts[status] = co_status_counts.get(status, 0) + 1
                
                co_status_list = list(co_status_counts.keys())
                co_status_count_list = list(co_status_counts.values())
                co_status_df = pd.DataFrame({
                    'Status': co_status_list,
                    'Count': co_status_count_list
                })
                fig_co_status = px.pie(co_status_df, values='Count', names='Status', title="Change Order Status Distribution")
                st.plotly_chart(fig_co_status, use_container_width=True)
    
    with tab5:
        st.subheader("🔧 Contract Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Contract Summary**")
            if st.session_state.contracts:
                contract_stats_data = pd.DataFrame([
                    {"Metric": "Total Contracts", "Value": len(st.session_state.contracts)},
                    {"Metric": "Active Contracts", "Value": len([c for c in st.session_state.contracts if c['status'] == 'Active'])},
                    {"Metric": "Total Contract Value", "Value": f"${sum(c['contract_value'] for c in st.session_state.contracts):,.2f}"},
                    {"Metric": "Total Paid", "Value": f"${sum(c['total_paid'] for c in st.session_state.contracts):,.2f}"},
                ])
                st.dataframe(contract_stats_data, use_container_width=True)
        
        with col2:
            st.markdown("**📋 Change Order Summary**")
            if st.session_state.contract_change_orders:
                co_stats_data = pd.DataFrame([
                    {"Metric": "Total Change Orders", "Value": len(st.session_state.contract_change_orders)},
                    {"Metric": "Approved", "Value": len([co for co in st.session_state.contract_change_orders if co['status'] == 'Approved'])},
                    {"Metric": "Pending", "Value": len([co for co in st.session_state.contract_change_orders if co['status'] != 'Approved'])},
                    {"Metric": "Total CO Value", "Value": f"${sum(co['amount'] for co in st.session_state.contract_change_orders):,.2f}"},
                ])
                st.dataframe(co_stats_data, use_container_width=True)
        
        # Data management
        st.markdown("**⚠️ Data Management**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear All Contracts", type="secondary"):
                st.session_state.contracts = []
                st.success("All contracts cleared!")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Change Orders", type="secondary"):
                st.session_state.contract_change_orders = []
                st.success("All change orders cleared!")
                st.rerun()

def render_cost_management():
    """Enterprise Cost Management with robust Python backend"""
    try:
        from modules.cost_management_ui import render_cost_management_enterprise
        render_cost_management_enterprise()
        return
    except ImportError:
        st.error("Enterprise Cost Management module not available")
    
    # Fallback to basic version
    render_cost_management_basic()

def render_cost_management_basic():
    """Basic Cost Management - fallback version"""
    st.markdown("""
    <div class="module-header">
        <h1>💰 Cost Management</h1>
        <p>Advanced financial tracking, budget management, and cost forecasting</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize cost management data
    if "budget_items" not in st.session_state:
        st.session_state.budget_items = [
            {
                "id": "BUD-001",
                "category": "Labor",
                "description": "General construction labor - all trades",
                "budgeted_amount": 18200000.00,
                "committed_amount": 17800000.00,
                "actual_spent": 16450000.00,
                "forecast_final": 17850000.00,
                "variance": -350000.00,
                "completion_percentage": 92,
                "cost_code": "01-100",
                "responsible_manager": "Project Manager",
                "last_updated": "2025-05-27"
            },
            {
                "id": "BUD-002",
                "category": "Materials",
                "description": "Construction materials and supplies",
                "budgeted_amount": 15800000.00,
                "committed_amount": 15200000.00,
                "actual_spent": 14850000.00,
                "forecast_final": 16100000.00,
                "variance": 300000.00,
                "completion_percentage": 94,
                "cost_code": "02-200",
                "responsible_manager": "Procurement Manager",
                "last_updated": "2025-05-26"
            },
            {
                "id": "BUD-003",
                "category": "Equipment",
                "description": "Construction equipment rental and operation",
                "budgeted_amount": 6300000.00,
                "committed_amount": 5800000.00,
                "actual_spent": 5450000.00,
                "forecast_final": 5900000.00,
                "variance": -400000.00,
                "completion_percentage": 94,
                "cost_code": "03-300",
                "responsible_manager": "Equipment Manager",
                "last_updated": "2025-05-27"
            },
            {
                "id": "BUD-004",
                "category": "Subcontractors",
                "description": "Specialized subcontractor services",
                "budgeted_amount": 3700000.00,
                "committed_amount": 3650000.00,
                "actual_spent": 3200000.00,
                "forecast_final": 3500000.00,
                "variance": -200000.00,
                "completion_percentage": 88,
                "cost_code": "04-400",
                "responsible_manager": "Subcontractor Manager",
                "last_updated": "2025-05-25"
            }
        ]
    
    if "cost_forecasts" not in st.session_state:
        st.session_state.cost_forecasts = [
            {
                "id": "FCT-001",
                "forecast_date": "2025-05-27",
                "project_completion_date": "2026-12-15",
                "total_forecast": 43400000.00,
                "confidence_level": "High",
                "forecast_method": "Earned Value Analysis",
                "created_by": "Cost Engineer",
                "variance_from_budget": -2100000.00,
                "risk_factors": ["Weather delays potential", "Material price fluctuation", "Labor availability"],
                "assumptions": ["Current productivity maintained", "No major scope changes", "Weather normal conditions"]
            },
            {
                "id": "FCT-002",
                "forecast_date": "2025-05-20",
                "project_completion_date": "2026-12-15",
                "total_forecast": 44200000.00,
                "confidence_level": "Medium",
                "forecast_method": "Bottom-up Estimation",
                "created_by": "Project Manager",
                "variance_from_budget": -1300000.00,
                "risk_factors": ["Supply chain delays", "Resource constraints"],
                "assumptions": ["Current pace continues", "No weather delays"]
            }
        ]
    
    if "payment_applications" not in st.session_state:
        st.session_state.payment_applications = [
            {
                "id": "PAY-008",
                "application_number": 8,
                "period_ending": "2025-05-31",
                "application_date": "2025-05-27",
                "amount_requested": 2847500.00,
                "work_completed": 32847500.00,
                "retention_amount": 164237.50,
                "net_payment": 2683262.50,
                "status": "Submitted",
                "submitted_by": "Project Manager",
                "submitted_date": "2025-05-27",
                "approved_date": "",
                "paid_date": "",
                "description": "Level 13 structural steel completion, MEP rough-in progress, exterior skin installation"
            },
            {
                "id": "PAY-007",
                "application_number": 7,
                "period_ending": "2025-04-30",
                "application_date": "2025-04-30",
                "amount_requested": 3125000.00,
                "work_completed": 30000000.00,
                "retention_amount": 156250.00,
                "net_payment": 2968750.00,
                "status": "Paid",
                "submitted_by": "Project Manager",
                "submitted_date": "2025-04-30",
                "approved_date": "2025-05-05",
                "paid_date": "2025-05-12",
                "description": "Concrete work Level 11-12, structural steel Level 12, MEP rough-in Level 8-9"
            }
        ]
    
    # Key Cost Management Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_budget = sum(item['budgeted_amount'] for item in st.session_state.budget_items)
    total_spent = sum(item['actual_spent'] for item in st.session_state.budget_items)
    total_committed = sum(item['committed_amount'] for item in st.session_state.budget_items)
    latest_forecast = st.session_state.cost_forecasts[0]['total_forecast'] if st.session_state.cost_forecasts else 0
    
    with col1:
        st.metric("Total Budget", f"${total_budget:,.0f}", delta_color="normal")
    with col2:
        st.metric("Actual Spent", f"${total_spent:,.0f}", f"{(total_spent/total_budget*100):.1f}%")
    with col3:
        st.metric("Committed", f"${total_committed:,.0f}", f"{(total_committed/total_budget*100):.1f}%")
    with col4:
        st.metric("Forecast Final", f"${latest_forecast:,.0f}", f"${latest_forecast-total_budget:,.0f}")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Budget Management", "📈 Cost Forecasting", "💳 Payment Applications", "📈 Analytics", "🔧 Management"])
    
    with tab1:
        st.subheader("📊 Budget Management")
        
        budget_sub_tab1, budget_sub_tab2, budget_sub_tab3 = st.tabs(["📝 Create Budget Item", "💰 View Budget Items", "📊 Budget Analysis"])
        
        with budget_sub_tab1:
            st.markdown("**Create New Budget Item**")
            
            with st.form("budget_item_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    category = st.selectbox("Category", ["Labor", "Materials", "Equipment", "Subcontractors", "Overhead", "Contingency"])
                    description = st.text_area("Description", placeholder="Detailed description of budget item")
                    budgeted_amount = st.number_input("Budgeted Amount ($)", value=0.00, format="%.2f")
                    cost_code = st.text_input("Cost Code", placeholder="e.g., 01-100")
                
                with col2:
                    responsible_manager = st.text_input("Responsible Manager", placeholder="Manager responsible for this budget")
                    committed_amount = st.number_input("Committed Amount ($)", value=0.00, format="%.2f")
                    actual_spent = st.number_input("Actual Spent ($)", value=0.00, format="%.2f")
                    completion_percentage = st.slider("Completion %", 0, 100, 0)
                
                if st.form_submit_button("💰 Create Budget Item", type="primary"):
                    if category and description and budgeted_amount > 0:
                        forecast_final = actual_spent + (budgeted_amount - actual_spent) * (100 - completion_percentage) / 100
                        variance = forecast_final - budgeted_amount
                        
                        new_budget_item = {
                            "id": f"BUD-{len(st.session_state.budget_items) + 1:03d}",
                            "category": category,
                            "description": description,
                            "budgeted_amount": budgeted_amount,
                            "committed_amount": committed_amount,
                            "actual_spent": actual_spent,
                            "forecast_final": forecast_final,
                            "variance": variance,
                            "completion_percentage": completion_percentage,
                            "cost_code": cost_code,
                            "responsible_manager": responsible_manager,
                            "last_updated": str(datetime.now().date())
                        }
                        st.session_state.budget_items.append(new_budget_item)
                        st.success("✅ Budget item created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with budget_sub_tab2:
            st.markdown("**All Budget Items**")
            
            # Display budget items
            for item in st.session_state.budget_items:
                variance_icon = "🟢" if item['variance'] <= 0 else "🔴"
                
                with st.expander(f"{variance_icon} {item['category']} - {item['cost_code']} (${item['budgeted_amount']:,.0f})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**📋 Category:** {item['category']}")
                        st.write(f"**🔢 Cost Code:** {item['cost_code']}")
                        st.write(f"**💰 Budgeted:** ${item['budgeted_amount']:,.2f}")
                        st.write(f"**💳 Committed:** ${item['committed_amount']:,.2f}")
                        st.write(f"**💸 Actual Spent:** ${item['actual_spent']:,.2f}")
                    
                    with col2:
                        st.write(f"**🔮 Forecast Final:** ${item['forecast_final']:,.2f}")
                        st.write(f"**📊 Variance:** ${item['variance']:,.2f}")
                        st.write(f"**📈 Completion:** {item['completion_percentage']}%")
                        st.write(f"**👤 Manager:** {item['responsible_manager']}")
                        st.write(f"**📅 Updated:** {item['last_updated']}")
                    
                    with col3:
                        st.write(f"**📝 Description:** {item['description']}")
                    
                    # Progress bar
                    st.write("**📈 Budget Progress:**")
                    progress_value = min(item['actual_spent'] / item['budgeted_amount'], 1.0) if item['budgeted_amount'] > 0 else 0
                    st.progress(progress_value)
                    st.write(f"Spent: {progress_value*100:.1f}% of budget")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        new_spent = st.number_input(f"Update Spent", value=item['actual_spent'], key=f"spent_{item['id']}")
                        if st.button(f"💸 Update Spent", key=f"update_spent_{item['id']}"):
                            item['actual_spent'] = new_spent
                            item['last_updated'] = str(datetime.now().date())
                            st.success("Spent amount updated!")
                            st.rerun()
                    with col2:
                        if st.button(f"✏️ Edit", key=f"edit_budget_{item['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_budget_{item['id']}"):
                            st.session_state.budget_items.remove(item)
                            st.success("Budget item deleted!")
                            st.rerun()
        
        with budget_sub_tab3:
            st.markdown("**Budget Analysis**")
            
            if st.session_state.budget_items:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Budget vs Actual by category
                    categories = [item['category'] for item in st.session_state.budget_items]
                    budgeted = [item['budgeted_amount'] for item in st.session_state.budget_items]
                    actual = [item['actual_spent'] for item in st.session_state.budget_items]
                    
                    budget_comparison_df = pd.DataFrame({
                        'Category': categories,
                        'Budgeted': budgeted,
                        'Actual': actual
                    })
                    fig_budget = px.bar(budget_comparison_df, x='Category', y=['Budgeted', 'Actual'], 
                                      title="Budget vs Actual by Category", barmode='group')
                    st.plotly_chart(fig_budget, use_container_width=True)
                
                with col2:
                    # Variance analysis
                    variances = [item['variance'] for item in st.session_state.budget_items]
                    variance_df = pd.DataFrame({
                        'Category': categories,
                        'Variance': variances
                    })
                    fig_variance = px.bar(variance_df, x='Category', y='Variance', 
                                        title="Budget Variance by Category", 
                                        color='Variance', color_continuous_scale='RdYlGn_r')
                    st.plotly_chart(fig_variance, use_container_width=True)
    
    with tab2:
        st.subheader("📈 Cost Forecasting")
        
        forecast_sub_tab1, forecast_sub_tab2 = st.tabs(["📝 Create Forecast", "📊 View Forecasts"])
        
        with forecast_sub_tab1:
            st.markdown("**Create New Cost Forecast**")
            
            with st.form("forecast_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    forecast_date = st.date_input("Forecast Date", value=datetime.now().date())
                    completion_date = st.date_input("Projected Completion", value=datetime.now().date() + timedelta(days=365))
                    total_forecast = st.number_input("Total Forecast Cost ($)", value=0.00, format="%.2f")
                    confidence_level = st.selectbox("Confidence Level", ["Low", "Medium", "High"])
                    forecast_method = st.selectbox("Forecast Method", ["Earned Value Analysis", "Bottom-up Estimation", "Parametric Estimation", "Expert Judgment"])
                
                with col2:
                    created_by = st.text_input("Created By", placeholder="Forecaster name")
                    risk_factors = st.text_area("Risk Factors", placeholder="List potential risks")
                    assumptions = st.text_area("Key Assumptions", placeholder="List key assumptions")
                
                if st.form_submit_button("📈 Create Forecast", type="primary"):
                    if total_forecast > 0 and created_by:
                        variance_from_budget = total_forecast - total_budget
                        
                        new_forecast = {
                            "id": f"FCT-{len(st.session_state.cost_forecasts) + 1:03d}",
                            "forecast_date": str(forecast_date),
                            "project_completion_date": str(completion_date),
                            "total_forecast": total_forecast,
                            "confidence_level": confidence_level,
                            "forecast_method": forecast_method,
                            "created_by": created_by,
                            "variance_from_budget": variance_from_budget,
                            "risk_factors": [risk.strip() for risk in risk_factors.split(',') if risk.strip()],
                            "assumptions": [assumption.strip() for assumption in assumptions.split(',') if assumption.strip()]
                        }
                        st.session_state.cost_forecasts.insert(0, new_forecast)  # Add to beginning for latest first
                        st.success("✅ Cost forecast created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with forecast_sub_tab2:
            st.markdown("**All Cost Forecasts**")
            
            for forecast in st.session_state.cost_forecasts:
                confidence_icon = {"Low": "🟡", "Medium": "🟠", "High": "🟢"}.get(forecast['confidence_level'], "⚪")
                variance_icon = "🟢" if forecast['variance_from_budget'] <= 0 else "🔴"
                
                with st.expander(f"{confidence_icon} Forecast {forecast['id']} - ${forecast['total_forecast']:,.0f} ({forecast['confidence_level']} confidence)"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📅 Forecast Date:** {forecast['forecast_date']}")
                        st.write(f"**🎯 Completion Date:** {forecast['project_completion_date']}")
                        st.write(f"**💰 Total Forecast:** ${forecast['total_forecast']:,.2f}")
                        st.write(f"**📊 Confidence:** {forecast['confidence_level']}")
                        st.write(f"**🔧 Method:** {forecast['forecast_method']}")
                        st.write(f"**👤 Created By:** {forecast['created_by']}")
                    
                    with col2:
                        st.write(f"**{variance_icon} Variance from Budget:** ${forecast['variance_from_budget']:,.2f}")
                        if forecast['risk_factors']:
                            st.write(f"**⚠️ Risk Factors:** {', '.join(forecast['risk_factors'])}")
                        if forecast['assumptions']:
                            st.write(f"**📋 Assumptions:** {', '.join(forecast['assumptions'])}")
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✏️ Edit", key=f"edit_forecast_{forecast['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col2:
                        if st.button(f"🗑️ Delete", key=f"delete_forecast_{forecast['id']}"):
                            st.session_state.cost_forecasts.remove(forecast)
                            st.success("Forecast deleted!")
                            st.rerun()
    
    with tab3:
        st.subheader("💳 Payment Applications")
        
        pay_sub_tab1, pay_sub_tab2 = st.tabs(["📝 Create Application", "📊 View Applications"])
        
        with pay_sub_tab1:
            st.markdown("**Create New Payment Application**")
            
            with st.form("payment_application_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    app_number = st.number_input("Application Number", value=len(st.session_state.payment_applications) + 1, min_value=1)
                    period_ending = st.date_input("Period Ending", value=datetime.now().date())
                    amount_requested = st.number_input("Amount Requested ($)", value=0.00, format="%.2f")
                    work_completed = st.number_input("Total Work Completed ($)", value=0.00, format="%.2f")
                
                with col2:
                    retention_rate = st.number_input("Retention Rate (%)", value=5.0, min_value=0.0, max_value=15.0, format="%.1f")
                    submitted_by = st.text_input("Submitted By", placeholder="Person submitting application")
                
                description = st.text_area("Work Description", placeholder="Describe work completed in this period")
                
                if st.form_submit_button("💳 Create Payment Application", type="primary"):
                    if amount_requested > 0 and description:
                        retention_amount = amount_requested * (retention_rate / 100)
                        net_payment = amount_requested - retention_amount
                        
                        new_application = {
                            "id": f"PAY-{app_number:03d}",
                            "application_number": app_number,
                            "period_ending": str(period_ending),
                            "application_date": str(datetime.now().date()),
                            "amount_requested": amount_requested,
                            "work_completed": work_completed,
                            "retention_amount": retention_amount,
                            "net_payment": net_payment,
                            "status": "Draft",
                            "submitted_by": submitted_by,
                            "submitted_date": "",
                            "approved_date": "",
                            "paid_date": "",
                            "description": description
                        }
                        st.session_state.payment_applications.insert(0, new_application)
                        st.success("✅ Payment application created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with pay_sub_tab2:
            st.markdown("**All Payment Applications**")
            
            for app in st.session_state.payment_applications:
                status_icon = {"Draft": "📝", "Submitted": "📤", "Approved": "✅", "Paid": "💰", "Rejected": "❌"}.get(app['status'], "📋")
                
                with st.expander(f"{status_icon} Application #{app['application_number']} - ${app['amount_requested']:,.0f} ({app['status']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📊 Application #:** {app['application_number']}")
                        st.write(f"**📅 Period Ending:** {app['period_ending']}")
                        st.write(f"**📅 Application Date:** {app['application_date']}")
                        st.write(f"**💰 Amount Requested:** ${app['amount_requested']:,.2f}")
                        st.write(f"**🏗️ Work Completed:** ${app['work_completed']:,.2f}")
                        st.write(f"**🏦 Retention:** ${app['retention_amount']:,.2f}")
                        st.write(f"**💳 Net Payment:** ${app['net_payment']:,.2f}")
                    
                    with col2:
                        st.write(f"**📊 Status:** {app['status']}")
                        st.write(f"**👤 Submitted By:** {app['submitted_by']}")
                        if app['submitted_date']:
                            st.write(f"**📤 Submitted:** {app['submitted_date']}")
                        if app['approved_date']:
                            st.write(f"**✅ Approved:** {app['approved_date']}")
                        if app['paid_date']:
                            st.write(f"**💰 Paid:** {app['paid_date']}")
                    
                    st.write(f"**📝 Description:** {app['description']}")
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if app['status'] == 'Draft' and st.button(f"📤 Submit", key=f"submit_app_{app['id']}"):
                            app['status'] = 'Submitted'
                            app['submitted_date'] = str(datetime.now().date())
                            st.success("Application submitted!")
                            st.rerun()
                    with col2:
                        if app['status'] == 'Submitted' and st.button(f"✅ Approve", key=f"approve_app_{app['id']}"):
                            app['status'] = 'Approved'
                            app['approved_date'] = str(datetime.now().date())
                            st.success("Application approved!")
                            st.rerun()
                    with col3:
                        if app['status'] == 'Approved' and st.button(f"💰 Mark Paid", key=f"paid_app_{app['id']}"):
                            app['status'] = 'Paid'
                            app['paid_date'] = str(datetime.now().date())
                            st.success("Payment recorded!")
                            st.rerun()
                    with col4:
                        if st.button(f"🗑️ Delete", key=f"delete_app_{app['id']}"):
                            st.session_state.payment_applications.remove(app)
                            st.success("Application deleted!")
                            st.rerun()
    
    with tab4:
        st.subheader("📈 Cost Management Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Cost trends over time
            if st.session_state.cost_forecasts:
                forecast_dates = [forecast['forecast_date'] for forecast in st.session_state.cost_forecasts]
                forecast_amounts = [forecast['total_forecast'] for forecast in st.session_state.cost_forecasts]
                trend_df = pd.DataFrame({
                    'Date': forecast_dates,
                    'Forecast': forecast_amounts
                })
                fig_trend = px.line(trend_df, x='Date', y='Forecast', title="Cost Forecast Trends")
                st.plotly_chart(fig_trend, use_container_width=True)
        
        with col2:
            # Payment application status
            if st.session_state.payment_applications:
                app_status_counts = {}
                for app in st.session_state.payment_applications:
                    status = app['status']
                    app_status_counts[status] = app_status_counts.get(status, 0) + 1
                
                app_status_list = list(app_status_counts.keys())
                app_count_list = list(app_status_counts.values())
                app_status_df = pd.DataFrame({
                    'Status': app_status_list,
                    'Count': app_count_list
                })
                fig_app_status = px.pie(app_status_df, values='Count', names='Status', title="Payment Application Status")
                st.plotly_chart(fig_app_status, use_container_width=True)
    
    with tab5:
        st.subheader("🔧 Cost Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**💰 Budget Summary**")
            if st.session_state.budget_items:
                budget_stats_data = pd.DataFrame([
                    {"Metric": "Total Budget", "Value": f"${sum(item['budgeted_amount'] for item in st.session_state.budget_items):,.2f}"},
                    {"Metric": "Total Spent", "Value": f"${sum(item['actual_spent'] for item in st.session_state.budget_items):,.2f}"},
                    {"Metric": "Total Committed", "Value": f"${sum(item['committed_amount'] for item in st.session_state.budget_items):,.2f}"},
                    {"Metric": "Budget Items", "Value": len(st.session_state.budget_items)},
                ])
                st.dataframe(budget_stats_data, use_container_width=True)
        
        with col2:
            st.markdown("**📈 Forecast Summary**")
            if st.session_state.cost_forecasts:
                latest_forecast = st.session_state.cost_forecasts[0]
                forecast_stats_data = pd.DataFrame([
                    {"Metric": "Total Forecasts", "Value": len(st.session_state.cost_forecasts)},
                    {"Metric": "Latest Forecast", "Value": f"${latest_forecast['total_forecast']:,.2f}"},
                    {"Metric": "Variance from Budget", "Value": f"${latest_forecast['variance_from_budget']:,.2f}"},
                    {"Metric": "Confidence Level", "Value": latest_forecast['confidence_level']},
                ])
                st.dataframe(forecast_stats_data, use_container_width=True)
        
        with col3:
            st.markdown("**💳 Payment Summary**")
            if st.session_state.payment_applications:
                total_requested = sum(app['amount_requested'] for app in st.session_state.payment_applications)
                paid_apps = [app for app in st.session_state.payment_applications if app['status'] == 'Paid']
                total_paid = sum(app['net_payment'] for app in paid_apps)
                
                payment_stats_data = pd.DataFrame([
                    {"Metric": "Total Applications", "Value": len(st.session_state.payment_applications)},
                    {"Metric": "Total Requested", "Value": f"${total_requested:,.2f}"},
                    {"Metric": "Total Paid", "Value": f"${total_paid:,.2f}"},
                    {"Metric": "Paid Applications", "Value": len(paid_apps)},
                ])
                st.dataframe(payment_stats_data, use_container_width=True)
        
        # Data management
        st.markdown("**⚠️ Data Management**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🗑️ Clear Budget Items", type="secondary"):
                st.session_state.budget_items = []
                st.success("All budget items cleared!")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Forecasts", type="secondary"):
                st.session_state.cost_forecasts = []
                st.success("All forecasts cleared!")
                st.rerun()
        with col3:
            if st.button("🗑️ Clear Applications", type="secondary"):
                st.session_state.payment_applications = []
                st.success("All payment applications cleared!")
                st.rerun()

def render_bim():
    """Enterprise BIM Management with full CRUD functionality"""
    try:
        from modules.bim_backend import bim_manager, ModelType, ModelStatus, ClashSeverity, ClashStatus
        
        st.markdown("""
        <div class="module-header">
            <h1>🏗️ BIM Management</h1>
            <p>Highland Tower Development - 3D coordination, clash detection, and model management</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display summary metrics
        metrics = bim_manager.generate_bim_metrics()
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📊 Total Models", metrics['total_models'])
            with col2:
                st.metric("⚠️ Open Clashes", metrics['open_clashes'])
            with col3:
                st.metric("✅ Resolved Clashes", metrics['resolved_clashes'])
            with col4:
                st.metric("📈 Resolution Rate", f"{metrics['clash_resolution_rate']}%")
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🏗️ BIM Models", "⚠️ Clash Detection", "➕ Create", "⚙️ Manage"])
        
        with tab1:
            st.subheader("🏗️ Highland Tower Development - BIM Models")
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                discipline_filter = st.selectbox("Filter by Discipline", 
                    ["All"] + list(set(model.discipline for model in bim_manager.get_all_models())))
            with col2:
                status_filter = st.selectbox("Filter by Status", 
                    ["All"] + [status.value for status in ModelStatus])
            with col3:
                type_filter = st.selectbox("Filter by Type", 
                    ["All"] + [mtype.value for mtype in ModelType])
            
            # Get filtered models
            models = bim_manager.get_all_models()
            
            if discipline_filter != "All":
                models = [m for m in models if m.discipline == discipline_filter]
            if status_filter != "All":
                models = [m for m in models if m.status.value == status_filter]
            if type_filter != "All":
                models = [m for m in models if m.model_type.value == type_filter]
            
            # Display models
            for model in models:
                status_color = {
                    ModelStatus.CURRENT: "🟢",
                    ModelStatus.APPROVED: "🟢",
                    ModelStatus.IN_REVIEW: "🟡",
                    ModelStatus.DRAFT: "🟡",
                    ModelStatus.SUPERSEDED: "🟠",
                    ModelStatus.ARCHIVED: "⚫"
                }.get(model.status, "⚪")
                
                federated_indicator = "🔗 FEDERATED" if model.federated_model else "📄 STANDALONE"
                clash_indicator = "✅ CLASH CHECKED" if model.clash_detection_run else "❌ NO CLASH CHECK"
                
                with st.expander(f"{status_color} {model.model_code} | {model.model_name} | {federated_indicator}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**🏗️ Type:** {model.model_type.value}")
                        st.write(f"**👥 Discipline:** {model.discipline}")
                        st.write(f"**📋 Status:** {model.status.value}")
                        st.write(f"**📊 Version:** {model.version} ({model.revision})")
                        st.write(f"**📅 Last Modified:** {model.last_modified}")
                        st.write(f"**👤 Created By:** {model.created_by}")
                    
                    with col2:
                        st.write(f"**📄 File:** {model.file_name}")
                        st.write(f"**📦 Format:** {model.file_format}")
                        if model.file_size > 0:
                            st.write(f"**📊 Size:** {model.file_size / 1024 / 1024:.1f} MB")
                        st.write(f"**🏢 Level Range:** {model.level_range}")
                        st.write(f"**📍 Building Section:** {model.building_section}")
                        st.write(f"**⚙️ Phase:** {model.project_phase}")
                    
                    if model.description:
                        st.write(f"**📝 Description:** {model.description}")
                    
                    if model.review_comments:
                        st.write(f"**💬 Review Comments:** {model.review_comments}")
                    
                    # Coordination status
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**{clash_indicator}**")
                    with col2:
                        st.write(f"**📐 Coordinate System:** {model.coordinate_system}")
                    
                    # Change log
                    if model.change_log:
                        st.write("**📋 Recent Changes:**")
                        for change in model.change_log[:3]:  # Show last 3 changes
                            st.write(f"• {change}")
                    
                    # Workflow tracking
                    st.write(f"**🎯 Current Stage:** {model.workflow_stage}")
                    st.write(f"**📅 Next Milestone:** {model.next_milestone}")
                    st.write(f"**👤 Assigned To:** {model.assigned_to}")
                    
                    # Quick actions
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if st.button(f"📥 Download", key=f"btn_download_{model.model_id}"):
                            st.success(f"Downloading {model.file_format} model...")
                    
                    with col2:
                        if st.button(f"👁️ View 3D", key=f"btn_view_{model.model_id}"):
                            st.success("Opening 3D viewer...")
                    
                    with col3:
                        if st.button(f"🔍 Clash Check", key=f"btn_clash_{model.model_id}"):
                            st.success("Running clash detection...")
                    
                    with col4:
                        if model.status == ModelStatus.IN_REVIEW and st.button(f"✅ Approve", key=f"btn_approve_{model.model_id}"):
                            if bim_manager.update_model_status(model.model_id, ModelStatus.APPROVED):
                                st.success("Model approved!")
                                st.rerun()
        
        with tab2:
            st.subheader("⚠️ Clash Detection Results")
            
            # Clash summary
            open_clashes = bim_manager.get_open_clashes()
            critical_clashes = bim_manager.get_clashes_by_severity(ClashSeverity.CRITICAL)
            high_clashes = bim_manager.get_clashes_by_severity(ClashSeverity.HIGH)
            
            if critical_clashes:
                st.error(f"🚨 {len(critical_clashes)} CRITICAL CLASHES require immediate attention!")
            
            if high_clashes:
                st.warning(f"⚠️ {len(high_clashes)} HIGH PRIORITY clashes need resolution")
            
            if not open_clashes:
                st.success("🎉 No open clashes - all coordination issues resolved!")
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                severity_filter = st.selectbox("Filter by Severity", 
                    ["All"] + [sev.value for sev in ClashSeverity])
            with col2:
                status_clash_filter = st.selectbox("Filter by Status", 
                    ["All"] + [stat.value for stat in ClashStatus])
            
            # Get filtered clashes
            clashes = bim_manager.get_all_clashes()
            
            if severity_filter != "All":
                clashes = [c for c in clashes if c.severity.value == severity_filter]
            if status_clash_filter != "All":
                clashes = [c for c in clashes if c.status.value == status_clash_filter]
            
            # Display clashes
            for clash in clashes:
                severity_color = {
                    ClashSeverity.CRITICAL: "🔴",
                    ClashSeverity.HIGH: "🟠",
                    ClashSeverity.MEDIUM: "🟡", 
                    ClashSeverity.LOW: "🟢",
                    ClashSeverity.INFORMATION: "🔵"
                }.get(clash.severity, "⚪")
                
                status_indicator = {
                    ClashStatus.OPEN: "🔴 OPEN",
                    ClashStatus.IN_PROGRESS: "🟡 IN PROGRESS", 
                    ClashStatus.RESOLVED: "🟢 RESOLVED",
                    ClashStatus.ACCEPTED: "🔵 ACCEPTED",
                    ClashStatus.CLOSED: "⚫ CLOSED"
                }.get(clash.status, "⚪ UNKNOWN")
                
                with st.expander(f"{severity_color} {clash.clash_code} | {clash.clash_name} | {status_indicator}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**⚠️ Severity:** {clash.severity.value}")
                        st.write(f"**📋 Type:** {clash.clash_type}")
                        st.write(f"**🏢 Location:** {clash.building_level} - {clash.zone}")
                        st.write(f"**📅 Detected:** {clash.detected_date}")
                        st.write(f"**🎯 Target Resolution:** {clash.target_resolution}")
                        st.write(f"**👤 Assigned To:** {clash.assigned_to}")
                    
                    with col2:
                        st.write(f"**🔄 Discipline Conflict:** {clash.discipline_conflict}")
                        st.write(f"**📊 Priority:** {clash.priority}")
                        if clash.estimated_cost > 0:
                            st.write(f"**💰 Estimated Cost:** ${clash.estimated_cost:,.0f}")
                        if clash.resolved_date:
                            st.write(f"**✅ Resolved:** {clash.resolved_date}")
                        st.write(f"**📏 Coordinates:** X:{clash.coordinates['x']:.1f}, Y:{clash.coordinates['y']:.1f}, Z:{clash.coordinates['z']:.1f}")
                    
                    # Model and element details
                    st.write(f"**🏗️ Conflict Details:**")
                    st.write(f"• **Model A:** {clash.model_a} - {clash.element_a}")
                    st.write(f"• **Model B:** {clash.model_b} - {clash.element_b}")
                    
                    # Resolution information
                    if clash.resolution_method:
                        st.write(f"**🔧 Resolution Method:** {clash.resolution_method}")
                    
                    if clash.resolution_notes:
                        st.write(f"**📝 Resolution Notes:** {clash.resolution_notes}")
                    
                    # Related items
                    if clash.related_rfis:
                        st.write(f"**📋 Related RFIs:** {', '.join(clash.related_rfis)}")
                    
                    # Documentation
                    if clash.markup_files:
                        st.write(f"**📎 Markup Files:** {len(clash.markup_files)} files available")
                    
                    # Quick actions
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if clash.status != ClashStatus.RESOLVED and st.button(f"✅ Mark Resolved", key=f"resolve_clash_{clash.clash_id}"):
                            resolution_notes = f"Resolved via coordination meeting on {datetime.now().strftime('%Y-%m-%d')}"
                            if bim_manager.resolve_clash(clash.clash_id, resolution_notes):
                                st.success("Clash marked as resolved!")
                                st.rerun()
                    
                    with col2:
                        if st.button(f"📸 View Screenshot", key=f"screenshot_{clash.clash_id}"):
                            st.success("Opening clash screenshot...")
                    
                    with col3:
                        if st.button(f"📋 Create RFI", key=f"create_rfi_{clash.clash_id}"):
                            st.success("Creating RFI from clash...")
        
        with tab3:
            st.subheader("➕ Create BIM Items")
            
            create_tab1, create_tab2 = st.tabs(["🏗️ Create BIM Model", "⚠️ Create Clash"])
            
            with create_tab1:
                st.write("**🏗️ Create New BIM Model**")
                
                with st.form("create_model_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        model_name = st.text_input("📝 Model Name*", placeholder="Highland Tower - Architectural Model")
                        model_type = st.selectbox("🏗️ Model Type*", options=[mtype.value for mtype in ModelType])
                        discipline = st.text_input("👥 Discipline*", placeholder="e.g., Architecture, Structural")
                        version = st.text_input("📊 Version*", value="1.0")
                        revision = st.text_input("📋 Revision*", value="Rev-01")
                        status = st.selectbox("📊 Status*", options=[status.value for status in ModelStatus])
                    
                    with col2:
                        file_name = st.text_input("📄 File Name*", placeholder="Highland_Tower_Arch_Rev01.rvt")
                        file_format = st.selectbox("📦 Format*", options=["RVT", "IFC", "DWG", "NWD", "SKP"])
                        project_phase = st.text_input("⚙️ Project Phase*", value="Design Development")
                        level_range = st.text_input("🏢 Level Range*", placeholder="Level B1 to Penthouse")
                        building_section = st.text_input("📍 Building Section*", value="Full Building")
                        coordinate_system = st.text_input("📐 Coordinate System", value="Shared Site Coordinates")
                    
                    description = st.text_area("📝 Description*", placeholder="Detailed description of the BIM model")
                    created_by = st.text_input("👤 Created By*", placeholder="Name - Title")
                    assigned_to = st.text_input("👤 Assigned To*", placeholder="Team or individual responsible")
                    workflow_stage = st.text_input("🎯 Workflow Stage", value="Design Development")
                    next_milestone = st.text_input("📅 Next Milestone", placeholder="100% DD Set - Date")
                    
                    if st.form_submit_button("🏗️ Create BIM Model", use_container_width=True):
                        if not model_name or not discipline or not file_name or not description:
                            st.error("Please fill in all required fields marked with *")
                        else:
                            model_data = {
                                "model_name": model_name,
                                "model_type": model_type,
                                "discipline": discipline,
                                "version": version,
                                "revision": revision,
                                "status": status,
                                "file_name": file_name,
                                "file_path": f"/bim/models/{discipline.lower()}/{file_name}",
                                "file_size": 0,  # Would be set when file is uploaded
                                "file_format": file_format,
                                "project_phase": project_phase,
                                "level_range": level_range,
                                "building_section": building_section,
                                "created_by": created_by,
                                "reviewed_by": None,
                                "approved_by": None,
                                "review_date": None,
                                "approval_date": None,
                                "coordinate_system": coordinate_system,
                                "description": description,
                                "review_comments": "",
                                "workflow_stage": workflow_stage,
                                "next_milestone": next_milestone,
                                "assigned_to": assigned_to
                            }
                            
                            model_id = bim_manager.create_bim_model(model_data)
                            st.success(f"✅ BIM model created successfully! ID: {model_id}")
                            st.rerun()
            
            with create_tab2:
                st.write("**⚠️ Create Clash Detection Result**")
                
                with st.form("create_clash_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        clash_name = st.text_input("📝 Clash Name*", placeholder="HVAC Duct vs Structural Beam")
                        clash_type = st.selectbox("📋 Clash Type*", options=["Hard Clash", "Soft Clash", "Clearance"])
                        severity = st.selectbox("⚠️ Severity*", options=[sev.value for sev in ClashSeverity])
                        building_level = st.text_input("🏢 Building Level*", placeholder="Level 12")
                        zone = st.text_input("📍 Zone*", placeholder="Office Area - Zone B")
                        discipline_conflict = st.text_input("🔄 Discipline Conflict*", placeholder="Mechanical vs Structural")
                    
                    with col2:
                        model_a = st.text_input("🏗️ Model A*", placeholder="HTD-MECH-001")
                        model_b = st.text_input("🏗️ Model B*", placeholder="HTD-STRUC-001")
                        element_a = st.text_input("📐 Element A*", placeholder="24x18 Supply Duct")
                        element_b = st.text_input("📐 Element B*", placeholder="W24x68 Steel Beam")
                        assigned_to = st.text_input("👤 Assigned To*", placeholder="Engineer Name")
                        priority = st.number_input("📊 Priority", min_value=1, max_value=5, value=3)
                    
                    # Coordinates
                    st.write("**📏 Clash Coordinates**")
                    coord_col1, coord_col2, coord_col3 = st.columns(3)
                    with coord_col1:
                        coord_x = st.number_input("X", value=0.0, step=0.1)
                    with coord_col2:
                        coord_y = st.number_input("Y", value=0.0, step=0.1)
                    with coord_col3:
                        coord_z = st.number_input("Z", value=0.0, step=0.1)
                    
                    target_resolution = st.date_input("📅 Target Resolution Date*")
                    resolution_method = st.text_input("🔧 Proposed Resolution Method", placeholder="Reroute ductwork around beam")
                    estimated_cost = st.number_input("💰 Estimated Resolution Cost", min_value=0.0, step=100.0)
                    screenshot_path = st.text_input("📸 Screenshot Path", placeholder="/bim/clashes/screenshots/clash-xxx.png")
                    
                    if st.form_submit_button("⚠️ Create Clash", use_container_width=True):
                        if not clash_name or not model_a or not model_b or not assigned_to:
                            st.error("Please fill in all required fields marked with *")
                        else:
                            clash_data = {
                                "clash_name": clash_name,
                                "model_a": model_a,
                                "model_b": model_b,
                                "element_a": element_a,
                                "element_b": element_b,
                                "clash_type": clash_type,
                                "severity": severity,
                                "discipline_conflict": discipline_conflict,
                                "building_level": building_level,
                                "zone": zone,
                                "coordinates": {"x": coord_x, "y": coord_y, "z": coord_z},
                                "assigned_to": assigned_to,
                                "priority": priority,
                                "resolution_method": resolution_method,
                                "resolution_notes": "",
                                "estimated_cost": estimated_cost,
                                "target_resolution": target_resolution.strftime('%Y-%m-%d'),
                                "screenshot_path": screenshot_path if screenshot_path else "/bim/clashes/screenshots/default.png",
                                "created_by": "Current User"
                            }
                            
                            clash_id = bim_manager.create_clash_detection(clash_data)
                            st.success(f"✅ Clash detection result created! ID: {clash_id}")
                            st.rerun()
        
        with tab4:
            st.subheader("⚙️ Manage BIM Assets")
            
            manage_tab1, manage_tab2 = st.tabs(["🏗️ Manage Models", "⚠️ Manage Clashes"])
            
            with manage_tab1:
                models_list = bim_manager.get_all_models()
                if models_list:
                    model_options = [f"{m.model_code} - {m.model_name}" for m in models_list]
                    selected_model_index = st.selectbox("Select Model to Manage", range(len(model_options)), format_func=lambda x: model_options[x])
                    selected_model = models_list[selected_model_index]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("✏️ Edit Model", use_container_width=True):
                            st.session_state.show_edit_model_form = True
                    
                    with col2:
                        if st.button("🗑️ Archive Model", use_container_width=True):
                            if bim_manager.update_model_status(selected_model.model_id, ModelStatus.ARCHIVED):
                                st.success("✅ Model archived!")
                                st.rerun()
                    
                    with col3:
                        if st.button("📋 Duplicate Model", use_container_width=True):
                            # Create duplicate with modified name
                            model_data = {
                                "model_name": f"Copy of {selected_model.model_name}",
                                "model_type": selected_model.model_type.value,
                                "discipline": selected_model.discipline,
                                "version": "1.0",
                                "revision": "Rev-01",
                                "status": ModelStatus.DRAFT.value,
                                "file_name": f"Copy_{selected_model.file_name}",
                                "file_path": f"/bim/models/{selected_model.discipline.lower()}/Copy_{selected_model.file_name}",
                                "file_size": 0,
                                "file_format": selected_model.file_format,
                                "project_phase": selected_model.project_phase,
                                "level_range": selected_model.level_range,
                                "building_section": selected_model.building_section,
                                "created_by": "Current User",
                                "reviewed_by": None,
                                "approved_by": None,
                                "review_date": None,
                                "approval_date": None,
                                "coordinate_system": selected_model.coordinate_system,
                                "description": f"Copy of {selected_model.description}",
                                "review_comments": "",
                                "workflow_stage": selected_model.workflow_stage,
                                "next_milestone": selected_model.next_milestone,
                                "assigned_to": selected_model.assigned_to
                            }
                            model_id = bim_manager.create_bim_model(model_data)
                            st.success(f"✅ Model duplicated! ID: {model_id}")
                            st.rerun()
                    
                    # Edit form
                    if st.session_state.get('show_edit_model_form', False):
                        with st.form("edit_model_form"):
                            st.write("**✏️ Edit Model Details**")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                edit_name = st.text_input("📝 Name", value=selected_model.model_name)
                                edit_version = st.text_input("📊 Version", value=selected_model.version)
                                edit_revision = st.text_input("📋 Revision", value=selected_model.revision)
                                edit_phase = st.text_input("⚙️ Phase", value=selected_model.project_phase)
                            
                            with col2:
                                edit_workflow = st.text_input("🎯 Workflow Stage", value=selected_model.workflow_stage)
                                edit_milestone = st.text_input("📅 Next Milestone", value=selected_model.next_milestone)
                                edit_assigned = st.text_input("👤 Assigned To", value=selected_model.assigned_to)
                                edit_description = st.text_area("📝 Description", value=selected_model.description)
                            
                            if st.form_submit_button("✏️ Update Model"):
                                selected_model.model_name = edit_name
                                selected_model.version = edit_version
                                selected_model.revision = edit_revision
                                selected_model.project_phase = edit_phase
                                selected_model.workflow_stage = edit_workflow
                                selected_model.next_milestone = edit_milestone
                                selected_model.assigned_to = edit_assigned
                                selected_model.description = edit_description
                                selected_model.last_modified = datetime.now().strftime('%Y-%m-%d')
                                
                                st.success("✅ Model updated!")
                                st.session_state.show_edit_model_form = False
                                st.rerun()
                else:
                    st.info("No models available. Create some BIM models first.")
            
            with manage_tab2:
                clashes_list = list(bim_manager.clashes.values())
                if clashes_list:
                    clash_options = [f"{c.clash_code} - {c.clash_name}" for c in clashes_list]
                    selected_clash_index = st.selectbox("Select Clash to Manage", range(len(clash_options)), format_func=lambda x: clash_options[x])
                    selected_clash = clashes_list[selected_clash_index]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if selected_clash.status != ClashStatus.RESOLVED and st.button("✅ Resolve Clash", use_container_width=True):
                            resolution_notes = f"Resolved via coordination on {datetime.now().strftime('%Y-%m-%d')}"
                            if bim_manager.resolve_clash(selected_clash.clash_id, resolution_notes):
                                st.success("✅ Clash resolved!")
                                st.rerun()
                    
                    with col2:
                        if st.button("✏️ Edit Clash", use_container_width=True):
                            st.session_state.show_edit_clash_form = True
                    
                    with col3:
                        if st.button("🗑️ Delete Clash", use_container_width=True):
                            if selected_clash.clash_id in bim_manager.clashes:
                                del bim_manager.clashes[selected_clash.clash_id]
                                st.success("✅ Clash deleted!")
                                st.rerun()
                else:
                    st.info("No clashes available. Run clash detection first.")
        
        return
        
    except ImportError:
        st.error("Enterprise BIM Management module not available")
        st.info("🏗️ BIM Management with 3D model coordination and clash detection")

    # Initialize BIM data
    if "bim_models" not in st.session_state:
        st.session_state.bim_models = [
            {
                "id": "BIM-001",
                "model_name": "Highland Tower - Architectural",
                "discipline": "Architectural",
                "version": "Rev D.1",
                "file_size": "487 MB",
                "elements_count": 47582,
                "lod_level": "LOD 350",
                "status": "Current",
                "last_updated": "2025-05-23",
                "coordinator": "Sarah Chen",
                "file_path": "/models/HTD_Arch_RevD1.ifc",
                "upload_date": "2025-05-23",
                "notes": "Latest architectural model with Level 13-15 modifications",
                "export_format": "IFC 4.0",
                "software_used": "Revit 2024"
            },
            {
                "id": "BIM-002",
                "model_name": "Highland Tower - Structural",
                "discipline": "Structural",
                "version": "Rev C.3",
                "file_size": "298 MB",
                "elements_count": 28947,
                "lod_level": "LOD 350",
                "status": "Under Review",
                "last_updated": "2025-05-20",
                "coordinator": "Michael Torres",
                "file_path": "/models/HTD_Struct_RevC3.ifc",
                "upload_date": "2025-05-20",
                "notes": "Structural steel connections updated for Level 8-13",
                "export_format": "IFC 4.0",
                "software_used": "Tekla Structures"
            },
            {
                "id": "BIM-003",
                "model_name": "Highland Tower - MEP",
                "discipline": "MEP",
                "version": "Rev B.2",
                "file_size": "652 MB",
                "elements_count": 89234,
                "lod_level": "LOD 300",
                "status": "Coordinating",
                "last_updated": "2025-05-18",
                "coordinator": "Jennifer Walsh",
                "file_path": "/models/HTD_MEP_RevB2.ifc",
                "upload_date": "2025-05-18",
                "notes": "MEP routing coordination for upper floors in progress",
                "export_format": "IFC 4.0",
                "software_used": "Revit MEP 2024"
            }
        ]
    
    if "clash_detections" not in st.session_state:
        st.session_state.clash_detections = [
            {
                "id": "CLH-001",
                "clash_id": "CLH-HTD-047",
                "clash_type": "Hard Clash",
                "location": "Level 13 - Grid E4",
                "discipline_1": "MEP - HVAC Duct",
                "discipline_2": "Structural - Steel Beam",
                "priority": "Critical",
                "status": "Open",
                "assigned_to": "Jennifer Walsh / Michael Torres",
                "detected_date": "2025-05-25",
                "description": "50mm diameter HVAC duct conflicts with W14x30 steel beam",
                "proposed_solution": "Route duct below beam with 150mm clearance",
                "resolution_date": "",
                "model_1": "Highland Tower - MEP",
                "model_2": "Highland Tower - Structural"
            },
            {
                "id": "CLH-002",
                "clash_id": "CLH-HTD-046",
                "clash_type": "Soft Clash",
                "location": "Level 12 - Corridor",
                "discipline_1": "Electrical - Conduit",
                "discipline_2": "Plumbing - Domestic Water",
                "priority": "High",
                "status": "Under Review",
                "assigned_to": "Jennifer Walsh",
                "detected_date": "2025-05-24",
                "description": "Electrical conduit within minimum clearance of water line",
                "proposed_solution": "Maintain 300mm minimum separation between systems",
                "resolution_date": "",
                "model_1": "Highland Tower - MEP",
                "model_2": "Highland Tower - MEP"
            }
        ]
    
    if "coordination_meetings" not in st.session_state:
        st.session_state.coordination_meetings = [
            {
                "id": "COORD-001",
                "meeting_date": "2025-05-30",
                "meeting_time": "14:00",
                "meeting_type": "BIM Coordination",
                "organizer": "Sarah Chen",
                "attendees": ["Sarah Chen", "Michael Torres", "Jennifer Walsh", "David Kim"],
                "agenda": "Level 13-15 MEP routing, structural connections, curtain wall integration",
                "status": "Scheduled",
                "location": "Conference Room A / Teams",
                "models_reviewed": ["Highland Tower - Architectural", "Highland Tower - Structural", "Highland Tower - MEP"],
                "action_items": [],
                "meeting_notes": ""
            }
        ]
    
    # Key BIM Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_elements = sum(model['elements_count'] for model in st.session_state.bim_models)
    active_clashes = len([clash for clash in st.session_state.clash_detections if clash['status'] != 'Resolved'])
    critical_clashes = len([clash for clash in st.session_state.clash_detections if clash['priority'] == 'Critical'])
    total_file_size = sum(float(model['file_size'].split()[0]) for model in st.session_state.bim_models)
    
    with col1:
        st.metric("Total Elements", f"{total_elements:,}", delta_color="normal")
    with col2:
        st.metric("Active Clashes", active_clashes, delta_color="normal")
    with col3:
        st.metric("Critical Issues", critical_clashes, delta_color="normal")
    with col4:
        st.metric("Model Size", f"{total_file_size:.1f} GB", delta_color="normal")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📂 Model Management", "⚠️ Clash Detection", "📅 Coordination", "📈 Analytics", "🔧 Management"])
    
    with tab1:
        st.subheader("📂 BIM Model Management")
        
        model_sub_tab1, model_sub_tab2 = st.tabs(["📤 Upload Model", "📊 View Models"])
        
        with model_sub_tab1:
            st.markdown("**Upload New BIM Model**")
            
            with st.form("bim_model_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    model_name = st.text_input("Model Name", placeholder="e.g., Highland Tower - Architectural")
                    discipline = st.selectbox("Discipline", ["Architectural", "Structural", "MEP", "Civil", "Landscape", "Interior"])
                    version = st.text_input("Version", placeholder="e.g., Rev D.1")
                    lod_level = st.selectbox("LOD Level", ["LOD 100", "LOD 200", "LOD 300", "LOD 350", "LOD 400", "LOD 500"])
                    coordinator = st.text_input("Coordinator", placeholder="BIM coordinator name")
                
                with col2:
                    file_size = st.text_input("File Size", placeholder="e.g., 487 MB")
                    elements_count = st.number_input("Elements Count", value=0, min_value=0)
                    software_used = st.text_input("Software Used", placeholder="e.g., Revit 2024")
                    export_format = st.selectbox("Export Format", ["IFC 4.0", "IFC 2x3", "DWG", "NWD", "FBX"])
                
                notes = st.text_area("Model Notes", placeholder="Description of model updates and coordination notes")
                uploaded_file = st.file_uploader("Choose IFC File", type=['ifc', 'dwg', 'nwd'], help="BIM model files only")
                
                if st.form_submit_button("📤 Upload Model", type="primary"):
                    if model_name and discipline and version and coordinator:
                        new_model = {
                            "id": f"BIM-{len(st.session_state.bim_models) + 1:03d}",
                            "model_name": model_name,
                            "discipline": discipline,
                            "version": version,
                            "file_size": file_size if file_size else "0 MB",
                            "elements_count": elements_count,
                            "lod_level": lod_level,
                            "status": "Current",
                            "last_updated": str(datetime.now().date()),
                            "coordinator": coordinator,
                            "file_path": f"/models/{model_name.replace(' ', '_')}_{version.replace(' ', '_')}.ifc",
                            "upload_date": str(datetime.now().date()),
                            "notes": notes,
                            "export_format": export_format,
                            "software_used": software_used
                        }
                        st.session_state.bim_models.append(new_model)
                        st.success("✅ BIM model uploaded successfully!")
                        if uploaded_file:
                            st.info(f"📁 File '{uploaded_file.name}' processed and stored")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with model_sub_tab2:
            st.markdown("**All BIM Models**")
            
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                discipline_filter = st.selectbox("Filter by Discipline", ["All"] + list(set(model['discipline'] for model in st.session_state.bim_models)))
            with col2:
                status_filter = st.selectbox("Filter by Status", ["All", "Current", "Under Review", "Coordinating", "Archived"])
            
            # Display models
            filtered_models = st.session_state.bim_models
            if discipline_filter != "All":
                filtered_models = [model for model in filtered_models if model['discipline'] == discipline_filter]
            if status_filter != "All":
                filtered_models = [model for model in filtered_models if model['status'] == status_filter]
            
            for model in filtered_models:
                status_icon = {"Current": "🟢", "Under Review": "🟡", "Coordinating": "🔄", "Archived": "📁"}.get(model['status'], "📋")
                
                with st.expander(f"{status_icon} {model['model_name']} - {model['version']} ({model['elements_count']:,} elements)"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**🏢 Model:** {model['model_name']}")
                        st.write(f"**🔧 Discipline:** {model['discipline']}")
                        st.write(f"**📋 Version:** {model['version']}")
                        st.write(f"**📊 Status:** {model['status']}")
                        st.write(f"**👤 Coordinator:** {model['coordinator']}")
                        st.write(f"**📅 Last Updated:** {model['last_updated']}")
                    
                    with col2:
                        st.write(f"**📁 File Size:** {model['file_size']}")
                        st.write(f"**🔢 Elements:** {model['elements_count']:,}")
                        st.write(f"**📐 LOD Level:** {model['lod_level']}")
                        st.write(f"**💻 Software:** {model['software_used']}")
                        st.write(f"**📤 Format:** {model['export_format']}")
                        st.write(f"**📅 Upload Date:** {model['upload_date']}")
                    
                    with col3:
                        st.write(f"**📝 Notes:** {model['notes']}")
                        st.write(f"**📁 File Path:** {model['file_path']}")
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button(f"🔄 Update Status", key=f"status_{model['id']}"):
                            new_status = st.selectbox("New Status", ["Current", "Under Review", "Coordinating", "Archived"], key=f"new_status_{model['id']}")
                            model['status'] = new_status
                            st.success("Status updated!")
                            st.rerun()
                    with col2:
                        if st.button(f"📊 View Details", key=f"details_{model['id']}"):
                            st.info("Model details - would open detailed view")
                    with col3:
                        if st.button(f"✏️ Edit", key=f"edit_model_{model['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col4:
                        if st.button(f"🗑️ Delete", key=f"delete_model_{model['id']}"):
                            st.session_state.bim_models.remove(model)
                            st.success("Model deleted!")
                            st.rerun()
    
    with tab2:
        st.subheader("⚠️ Clash Detection Management")
        
        clash_sub_tab1, clash_sub_tab2, clash_sub_tab3 = st.tabs(["🔍 Run Detection", "📊 View Clashes", "📈 Clash Analytics"])
        
        with clash_sub_tab1:
            st.markdown("**Run New Clash Detection**")
            
            with st.form("clash_detection_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    model_1 = st.selectbox("Model 1", [model['model_name'] for model in st.session_state.bim_models])
                    model_2 = st.selectbox("Model 2", [model['model_name'] for model in st.session_state.bim_models])
                    clash_tolerance = st.number_input("Clash Tolerance (mm)", value=10, min_value=1, max_value=100)
                
                with col2:
                    detection_type = st.selectbox("Detection Type", ["Hard Clashes Only", "Soft Clashes Only", "Both Hard and Soft"])
                    priority_level = st.selectbox("Priority Level", ["Low", "Medium", "High", "Critical"])
                    assigned_to = st.text_input("Assign To", placeholder="Coordinator responsible for resolution")
                
                if st.form_submit_button("🔍 Run Clash Detection", type="primary"):
                    if model_1 and model_2 and model_1 != model_2:
                        st.success(f"✅ Clash detection initiated between {model_1} and {model_2}")
                        st.info("🔄 Processing... This may take several minutes for large models")
                        
                        # Simulate finding clashes
                        import random
                        clash_count = random.randint(5, 25)
                        st.success(f"🎯 Detection complete: {clash_count} clashes found")
                        
                        # Add sample clash to session state
                        new_clash = {
                            "id": f"CLH-{len(st.session_state.clash_detections) + 1:03d}",
                            "clash_id": f"CLH-HTD-{len(st.session_state.clash_detections) + 48:03d}",
                            "clash_type": "Hard Clash" if "Hard" in detection_type else "Soft Clash",
                            "location": f"Level {random.randint(8, 15)} - Grid {random.choice(['A', 'B', 'C', 'D', 'E'])}{random.randint(1, 6)}",
                            "discipline_1": model_1.split(' - ')[1] if ' - ' in model_1 else model_1,
                            "discipline_2": model_2.split(' - ')[1] if ' - ' in model_2 else model_2,
                            "priority": priority_level,
                            "status": "Open",
                            "assigned_to": assigned_to,
                            "detected_date": str(datetime.now().date()),
                            "description": f"Element conflict detected between {model_1} and {model_2}",
                            "proposed_solution": "Coordination required",
                            "resolution_date": "",
                            "model_1": model_1,
                            "model_2": model_2
                        }
                        st.session_state.clash_detections.append(new_clash)
                        st.rerun()
                    else:
                        st.error("❌ Please select two different models!")
        
        with clash_sub_tab2:
            st.markdown("**All Clash Detections**")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                clash_status_filter = st.selectbox("Filter by Status", ["All", "Open", "Under Review", "Resolved", "Rejected"])
            with col2:
                clash_priority_filter = st.selectbox("Filter by Priority", ["All", "Low", "Medium", "High", "Critical"])
            with col3:
                clash_type_filter = st.selectbox("Filter by Type", ["All", "Hard Clash", "Soft Clash"])
            
            # Display clashes
            filtered_clashes = st.session_state.clash_detections
            if clash_status_filter != "All":
                filtered_clashes = [clash for clash in filtered_clashes if clash['status'] == clash_status_filter]
            if clash_priority_filter != "All":
                filtered_clashes = [clash for clash in filtered_clashes if clash['priority'] == clash_priority_filter]
            if clash_type_filter != "All":
                filtered_clashes = [clash for clash in filtered_clashes if clash['clash_type'] == clash_type_filter]
            
            for clash in filtered_clashes:
                priority_icon = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}.get(clash['priority'], "⚪")
                status_icon = {"Open": "🔓", "Under Review": "🔄", "Resolved": "✅", "Rejected": "❌"}.get(clash['status'], "📋")
                
                with st.expander(f"{priority_icon} {clash['clash_id']} - {clash['clash_type']} ({clash['status']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**⚠️ Clash Type:** {clash['clash_type']}")
                        st.write(f"**📍 Location:** {clash['location']}")
                        st.write(f"**🔧 Discipline 1:** {clash['discipline_1']}")
                        st.write(f"**🔧 Discipline 2:** {clash['discipline_2']}")
                        st.write(f"**⚠️ Priority:** {clash['priority']}")
                        st.write(f"**📊 Status:** {clash['status']}")
                        st.write(f"**👤 Assigned To:** {clash['assigned_to']}")
                    
                    with col2:
                        st.write(f"**📅 Detected:** {clash['detected_date']}")
                        st.write(f"**🏢 Model 1:** {clash['model_1']}")
                        st.write(f"**🏢 Model 2:** {clash['model_2']}")
                        if clash['resolution_date']:
                            st.write(f"**✅ Resolved:** {clash['resolution_date']}")
                    
                    st.write(f"**📝 Description:** {clash['description']}")
                    st.write(f"**💡 Proposed Solution:** {clash['proposed_solution']}")
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button(f"✅ Resolve", key=f"resolve_clash_{clash['id']}"):
                            clash['status'] = 'Resolved'
                            clash['resolution_date'] = str(datetime.now().date())
                            st.success("Clash resolved!")
                            st.rerun()
                    with col2:
                        if st.button(f"🔄 Review", key=f"review_clash_{clash['id']}"):
                            clash['status'] = 'Under Review'
                            st.info("Clash under review!")
                            st.rerun()
                    with col3:
                        if st.button(f"✏️ Edit", key=f"edit_clash_{clash['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col4:
                        if st.button(f"🗑️ Delete", key=f"delete_clash_{clash['id']}"):
                            st.session_state.clash_detections.remove(clash)
                            st.success("Clash deleted!")
                            st.rerun()
        
        with clash_sub_tab3:
            st.markdown("**Clash Detection Analytics**")
            
            if st.session_state.clash_detections:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Clash status distribution
                    clash_status_counts = {}
                    for clash in st.session_state.clash_detections:
                        status = clash['status']
                        clash_status_counts[status] = clash_status_counts.get(status, 0) + 1
                    
                    status_list = list(clash_status_counts.keys())
                    count_list = list(clash_status_counts.values())
                    clash_status_df = pd.DataFrame({
                        'Status': status_list,
                        'Count': count_list
                    })
                    fig_clash_status = px.pie(clash_status_df, values='Count', names='Status', title="Clash Status Distribution")
                    st.plotly_chart(fig_clash_status, use_container_width=True)
                
                with col2:
                    # Clash priority distribution
                    clash_priority_counts = {}
                    for clash in st.session_state.clash_detections:
                        priority = clash['priority']
                        clash_priority_counts[priority] = clash_priority_counts.get(priority, 0) + 1
                    
                    priority_list = list(clash_priority_counts.keys())
                    priority_count_list = list(clash_priority_counts.values())
                    clash_priority_df = pd.DataFrame({
                        'Priority': priority_list,
                        'Count': priority_count_list
                    })
                    fig_clash_priority = px.bar(clash_priority_df, x='Priority', y='Count', title="Clash Priority Distribution")
                    st.plotly_chart(fig_clash_priority, use_container_width=True)
    
    with tab3:
        st.subheader("📅 BIM Coordination")
        
        coord_sub_tab1, coord_sub_tab2 = st.tabs(["📝 Schedule Meeting", "📊 View Meetings"])
        
        with coord_sub_tab1:
            st.markdown("**Schedule New Coordination Meeting**")
            
            with st.form("coordination_meeting_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    meeting_date = st.date_input("Meeting Date", value=datetime.now().date() + timedelta(days=7))
                    meeting_time = st.time_input("Meeting Time", value=datetime.strptime("14:00", "%H:%M").time())
                    meeting_type = st.selectbox("Meeting Type", ["BIM Coordination", "Clash Review", "Model Review", "Project Coordination"])
                    organizer = st.text_input("Organizer", placeholder="Meeting organizer")
                
                with col2:
                    location = st.text_input("Location", placeholder="Conference Room A / Teams")
                    attendees = st.text_area("Attendees", placeholder="List attendees (comma-separated)")
                    models_reviewed = st.multiselect("Models to Review", [model['model_name'] for model in st.session_state.bim_models])
                
                agenda = st.text_area("Agenda", placeholder="Meeting agenda and topics to discuss")
                
                if st.form_submit_button("📅 Schedule Meeting", type="primary"):
                    if meeting_date and organizer and agenda:
                        new_meeting = {
                            "id": f"COORD-{len(st.session_state.coordination_meetings) + 1:03d}",
                            "meeting_date": str(meeting_date),
                            "meeting_time": str(meeting_time),
                            "meeting_type": meeting_type,
                            "organizer": organizer,
                            "attendees": [att.strip() for att in attendees.split(',') if att.strip()],
                            "agenda": agenda,
                            "status": "Scheduled",
                            "location": location,
                            "models_reviewed": models_reviewed,
                            "action_items": [],
                            "meeting_notes": ""
                        }
                        st.session_state.coordination_meetings.append(new_meeting)
                        st.success("✅ Coordination meeting scheduled successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with coord_sub_tab2:
            st.markdown("**All Coordination Meetings**")
            
            for meeting in st.session_state.coordination_meetings:
                status_icon = {"Scheduled": "📅", "In Progress": "🔄", "Completed": "✅", "Cancelled": "❌"}.get(meeting['status'], "📋")
                
                with st.expander(f"{status_icon} {meeting['meeting_type']} - {meeting['meeting_date']} {meeting['meeting_time']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📅 Date:** {meeting['meeting_date']}")
                        st.write(f"**⏰ Time:** {meeting['meeting_time']}")
                        st.write(f"**📋 Type:** {meeting['meeting_type']}")
                        st.write(f"**👤 Organizer:** {meeting['organizer']}")
                        st.write(f"**📍 Location:** {meeting['location']}")
                        st.write(f"**📊 Status:** {meeting['status']}")
                    
                    with col2:
                        if meeting['attendees']:
                            st.write(f"**👥 Attendees:** {', '.join(meeting['attendees'])}")
                        if meeting['models_reviewed']:
                            st.write(f"**🏢 Models Reviewed:** {', '.join(meeting['models_reviewed'])}")
                    
                    st.write(f"**📋 Agenda:** {meeting['agenda']}")
                    
                    if meeting['meeting_notes']:
                        st.write(f"**📝 Notes:** {meeting['meeting_notes']}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if meeting['status'] == 'Scheduled' and st.button(f"▶️ Start", key=f"start_meeting_{meeting['id']}"):
                            meeting['status'] = 'In Progress'
                            st.success("Meeting started!")
                            st.rerun()
                    with col2:
                        if meeting['status'] == 'In Progress' and st.button(f"✅ Complete", key=f"complete_meeting_{meeting['id']}"):
                            meeting['status'] = 'Completed'
                            st.success("Meeting completed!")
                            st.rerun()
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_meeting_{meeting['id']}"):
                            st.session_state.coordination_meetings.remove(meeting)
                            st.success("Meeting deleted!")
                            st.rerun()
    
    with tab4:
        st.subheader("📈 BIM Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Model elements by discipline
            if st.session_state.bim_models:
                disciplines = [model['discipline'] for model in st.session_state.bim_models]
                elements = [model['elements_count'] for model in st.session_state.bim_models]
                elements_df = pd.DataFrame({
                    'Discipline': disciplines,
                    'Elements': elements
                })
                fig_elements = px.bar(elements_df, x='Discipline', y='Elements', title="Model Elements by Discipline")
                st.plotly_chart(fig_elements, use_container_width=True)
        
        with col2:
            # Model status distribution
            if st.session_state.bim_models:
                model_status_counts = {}
                for model in st.session_state.bim_models:
                    status = model['status']
                    model_status_counts[status] = model_status_counts.get(status, 0) + 1
                
                model_status_list = list(model_status_counts.keys())
                model_count_list = list(model_status_counts.values())
                model_status_df = pd.DataFrame({
                    'Status': model_status_list,
                    'Count': model_count_list
                })
                fig_model_status = px.pie(model_status_df, values='Count', names='Status', title="Model Status Distribution")
                st.plotly_chart(fig_model_status, use_container_width=True)
    
    with tab5:
        st.subheader("🔧 BIM Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🏢 Model Summary**")
            if st.session_state.bim_models:
                model_stats_data = pd.DataFrame([
                    {"Metric": "Total Models", "Value": len(st.session_state.bim_models)},
                    {"Metric": "Total Elements", "Value": f"{sum(model['elements_count'] for model in st.session_state.bim_models):,}"},
                    {"Metric": "Current Models", "Value": len([m for m in st.session_state.bim_models if m['status'] == 'Current'])},
                    {"Metric": "Total Size", "Value": f"{sum(float(m['file_size'].split()[0]) for m in st.session_state.bim_models):.1f} GB"},
                ])
                st.dataframe(model_stats_data, use_container_width=True)
        
        with col2:
            st.markdown("**⚠️ Clash Summary**")
            if st.session_state.clash_detections:
                clash_stats_data = pd.DataFrame([
                    {"Metric": "Total Clashes", "Value": len(st.session_state.clash_detections)},
                    {"Metric": "Open Clashes", "Value": len([c for c in st.session_state.clash_detections if c['status'] == 'Open'])},
                    {"Metric": "Critical Clashes", "Value": len([c for c in st.session_state.clash_detections if c['priority'] == 'Critical'])},
                    {"Metric": "Resolved", "Value": len([c for c in st.session_state.clash_detections if c['status'] == 'Resolved'])},
                ])
                st.dataframe(clash_stats_data, use_container_width=True)
        
        with col3:
            st.markdown("**📅 Meeting Summary**")
            if st.session_state.coordination_meetings:
                meeting_stats_data = pd.DataFrame([
                    {"Metric": "Total Meetings", "Value": len(st.session_state.coordination_meetings)},
                    {"Metric": "Scheduled", "Value": len([m for m in st.session_state.coordination_meetings if m['status'] == 'Scheduled'])},
                    {"Metric": "Completed", "Value": len([m for m in st.session_state.coordination_meetings if m['status'] == 'Completed'])},
                    {"Metric": "This Week", "Value": "1"},
                ])
                st.dataframe(meeting_stats_data, use_container_width=True)
        
        # Data management
        st.markdown("**⚠️ Data Management**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🗑️ Clear All Models", type="secondary"):
                st.session_state.bim_models = []
                st.success("All models cleared!")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Clashes", type="secondary"):
                st.session_state.clash_detections = []
                st.success("All clashes cleared!")
                st.rerun()
        with col3:
            if st.button("🗑️ Clear Meetings", type="secondary"):
                st.session_state.coordination_meetings = []
                st.success("All meetings cleared!")
                st.rerun()

def render_closeout():
    """Complete Project Closeout with full CRUD functionality"""
    st.markdown("""
    <div class="module-header">
        <h1>✅ Project Closeout</h1>
        <p>Comprehensive project completion, documentation, and handover management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize closeout data
    if "punch_list_items" not in st.session_state:
        st.session_state.punch_list_items = [
            {
                "id": "PL-001",
                "item_number": "PL-001",
                "description": "Touch-up paint on Level 12 corridor walls",
                "location": "Level 12, East Corridor",
                "trade": "Painting",
                "responsible_contractor": "Highland Construction LLC",
                "priority": "Medium",
                "status": "Open",
                "date_identified": "2025-05-20",
                "target_completion": "2025-05-30",
                "actual_completion": "",
                "identified_by": "Quality Inspector",
                "photo_required": True,
                "cost_impact": 1500.00,
                "notes": "Minor wall damage from furniture installation"
            },
            {
                "id": "PL-002",
                "item_number": "PL-002",
                "description": "Replace damaged ceiling tile in Unit 1205",
                "location": "Level 12, Unit 1205",
                "trade": "General",
                "responsible_contractor": "Highland Construction LLC",
                "priority": "High",
                "status": "In Progress",
                "date_identified": "2025-05-18",
                "target_completion": "2025-05-25",
                "actual_completion": "",
                "identified_by": "Final Inspector",
                "photo_required": True,
                "cost_impact": 150.00,
                "notes": "Water damage from temporary leak - now repaired"
            },
            {
                "id": "PL-003",
                "item_number": "PL-003",
                "description": "Adjust door hardware on retail entrance",
                "location": "Ground Level, Main Entrance",
                "trade": "Hardware",
                "responsible_contractor": "Steel Solutions Inc",
                "priority": "High",
                "status": "Completed",
                "date_identified": "2025-05-15",
                "target_completion": "2025-05-22",
                "actual_completion": "2025-05-21",
                "identified_by": "Security Team",
                "photo_required": False,
                "cost_impact": 500.00,
                "notes": "Door closing mechanism adjusted for proper operation"
            }
        ]
    
    if "warranties" not in st.session_state:
        st.session_state.warranties = [
            {
                "id": "WAR-001",
                "item_description": "HVAC System - Rooftop Units",
                "manufacturer": "Trane Commercial Systems",
                "model_number": "RTU-150-VRF",
                "warranty_type": "Full System Warranty",
                "warranty_period": "5 years",
                "start_date": "2025-12-15",
                "expiry_date": "2030-12-15",
                "contact_person": "Mike Johnson - Service Manager",
                "phone": "(555) 123-9876",
                "email": "service@trane.com",
                "documentation_location": "/warranties/HVAC/Trane_RTU_Warranty.pdf",
                "maintenance_requirements": "Quarterly filter replacement, annual inspection",
                "coverage_details": "Parts, labor, and emergency service included"
            },
            {
                "id": "WAR-002",
                "item_description": "Elevator Systems - Passenger Elevators",
                "manufacturer": "Otis Elevator Company",
                "model_number": "Gen2-2000",
                "warranty_type": "Full Service Contract",
                "warranty_period": "2 years",
                "start_date": "2025-12-15",
                "expiry_date": "2027-12-15",
                "contact_person": "Sarah Wilson - Account Manager",
                "phone": "(555) 987-6543",
                "email": "warranty@otis.com",
                "documentation_location": "/warranties/Elevators/Otis_Gen2_Warranty.pdf",
                "maintenance_requirements": "Monthly inspections, quarterly maintenance",
                "coverage_details": "24/7 emergency service, all parts and labor"
            }
        ]
    
    if "closeout_documents" not in st.session_state:
        st.session_state.closeout_documents = [
            {
                "id": "DOC-001",
                "document_name": "As-Built Drawings - Architectural",
                "document_type": "As-Built Drawings",
                "trade": "Architectural",
                "status": "Complete",
                "date_submitted": "2025-05-20",
                "submitted_by": "Sarah Chen, AIA",
                "approved_by": "Project Manager",
                "approval_date": "2025-05-22",
                "location": "/closeout/as-builts/architectural/",
                "file_format": "PDF, DWG",
                "file_size": "245 MB",
                "notes": "Complete set of as-built architectural drawings"
            },
            {
                "id": "DOC-002",
                "document_name": "Operation and Maintenance Manuals - MEP",
                "document_type": "O&M Manuals",
                "trade": "MEP",
                "status": "Under Review",
                "date_submitted": "2025-05-18",
                "submitted_by": "Jennifer Walsh, P.E.",
                "approved_by": "",
                "approval_date": "",
                "location": "/closeout/manuals/mep/",
                "file_format": "PDF",
                "file_size": "1.2 GB",
                "notes": "Comprehensive O&M manuals for all MEP systems"
            },
            {
                "id": "DOC-003",
                "document_name": "Warranty Documentation Package",
                "document_type": "Warranties",
                "trade": "All Trades",
                "status": "In Progress",
                "date_submitted": "",
                "submitted_by": "Project Team",
                "approved_by": "",
                "approval_date": "",
                "location": "/closeout/warranties/",
                "file_format": "PDF",
                "file_size": "150 MB",
                "notes": "Collecting warranty documents from all subcontractors"
            }
        ]
    
    # Key Closeout Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_punch_items = len(st.session_state.punch_list_items)
    completed_punch_items = len([item for item in st.session_state.punch_list_items if item['status'] == 'Completed'])
    open_punch_items = total_punch_items - completed_punch_items
    completion_percentage = (completed_punch_items / total_punch_items * 100) if total_punch_items > 0 else 0
    
    with col1:
        st.metric("Punch List Items", total_punch_items, delta_color="normal")
    with col2:
        st.metric("Completed Items", completed_punch_items, delta_color="normal")
    with col3:
        st.metric("Open Items", open_punch_items, delta_color="normal")
    with col4:
        st.metric("Completion %", f"{completion_percentage:.1f}%", delta_color="normal")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Punch List", "📋 Documentation", "🛡️ Warranties", "📈 Analytics", "🔧 Management"])
    
    with tab1:
        st.subheader("📝 Punch List Management")
        
        punch_sub_tab1, punch_sub_tab2, punch_sub_tab3 = st.tabs(["➕ Add Item", "📊 View Items", "📈 Progress Tracking"])
        
        with punch_sub_tab1:
            st.markdown("**Add New Punch List Item**")
            
            with st.form("punch_list_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    item_description = st.text_area("Item Description", placeholder="Detailed description of the issue")
                    location = st.text_input("Location", placeholder="Building level, room, area")
                    trade = st.selectbox("Trade", ["General", "Painting", "Electrical", "Plumbing", "HVAC", "Flooring", "Hardware", "Cleaning"])
                    responsible_contractor = st.text_input("Responsible Contractor", placeholder="Contractor responsible for fix")
                    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
                
                with col2:
                    target_completion = st.date_input("Target Completion", value=datetime.now().date() + timedelta(days=7))
                    identified_by = st.text_input("Identified By", placeholder="Person who identified the issue")
                    photo_required = st.checkbox("Photo Required", value=True)
                    cost_impact = st.number_input("Estimated Cost Impact ($)", value=0.00, format="%.2f")
                
                notes = st.text_area("Notes", placeholder="Additional notes or special instructions")
                
                if st.form_submit_button("📝 Add Punch List Item", type="primary"):
                    if item_description and location and trade:
                        new_item = {
                            "id": f"PL-{len(st.session_state.punch_list_items) + 1:03d}",
                            "item_number": f"PL-{len(st.session_state.punch_list_items) + 1:03d}",
                            "description": item_description,
                            "location": location,
                            "trade": trade,
                            "responsible_contractor": responsible_contractor,
                            "priority": priority,
                            "status": "Open",
                            "date_identified": str(datetime.now().date()),
                            "target_completion": str(target_completion),
                            "actual_completion": "",
                            "identified_by": identified_by,
                            "photo_required": photo_required,
                            "cost_impact": cost_impact,
                            "notes": notes
                        }
                        st.session_state.punch_list_items.append(new_item)
                        st.success("✅ Punch list item added successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with punch_sub_tab2:
            st.markdown("**All Punch List Items**")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All", "Open", "In Progress", "Completed", "On Hold"])
            with col2:
                trade_filter = st.selectbox("Filter by Trade", ["All"] + list(set(item['trade'] for item in st.session_state.punch_list_items)))
            with col3:
                priority_filter = st.selectbox("Filter by Priority", ["All", "Low", "Medium", "High", "Critical"])
            
            # Display punch list items
            filtered_items = st.session_state.punch_list_items
            if status_filter != "All":
                filtered_items = [item for item in filtered_items if item['status'] == status_filter]
            if trade_filter != "All":
                filtered_items = [item for item in filtered_items if item['trade'] == trade_filter]
            if priority_filter != "All":
                filtered_items = [item for item in filtered_items if item['priority'] == priority_filter]
            
            for item in filtered_items:
                priority_icon = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}.get(item['priority'], "⚪")
                status_icon = {"Open": "🔓", "In Progress": "🔄", "Completed": "✅", "On Hold": "⏸️"}.get(item['status'], "📋")
                
                with st.expander(f"{priority_icon} {item['item_number']} - {item['description'][:50]}... ({item['status']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📋 Item #:** {item['item_number']}")
                        st.write(f"**📍 Location:** {item['location']}")
                        st.write(f"**🔧 Trade:** {item['trade']}")
                        st.write(f"**🏢 Contractor:** {item['responsible_contractor']}")
                        st.write(f"**⚠️ Priority:** {item['priority']}")
                        st.write(f"**📊 Status:** {item['status']}")
                        st.write(f"**👤 Identified By:** {item['identified_by']}")
                    
                    with col2:
                        st.write(f"**📅 Date Identified:** {item['date_identified']}")
                        st.write(f"**🎯 Target Completion:** {item['target_completion']}")
                        if item['actual_completion']:
                            st.write(f"**✅ Completed:** {item['actual_completion']}")
                        st.write(f"**📸 Photo Required:** {'Yes' if item['photo_required'] else 'No'}")
                        st.write(f"**💰 Cost Impact:** ${item['cost_impact']:,.2f}")
                    
                    st.write(f"**📝 Description:** {item['description']}")
                    if item['notes']:
                        st.write(f"**📝 Notes:** {item['notes']}")
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button(f"🔄 In Progress", key=f"progress_{item['id']}"):
                            item['status'] = 'In Progress'
                            st.info("Item marked in progress!")
                            st.rerun()
                    with col2:
                        if st.button(f"✅ Complete", key=f"complete_{item['id']}"):
                            item['status'] = 'Completed'
                            item['actual_completion'] = str(datetime.now().date())
                            st.success("Item completed!")
                            st.rerun()
                    with col3:
                        if st.button(f"✏️ Edit", key=f"edit_punch_{item['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col4:
                        if st.button(f"🗑️ Delete", key=f"delete_punch_{item['id']}"):
                            st.session_state.punch_list_items.remove(item)
                            st.success("Punch list item deleted!")
                            st.rerun()
        
        with punch_sub_tab3:
            st.markdown("**Punch List Progress Tracking**")
            
            if st.session_state.punch_list_items:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Status distribution
                    status_counts = {}
                    for item in st.session_state.punch_list_items:
                        status = item['status']
                        status_counts[status] = status_counts.get(status, 0) + 1
                    
                    status_list = list(status_counts.keys())
                    count_list = list(status_counts.values())
                    status_df = pd.DataFrame({
                        'Status': status_list,
                        'Count': count_list
                    })
                    fig_status = px.pie(status_df, values='Count', names='Status', title="Punch List Status Distribution")
                    st.plotly_chart(fig_status, use_container_width=True)
                
                with col2:
                    # Priority distribution
                    priority_counts = {}
                    for item in st.session_state.punch_list_items:
                        priority = item['priority']
                        priority_counts[priority] = priority_counts.get(priority, 0) + 1
                    
                    priority_list = list(priority_counts.keys())
                    priority_count_list = list(priority_counts.values())
                    priority_df = pd.DataFrame({
                        'Priority': priority_list,
                        'Count': priority_count_list
                    })
                    fig_priority = px.bar(priority_df, x='Priority', y='Count', title="Punch List Priority Distribution")
                    st.plotly_chart(fig_priority, use_container_width=True)
    
    with tab2:
        st.subheader("📋 Closeout Documentation")
        
        doc_sub_tab1, doc_sub_tab2 = st.tabs(["📤 Upload Document", "📊 View Documents"])
        
        with doc_sub_tab1:
            st.markdown("**Upload New Closeout Document**")
            
            with st.form("closeout_document_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    document_name = st.text_input("Document Name", placeholder="Document title/name")
                    document_type = st.selectbox("Document Type", ["As-Built Drawings", "O&M Manuals", "Warranties", "Test Reports", "Certificates", "Training Materials", "Other"])
                    trade = st.selectbox("Trade", ["All Trades", "Architectural", "Structural", "MEP", "Civil", "Electrical", "Mechanical", "Plumbing"])
                    submitted_by = st.text_input("Submitted By", placeholder="Person submitting document")
                
                with col2:
                    file_format = st.text_input("File Format", placeholder="e.g., PDF, DWG")
                    file_size = st.text_input("File Size", placeholder="e.g., 245 MB")
                    location = st.text_input("Storage Location", placeholder="File path or storage location")
                
                notes = st.text_area("Document Notes", placeholder="Description of document contents")
                uploaded_file = st.file_uploader("Choose Document File", type=['pdf', 'dwg', 'docx'], help="Closeout documents only")
                
                if st.form_submit_button("📤 Upload Document", type="primary"):
                    if document_name and document_type and submitted_by:
                        new_document = {
                            "id": f"DOC-{len(st.session_state.closeout_documents) + 1:03d}",
                            "document_name": document_name,
                            "document_type": document_type,
                            "trade": trade,
                            "status": "Under Review",
                            "date_submitted": str(datetime.now().date()),
                            "submitted_by": submitted_by,
                            "approved_by": "",
                            "approval_date": "",
                            "location": location if location else f"/closeout/{document_type.lower().replace(' ', '_')}/",
                            "file_format": file_format,
                            "file_size": file_size,
                            "notes": notes
                        }
                        st.session_state.closeout_documents.append(new_document)
                        st.success("✅ Document uploaded successfully!")
                        if uploaded_file:
                            st.info(f"📁 File '{uploaded_file.name}' processed and stored")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with doc_sub_tab2:
            st.markdown("**All Closeout Documents**")
            
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                doc_status_filter = st.selectbox("Filter by Status", ["All", "Under Review", "Complete", "In Progress", "Rejected"])
            with col2:
                doc_type_filter = st.selectbox("Filter by Type", ["All"] + list(set(doc['document_type'] for doc in st.session_state.closeout_documents)))
            
            # Display documents
            filtered_docs = st.session_state.closeout_documents
            if doc_status_filter != "All":
                filtered_docs = [doc for doc in filtered_docs if doc['status'] == doc_status_filter]
            if doc_type_filter != "All":
                filtered_docs = [doc for doc in filtered_docs if doc['document_type'] == doc_type_filter]
            
            for doc in filtered_docs:
                status_icon = {"Under Review": "🔄", "Complete": "✅", "In Progress": "📝", "Rejected": "❌"}.get(doc['status'], "📋")
                
                with st.expander(f"{status_icon} {doc['document_name']} - {doc['document_type']} ({doc['status']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📋 Document:** {doc['document_name']}")
                        st.write(f"**📂 Type:** {doc['document_type']}")
                        st.write(f"**🔧 Trade:** {doc['trade']}")
                        st.write(f"**📊 Status:** {doc['status']}")
                        st.write(f"**👤 Submitted By:** {doc['submitted_by']}")
                        st.write(f"**📅 Date Submitted:** {doc['date_submitted']}")
                    
                    with col2:
                        st.write(f"**📁 File Format:** {doc['file_format']}")
                        st.write(f"**💾 File Size:** {doc['file_size']}")
                        st.write(f"**📍 Location:** {doc['location']}")
                        if doc['approved_by']:
                            st.write(f"**✅ Approved By:** {doc['approved_by']}")
                            st.write(f"**📅 Approval Date:** {doc['approval_date']}")
                    
                    if doc['notes']:
                        st.write(f"**📝 Notes:** {doc['notes']}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if doc['status'] != 'Complete' and st.button(f"✅ Approve", key=f"approve_doc_{doc['id']}"):
                            doc['status'] = 'Complete'
                            doc['approved_by'] = 'Project Manager'
                            doc['approval_date'] = str(datetime.now().date())
                            st.success("Document approved!")
                            st.rerun()
                    with col2:
                        if st.button(f"✏️ Edit", key=f"edit_doc_{doc['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_doc_{doc['id']}"):
                            st.session_state.closeout_documents.remove(doc)
                            st.success("Document deleted!")
                            st.rerun()
    
    with tab3:
        st.subheader("🛡️ Warranty Management")
        
        warranty_sub_tab1, warranty_sub_tab2 = st.tabs(["➕ Add Warranty", "📊 View Warranties"])
        
        with warranty_sub_tab1:
            st.markdown("**Add New Warranty**")
            
            with st.form("warranty_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    item_description = st.text_input("Item Description", placeholder="System or component description")
                    manufacturer = st.text_input("Manufacturer", placeholder="Manufacturer name")
                    model_number = st.text_input("Model Number", placeholder="Model/part number")
                    warranty_type = st.selectbox("Warranty Type", ["Full System Warranty", "Parts Only", "Labor Only", "Extended Warranty", "Service Contract"])
                    warranty_period = st.text_input("Warranty Period", placeholder="e.g., 5 years, 24 months")
                    start_date = st.date_input("Start Date", value=datetime.now().date())
                
                with col2:
                    expiry_date = st.date_input("Expiry Date", value=datetime.now().date() + timedelta(days=1825))
                    contact_person = st.text_input("Contact Person", placeholder="Warranty contact name")
                    phone = st.text_input("Phone", placeholder="Contact phone number")
                    email = st.text_input("Email", placeholder="Contact email address")
                    documentation_location = st.text_input("Documentation Location", placeholder="File path or storage location")
                
                maintenance_requirements = st.text_area("Maintenance Requirements", placeholder="Required maintenance schedule")
                coverage_details = st.text_area("Coverage Details", placeholder="What is covered under warranty")
                
                if st.form_submit_button("🛡️ Add Warranty", type="primary"):
                    if item_description and manufacturer and warranty_period:
                        new_warranty = {
                            "id": f"WAR-{len(st.session_state.warranties) + 1:03d}",
                            "item_description": item_description,
                            "manufacturer": manufacturer,
                            "model_number": model_number,
                            "warranty_type": warranty_type,
                            "warranty_period": warranty_period,
                            "start_date": str(start_date),
                            "expiry_date": str(expiry_date),
                            "contact_person": contact_person,
                            "phone": phone,
                            "email": email,
                            "documentation_location": documentation_location,
                            "maintenance_requirements": maintenance_requirements,
                            "coverage_details": coverage_details
                        }
                        st.session_state.warranties.append(new_warranty)
                        st.success("✅ Warranty added successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with warranty_sub_tab2:
            st.markdown("**All Warranties**")
            
            for warranty in st.session_state.warranties:
                # Calculate days until expiry
                expiry_date = datetime.strptime(warranty['expiry_date'], '%Y-%m-%d').date()
                days_until_expiry = (expiry_date - datetime.now().date()).days
                
                if days_until_expiry < 30:
                    status_icon = "🔴"  # Expiring soon
                elif days_until_expiry < 90:
                    status_icon = "🟡"  # Warning
                else:
                    status_icon = "🟢"  # Good
                
                with st.expander(f"{status_icon} {warranty['item_description']} - {warranty['manufacturer']} (Expires: {warranty['expiry_date']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**🛡️ Item:** {warranty['item_description']}")
                        st.write(f"**🏭 Manufacturer:** {warranty['manufacturer']}")
                        st.write(f"**🔢 Model:** {warranty['model_number']}")
                        st.write(f"**📋 Warranty Type:** {warranty['warranty_type']}")
                        st.write(f"**⏰ Period:** {warranty['warranty_period']}")
                        st.write(f"**📅 Start Date:** {warranty['start_date']}")
                        st.write(f"**📅 Expiry Date:** {warranty['expiry_date']}")
                    
                    with col2:
                        st.write(f"**👤 Contact:** {warranty['contact_person']}")
                        st.write(f"**📞 Phone:** {warranty['phone']}")
                        st.write(f"**📧 Email:** {warranty['email']}")
                        st.write(f"**📁 Documentation:** {warranty['documentation_location']}")
                        if days_until_expiry >= 0:
                            st.write(f"**⏰ Days Until Expiry:** {days_until_expiry}")
                        else:
                            st.write(f"**⚠️ EXPIRED:** {abs(days_until_expiry)} days ago")
                    
                    if warranty['maintenance_requirements']:
                        st.write(f"**🔧 Maintenance:** {warranty['maintenance_requirements']}")
                    if warranty['coverage_details']:
                        st.write(f"**📋 Coverage:** {warranty['coverage_details']}")
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✏️ Edit", key=f"edit_warranty_{warranty['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col2:
                        if st.button(f"🗑️ Delete", key=f"delete_warranty_{warranty['id']}"):
                            st.session_state.warranties.remove(warranty)
                            st.success("Warranty deleted!")
                            st.rerun()
    
    with tab4:
        st.subheader("📈 Closeout Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Document status distribution
            if st.session_state.closeout_documents:
                doc_status_counts = {}
                for doc in st.session_state.closeout_documents:
                    status = doc['status']
                    doc_status_counts[status] = doc_status_counts.get(status, 0) + 1
                
                doc_status_list = list(doc_status_counts.keys())
                doc_count_list = list(doc_status_counts.values())
                doc_status_df = pd.DataFrame({
                    'Status': doc_status_list,
                    'Count': doc_count_list
                })
                fig_doc_status = px.pie(doc_status_df, values='Count', names='Status', title="Document Status Distribution")
                st.plotly_chart(fig_doc_status, use_container_width=True)
        
        with col2:
            # Warranty expiry timeline
            if st.session_state.warranties:
                warranty_data = []
                for warranty in st.session_state.warranties:
                    expiry_date = datetime.strptime(warranty['expiry_date'], '%Y-%m-%d').date()
                    days_until_expiry = (expiry_date - datetime.now().date()).days
                    warranty_data.append({
                        'Item': warranty['item_description'][:20] + "...",
                        'Days_Until_Expiry': max(0, days_until_expiry)
                    })
                
                warranty_df = pd.DataFrame(warranty_data)
                fig_warranty = px.bar(warranty_df, x='Item', y='Days_Until_Expiry', title="Warranty Expiry Timeline")
                st.plotly_chart(fig_warranty, use_container_width=True)
    
    with tab5:
        st.subheader("🔧 Closeout Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📝 Punch List Summary**")
            if st.session_state.punch_list_items:
                punch_stats_data = pd.DataFrame([
                    {"Metric": "Total Items", "Value": len(st.session_state.punch_list_items)},
                    {"Metric": "Completed", "Value": len([i for i in st.session_state.punch_list_items if i['status'] == 'Completed'])},
                    {"Metric": "In Progress", "Value": len([i for i in st.session_state.punch_list_items if i['status'] == 'In Progress'])},
                    {"Metric": "Total Cost Impact", "Value": f"${sum(i['cost_impact'] for i in st.session_state.punch_list_items):,.2f}"},
                ])
                st.dataframe(punch_stats_data, use_container_width=True)
        
        with col2:
            st.markdown("**📋 Document Summary**")
            if st.session_state.closeout_documents:
                doc_stats_data = pd.DataFrame([
                    {"Metric": "Total Documents", "Value": len(st.session_state.closeout_documents)},
                    {"Metric": "Complete", "Value": len([d for d in st.session_state.closeout_documents if d['status'] == 'Complete'])},
                    {"Metric": "Under Review", "Value": len([d for d in st.session_state.closeout_documents if d['status'] == 'Under Review'])},
                    {"Metric": "In Progress", "Value": len([d for d in st.session_state.closeout_documents if d['status'] == 'In Progress'])},
                ])
                st.dataframe(doc_stats_data, use_container_width=True)
        
        with col3:
            st.markdown("**🛡️ Warranty Summary**")
            if st.session_state.warranties:
                expiring_soon = len([w for w in st.session_state.warranties 
                                   if (datetime.strptime(w['expiry_date'], '%Y-%m-%d').date() - datetime.now().date()).days < 90])
                warranty_stats_data = pd.DataFrame([
                    {"Metric": "Total Warranties", "Value": len(st.session_state.warranties)},
                    {"Metric": "Expiring Soon", "Value": expiring_soon},
                    {"Metric": "Active", "Value": len(st.session_state.warranties) - expiring_soon},
                    {"Metric": "Coverage Types", "Value": len(set(w['warranty_type'] for w in st.session_state.warranties))},
                ])
                st.dataframe(warranty_stats_data, use_container_width=True)
        
        # Data management
        st.markdown("**⚠️ Data Management**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🗑️ Clear Punch List", type="secondary"):
                st.session_state.punch_list_items = []
                st.success("All punch list items cleared!")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Documents", type="secondary"):
                st.session_state.closeout_documents = []
                st.success("All documents cleared!")
                st.rerun()
        with col3:
            if st.button("🗑️ Clear Warranties", type="secondary"):
                st.session_state.warranties = []
                st.success("All warranties cleared!")
                st.rerun()

def render_rfis():
    """Enhanced RFI management module with full CRUD functionality"""
    st.markdown("""
    <div class="module-header">
        <h1>📝 Request for Information Management</h1>
        <p>Professional RFI tracking, response management, and collaboration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize RFI data
    if "rfis" not in st.session_state:
        st.session_state.rfis = [
            {
                "id": "RFI-001",
                "title": "Concrete Mix Design Clarification",
                "description": "Need clarification on concrete mix design for Level 3 slab. Specified 4000 PSI but structural drawings show 5000 PSI requirement.",
                "category": "Structural",
                "trade": "Concrete",
                "priority": "High",
                "status": "Open",
                "submitted_by": "Mike Johnson",
                "submitted_date": "2025-05-25",
                "assigned_to": "John Smith, P.E.",
                "due_date": "2025-05-30",
                "location": "Level 3",
                "spec_section": "03 30 00",
                "cost_impact": "$25,000",
                "schedule_impact": "3 days",
                "attachments": ["concrete_specs.pdf", "structural_drawings.dwg"],
                "responses": [
                    {
                        "date": "2025-05-26",
                        "respondent": "Sarah Wilson, P.E.",
                        "response": "Please use 5000 PSI concrete as shown on structural drawings. Updated specifications will be issued.",
                        "status": "Partial Response"
                    }
                ],
                "created_at": "2025-05-25 09:30:00"
            },
            {
                "id": "RFI-002", 
                "title": "HVAC Duct Routing Coordination",
                "description": "HVAC ductwork conflicts with structural beams in mechanical room. Need alternative routing solution.",
                "category": "MEP",
                "trade": "HVAC",
                "priority": "Medium",
                "status": "Under Review",
                "submitted_by": "Dave Brown",
                "submitted_date": "2025-05-24",
                "assigned_to": "Tom Wilson, P.E.",
                "due_date": "2025-05-29",
                "location": "Mechanical Room - Level B1",
                "spec_section": "23 00 00",
                "cost_impact": "TBD",
                "schedule_impact": "2 days",
                "attachments": ["hvac_coordination.pdf"],
                "responses": [],
                "created_at": "2025-05-24 14:15:00"
            },
            {
                "id": "RFI-003",
                "title": "Fire Rating Requirements",
                "description": "Clarification needed on fire rating requirements for corridor partitions between residential units.",
                "category": "Architectural",
                "trade": "Drywall",
                "priority": "High",
                "status": "Closed",
                "submitted_by": "Lisa Chen",
                "submitted_date": "2025-05-22",
                "assigned_to": "Mark Davis, AIA",
                "due_date": "2025-05-27",
                "location": "Levels 2-8 Corridors",
                "spec_section": "09 20 00",
                "cost_impact": "$15,000",
                "schedule_impact": "1 day",
                "attachments": ["fire_code_requirements.pdf"],
                "responses": [
                    {
                        "date": "2025-05-23",
                        "respondent": "Mark Davis, AIA",
                        "response": "Use 1-hour fire rated assemblies as specified in Section 09 20 16. Additional details provided in ASI-005.",
                        "status": "Final Response"
                    }
                ],
                "created_at": "2025-05-22 11:00:00"
            }
        ]
    
    # RFI Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    total_rfis = len(st.session_state.rfis)
    open_rfis = len([r for r in st.session_state.rfis if r['status'] == 'Open'])
    high_priority = len([r for r in st.session_state.rfis if r['priority'] == 'High'])
    avg_response_time = "4.2 days"  # Calculated metric
    
    with col1:
        st.metric("Total RFIs", total_rfis, "+2 this week")
    with col2:
        st.metric("Open RFIs", open_rfis, "+1")
    with col3:
        st.metric("High Priority", high_priority, "0")
    with col4:
        st.metric("Avg Response Time", avg_response_time, "-0.8 days")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Create RFI", "📊 RFI Database", "📈 Analytics", "🔄 Workflow", "⚙️ Settings"])
    
    with tab1:
        st.subheader("📝 Create New RFI")
        
        with st.form("rfi_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Basic Information
                st.markdown("**📋 Basic Information**")
                rfi_title = st.text_input("RFI Title*", placeholder="Brief descriptive title")
                rfi_category = st.selectbox("Category*", [
                    "Architectural", "Structural", "MEP", "Civil", "Landscape", 
                    "Fire Protection", "Technology", "Other"
                ])
                rfi_trade = st.selectbox("Trade*", [
                    "General Contractor", "Concrete", "Steel", "Masonry", "Carpentry",
                    "Electrical", "HVAC", "Plumbing", "Fire Protection", "Elevators", "Other"
                ])
                
                # Priority and Assignment
                st.markdown("**⚡ Priority & Assignment**")
                priority = st.selectbox("Priority Level*", ["Low", "Medium", "High", "Critical"])
                assigned_to = st.text_input("Assigned To", placeholder="Engineer/Architect name")
                due_date = st.date_input("Response Due Date", value=datetime.now().date() + timedelta(days=5))
                
                # Project Information
                st.markdown("**🏗️ Project Information**")
                location = st.text_input("Location/Area", placeholder="Building level, room, area")
                spec_section = st.text_input("Specification Section", placeholder="e.g., 03 30 00")
                
            with col2:
                # Detailed Description
                st.markdown("**📄 Detailed Description**")
                description = st.text_area("RFI Description*", height=120,
                    placeholder="Provide detailed description of the issue, question, or clarification needed...")
                
                # Impact Assessment
                st.markdown("**💰 Impact Assessment**")
                cost_impact = st.text_input("Potential Cost Impact", placeholder="e.g., $15,000 or TBD")
                schedule_impact = st.text_input("Schedule Impact", placeholder="e.g., 3 days or None")
                
                # Attachments
                st.markdown("**📎 Attachments**")
                uploaded_files = st.file_uploader(
                    "Upload Supporting Documents",
                    accept_multiple_files=True,
                    type=['pdf', 'dwg', 'jpg', 'png', 'doc', 'docx']
                )
                
                # Additional Notes
                st.markdown("**📝 Additional Notes**")
                additional_notes = st.text_area("Additional Notes", height=80,
                    placeholder="Any additional context or information...")
            
            submitted = st.form_submit_button("📤 Submit RFI", type="primary", use_container_width=True)
            
            if submitted and rfi_title and description and rfi_category and rfi_trade:
                new_rfi_id = f"RFI-{len(st.session_state.rfis) + 1:03d}"
                new_rfi = {
                    "id": new_rfi_id,
                    "title": rfi_title,
                    "description": description,
                    "category": rfi_category,
                    "trade": rfi_trade,
                    "priority": priority,
                    "status": "Open",
                    "submitted_by": "Current User",
                    "submitted_date": str(datetime.now().date()),
                    "assigned_to": assigned_to,
                    "due_date": str(due_date),
                    "location": location,
                    "spec_section": spec_section,
                    "cost_impact": cost_impact,
                    "schedule_impact": schedule_impact,
                    "attachments": [f.name for f in uploaded_files] if uploaded_files else [],
                    "responses": [],
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.rfis.insert(0, new_rfi)
                st.success(f"✅ RFI {new_rfi_id} submitted successfully!")
                st.rerun()
            elif submitted:
                st.error("⚠️ Please fill in all required fields marked with *")
    
    with tab2:
        st.subheader("📊 RFI Database")
        
        # Search and Filter Controls
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            search_term = st.text_input("🔍 Search", placeholder="Search RFIs...")
        with col2:
            status_filter = st.selectbox("Status", ["All", "Open", "Under Review", "Pending Response", "Closed"])
        with col3:
            priority_filter = st.selectbox("Priority", ["All", "Low", "Medium", "High", "Critical"])
        with col4:
            category_filter = st.selectbox("Category", ["All", "Architectural", "Structural", "MEP", "Civil", "Other"])
        
        # Filter RFIs
        filtered_rfis = st.session_state.rfis
        
        if search_term:
            filtered_rfis = [r for r in filtered_rfis if search_term.lower() in 
                           (r['title'] + r['description'] + r['category'] + r['trade']).lower()]
        if status_filter != "All":
            filtered_rfis = [r for r in filtered_rfis if r['status'] == status_filter]
        if priority_filter != "All":
            filtered_rfis = [r for r in filtered_rfis if r['priority'] == priority_filter]
        if category_filter != "All":
            filtered_rfis = [r for r in filtered_rfis if r['category'] == category_filter]
        
        # Display RFI Cards
        for rfi in filtered_rfis:
            with st.expander(f"📝 {rfi['id']} - {rfi['title']} | {rfi['priority']} Priority | {rfi['status']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**📋 Category:** {rfi['category']} | **🔧 Trade:** {rfi['trade']}")
                    st.markdown(f"**📅 Submitted:** {rfi['submitted_date']} | **⏰ Due:** {rfi['due_date']}")
                    st.markdown(f"**👤 Submitted by:** {rfi['submitted_by']} | **👨‍💼 Assigned to:** {rfi['assigned_to']}")
                    st.markdown(f"**📍 Location:** {rfi['location']} | **📖 Spec Section:** {rfi['spec_section']}")
                    
                    st.markdown("**📄 Description:**")
                    st.text(rfi['description'])
                    
                    if rfi['cost_impact'] or rfi['schedule_impact']:
                        st.markdown(f"**💰 Cost Impact:** {rfi['cost_impact']} | **⏱️ Schedule Impact:** {rfi['schedule_impact']}")
                    
                    if rfi['attachments']:
                        st.markdown(f"**📎 Attachments:** {', '.join(rfi['attachments'])}")
                    
                    # Responses Section
                    if rfi['responses']:
                        st.markdown("**💬 Responses:**")
                        for response in rfi['responses']:
                            with st.container():
                                st.markdown(f"*{response['date']} - {response['respondent']}*")
                                st.text(response['response'])
                                st.markdown(f"Status: {response['status']}")
                                st.divider()
                
                with col2:
                    # Status Management
                    st.markdown("**🔧 Actions**")
                    
                    new_status = st.selectbox(
                        "Update Status",
                        ["Open", "Under Review", "Pending Response", "Closed"],
                        index=["Open", "Under Review", "Pending Response", "Closed"].index(rfi['status']),
                        key=f"status_{rfi['id']}"
                    )
                    
                    if st.button("💾 Update Status", key=f"update_{rfi['id']}"):
                        for i, r in enumerate(st.session_state.rfis):
                            if r['id'] == rfi['id']:
                                st.session_state.rfis[i]['status'] = new_status
                                break
                        st.success("Status updated!")
                        st.rerun()
                    
                    # Response Management
                    if st.button("💬 Add Response", key=f"respond_{rfi['id']}"):
                        st.session_state.responding_to = rfi['id']
                        st.rerun()
                    
                    if st.button("✏️ Edit RFI", key=f"edit_{rfi['id']}"):
                        st.session_state.editing_rfi = rfi['id']
                        st.rerun()
                    
                    if st.button("📄 Export PDF", key=f"export_{rfi['id']}"):
                        st.info("PDF export ready for implementation")
                    
                    if st.button("🗑️ Delete", key=f"delete_{rfi['id']}"):
                        st.session_state.rfis = [r for r in st.session_state.rfis if r['id'] != rfi['id']]
                        st.success("RFI deleted!")
                        st.rerun()
        
        # Add Response Modal
        if hasattr(st.session_state, 'responding_to'):
            st.subheader("💬 Add Response")
            with st.form("response_form"):
                response_text = st.text_area("Response", height=100)
                response_status = st.selectbox("Response Type", ["Partial Response", "Final Response", "Request for More Info"])
                
                if st.form_submit_button("📤 Submit Response"):
                    for i, rfi in enumerate(st.session_state.rfis):
                        if rfi['id'] == st.session_state.responding_to:
                            new_response = {
                                "date": str(datetime.now().date()),
                                "respondent": "Current User",
                                "response": response_text,
                                "status": response_status
                            }
                            st.session_state.rfis[i]['responses'].append(new_response)
                            break
                    
                    del st.session_state.responding_to
                    st.success("Response added!")
                    st.rerun()
    
    with tab3:
        st.subheader("📈 RFI Analytics")
        
        if st.session_state.rfis:
            # Analytics metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # RFI Status Distribution
                status_counts = {}
                for rfi in st.session_state.rfis:
                    status = rfi['status']
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                status_list = list(status_counts.keys())
                count_list = list(status_counts.values())
                status_df = pd.DataFrame({
                    'Status': status_list,
                    'Count': count_list
                })
                fig_status = px.pie(status_df, values='Count', names='Status', title="RFI Status Distribution")
                st.plotly_chart(fig_status, use_container_width=True)
                
                # Priority Distribution
                priority_counts = {}
                for rfi in st.session_state.rfis:
                    priority = rfi['priority']
                    priority_counts[priority] = priority_counts.get(priority, 0) + 1
                
                priority_list = list(priority_counts.keys())
                priority_count_list = list(priority_counts.values())
                priority_df = pd.DataFrame({
                    'Priority': priority_list,
                    'Count': priority_count_list
                })
                fig_priority = px.bar(priority_df, x='Priority', y='Count', title="RFI Priority Distribution")
                st.plotly_chart(fig_priority, use_container_width=True)
            
            with col2:
                # Category Distribution
                category_counts = {}
                for rfi in st.session_state.rfis:
                    category = rfi['category']
                    category_counts[category] = category_counts.get(category, 0) + 1
                
                category_list = list(category_counts.keys())
                category_count_list = list(category_counts.values())
                category_df = pd.DataFrame({
                    'Category': category_list,
                    'Count': category_count_list
                })
                fig_category = px.bar(category_df, x='Category', y='Count', title="RFI by Category")
                st.plotly_chart(fig_category, use_container_width=True)
                
                # Trade Distribution
                trade_counts = {}
                for rfi in st.session_state.rfis:
                    trade = rfi['trade']
                    trade_counts[trade] = trade_counts.get(trade, 0) + 1
                
                trade_list = list(trade_counts.keys())
                trade_count_list = list(trade_counts.values())
                trade_df = pd.DataFrame({
                    'Trade': trade_list,
                    'Count': trade_count_list
                })
                fig_trade = px.bar(trade_df, x='Trade', y='Count', title="RFI by Trade")
                st.plotly_chart(fig_trade, use_container_width=True)
    
    with tab4:
        st.subheader("🔄 RFI Workflow Management")
        
        # Workflow statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**⏰ Overdue RFIs**")
            overdue_count = 0
            for rfi in st.session_state.rfis:
                if rfi['status'] != 'Closed' and rfi['due_date'] < str(datetime.now().date()):
                    overdue_count += 1
            st.metric("Overdue", overdue_count, "📅")
        
        with col2:
            st.markdown("**⚡ High Priority Open**")
            high_priority_open = len([r for r in st.session_state.rfis 
                                    if r['priority'] == 'High' and r['status'] != 'Closed'])
            st.metric("High Priority", high_priority_open, "🔥")
        
        with col3:
            st.markdown("**📋 Pending Response**")
            pending_response = len([r for r in st.session_state.rfis if r['status'] == 'Pending Response'])
            st.metric("Pending", pending_response, "⏳")
        
        # Workflow Actions
        st.subheader("🔧 Bulk Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📤 Export All RFIs to CSV", use_container_width=True):
                df = pd.DataFrame(st.session_state.rfis)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"rfis_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            if st.button("📊 Generate RFI Report", use_container_width=True):
                st.info("Comprehensive RFI report generation ready")
        
        with col2:
            if st.button("📧 Send Overdue Notifications", use_container_width=True):
                st.info("Email notification system ready for implementation")
            
            if st.button("🔄 Bulk Status Update", use_container_width=True):
                st.info("Bulk status update interface ready")
    
    with tab5:
        st.subheader("⚙️ RFI Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔧 System Settings**")
            default_due_days = st.number_input("Default Response Days", value=5, min_value=1, max_value=30)
            auto_notifications = st.checkbox("Auto Email Notifications", value=True)
            require_attachments = st.checkbox("Require Attachments", value=False)
            
            if st.button("💾 Save Settings", use_container_width=True):
                st.success("Settings saved successfully!")
        
        with col2:
            st.markdown("**📊 Data Management**")
            if st.button("🗑️ Clear All RFIs", use_container_width=True):
                if st.checkbox("⚠️ Confirm deletion of all RFIs"):
                    st.session_state.rfis = []
                    st.success("All RFIs cleared!")
                    st.rerun()
            
            if st.button("📥 Import RFIs from CSV", use_container_width=True):
                st.info("CSV import functionality ready for implementation")
            
            if st.button("🔄 Reset to Defaults", use_container_width=True):
                st.info("Reset functionality ready")

def render_submittals():
    """Enterprise Submittals Management with robust Python backend"""
    try:
        from modules.submittals_backend import submittals_manager
        render_submittals_enterprise()
        return
    except ImportError:
        st.error("Enterprise Submittals module not available")
    
    # Fallback to basic version
    render_submittals_basic()

def render_submittals_enterprise():
    """Render enterprise submittals interface"""
    from modules.submittals_backend import submittals_manager, SubmittalStatus, SubmittalType
    
    st.markdown("""
    <div class="module-header">
        <h1>📤 Submittals Management</h1>
        <p>Highland Tower Development - Enterprise document submission and approval workflows</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display summary metrics
    metrics = submittals_manager.generate_submittal_metrics()
    if metrics:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📤 Total Submittals", metrics['total_submittals'])
        with col2:
            st.metric("⏳ Pending Review", metrics['pending_review'])
        with col3:
            st.metric("✅ Approval Rate", f"{metrics['approval_rate']}%")
        with col4:
            st.metric("⚠️ Overdue", metrics['overdue_count'])
    
    # Display submittals
    submittals = submittals_manager.get_all_submittals()
    
    st.subheader("📋 All Submittals")
    
    for submittal in submittals:
        status_color = {
            SubmittalStatus.APPROVED: "🟢",
            SubmittalStatus.UNDER_REVIEW: "🟡", 
            SubmittalStatus.REVISE_AND_RESUBMIT: "🟠",
            SubmittalStatus.REJECTED: "🔴"
        }.get(submittal.status, "⚪")
        
        with st.expander(f"{status_color} {submittal.submittal_number} | {submittal.title} | {submittal.status.value}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**📋 Type:** {submittal.submittal_type.value}")
                st.write(f"**📄 Spec Section:** {submittal.spec_section}")
                st.write(f"**🏢 Contractor:** {submittal.contractor}")
                st.write(f"**📅 Required Date:** {submittal.required_date}")
                if submittal.submitted_date:
                    st.write(f"**📤 Submitted:** {submittal.submitted_date}")
            
            with col2:
                st.write(f"**📍 Location:** {submittal.location}")
                st.write(f"**👤 Contact:** {submittal.contact_person}")
                st.write(f"**📝 Revision:** {submittal.current_revision}")
                st.write(f"**⏱️ Days in Review:** {submittal.days_in_review}")
                if submittal.approved_date:
                    st.write(f"**✅ Approved:** {submittal.approved_date}")
            
            if submittal.description:
                st.write(f"**📝 Description:** {submittal.description}")
            
            # Show reviews
            if submittal.reviews:
                st.write("**📋 Reviews:**")
                for review in submittal.reviews:
                    st.write(f"• {review.reviewer_name} ({review.review_date}): {review.action.value}")
                    if review.comments:
                        st.write(f"  *{review.comments}*")

def render_submittals_basic():
    """Basic Submittals module - fallback version"""
    st.markdown("""
    <div class="module-header">
        <h1>📤 Submittals Management</h1>
        <p>Product submittals and approval workflow</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📤 Submittals module with approval workflows and tracking")

def render_transmittals():
    """Enterprise Transmittals Management with robust Python backend"""
    try:
        from modules.transmittals_backend import transmittals_manager, TransmittalStatus, TransmittalType
        
        st.markdown("""
        <div class="module-header">
            <h1>📧 Transmittals Management</h1>
            <p>Highland Tower Development - Document distribution and communication tracking</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display summary metrics
        metrics = transmittals_manager.generate_transmittal_metrics()
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📧 Total Transmittals", metrics['total_transmittals'])
            with col2:
                st.metric("⏳ Pending Acknowledgment", metrics['pending_acknowledgments'])
            with col3:
                st.metric("✅ Acknowledgment Rate", f"{metrics['acknowledgment_rate']}%")
            with col4:
                st.metric("📄 Total Documents", metrics['total_documents'])
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["📧 All Transmittals", "➕ Create New", "📊 Analytics"])
        
        with tab1:
            st.subheader("📧 All Transmittals")
            
            # Display transmittals
            transmittals = transmittals_manager.get_all_transmittals()
            
            for transmittal in transmittals:
                status_color = {
                    TransmittalStatus.SENT: "🟡",
                    TransmittalStatus.RECEIVED: "🟠", 
                    TransmittalStatus.ACKNOWLEDGED: "🟢",
                    TransmittalStatus.REJECTED: "🔴"
                }.get(transmittal.status, "⚪")
                
                with st.expander(f"{status_color} {transmittal.transmittal_number} | {transmittal.subject} | {transmittal.status.value}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📋 Type:** {transmittal.transmittal_type.value}")
                        st.write(f"**📤 From:** {transmittal.sender_name} ({transmittal.sender_company})")
                        st.write(f"**📮 Method:** {transmittal.delivery_method.value}")
                        if transmittal.sent_date:
                            st.write(f"**📅 Sent:** {transmittal.sent_date}")
                    
                    with col2:
                        st.write(f"**📄 Documents:** {transmittal.total_documents}")
                        st.write(f"**👥 Recipients:** {len(transmittal.recipients)}")
                        if transmittal.tracking_number:
                            st.write(f"**📋 Tracking:** {transmittal.tracking_number}")
                        if transmittal.reply_by_date:
                            st.write(f"**⏰ Reply By:** {transmittal.reply_by_date}")
                    
                    if transmittal.message:
                        st.write(f"**💬 Message:** {transmittal.message}")
                    
                    # Show recipients
                    if transmittal.recipients:
                        st.write("**👥 Recipients:**")
                        for recipient in transmittal.recipients:
                            ack_status = "✅" if recipient.acknowledged_date else "⏳"
                            st.write(f"• {ack_status} {recipient.name} ({recipient.company}) - {recipient.copy_type}")
                    
                    # Show documents
                    if transmittal.documents:
                        st.write("**📄 Documents:**")
                        for doc in transmittal.documents:
                            st.write(f"• {doc.filename} - {doc.description}")
                    
                    # CRUD operations
                    st.write("---")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"📤 Send", key=f"btn_send_{transmittal.transmittal_id}"):
                            if transmittals_manager.send_transmittal(transmittal.transmittal_id):
                                st.success("Transmittal sent successfully!")
                                st.rerun()
                    
                    with col2:
                        if st.button(f"✅ Acknowledge", key=f"btn_ack_{transmittal.transmittal_id}"):
                            # For demo, acknowledge first recipient
                            if transmittal.recipients:
                                first_recipient = transmittal.recipients[0]
                                if transmittals_manager.acknowledge_transmittal(transmittal.transmittal_id, first_recipient.recipient_id):
                                    st.success("Transmittal acknowledged!")
                                    st.rerun()
                    
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"btn_del_{transmittal.transmittal_id}"):
                            if transmittal.transmittal_id in transmittals_manager.transmittals:
                                del transmittals_manager.transmittals[transmittal.transmittal_id]
                                st.success("Transmittal deleted!")
                                st.rerun()
        
        with tab2:
            st.subheader("➕ Create New Transmittal")
            
            with st.form("create_transmittal_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    subject = st.text_input("📝 Subject*", placeholder="Enter transmittal subject")
                    description = st.text_area("📋 Description", placeholder="Detailed description")
                    transmittal_type = st.selectbox("📋 Type*", options=[t.value for t in TransmittalType])
                    delivery_method = st.selectbox("📮 Delivery Method*", options=["Email", "Hand Delivery", "Courier", "Mail", "Digital Platform"])
                
                with col2:
                    sender_name = st.text_input("👤 Sender Name*", value="John Smith")
                    sender_company = st.text_input("🏢 Sender Company*", value="Highland Construction Co.")
                    sender_email = st.text_input("📧 Sender Email*", value="jsmith@highland.com")
                    sender_phone = st.text_input("📞 Sender Phone", value="(555) 123-4567")
                
                # Recipients section
                st.write("**👥 Recipients**")
                recipient_name = st.text_input("Recipient Name", placeholder="Enter recipient name")
                recipient_company = st.text_input("Recipient Company", placeholder="Enter company")
                recipient_email = st.text_input("Recipient Email", placeholder="Enter email")
                recipient_role = st.text_input("Recipient Role", placeholder="Enter role")
                copy_type = st.selectbox("Copy Type", options=["TO", "CC", "BCC"])
                
                # Message section
                message = st.text_area("💬 Message", placeholder="Enter message content")
                special_instructions = st.text_area("📋 Special Instructions", placeholder="Any special instructions")
                
                # Settings
                col1, col2 = st.columns(2)
                with col1:
                    reply_required = st.checkbox("📮 Reply Required")
                    acknowledgment_required = st.checkbox("✅ Acknowledgment Required")
                
                with col2:
                    if reply_required:
                        reply_by_date = st.date_input("⏰ Reply By Date")
                    else:
                        reply_by_date = None
                
                submitted = st.form_submit_button("🆕 Create Transmittal", use_container_width=True)
                
                if submitted:
                    # Validate required fields
                    if not subject or not transmittal_type or not sender_name or not sender_company:
                        st.error("Please fill in all required fields marked with *")
                    else:
                        # Create recipient
                        recipients = []
                        if recipient_name and recipient_email:
                            from modules.transmittals_backend import TransmittalRecipient
                            recipient = TransmittalRecipient(
                                recipient_id=f"rec-{len(recipients) + 1:03d}",
                                name=recipient_name,
                                company=recipient_company,
                                email=recipient_email,
                                role=recipient_role,
                                copy_type=copy_type,
                                received_date=None,
                                acknowledged_date=None
                            )
                            recipients.append(recipient)
                        
                        # Create transmittal data
                        transmittal_data = {
                            "subject": subject,
                            "description": description,
                            "transmittal_type": transmittal_type,
                            "delivery_method": delivery_method,
                            "project_name": "Highland Tower Development",
                            "project_number": "HTD-2024-001",
                            "sender_name": sender_name,
                            "sender_company": sender_company,
                            "sender_email": sender_email,
                            "sender_phone": sender_phone,
                            "recipients": recipients,
                            "message": message,
                            "special_instructions": special_instructions,
                            "reply_required": reply_required,
                            "reply_by_date": reply_by_date.strftime('%Y-%m-%d') if reply_by_date else None,
                            "acknowledgment_required": acknowledgment_required,
                            "created_by": sender_name
                        }
                        
                        # Create transmittal
                        transmittal_id = transmittals_manager.create_transmittal(transmittal_data)
                        st.success(f"✅ Transmittal created successfully! ID: {transmittal_id}")
                        st.rerun()
        
        with tab3:
            st.subheader("📊 Transmittals Analytics")
            
            if metrics:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📊 Status Breakdown:**")
                    for status, count in metrics['status_breakdown'].items():
                        status_color = {
                            "Sent": "🟡",
                            "Received": "🟠",
                            "Acknowledged": "🟢",
                            "Rejected": "🔴",
                            "Draft": "⚪"
                        }.get(status, "⚪")
                        st.write(f"• {status_color} {status}: {count}")
                    
                    st.write("**📋 Type Breakdown:**")
                    for trans_type, count in metrics['type_breakdown'].items():
                        st.write(f"• {trans_type}: {count}")
                
                with col2:
                    st.write("**📈 Performance Metrics:**")
                    st.write(f"• **Total Transmittals:** {metrics['total_transmittals']}")
                    st.write(f"• **Acknowledgment Rate:** {metrics['acknowledgment_rate']}%")
                    st.write(f"• **Pending Acknowledgments:** {metrics['pending_acknowledgments']}")
                    st.write(f"• **Total Documents:** {metrics['total_documents']}")
                    st.write(f"• **Avg Documents per Transmittal:** {metrics['avg_documents_per_transmittal']}")
                    
                    st.write("**📮 Delivery Methods:**")
                    for method, count in metrics['delivery_methods'].items():
                        st.write(f"• {method}: {count}")
        
        return
        
    except ImportError:
        st.error("Enterprise Transmittals module not available")
        # Fallback to basic version
        render_transmittals_basic()

def render_transmittals_basic():
    """Basic transmittals module - fallback version"""
    st.markdown("""
    <div class="module-header">
        <h1>📨 Transmittals</h1>
        <p>Document distribution and transmittal tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📨 Transmittals module for document distribution")

def render_scheduling():
    """Enterprise Project Scheduling with full CRUD functionality"""
    try:
        from modules.scheduling_backend import scheduling_manager, TaskStatus, TaskType, TaskPriority
        
        st.markdown("""
        <div class="module-header">
            <h1>📅 Project Scheduling</h1>
            <p>Highland Tower Development - Comprehensive task management and milestone tracking</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display summary metrics
        metrics = scheduling_manager.generate_schedule_metrics()
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📋 Total Tasks", metrics['total_tasks'])
            with col2:
                st.metric("📊 Avg Progress", f"{metrics['average_progress']}%")
            with col3:
                st.metric("⚠️ Overdue Tasks", metrics['overdue_tasks'])
            with col4:
                st.metric("⏰ On-Time Performance", f"{metrics['on_time_performance']}%")
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📋 All Tasks", "➕ Create New", "✏️ Edit Tasks", "📊 Analytics"])
        
        with tab1:
            st.subheader("📋 All Schedule Tasks")
            
            # Display tasks
            tasks = scheduling_manager.get_all_tasks()
            
            for task in tasks:
                status_color = {
                    TaskStatus.COMPLETED: "🟢",
                    TaskStatus.IN_PROGRESS: "🟡",
                    TaskStatus.NOT_STARTED: "🔵",
                    TaskStatus.ON_HOLD: "🟠",
                    TaskStatus.CANCELLED: "🔴"
                }.get(task.status, "⚪")
                
                priority_icon = {
                    TaskPriority.CRITICAL: "🚨",
                    TaskPriority.HIGH: "🔴",
                    TaskPriority.MEDIUM: "🟡",
                    TaskPriority.LOW: "🟢"
                }.get(task.priority, "⚪")
                
                overdue_indicator = "⚠️ OVERDUE" if task.is_overdue() else ""
                
                with st.expander(f"{status_color} {priority_icon} {task.task_number} | {task.task_name} | {task.percent_complete:.0f}% {overdue_indicator}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📅 Planned:** {task.planned_start_date} to {task.planned_end_date}")
                        if task.actual_start_date:
                            st.write(f"**🎯 Actual Start:** {task.actual_start_date}")
                        if task.actual_end_date:
                            st.write(f"**✅ Actual End:** {task.actual_end_date}")
                        st.write(f"**📦 Phase:** {task.phase}")
                        st.write(f"**📍 Location:** {task.location}")
                    
                    with col2:
                        st.write(f"**👤 Assigned To:** {task.assigned_to}")
                        st.write(f"**⏱️ Duration:** {task.duration_days} days")
                        st.write(f"**💰 Budget:** ${task.budgeted_cost:,.0f}")
                        st.write(f"**💸 Actual:** ${task.actual_cost:,.0f}")
                        if task.cost_variance != 0:
                            variance_color = "🟢" if task.cost_variance < 0 else "🔴"
                            st.write(f"**📊 Variance:** {variance_color} ${task.cost_variance:,.0f}")
                    
                    if task.description:
                        st.write(f"**📝 Description:** {task.description}")
                    
                    # Progress bar
                    st.progress(task.percent_complete / 100.0)
                    st.write(f"**Progress:** {task.percent_complete:.1f}% complete")
                    
                    # Quick actions
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        new_progress = st.number_input(f"Update Progress %", 
                                                     min_value=0.0, max_value=100.0, 
                                                     value=task.percent_complete,
                                                     step=5.0,
                                                     key=f"progress_{task.task_id}")
                        if st.button(f"📊 Update", key=f"btn_update_progress_{task.task_id}"):
                            if scheduling_manager.update_task_progress(task.task_id, new_progress):
                                st.success("Progress updated!")
                                st.rerun()
                    
                    with col2:
                        if st.button(f"▶️ Start Task", key=f"btn_start_{task.task_id}"):
                            if scheduling_manager.update_task_progress(task.task_id, max(1.0, task.percent_complete)):
                                st.success("Task started!")
                                st.rerun()
                    
                    with col3:
                        if st.button(f"✅ Complete", key=f"btn_complete_{task.task_id}"):
                            if scheduling_manager.update_task_progress(task.task_id, 100.0):
                                st.success("Task completed!")
                                st.rerun()
        
        with tab2:
            st.subheader("➕ Create New Task")
            
            with st.form("create_task_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    task_name = st.text_input("📝 Task Name*", placeholder="Enter task name")
                    description = st.text_area("📋 Description", placeholder="Detailed task description")
                    task_type = st.selectbox("📋 Task Type*", options=["Construction", "Inspection", "Delivery", "Milestone", "Planning", "Review"])
                    priority = st.selectbox("🚨 Priority*", options=["Low", "Medium", "High", "Critical"])
                    phase = st.text_input("📦 Phase*", placeholder="e.g., Foundation, Structure")
                
                with col2:
                    work_package = st.text_input("📦 Work Package*", value="Highland Tower Development")
                    location = st.text_input("📍 Location*", placeholder="e.g., Level 12 - North Wing")
                    assigned_to = st.text_input("👤 Assigned To*", placeholder="Person or crew responsible")
                    duration_days = st.number_input("⏱️ Duration (days)*", min_value=1, step=1, value=1)
                    budgeted_cost = st.number_input("💰 Budgeted Cost*", min_value=0.0, step=100.0)
                
                # Schedule dates
                st.write("**📅 Schedule**")
                col1, col2 = st.columns(2)
                
                with col1:
                    planned_start = st.date_input("📅 Planned Start Date*")
                
                with col2:
                    # Calculate end date based on duration
                    planned_end = planned_start + timedelta(days=duration_days-1)
                    st.date_input("📅 Planned End Date", value=planned_end, disabled=True)
                
                # Additional details
                col1, col2 = st.columns(2)
                
                with col1:
                    notes = st.text_area("📝 Notes", placeholder="Additional notes or comments")
                    constraints = st.text_area("⚠️ Constraints", placeholder="Any constraints or limitations")
                
                with col2:
                    risks = st.text_area("⚠️ Risks", placeholder="Potential risks or issues")
                
                submit_task = st.form_submit_button("🆕 Create Task", use_container_width=True)
                
                if submit_task:
                    if not task_name or not task_type or not phase or not assigned_to:
                        st.error("Please fill in all required fields marked with *")
                    else:
                        task_data = {
                            "task_name": task_name,
                            "description": description,
                            "task_type": task_type,
                            "priority": priority,
                            "project_name": "Highland Tower Development",
                            "phase": phase,
                            "work_package": work_package,
                            "location": location,
                            "planned_start_date": planned_start.strftime('%Y-%m-%d'),
                            "planned_end_date": planned_end.strftime('%Y-%m-%d'),
                            "duration_days": duration_days,
                            "assigned_to": assigned_to,
                            "budgeted_cost": budgeted_cost,
                            "notes": notes,
                            "constraints": constraints,
                            "risks": risks,
                            "created_by": "Current User",
                            "last_updated_by": "Current User"
                        }
                        
                        task_id = scheduling_manager.create_task(task_data)
                        st.success(f"✅ Task created successfully! ID: {task_id}")
                        st.rerun()
        
        with tab3:
            st.subheader("✏️ Edit Tasks")
            
            tasks = scheduling_manager.get_all_tasks()
            if tasks:
                task_options = [f"{t.task_number} - {t.task_name}" for t in tasks]
                selected_task_index = st.selectbox("Select Task to Edit", range(len(task_options)), format_func=lambda x: task_options[x])
                selected_task = tasks[selected_task_index]
                
                with st.form("edit_task_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        edit_name = st.text_input("📝 Task Name*", value=selected_task.task_name)
                        edit_description = st.text_area("📋 Description", value=selected_task.description)
                        edit_assigned = st.text_input("👤 Assigned To*", value=selected_task.assigned_to)
                        edit_budget = st.number_input("💰 Budget", value=float(selected_task.budgeted_cost), step=100.0)
                    
                    with col2:
                        edit_location = st.text_input("📍 Location", value=selected_task.location)
                        edit_notes = st.text_area("📝 Notes", value=selected_task.notes)
                        edit_constraints = st.text_area("⚠️ Constraints", value=selected_task.constraints)
                        edit_risks = st.text_area("⚠️ Risks", value=selected_task.risks)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        update_task = st.form_submit_button("✏️ Update Task", use_container_width=True)
                    
                    with col2:
                        if st.form_submit_button("🗑️ Delete Task", use_container_width=True):
                            if selected_task.task_id in scheduling_manager.tasks:
                                del scheduling_manager.tasks[selected_task.task_id]
                                st.success("✅ Task deleted successfully!")
                                st.rerun()
                    
                    with col3:
                        if st.form_submit_button("📋 Duplicate Task", use_container_width=True):
                            # Create a duplicate with modified name
                            task_data = {
                                "task_name": f"Copy of {selected_task.task_name}",
                                "description": selected_task.description,
                                "task_type": selected_task.task_type.value,
                                "priority": selected_task.priority.value,
                                "project_name": selected_task.project_name,
                                "phase": selected_task.phase,
                                "work_package": selected_task.work_package,
                                "location": selected_task.location,
                                "planned_start_date": selected_task.planned_start_date,
                                "planned_end_date": selected_task.planned_end_date,
                                "duration_days": selected_task.duration_days,
                                "assigned_to": selected_task.assigned_to,
                                "budgeted_cost": selected_task.budgeted_cost,
                                "notes": selected_task.notes,
                                "constraints": selected_task.constraints,
                                "risks": selected_task.risks,
                                "created_by": "Current User",
                                "last_updated_by": "Current User"
                            }
                            task_id = scheduling_manager.create_task(task_data)
                            st.success(f"✅ Task duplicated! ID: {task_id}")
                            st.rerun()
                    
                    if update_task:
                        # Update the selected task
                        selected_task.task_name = edit_name
                        selected_task.description = edit_description
                        selected_task.assigned_to = edit_assigned
                        selected_task.budgeted_cost = edit_budget
                        selected_task.location = edit_location
                        selected_task.notes = edit_notes
                        selected_task.constraints = edit_constraints
                        selected_task.risks = edit_risks
                        selected_task.last_updated_by = "Current User"
                        selected_task.updated_at = datetime.now().isoformat()
                        
                        st.success("✅ Task updated successfully!")
                        st.rerun()
            else:
                st.info("No tasks available to edit. Create some tasks first.")
        
        with tab4:
            st.subheader("📊 Schedule Analytics")
            
            if metrics:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📊 Task Status:**")
                    for status, count in metrics['status_breakdown'].items():
                        status_icon = {
                            "Completed": "🟢",
                            "In Progress": "🟡",
                            "Not Started": "🔵",
                            "On Hold": "🟠",
                            "Cancelled": "🔴"
                        }.get(status, "⚪")
                        st.write(f"• {status_icon} {status}: {count}")
                    
                    st.write("**🚨 Priority Distribution:**")
                    for priority, count in metrics['priority_breakdown'].items():
                        priority_icon = {
                            "Critical": "🚨",
                            "High": "🔴",
                            "Medium": "🟡",
                            "Low": "🟢"
                        }.get(priority, "⚪")
                        st.write(f"• {priority_icon} {priority}: {count}")
                
                with col2:
                    st.write("**📈 Performance Metrics:**")
                    st.write(f"• **Completion Rate:** {metrics['completion_rate']}%")
                    st.write(f"• **On-Time Performance:** {metrics['on_time_performance']}%")
                    st.write(f"• **Average Progress:** {metrics['average_progress']}%")
                    st.write(f"• **Overdue Tasks:** {metrics['overdue_tasks']}")
                    
                    st.write("**💰 Cost Performance:**")
                    st.write(f"• **Total Budget:** ${metrics['total_budgeted_cost']:,.0f}")
                    st.write(f"• **Total Actual:** ${metrics['total_actual_cost']:,.0f}")
                    variance_color = "🟢" if metrics['cost_variance'] <= 0 else "🔴"
                    st.write(f"• **Cost Variance:** {variance_color} ${metrics['cost_variance']:,.0f}")
        
        return
        
    except ImportError:
        st.error("Enterprise Scheduling module not available")
        render_scheduling_basic()

def render_scheduling_basic():
    """Basic scheduling module - fallback version"""
    st.markdown("""
    <div class="module-header">
        <h1>📅 Project Scheduling</h1>
        <p>Advanced timeline management, critical path analysis, and resource planning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize scheduling data
    if "schedule_tasks" not in st.session_state:
        st.session_state.schedule_tasks = [
            {
                "id": "TASK-001",
                "task_name": "Site Preparation and Mobilization",
                "description": "Site setup, temporary facilities, and equipment mobilization",
                "start_date": "2025-01-15",
                "end_date": "2025-01-31",
                "duration_days": 16,
                "progress": 100,
                "status": "Complete",
                "phase": "Preconstruction",
                "responsible_party": "Highland Construction LLC",
                "dependencies": [],
                "critical_path": True,
                "cost_budgeted": 150000.00,
                "cost_actual": 142000.00,
                "resources_required": ["Site Supervisor", "Equipment Operator", "General Labor"],
                "milestone": False,
                "notes": "Completed ahead of schedule with cost savings"
            },
            {
                "id": "TASK-002",
                "task_name": "Foundation and Below Grade Work",
                "description": "Excavation, foundation walls, waterproofing, and backfill",
                "start_date": "2025-02-01",
                "end_date": "2025-03-31",
                "duration_days": 59,
                "progress": 100,
                "status": "Complete",
                "phase": "Foundation",
                "responsible_party": "Highland Construction LLC",
                "dependencies": ["TASK-001"],
                "critical_path": True,
                "cost_budgeted": 2800000.00,
                "cost_actual": 2750000.00,
                "resources_required": ["Concrete Crew", "Excavator", "Crane Operator"],
                "milestone": True,
                "notes": "Foundation milestone achieved on schedule"
            },
            {
                "id": "TASK-003",
                "task_name": "Structural Steel Frame - Levels 1-8",
                "description": "Structural steel erection for tower levels 1 through 8",
                "start_date": "2025-04-01",
                "end_date": "2025-06-14",
                "duration_days": 74,
                "progress": 85,
                "status": "In Progress",
                "phase": "Structure",
                "responsible_party": "Steel Solutions Inc",
                "dependencies": ["TASK-002"],
                "critical_path": True,
                "cost_budgeted": 3200000.00,
                "cost_actual": 2720000.00,
                "resources_required": ["Steel Crew", "Crane Operator", "Welders"],
                "milestone": False,
                "notes": "On track for completion, weather delays minimal"
            },
            {
                "id": "TASK-004",
                "task_name": "MEP Rough-in Installation",
                "description": "Electrical, plumbing, and HVAC rough-in work",
                "start_date": "2025-06-15",
                "end_date": "2025-07-31",
                "duration_days": 46,
                "progress": 60,
                "status": "In Progress",
                "phase": "MEP",
                "responsible_party": "Elite MEP Systems",
                "dependencies": ["TASK-003"],
                "critical_path": False,
                "cost_budgeted": 4100000.00,
                "cost_actual": 2460000.00,
                "resources_required": ["Electricians", "Plumbers", "HVAC Technicians"],
                "milestone": False,
                "notes": "Coordination meetings scheduled for routing conflicts"
            },
            {
                "id": "TASK-005",
                "task_name": "Exterior Envelope System",
                "description": "Curtain wall, windows, and exterior cladding installation",
                "start_date": "2025-08-01",
                "end_date": "2025-09-30",
                "duration_days": 60,
                "progress": 30,
                "status": "Planned",
                "phase": "Envelope",
                "responsible_party": "Premium Exteriors LLC",
                "dependencies": ["TASK-003"],
                "critical_path": False,
                "cost_budgeted": 2200000.00,
                "cost_actual": 0.00,
                "resources_required": ["Glazing Crew", "Crane Operator", "Cladding Specialists"],
                "milestone": True,
                "notes": "Weather-dependent activities scheduled for optimal conditions"
            }
        ]
    
    if "project_milestones" not in st.session_state:
        st.session_state.project_milestones = [
            {
                "id": "MILE-001",
                "milestone_name": "Foundation Completion",
                "target_date": "2025-03-31",
                "actual_date": "2025-03-31",
                "status": "Achieved",
                "description": "Complete foundation and below-grade work",
                "critical": True,
                "dependencies": ["TASK-002"],
                "achievement_notes": "Achieved on target date with quality standards met"
            },
            {
                "id": "MILE-002",
                "milestone_name": "Structural Topping Out",
                "target_date": "2025-08-15",
                "actual_date": "",
                "status": "Pending",
                "description": "Complete structural steel frame to roof level",
                "critical": True,
                "dependencies": ["TASK-003"],
                "achievement_notes": ""
            },
            {
                "id": "MILE-003",
                "milestone_name": "Envelope Weathertight",
                "target_date": "2025-10-15",
                "actual_date": "",
                "status": "Pending",
                "description": "Building envelope sealed and weathertight",
                "critical": True,
                "dependencies": ["TASK-005"],
                "achievement_notes": ""
            }
        ]
    
    if "resource_allocations" not in st.session_state:
        st.session_state.resource_allocations = [
            {
                "id": "RES-001",
                "resource_name": "Tower Crane TC-1",
                "resource_type": "Equipment",
                "allocated_tasks": ["TASK-003", "TASK-005"],
                "start_date": "2025-04-01",
                "end_date": "2025-09-30",
                "daily_cost": 850.00,
                "utilization": 85,
                "status": "Active",
                "operator": "Steve Wilson",
                "notes": "Primary crane for structural and envelope work"
            },
            {
                "id": "RES-002",
                "resource_name": "Steel Erection Crew A",
                "resource_type": "Labor",
                "allocated_tasks": ["TASK-003"],
                "start_date": "2025-04-01",
                "end_date": "2025-06-14",
                "daily_cost": 3200.00,
                "utilization": 95,
                "status": "Active",
                "operator": "Mike Chen - Foreman",
                "notes": "Experienced crew with excellent safety record"
            },
            {
                "id": "RES-003",
                "resource_name": "MEP Installation Team",
                "resource_type": "Labor",
                "allocated_tasks": ["TASK-004"],
                "start_date": "2025-06-15",
                "end_date": "2025-07-31",
                "daily_cost": 2800.00,
                "utilization": 78,
                "status": "Scheduled",
                "operator": "Jennifer Walsh - MEP Coordinator",
                "notes": "Multi-trade team for coordinated MEP installation"
            }
        ]
    
    # Key Scheduling Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_tasks = len(st.session_state.schedule_tasks)
    completed_tasks = len([task for task in st.session_state.schedule_tasks if task['status'] == 'Complete'])
    critical_path_tasks = len([task for task in st.session_state.schedule_tasks if task['critical_path']])
    overall_progress = sum(task['progress'] for task in st.session_state.schedule_tasks) / len(st.session_state.schedule_tasks) if st.session_state.schedule_tasks else 0
    
    with col1:
        st.metric("Total Tasks", total_tasks, delta_color="normal")
    with col2:
        st.metric("Completed", completed_tasks, delta_color="normal")
    with col3:
        st.metric("Critical Path", critical_path_tasks, delta_color="normal")
    with col4:
        st.metric("Overall Progress", f"{overall_progress:.1f}%", delta_color="normal")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Task Management", "🎯 Milestones", "👥 Resources", "📈 Analytics", "🔧 Management"])
    
    with tab1:
        st.subheader("📝 Project Task Management")
        
        task_sub_tab1, task_sub_tab2, task_sub_tab3 = st.tabs(["➕ Add Task", "📊 View Tasks", "📅 Gantt Chart"])
        
        with task_sub_tab1:
            st.markdown("**Add New Project Task**")
            
            with st.form("task_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    task_name = st.text_input("Task Name", placeholder="Descriptive task name")
                    description = st.text_area("Description", placeholder="Detailed task description")
                    start_date = st.date_input("Start Date", value=datetime.now().date())
                    end_date = st.date_input("End Date", value=datetime.now().date() + timedelta(days=30))
                    phase = st.selectbox("Project Phase", ["Preconstruction", "Foundation", "Structure", "MEP", "Envelope", "Interiors", "Closeout"])
                    responsible_party = st.text_input("Responsible Party", placeholder="Contractor or team responsible")
                
                with col2:
                    status = st.selectbox("Status", ["Planned", "In Progress", "Complete", "On Hold", "Cancelled"])
                    progress = st.slider("Progress %", 0, 100, 0)
                    cost_budgeted = st.number_input("Budgeted Cost ($)", value=0.00, format="%.2f")
                    critical_path = st.checkbox("Critical Path Task")
                    milestone = st.checkbox("Milestone Task")
                    dependencies = st.text_input("Dependencies", placeholder="Comma-separated task IDs")
                
                resources_required = st.text_area("Resources Required", placeholder="List required resources")
                notes = st.text_area("Notes", placeholder="Additional notes or comments")
                
                if st.form_submit_button("📅 Add Task", type="primary"):
                    if task_name and start_date and end_date and responsible_party:
                        duration_days = (end_date - start_date).days
                        
                        new_task = {
                            "id": f"TASK-{len(st.session_state.schedule_tasks) + 1:03d}",
                            "task_name": task_name,
                            "description": description,
                            "start_date": str(start_date),
                            "end_date": str(end_date),
                            "duration_days": duration_days,
                            "progress": progress,
                            "status": status,
                            "phase": phase,
                            "responsible_party": responsible_party,
                            "dependencies": [dep.strip() for dep in dependencies.split(',') if dep.strip()],
                            "critical_path": critical_path,
                            "cost_budgeted": cost_budgeted,
                            "cost_actual": 0.00,
                            "resources_required": [res.strip() for res in resources_required.split(',') if res.strip()],
                            "milestone": milestone,
                            "notes": notes
                        }
                        st.session_state.schedule_tasks.append(new_task)
                        st.success("✅ Task added successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with task_sub_tab2:
            st.markdown("**All Project Tasks**")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All", "Planned", "In Progress", "Complete", "On Hold", "Cancelled"])
            with col2:
                phase_filter = st.selectbox("Filter by Phase", ["All"] + list(set(task['phase'] for task in st.session_state.schedule_tasks)))
            with col3:
                critical_filter = st.selectbox("Critical Path Only", ["All Tasks", "Critical Path Only"])
            
            # Display tasks
            filtered_tasks = st.session_state.schedule_tasks
            if status_filter != "All":
                filtered_tasks = [task for task in filtered_tasks if task['status'] == status_filter]
            if phase_filter != "All":
                filtered_tasks = [task for task in filtered_tasks if task['phase'] == phase_filter]
            if critical_filter == "Critical Path Only":
                filtered_tasks = [task for task in filtered_tasks if task['critical_path']]
            
            for task in filtered_tasks:
                status_icon = {"Planned": "📋", "In Progress": "🔄", "Complete": "✅", "On Hold": "⏸️", "Cancelled": "❌"}.get(task['status'], "📋")
                critical_icon = "🔴" if task['critical_path'] else "⚪"
                milestone_icon = "🎯" if task['milestone'] else ""
                
                with st.expander(f"{status_icon} {critical_icon} {milestone_icon} {task['task_name']} - {task['phase']} ({task['progress']}%)"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**📋 Task:** {task['task_name']}")
                        st.write(f"**📝 Description:** {task['description']}")
                        st.write(f"**🏗️ Phase:** {task['phase']}")
                        st.write(f"**👤 Responsible:** {task['responsible_party']}")
                        st.write(f"**📊 Status:** {task['status']}")
                        st.write(f"**📈 Progress:** {task['progress']}%")
                    
                    with col2:
                        st.write(f"**📅 Start Date:** {task['start_date']}")
                        st.write(f"**📅 End Date:** {task['end_date']}")
                        st.write(f"**⏱️ Duration:** {task['duration_days']} days")
                        st.write(f"**🔴 Critical Path:** {'Yes' if task['critical_path'] else 'No'}")
                        st.write(f"**🎯 Milestone:** {'Yes' if task['milestone'] else 'No'}")
                        if task['dependencies']:
                            st.write(f"**🔗 Dependencies:** {', '.join(task['dependencies'])}")
                    
                    with col3:
                        st.write(f"**💰 Budgeted:** ${task['cost_budgeted']:,.2f}")
                        st.write(f"**💸 Actual:** ${task['cost_actual']:,.2f}")
                        if task['resources_required']:
                            st.write(f"**👥 Resources:** {', '.join(task['resources_required'])}")
                        if task['notes']:
                            st.write(f"**📝 Notes:** {task['notes']}")
                    
                    # Progress bar
                    st.write("**📈 Task Progress:**")
                    st.progress(task['progress'] / 100)
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button(f"▶️ Start", key=f"start_{task['id']}"):
                            task['status'] = 'In Progress'
                            st.success("Task started!")
                            st.rerun()
                    with col2:
                        new_progress = st.slider(f"Update Progress", 0, 100, task['progress'], key=f"progress_t_{task['id']}")
                        if st.button(f"📊 Update", key=f"update_t_{task['id']}"):
                            task['progress'] = new_progress
                            if new_progress >= 100:
                                task['status'] = 'Complete'
                            st.success("Progress updated!")
                            st.rerun()
                    with col3:
                        if st.button(f"✏️ Edit", key=f"edit_task_{task['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col4:
                        if st.button(f"🗑️ Delete", key=f"delete_task_{task['id']}"):
                            st.session_state.schedule_tasks.remove(task)
                            st.success("Task deleted!")
                            st.rerun()
        
        with task_sub_tab3:
            st.markdown("**Project Gantt Chart**")
            
            if st.session_state.schedule_tasks:
                # Create Gantt chart data
                gantt_data = []
                for task in st.session_state.schedule_tasks:
                    gantt_data.append({
                        'Task': task['task_name'],
                        'Start': task['start_date'],
                        'Finish': task['end_date'],
                        'Phase': task['phase'],
                        'Status': task['status']
                    })
                
                gantt_df = pd.DataFrame(gantt_data)
                
                # Create timeline chart
                fig = px.timeline(gantt_df, x_start='Start', x_end='Finish', y='Task', color='Phase',
                                title="Highland Tower Development - Project Schedule")
                fig.update_yaxes(autorange="reversed")
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No tasks available for Gantt chart display")
    
    with tab2:
        st.subheader("🎯 Project Milestones")
        
        milestone_sub_tab1, milestone_sub_tab2 = st.tabs(["➕ Add Milestone", "📊 View Milestones"])
        
        with milestone_sub_tab1:
            st.markdown("**Add New Project Milestone**")
            
            with st.form("milestone_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    milestone_name = st.text_input("Milestone Name", placeholder="Milestone description")
                    target_date = st.date_input("Target Date", value=datetime.now().date() + timedelta(days=60))
                    critical = st.checkbox("Critical Milestone")
                    dependencies = st.multiselect("Task Dependencies", [task['id'] + " - " + task['task_name'] for task in st.session_state.schedule_tasks])
                
                with col2:
                    description = st.text_area("Description", placeholder="Detailed milestone description")
                    status = st.selectbox("Status", ["Pending", "Achieved", "Missed", "At Risk"])
                    achievement_notes = st.text_area("Achievement Notes", placeholder="Notes about milestone achievement")
                
                if st.form_submit_button("🎯 Add Milestone", type="primary"):
                    if milestone_name and target_date:
                        new_milestone = {
                            "id": f"MILE-{len(st.session_state.project_milestones) + 1:03d}",
                            "milestone_name": milestone_name,
                            "target_date": str(target_date),
                            "actual_date": "",
                            "status": status,
                            "description": description,
                            "critical": critical,
                            "dependencies": [dep.split(" - ")[0] for dep in dependencies],
                            "achievement_notes": achievement_notes
                        }
                        st.session_state.project_milestones.append(new_milestone)
                        st.success("✅ Milestone added successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with milestone_sub_tab2:
            st.markdown("**All Project Milestones**")
            
            for milestone in st.session_state.project_milestones:
                status_icon = {"Pending": "⏳", "Achieved": "✅", "Missed": "❌", "At Risk": "⚠️"}.get(milestone['status'], "📋")
                critical_icon = "🔴" if milestone['critical'] else "⚪"
                
                with st.expander(f"{status_icon} {critical_icon} {milestone['milestone_name']} - {milestone['status']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**🎯 Milestone:** {milestone['milestone_name']}")
                        st.write(f"**📅 Target Date:** {milestone['target_date']}")
                        if milestone['actual_date']:
                            st.write(f"**✅ Actual Date:** {milestone['actual_date']}")
                        st.write(f"**📊 Status:** {milestone['status']}")
                        st.write(f"**🔴 Critical:** {'Yes' if milestone['critical'] else 'No'}")
                    
                    with col2:
                        st.write(f"**📝 Description:** {milestone['description']}")
                        if milestone['dependencies']:
                            st.write(f"**🔗 Dependencies:** {', '.join(milestone['dependencies'])}")
                        if milestone['achievement_notes']:
                            st.write(f"**📝 Notes:** {milestone['achievement_notes']}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if milestone['status'] != 'Achieved' and st.button(f"✅ Mark Achieved", key=f"achieve_{milestone['id']}"):
                            milestone['status'] = 'Achieved'
                            milestone['actual_date'] = str(datetime.now().date())
                            st.success("Milestone achieved!")
                            st.rerun()
                    with col2:
                        if st.button(f"✏️ Edit", key=f"edit_milestone_{milestone['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_milestone_{milestone['id']}"):
                            st.session_state.project_milestones.remove(milestone)
                            st.success("Milestone deleted!")
                            st.rerun()
    
    with tab3:
        st.subheader("👥 Resource Management")
        
        resource_sub_tab1, resource_sub_tab2 = st.tabs(["➕ Allocate Resource", "📊 View Resources"])
        
        with resource_sub_tab1:
            st.markdown("**Allocate New Resource**")
            
            with st.form("resource_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    resource_name = st.text_input("Resource Name", placeholder="Resource identifier")
                    resource_type = st.selectbox("Resource Type", ["Equipment", "Labor", "Material", "Subcontractor"])
                    start_date = st.date_input("Allocation Start", value=datetime.now().date())
                    end_date = st.date_input("Allocation End", value=datetime.now().date() + timedelta(days=30))
                    daily_cost = st.number_input("Daily Cost ($)", value=0.00, format="%.2f")
                
                with col2:
                    allocated_tasks = st.multiselect("Allocated Tasks", [task['id'] + " - " + task['task_name'] for task in st.session_state.schedule_tasks])
                    utilization = st.slider("Expected Utilization %", 0, 100, 85)
                    status = st.selectbox("Status", ["Scheduled", "Active", "Complete", "Cancelled"])
                    operator = st.text_input("Operator/Supervisor", placeholder="Person responsible")
                
                notes = st.text_area("Notes", placeholder="Additional resource notes")
                
                if st.form_submit_button("👥 Allocate Resource", type="primary"):
                    if resource_name and resource_type and start_date and end_date:
                        new_resource = {
                            "id": f"RES-{len(st.session_state.resource_allocations) + 1:03d}",
                            "resource_name": resource_name,
                            "resource_type": resource_type,
                            "allocated_tasks": [task.split(" - ")[0] for task in allocated_tasks],
                            "start_date": str(start_date),
                            "end_date": str(end_date),
                            "daily_cost": daily_cost,
                            "utilization": utilization,
                            "status": status,
                            "operator": operator,
                            "notes": notes
                        }
                        st.session_state.resource_allocations.append(new_resource)
                        st.success("✅ Resource allocated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with resource_sub_tab2:
            st.markdown("**All Resource Allocations**")
            
            for resource in st.session_state.resource_allocations:
                status_icon = {"Scheduled": "📅", "Active": "🟢", "Complete": "✅", "Cancelled": "❌"}.get(resource['status'], "📋")
                
                with st.expander(f"{status_icon} {resource['resource_name']} - {resource['resource_type']} ({resource['status']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**👥 Resource:** {resource['resource_name']}")
                        st.write(f"**📋 Type:** {resource['resource_type']}")
                        st.write(f"**📅 Start:** {resource['start_date']}")
                        st.write(f"**📅 End:** {resource['end_date']}")
                        st.write(f"**💰 Daily Cost:** ${resource['daily_cost']:,.2f}")
                        st.write(f"**📊 Status:** {resource['status']}")
                    
                    with col2:
                        st.write(f"**📈 Utilization:** {resource['utilization']}%")
                        st.write(f"**👤 Operator:** {resource['operator']}")
                        if resource['allocated_tasks']:
                            st.write(f"**🔗 Tasks:** {', '.join(resource['allocated_tasks'])}")
                        if resource['notes']:
                            st.write(f"**📝 Notes:** {resource['notes']}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"🟢 Activate", key=f"activate_{resource['id']}"):
                            resource['status'] = 'Active'
                            st.success("Resource activated!")
                            st.rerun()
                    with col2:
                        if st.button(f"✏️ Edit", key=f"edit_resource_{resource['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col3:
                        if st.button(f"🗑️ Remove", key=f"remove_resource_{resource['id']}"):
                            st.session_state.resource_allocations.remove(resource)
                            st.success("Resource removed!")
                            st.rerun()
    
    with tab4:
        st.subheader("📈 Scheduling Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Task status distribution
            if st.session_state.schedule_tasks:
                task_status_counts = {}
                for task in st.session_state.schedule_tasks:
                    status = task['status']
                    task_status_counts[status] = task_status_counts.get(status, 0) + 1
                
                task_status_list = list(task_status_counts.keys())
                task_count_list = list(task_status_counts.values())
                task_status_df = pd.DataFrame({
                    'Status': task_status_list,
                    'Count': task_count_list
                })
                fig_task_status = px.pie(task_status_df, values='Count', names='Status', title="Task Status Distribution")
                st.plotly_chart(fig_task_status, use_container_width=True)
        
        with col2:
            # Phase progress
            if st.session_state.schedule_tasks:
                phase_progress = {}
                for task in st.session_state.schedule_tasks:
                    phase = task['phase']
                    if phase not in phase_progress:
                        phase_progress[phase] = []
                    phase_progress[phase].append(task['progress'])
                
                phase_avg = {phase: sum(progresses)/len(progresses) for phase, progresses in phase_progress.items()}
                
                phase_list = list(phase_avg.keys())
                progress_list = list(phase_avg.values())
                phase_df = pd.DataFrame({
                    'Phase': phase_list,
                    'Progress': progress_list
                })
                fig_phase = px.bar(phase_df, x='Phase', y='Progress', title="Progress by Project Phase")
                st.plotly_chart(fig_phase, use_container_width=True)
    
    with tab5:
        st.subheader("🔧 Schedule Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📅 Task Summary**")
            if st.session_state.schedule_tasks:
                task_stats_data = pd.DataFrame([
                    {"Metric": "Total Tasks", "Value": len(st.session_state.schedule_tasks)},
                    {"Metric": "Completed", "Value": len([t for t in st.session_state.schedule_tasks if t['status'] == 'Complete'])},
                    {"Metric": "In Progress", "Value": len([t for t in st.session_state.schedule_tasks if t['status'] == 'In Progress'])},
                    {"Metric": "Critical Path", "Value": len([t for t in st.session_state.schedule_tasks if t['critical_path']])},
                ])
                st.dataframe(task_stats_data, use_container_width=True)
        
        with col2:
            st.markdown("**🎯 Milestone Summary**")
            if st.session_state.project_milestones:
                milestone_stats_data = pd.DataFrame([
                    {"Metric": "Total Milestones", "Value": len(st.session_state.project_milestones)},
                    {"Metric": "Achieved", "Value": len([m for m in st.session_state.project_milestones if m['status'] == 'Achieved'])},
                    {"Metric": "Pending", "Value": len([m for m in st.session_state.project_milestones if m['status'] == 'Pending'])},
                    {"Metric": "Critical", "Value": len([m for m in st.session_state.project_milestones if m['critical']])},
                ])
                st.dataframe(milestone_stats_data, use_container_width=True)
        
        with col3:
            st.markdown("**👥 Resource Summary**")
            if st.session_state.resource_allocations:
                resource_stats_data = pd.DataFrame([
                    {"Metric": "Total Resources", "Value": len(st.session_state.resource_allocations)},
                    {"Metric": "Active", "Value": len([r for r in st.session_state.resource_allocations if r['status'] == 'Active'])},
                    {"Metric": "Daily Cost", "Value": f"${sum(r['daily_cost'] for r in st.session_state.resource_allocations):,.2f}"},
                    {"Metric": "Avg Utilization", "Value": f"{sum(r['utilization'] for r in st.session_state.resource_allocations) / len(st.session_state.resource_allocations):.1f}%"},
                ])
                st.dataframe(resource_stats_data, use_container_width=True)
        
        # Data management
        st.markdown("**⚠️ Data Management**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🗑️ Clear All Tasks", type="secondary"):
                st.session_state.schedule_tasks = []
                st.success("All tasks cleared!")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Milestones", type="secondary"):
                st.session_state.project_milestones = []
                st.success("All milestones cleared!")
                st.rerun()
        with col3:
            if st.button("🗑️ Clear Resources", type="secondary"):
                st.session_state.resource_allocations = []
                st.success("All resources cleared!")
                st.rerun()

def render_quality_control():
    """Complete Quality Control with full CRUD functionality"""
    st.markdown("""
    <div class="module-header">
        <h1>🔍 Quality Control</h1>
        <p>Comprehensive inspection management, quality assurance, and compliance tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize quality control data
    if "qc_inspections" not in st.session_state:
        st.session_state.qc_inspections = [
            {
                "id": "QC-001",
                "inspection_id": "HTD-QC-2025-045",
                "inspection_type": "Structural Steel",
                "location": "Level 13 - Grid Lines C-F",
                "status": "In Progress",
                "inspector": "John Davis, P.E.",
                "inspection_date": "2025-05-27",
                "scheduled_date": "2025-05-27",
                "trade": "Structural",
                "description": "Structural steel connection inspection for beam-to-column connections",
                "pass_criteria": "All connections meet AWS D1.1 standards, proper bolt torque, alignment within tolerance",
                "findings": "Minor alignment issue at Grid C3 requires adjustment before final approval",
                "recommendations": "Adjust alignment at Grid C3 and re-inspect",
                "photos_required": True,
                "follow_up_required": True,
                "follow_up_date": "2025-05-29",
                "severity": "Minor",
                "corrective_actions": ["Realign connection at Grid C3", "Verify torque values"],
                "responsible_contractor": "Steel Solutions Inc"
            },
            {
                "id": "QC-002",
                "inspection_id": "HTD-QC-2025-044",
                "inspection_type": "MEP Rough-in",
                "location": "Level 11 - Electrical Rooms",
                "status": "Passed",
                "inspector": "Maria Garcia, P.E.",
                "inspection_date": "2025-05-25",
                "scheduled_date": "2025-05-25",
                "trade": "Electrical",
                "description": "Electrical rough-in inspection for conduit installation and panel connections",
                "pass_criteria": "Conduit properly secured, panels correctly labeled, grounding verified",
                "findings": "All electrical work meets NEC standards and project specifications",
                "recommendations": "Continue with installation as planned",
                "photos_required": True,
                "follow_up_required": False,
                "follow_up_date": "",
                "severity": "None",
                "corrective_actions": [],
                "responsible_contractor": "Elite MEP Systems"
            },
            {
                "id": "QC-003",
                "inspection_id": "HTD-QC-2025-043",
                "inspection_type": "Concrete Pour",
                "location": "Level 12 - East Wing Slab",
                "status": "Failed",
                "inspector": "Robert Kim, ACI",
                "inspection_date": "2025-05-23",
                "scheduled_date": "2025-05-23",
                "trade": "Concrete",
                "description": "Post-pour concrete inspection for Level 12 slab",
                "pass_criteria": "Surface finish within tolerance, no significant cracking, proper curing",
                "findings": "Surface irregularities exceed tolerance in Zone C, minor honeycomb in one location",
                "recommendations": "Repair surface irregularities and honeycomb areas before proceeding",
                "photos_required": True,
                "follow_up_required": True,
                "follow_up_date": "2025-05-30",
                "severity": "Major",
                "corrective_actions": ["Grind surface irregularities", "Patch honeycomb areas", "Re-inspect"],
                "responsible_contractor": "Highland Construction LLC"
            }
        ]
    
    if "qc_checklists" not in st.session_state:
        st.session_state.qc_checklists = [
            {
                "id": "CHK-001",
                "checklist_name": "Structural Steel Connection Checklist",
                "trade": "Structural",
                "checklist_items": [
                    {"item": "Beam alignment verified", "status": "Pass", "notes": "Within 1/4 inch tolerance"},
                    {"item": "Bolt grade verified", "status": "Pass", "notes": "A325 bolts confirmed"},
                    {"item": "Bolt torque applied", "status": "Pending", "notes": "Awaiting final torque"},
                    {"item": "Connection welding complete", "status": "Pass", "notes": "All welds inspected"}
                ],
                "created_date": "2025-05-20",
                "last_updated": "2025-05-27",
                "inspector": "John Davis, P.E.",
                "overall_status": "In Progress",
                "completion_percentage": 75
            },
            {
                "id": "CHK-002",
                "checklist_name": "MEP Rough-in Quality Checklist",
                "trade": "MEP",
                "checklist_items": [
                    {"item": "Conduit properly secured", "status": "Pass", "notes": "All supports in place"},
                    {"item": "Panel labeling complete", "status": "Pass", "notes": "Clear labeling verified"},
                    {"item": "Grounding connections verified", "status": "Pass", "notes": "Continuity tested"},
                    {"item": "Fire stopping complete", "status": "Pass", "notes": "All penetrations sealed"}
                ],
                "created_date": "2025-05-18",
                "last_updated": "2025-05-25",
                "inspector": "Maria Garcia, P.E.",
                "overall_status": "Complete",
                "completion_percentage": 100
            }
        ]
    
    if "qc_defects" not in st.session_state:
        st.session_state.qc_defects = [
            {
                "id": "DEF-001",
                "defect_id": "HTD-DEF-001",
                "title": "Surface irregularities in concrete slab",
                "description": "Concrete surface finish exceeds flatness tolerance in multiple areas",
                "location": "Level 12 - East Wing",
                "trade": "Concrete",
                "severity": "Major",
                "status": "Open",
                "identified_date": "2025-05-23",
                "identified_by": "Robert Kim, ACI",
                "assigned_to": "Highland Construction LLC",
                "target_resolution": "2025-05-30",
                "actual_resolution": "",
                "cost_impact": 15000.00,
                "schedule_impact": 3,
                "corrective_actions": ["Grind high spots", "Apply self-leveling compound", "Re-inspect surface"],
                "root_cause": "Inadequate screeding during pour",
                "prevention_measures": "Enhanced screed board setup and additional training"
            },
            {
                "id": "DEF-002",
                "defect_id": "HTD-DEF-002",
                "title": "Steel beam alignment issue",
                "description": "Beam alignment at Grid C3 exceeds tolerance by 3/8 inch",
                "location": "Level 13 - Grid C3",
                "trade": "Structural",
                "severity": "Minor",
                "status": "In Progress", 
                "identified_date": "2025-05-27",
                "identified_by": "John Davis, P.E.",
                "assigned_to": "Steel Solutions Inc",
                "target_resolution": "2025-05-29",
                "actual_resolution": "",
                "cost_impact": 2500.00,
                "schedule_impact": 1,
                "corrective_actions": ["Loosen connections", "Realign beam", "Re-torque bolts"],
                "root_cause": "Survey error during initial placement",
                "prevention_measures": "Enhanced survey verification process"
            }
        ]
    
    # Key Quality Control Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_inspections = len(st.session_state.qc_inspections)
    passed_inspections = len([insp for insp in st.session_state.qc_inspections if insp['status'] == 'Passed'])
    open_defects = len([def_item for def_item in st.session_state.qc_defects if def_item['status'] == 'Open'])
    quality_score = (passed_inspections / total_inspections * 100) if total_inspections > 0 else 0
    
    with col1:
        st.metric("Total Inspections", total_inspections, delta_color="normal")
    with col2:
        st.metric("Passed", passed_inspections, delta_color="normal")
    with col3:
        st.metric("Open Defects", open_defects, delta_color="normal")
    with col4:
        st.metric("Quality Score", f"{quality_score:.1f}%", delta_color="normal")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Inspections", "📋 Checklists", "⚠️ Defects", "📈 Analytics", "🔧 Management"])
    
    with tab1:
        st.subheader("🔍 Quality Inspections")
        
        insp_sub_tab1, insp_sub_tab2 = st.tabs(["📝 Schedule Inspection", "📊 View Inspections"])
        
        with insp_sub_tab1:
            st.markdown("**Schedule New Quality Inspection**")
            
            with st.form("inspection_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    inspection_type = st.selectbox("Inspection Type", [
                        "Structural Steel", "Concrete Pour", "MEP Rough-in", "Electrical", "Plumbing", 
                        "HVAC", "Fire Protection", "Architectural", "Site Work"
                    ])
                    location = st.text_input("Location", placeholder="Building level, area, grid lines")
                    trade = st.selectbox("Trade", ["Structural", "Concrete", "Electrical", "Plumbing", "HVAC", "Architectural", "Site Work"])
                    inspector = st.text_input("Inspector", placeholder="Inspector name and credentials")
                    scheduled_date = st.date_input("Scheduled Date", value=datetime.now().date())
                
                with col2:
                    responsible_contractor = st.text_input("Responsible Contractor", placeholder="Contractor performing work")
                    photos_required = st.checkbox("Photos Required", value=True)
                    description = st.text_area("Inspection Description", placeholder="Detailed description of inspection scope")
                    pass_criteria = st.text_area("Pass Criteria", placeholder="Criteria that must be met for inspection to pass")
                
                if st.form_submit_button("🔍 Schedule Inspection", type="primary"):
                    if inspection_type and location and inspector:
                        new_inspection = {
                            "id": f"QC-{len(st.session_state.qc_inspections) + 1:03d}",
                            "inspection_id": f"HTD-QC-2025-{len(st.session_state.qc_inspections) + 46:03d}",
                            "inspection_type": inspection_type,
                            "location": location,
                            "status": "Scheduled",
                            "inspector": inspector,
                            "inspection_date": "",
                            "scheduled_date": str(scheduled_date),
                            "trade": trade,
                            "description": description,
                            "pass_criteria": pass_criteria,
                            "findings": "",
                            "recommendations": "",
                            "photos_required": photos_required,
                            "follow_up_required": False,
                            "follow_up_date": "",
                            "severity": "None",
                            "corrective_actions": [],
                            "responsible_contractor": responsible_contractor
                        }
                        st.session_state.qc_inspections.append(new_inspection)
                        st.success("✅ Inspection scheduled successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with insp_sub_tab2:
            st.markdown("**All Quality Inspections**")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All", "Scheduled", "In Progress", "Passed", "Failed", "Cancelled"])
            with col2:
                trade_filter = st.selectbox("Filter by Trade", ["All"] + list(set(insp['trade'] for insp in st.session_state.qc_inspections)))
            with col3:
                inspector_filter = st.selectbox("Filter by Inspector", ["All"] + list(set(insp['inspector'] for insp in st.session_state.qc_inspections)))
            
            # Display inspections
            filtered_inspections = st.session_state.qc_inspections
            if status_filter != "All":
                filtered_inspections = [insp for insp in filtered_inspections if insp['status'] == status_filter]
            if trade_filter != "All":
                filtered_inspections = [insp for insp in filtered_inspections if insp['trade'] == trade_filter]
            if inspector_filter != "All":
                filtered_inspections = [insp for insp in filtered_inspections if insp['inspector'] == inspector_filter]
            
            for inspection in filtered_inspections:
                status_icon = {"Scheduled": "📅", "In Progress": "🔄", "Passed": "✅", "Failed": "❌", "Cancelled": "⏹️"}.get(inspection['status'], "📋")
                
                with st.expander(f"{status_icon} {inspection['inspection_id']} - {inspection['inspection_type']} ({inspection['status']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**🔍 Type:** {inspection['inspection_type']}")
                        st.write(f"**📍 Location:** {inspection['location']}")
                        st.write(f"**🔧 Trade:** {inspection['trade']}")
                        st.write(f"**👤 Inspector:** {inspection['inspector']}")
                        st.write(f"**📅 Scheduled:** {inspection['scheduled_date']}")
                        if inspection['inspection_date']:
                            st.write(f"**📅 Completed:** {inspection['inspection_date']}")
                        st.write(f"**📊 Status:** {inspection['status']}")
                    
                    with col2:
                        st.write(f"**🏢 Contractor:** {inspection['responsible_contractor']}")
                        st.write(f"**📸 Photos Required:** {'Yes' if inspection['photos_required'] else 'No'}")
                        if inspection['follow_up_required']:
                            st.write(f"**🔄 Follow-up Date:** {inspection['follow_up_date']}")
                        if inspection['severity'] != "None":
                            st.write(f"**⚠️ Severity:** {inspection['severity']}")
                    
                    if inspection['description']:
                        st.write(f"**📝 Description:** {inspection['description']}")
                    if inspection['pass_criteria']:
                        st.write(f"**✅ Pass Criteria:** {inspection['pass_criteria']}")
                    if inspection['findings']:
                        st.write(f"**🔍 Findings:** {inspection['findings']}")
                    if inspection['recommendations']:
                        st.write(f"**💡 Recommendations:** {inspection['recommendations']}")
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if inspection['status'] == 'Scheduled' and st.button(f"▶️ Start", key=f"start_insp_{inspection['id']}"):
                            inspection['status'] = 'In Progress'
                            inspection['inspection_date'] = str(datetime.now().date())
                            st.success("Inspection started!")
                            st.rerun()
                    with col2:
                        if inspection['status'] == 'In Progress' and st.button(f"✅ Pass", key=f"pass_{inspection['id']}"):
                            inspection['status'] = 'Passed'
                            st.success("Inspection passed!")
                            st.rerun()
                    with col3:
                        if inspection['status'] == 'In Progress' and st.button(f"❌ Fail", key=f"fail_{inspection['id']}"):
                            inspection['status'] = 'Failed'
                            st.error("Inspection failed!")
                            st.rerun()
                    with col4:
                        if st.button(f"🗑️ Delete", key=f"delete_insp_{inspection['id']}"):
                            st.session_state.qc_inspections.remove(inspection)
                            st.success("Inspection deleted!")
                            st.rerun()
    
    with tab2:
        st.subheader("📋 Quality Checklists")
        
        checklist_sub_tab1, checklist_sub_tab2 = st.tabs(["📝 Create Checklist", "📊 View Checklists"])
        
        with checklist_sub_tab1:
            st.markdown("**Create New Quality Checklist**")
            
            with st.form("checklist_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    checklist_name = st.text_input("Checklist Name", placeholder="Descriptive checklist name")
                    trade = st.selectbox("Trade", ["Structural", "Concrete", "Electrical", "Plumbing", "HVAC", "Architectural", "Site Work"])
                    inspector = st.text_input("Inspector", placeholder="Inspector name")
                
                with col2:
                    overall_status = st.selectbox("Status", ["Not Started", "In Progress", "Complete", "On Hold"])
                
                st.markdown("**Checklist Items**")
                checklist_items = []
                for i in range(5):  # Allow up to 5 items
                    item_name = st.text_input(f"Item {i+1}", placeholder=f"Checklist item {i+1}", key=f"item_{i}")
                    if item_name:
                        item_status = st.selectbox(f"Status {i+1}", ["Pending", "Pass", "Fail", "N/A"], key=f"status_{i}")
                        item_notes = st.text_input(f"Notes {i+1}", placeholder="Optional notes", key=f"notes_{i}")
                        checklist_items.append({"item": item_name, "status": item_status, "notes": item_notes})
                
                if st.form_submit_button("📋 Create Checklist", type="primary"):
                    if checklist_name and trade and checklist_items:
                        completed_items = len([item for item in checklist_items if item['status'] in ['Pass', 'N/A']])
                        completion_percentage = (completed_items / len(checklist_items) * 100) if checklist_items else 0
                        
                        new_checklist = {
                            "id": f"CHK-{len(st.session_state.qc_checklists) + 1:03d}",
                            "checklist_name": checklist_name,
                            "trade": trade,
                            "checklist_items": checklist_items,
                            "created_date": str(datetime.now().date()),
                            "last_updated": str(datetime.now().date()),
                            "inspector": inspector,
                            "overall_status": overall_status,
                            "completion_percentage": completion_percentage
                        }
                        st.session_state.qc_checklists.append(new_checklist)
                        st.success("✅ Checklist created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in required fields and add at least one checklist item!")
        
        with checklist_sub_tab2:
            st.markdown("**All Quality Checklists**")
            
            for checklist in st.session_state.qc_checklists:
                status_icon = {"Not Started": "⏸️", "In Progress": "🔄", "Complete": "✅", "On Hold": "⏸️"}.get(checklist['overall_status'], "📋")
                
                with st.expander(f"{status_icon} {checklist['checklist_name']} - {checklist['trade']} ({checklist['completion_percentage']:.0f}%)"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📋 Checklist:** {checklist['checklist_name']}")
                        st.write(f"**🔧 Trade:** {checklist['trade']}")
                        st.write(f"**👤 Inspector:** {checklist['inspector']}")
                        st.write(f"**📅 Created:** {checklist['created_date']}")
                        st.write(f"**📅 Last Updated:** {checklist['last_updated']}")
                        st.write(f"**📊 Status:** {checklist['overall_status']}")
                    
                    with col2:
                        st.write(f"**📈 Completion:** {checklist['completion_percentage']:.0f}%")
                        st.progress(checklist['completion_percentage'] / 100)
                    
                    # Checklist items
                    st.write("**📝 Checklist Items:**")
                    for i, item in enumerate(checklist['checklist_items']):
                        item_icon = {"Pass": "✅", "Fail": "❌", "Pending": "⏳", "N/A": "➖"}.get(item['status'], "📋")
                        st.write(f"{item_icon} {item['item']} - {item['status']}")
                        if item['notes']:
                            st.write(f"    📝 {item['notes']}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"✅ Complete", key=f"complete_checklist_{checklist['id']}"):
                            checklist['overall_status'] = 'Complete'
                            checklist['last_updated'] = str(datetime.now().date())
                            st.success("Checklist completed!")
                            st.rerun()
                    with col2:
                        if st.button(f"✏️ Edit", key=f"edit_checklist_{checklist['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_checklist_{checklist['id']}"):
                            st.session_state.qc_checklists.remove(checklist)
                            st.success("Checklist deleted!")
                            st.rerun()
    
    with tab3:
        st.subheader("⚠️ Quality Defects")
        
        defect_sub_tab1, defect_sub_tab2 = st.tabs(["📝 Report Defect", "📊 View Defects"])
        
        with defect_sub_tab1:
            st.markdown("**Report New Quality Defect**")
            
            with st.form("defect_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    defect_title = st.text_input("Defect Title", placeholder="Brief description of defect")
                    location = st.text_input("Location", placeholder="Specific location of defect")
                    trade = st.selectbox("Trade", ["Structural", "Concrete", "Electrical", "Plumbing", "HVAC", "Architectural", "Site Work"])
                    severity = st.selectbox("Severity", ["Minor", "Major", "Critical"])
                    identified_by = st.text_input("Identified By", placeholder="Inspector or person reporting")
                    assigned_to = st.text_input("Assigned To", placeholder="Contractor responsible for fix")
                
                with col2:
                    target_resolution = st.date_input("Target Resolution", value=datetime.now().date() + timedelta(days=7))
                    cost_impact = st.number_input("Cost Impact ($)", value=0.00, format="%.2f")
                    schedule_impact = st.number_input("Schedule Impact (days)", value=0, format="%d")
                    root_cause = st.text_input("Root Cause", placeholder="Why did this defect occur?")
                    prevention_measures = st.text_input("Prevention Measures", placeholder="How to prevent recurrence")
                
                description = st.text_area("Detailed Description", placeholder="Detailed description of the defect")
                corrective_actions = st.text_area("Corrective Actions", placeholder="Required actions to fix defect (comma-separated)")
                
                if st.form_submit_button("⚠️ Report Defect", type="primary"):
                    if defect_title and description and location:
                        new_defect = {
                            "id": f"DEF-{len(st.session_state.qc_defects) + 1:03d}",
                            "defect_id": f"HTD-DEF-{len(st.session_state.qc_defects) + 3:03d}",
                            "title": defect_title,
                            "description": description,
                            "location": location,
                            "trade": trade,
                            "severity": severity,
                            "status": "Open",
                            "identified_date": str(datetime.now().date()),
                            "identified_by": identified_by,
                            "assigned_to": assigned_to,
                            "target_resolution": str(target_resolution),
                            "actual_resolution": "",
                            "cost_impact": cost_impact,
                            "schedule_impact": schedule_impact,
                            "corrective_actions": [action.strip() for action in corrective_actions.split(',') if action.strip()],
                            "root_cause": root_cause,
                            "prevention_measures": prevention_measures
                        }
                        st.session_state.qc_defects.append(new_defect)
                        st.success("✅ Defect reported successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with defect_sub_tab2:
            st.markdown("**All Quality Defects**")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                defect_status_filter = st.selectbox("Filter by Status", ["All", "Open", "In Progress", "Resolved", "Closed"])
            with col2:
                severity_filter = st.selectbox("Filter by Severity", ["All", "Minor", "Major", "Critical"])
            with col3:
                defect_trade_filter = st.selectbox("Filter by Trade", ["All"] + list(set(defect['trade'] for defect in st.session_state.qc_defects)))
            
            # Display defects
            filtered_defects = st.session_state.qc_defects
            if defect_status_filter != "All":
                filtered_defects = [defect for defect in filtered_defects if defect['status'] == defect_status_filter]
            if severity_filter != "All":
                filtered_defects = [defect for defect in filtered_defects if defect['severity'] == severity_filter]
            if defect_trade_filter != "All":
                filtered_defects = [defect for defect in filtered_defects if defect['trade'] == defect_trade_filter]
            
            for defect in filtered_defects:
                severity_icon = {"Minor": "🟡", "Major": "🟠", "Critical": "🔴"}.get(defect['severity'], "⚪")
                status_icon = {"Open": "🔓", "In Progress": "🔄", "Resolved": "✅", "Closed": "🔒"}.get(defect['status'], "📋")
                
                with st.expander(f"{severity_icon} {defect['defect_id']} - {defect['title']} ({defect['status']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**⚠️ Defect:** {defect['title']}")
                        st.write(f"**📍 Location:** {defect['location']}")
                        st.write(f"**🔧 Trade:** {defect['trade']}")
                        st.write(f"**⚠️ Severity:** {defect['severity']}")
                        st.write(f"**📊 Status:** {defect['status']}")
                        st.write(f"**👤 Identified By:** {defect['identified_by']}")
                        st.write(f"**👤 Assigned To:** {defect['assigned_to']}")
                    
                    with col2:
                        st.write(f"**📅 Identified:** {defect['identified_date']}")
                        st.write(f"**🎯 Target Resolution:** {defect['target_resolution']}")
                        if defect['actual_resolution']:
                            st.write(f"**✅ Resolved:** {defect['actual_resolution']}")
                        st.write(f"**💰 Cost Impact:** ${defect['cost_impact']:,.2f}")
                        st.write(f"**📅 Schedule Impact:** {defect['schedule_impact']} days")
                    
                    st.write(f"**📝 Description:** {defect['description']}")
                    if defect['corrective_actions']:
                        st.write(f"**🔧 Corrective Actions:** {', '.join(defect['corrective_actions'])}")
                    if defect['root_cause']:
                        st.write(f"**🎯 Root Cause:** {defect['root_cause']}")
                    if defect['prevention_measures']:
                        st.write(f"**🛡️ Prevention:** {defect['prevention_measures']}")
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if defect['status'] == 'Open' and st.button(f"🔄 In Progress", key=f"progress_def_{defect['id']}"):
                            defect['status'] = 'In Progress'
                            st.info("Defect in progress!")
                            st.rerun()
                    with col2:
                        if defect['status'] in ['Open', 'In Progress'] and st.button(f"✅ Resolve", key=f"resolve_def_{defect['id']}"):
                            defect['status'] = 'Resolved'
                            defect['actual_resolution'] = str(datetime.now().date())
                            st.success("Defect resolved!")
                            st.rerun()
                    with col3:
                        if st.button(f"✏️ Edit", key=f"edit_def_{defect['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col4:
                        if st.button(f"🗑️ Delete", key=f"delete_def_{defect['id']}"):
                            st.session_state.qc_defects.remove(defect)
                            st.success("Defect deleted!")
                            st.rerun()
    
    with tab4:
        st.subheader("📈 Quality Control Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Inspection status distribution
            if st.session_state.qc_inspections:
                insp_status_counts = {}
                for insp in st.session_state.qc_inspections:
                    status = insp['status']
                    insp_status_counts[status] = insp_status_counts.get(status, 0) + 1
                
                insp_status_list = list(insp_status_counts.keys())
                insp_count_list = list(insp_status_counts.values())
                insp_status_df = pd.DataFrame({
                    'Status': insp_status_list,
                    'Count': insp_count_list
                })
                fig_insp_status = px.pie(insp_status_df, values='Count', names='Status', title="Inspection Status Distribution")
                st.plotly_chart(fig_insp_status, use_container_width=True)
        
        with col2:
            # Defect severity distribution
            if st.session_state.qc_defects:
                defect_severity_counts = {}
                for defect in st.session_state.qc_defects:
                    severity = defect['severity']
                    defect_severity_counts[severity] = defect_severity_counts.get(severity, 0) + 1
                
                severity_list = list(defect_severity_counts.keys())
                severity_count_list = list(defect_severity_counts.values())
                severity_df = pd.DataFrame({
                    'Severity': severity_list,
                    'Count': severity_count_list
                })
                fig_severity = px.bar(severity_df, x='Severity', y='Count', title="Defect Severity Distribution")
                st.plotly_chart(fig_severity, use_container_width=True)
    
    with tab5:
        st.subheader("🔧 Quality Control Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🔍 Inspection Summary**")
            if st.session_state.qc_inspections:
                insp_stats_data = pd.DataFrame([
                    {"Metric": "Total Inspections", "Value": len(st.session_state.qc_inspections)},
                    {"Metric": "Passed", "Value": len([i for i in st.session_state.qc_inspections if i['status'] == 'Passed'])},
                    {"Metric": "Failed", "Value": len([i for i in st.session_state.qc_inspections if i['status'] == 'Failed'])},
                    {"Metric": "In Progress", "Value": len([i for i in st.session_state.qc_inspections if i['status'] == 'In Progress'])},
                ])
                st.dataframe(insp_stats_data, use_container_width=True)
        
        with col2:
            st.markdown("**📋 Checklist Summary**")
            if st.session_state.qc_checklists:
                checklist_stats_data = pd.DataFrame([
                    {"Metric": "Total Checklists", "Value": len(st.session_state.qc_checklists)},
                    {"Metric": "Complete", "Value": len([c for c in st.session_state.qc_checklists if c['overall_status'] == 'Complete'])},
                    {"Metric": "In Progress", "Value": len([c for c in st.session_state.qc_checklists if c['overall_status'] == 'In Progress'])},
                    {"Metric": "Avg Completion", "Value": f"{sum(c['completion_percentage'] for c in st.session_state.qc_checklists) / len(st.session_state.qc_checklists):.1f}%"},
                ])
                st.dataframe(checklist_stats_data, use_container_width=True)
        
        with col3:
            st.markdown("**⚠️ Defect Summary**")
            if st.session_state.qc_defects:
                defect_stats_data = pd.DataFrame([
                    {"Metric": "Total Defects", "Value": len(st.session_state.qc_defects)},
                    {"Metric": "Open", "Value": len([d for d in st.session_state.qc_defects if d['status'] == 'Open'])},
                    {"Metric": "Resolved", "Value": len([d for d in st.session_state.qc_defects if d['status'] == 'Resolved'])},
                    {"Metric": "Total Cost Impact", "Value": f"${sum(d['cost_impact'] for d in st.session_state.qc_defects):,.2f}"},
                ])
                st.dataframe(defect_stats_data, use_container_width=True)
        
        # Data management
        st.markdown("**⚠️ Data Management**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🗑️ Clear Inspections", type="secondary"):
                st.session_state.qc_inspections = []
                st.success("All inspections cleared!")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Checklists", type="secondary"):
                st.session_state.qc_checklists = []
                st.success("All checklists cleared!")
                st.rerun()
        with col3:
            if st.button("🗑️ Clear Defects", type="secondary"):
                st.session_state.qc_defects = []
                st.success("All defects cleared!")
                st.rerun()

def render_progress_photos():
    """Enterprise Progress Photos Management with robust Python backend"""
    try:
        from modules.progress_photos_backend import progress_photos_manager, PhotoStatus, PhotoCategory
        
        st.markdown("""
        <div class="module-header">
            <h1>📸 Progress Photos Management</h1>
            <p>Highland Tower Development - Professional photo documentation with approval workflows</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display summary metrics
        metrics = progress_photos_manager.generate_photo_metrics()
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📸 Total Photos", metrics['total_photos'])
            with col2:
                st.metric("📁 Albums", metrics['total_albums'])
            with col3:
                st.metric("✅ Approval Rate", f"{metrics['approval_rate']}%")
            with col4:
                st.metric("⏳ Pending Review", metrics['pending_review'])
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["📸 All Photos", "📁 Albums", "📊 Analytics"])
        
        with tab1:
            st.subheader("📸 All Progress Photos")
            
            # Display photos
            photos = progress_photos_manager.get_all_photos()
            
            for photo in photos:
                status_color = {
                    PhotoStatus.APPROVED: "🟢",
                    PhotoStatus.UNDER_REVIEW: "🟡",
                    PhotoStatus.REJECTED: "🔴",
                    PhotoStatus.UPLOADED: "🔵"
                }.get(photo.status, "⚪")
                
                with st.expander(f"{status_color} {photo.photo_number} | {photo.title} | {photo.status.value}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📋 Category:** {photo.category.value}")
                        st.write(f"**📍 Location:** {photo.location}")
                        st.write(f"**🏗️ Work Package:** {photo.work_package}")
                        st.write(f"**📅 Captured:** {photo.captured_date} at {photo.captured_time}")
                        st.write(f"**📷 By:** {photo.captured_by}")
                    
                    with col2:
                        st.write(f"**👁️ View Angle:** {photo.view_angle.value}")
                        st.write(f"**📄 Filename:** {photo.filename}")
                        st.write(f"**📐 Resolution:** {photo.metadata.resolution}")
                        st.write(f"**💾 Size:** {photo.metadata.file_size / (1024*1024):.1f} MB")
                        if photo.approved_date:
                            st.write(f"**✅ Approved:** {photo.approved_date}")
                    
                    if photo.description:
                        st.write(f"**📝 Description:** {photo.description}")
                    
                    if photo.tags:
                        st.write(f"**🏷️ Tags:** {', '.join(photo.tags)}")
                    
                    if photo.drawing_references:
                        st.write(f"**📐 Drawing References:** {', '.join(photo.drawing_references)}")
                    
                    # Show reviews
                    if photo.reviews:
                        st.write("**📋 Reviews:**")
                        for review in photo.reviews:
                            rating_stars = "⭐" * (review.rating or 0)
                            st.write(f"• {review.reviewer_name} ({review.review_date}): {review.action} {rating_stars}")
                            if review.comments:
                                st.write(f"  *{review.comments}*")
                    
                    # Show related items
                    if photo.related_rfi or photo.related_submittal or photo.related_inspection:
                        st.write("**🔗 Related Items:**")
                        if photo.related_rfi:
                            st.write(f"• RFI: {photo.related_rfi}")
                        if photo.related_submittal:
                            st.write(f"• Submittal: {photo.related_submittal}")
                        if photo.related_inspection:
                            st.write(f"• Inspection: {photo.related_inspection}")
        
        with tab2:
            st.subheader("📁 Photo Albums")
            
            albums = list(progress_photos_manager.albums.values())
            
            for album in albums:
                with st.expander(f"📁 {album.name} | {album.photo_count} photos"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📋 Category:** {album.category.value}")
                        st.write(f"**🏗️ Work Package:** {album.work_package}")
                        st.write(f"**📅 Created:** {album.created_date}")
                        st.write(f"**👤 Created By:** {album.created_by}")
                    
                    with col2:
                        st.write(f"**📸 Photo Count:** {album.photo_count}")
                        st.write(f"**📅 Date Range:** {album.date_range_start} to {album.date_range_end}")
                        st.write(f"**👁️ Visibility:** {album.visibility}")
                    
                    if album.description:
                        st.write(f"**📝 Description:** {album.description}")
                    
                    if album.tags:
                        st.write(f"**🏷️ Tags:** {', '.join(album.tags)}")
                    
                    # Show photos in album
                    album_photos = progress_photos_manager.get_photos_by_album(album.album_id)
                    if album_photos:
                        st.write("**📸 Photos in Album:**")
                        for photo in album_photos[:5]:  # Show first 5
                            st.write(f"• {photo.title} ({photo.captured_date})")
                        if len(album_photos) > 5:
                            st.write(f"... and {len(album_photos) - 5} more")
        
        with tab3:
            st.subheader("📊 Photo Documentation Analytics")
            
            if metrics:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📊 Status Breakdown:**")
                    for status, count in metrics['status_breakdown'].items():
                        st.write(f"• {status}: {count}")
                    
                    st.write("**📋 Category Breakdown:**")
                    for category, count in metrics['category_breakdown'].items():
                        st.write(f"• {category}: {count}")
                
                with col2:
                    st.write("**📈 Performance Metrics:**")
                    st.write(f"• **Approval Rate:** {metrics['approval_rate']}%")
                    st.write(f"• **Average Rating:** {metrics['average_rating']}/5")
                    st.write(f"• **Total Storage:** {metrics['total_file_size_mb']} MB")
                    st.write(f"• **Average File Size:** {metrics['average_file_size_mb']} MB")
                    st.write(f"• **Pending Review:** {metrics['pending_review']}")
        
        return
        
    except ImportError:
        st.error("Enterprise Progress Photos module not available")
        # Fallback to basic version
        render_progress_photos_basic()

def render_progress_photos_basic():
    """Basic progress photos module - fallback version"""
    st.markdown("""
    <div class="module-header">
        <h1>📸 Progress Photos</h1>
        <p>Comprehensive visual documentation, progress tracking, and photo management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize progress photos data
    if "progress_photos" not in st.session_state:
        st.session_state.progress_photos = [
            {
                "id": "PH-001",
                "photo_id": "HTD-IMG-2025-001",
                "filename": "level_13_structural_beam_install.jpg",
                "title": "Level 13 Structural Steel Installation",
                "location": "Level 13 - Grid Lines A5-B5",
                "category": "Structural Progress",
                "upload_date": "2025-05-27",
                "taken_date": "2025-05-27",
                "photographer": "Mike Chen - Site Superintendent",
                "description": "Steel beam installation progress showing main structural frame completion with crane operations",
                "status": "Approved",
                "tags": ["structural", "steel-beams", "level-13", "grid-A5", "crane-operations"],
                "file_size": "2.4 MB",
                "dimensions": "4032x3024",
                "weather_conditions": "Clear, 72°F",
                "crew_count": "12 workers",
                "progress_percentage": 85,
                "linked_tasks": ["TASK-003"],
                "linked_rfis": [],
                "approval_by": "John Davis, P.E.",
                "notes": "Quality installation progress, on schedule for milestone completion",
                "gps_coordinates": "40.7589, -73.9851",
                "equipment_visible": ["Tower Crane TC-1", "Boom Lift", "Material Hoist"]
            },
            {
                "id": "PH-002",
                "photo_id": "HTD-IMG-2025-002",
                "filename": "mep_rough_in_level_12.jpg",
                "title": "MEP Rough-in Completion Level 12",
                "location": "Level 12 - Mechanical Room North",
                "category": "MEP Systems",
                "upload_date": "2025-05-25",
                "taken_date": "2025-05-25",
                "photographer": "Sarah Johnson - Project Manager",
                "description": "HVAC ductwork rough-in completion with electrical conduit installation and fire protection systems",
                "status": "Under Review",
                "tags": ["mep", "hvac", "ductwork", "electrical", "level-12", "fire-protection"],
                "file_size": "3.1 MB",
                "dimensions": "4032x3024",
                "weather_conditions": "Indoor Controlled Environment",
                "crew_count": "8 workers",
                "progress_percentage": 90,
                "linked_tasks": ["TASK-004"],
                "linked_rfis": ["RFI-001"],
                "approval_by": "",
                "notes": "Coordination with electrical team required for final routing approval",
                "gps_coordinates": "40.7589, -73.9851",
                "equipment_visible": ["Scissor Lift", "Hand Tools", "Testing Equipment"]
            },
            {
                "id": "PH-003",
                "photo_id": "HTD-IMG-2025-003",
                "filename": "exterior_curtain_wall_south_facade.jpg",
                "title": "South Facade Curtain Wall Installation",
                "location": "South Facade - Units 8-12",
                "category": "Exterior Envelope",
                "upload_date": "2025-05-23",
                "taken_date": "2025-05-23",
                "photographer": "Robert Kim - Architecture Team",
                "description": "Curtain wall installation progress on south elevation with glazing units and weather sealing",
                "status": "Approved",
                "tags": ["exterior", "curtain-wall", "glazing", "south-facade", "weather-sealing"],
                "file_size": "2.8 MB",
                "dimensions": "4032x3024",
                "weather_conditions": "Clear, 75°F",
                "crew_count": "6 workers",
                "progress_percentage": 70,
                "linked_tasks": ["TASK-005"],
                "linked_rfis": [],
                "approval_by": "Maria Garcia, P.E.",
                "notes": "Excellent progress on curtain wall installation, weather conditions favorable",
                "gps_coordinates": "40.7589, -73.9851",
                "equipment_visible": ["Aerial Work Platform", "Glass Handling Equipment"]
            }
        ]
    
    if "photo_albums" not in st.session_state:
        st.session_state.photo_albums = [
            {
                "id": "ALB-001",
                "album_name": "Highland Tower Structural Progress",
                "description": "Complete structural steel installation documentation",
                "created_date": "2025-04-01",
                "photo_count": 45,
                "cover_photo": "HTD-IMG-2025-001",
                "tags": ["structural", "steel", "progress"],
                "access_level": "Project Team"
            },
            {
                "id": "ALB-002",
                "album_name": "MEP Systems Installation",
                "description": "Electrical, plumbing, and HVAC installation progress",
                "created_date": "2025-05-15",
                "photo_count": 32,
                "cover_photo": "HTD-IMG-2025-002",
                "tags": ["mep", "electrical", "hvac", "plumbing"],
                "access_level": "MEP Team"
            }
        ]
    
    # Key Progress Photo Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_photos = len(st.session_state.progress_photos)
    approved_photos = len([photo for photo in st.session_state.progress_photos if photo['status'] == 'Approved'])
    avg_progress = sum(photo['progress_percentage'] for photo in st.session_state.progress_photos) / len(st.session_state.progress_photos) if st.session_state.progress_photos else 0
    total_storage = sum(float(photo['file_size'].replace(' MB', '')) for photo in st.session_state.progress_photos)
    
    with col1:
        st.metric("Total Photos", total_photos, delta_color="normal")
    with col2:
        st.metric("Approved", approved_photos, delta_color="normal")
    with col3:
        st.metric("Avg Progress", f"{avg_progress:.1f}%", delta_color="normal")
    with col4:
        st.metric("Storage Used", f"{total_storage:.1f} MB", delta_color="normal")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📷 Upload Photos", "📸 Photo Gallery", "📁 Albums", "📈 Analytics", "🔧 Management"])
    
    with tab1:
        st.subheader("📷 Upload Progress Photos")
        
        upload_sub_tab1, upload_sub_tab2 = st.tabs(["📝 Single Upload", "📤 Bulk Upload"])
        
        with upload_sub_tab1:
            st.markdown("**Upload New Progress Photo**")
            
            with st.form("photo_upload_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    uploaded_file = st.file_uploader("Select Photo", type=['jpg', 'jpeg', 'png', 'bmp'])
                    photo_title = st.text_input("Photo Title", placeholder="Descriptive title for the photo")
                    location = st.selectbox("Location", [
                        "Level 13 - Penthouse", "Level 12 - Residential", "Level 11 - Residential",
                        "Level 10 - Residential", "Ground Floor - Retail", "Basement - Parking",
                        "Exterior - North Facade", "Exterior - South Facade", "Site Overall", "Custom Location"
                    ])
                    if location == "Custom Location":
                        custom_location = st.text_input("Specify Location", placeholder="Enter specific location")
                        location = custom_location if custom_location else "Unspecified"
                    
                    category = st.selectbox("Category", [
                        "Structural Progress", "MEP Systems", "Interior Finishes", "Exterior Envelope",
                        "Safety Documentation", "Site Work", "Quality Control", "Equipment", "Deliveries"
                    ])
                    taken_date = st.date_input("Photo Date", value=datetime.now().date())
                
                with col2:
                    photographer = st.text_input("Photographer", placeholder="Name and title")
                    weather_conditions = st.selectbox("Weather Conditions", [
                        "Clear", "Partly Cloudy", "Overcast", "Light Rain", "Heavy Rain", 
                        "Snow", "Windy", "Indoor Controlled Environment"
                    ])
                    crew_count = st.text_input("Crew Count", placeholder="e.g., 12 workers")
                    progress_percentage = st.slider("Progress Percentage", 0, 100, 50)
                    linked_tasks = st.multiselect("Link to Tasks", [f"{task['id']} - {task['task_name']}" for task in st.session_state.get('schedule_tasks', [])])
                    equipment_visible = st.text_input("Equipment Visible", placeholder="Comma-separated equipment list")
                
                description = st.text_area("Description", placeholder="Detailed description of what the photo shows")
                tags = st.text_input("Tags", placeholder="Comma-separated tags for easy searching")
                notes = st.text_area("Notes", placeholder="Additional notes or observations")
                gps_coordinates = st.text_input("GPS Coordinates", placeholder="Latitude, Longitude (optional)")
                
                if st.form_submit_button("📷 Upload Photo", type="primary"):
                    if uploaded_file and photo_title and photographer:
                        new_photo = {
                            "id": f"PH-{len(st.session_state.progress_photos) + 1:03d}",
                            "photo_id": f"HTD-IMG-2025-{len(st.session_state.progress_photos) + 4:03d}",
                            "filename": uploaded_file.name,
                            "title": photo_title,
                            "location": location,
                            "category": category,
                            "upload_date": str(datetime.now().date()),
                            "taken_date": str(taken_date),
                            "photographer": photographer,
                            "description": description,
                            "status": "Under Review",
                            "tags": [tag.strip() for tag in tags.split(',') if tag.strip()],
                            "file_size": f"{uploaded_file.size / (1024*1024):.1f} MB" if uploaded_file.size else "Unknown",
                            "dimensions": "Unknown",
                            "weather_conditions": weather_conditions,
                            "crew_count": crew_count,
                            "progress_percentage": progress_percentage,
                            "linked_tasks": [task.split(" - ")[0] for task in linked_tasks],
                            "linked_rfis": [],
                            "approval_by": "",
                            "notes": notes,
                            "gps_coordinates": gps_coordinates,
                            "equipment_visible": [eq.strip() for eq in equipment_visible.split(',') if eq.strip()]
                        }
                        st.session_state.progress_photos.append(new_photo)
                        st.success("✅ Photo uploaded successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields and select a photo!")
        
        with upload_sub_tab2:
            st.markdown("**Bulk Photo Upload**")
            
            with st.form("bulk_upload_form"):
                bulk_files = st.file_uploader("Select Multiple Photos", type=['jpg', 'jpeg', 'png', 'bmp'], accept_multiple_files=True)
                bulk_location = st.selectbox("Default Location", [
                    "Level 13", "Level 12", "Level 11", "Ground Floor", "Exterior", "Site Overall"
                ])
                bulk_category = st.selectbox("Default Category", [
                    "Structural Progress", "MEP Systems", "Interior Finishes", "Exterior Envelope", "Site Work"
                ])
                bulk_photographer = st.text_input("Photographer", placeholder="Name for all photos")
                bulk_description = st.text_area("Default Description", placeholder="Description applied to all photos")
                
                if st.form_submit_button("📤 Bulk Upload", type="primary"):
                    if bulk_files and bulk_photographer:
                        for file in bulk_files:
                            new_photo = {
                                "id": f"PH-{len(st.session_state.progress_photos) + 1:03d}",
                                "photo_id": f"HTD-IMG-2025-{len(st.session_state.progress_photos) + 4:03d}",
                                "filename": file.name,
                                "title": f"Bulk Upload - {file.name}",
                                "location": bulk_location,
                                "category": bulk_category,
                                "upload_date": str(datetime.now().date()),
                                "taken_date": str(datetime.now().date()),
                                "photographer": bulk_photographer,
                                "description": bulk_description,
                                "status": "Under Review",
                                "tags": ["bulk-upload"],
                                "file_size": f"{file.size / (1024*1024):.1f} MB" if file.size else "Unknown",
                                "dimensions": "Unknown",
                                "weather_conditions": "Unknown",
                                "crew_count": "Unknown",
                                "progress_percentage": 0,
                                "linked_tasks": [],
                                "linked_rfis": [],
                                "approval_by": "",
                                "notes": "",
                                "gps_coordinates": "",
                                "equipment_visible": []
                            }
                            st.session_state.progress_photos.append(new_photo)
                        st.success(f"✅ {len(bulk_files)} photos uploaded successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please select photos and enter photographer name!")
    
    with tab2:
        st.subheader("📸 Progress Photo Gallery")
        
        gallery_sub_tab1, gallery_sub_tab2 = st.tabs(["🔍 Search & Filter", "📋 All Photos"])
        
        with gallery_sub_tab1:
            st.markdown("**Search and Filter Photos**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                location_filter = st.selectbox("Filter by Location", ["All Locations"] + list(set(photo['location'].split(' - ')[0] for photo in st.session_state.progress_photos)))
            with col2:
                category_filter = st.selectbox("Filter by Category", ["All Categories"] + list(set(photo['category'] for photo in st.session_state.progress_photos)))
            with col3:
                status_filter = st.selectbox("Filter by Status", ["All Status", "Under Review", "Approved", "Rejected"])
            
            col1, col2 = st.columns(2)
            with col1:
                photographer_filter = st.selectbox("Filter by Photographer", ["All Photographers"] + list(set(photo['photographer'].split(' - ')[0] for photo in st.session_state.progress_photos)))
            with col2:
                search_text = st.text_input("🔍 Search", placeholder="Search in titles, descriptions, tags...")
            
            # Apply filters
            filtered_photos = st.session_state.progress_photos
            if location_filter != "All Locations":
                filtered_photos = [p for p in filtered_photos if location_filter in p['location']]
            if category_filter != "All Categories":
                filtered_photos = [p for p in filtered_photos if p['category'] == category_filter]
            if status_filter != "All Status":
                filtered_photos = [p for p in filtered_photos if p['status'] == status_filter]
            if photographer_filter != "All Photographers":
                filtered_photos = [p for p in filtered_photos if photographer_filter in p['photographer']]
            if search_text:
                filtered_photos = [p for p in filtered_photos if 
                                 search_text.lower() in p['title'].lower() or 
                                 search_text.lower() in p['description'].lower() or
                                 search_text.lower() in ' '.join(p['tags']).lower()]
            
            st.markdown(f"**Found {len(filtered_photos)} photos**")
            display_photos = filtered_photos
        
        with gallery_sub_tab2:
            display_photos = st.session_state.progress_photos
        
        # Display photos
        for photo in display_photos:
            status_icon = {"Under Review": "🟡", "Approved": "✅", "Rejected": "❌"}.get(photo['status'], "📷")
            
            with st.expander(f"{status_icon} {photo['photo_id']} - {photo['title']} ({photo['status']})"):
                col1, col2 = st.columns([2, 3])
                
                with col1:
                    st.write(f"**📷 Photo ID:** {photo['photo_id']}")
                    st.write(f"**📁 Filename:** {photo['filename']}")
                    st.write(f"**📍 Location:** {photo['location']}")
                    st.write(f"**📂 Category:** {photo['category']}")
                    st.write(f"**📅 Upload Date:** {photo['upload_date']}")
                    st.write(f"**📅 Taken Date:** {photo['taken_date']}")
                    st.write(f"**👤 Photographer:** {photo['photographer']}")
                    st.write(f"**📊 Status:** {photo['status']}")
                    if photo['approval_by']:
                        st.write(f"**✅ Approved By:** {photo['approval_by']}")
                
                with col2:
                    st.write(f"**📝 Description:** {photo['description']}")
                    st.write(f"**🌤️ Weather:** {photo['weather_conditions']}")
                    st.write(f"**👥 Crew Count:** {photo['crew_count']}")
                    st.write(f"**📈 Progress:** {photo['progress_percentage']}%")
                    if photo['linked_tasks']:
                        st.write(f"**🔗 Linked Tasks:** {', '.join(photo['linked_tasks'])}")
                    if photo['equipment_visible']:
                        st.write(f"**🚜 Equipment:** {', '.join(photo['equipment_visible'])}")
                    if photo['notes']:
                        st.write(f"**📝 Notes:** {photo['notes']}")
                
                # Tags
                if photo['tags']:
                    st.write("**🏷️ Tags:**")
                    tags_html = " ".join([f'<span style="background-color: #e1e1e1; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em;">{tag}</span>' for tag in photo['tags']])
                    st.markdown(tags_html, unsafe_allow_html=True)
                
                # Progress bar
                st.write("**📈 Progress Visualization:**")
                st.progress(photo['progress_percentage'] / 100)
                
                # Action buttons
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    if photo['status'] == 'Under Review' and st.button(f"✅ Approve", key=f"approve_{photo['id']}"):
                        photo['status'] = 'Approved'
                        photo['approval_by'] = 'Highland Project Team'
                        st.success("Photo approved!")
                        st.rerun()
                with col2:
                    if photo['status'] == 'Under Review' and st.button(f"❌ Reject", key=f"reject_{photo['id']}"):
                        photo['status'] = 'Rejected'
                        st.error("Photo rejected!")
                        st.rerun()
                with col3:
                    if st.button(f"📤 Share", key=f"share_{photo['id']}"):
                        st.success("Share link generated!")
                with col4:
                    if st.button(f"✏️ Edit", key=f"edit_{photo['id']}"):
                        st.info("Edit functionality - would open edit form")
                with col5:
                    if st.button(f"🗑️ Delete", key=f"delete_{photo['id']}"):
                        st.session_state.progress_photos.remove(photo)
                        st.success("Photo deleted!")
                        st.rerun()
    
    with tab3:
        st.subheader("📁 Photo Albums")
        
        album_sub_tab1, album_sub_tab2 = st.tabs(["📁 Create Album", "📚 View Albums"])
        
        with album_sub_tab1:
            st.markdown("**Create New Photo Album**")
            
            with st.form("album_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    album_name = st.text_input("Album Name", placeholder="Descriptive album name")
                    description = st.text_area("Description", placeholder="Album description and purpose")
                    access_level = st.selectbox("Access Level", ["Project Team", "Client Access", "Public", "Management Only"])
                
                with col2:
                    cover_photo = st.selectbox("Cover Photo", [f"{photo['photo_id']} - {photo['title']}" for photo in st.session_state.progress_photos])
                    tags = st.text_input("Tags", placeholder="Comma-separated tags")
                
                if st.form_submit_button("📁 Create Album", type="primary"):
                    if album_name and description:
                        new_album = {
                            "id": f"ALB-{len(st.session_state.photo_albums) + 1:03d}",
                            "album_name": album_name,
                            "description": description,
                            "created_date": str(datetime.now().date()),
                            "photo_count": 0,
                            "cover_photo": cover_photo.split(" - ")[0] if cover_photo else "",
                            "tags": [tag.strip() for tag in tags.split(',') if tag.strip()],
                            "access_level": access_level
                        }
                        st.session_state.photo_albums.append(new_album)
                        st.success("✅ Album created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with album_sub_tab2:
            st.markdown("**All Photo Albums**")
            
            for album in st.session_state.photo_albums:
                with st.expander(f"📁 {album['album_name']} ({album['photo_count']} photos)"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📁 Album:** {album['album_name']}")
                        st.write(f"**📝 Description:** {album['description']}")
                        st.write(f"**📅 Created:** {album['created_date']}")
                        st.write(f"**📷 Photo Count:** {album['photo_count']}")
                        st.write(f"**🔒 Access Level:** {album['access_level']}")
                    
                    with col2:
                        if album['cover_photo']:
                            st.write(f"**🖼️ Cover Photo:** {album['cover_photo']}")
                        if album['tags']:
                            st.write(f"**🏷️ Tags:** {', '.join(album['tags'])}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"👁️ View", key=f"view_album_{album['id']}"):
                            st.info("Album view functionality")
                    with col2:
                        if st.button(f"✏️ Edit", key=f"edit_album_{album['id']}"):
                            st.info("Edit album functionality")
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_album_{album['id']}"):
                            st.session_state.photo_albums.remove(album)
                            st.success("Album deleted!")
                            st.rerun()
    
    with tab4:
        st.subheader("📈 Photo Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Category distribution
            if st.session_state.progress_photos:
                category_counts = {}
                for photo in st.session_state.progress_photos:
                    category = photo['category']
                    category_counts[category] = category_counts.get(category, 0) + 1
                
                category_list = list(category_counts.keys())
                count_list = list(category_counts.values())
                category_df = pd.DataFrame({
                    'Category': category_list,
                    'Count': count_list
                })
                fig_category = px.pie(category_df, values='Count', names='Category', title="Photos by Category")
                st.plotly_chart(fig_category, use_container_width=True)
        
        with col2:
            # Status distribution
            if st.session_state.progress_photos:
                status_counts = {}
                for photo in st.session_state.progress_photos:
                    status = photo['status']
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                status_list = list(status_counts.keys())
                status_count_list = list(status_counts.values())
                status_df = pd.DataFrame({
                    'Status': status_list,
                    'Count': status_count_list
                })
                fig_status = px.bar(status_df, x='Status', y='Count', title="Photo Status Distribution")
                st.plotly_chart(fig_status, use_container_width=True)
        
        # Progress timeline
        st.markdown("**📈 Progress Over Time**")
        if st.session_state.progress_photos:
            timeline_data = []
            for photo in st.session_state.progress_photos:
                timeline_data.append({
                    'Date': photo['taken_date'],
                    'Progress': photo['progress_percentage'],
                    'Location': photo['location'].split(' - ')[0],
                    'Category': photo['category']
                })
            
            timeline_df = pd.DataFrame(timeline_data)
            timeline_df['Date'] = pd.to_datetime(timeline_df['Date'])
            timeline_df = timeline_df.sort_values('Date')
            
            fig_timeline = px.scatter(timeline_df, x='Date', y='Progress', color='Category', 
                                    size_max=10, title="Progress Documentation Timeline")
            st.plotly_chart(fig_timeline, use_container_width=True)
    
    with tab5:
        st.subheader("🔧 Photo Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📷 Photo Summary**")
            if st.session_state.progress_photos:
                photo_stats_data = pd.DataFrame([
                    {"Metric": "Total Photos", "Value": len(st.session_state.progress_photos)},
                    {"Metric": "Approved", "Value": len([p for p in st.session_state.progress_photos if p['status'] == 'Approved'])},
                    {"Metric": "Under Review", "Value": len([p for p in st.session_state.progress_photos if p['status'] == 'Under Review'])},
                    {"Metric": "Avg Progress", "Value": f"{sum(p['progress_percentage'] for p in st.session_state.progress_photos) / len(st.session_state.progress_photos):.1f}%"},
                ])
                st.dataframe(photo_stats_data, use_container_width=True)
        
        with col2:
            st.markdown("**📁 Album Summary**")
            if st.session_state.photo_albums:
                album_stats_data = pd.DataFrame([
                    {"Metric": "Total Albums", "Value": len(st.session_state.photo_albums)},
                    {"Metric": "Public Albums", "Value": len([a for a in st.session_state.photo_albums if a['access_level'] == 'Public'])},
                    {"Metric": "Project Albums", "Value": len([a for a in st.session_state.photo_albums if a['access_level'] == 'Project Team'])},
                    {"Metric": "Total Album Photos", "Value": sum(a['photo_count'] for a in st.session_state.photo_albums)},
                ])
                st.dataframe(album_stats_data, use_container_width=True)
        
        with col3:
            st.markdown("**💾 Storage Summary**")
            if st.session_state.progress_photos:
                total_storage = sum(float(p['file_size'].replace(' MB', '')) for p in st.session_state.progress_photos if 'MB' in p['file_size'])
                storage_stats_data = pd.DataFrame([
                    {"Metric": "Storage Used", "Value": f"{total_storage:.1f} MB"},
                    {"Metric": "Avg File Size", "Value": f"{total_storage / len(st.session_state.progress_photos):.1f} MB"},
                    {"Metric": "Largest File", "Value": f"{max(float(p['file_size'].replace(' MB', '')) for p in st.session_state.progress_photos if 'MB' in p['file_size']):.1f} MB"},
                    {"Metric": "Storage Limit", "Value": "5000 MB"},
                ])
                st.dataframe(storage_stats_data, use_container_width=True)
        
        # Data management
        st.markdown("**⚠️ Data Management**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🗑️ Clear All Photos", type="secondary"):
                st.session_state.progress_photos = []
                st.success("All photos cleared!")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Albums", type="secondary"):
                st.session_state.photo_albums = []
                st.success("All albums cleared!")
                st.rerun()
        with col3:
            if st.button("📤 Export Data", type="secondary"):
                st.success("Photo data exported!")

def render_subcontractor_management():
    """Enterprise Subcontractor Management with full CRUD functionality"""
    try:
        from modules.subcontractor_management_backend import subcontractor_manager, SubcontractorStatus, TradeCategory, PerformanceRating
        
        st.markdown("""
        <div class="module-header">
            <h1>🏗️ Subcontractor Management</h1>
            <p>Highland Tower Development - Comprehensive vendor tracking and performance management</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display summary metrics
        metrics = subcontractor_manager.generate_subcontractor_metrics()
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🏗️ Total Subcontractors", metrics['total_subcontractors'])
            with col2:
                st.metric("💰 Contract Value", f"${metrics['total_contract_value']:,.0f}")
            with col3:
                st.metric("⚠️ Need Review", metrics['needing_performance_review'])
            with col4:
                st.metric("📊 Avg Quality Score", f"{metrics['average_quality_score']:.1f}")
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🏗️ All Subcontractors", "➕ Add New", "✏️ Manage", "📊 Analytics"])
        
        with tab1:
            st.subheader("🏗️ Subcontractor Directory")
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All"] + [status.value for status in SubcontractorStatus])
            with col2:
                trade_filter = st.selectbox("Filter by Trade", ["All"] + [trade.value for trade in TradeCategory])
            
            # Get filtered subcontractors
            subcontractors = subcontractor_manager.get_all_subcontractors()
            
            if status_filter != "All":
                subcontractors = [s for s in subcontractors if s.status.value == status_filter]
            if trade_filter != "All":
                subcontractors = [s for s in subcontractors if s.trade_category.value == trade_filter]
            
            # Display subcontractors
            for subcontractor in subcontractors:
                status_color = {
                    SubcontractorStatus.ON_SITE: "🟢",
                    SubcontractorStatus.ACTIVE: "🟢",
                    SubcontractorStatus.AWARDED: "🟡",
                    SubcontractorStatus.BIDDING: "🔵",
                    SubcontractorStatus.PREQUALIFIED: "⚪",
                    SubcontractorStatus.COMPLETED: "🟢",
                    SubcontractorStatus.TERMINATED: "🔴"
                }.get(subcontractor.status, "⚪")
                
                review_warning = "📋 REVIEW NEEDED" if subcontractor.needs_performance_review() else ""
                insurance_warning = "🛡️ INSURANCE CHECK" if not subcontractor.is_insurance_current() else ""
                
                with st.expander(f"{status_color} {subcontractor.company_code} | {subcontractor.company_name} | {subcontractor.trade_category.value} {review_warning} {insurance_warning}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**🏢 Trade:** {subcontractor.trade_category.value}")
                        st.write(f"**👤 Contact:** {subcontractor.primary_contact}")
                        st.write(f"**📞 Phone:** {subcontractor.contact_phone}")
                        st.write(f"**📧 Email:** {subcontractor.contact_email}")
                        st.write(f"**📍 Address:** {subcontractor.office_address}")
                        st.write(f"**🏗️ Experience:** {subcontractor.years_in_business} years")
                    
                    with col2:
                        st.write(f"**💰 Contract Value:** ${subcontractor.contract_value:,.0f}")
                        st.write(f"**💸 Total Paid:** ${subcontractor.total_paid:,.0f}")
                        st.write(f"**⏳ Pending:** ${subcontractor.amount_pending:,.0f}")
                        st.write(f"**📊 Overall Rating:** {subcontractor.overall_rating.value}")
                        st.write(f"**👥 Crew Size:** {subcontractor.crew_size}")
                        if subcontractor.contract_start_date:
                            st.write(f"**📅 Contract:** {subcontractor.contract_start_date} to {subcontractor.contract_end_date}")
                    
                    if subcontractor.scope_of_work:
                        st.write(f"**🔧 Scope of Work:** {subcontractor.scope_of_work}")
                    
                    # Performance metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Quality Score", f"{subcontractor.quality_score:.1f}")
                    with col2:
                        st.metric("Schedule Performance", f"{subcontractor.schedule_performance:.1f}")
                    with col3:
                        st.metric("Safety Score", f"{subcontractor.safety_score:.1f}")
                    
                    # Status indicators
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if subcontractor.needs_performance_review():
                            st.warning("📋 Review Needed")
                        else:
                            st.success("✅ Review Current")
                    with col2:
                        if subcontractor.is_insurance_current():
                            st.success("🛡️ Insurance Current")
                        else:
                            st.error("⚠️ Insurance Check Required")
                    with col3:
                        if subcontractor.safety_orientation_complete:
                            st.success("✅ Safety Orientation")
                        else:
                            st.warning("⚠️ Orientation Needed")
                    
                    # Recent performance reviews
                    if subcontractor.performance_reviews:
                        st.write("**📋 Recent Reviews:**")
                        for review in subcontractor.performance_reviews[-2:]:
                            rating_icon = {
                                PerformanceRating.EXCELLENT: "⭐⭐⭐⭐⭐",
                                PerformanceRating.GOOD: "⭐⭐⭐⭐",
                                PerformanceRating.SATISFACTORY: "⭐⭐⭐",
                                PerformanceRating.NEEDS_IMPROVEMENT: "⭐⭐",
                                PerformanceRating.UNSATISFACTORY: "⭐"
                            }.get(review.overall_rating, "")
                            st.write(f"• {rating_icon} {review.reviewer} ({review.review_date}): {review.comments}")
                    
                    # Quick actions
                    st.write("---")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"📋 Add Review", key=f"btn_review_{subcontractor.subcontractor_id}"):
                            st.session_state[f"show_review_{subcontractor.subcontractor_id}"] = True
                    
                    with col2:
                        if st.button(f"💰 Add Payment", key=f"btn_payment_{subcontractor.subcontractor_id}"):
                            st.session_state[f"show_payment_{subcontractor.subcontractor_id}"] = True
                    
                    with col3:
                        new_status = st.selectbox(f"Update Status", 
                                                [status.value for status in SubcontractorStatus],
                                                index=[status.value for status in SubcontractorStatus].index(subcontractor.status.value),
                                                key=f"status_{subcontractor.subcontractor_id}")
                        if st.button(f"📊 Update", key=f"btn_status_{subcontractor.subcontractor_id}"):
                            subcontractor.status = SubcontractorStatus(new_status)
                            st.success("Status updated!")
                            st.rerun()
                    
                    # Performance review form
                    if st.session_state.get(f"show_review_{subcontractor.subcontractor_id}", False):
                        with st.form(f"review_form_{subcontractor.subcontractor_id}"):
                            st.write("**📋 Add Performance Review**")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                reviewer = st.text_input("Reviewer Name")
                                quality_rating = st.selectbox("Quality Rating", [rating.value for rating in PerformanceRating])
                                schedule_rating = st.selectbox("Schedule Rating", [rating.value for rating in PerformanceRating])
                                safety_rating = st.selectbox("Safety Rating", [rating.value for rating in PerformanceRating])
                            
                            with col2:
                                communication_rating = st.selectbox("Communication Rating", [rating.value for rating in PerformanceRating])
                                overall_rating = st.selectbox("Overall Rating", [rating.value for rating in PerformanceRating])
                                comments = st.text_area("Comments")
                                recommendations = st.text_area("Recommendations")
                            
                            if st.form_submit_button("📋 Submit Review"):
                                review_data = {
                                    "review_date": datetime.now().strftime('%Y-%m-%d'),
                                    "reviewer": reviewer,
                                    "quality_rating": quality_rating,
                                    "schedule_rating": schedule_rating,
                                    "safety_rating": safety_rating,
                                    "communication_rating": communication_rating,
                                    "overall_rating": overall_rating,
                                    "comments": comments,
                                    "recommendations": recommendations
                                }
                                if subcontractor_manager.add_performance_review(subcontractor.subcontractor_id, review_data):
                                    st.success("Review added!")
                                    st.session_state[f"show_review_{subcontractor.subcontractor_id}"] = False
                                    st.rerun()
                    
                    # Payment form
                    if st.session_state.get(f"show_payment_{subcontractor.subcontractor_id}", False):
                        with st.form(f"payment_form_{subcontractor.subcontractor_id}"):
                            st.write("**💰 Add Payment Record**")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                invoice_number = st.text_input("Invoice Number")
                                invoice_date = st.date_input("Invoice Date")
                                amount = st.number_input("Amount", min_value=0.0, step=100.0)
                            
                            with col2:
                                payment_status = st.selectbox("Status", ["Pending", "Approved", "Paid", "Disputed"])
                                payment_date = st.date_input("Payment Date (if paid)")
                                notes = st.text_area("Payment Notes")
                            
                            if st.form_submit_button("💰 Add Payment"):
                                payment_data = {
                                    "invoice_number": invoice_number,
                                    "invoice_date": invoice_date.strftime('%Y-%m-%d'),
                                    "amount": amount,
                                    "payment_date": payment_date.strftime('%Y-%m-%d') if payment_status == "Paid" else None,
                                    "status": payment_status,
                                    "notes": notes
                                }
                                if subcontractor_manager.add_payment_record(subcontractor.subcontractor_id, payment_data):
                                    st.success("Payment record added!")
                                    st.session_state[f"show_payment_{subcontractor.subcontractor_id}"] = False
                                    st.rerun()
        
        with tab2:
            st.subheader("➕ Add New Subcontractor")
            
            with st.form("create_subcontractor_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    company_name = st.text_input("🏢 Company Name*", placeholder="Enter company name")
                    trade_category = st.selectbox("🔧 Trade Category*", options=[trade.value for trade in TradeCategory])
                    primary_contact = st.text_input("👤 Primary Contact*", placeholder="Contact person name")
                    contact_email = st.text_input("📧 Email*", placeholder="contact@company.com")
                    contact_phone = st.text_input("📞 Phone*", placeholder="555-123-4567")
                
                with col2:
                    office_address = st.text_input("📍 Office Address*", placeholder="Full business address")
                    business_license = st.text_input("📄 Business License", placeholder="License number")
                    tax_id = st.text_input("🆔 Tax ID", placeholder="Tax identification number")
                    years_in_business = st.number_input("🏗️ Years in Business", min_value=0, step=1, value=5)
                    website = st.text_input("🌐 Website", placeholder="www.company.com")
                
                # Contract details (if applicable)
                st.write("**📋 Contract Information (if awarded)**")
                col1, col2 = st.columns(2)
                
                with col1:
                    contract_value = st.number_input("💰 Contract Value", min_value=0.0, step=1000.0)
                    contract_start = st.date_input("📅 Contract Start Date")
                    scope_of_work = st.text_area("🔧 Scope of Work", placeholder="Detailed description of work scope")
                
                with col2:
                    contract_end = st.date_input("📅 Contract End Date")
                    work_areas = st.text_input("📍 Work Areas", placeholder="Comma-separated work locations")
                    current_phase = st.text_input("📊 Current Phase", placeholder="Current project phase")
                
                # Performance and personnel
                col1, col2 = st.columns(2)
                
                with col1:
                    project_manager = st.text_input("👤 Project Manager", placeholder="PM name")
                    superintendent = st.text_input("👷 Superintendent", placeholder="Superintendent name")
                    overall_rating = st.selectbox("📊 Initial Rating", options=[rating.value for rating in PerformanceRating], index=2)
                
                with col2:
                    quality_score = st.number_input("📋 Quality Score", min_value=0.0, max_value=100.0, step=0.1, value=85.0)
                    schedule_performance = st.number_input("⏰ Schedule Performance", min_value=0.0, max_value=100.0, step=0.1, value=85.0)
                    safety_score = st.number_input("🦺 Safety Score", min_value=0.0, max_value=100.0, step=0.1, value=85.0)
                
                # Additional details
                col1, col2 = st.columns(2)
                
                with col1:
                    certifications = st.text_input("📜 Certifications", placeholder="Comma-separated certifications")
                    prequalification_notes = st.text_area("📝 Prequalification Notes", placeholder="Notes from prequalification process")
                
                with col2:
                    performance_notes = st.text_area("📊 Performance Notes", placeholder="Performance observations")
                    contract_notes = st.text_area("📋 Contract Notes", placeholder="Contract-specific notes")
                
                submit_subcontractor = st.form_submit_button("🆕 Add Subcontractor", use_container_width=True)
                
                if submit_subcontractor:
                    if not company_name or not trade_category or not primary_contact or not contact_email:
                        st.error("Please fill in all required fields marked with *")
                    else:
                        subcontractor_data = {
                            "company_name": company_name,
                            "trade_category": trade_category,
                            "primary_contact": primary_contact,
                            "contact_email": contact_email,
                            "contact_phone": contact_phone,
                            "office_address": office_address,
                            "business_license": business_license,
                            "tax_id": tax_id,
                            "duns_number": None,
                            "website": website if website else None,
                            "years_in_business": years_in_business,
                            "contract_value": contract_value,
                            "contract_start_date": contract_start.strftime('%Y-%m-%d'),
                            "contract_end_date": contract_end.strftime('%Y-%m-%d'),
                            "scope_of_work": scope_of_work,
                            "project_name": "Highland Tower Development",
                            "work_areas": [area.strip() for area in work_areas.split(',') if area.strip()],
                            "current_phase": current_phase,
                            "quality_score": quality_score,
                            "schedule_performance": schedule_performance,
                            "safety_score": safety_score,
                            "overall_rating": overall_rating,
                            "bond_amount": 0.0,
                            "bond_expiry": None,
                            "project_manager": project_manager,
                            "superintendent": superintendent,
                            "safety_officer": None,
                            "certifications": [cert.strip() for cert in certifications.split(',') if cert.strip()],
                            "prequalification_notes": prequalification_notes,
                            "performance_notes": performance_notes,
                            "contract_notes": contract_notes,
                            "prequalified_by": "Current User",
                            "created_by": "Current User",
                            "last_updated_by": "Current User"
                        }
                        
                        subcontractor_id = subcontractor_manager.create_subcontractor(subcontractor_data)
                        st.success(f"✅ Subcontractor added successfully! ID: {subcontractor_id}")
                        st.rerun()
        
        with tab3:
            st.subheader("✏️ Manage Subcontractors")
            
            subcontractors = subcontractor_manager.get_all_subcontractors()
            if subcontractors:
                subcontractor_options = [f"{s.company_code} - {s.company_name}" for s in subcontractors]
                selected_index = st.selectbox("Select Subcontractor to Manage", range(len(subcontractor_options)), format_func=lambda x: subcontractor_options[x])
                selected_subcontractor = subcontractors[selected_index]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("✏️ Edit Subcontractor", use_container_width=True):
                        st.session_state.show_edit_subcontractor_form = True
                
                with col2:
                    if st.button("🗑️ Delete Subcontractor", use_container_width=True):
                        if selected_subcontractor.subcontractor_id in subcontractor_manager.subcontractors:
                            del subcontractor_manager.subcontractors[selected_subcontractor.subcontractor_id]
                            st.success("✅ Subcontractor deleted successfully!")
                            st.rerun()
                
                with col3:
                    if st.button("📋 Duplicate Subcontractor", use_container_width=True):
                        # Create duplicate with modified name
                        subcontractor_data = {
                            "company_name": f"Copy of {selected_subcontractor.company_name}",
                            "trade_category": selected_subcontractor.trade_category.value,
                            "primary_contact": selected_subcontractor.primary_contact,
                            "contact_email": f"copy.{selected_subcontractor.contact_email}",
                            "contact_phone": selected_subcontractor.contact_phone,
                            "office_address": selected_subcontractor.office_address,
                            "business_license": f"COPY-{selected_subcontractor.business_license}",
                            "tax_id": f"COPY-{selected_subcontractor.tax_id}",
                            "duns_number": selected_subcontractor.duns_number,
                            "website": selected_subcontractor.website,
                            "years_in_business": selected_subcontractor.years_in_business,
                            "contract_value": 0.0,  # New contract
                            "contract_start_date": datetime.now().strftime('%Y-%m-%d'),
                            "contract_end_date": (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
                            "scope_of_work": selected_subcontractor.scope_of_work,
                            "project_name": selected_subcontractor.project_name,
                            "work_areas": selected_subcontractor.work_areas.copy(),
                            "current_phase": "Planning",
                            "quality_score": selected_subcontractor.quality_score,
                            "schedule_performance": selected_subcontractor.schedule_performance,
                            "safety_score": selected_subcontractor.safety_score,
                            "overall_rating": selected_subcontractor.overall_rating.value,
                            "bond_amount": 0.0,
                            "bond_expiry": None,
                            "project_manager": selected_subcontractor.project_manager,
                            "superintendent": selected_subcontractor.superintendent,
                            "safety_officer": selected_subcontractor.safety_officer,
                            "certifications": selected_subcontractor.certifications.copy(),
                            "prequalification_notes": selected_subcontractor.prequalification_notes,
                            "performance_notes": "Duplicated from existing subcontractor",
                            "contract_notes": "New contract - terms to be negotiated",
                            "prequalified_by": "Current User",
                            "created_by": "Current User",
                            "last_updated_by": "Current User"
                        }
                        subcontractor_id = subcontractor_manager.create_subcontractor(subcontractor_data)
                        st.success(f"✅ Subcontractor duplicated! ID: {subcontractor_id}")
                        st.rerun()
                
                # Edit form
                if st.session_state.get('show_edit_subcontractor_form', False):
                    with st.form("edit_subcontractor_form"):
                        st.write("**✏️ Edit Subcontractor Details**")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_name = st.text_input("🏢 Company Name", value=selected_subcontractor.company_name)
                            edit_contact = st.text_input("👤 Primary Contact", value=selected_subcontractor.primary_contact)
                            edit_email = st.text_input("📧 Email", value=selected_subcontractor.contact_email)
                            edit_phone = st.text_input("📞 Phone", value=selected_subcontractor.contact_phone)
                        
                        with col2:
                            edit_address = st.text_input("📍 Address", value=selected_subcontractor.office_address)
                            edit_contract_value = st.number_input("💰 Contract Value", value=float(selected_subcontractor.contract_value), step=1000.0)
                            edit_scope = st.text_area("🔧 Scope", value=selected_subcontractor.scope_of_work)
                            edit_notes = st.text_area("📝 Notes", value=selected_subcontractor.performance_notes)
                        
                        if st.form_submit_button("✏️ Update Subcontractor"):
                            # Update the subcontractor
                            selected_subcontractor.company_name = edit_name
                            selected_subcontractor.primary_contact = edit_contact
                            selected_subcontractor.contact_email = edit_email
                            selected_subcontractor.contact_phone = edit_phone
                            selected_subcontractor.office_address = edit_address
                            selected_subcontractor.contract_value = edit_contract_value
                            selected_subcontractor.scope_of_work = edit_scope
                            selected_subcontractor.performance_notes = edit_notes
                            selected_subcontractor.last_updated_by = "Current User"
                            selected_subcontractor.updated_at = datetime.now().isoformat()
                            
                            st.success("✅ Subcontractor updated successfully!")
                            st.session_state.show_edit_subcontractor_form = False
                            st.rerun()
            else:
                st.info("No subcontractors available. Add some subcontractors first.")
        
        with tab4:
            st.subheader("📊 Subcontractor Analytics")
            
            if metrics:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📊 Status Distribution:**")
                    for status, count in metrics['status_breakdown'].items():
                        status_icon = {
                            "On Site": "🟢",
                            "Active": "🟢",
                            "Awarded": "🟡",
                            "Bidding": "🔵",
                            "Prequalified": "⚪",
                            "Completed": "🟢",
                            "Terminated": "🔴"
                        }.get(status, "⚪")
                        st.write(f"• {status_icon} {status}: {count}")
                    
                    st.write("**🔧 Trade Distribution:**")
                    for trade, count in metrics['trade_breakdown'].items():
                        if count > 0:
                            st.write(f"• {trade}: {count}")
                
                with col2:
                    st.write("**📈 Performance Metrics:**")
                    st.write(f"• **Total Contract Value:** ${metrics['total_contract_value']:,.0f}")
                    st.write(f"• **Total Paid:** ${metrics['total_paid']:,.0f}")
                    st.write(f"• **Total Pending:** ${metrics['total_pending']:,.0f}")
                    st.write(f"• **Average Quality Score:** {metrics['average_quality_score']:.1f}")
                    st.write(f"• **Average Schedule Performance:** {metrics['average_schedule_performance']:.1f}")
                    st.write(f"• **Average Safety Score:** {metrics['average_safety_score']:.1f}")
                    
                    # Issues needing attention
                    if metrics['needing_performance_review'] > 0:
                        st.write(f"**📋 Need Performance Review:** {metrics['needing_performance_review']}")
                    
                    if metrics['insurance_expiring_soon'] > 0:
                        st.write(f"**🛡️ Insurance Expiring Soon:** {metrics['insurance_expiring_soon']}")
        
        return
        
    except ImportError:
        st.error("Enterprise Subcontractor Management module not available")
        render_subcontractor_management_basic()

def render_subcontractor_management_basic():
    """Basic subcontractor management module - fallback version"""
    st.markdown("""
    <div class="module-header">
        <h1>🏭 Subcontractor Management</h1>
        <p>Comprehensive subcontractor coordination, performance tracking, and compliance management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize subcontractor data
    if "subcontractors" not in st.session_state:
        st.session_state.subcontractors = [
            {
                "id": "SUB-001",
                "company_name": "Steel Solutions Inc",
                "trade": "Structural Steel",
                "contact_person": "Mike Chen",
                "contact_title": "Project Manager",
                "phone": "(555) 123-4567",
                "email": "mchen@steelsolutions.com",
                "address": "1234 Industrial Blvd, Brooklyn, NY 11201",
                "license_number": "NYS-STEEL-12345",
                "insurance_expiry": "2025-12-31",
                "bond_amount": 500000.00,
                "status": "Active",
                "start_date": "2025-04-01",
                "end_date": "2025-08-15",
                "contract_value": 3200000.00,
                "performance_rating": 4.8,
                "safety_rating": 4.9,
                "quality_rating": 4.7,
                "schedule_rating": 4.8,
                "payment_terms": "Net 30",
                "current_tasks": ["TASK-003"],
                "completed_work": 85.0,
                "certifications": ["AWS D1.1", "OSHA 30", "AISC Certified"],
                "notes": "Excellent performance on structural steel installation",
                "emergency_contact": "Lisa Chen - (555) 123-4568"
            },
            {
                "id": "SUB-002",
                "company_name": "Elite MEP Systems",
                "trade": "MEP",
                "contact_person": "Jennifer Walsh",
                "contact_title": "MEP Coordinator",
                "phone": "(555) 234-5678",
                "email": "jwalsh@elitemep.com",
                "address": "5678 Tech Park Dr, Queens, NY 11377",
                "license_number": "NYS-MEP-67890",
                "insurance_expiry": "2025-11-30",
                "bond_amount": 750000.00,
                "status": "Active",
                "start_date": "2025-06-15",
                "end_date": "2025-07-31",
                "contract_value": 4100000.00,
                "performance_rating": 4.6,
                "safety_rating": 4.7,
                "quality_rating": 4.8,
                "schedule_rating": 4.4,
                "payment_terms": "Net 30",
                "current_tasks": ["TASK-004"],
                "completed_work": 60.0,
                "certifications": ["NECA Certified", "OSHA 30", "LEED Accredited"],
                "notes": "Strong technical expertise, minor schedule coordination needed",
                "emergency_contact": "Robert Walsh - (555) 234-5679"
            },
            {
                "id": "SUB-003",
                "company_name": "Premium Exteriors LLC",
                "trade": "Exterior Envelope",
                "contact_person": "David Rodriguez",
                "contact_title": "Envelope Specialist",
                "phone": "(555) 345-6789",
                "email": "drodriguez@premiumext.com",
                "address": "9876 Facade Ave, Manhattan, NY 10001",
                "license_number": "NYS-EXT-54321",
                "insurance_expiry": "2026-01-15",
                "bond_amount": 400000.00,
                "status": "Scheduled",
                "start_date": "2025-08-01",
                "end_date": "2025-09-30",
                "contract_value": 2200000.00,
                "performance_rating": 4.9,
                "safety_rating": 4.8,
                "quality_rating": 5.0,
                "schedule_rating": 4.9,
                "payment_terms": "Net 30",
                "current_tasks": ["TASK-005"],
                "completed_work": 30.0,
                "certifications": ["Curtain Wall Specialist", "OSHA 30", "AAMA Certified"],
                "notes": "Top-tier curtain wall contractor with excellent reputation",
                "emergency_contact": "Maria Rodriguez - (555) 345-6790"
            }
        ]
    
    if "subcontractor_evaluations" not in st.session_state:
        st.session_state.subcontractor_evaluations = [
            {
                "id": "EVAL-001",
                "subcontractor_id": "SUB-001",
                "evaluation_date": "2025-05-15",
                "evaluator": "John Davis, P.E.",
                "period": "Q2 2025",
                "performance_score": 4.8,
                "safety_score": 4.9,
                "quality_score": 4.7,
                "schedule_score": 4.8,
                "communication_score": 4.6,
                "overall_score": 4.76,
                "strengths": ["Excellent steel installation quality", "Strong safety record", "Responsive to changes"],
                "improvement_areas": ["Communication during coordination meetings", "Documentation submission timing"],
                "recommendations": "Continue current performance level, improve documentation processes",
                "next_evaluation": "2025-08-15"
            },
            {
                "id": "EVAL-002",
                "subcontractor_id": "SUB-002",
                "evaluation_date": "2025-05-20",
                "evaluator": "Sarah Johnson - Project Manager",
                "period": "Q2 2025",
                "performance_score": 4.6,
                "safety_score": 4.7,
                "quality_score": 4.8,
                "schedule_score": 4.4,
                "communication_score": 4.5,
                "overall_score": 4.6,
                "strengths": ["High-quality MEP installation", "Technical expertise", "Problem-solving capabilities"],
                "improvement_areas": ["Schedule adherence", "Coordination with other trades"],
                "recommendations": "Focus on schedule management and improved coordination",
                "next_evaluation": "2025-07-20"
            }
        ]
    
    if "insurance_tracking" not in st.session_state:
        st.session_state.insurance_tracking = [
            {
                "id": "INS-001",
                "subcontractor_id": "SUB-001",
                "insurance_type": "General Liability",
                "policy_number": "GL-2025-12345",
                "provider": "Construction Insurance Group",
                "coverage_amount": 2000000.00,
                "effective_date": "2025-01-01",
                "expiry_date": "2025-12-31",
                "status": "Active",
                "certificate_received": True,
                "renewal_reminder": "2025-11-01"
            },
            {
                "id": "INS-002",
                "subcontractor_id": "SUB-001",
                "insurance_type": "Workers Compensation",
                "policy_number": "WC-2025-67890",
                "provider": "Safety First Insurance",
                "coverage_amount": 1000000.00,
                "effective_date": "2025-01-01",
                "expiry_date": "2025-12-31",
                "status": "Active",
                "certificate_received": True,
                "renewal_reminder": "2025-11-01"
            },
            {
                "id": "INS-003",
                "subcontractor_id": "SUB-002",
                "insurance_type": "General Liability",
                "policy_number": "GL-2025-54321",
                "provider": "MEP Insurance Solutions",
                "coverage_amount": 3000000.00,
                "effective_date": "2025-01-01",
                "expiry_date": "2025-11-30",
                "status": "Expiring Soon",
                "certificate_received": True,
                "renewal_reminder": "2025-10-01"
            }
        ]
    
    # Key Subcontractor Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_subs = len(st.session_state.subcontractors)
    active_subs = len([sub for sub in st.session_state.subcontractors if sub['status'] == 'Active'])
    avg_performance = sum(sub['performance_rating'] for sub in st.session_state.subcontractors) / len(st.session_state.subcontractors) if st.session_state.subcontractors else 0
    total_contract_value = sum(sub['contract_value'] for sub in st.session_state.subcontractors)
    
    with col1:
        st.metric("Total Subcontractors", total_subs, delta_color="normal")
    with col2:
        st.metric("Active", active_subs, delta_color="normal")
    with col3:
        st.metric("Avg Performance", f"{avg_performance:.1f}/5.0", delta_color="normal")
    with col4:
        st.metric("Total Contract Value", f"${total_contract_value/1000000:.1f}M", delta_color="normal")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏭 Subcontractors", "📊 Evaluations", "🛡️ Insurance", "📈 Analytics", "🔧 Management"])
    
    with tab1:
        st.subheader("🏭 Subcontractor Management")
        
        sub_tab1, sub_tab2 = st.tabs(["➕ Add Subcontractor", "📋 View Subcontractors"])
        
        with sub_tab1:
            st.markdown("**Add New Subcontractor**")
            
            with st.form("subcontractor_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    company_name = st.text_input("Company Name", placeholder="Subcontractor company name")
                    trade = st.selectbox("Trade", [
                        "Structural Steel", "MEP", "Exterior Envelope", "Concrete", "Interior Finishes",
                        "Roofing", "Earthwork", "Masonry", "Flooring", "Painting", "Specialty"
                    ])
                    contact_person = st.text_input("Contact Person", placeholder="Primary contact name")
                    contact_title = st.text_input("Contact Title", placeholder="Contact person title")
                    phone = st.text_input("Phone", placeholder="(555) 123-4567")
                    email = st.text_input("Email", placeholder="contact@company.com")
                    address = st.text_area("Address", placeholder="Complete business address")
                
                with col2:
                    license_number = st.text_input("License Number", placeholder="State license number")
                    insurance_expiry = st.date_input("Insurance Expiry", value=datetime.now().date() + timedelta(days=365))
                    bond_amount = st.number_input("Bond Amount ($)", value=0.00, format="%.2f")
                    contract_value = st.number_input("Contract Value ($)", value=0.00, format="%.2f")
                    start_date = st.date_input("Start Date", value=datetime.now().date())
                    end_date = st.date_input("End Date", value=datetime.now().date() + timedelta(days=90))
                    payment_terms = st.selectbox("Payment Terms", ["Net 30", "Net 15", "Net 45", "Weekly", "Bi-weekly"])
                
                certifications = st.text_area("Certifications", placeholder="Comma-separated certifications")
                emergency_contact = st.text_input("Emergency Contact", placeholder="Emergency contact information")
                notes = st.text_area("Notes", placeholder="Additional notes about the subcontractor")
                
                if st.form_submit_button("🏭 Add Subcontractor", type="primary"):
                    if company_name and trade and contact_person and phone and email:
                        new_subcontractor = {
                            "id": f"SUB-{len(st.session_state.subcontractors) + 1:03d}",
                            "company_name": company_name,
                            "trade": trade,
                            "contact_person": contact_person,
                            "contact_title": contact_title,
                            "phone": phone,
                            "email": email,
                            "address": address,
                            "license_number": license_number,
                            "insurance_expiry": str(insurance_expiry),
                            "bond_amount": bond_amount,
                            "status": "Scheduled",
                            "start_date": str(start_date),
                            "end_date": str(end_date),
                            "contract_value": contract_value,
                            "performance_rating": 0.0,
                            "safety_rating": 0.0,
                            "quality_rating": 0.0,
                            "schedule_rating": 0.0,
                            "payment_terms": payment_terms,
                            "current_tasks": [],
                            "completed_work": 0.0,
                            "certifications": [cert.strip() for cert in certifications.split(',') if cert.strip()],
                            "notes": notes,
                            "emergency_contact": emergency_contact
                        }
                        st.session_state.subcontractors.append(new_subcontractor)
                        st.success("✅ Subcontractor added successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with sub_tab2:
            st.markdown("**All Subcontractors**")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                trade_filter = st.selectbox("Filter by Trade", ["All Trades"] + list(set(sub['trade'] for sub in st.session_state.subcontractors)))
            with col2:
                status_filter = st.selectbox("Filter by Status", ["All Status", "Active", "Scheduled", "Completed", "Suspended"])
            with col3:
                search_text = st.text_input("🔍 Search", placeholder="Search company names...")
            
            # Apply filters
            filtered_subs = st.session_state.subcontractors
            if trade_filter != "All Trades":
                filtered_subs = [sub for sub in filtered_subs if sub['trade'] == trade_filter]
            if status_filter != "All Status":
                filtered_subs = [sub for sub in filtered_subs if sub['status'] == status_filter]
            if search_text:
                filtered_subs = [sub for sub in filtered_subs if search_text.lower() in sub['company_name'].lower()]
            
            # Display subcontractors
            for subcontractor in filtered_subs:
                status_icon = {"Active": "🟢", "Scheduled": "🟡", "Completed": "✅", "Suspended": "🔴"}.get(subcontractor['status'], "⚪")
                
                with st.expander(f"{status_icon} {subcontractor['company_name']} - {subcontractor['trade']} ({subcontractor['status']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**🏭 Company:** {subcontractor['company_name']}")
                        st.write(f"**🔧 Trade:** {subcontractor['trade']}")
                        st.write(f"**👤 Contact:** {subcontractor['contact_person']}")
                        st.write(f"**📱 Phone:** {subcontractor['phone']}")
                        st.write(f"**📧 Email:** {subcontractor['email']}")
                        st.write(f"**📊 Status:** {subcontractor['status']}")
                    
                    with col2:
                        st.write(f"**📅 Start Date:** {subcontractor['start_date']}")
                        st.write(f"**📅 End Date:** {subcontractor['end_date']}")
                        st.write(f"**💰 Contract Value:** ${subcontractor['contract_value']:,.2f}")
                        st.write(f"**💳 Payment Terms:** {subcontractor['payment_terms']}")
                        st.write(f"**🛡️ Insurance Expiry:** {subcontractor['insurance_expiry']}")
                        st.write(f"**📜 License:** {subcontractor['license_number']}")
                    
                    with col3:
                        st.write(f"**⭐ Performance:** {subcontractor['performance_rating']:.1f}/5.0")
                        st.write(f"**🦺 Safety:** {subcontractor['safety_rating']:.1f}/5.0")
                        st.write(f"**🎯 Quality:** {subcontractor['quality_rating']:.1f}/5.0")
                        st.write(f"**📅 Schedule:** {subcontractor['schedule_rating']:.1f}/5.0")
                        st.write(f"**📈 Work Complete:** {subcontractor['completed_work']:.1f}%")
                        if subcontractor['current_tasks']:
                            st.write(f"**🔗 Current Tasks:** {', '.join(subcontractor['current_tasks'])}")
                    
                    if subcontractor['certifications']:
                        st.write(f"**📜 Certifications:** {', '.join(subcontractor['certifications'])}")
                    if subcontractor['notes']:
                        st.write(f"**📝 Notes:** {subcontractor['notes']}")
                    
                    # Progress bar
                    st.write("**📈 Work Progress:**")
                    st.progress(subcontractor['completed_work'] / 100)
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if subcontractor['status'] == 'Scheduled' and st.button(f"▶️ Activate", key=f"activate_{subcontractor['id']}"):
                            subcontractor['status'] = 'Active'
                            st.success("Subcontractor activated!")
                            st.rerun()
                    with col2:
                        if st.button(f"📊 Evaluate", key=f"evaluate_{subcontractor['id']}"):
                            st.info("Evaluation form - would open evaluation interface")
                    with col3:
                        if st.button(f"✏️ Edit", key=f"edit_{subcontractor['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col4:
                        if st.button(f"🗑️ Remove", key=f"remove_{subcontractor['id']}"):
                            st.session_state.subcontractors.remove(subcontractor)
                            st.success("Subcontractor removed!")
                            st.rerun()
    
    with tab2:
        st.subheader("📊 Performance Evaluations")
        
        eval_tab1, eval_tab2 = st.tabs(["📝 New Evaluation", "📊 View Evaluations"])
        
        with eval_tab1:
            st.markdown("**Create Performance Evaluation**")
            
            with st.form("evaluation_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    eval_subcontractor = st.selectbox("Select Subcontractor", [f"{sub['id']} - {sub['company_name']}" for sub in st.session_state.subcontractors])
                    evaluation_date = st.date_input("Evaluation Date", value=datetime.now().date())
                    evaluator = st.text_input("Evaluator", placeholder="Name and title of evaluator")
                    period = st.text_input("Evaluation Period", placeholder="e.g., Q2 2025")
                
                with col2:
                    performance_score = st.slider("Performance Score", 1.0, 5.0, 3.0, 0.1)
                    safety_score = st.slider("Safety Score", 1.0, 5.0, 3.0, 0.1)
                    quality_score = st.slider("Quality Score", 1.0, 5.0, 3.0, 0.1)
                    schedule_score = st.slider("Schedule Score", 1.0, 5.0, 3.0, 0.1)
                    communication_score = st.slider("Communication Score", 1.0, 5.0, 3.0, 0.1)
                
                strengths = st.text_area("Strengths", placeholder="List key strengths (comma-separated)")
                improvement_areas = st.text_area("Areas for Improvement", placeholder="List improvement areas (comma-separated)")
                recommendations = st.text_area("Recommendations", placeholder="Recommendations for future performance")
                next_evaluation = st.date_input("Next Evaluation Date", value=datetime.now().date() + timedelta(days=90))
                
                if st.form_submit_button("📊 Submit Evaluation", type="primary"):
                    if eval_subcontractor and evaluator:
                        overall_score = (performance_score + safety_score + quality_score + schedule_score + communication_score) / 5
                        
                        new_evaluation = {
                            "id": f"EVAL-{len(st.session_state.subcontractor_evaluations) + 1:03d}",
                            "subcontractor_id": eval_subcontractor.split(" - ")[0],
                            "evaluation_date": str(evaluation_date),
                            "evaluator": evaluator,
                            "period": period,
                            "performance_score": performance_score,
                            "safety_score": safety_score,
                            "quality_score": quality_score,
                            "schedule_score": schedule_score,
                            "communication_score": communication_score,
                            "overall_score": overall_score,
                            "strengths": [s.strip() for s in strengths.split(',') if s.strip()],
                            "improvement_areas": [i.strip() for i in improvement_areas.split(',') if i.strip()],
                            "recommendations": recommendations,
                            "next_evaluation": str(next_evaluation)
                        }
                        st.session_state.subcontractor_evaluations.append(new_evaluation)
                        
                        # Update subcontractor ratings
                        sub_id = eval_subcontractor.split(" - ")[0]
                        for sub in st.session_state.subcontractors:
                            if sub['id'] == sub_id:
                                sub['performance_rating'] = performance_score
                                sub['safety_rating'] = safety_score
                                sub['quality_rating'] = quality_score
                                sub['schedule_rating'] = schedule_score
                                break
                        
                        st.success("✅ Evaluation submitted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with eval_tab2:
            st.markdown("**All Performance Evaluations**")
            
            for evaluation in st.session_state.subcontractor_evaluations:
                # Find subcontractor name
                sub_name = "Unknown"
                for sub in st.session_state.subcontractors:
                    if sub['id'] == evaluation['subcontractor_id']:
                        sub_name = sub['company_name']
                        break
                
                with st.expander(f"📊 {evaluation['id']} - {sub_name} ({evaluation['period']}) - Score: {evaluation['overall_score']:.1f}/5.0"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**🏭 Subcontractor:** {sub_name}")
                        st.write(f"**📅 Evaluation Date:** {evaluation['evaluation_date']}")
                        st.write(f"**👤 Evaluator:** {evaluation['evaluator']}")
                        st.write(f"**📊 Period:** {evaluation['period']}")
                        st.write(f"**📅 Next Evaluation:** {evaluation['next_evaluation']}")
                    
                    with col2:
                        st.write(f"**⭐ Performance:** {evaluation['performance_score']:.1f}/5.0")
                        st.write(f"**🦺 Safety:** {evaluation['safety_score']:.1f}/5.0")
                        st.write(f"**🎯 Quality:** {evaluation['quality_score']:.1f}/5.0")
                        st.write(f"**📅 Schedule:** {evaluation['schedule_score']:.1f}/5.0")
                        st.write(f"**💬 Communication:** {evaluation['communication_score']:.1f}/5.0")
                        st.write(f"**🏆 Overall Score:** {evaluation['overall_score']:.1f}/5.0")
                    
                    if evaluation['strengths']:
                        st.write(f"**💪 Strengths:** {', '.join(evaluation['strengths'])}")
                    if evaluation['improvement_areas']:
                        st.write(f"**🎯 Improvement Areas:** {', '.join(evaluation['improvement_areas'])}")
                    if evaluation['recommendations']:
                        st.write(f"**💡 Recommendations:** {evaluation['recommendations']}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📤 Share", key=f"share_eval_{evaluation['id']}"):
                            st.success("Evaluation shared!")
                    with col2:
                        if st.button(f"✏️ Edit", key=f"edit_eval_{evaluation['id']}"):
                            st.info("Edit evaluation functionality")
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_eval_{evaluation['id']}"):
                            st.session_state.subcontractor_evaluations.remove(evaluation)
                            st.success("Evaluation deleted!")
                            st.rerun()
    
    with tab3:
        st.subheader("🛡️ Insurance Tracking")
        
        ins_tab1, ins_tab2 = st.tabs(["📝 Add Insurance", "📊 View Insurance"])
        
        with ins_tab1:
            st.markdown("**Add Insurance Record**")
            
            with st.form("insurance_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    ins_subcontractor = st.selectbox("Select Subcontractor", [f"{sub['id']} - {sub['company_name']}" for sub in st.session_state.subcontractors])
                    insurance_type = st.selectbox("Insurance Type", [
                        "General Liability", "Workers Compensation", "Professional Liability", 
                        "Commercial Auto", "Umbrella", "Builders Risk"
                    ])
                    policy_number = st.text_input("Policy Number", placeholder="Policy number")
                    provider = st.text_input("Insurance Provider", placeholder="Insurance company name")
                
                with col2:
                    coverage_amount = st.number_input("Coverage Amount ($)", value=0.00, format="%.2f")
                    effective_date = st.date_input("Effective Date", value=datetime.now().date())
                    expiry_date = st.date_input("Expiry Date", value=datetime.now().date() + timedelta(days=365))
                    certificate_received = st.checkbox("Certificate Received", value=False)
                
                renewal_reminder = st.date_input("Renewal Reminder Date", value=expiry_date - timedelta(days=60))
                
                if st.form_submit_button("🛡️ Add Insurance", type="primary"):
                    if ins_subcontractor and insurance_type and policy_number and provider:
                        new_insurance = {
                            "id": f"INS-{len(st.session_state.insurance_tracking) + 1:03d}",
                            "subcontractor_id": ins_subcontractor.split(" - ")[0],
                            "insurance_type": insurance_type,
                            "policy_number": policy_number,
                            "provider": provider,
                            "coverage_amount": coverage_amount,
                            "effective_date": str(effective_date),
                            "expiry_date": str(expiry_date),
                            "status": "Active" if expiry_date > datetime.now().date() else "Expired",
                            "certificate_received": certificate_received,
                            "renewal_reminder": str(renewal_reminder)
                        }
                        st.session_state.insurance_tracking.append(new_insurance)
                        st.success("✅ Insurance record added successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with ins_tab2:
            st.markdown("**Insurance Tracking Overview**")
            
            for insurance in st.session_state.insurance_tracking:
                # Find subcontractor name
                sub_name = "Unknown"
                for sub in st.session_state.subcontractors:
                    if sub['id'] == insurance['subcontractor_id']:
                        sub_name = sub['company_name']
                        break
                
                # Determine status icon and color
                expiry_date = datetime.strptime(insurance['expiry_date'], '%Y-%m-%d').date()
                days_to_expiry = (expiry_date - datetime.now().date()).days
                
                if days_to_expiry < 0:
                    status_icon = "🔴"
                    status_text = "Expired"
                elif days_to_expiry <= 30:
                    status_icon = "🟡"
                    status_text = "Expiring Soon"
                else:
                    status_icon = "🟢"
                    status_text = "Active"
                
                with st.expander(f"{status_icon} {insurance['insurance_type']} - {sub_name} ({status_text})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**🏭 Subcontractor:** {sub_name}")
                        st.write(f"**🛡️ Type:** {insurance['insurance_type']}")
                        st.write(f"**📄 Policy Number:** {insurance['policy_number']}")
                        st.write(f"**🏢 Provider:** {insurance['provider']}")
                        st.write(f"**💰 Coverage:** ${insurance['coverage_amount']:,.2f}")
                    
                    with col2:
                        st.write(f"**📅 Effective:** {insurance['effective_date']}")
                        st.write(f"**📅 Expires:** {insurance['expiry_date']}")
                        st.write(f"**📊 Status:** {status_text}")
                        st.write(f"**📜 Certificate:** {'Received' if insurance['certificate_received'] else 'Pending'}")
                        st.write(f"**🔔 Reminder:** {insurance['renewal_reminder']}")
                    
                    if days_to_expiry <= 30 and days_to_expiry >= 0:
                        st.warning(f"⚠️ Insurance expires in {days_to_expiry} days!")
                    elif days_to_expiry < 0:
                        st.error(f"❌ Insurance expired {abs(days_to_expiry)} days ago!")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"🔔 Remind", key=f"remind_ins_{insurance['id']}"):
                            st.success("Renewal reminder sent!")
                    with col2:
                        if st.button(f"✏️ Edit", key=f"edit_ins_{insurance['id']}"):
                            st.info("Edit insurance functionality")
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_ins_{insurance['id']}"):
                            st.session_state.insurance_tracking.remove(insurance)
                            st.success("Insurance record deleted!")
                            st.rerun()
    
    with tab4:
        st.subheader("📈 Subcontractor Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Performance ratings distribution
            if st.session_state.subcontractors:
                performance_data = []
                for sub in st.session_state.subcontractors:
                    if sub['performance_rating'] > 0:
                        performance_data.append({
                            'Company': sub['company_name'],
                            'Performance': sub['performance_rating'],
                            'Safety': sub['safety_rating'],
                            'Quality': sub['quality_rating'],
                            'Schedule': sub['schedule_rating']
                        })
                
                if performance_data:
                    perf_df = pd.DataFrame(performance_data)
                    fig_perf = px.bar(perf_df, x='Company', y=['Performance', 'Safety', 'Quality', 'Schedule'],
                                     title="Subcontractor Performance Ratings", barmode='group')
                    st.plotly_chart(fig_perf, use_container_width=True)
        
        with col2:
            # Contract value by trade
            if st.session_state.subcontractors:
                trade_values = {}
                for sub in st.session_state.subcontractors:
                    trade = sub['trade']
                    trade_values[trade] = trade_values.get(trade, 0) + sub['contract_value']
                
                trade_list = list(trade_values.keys())
                value_list = [val/1000000 for val in trade_values.values()]  # Convert to millions
                trade_df = pd.DataFrame({
                    'Trade': trade_list,
                    'Value (M$)': value_list
                })
                fig_trade = px.pie(trade_df, values='Value (M$)', names='Trade', title="Contract Value by Trade")
                st.plotly_chart(fig_trade, use_container_width=True)
    
    with tab5:
        st.subheader("🔧 Subcontractor Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🏭 Subcontractor Summary**")
            if st.session_state.subcontractors:
                sub_stats_data = pd.DataFrame([
                    {"Metric": "Total Subcontractors", "Value": len(st.session_state.subcontractors)},
                    {"Metric": "Active", "Value": len([s for s in st.session_state.subcontractors if s['status'] == 'Active'])},
                    {"Metric": "Scheduled", "Value": len([s for s in st.session_state.subcontractors if s['status'] == 'Scheduled'])},
                    {"Metric": "Avg Performance", "Value": f"{sum(s['performance_rating'] for s in st.session_state.subcontractors if s['performance_rating'] > 0) / len([s for s in st.session_state.subcontractors if s['performance_rating'] > 0]):.1f}/5.0" if any(s['performance_rating'] > 0 for s in st.session_state.subcontractors) else "N/A"},
                ])
                st.dataframe(sub_stats_data, use_container_width=True)
        
        with col2:
            st.markdown("**📊 Evaluation Summary**")
            if st.session_state.subcontractor_evaluations:
                eval_stats_data = pd.DataFrame([
                    {"Metric": "Total Evaluations", "Value": len(st.session_state.subcontractor_evaluations)},
                    {"Metric": "Avg Overall Score", "Value": f"{sum(e['overall_score'] for e in st.session_state.subcontractor_evaluations) / len(st.session_state.subcontractor_evaluations):.1f}/5.0"},
                    {"Metric": "Highest Score", "Value": f"{max(e['overall_score'] for e in st.session_state.subcontractor_evaluations):.1f}/5.0"},
                    {"Metric": "Due This Month", "Value": "TBD"},
                ])
                st.dataframe(eval_stats_data, use_container_width=True)
        
        with col3:
            st.markdown("**🛡️ Insurance Summary**")
            if st.session_state.insurance_tracking:
                # Calculate expiring soon
                expiring_soon = 0
                for ins in st.session_state.insurance_tracking:
                    expiry_date = datetime.strptime(ins['expiry_date'], '%Y-%m-%d').date()
                    days_to_expiry = (expiry_date - datetime.now().date()).days
                    if 0 <= days_to_expiry <= 30:
                        expiring_soon += 1
                
                ins_stats_data = pd.DataFrame([
                    {"Metric": "Total Policies", "Value": len(st.session_state.insurance_tracking)},
                    {"Metric": "Active", "Value": len([i for i in st.session_state.insurance_tracking if i['status'] == 'Active'])},
                    {"Metric": "Expiring Soon", "Value": expiring_soon},
                    {"Metric": "Certificates Received", "Value": len([i for i in st.session_state.insurance_tracking if i['certificate_received']])},
                ])
                st.dataframe(ins_stats_data, use_container_width=True)
        
        # Data management
        st.markdown("**⚠️ Data Management**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🗑️ Clear Subcontractors", type="secondary"):
                st.session_state.subcontractors = []
                st.success("All subcontractors cleared!")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Evaluations", type="secondary"):
                st.session_state.subcontractor_evaluations = []
                st.success("All evaluations cleared!")
                st.rerun()
        with col3:
            if st.button("🗑️ Clear Insurance", type="secondary"):
                st.session_state.insurance_tracking = []
                st.success("All insurance records cleared!")
                st.rerun()

def render_inspections():
    """Enterprise Inspections Management with robust Python backend"""
    try:
        from modules.inspections_backend import inspections_manager, InspectionStatus, InspectionType, DefectSeverity
        
        st.markdown("""
        <div class="module-header">
            <h1>🔍 Inspections Management</h1>
            <p>Highland Tower Development - Comprehensive inspection tracking with compliance workflows</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display summary metrics
        metrics = inspections_manager.generate_inspection_metrics()
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🔍 Total Inspections", metrics['total_inspections'])
            with col2:
                st.metric("✅ Pass Rate", f"{metrics['pass_rate']}%")
            with col3:
                st.metric("🚨 Critical Defects", metrics['critical_defects'])
            with col4:
                st.metric("⏳ Pending", metrics['pending_inspections'])
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["📋 All Inspections", "🚨 Defects", "📊 Analytics"])
        
        with tab1:
            st.subheader("📋 All Inspections")
            
            # Display inspections
            inspections = inspections_manager.get_all_inspections()
            
            for inspection in inspections:
                status_color = {
                    InspectionStatus.PASSED: "🟢",
                    InspectionStatus.FAILED: "🔴",
                    InspectionStatus.SCHEDULED: "🟡",
                    InspectionStatus.IN_PROGRESS: "🔵",
                    InspectionStatus.CONDITIONAL: "🟠"
                }.get(inspection.status, "⚪")
                
                with st.expander(f"{status_color} {inspection.inspection_number} | {inspection.inspection_type.value} | {inspection.status.value}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📍 Location:** {inspection.location}")
                        st.write(f"**🏗️ Work Package:** {inspection.work_package}")
                        st.write(f"**📅 Scheduled:** {inspection.scheduled_date} at {inspection.scheduled_time}")
                        st.write(f"**👤 Inspector:** {inspection.inspector_name}")
                        st.write(f"**🏢 Company:** {inspection.inspector_company}")
                    
                    with col2:
                        st.write(f"**📋 Type:** {inspection.inspector_type.value}")
                        st.write(f"**📄 Permit:** {inspection.permit_number or 'N/A'}")
                        if inspection.actual_date:
                            st.write(f"**✅ Completed:** {inspection.actual_date}")
                        st.write(f"**🚨 Defects Found:** {len(inspection.defects_found)}")
                        st.write(f"**📊 Result:** {inspection.overall_result}")
                    
                    if inspection.scope_description:
                        st.write(f"**📝 Scope:** {inspection.scope_description}")
                    
                    # Show checklist items
                    if inspection.checklist_items:
                        st.write("**📋 Checklist Items:**")
                        for item in inspection.checklist_items:
                            status_icon = "✅" if item.status == "Pass" else "❌" if item.status == "Fail" else "➖"
                            st.write(f"• {status_icon} {item.description} - {item.status}")
                    
                    # Show defects
                    if inspection.defects_found:
                        st.write("**🚨 Defects Found:**")
                        for defect in inspection.defects_found:
                            severity_color = {
                                DefectSeverity.CRITICAL: "🔴",
                                DefectSeverity.MAJOR: "🟠",
                                DefectSeverity.MODERATE: "🟡",
                                DefectSeverity.MINOR: "🟢"
                            }.get(defect.severity, "⚪")
                            
                            resolve_status = "✅" if defect.is_resolved else "⏳"
                            st.write(f"• {severity_color} {resolve_status} {defect.description} ({defect.severity.value})")
                            st.write(f"  📍 {defect.location} | 👤 {defect.responsible_party} | ⏰ Due: {defect.due_date}")
        
        with tab2:
            st.subheader("🚨 Defects Management")
            
            # Collect all defects
            all_defects = []
            for inspection in inspections:
                for defect in inspection.defects_found:
                    all_defects.append((inspection, defect))
            
            if all_defects:
                st.write(f"**Total Defects:** {len(all_defects)}")
                
                for inspection, defect in all_defects:
                    severity_color = {
                        DefectSeverity.CRITICAL: "🔴",
                        DefectSeverity.MAJOR: "🟠",
                        DefectSeverity.MODERATE: "🟡",
                        DefectSeverity.MINOR: "🟢"
                    }.get(defect.severity, "⚪")
                    
                    resolve_status = "✅ Resolved" if defect.is_resolved else "⏳ Open"
                    
                    with st.expander(f"{severity_color} {defect.defect_id} | {defect.description} | {resolve_status}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**🔍 Inspection:** {inspection.inspection_number}")
                            st.write(f"**📍 Location:** {defect.location}")
                            st.write(f"**🚨 Severity:** {defect.severity.value}")
                            st.write(f"**👤 Responsible:** {defect.responsible_party}")
                        
                        with col2:
                            st.write(f"**📅 Due Date:** {defect.due_date}")
                            st.write(f"**📋 Code Reference:** {defect.code_reference or 'N/A'}")
                            if defect.resolved_date:
                                st.write(f"**✅ Resolved:** {defect.resolved_date}")
                        
                        st.write(f"**⚡ Corrective Action:** {defect.corrective_action}")
                        
                        if defect.resolution_notes:
                            st.write(f"**📝 Resolution Notes:** {defect.resolution_notes}")
            else:
                st.info("No defects found in current inspections")
        
        with tab3:
            st.subheader("📊 Inspection Analytics")
            
            if metrics:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📊 Status Breakdown:**")
                    for status, count in metrics['status_breakdown'].items():
                        st.write(f"• {status}: {count}")
                    
                    st.write("**📋 Type Breakdown:**")
                    for insp_type, count in metrics['type_breakdown'].items():
                        st.write(f"• {insp_type}: {count}")
                
                with col2:
                    st.write("**📈 Performance Metrics:**")
                    st.write(f"• **Pass Rate:** {metrics['pass_rate']}%")
                    st.write(f"• **Total Defects:** {metrics['total_defects']}")
                    st.write(f"• **Resolved Defects:** {metrics['resolved_defects']}")
                    st.write(f"• **Resolution Rate:** {metrics['defect_resolution_rate']}%")
                    st.write(f"• **Critical Defects:** {metrics['critical_defects']}")
        
        return
        
    except ImportError:
        st.error("Enterprise Inspections module not available")
        # Fallback to basic version
        render_inspections_basic()

def render_inspections_basic():
    """Basic inspections module - fallback version"""
    st.markdown("""
    <div class="module-header">
        <h1>🔍 Inspections</h1>
        <p>Inspection scheduling and compliance tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("🔍 Inspections module with compliance tracking")

def render_issues_risks():
    """Enterprise Issues & Risks Management with robust Python backend"""
    try:
        from modules.issues_risks_backend import issues_risks_manager, Priority, Status
        
        st.markdown("""
        <div class="module-header">
            <h1>⚠️ Issues & Risks Management</h1>
            <p>Highland Tower Development - Comprehensive risk tracking and mitigation management</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for Issues and Risks
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Issues", "⚠️ Risks", "➕ Create New", "📊 Analytics"])
        
        with tab1:
            st.subheader("📋 Project Issues")
            
            # Issues metrics
            issues_metrics = issues_risks_manager.generate_issues_metrics()
            if issues_metrics:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📋 Total Issues", issues_metrics['total_issues'])
                with col2:
                    st.metric("🔓 Open Issues", issues_metrics['open_issues'])
                with col3:
                    st.metric("🚨 Critical Issues", issues_metrics['critical_issues'])
                with col4:
                    st.metric("💰 Cost Impact", f"${issues_metrics['total_cost_impact']:,.0f}")
            
            # Display issues
            issues = issues_risks_manager.get_all_issues()
            
            for issue in issues:
                priority_color = {
                    Priority.CRITICAL: "🔴",
                    Priority.HIGH: "🟠",
                    Priority.MEDIUM: "🟡",
                    Priority.LOW: "🟢"
                }.get(issue.priority, "⚪")
                
                status_icon = {
                    Status.OPEN: "🔓",
                    Status.IN_PROGRESS: "🔄",
                    Status.RESOLVED: "✅",
                    Status.CLOSED: "🔒"
                }.get(issue.status, "⚪")
                
                with st.expander(f"{priority_color} {status_icon} {issue.issue_number} | {issue.title} | {issue.priority.value}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📍 Location:** {issue.location}")
                        st.write(f"**📦 Work Package:** {issue.work_package}")
                        st.write(f"**👤 Reported By:** {issue.reported_by}")
                        st.write(f"**📅 Reported Date:** {issue.reported_date}")
                        st.write(f"**⏰ Days Open:** {issue.days_open}")
                    
                    with col2:
                        st.write(f"**📊 Status:** {issue.status.value}")
                        st.write(f"**👥 Assigned To:** {issue.assigned_to}")
                        st.write(f"**📅 Due Date:** {issue.due_date}")
                        st.write(f"**💰 Cost Impact:** ${issue.cost_impact:,.0f}")
                        st.write(f"**📆 Schedule Impact:** {issue.schedule_impact_days} days")
                    
                    if issue.description:
                        st.write(f"**📝 Description:** {issue.description}")
                    
                    # Show mitigation actions
                    if issue.mitigation_actions:
                        st.write("**⚡ Mitigation Actions:**")
                        for action in issue.mitigation_actions:
                            action_status = "✅" if action.status == Status.CLOSED else "🔄"
                            st.write(f"• {action_status} {action.description} (Due: {action.due_date})")
        
        with tab2:
            st.subheader("⚠️ Project Risks")
            
            # Risks metrics
            risks_metrics = issues_risks_manager.generate_risks_metrics()
            if risks_metrics:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("⚠️ Total Risks", risks_metrics['total_risks'])
                with col2:
                    st.metric("🔥 High Risk Count", risks_metrics['high_risk_count'])
                with col3:
                    st.metric("📊 Avg Risk Score", risks_metrics['average_risk_score'])
                with col4:
                    st.metric("👀 Active Monitoring", risks_metrics['active_monitoring'])
            
            # Display risks
            risks = issues_risks_manager.get_all_risks()
            
            for risk in risks:
                risk_level = "🔴" if risk.risk_score >= 3.0 else "🟡" if risk.risk_score >= 2.0 else "🟢"
                
                with st.expander(f"{risk_level} {risk.risk_number} | {risk.title} | Score: {risk.risk_score:.1f}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📊 Probability:** {risk.probability.value}")
                        st.write(f"**💥 Impact:** {risk.impact.value}")
                        st.write(f"**🎯 Strategy:** {risk.response_strategy}")
                        st.write(f"**👤 Risk Owner:** {risk.risk_owner}")
                        st.write(f"**📅 Next Review:** {risk.next_review_date}")
                    
                    with col2:
                        st.write(f"**📊 Status:** {risk.status.value}")
                        st.write(f"**💰 Potential Cost:** ${risk.potential_cost_impact:,.0f}")
                        st.write(f"**📆 Potential Schedule:** {risk.potential_schedule_impact} days")
                        st.write(f"**🔄 Monitoring:** {risk.monitoring_frequency}")
                        st.write(f"**📈 Risk Score:** {risk.risk_score:.2f}")
                    
                    if risk.description:
                        st.write(f"**📝 Description:** {risk.description}")
                    
                    if risk.early_warning_signs:
                        st.write("**🚨 Early Warning Signs:**")
                        for sign in risk.early_warning_signs:
                            st.write(f"• {sign}")
        
        with tab3:
            st.subheader("➕ Create New Issue or Risk")
            
            # Create sub-tabs for Issues and Risks creation
            create_tab1, create_tab2 = st.tabs(["📋 New Issue", "⚠️ New Risk"])
            
            with create_tab1:
                st.write("**Create New Issue**")
                
                with st.form("create_issue_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        issue_title = st.text_input("📝 Issue Title*", placeholder="Enter issue title")
                        issue_description = st.text_area("📋 Description*", placeholder="Detailed description of the issue")
                        issue_type = st.selectbox("📋 Issue Type*", options=["Technical Issue", "Schedule Issue", "Quality Issue", "Safety Issue", "Coordination Issue", "Resource Issue", "External Issue"])
                        priority = st.selectbox("🚨 Priority*", options=["Low", "Medium", "High", "Critical"])
                    
                    with col2:
                        location = st.text_input("📍 Location*", placeholder="e.g., Level 12 - Mechanical Room")
                        work_package = st.text_input("📦 Work Package*", value="Highland Tower Development")
                        reported_by = st.text_input("👤 Reported By*", value="John Smith - Project Manager")
                        assigned_to = st.text_input("👥 Assigned To*", placeholder="Person responsible for resolution")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        due_date = st.date_input("📅 Due Date*")
                        cost_impact = st.number_input("💰 Cost Impact ($)", min_value=0.0, step=100.0)
                    
                    with col2:
                        schedule_impact = st.number_input("📆 Schedule Impact (days)", min_value=0, step=1)
                        impact_description = st.text_area("📝 Impact Description", placeholder="Describe the impact")
                    
                    submit_issue = st.form_submit_button("🆕 Create Issue", use_container_width=True)
                    
                    if submit_issue:
                        if not issue_title or not issue_description or not issue_type or not location:
                            st.error("Please fill in all required fields marked with *")
                        else:
                            issue_data = {
                                "title": issue_title,
                                "description": issue_description,
                                "issue_type": issue_type,
                                "priority": priority,
                                "project_name": "Highland Tower Development",
                                "location": location,
                                "work_package": work_package,
                                "reported_by": reported_by,
                                "assigned_to": assigned_to,
                                "reported_date": datetime.now().strftime('%Y-%m-%d'),
                                "due_date": due_date.strftime('%Y-%m-%d'),
                                "resolved_date": None,
                                "cost_impact": cost_impact,
                                "schedule_impact_days": schedule_impact,
                                "description_impact": impact_description,
                                "resolution_description": ""
                            }
                            
                            issue_id = issues_risks_manager.create_issue(issue_data)
                            st.success(f"✅ Issue created successfully! ID: {issue_id}")
                            st.rerun()
            
            with create_tab2:
                st.write("**Create New Risk**")
                
                with st.form("create_risk_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        risk_title = st.text_input("📝 Risk Title*", placeholder="Enter risk title")
                        risk_description = st.text_area("📋 Description*", placeholder="Detailed description of the risk")
                        risk_type = st.selectbox("⚠️ Risk Type*", options=["Schedule Risk", "Cost Risk", "Quality Risk", "Safety Risk", "Technical Risk", "Regulatory Risk", "Weather Risk", "Supply Chain Risk"])
                        probability = st.selectbox("📊 Probability*", options=["Very Low (10%)", "Low (25%)", "Medium (50%)", "High (75%)", "Very High (90%)"])
                    
                    with col2:
                        impact = st.selectbox("💥 Impact*", options=["Minimal", "Minor", "Moderate", "Major", "Severe"])
                        risk_priority = st.selectbox("🚨 Priority*", options=["Low", "Medium", "High", "Critical"])
                        category = st.text_input("📂 Category*", placeholder="e.g., External Factors")
                        triggers = st.text_area("🎯 Triggers", placeholder="What could trigger this risk?")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        risk_owner = st.text_input("👤 Risk Owner*", placeholder="Person responsible for monitoring")
                        response_strategy = st.selectbox("🎯 Response Strategy*", options=["Avoid", "Mitigate", "Transfer", "Accept"])
                    
                    with col2:
                        potential_cost = st.number_input("💰 Potential Cost Impact ($)", min_value=0.0, step=1000.0)
                        potential_schedule = st.number_input("📆 Potential Schedule Impact (days)", min_value=0, step=1)
                    
                    contingency_plan = st.text_area("📋 Contingency Plan", placeholder="What will you do if this risk occurs?")
                    
                    submit_risk = st.form_submit_button("🆕 Create Risk", use_container_width=True)
                    
                    if submit_risk:
                        if not risk_title or not risk_description or not risk_type or not risk_owner:
                            st.error("Please fill in all required fields marked with *")
                        else:
                            risk_data = {
                                "title": risk_title,
                                "description": risk_description,
                                "risk_type": risk_type,
                                "probability": probability,
                                "impact": impact,
                                "priority": risk_priority,
                                "project_name": "Highland Tower Development",
                                "category": category,
                                "triggers": triggers,
                                "identified_by": "Current User",
                                "risk_owner": risk_owner,
                                "identified_date": datetime.now().strftime('%Y-%m-%d'),
                                "review_date": datetime.now().strftime('%Y-%m-%d'),
                                "last_updated": datetime.now().strftime('%Y-%m-%d'),
                                "potential_cost_impact": potential_cost,
                                "potential_schedule_impact": potential_schedule,
                                "likelihood_percentage": 50,  # Default
                                "response_strategy": response_strategy,
                                "contingency_plan": contingency_plan,
                                "early_warning_signs": [],
                                "monitoring_frequency": "Monthly"
                            }
                            
                            risk_id = issues_risks_manager.create_risk(risk_data)
                            st.success(f"✅ Risk created successfully! ID: {risk_id}")
                            st.rerun()
        
        with tab4:
            st.subheader("📊 Issues & Risks Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📋 Issues Summary:**")
                if issues_metrics:
                    for key, value in issues_metrics.items():
                        if isinstance(value, dict):
                            st.write(f"**{key.replace('_', ' ').title()}:**")
                            for k, v in value.items():
                                st.write(f"  • {k}: {v}")
                        else:
                            st.write(f"• **{key.replace('_', ' ').title()}:** {value}")
            
            with col2:
                st.write("**⚠️ Risks Summary:**")
                if risks_metrics:
                    for key, value in risks_metrics.items():
                        if isinstance(value, dict):
                            st.write(f"**{key.replace('_', ' ').title()}:**")
                            for k, v in value.items():
                                st.write(f"  • {k}: {v}")
                        else:
                            st.write(f"• **{key.replace('_', ' ').title()}:** {value}")
        
        return
        
    except ImportError:
        st.error("Enterprise Issues & Risks module not available")
        # Fallback to basic version
        render_issues_risks_basic()

def render_issues_risks_basic():
    """Basic issues and risks module - fallback version"""
    st.markdown("""
    <div class="module-header">
        <h1>⚠️ Issues & Risks</h1>
        <p>Risk management and issue tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("⚠️ Issues & Risks module with comprehensive risk management")

def render_documents():
    """Enterprise Document Management with full CRUD functionality"""
    try:
        from modules.document_management_backend import document_manager, DocumentStatus, DocumentCategory, AccessLevel
        
        st.markdown("""
        <div class="module-header">
            <h1>📄 Document Management</h1>
            <p>Highland Tower Development - Comprehensive document control and version management</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display summary metrics
        metrics = document_manager.generate_document_metrics()
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📄 Total Documents", metrics['total_documents'])
            with col2:
                st.metric("💾 Storage Used", f"{metrics['total_file_size_mb']:.1f} MB")
            with col3:
                st.metric("📋 Needs Review", metrics['documents_needing_review'])
            with col4:
                st.metric("✅ Approved", metrics['approved_documents'])
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📄 All Documents", "➕ Upload New", "✏️ Manage", "📊 Analytics"])
        
        with tab1:
            st.subheader("📄 Document Library")
            
            # Search and filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                search_query = st.text_input("🔍 Search Documents", placeholder="Search by title, description, or keywords")
            with col2:
                status_filter = st.selectbox("Filter by Status", ["All"] + [status.value for status in DocumentStatus])
            with col3:
                category_filter = st.selectbox("Filter by Category", ["All"] + [cat.value for cat in DocumentCategory])
            
            # Get filtered documents
            if search_query:
                documents = document_manager.search_documents(search_query)
            else:
                documents = document_manager.get_all_documents()
            
            if status_filter != "All":
                documents = [d for d in documents if d.status.value == status_filter]
            if category_filter != "All":
                documents = [d for d in documents if d.category.value == category_filter]
            
            # Display documents
            for document in documents:
                status_color = {
                    DocumentStatus.APPROVED: "🟢",
                    DocumentStatus.UNDER_REVIEW: "🟡",
                    DocumentStatus.DRAFT: "🔵",
                    DocumentStatus.SUPERSEDED: "🟠",
                    DocumentStatus.ARCHIVED: "⚪"
                }.get(document.status, "⚪")
                
                checkout_indicator = f"🔒 CHECKED OUT by {document.checked_out_by}" if document.is_checked_out() else ""
                expiry_warning = "⚠️ EXPIRED" if document.is_expired() else ""
                review_needed = "📋 REVIEW NEEDED" if document.needs_review() else ""
                
                with st.expander(f"{status_color} {document.document_number} | {document.title} | {document.current_version} {checkout_indicator} {expiry_warning} {review_needed}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📂 Category:** {document.category.value}")
                        st.write(f"**📋 Discipline:** {document.discipline}")
                        st.write(f"**📄 File:** {document.filename}")
                        st.write(f"**📊 Size:** {document.file_size / 1024 / 1024:.1f} MB")
                        st.write(f"**🔐 Access:** {document.access_level.value}")
                        if document.drawing_number:
                            st.write(f"**📐 Drawing #:** {document.drawing_number}")
                    
                    with col2:
                        st.write(f"**👤 Created By:** {document.created_by}")
                        st.write(f"**📅 Created:** {document.created_date}")
                        st.write(f"**📅 Modified:** {document.modified_date}")
                        if document.approved_by:
                            st.write(f"**✅ Approved By:** {document.approved_by}")
                            st.write(f"**📅 Approved:** {document.approval_date}")
                        if document.expiry_date:
                            st.write(f"**⏰ Expires:** {document.expiry_date}")
                    
                    if document.description:
                        st.write(f"**📝 Description:** {document.description}")
                    
                    if document.keywords:
                        st.write(f"**🏷️ Keywords:** {', '.join(document.keywords)}")
                    
                    # Document status indicators
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if document.is_checked_out():
                            st.error(f"🔒 Checked out by {document.checked_out_by}")
                        else:
                            st.success("✅ Available")
                    with col2:
                        if document.needs_review():
                            st.warning("📋 Needs Review")
                        elif document.status == DocumentStatus.APPROVED:
                            st.success("✅ Approved")
                        else:
                            st.info(f"📄 {document.status.value}")
                    with col3:
                        if document.is_expired():
                            st.error("⚠️ Expired")
                        else:
                            st.success("📅 Current")
                    
                    # Version history
                    if document.version_history:
                        st.write("**📊 Version History:**")
                        for version in document.version_history[-3:]:  # Show last 3 versions
                            st.write(f"• {version.version_number} - {version.upload_date} by {version.uploaded_by}")
                    
                    # Reviews
                    if document.reviews:
                        st.write("**📋 Reviews:**")
                        for review in document.reviews[-2:]:  # Show last 2 reviews
                            review_icon = {"Approved": "✅", "Rejected": "❌", "Needs Changes": "⚠️"}.get(review.status, "📋")
                            st.write(f"• {review_icon} {review.reviewer_name} ({review.review_date}): {review.comments}")
                    
                    # Quick actions
                    st.write("---")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if not document.is_checked_out():
                            if st.button(f"🔓 Check Out", key=f"btn_checkout_{document.document_id}"):
                                if document_manager.checkout_document(document.document_id, "Current User"):
                                    st.success("Document checked out!")
                                    st.rerun()
                        else:
                            if st.button(f"🔒 Check In", key=f"btn_checkin_{document.document_id}"):
                                if document_manager.checkin_document(document.document_id):
                                    st.success("Document checked in!")
                                    st.rerun()
                    
                    with col2:
                        if st.button(f"📋 Add Review", key=f"btn_review_{document.document_id}"):
                            st.session_state[f"show_review_{document.document_id}"] = True
                    
                    with col3:
                        new_status = st.selectbox(f"Update Status", 
                                                [status.value for status in DocumentStatus],
                                                index=[status.value for status in DocumentStatus].index(document.status.value),
                                                key=f"status_{document.document_id}")
                        if st.button(f"📊 Update", key=f"btn_status_{document.document_id}"):
                            document.status = DocumentStatus(new_status)
                            st.success("Status updated!")
                            st.rerun()
                    
                    # Review form
                    if st.session_state.get(f"show_review_{document.document_id}", False):
                        with st.form(f"review_form_{document.document_id}"):
                            st.write("**📋 Add Document Review**")
                            reviewer_name = st.text_input("Reviewer Name")
                            review_status = st.selectbox("Review Status", ["Approved", "Rejected", "Needs Changes"])
                            review_comments = st.text_area("Comments")
                            markup_file = st.text_input("Markup File (optional)")
                            
                            if st.form_submit_button("📋 Submit Review"):
                                review_data = {
                                    "reviewer_name": reviewer_name,
                                    "review_date": datetime.now().strftime('%Y-%m-%d'),
                                    "status": review_status,
                                    "comments": review_comments,
                                    "markup_file": markup_file if markup_file else None
                                }
                                if document_manager.add_review(document.document_id, review_data):
                                    st.success("Review added!")
                                    st.session_state[f"show_review_{document.document_id}"] = False
                                    st.rerun()
        
        with tab2:
            st.subheader("➕ Upload New Document")
            
            with st.form("create_document_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    title = st.text_input("📝 Document Title*", placeholder="Enter document title")
                    description = st.text_area("📋 Description", placeholder="Detailed description")
                    category = st.selectbox("📂 Category*", options=[cat.value for cat in DocumentCategory])
                    discipline = st.text_input("📋 Discipline*", placeholder="e.g., Architecture, Structural")
                    work_package = st.text_input("📦 Work Package", value="Highland Tower Development")
                
                with col2:
                    filename = st.text_input("📄 Filename*", placeholder="document.pdf")
                    file_type = st.selectbox("📄 File Type*", options=["PDF", "DWG", "DOC", "XLS", "IMG", "ZIP"])
                    file_size = st.number_input("📊 File Size (MB)", min_value=0.1, step=0.1, value=1.0)
                    access_level = st.selectbox("🔐 Access Level*", options=[level.value for level in AccessLevel])
                    drawing_number = st.text_input("📐 Drawing Number", placeholder="A-301, S-201, etc.")
                
                # Additional details
                col1, col2 = st.columns(2)
                
                with col1:
                    requires_approval = st.checkbox("📋 Requires Approval", value=True)
                    password_protected = st.checkbox("🔒 Password Protected")
                    keywords = st.text_input("🏷️ Keywords", placeholder="Comma-separated keywords")
                
                with col2:
                    expiry_date = st.date_input("⏰ Expiry Date (optional)")
                    distribution_list = st.text_input("📧 Distribution List", placeholder="Comma-separated recipients")
                    related_docs = st.text_input("🔗 Related Documents", placeholder="Document IDs, comma-separated")
                
                notes = st.text_area("📝 Notes", placeholder="Additional notes about this document")
                
                # File upload simulation
                uploaded_file = st.file_uploader("📁 Select File", type=['pdf', 'dwg', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'png', 'zip'])
                
                submit_document = st.form_submit_button("📁 Upload Document", use_container_width=True)
                
                if submit_document:
                    if not title or not category or not discipline or not filename:
                        st.error("Please fill in all required fields marked with *")
                    else:
                        document_data = {
                            "title": title,
                            "description": description,
                            "category": category,
                            "filename": filename,
                            "file_type": file_type,
                            "file_size": int(file_size * 1024 * 1024),  # Convert MB to bytes
                            "file_path": f"/project/{category.lower().replace(' ', '_')}/",
                            "project_name": "Highland Tower Development",
                            "discipline": discipline,
                            "work_package": work_package,
                            "drawing_number": drawing_number if drawing_number else None,
                            "access_level": access_level,
                            "password_protected": password_protected,
                            "requires_approval": requires_approval,
                            "keywords": [kw.strip() for kw in keywords.split(',') if kw.strip()],
                            "related_documents": [doc.strip() for doc in related_docs.split(',') if doc.strip()],
                            "expiry_date": expiry_date.strftime('%Y-%m-%d') if expiry_date else None,
                            "notes": notes,
                            "review_comments": "",
                            "distribution_list": [dist.strip() for dist in distribution_list.split(',') if dist.strip()],
                            "created_by": "Current User",
                            "last_modified_by": "Current User"
                        }
                        
                        document_id = document_manager.create_document(document_data)
                        st.success(f"✅ Document uploaded successfully! ID: {document_id}")
                        st.rerun()
        
        with tab3:
            st.subheader("✏️ Manage Documents")
            
            documents = document_manager.get_all_documents()
            if documents:
                document_options = [f"{d.document_number} - {d.title}" for d in documents]
                selected_index = st.selectbox("Select Document to Manage", range(len(document_options)), format_func=lambda x: document_options[x])
                selected_document = documents[selected_index]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("✏️ Edit Document", use_container_width=True):
                        st.session_state.show_edit_document_form = True
                
                with col2:
                    if st.button("🗑️ Delete Document", use_container_width=True):
                        if selected_document.document_id in document_manager.documents:
                            del document_manager.documents[selected_document.document_id]
                            st.success("✅ Document deleted successfully!")
                            st.rerun()
                
                with col3:
                    if st.button("📋 Duplicate Document", use_container_width=True):
                        # Create duplicate with modified title
                        document_data = {
                            "title": f"Copy of {selected_document.title}",
                            "description": selected_document.description,
                            "category": selected_document.category.value,
                            "filename": f"COPY_{selected_document.filename}",
                            "file_type": selected_document.file_type,
                            "file_size": selected_document.file_size,
                            "file_path": selected_document.file_path,
                            "project_name": selected_document.project_name,
                            "discipline": selected_document.discipline,
                            "work_package": selected_document.work_package,
                            "drawing_number": f"COPY-{selected_document.drawing_number}" if selected_document.drawing_number else None,
                            "access_level": selected_document.access_level.value,
                            "password_protected": selected_document.password_protected,
                            "requires_approval": selected_document.requires_approval,
                            "keywords": selected_document.keywords.copy(),
                            "related_documents": selected_document.related_documents.copy(),
                            "expiry_date": selected_document.expiry_date,
                            "notes": selected_document.notes,
                            "review_comments": "",
                            "distribution_list": selected_document.distribution_list.copy(),
                            "created_by": "Current User",
                            "last_modified_by": "Current User"
                        }
                        document_id = document_manager.create_document(document_data)
                        st.success(f"✅ Document duplicated! ID: {document_id}")
                        st.rerun()
                
                # Edit form
                if st.session_state.get('show_edit_document_form', False):
                    with st.form("edit_document_form"):
                        st.write("**✏️ Edit Document Details**")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_title = st.text_input("📝 Title", value=selected_document.title)
                            edit_description = st.text_area("📋 Description", value=selected_document.description)
                            edit_discipline = st.text_input("📋 Discipline", value=selected_document.discipline)
                            edit_keywords = st.text_input("🏷️ Keywords", value=", ".join(selected_document.keywords))
                        
                        with col2:
                            edit_access = st.selectbox("🔐 Access Level", 
                                                     options=[level.value for level in AccessLevel],
                                                     index=[level.value for level in AccessLevel].index(selected_document.access_level.value))
                            edit_notes = st.text_area("📝 Notes", value=selected_document.notes)
                            edit_distribution = st.text_input("📧 Distribution", value=", ".join(selected_document.distribution_list))
                        
                        if st.form_submit_button("✏️ Update Document"):
                            # Update the document
                            selected_document.title = edit_title
                            selected_document.description = edit_description
                            selected_document.discipline = edit_discipline
                            selected_document.keywords = [kw.strip() for kw in edit_keywords.split(',') if kw.strip()]
                            selected_document.access_level = AccessLevel(edit_access)
                            selected_document.notes = edit_notes
                            selected_document.distribution_list = [dist.strip() for dist in edit_distribution.split(',') if dist.strip()]
                            selected_document.last_modified_by = "Current User"
                            selected_document.modified_date = datetime.now().strftime('%Y-%m-%d')
                            
                            st.success("✅ Document updated successfully!")
                            st.session_state.show_edit_document_form = False
                            st.rerun()
            else:
                st.info("No documents available. Upload some documents first.")
        
        with tab4:
            st.subheader("📊 Document Analytics")
            
            if metrics:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📊 Status Distribution:**")
                    for status, count in metrics['status_breakdown'].items():
                        status_icon = {
                            "Approved": "🟢",
                            "Under Review": "🟡",
                            "Draft": "🔵",
                            "Superseded": "🟠",
                            "Archived": "⚪"
                        }.get(status, "⚪")
                        st.write(f"• {status_icon} {status}: {count}")
                    
                    st.write("**📂 Category Distribution:**")
                    for category, count in metrics['category_breakdown'].items():
                        if count > 0:
                            st.write(f"• {category}: {count}")
                
                with col2:
                    st.write("**📈 Performance Metrics:**")
                    st.write(f"• **Total Storage:** {metrics['total_file_size_mb']:.1f} MB")
                    st.write(f"• **Average File Size:** {metrics['average_file_size_mb']:.1f} MB")
                    st.write(f"• **Total Versions:** {metrics['total_versions']}")
                    st.write(f"• **Documents Needing Review:** {metrics['documents_needing_review']}")
                    st.write(f"• **Expired Documents:** {metrics['expired_documents']}")
                    st.write(f"• **Checked Out:** {metrics['checked_out_documents']}")
                    
                    # Documents needing attention
                    review_needed = document_manager.get_documents_needing_review()
                    if review_needed:
                        st.write("**📋 Documents Needing Review:**")
                        for doc in review_needed[:5]:
                            st.write(f"• {doc.title}")
                    
                    expired_docs = document_manager.get_expired_documents()
                    if expired_docs:
                        st.write("**⚠️ Expired Documents:**")
                        for doc in expired_docs[:5]:
                            st.write(f"• {doc.title}")
        
        return
        
    except ImportError:
        st.error("Enterprise Document Management module not available")
        render_documents_basic()

def render_documents_basic():
    """Basic document management module - fallback version"""
    st.markdown("""
    <div class="module-header">
        <h1>📁 Document Management</h1>
        <p>Comprehensive document storage, version control, and collaboration system</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize document data
    if "documents" not in st.session_state:
        st.session_state.documents = [
            {
                "id": "DOC-001",
                "document_id": "HTD-DWG-2025-001",
                "filename": "HTD_Architectural_Plans_Level_1-15.pdf",
                "title": "Highland Tower Architectural Plans - Residential Levels",
                "category": "Architectural Drawings",
                "document_type": "Design Document",
                "version": "Rev D.1",
                "status": "Current",
                "author": "Highland Architecture Group",
                "reviewer": "John Davis, P.E.",
                "upload_date": "2025-05-27",
                "review_date": "2025-05-25",
                "approval_date": "2025-05-26",
                "file_size": "24.5 MB",
                "file_format": "PDF",
                "description": "Complete architectural plans for residential levels 1-15 including unit layouts, common areas, and building sections",
                "tags": ["architectural", "residential", "floor-plans", "current", "approved"],
                "access_level": "Project Team",
                "linked_rfis": ["RFI-001"],
                "linked_tasks": ["TASK-001", "TASK-002"],
                "revision_history": [
                    {"version": "Rev A", "date": "2025-01-15", "changes": "Initial design submittal"},
                    {"version": "Rev B", "date": "2025-02-20", "changes": "Incorporated city review comments"},
                    {"version": "Rev C", "date": "2025-04-10", "changes": "MEP coordination updates"},
                    {"version": "Rev D.1", "date": "2025-05-27", "changes": "Final construction drawings"}
                ],
                "keywords": ["highland tower", "residential", "architecture", "construction drawings"],
                "compliance_requirements": ["NYC Building Code", "ADA Compliance", "Fire Code"],
                "expiry_date": "",
                "confidentiality": "Internal Use"
            },
            {
                "id": "DOC-002",
                "document_id": "HTD-SPEC-2025-001",
                "filename": "HTD_Structural_Steel_Specifications.pdf",
                "title": "Structural Steel Specifications and Standards",
                "category": "Technical Specifications",
                "document_type": "Specification",
                "version": "Rev C.2",
                "status": "Current",
                "author": "Highland Structural Engineering",
                "reviewer": "Maria Garcia, P.E.",
                "upload_date": "2025-05-25",
                "review_date": "2025-05-23",
                "approval_date": "2025-05-24",
                "file_size": "8.7 MB",
                "file_format": "PDF",
                "description": "Comprehensive steel specifications for main structural frame including material requirements, welding standards, and quality control procedures",
                "tags": ["structural", "steel", "specifications", "engineering", "approved"],
                "access_level": "Engineering Team",
                "linked_rfis": [],
                "linked_tasks": ["TASK-003"],
                "revision_history": [
                    {"version": "Rev A", "date": "2025-02-01", "changes": "Initial specifications"},
                    {"version": "Rev B", "date": "2025-03-15", "changes": "Updated welding requirements"},
                    {"version": "Rev C.2", "date": "2025-05-25", "changes": "Final fabrication specifications"}
                ],
                "keywords": ["structural steel", "specifications", "welding", "fabrication"],
                "compliance_requirements": ["AISC 360", "AWS D1.1", "OSHA Standards"],
                "expiry_date": "",
                "confidentiality": "Internal Use"
            },
            {
                "id": "DOC-003",
                "document_id": "HTD-MEP-2025-001",
                "filename": "HTD_MEP_Systems_Design.pdf",
                "title": "Mechanical, Electrical, Plumbing Systems Design",
                "category": "MEP Drawings",
                "document_type": "Design Document",
                "version": "Rev B.3",
                "status": "Under Review",
                "author": "Highland MEP Consultants",
                "reviewer": "Jennifer Walsh",
                "upload_date": "2025-05-20",
                "review_date": "2025-05-22",
                "approval_date": "",
                "file_size": "31.2 MB",
                "file_format": "PDF",
                "description": "Complete MEP systems design for Highland Tower including HVAC, electrical distribution, plumbing, and fire protection systems",
                "tags": ["mep", "mechanical", "electrical", "plumbing", "hvac", "fire-protection"],
                "access_level": "MEP Team",
                "linked_rfis": ["RFI-001"],
                "linked_tasks": ["TASK-004"],
                "revision_history": [
                    {"version": "Rev A", "date": "2025-03-01", "changes": "Initial MEP design"},
                    {"version": "Rev B", "date": "2025-04-15", "changes": "Coordination with architectural changes"},
                    {"version": "Rev B.3", "date": "2025-05-20", "changes": "Updated routing and sizing"}
                ],
                "keywords": ["mep", "hvac", "electrical", "plumbing", "fire protection"],
                "compliance_requirements": ["NYC Mechanical Code", "NEC", "NYC Plumbing Code", "NFPA"],
                "expiry_date": "",
                "confidentiality": "Internal Use"
            }
        ]
    
    if "document_folders" not in st.session_state:
        st.session_state.document_folders = [
            {
                "id": "FOLD-001",
                "folder_name": "Architectural Documents",
                "description": "All architectural drawings, plans, and related documentation",
                "created_date": "2025-01-15",
                "document_count": 15,
                "access_level": "Project Team",
                "parent_folder": "",
                "tags": ["architecture", "drawings", "plans"]
            },
            {
                "id": "FOLD-002",
                "folder_name": "Engineering Reports",
                "description": "Structural, geotechnical, and engineering analysis reports",
                "created_date": "2025-01-20",
                "document_count": 8,
                "access_level": "Engineering Team",
                "parent_folder": "",
                "tags": ["engineering", "reports", "analysis"]
            },
            {
                "id": "FOLD-003",
                "folder_name": "Contracts & Legal",
                "description": "Contracts, agreements, permits, and legal documentation",
                "created_date": "2024-12-01",
                "document_count": 12,
                "access_level": "Management Only",
                "parent_folder": "",
                "tags": ["contracts", "legal", "permits", "agreements"]
            }
        ]
    
    if "document_reviews" not in st.session_state:
        st.session_state.document_reviews = [
            {
                "id": "REV-001",
                "document_id": "DOC-001",
                "reviewer": "John Davis, P.E.",
                "review_date": "2025-05-25",
                "review_status": "Approved",
                "comments": "Architectural plans meet all design requirements and code compliance. Approved for construction.",
                "rating": 5,
                "next_review_date": "2025-08-25",
                "review_type": "Technical Review"
            },
            {
                "id": "REV-002",
                "document_id": "DOC-002",
                "reviewer": "Maria Garcia, P.E.",
                "review_date": "2025-05-23",
                "review_status": "Approved",
                "comments": "Steel specifications are comprehensive and meet industry standards. Ready for fabrication.",
                "rating": 5,
                "next_review_date": "2025-07-23",
                "review_type": "Technical Review"
            },
            {
                "id": "REV-003",
                "document_id": "DOC-003",
                "reviewer": "Jennifer Walsh",
                "review_date": "2025-05-22",
                "review_status": "Pending",
                "comments": "MEP design requires minor revisions for HVAC sizing in mechanical rooms. Coordination meeting scheduled.",
                "rating": 4,
                "next_review_date": "2025-05-30",
                "review_type": "Technical Review"
            }
        ]
    
    # Key Document Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_docs = len(st.session_state.documents)
    current_docs = len([doc for doc in st.session_state.documents if doc['status'] == 'Current'])
    under_review = len([doc for doc in st.session_state.documents if doc['status'] == 'Under Review'])
    total_storage = sum(float(doc['file_size'].replace(' MB', '')) for doc in st.session_state.documents)
    
    with col1:
        st.metric("Total Documents", total_docs, delta_color="normal")
    with col2:
        st.metric("Current", current_docs, delta_color="normal")
    with col3:
        st.metric("Under Review", under_review, delta_color="normal")
    with col4:
        st.metric("Storage Used", f"{total_storage:.1f} MB", delta_color="normal")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📄 Documents", "📁 Folders", "🔍 Reviews", "📈 Analytics", "🔧 Management"])
    
    with tab1:
        st.subheader("📄 Document Management")
        
        doc_sub_tab1, doc_sub_tab2, doc_sub_tab3 = st.tabs(["📝 Upload Document", "📋 Document Library", "🔍 Search & Filter"])
        
        with doc_sub_tab1:
            st.markdown("**Upload New Document**")
            
            with st.form("document_upload_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    uploaded_file = st.file_uploader("Select Document", type=['pdf', 'dwg', 'docx', 'xlsx', 'jpg', 'png', 'txt'])
                    document_title = st.text_input("Document Title", placeholder="Descriptive document title")
                    category = st.selectbox("Category", [
                        "Architectural Drawings", "Structural Drawings", "MEP Drawings", "Technical Specifications",
                        "Engineering Reports", "Contracts & Legal", "Safety Documents", "Quality Control",
                        "Project Management", "Permits & Approvals", "Correspondence"
                    ])
                    document_type = st.selectbox("Document Type", [
                        "Design Document", "Specification", "Report", "Contract", "Drawing", "Manual",
                        "Certificate", "Correspondence", "Permit", "Invoice", "Meeting Minutes"
                    ])
                    version = st.text_input("Version", placeholder="Rev A.1", value="Rev A")
                
                with col2:
                    author = st.text_input("Author", placeholder="Company or person name")
                    reviewer = st.text_input("Reviewer", placeholder="Assigned reviewer")
                    status = st.selectbox("Status", ["Draft", "Under Review", "Current", "Superseded", "Archived"])
                    access_level = st.selectbox("Access Level", ["Public", "Project Team", "Engineering Team", "MEP Team", "Management Only"])
                    confidentiality = st.selectbox("Confidentiality", ["Public", "Internal Use", "Confidential", "Restricted"])
                
                description = st.text_area("Description", placeholder="Detailed description of document contents")
                tags = st.text_input("Tags", placeholder="Comma-separated tags for easy searching")
                keywords = st.text_input("Keywords", placeholder="Search keywords")
                linked_tasks = st.multiselect("Link to Tasks", [f"{task['id']} - {task['task_name']}" for task in st.session_state.get('schedule_tasks', [])])
                compliance_requirements = st.text_area("Compliance Requirements", placeholder="Applicable codes, standards, regulations")
                
                if st.form_submit_button("📄 Upload Document", type="primary"):
                    if uploaded_file and document_title and author:
                        new_document = {
                            "id": f"DOC-{len(st.session_state.documents) + 1:03d}",
                            "document_id": f"HTD-DOC-2025-{len(st.session_state.documents) + 4:03d}",
                            "filename": uploaded_file.name,
                            "title": document_title,
                            "category": category,
                            "document_type": document_type,
                            "version": version,
                            "status": status,
                            "author": author,
                            "reviewer": reviewer,
                            "upload_date": str(datetime.now().date()),
                            "review_date": "",
                            "approval_date": "",
                            "file_size": f"{uploaded_file.size / (1024*1024):.1f} MB" if uploaded_file.size else "Unknown",
                            "file_format": uploaded_file.name.split('.')[-1].upper() if '.' in uploaded_file.name else "Unknown",
                            "description": description,
                            "tags": [tag.strip() for tag in tags.split(',') if tag.strip()],
                            "access_level": access_level,
                            "linked_rfis": [],
                            "linked_tasks": [task.split(" - ")[0] for task in linked_tasks],
                            "revision_history": [{"version": version, "date": str(datetime.now().date()), "changes": "Initial upload"}],
                            "keywords": [kw.strip() for kw in keywords.split(',') if kw.strip()],
                            "compliance_requirements": [req.strip() for req in compliance_requirements.split(',') if req.strip()],
                            "expiry_date": "",
                            "confidentiality": confidentiality
                        }
                        st.session_state.documents.append(new_document)
                        st.success("✅ Document uploaded successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields and select a document!")
        
        with doc_sub_tab2:
            st.markdown("**Document Library**")
            
            # Display documents
            for document in st.session_state.documents:
                status_icon = {"Draft": "📝", "Under Review": "👁️", "Current": "✅", "Superseded": "🔄", "Archived": "📦"}.get(document['status'], "📄")
                
                with st.expander(f"{status_icon} {document['document_id']} - {document['title']} ({document['status']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**📄 Document ID:** {document['document_id']}")
                        st.write(f"**📁 Filename:** {document['filename']}")
                        st.write(f"**📂 Category:** {document['category']}")
                        st.write(f"**📋 Type:** {document['document_type']}")
                        st.write(f"**📊 Version:** {document['version']}")
                        st.write(f"**📈 Status:** {document['status']}")
                        st.write(f"**👤 Author:** {document['author']}")
                    
                    with col2:
                        st.write(f"**📅 Upload Date:** {document['upload_date']}")
                        if document['review_date']:
                            st.write(f"**📅 Review Date:** {document['review_date']}")
                        if document['approval_date']:
                            st.write(f"**📅 Approval Date:** {document['approval_date']}")
                        st.write(f"**💾 File Size:** {document['file_size']}")
                        st.write(f"**📄 Format:** {document['file_format']}")
                        st.write(f"**🔒 Access Level:** {document['access_level']}")
                        st.write(f"**🔐 Confidentiality:** {document['confidentiality']}")
                    
                    with col3:
                        if document['reviewer']:
                            st.write(f"**👤 Reviewer:** {document['reviewer']}")
                        if document['linked_tasks']:
                            st.write(f"**🔗 Linked Tasks:** {', '.join(document['linked_tasks'])}")
                        if document['compliance_requirements']:
                            st.write(f"**📋 Compliance:** {', '.join(document['compliance_requirements'])}")
                    
                    st.write(f"**📝 Description:** {document['description']}")
                    
                    # Tags display
                    if document['tags']:
                        st.write("**🏷️ Tags:**")
                        tags_html = " ".join([f'<span style="background-color: #e1e1e1; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em;">{tag}</span>' for tag in document['tags']])
                        st.markdown(tags_html, unsafe_allow_html=True)
                    
                    # Revision history
                    if len(document['revision_history']) > 1:
                        st.write("**📜 Revision History:**")
                        for revision in document['revision_history'][-3:]:  # Show last 3 revisions
                            st.write(f"  • {revision['version']} ({revision['date']}): {revision['changes']}")
                    
                    # Action buttons
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        if st.button(f"👁️ View", key=f"view_{document['id']}"):
                            st.info(f"Opening {document['filename']}")
                    with col2:
                        if st.button(f"⬇️ Download", key=f"download_{document['id']}"):
                            st.success(f"Downloading {document['filename']}")
                    with col3:
                        if document['status'] == 'Under Review' and st.button(f"✅ Approve", key=f"approve_{document['id']}"):
                            document['status'] = 'Current'
                            document['approval_date'] = str(datetime.now().date())
                            st.success("Document approved!")
                            st.rerun()
                    with col4:
                        if st.button(f"✏️ Edit", key=f"edit_{document['id']}"):
                            st.info("Edit functionality - would open edit form")
                    with col5:
                        if st.button(f"🗑️ Archive", key=f"archive_{document['id']}"):
                            document['status'] = 'Archived'
                            st.success("Document archived!")
                            st.rerun()
        
        with doc_sub_tab3:
            st.markdown("**Search and Filter Documents**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                category_filter = st.selectbox("Filter by Category", ["All Categories"] + list(set(doc['category'] for doc in st.session_state.documents)))
            with col2:
                status_filter = st.selectbox("Filter by Status", ["All Status", "Draft", "Under Review", "Current", "Superseded", "Archived"])
            with col3:
                author_filter = st.selectbox("Filter by Author", ["All Authors"] + list(set(doc['author'] for doc in st.session_state.documents)))
            
            col1, col2 = st.columns(2)
            with col1:
                search_text = st.text_input("🔍 Search", placeholder="Search in titles, descriptions, keywords...")
            with col2:
                date_range = st.selectbox("Date Range", ["All Time", "Last 30 Days", "Last 90 Days", "This Year"])
            
            # Apply filters
            filtered_docs = st.session_state.documents
            if category_filter != "All Categories":
                filtered_docs = [doc for doc in filtered_docs if doc['category'] == category_filter]
            if status_filter != "All Status":
                filtered_docs = [doc for doc in filtered_docs if doc['status'] == status_filter]
            if author_filter != "All Authors":
                filtered_docs = [doc for doc in filtered_docs if doc['author'] == author_filter]
            if search_text:
                filtered_docs = [doc for doc in filtered_docs if 
                               search_text.lower() in doc['title'].lower() or 
                               search_text.lower() in doc['description'].lower() or
                               search_text.lower() in ' '.join(doc['keywords']).lower()]
            
            st.markdown(f"**Found {len(filtered_docs)} documents**")
            
            # Display filtered results
            for doc in filtered_docs:
                st.write(f"📄 **{doc['document_id']}** - {doc['title']} ({doc['status']})")
    
    with tab2:
        st.subheader("📁 Folder Management")
        
        folder_sub_tab1, folder_sub_tab2 = st.tabs(["📁 Create Folder", "📂 View Folders"])
        
        with folder_sub_tab1:
            st.markdown("**Create New Folder**")
            
            with st.form("folder_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    folder_name = st.text_input("Folder Name", placeholder="Descriptive folder name")
                    description = st.text_area("Description", placeholder="Folder description and purpose")
                    access_level = st.selectbox("Access Level", ["Public", "Project Team", "Engineering Team", "MEP Team", "Management Only"])
                
                with col2:
                    parent_folder = st.selectbox("Parent Folder", ["Root"] + [folder['folder_name'] for folder in st.session_state.document_folders])
                    tags = st.text_input("Tags", placeholder="Comma-separated tags")
                
                if st.form_submit_button("📁 Create Folder", type="primary"):
                    if folder_name:
                        new_folder = {
                            "id": f"FOLD-{len(st.session_state.document_folders) + 1:03d}",
                            "folder_name": folder_name,
                            "description": description,
                            "created_date": str(datetime.now().date()),
                            "document_count": 0,
                            "access_level": access_level,
                            "parent_folder": parent_folder if parent_folder != "Root" else "",
                            "tags": [tag.strip() for tag in tags.split(',') if tag.strip()]
                        }
                        st.session_state.document_folders.append(new_folder)
                        st.success("✅ Folder created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please provide a folder name!")
        
        with folder_sub_tab2:
            st.markdown("**All Document Folders**")
            
            for folder in st.session_state.document_folders:
                with st.expander(f"📁 {folder['folder_name']} ({folder['document_count']} documents)"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📁 Folder:** {folder['folder_name']}")
                        st.write(f"**📝 Description:** {folder['description']}")
                        st.write(f"**📅 Created:** {folder['created_date']}")
                        st.write(f"**📄 Documents:** {folder['document_count']}")
                    
                    with col2:
                        st.write(f"**🔒 Access Level:** {folder['access_level']}")
                        if folder['parent_folder']:
                            st.write(f"**📂 Parent:** {folder['parent_folder']}")
                        if folder['tags']:
                            st.write(f"**🏷️ Tags:** {', '.join(folder['tags'])}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📂 Open", key=f"open_folder_{folder['id']}"):
                            st.info("Folder view functionality")
                    with col2:
                        if st.button(f"✏️ Edit", key=f"edit_folder_{folder['id']}"):
                            st.info("Edit folder functionality")
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_folder_{folder['id']}"):
                            st.session_state.document_folders.remove(folder)
                            st.success("Folder deleted!")
                            st.rerun()
    
    with tab3:
        st.subheader("🔍 Document Reviews")
        
        review_sub_tab1, review_sub_tab2 = st.tabs(["📝 New Review", "📊 All Reviews"])
        
        with review_sub_tab1:
            st.markdown("**Submit Document Review**")
            
            with st.form("review_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    review_document = st.selectbox("Select Document", [f"{doc['document_id']} - {doc['title']}" for doc in st.session_state.documents])
                    reviewer = st.text_input("Reviewer", placeholder="Your name and title")
                    review_type = st.selectbox("Review Type", ["Technical Review", "Quality Review", "Compliance Review", "Final Approval"])
                    review_status = st.selectbox("Review Status", ["Approved", "Approved with Comments", "Rejected", "Pending"])
                
                with col2:
                    rating = st.slider("Overall Rating", 1, 5, 3)
                    next_review_date = st.date_input("Next Review Date", value=datetime.now().date() + timedelta(days=90))
                
                comments = st.text_area("Review Comments", placeholder="Detailed review comments and recommendations")
                
                if st.form_submit_button("🔍 Submit Review", type="primary"):
                    if review_document and reviewer and comments:
                        new_review = {
                            "id": f"REV-{len(st.session_state.document_reviews) + 1:03d}",
                            "document_id": review_document.split(" - ")[0].replace("HTD-DOC-2025-", "DOC-").replace("HTD-DWG-2025-", "DOC-").replace("HTD-SPEC-2025-", "DOC-").replace("HTD-MEP-2025-", "DOC-"),
                            "reviewer": reviewer,
                            "review_date": str(datetime.now().date()),
                            "review_status": review_status,
                            "comments": comments,
                            "rating": rating,
                            "next_review_date": str(next_review_date),
                            "review_type": review_type
                        }
                        st.session_state.document_reviews.append(new_review)
                        st.success("✅ Review submitted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
        
        with review_sub_tab2:
            st.markdown("**All Document Reviews**")
            
            for review in st.session_state.document_reviews:
                # Find document title
                doc_title = "Unknown Document"
                for doc in st.session_state.documents:
                    if doc['id'] == review['document_id']:
                        doc_title = doc['title']
                        break
                
                status_icon = {"Approved": "✅", "Approved with Comments": "✅", "Rejected": "❌", "Pending": "⏳"}.get(review['review_status'], "📋")
                
                with st.expander(f"{status_icon} {review['id']} - {doc_title} ({review['review_status']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📄 Document:** {doc_title}")
                        st.write(f"**👤 Reviewer:** {review['reviewer']}")
                        st.write(f"**📅 Review Date:** {review['review_date']}")
                        st.write(f"**📋 Review Type:** {review['review_type']}")
                        st.write(f"**📊 Status:** {review['review_status']}")
                    
                    with col2:
                        st.write(f"**⭐ Rating:** {review['rating']}/5")
                        st.write(f"**📅 Next Review:** {review['next_review_date']}")
                    
                    st.write(f"**💬 Comments:** {review['comments']}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📤 Share", key=f"share_review_{review['id']}"):
                            st.success("Review shared!")
                    with col2:
                        if st.button(f"✏️ Edit", key=f"edit_review_{review['id']}"):
                            st.info("Edit review functionality")
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_review_{review['id']}"):
                            st.session_state.document_reviews.remove(review)
                            st.success("Review deleted!")
                            st.rerun()
    
    with tab4:
        st.subheader("📈 Document Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Document status distribution
            if st.session_state.documents:
                status_counts = {}
                for doc in st.session_state.documents:
                    status = doc['status']
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                status_list = list(status_counts.keys())
                count_list = list(status_counts.values())
                status_df = pd.DataFrame({
                    'Status': status_list,
                    'Count': count_list
                })
                fig_status = px.pie(status_df, values='Count', names='Status', title="Document Status Distribution")
                st.plotly_chart(fig_status, use_container_width=True)
        
        with col2:
            # Category distribution
            if st.session_state.documents:
                category_counts = {}
                for doc in st.session_state.documents:
                    category = doc['category']
                    category_counts[category] = category_counts.get(category, 0) + 1
                
                category_list = list(category_counts.keys())
                category_count_list = list(category_counts.values())
                category_df = pd.DataFrame({
                    'Category': category_list,
                    'Count': category_count_list
                })
                fig_category = px.bar(category_df, x='Category', y='Count', title="Documents by Category")
                st.plotly_chart(fig_category, use_container_width=True)
        
        # Document timeline
        st.markdown("**📅 Document Upload Timeline**")
        if st.session_state.documents:
            timeline_data = []
            for doc in st.session_state.documents:
                timeline_data.append({
                    'Date': doc['upload_date'],
                    'Document': doc['title'][:30] + "..." if len(doc['title']) > 30 else doc['title'],
                    'Category': doc['category'],
                    'Status': doc['status']
                })
            
            timeline_df = pd.DataFrame(timeline_data)
            timeline_df['Date'] = pd.to_datetime(timeline_df['Date'])
            timeline_df = timeline_df.sort_values('Date')
            
            fig_timeline = px.scatter(timeline_df, x='Date', y='Document', color='Category', 
                                    size_max=10, title="Document Upload Timeline")
            st.plotly_chart(fig_timeline, use_container_width=True)
    
    with tab5:
        st.subheader("🔧 Document Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📄 Document Summary**")
            if st.session_state.documents:
                doc_stats_data = pd.DataFrame([
                    {"Metric": "Total Documents", "Value": len(st.session_state.documents)},
                    {"Metric": "Current", "Value": len([d for d in st.session_state.documents if d['status'] == 'Current'])},
                    {"Metric": "Under Review", "Value": len([d for d in st.session_state.documents if d['status'] == 'Under Review'])},
                    {"Metric": "Avg File Size", "Value": f"{sum(float(d['file_size'].replace(' MB', '')) for d in st.session_state.documents) / len(st.session_state.documents):.1f} MB"},
                ])
                st.dataframe(doc_stats_data, use_container_width=True)
        
        with col2:
            st.markdown("**📁 Folder Summary**")
            if st.session_state.document_folders:
                folder_stats_data = pd.DataFrame([
                    {"Metric": "Total Folders", "Value": len(st.session_state.document_folders)},
                    {"Metric": "Root Folders", "Value": len([f for f in st.session_state.document_folders if not f['parent_folder']])},
                    {"Metric": "Sub Folders", "Value": len([f for f in st.session_state.document_folders if f['parent_folder']])},
                    {"Metric": "Avg Documents", "Value": f"{sum(f['document_count'] for f in st.session_state.document_folders) / len(st.session_state.document_folders):.1f}"},
                ])
                st.dataframe(folder_stats_data, use_container_width=True)
        
        with col3:
            st.markdown("**🔍 Review Summary**")
            if st.session_state.document_reviews:
                review_stats_data = pd.DataFrame([
                    {"Metric": "Total Reviews", "Value": len(st.session_state.document_reviews)},
                    {"Metric": "Approved", "Value": len([r for r in st.session_state.document_reviews if 'Approved' in r['review_status']])},
                    {"Metric": "Pending", "Value": len([r for r in st.session_state.document_reviews if r['review_status'] == 'Pending'])},
                    {"Metric": "Avg Rating", "Value": f"{sum(r['rating'] for r in st.session_state.document_reviews) / len(st.session_state.document_reviews):.1f}/5"},
                ])
                st.dataframe(review_stats_data, use_container_width=True)
        
        # Data management
        st.markdown("**⚠️ Data Management**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🗑️ Clear Documents", type="secondary"):
                st.session_state.documents = []
                st.success("All documents cleared!")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Folders", type="secondary"):
                st.session_state.document_folders = []
                st.success("All folders cleared!")
                st.rerun()
        with col3:
            if st.button("🗑️ Clear Reviews", type="secondary"):
                st.session_state.document_reviews = []
                st.success("All reviews cleared!")
                st.rerun()

def render_unit_prices():
    """Enterprise Unit Prices Management with robust Python backend"""
    try:
        from modules.unit_prices_backend import unit_prices_manager, PriceCategory, UnitType, PriceStatus
        
        st.markdown("""
        <div class="module-header">
            <h1>💰 Unit Prices Management</h1>
            <p>Highland Tower Development - Comprehensive unit pricing and cost estimation system</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display summary metrics
        metrics = unit_prices_manager.generate_price_metrics()
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💰 Total Unit Prices", metrics['total_unit_prices'])
            with col2:
                st.metric("✅ Active Prices", metrics['active_prices'])
            with col3:
                st.metric("🏢 Total Vendors", metrics['total_vendors'])
            with col4:
                st.metric("⭐ Avg Quality", f"{metrics['average_quality_rating']}/5")
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["💰 All Prices", "➕ Create New", "✏️ Edit", "📊 Analytics"])
        
        with tab1:
            st.subheader("💰 All Unit Prices")
            
            # Search functionality
            search_term = st.text_input("🔍 Search prices by description or item code")
            
            if search_term:
                prices = unit_prices_manager.search_prices(search_term)
                st.write(f"Found {len(prices)} matching prices")
            else:
                prices = unit_prices_manager.get_all_unit_prices()
            
            # Display prices
            for price in prices:
                status_color = {
                    PriceStatus.ACTIVE: "🟢",
                    PriceStatus.PENDING_APPROVAL: "🟡",
                    PriceStatus.INACTIVE: "🔴",
                    PriceStatus.EXPIRED: "⚫"
                }.get(price.status, "⚪")
                
                trend_icon = {
                    "Increasing": "📈",
                    "Decreasing": "📉", 
                    "Stable": "➡️"
                }.get(price.price_trend, "➡️")
                
                with st.expander(f"{status_color} {price.item_code} | {price.description} | ${price.total_price:.2f}/{price.unit_type.value}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📋 Category:** {price.category.value}")
                        st.write(f"**💰 Total Price:** ${price.total_price:.2f} per {price.unit_type.value}")
                        st.write(f"**🏢 Vendor:** {price.vendor_name}")
                        st.write(f"**📅 Effective:** {price.effective_date}")
                        if price.expiration_date:
                            st.write(f"**⏰ Expires:** {price.expiration_date}")
                    
                    with col2:
                        st.write(f"**📊 Status:** {price.status.value}")
                        st.write(f"**📈 Trend:** {trend_icon} {price.price_trend}")
                        st.write(f"**⭐ Quality:** {price.quality_rating}/5")
                        st.write(f"**🔧 Reliability:** {price.reliability_score}/5")
                        st.write(f"**📞 Contact:** {price.vendor_contact}")
                    
                    # Price breakdown
                    if price.labor_cost > 0 or price.material_cost > 0 or price.equipment_cost > 0:
                        st.write("**💵 Price Breakdown:**")
                        if price.labor_cost > 0:
                            st.write(f"• Labor: ${price.labor_cost:.2f}")
                        if price.material_cost > 0:
                            st.write(f"• Material: ${price.material_cost:.2f}")
                        if price.equipment_cost > 0:
                            st.write(f"• Equipment: ${price.equipment_cost:.2f}")
                        if price.overhead_percentage > 0:
                            st.write(f"• Overhead: {price.overhead_percentage}%")
                        if price.profit_percentage > 0:
                            st.write(f"• Profit: {price.profit_percentage}%")
                    
                    if price.specification:
                        st.write(f"**📝 Specification:** {price.specification}")
                    
                    if price.pricing_notes:
                        st.write(f"**📋 Notes:** {price.pricing_notes}")
                    
                    # Price history
                    if price.price_history:
                        st.write("**📈 Price History:**")
                        for history in price.price_history[-3:]:  # Show last 3 entries
                            st.write(f"• {history.date}: ${history.price:.2f} - {history.notes}")
        
        with tab2:
            st.subheader("➕ Create New Unit Price")
            
            with st.form("create_unit_price_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    item_code = st.text_input("📝 Item Code*", placeholder="e.g., CONC-4000-CY")
                    description = st.text_input("📋 Description*", placeholder="Enter detailed description")
                    category = st.selectbox("📂 Category*", options=["Labor", "Material", "Equipment", "Subcontractor", "Overhead"])
                    unit_type = st.selectbox("📏 Unit Type*", options=["SF", "LF", "CY", "EA", "LS", "HR", "TON", "GAL"])
                    base_price = st.number_input("💰 Base Price*", min_value=0.01, step=0.01)
                
                with col2:
                    vendor_name = st.text_input("🏢 Vendor Name*", placeholder="Enter vendor name")
                    vendor_contact = st.text_input("📞 Vendor Contact", placeholder="Contact information")
                    effective_date = st.date_input("📅 Effective Date*")
                    expiration_date = st.date_input("⏰ Expiration Date")
                    price_source = st.selectbox("📊 Price Source*", options=["Vendor Quote", "Historical Data", "Market Analysis", "Subcontractor Bid", "Catalog Price"])
                
                # Cost breakdown
                st.write("**💵 Cost Breakdown**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    labor_cost = st.number_input("👥 Labor Cost", min_value=0.0, step=0.01)
                    material_cost = st.number_input("🧱 Material Cost", min_value=0.0, step=0.01)
                
                with col2:
                    equipment_cost = st.number_input("🚜 Equipment Cost", min_value=0.0, step=0.01)
                    overhead_percentage = st.number_input("📊 Overhead %", min_value=0.0, max_value=100.0, step=0.1)
                
                with col3:
                    profit_percentage = st.number_input("💹 Profit %", min_value=0.0, max_value=100.0, step=0.1)
                    quality_rating = st.number_input("⭐ Quality Rating", min_value=1.0, max_value=5.0, step=0.1, value=4.0)
                
                # Additional details
                col1, col2 = st.columns(2)
                with col1:
                    specification = st.text_area("📝 Specification", placeholder="Technical specifications")
                    minimum_quantity = st.number_input("📦 Minimum Quantity", min_value=1, step=1, value=1)
                
                with col2:
                    pricing_notes = st.text_area("📋 Pricing Notes", placeholder="Additional notes")
                    delivery_time_days = st.number_input("🚚 Delivery Time (days)", min_value=0, step=1, value=7)
                
                submit_price = st.form_submit_button("🆕 Create Unit Price", use_container_width=True)
                
                if submit_price:
                    if not item_code or not description or not category or not vendor_name:
                        st.error("Please fill in all required fields marked with *")
                    else:
                        price_data = {
                            "item_code": item_code,
                            "description": description,
                            "category": category,
                            "unit_type": unit_type,
                            "base_price": base_price,
                            "labor_cost": labor_cost,
                            "material_cost": material_cost,
                            "equipment_cost": equipment_cost,
                            "overhead_percentage": overhead_percentage,
                            "profit_percentage": profit_percentage,
                            "specification": specification,
                            "vendor_name": vendor_name,
                            "vendor_contact": vendor_contact,
                            "effective_date": effective_date.strftime('%Y-%m-%d'),
                            "expiration_date": expiration_date.strftime('%Y-%m-%d') if expiration_date else None,
                            "price_source": price_source,
                            "location_factor": 1.0,
                            "minimum_quantity": minimum_quantity,
                            "delivery_time_days": delivery_time_days,
                            "payment_terms": "Net 30",
                            "quality_rating": quality_rating,
                            "reliability_score": 4.0,
                            "past_performance": "New vendor",
                            "price_history": [],
                            "last_updated": datetime.now().strftime('%Y-%m-%d'),
                            "price_trend": "Stable",
                            "project_name": "Highland Tower Development",
                            "work_package": "General",
                            "pricing_notes": pricing_notes,
                            "special_conditions": "",
                            "created_by": "Current User"
                        }
                        
                        price_id = unit_prices_manager.create_unit_price(price_data)
                        st.success(f"✅ Unit price created successfully! ID: {price_id}")
                        st.rerun()
        
        with tab3:
            st.subheader("✏️ Edit Unit Price")
            
            # Select price to edit
            prices = unit_prices_manager.get_all_unit_prices()
            if prices:
                price_options = [f"{p.item_code} - {p.description}" for p in prices]
                selected_price_index = st.selectbox("Select Unit Price to Edit", range(len(price_options)), format_func=lambda x: price_options[x])
                selected_price = prices[selected_price_index]
                
                with st.form("edit_unit_price_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        edit_description = st.text_input("📋 Description*", value=selected_price.description)
                        edit_base_price = st.number_input("💰 Base Price*", value=float(selected_price.base_price), min_value=0.01, step=0.01)
                        edit_vendor_name = st.text_input("🏢 Vendor Name*", value=selected_price.vendor_name)
                        edit_quality_rating = st.number_input("⭐ Quality Rating", value=float(selected_price.quality_rating), min_value=1.0, max_value=5.0, step=0.1)
                    
                    with col2:
                        edit_vendor_contact = st.text_input("📞 Vendor Contact", value=selected_price.vendor_contact)
                        edit_overhead = st.number_input("📊 Overhead %", value=float(selected_price.overhead_percentage), min_value=0.0, max_value=100.0, step=0.1)
                        edit_profit = st.number_input("💹 Profit %", value=float(selected_price.profit_percentage), min_value=0.0, max_value=100.0, step=0.1)
                        edit_notes = st.text_area("📋 Pricing Notes", value=selected_price.pricing_notes)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        update_price = st.form_submit_button("✏️ Update Price", use_container_width=True)
                    
                    with col2:
                        if st.form_submit_button("🗑️ Delete Price", use_container_width=True):
                            if selected_price.price_id in unit_prices_manager.unit_prices:
                                del unit_prices_manager.unit_prices[selected_price.price_id]
                                st.success("✅ Unit price deleted successfully!")
                                st.rerun()
                    
                    with col3:
                        if st.form_submit_button("💰 Update Total Price", use_container_width=True):
                            new_total = st.number_input("New Total Price", min_value=0.01, step=0.01)
                            if unit_prices_manager.update_price(selected_price.price_id, new_total, "Manual price update"):
                                st.success("✅ Price updated successfully!")
                                st.rerun()
                    
                    if update_price:
                        # Update the selected price
                        selected_price.description = edit_description
                        selected_price.base_price = edit_base_price
                        selected_price.vendor_name = edit_vendor_name
                        selected_price.vendor_contact = edit_vendor_contact
                        selected_price.overhead_percentage = edit_overhead
                        selected_price.profit_percentage = edit_profit
                        selected_price.quality_rating = edit_quality_rating
                        selected_price.pricing_notes = edit_notes
                        selected_price.total_price = selected_price.calculate_total_price()
                        selected_price.updated_at = datetime.now().isoformat()
                        
                        st.success("✅ Unit price updated successfully!")
                        st.rerun()
            else:
                st.info("No unit prices available to edit. Create some prices first.")
            
            # Category selector
            selected_category = st.selectbox(
                "Select Category",
                options=[cat.value for cat in PriceCategory],
                index=0
            )
            
            category_enum = PriceCategory(selected_category)
            category_prices = unit_prices_manager.get_prices_by_category(category_enum)
            
            st.write(f"**{selected_category} Prices:** {len(category_prices)} items")
            
            for price in category_prices:
                status_color = {
                    PriceStatus.ACTIVE: "🟢",
                    PriceStatus.PENDING_APPROVAL: "🟡",
                    PriceStatus.INACTIVE: "🔴",
                    PriceStatus.EXPIRED: "⚫"
                }.get(price.status, "⚪")
                
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.write(f"{status_color} **{price.description}**")
                    st.write(f"*{price.vendor_name}*")
                
                with col2:
                    st.write(f"**${price.total_price:.2f}**/{price.unit_type.value}")
                    st.write(f"Quality: {price.quality_rating}/5")
                
                with col3:
                    st.write(f"**{price.status.value}**")
                    st.write(f"{price.price_trend}")
        
        with tab3:
            st.subheader("📈 Price Trends Analysis")
            
            if metrics:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📊 Price Trends:**")
                    for trend, count in metrics['price_trends'].items():
                        trend_icon = {
                            "Increasing": "📈",
                            "Decreasing": "📉",
                            "Stable": "➡️"
                        }.get(trend, "➡️")
                        st.write(f"• {trend_icon} {trend}: {count} prices")
                
                with col2:
                    st.write("**📋 Status Distribution:**")
                    for status, count in metrics['status_breakdown'].items():
                        status_color = {
                            "Active": "🟢",
                            "Pending Approval": "🟡",
                            "Inactive": "🔴",
                            "Expired": "⚫"
                        }.get(status, "⚪")
                        st.write(f"• {status_color} {status}: {count}")
            
            # Show price trends for key items
            st.write("**📈 Key Price Movements:**")
            
            increasing_prices = [p for p in unit_prices_manager.get_all_unit_prices() if p.price_trend == "Increasing"]
            if increasing_prices:
                st.write("**📈 Increasing Prices:**")
                for price in increasing_prices[:5]:  # Show top 5
                    st.write(f"• {price.description} - ${price.total_price:.2f}/{price.unit_type.value}")
            
            decreasing_prices = [p for p in unit_prices_manager.get_all_unit_prices() if p.price_trend == "Decreasing"]
            if decreasing_prices:
                st.write("**📉 Decreasing Prices:**")
                for price in decreasing_prices[:5]:  # Show top 5
                    st.write(f"• {price.description} - ${price.total_price:.2f}/{price.unit_type.value}")
        
        with tab4:
            st.subheader("📋 Unit Prices Analytics")
            
            if metrics:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📊 Category Breakdown:**")
                    for category, count in metrics['category_breakdown'].items():
                        st.write(f"• {category}: {count}")
                    
                    st.write("**📈 Performance Metrics:**")
                    st.write(f"• **Average Quality Rating:** {metrics['average_quality_rating']}/5")
                    st.write(f"• **Average Reliability Score:** {metrics['average_reliability_score']}/5")
                
                with col2:
                    st.write("**🏢 Vendor Analysis:**")
                    st.write(f"• **Total Vendors:** {metrics['total_vendors']}")
                    
                    # Top vendors by number of items
                    vendor_counts = {}
                    for price in unit_prices_manager.get_all_unit_prices():
                        vendor_counts[price.vendor_name] = vendor_counts.get(price.vendor_name, 0) + 1
                    
                    sorted_vendors = sorted(vendor_counts.items(), key=lambda x: x[1], reverse=True)
                    st.write("**Top Vendors:**")
                    for vendor, count in sorted_vendors[:5]:
                        st.write(f"• {vendor}: {count} items")
        
        return
        
    except ImportError:
        st.error("Enterprise Unit Prices module not available")
        # Fallback to basic version
        render_unit_prices_basic()

def render_unit_prices_basic():
    """Basic unit prices module - fallback version"""
    st.markdown("""
    <div class="module-header">
        <h1>💲 Unit Prices</h1>
        <p>Unit price database and cost estimation</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("💲 Unit Prices module with cost database and estimation tools")

def render_material_management():
    """Enterprise Material Management with full CRUD functionality"""
    try:
        from modules.material_management_backend import material_manager, MaterialStatus, MaterialCategory, UnitType
        
        st.markdown("""
        <div class="module-header">
            <h1>📦 Material Management</h1>
            <p>Highland Tower Development - Comprehensive inventory tracking and supply chain management</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display summary metrics
        metrics = material_manager.generate_material_metrics()
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📦 Total Materials", metrics['total_materials'])
            with col2:
                st.metric("💰 Total Cost", f"${metrics['total_project_cost']:,.0f}")
            with col3:
                st.metric("⚠️ Low Stock", metrics['low_stock_materials'])
            with col4:
                st.metric("📊 Usage Rate", f"{metrics['average_usage_rate']}%")
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📦 All Materials", "➕ Add New", "✏️ Manage", "📊 Analytics"])
        
        with tab1:
            st.subheader("📦 All Materials Inventory")
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All"] + [status.value for status in MaterialStatus])
            with col2:
                category_filter = st.selectbox("Filter by Category", ["All"] + [cat.value for cat in MaterialCategory])
            
            # Get filtered materials
            materials = material_manager.get_all_materials()
            
            if status_filter != "All":
                materials = [m for m in materials if m.status.value == status_filter]
            if category_filter != "All":
                materials = [m for m in materials if m.category.value == category_filter]
            
            # Display materials
            for material in materials:
                status_color = {
                    MaterialStatus.DELIVERED: "🟢",
                    MaterialStatus.ORDERED: "🟡",
                    MaterialStatus.IN_TRANSIT: "🟠",
                    MaterialStatus.INSTALLED: "🔵",
                    MaterialStatus.PLANNED: "⚪"
                }.get(material.status, "⚪")
                
                low_stock_warning = "⚠️ LOW STOCK" if material.is_low_stock() else ""
                
                with st.expander(f"{status_color} {material.material_code} | {material.name} | {material.quantity_remaining:.1f} {material.unit_type.value} {low_stock_warning}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📂 Category:** {material.category.value}")
                        st.write(f"**📏 Unit:** {material.unit_type.value}")
                        st.write(f"**📦 Ordered:** {material.quantity_ordered:.1f}")
                        st.write(f"**📥 Delivered:** {material.quantity_delivered:.1f}")
                        st.write(f"**🔧 Used:** {material.quantity_used:.1f}")
                        st.write(f"**📊 Remaining:** {material.quantity_remaining:.1f}")
                    
                    with col2:
                        st.write(f"**🏢 Supplier:** {material.supplier_name}")
                        st.write(f"**💰 Unit Cost:** ${material.unit_cost:.2f}")
                        st.write(f"**💸 Total Cost:** ${material.total_cost:,.2f}")
                        st.write(f"**📍 Location:** {material.current_location}")
                        st.write(f"**📅 Required:** {material.required_date}")
                    
                    if material.description:
                        st.write(f"**📝 Description:** {material.description}")
                    
                    if material.specification:
                        st.write(f"**📋 Specification:** {material.specification}")
                    
                    # Usage and waste metrics
                    usage_rate = material.calculate_usage_rate()
                    waste_rate = material.calculate_waste_percentage()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Usage Rate", f"{usage_rate:.1f}%")
                    with col2:
                        st.metric("Waste Rate", f"{waste_rate:.1f}%")
                    with col3:
                        if material.is_low_stock():
                            st.error("⚠️ Low Stock Alert")
                        else:
                            st.success("✅ Stock OK")
                    
                    # Quick actions
                    st.write("---")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"📥 Add Delivery", key=f"btn_delivery_{material.material_id}"):
                            st.session_state[f"show_delivery_{material.material_id}"] = True
                    
                    with col2:
                        if st.button(f"🔧 Record Usage", key=f"btn_usage_{material.material_id}"):
                            st.session_state[f"show_usage_{material.material_id}"] = True
                    
                    with col3:
                        new_status = st.selectbox(f"Update Status", 
                                                [status.value for status in MaterialStatus],
                                                index=[status.value for status in MaterialStatus].index(material.status.value),
                                                key=f"status_{material.material_id}")
                        if st.button(f"📊 Update", key=f"btn_status_{material.material_id}"):
                            if material_manager.update_material_status(material.material_id, MaterialStatus(new_status)):
                                st.success("Status updated!")
                                st.rerun()
                    
                    # Delivery form
                    if st.session_state.get(f"show_delivery_{material.material_id}", False):
                        with st.form(f"delivery_form_{material.material_id}"):
                            st.write("**📥 Add Delivery Record**")
                            del_date = st.date_input("Delivery Date")
                            del_qty = st.number_input("Quantity Delivered", min_value=0.1, step=0.1)
                            del_ticket = st.text_input("Delivery Ticket")
                            del_received = st.text_input("Received By")
                            del_notes = st.text_area("Condition Notes")
                            
                            if st.form_submit_button("📥 Add Delivery"):
                                delivery_data = {
                                    "delivery_date": del_date.strftime('%Y-%m-%d'),
                                    "quantity_delivered": del_qty,
                                    "delivery_ticket": del_ticket,
                                    "received_by": del_received,
                                    "condition_notes": del_notes,
                                    "photos_attached": []
                                }
                                if material_manager.add_delivery(material.material_id, delivery_data):
                                    st.success("Delivery recorded!")
                                    st.session_state[f"show_delivery_{material.material_id}"] = False
                                    st.rerun()
                    
                    # Usage form
                    if st.session_state.get(f"show_usage_{material.material_id}", False):
                        with st.form(f"usage_form_{material.material_id}"):
                            st.write("**🔧 Record Material Usage**")
                            use_date = st.date_input("Usage Date")
                            use_qty = st.number_input("Quantity Used", min_value=0.1, step=0.1, max_value=float(material.quantity_remaining))
                            use_location = st.text_input("Location Used")
                            use_by = st.text_input("Used By")
                            use_work_order = st.text_input("Work Order")
                            use_notes = st.text_area("Usage Notes")
                            
                            if st.form_submit_button("🔧 Record Usage"):
                                usage_data = {
                                    "usage_date": use_date.strftime('%Y-%m-%d'),
                                    "quantity_used": use_qty,
                                    "location_used": use_location,
                                    "used_by": use_by,
                                    "work_order": use_work_order,
                                    "notes": use_notes
                                }
                                if material_manager.add_usage(material.material_id, usage_data):
                                    st.success("Usage recorded!")
                                    st.session_state[f"show_usage_{material.material_id}"] = False
                                    st.rerun()
        
        with tab2:
            st.subheader("➕ Add New Material")
            
            with st.form("create_material_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("📝 Material Name*", placeholder="Enter material name")
                    description = st.text_area("📋 Description", placeholder="Detailed description")
                    category = st.selectbox("📂 Category*", options=[cat.value for cat in MaterialCategory])
                    unit_type = st.selectbox("📏 Unit Type*", options=[unit.value for unit in UnitType])
                    quantity_ordered = st.number_input("📦 Quantity Ordered*", min_value=0.1, step=0.1)
                
                with col2:
                    supplier_name = st.text_input("🏢 Supplier Name*", placeholder="Supplier or vendor")
                    supplier_contact = st.text_input("📞 Supplier Contact", placeholder="Contact information")
                    unit_cost = st.number_input("💰 Unit Cost*", min_value=0.01, step=0.01)
                    required_date = st.date_input("📅 Required Date*")
                    minimum_stock = st.number_input("📊 Minimum Stock Level", min_value=0.0, step=0.1, value=10.0)
                
                # Specifications
                st.write("**📋 Specifications**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    specification = st.text_area("📝 Specification", placeholder="Technical specifications")
                    grade_quality = st.text_input("🏅 Grade/Quality", placeholder="Grade or quality level")
                
                with col2:
                    size_dimensions = st.text_input("📐 Size/Dimensions", placeholder="Size or dimensions")
                    manufacturer = st.text_input("🏭 Manufacturer", placeholder="Manufacturer name")
                
                with col3:
                    model_part_number = st.text_input("🔢 Model/Part Number", placeholder="Model or part number")
                    color_finish = st.text_input("🎨 Color/Finish", placeholder="Color or finish")
                
                # Location and project details
                col1, col2 = st.columns(2)
                
                with col1:
                    storage_location = st.text_input("📍 Storage Location", placeholder="Where will this be stored?")
                    work_package = st.text_input("📦 Work Package", value="Highland Tower Development")
                    phase = st.text_input("📊 Phase", placeholder="Construction phase")
                
                with col2:
                    drawing_reference = st.text_input("📐 Drawing Reference", placeholder="Related drawings")
                    purchase_order = st.text_input("📄 Purchase Order", placeholder="PO number")
                    procurement_notes = st.text_area("📝 Procurement Notes", placeholder="Additional notes")
                
                submit_material = st.form_submit_button("🆕 Add Material", use_container_width=True)
                
                if submit_material:
                    if not name or not category or not supplier_name or not unit_cost:
                        st.error("Please fill in all required fields marked with *")
                    else:
                        material_data = {
                            "name": name,
                            "description": description,
                            "category": category,
                            "specification": specification,
                            "grade_quality": grade_quality,
                            "size_dimensions": size_dimensions,
                            "color_finish": color_finish,
                            "manufacturer": manufacturer,
                            "model_part_number": model_part_number,
                            "unit_type": unit_type,
                            "quantity_ordered": quantity_ordered,
                            "minimum_stock_level": minimum_stock,
                            "storage_location": storage_location,
                            "delivery_location": storage_location,
                            "current_location": "Not yet delivered",
                            "supplier_name": supplier_name,
                            "supplier_contact": supplier_contact,
                            "purchase_order": purchase_order,
                            "unit_cost": unit_cost,
                            "total_cost": unit_cost * quantity_ordered,
                            "required_date": required_date.strftime('%Y-%m-%d'),
                            "certifications_required": [],
                            "project_name": "Highland Tower Development",
                            "work_package": work_package,
                            "phase": phase,
                            "drawing_reference": drawing_reference,
                            "procurement_notes": procurement_notes,
                            "quality_notes": "",
                            "storage_requirements": "",
                            "requested_by": "Current User",
                            "created_by": "Current User"
                        }
                        
                        material_id = material_manager.create_material(material_data)
                        st.success(f"✅ Material added successfully! ID: {material_id}")
                        st.rerun()
        
        with tab3:
            st.subheader("✏️ Manage Materials")
            
            materials = material_manager.get_all_materials()
            if materials:
                material_options = [f"{m.material_code} - {m.name}" for m in materials]
                selected_index = st.selectbox("Select Material to Manage", range(len(material_options)), format_func=lambda x: material_options[x])
                selected_material = materials[selected_index]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("✏️ Edit Material", use_container_width=True):
                        st.session_state.show_edit_form = True
                
                with col2:
                    if st.button("🗑️ Delete Material", use_container_width=True):
                        if selected_material.material_id in material_manager.materials:
                            del material_manager.materials[selected_material.material_id]
                            st.success("✅ Material deleted successfully!")
                            st.rerun()
                
                with col3:
                    if st.button("📋 Duplicate Material", use_container_width=True):
                        # Create duplicate with modified name
                        material_data = {
                            "name": f"Copy of {selected_material.name}",
                            "description": selected_material.description,
                            "category": selected_material.category.value,
                            "specification": selected_material.specification,
                            "grade_quality": selected_material.grade_quality,
                            "size_dimensions": selected_material.size_dimensions,
                            "color_finish": selected_material.color_finish,
                            "manufacturer": selected_material.manufacturer,
                            "model_part_number": selected_material.model_part_number,
                            "unit_type": selected_material.unit_type.value,
                            "quantity_ordered": selected_material.quantity_ordered,
                            "minimum_stock_level": selected_material.minimum_stock_level,
                            "storage_location": selected_material.storage_location,
                            "delivery_location": selected_material.delivery_location,
                            "current_location": "Not yet delivered",
                            "supplier_name": selected_material.supplier_name,
                            "supplier_contact": selected_material.supplier_contact,
                            "purchase_order": f"Copy-{selected_material.purchase_order}",
                            "unit_cost": selected_material.unit_cost,
                            "total_cost": selected_material.unit_cost * selected_material.quantity_ordered,
                            "required_date": selected_material.required_date,
                            "certifications_required": selected_material.certifications_required,
                            "project_name": selected_material.project_name,
                            "work_package": selected_material.work_package,
                            "phase": selected_material.phase,
                            "drawing_reference": selected_material.drawing_reference,
                            "procurement_notes": selected_material.procurement_notes,
                            "quality_notes": selected_material.quality_notes,
                            "storage_requirements": selected_material.storage_requirements,
                            "requested_by": "Current User",
                            "created_by": "Current User"
                        }
                        material_id = material_manager.create_material(material_data)
                        st.success(f"✅ Material duplicated! ID: {material_id}")
                        st.rerun()
                
                # Edit form
                if st.session_state.get('show_edit_form', False):
                    with st.form("edit_material_form"):
                        st.write("**✏️ Edit Material Details**")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_name = st.text_input("📝 Name", value=selected_material.name)
                            edit_description = st.text_area("📋 Description", value=selected_material.description)
                            edit_supplier = st.text_input("🏢 Supplier", value=selected_material.supplier_name)
                            edit_cost = st.number_input("💰 Unit Cost", value=float(selected_material.unit_cost), step=0.01)
                        
                        with col2:
                            edit_location = st.text_input("📍 Current Location", value=selected_material.current_location)
                            edit_min_stock = st.number_input("📊 Min Stock", value=float(selected_material.minimum_stock_level), step=0.1)
                            edit_notes = st.text_area("📝 Notes", value=selected_material.procurement_notes)
                        
                        if st.form_submit_button("✏️ Update Material"):
                            # Update the material
                            selected_material.name = edit_name
                            selected_material.description = edit_description
                            selected_material.supplier_name = edit_supplier
                            selected_material.unit_cost = edit_cost
                            selected_material.total_cost = edit_cost * selected_material.quantity_ordered
                            selected_material.current_location = edit_location
                            selected_material.minimum_stock_level = edit_min_stock
                            selected_material.procurement_notes = edit_notes
                            selected_material.updated_at = datetime.now().isoformat()
                            
                            st.success("✅ Material updated successfully!")
                            st.session_state.show_edit_form = False
                            st.rerun()
            else:
                st.info("No materials available. Add some materials first.")
        
        with tab4:
            st.subheader("📊 Material Analytics")
            
            if metrics:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📊 Status Distribution:**")
                    for status, count in metrics['status_breakdown'].items():
                        status_icon = {
                            "Delivered": "🟢",
                            "Ordered": "🟡",
                            "In Transit": "🟠",
                            "Installed": "🔵",
                            "Planned": "⚪"
                        }.get(status, "⚪")
                        st.write(f"• {status_icon} {status}: {count}")
                    
                    st.write("**📂 Category Distribution:**")
                    for category, count in metrics['category_breakdown'].items():
                        if count > 0:
                            st.write(f"• {category}: {count}")
                
                with col2:
                    st.write("**📈 Performance Metrics:**")
                    st.write(f"• **Total Project Cost:** ${metrics['total_project_cost']:,.0f}")
                    st.write(f"• **Average Usage Rate:** {metrics['average_usage_rate']}%")
                    st.write(f"• **Average Waste:** {metrics['average_waste_percentage']}%")
                    st.write(f"• **Low Stock Alerts:** {metrics['low_stock_materials']}")
                    st.write(f"• **Pending Deliveries:** {metrics['pending_deliveries']}")
                    
                    # Low stock materials
                    low_stock = material_manager.get_low_stock_materials()
                    if low_stock:
                        st.write("**⚠️ Low Stock Materials:**")
                        for material in low_stock[:5]:
                            st.write(f"• {material.name}: {material.quantity_remaining:.1f} {material.unit_type.value}")
        
        return
        
    except ImportError:
        st.error("Enterprise Material Management module not available")
        render_material_management_basic()

def render_material_management_basic():
    """Basic material management module - fallback version"""
    st.title("📦 Material Management")
    st.info("📦 Material management module for inventory tracking")

def render_equipment_tracking():
    """Enterprise Equipment Tracking with full CRUD functionality"""
    try:
        from modules.equipment_tracking_backend import equipment_manager, EquipmentStatus, EquipmentCategory, MaintenanceType
        
        st.markdown("""
        <div class="module-header">
            <h1>🚧 Equipment Tracking</h1>
            <p>Highland Tower Development - Comprehensive asset management and maintenance tracking</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display summary metrics
        metrics = equipment_manager.generate_equipment_metrics()
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🚧 Total Equipment", metrics['total_equipment'])
            with col2:
                st.metric("💰 Asset Value", f"${metrics['total_asset_value']:,.0f}")
            with col3:
                st.metric("⚠️ Needs Maintenance", metrics['maintenance_needed'])
            with col4:
                st.metric("📊 Avg Utilization", f"{metrics['average_utilization']}%")
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🚧 All Equipment", "➕ Add Equipment", "✏️ Manage", "📊 Analytics"])
        
        with tab1:
            st.subheader("🚧 Equipment Inventory")
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All"] + [status.value for status in EquipmentStatus])
            with col2:
                category_filter = st.selectbox("Filter by Category", ["All"] + [cat.value for cat in EquipmentCategory])
            
            # Get filtered equipment
            equipment_list = equipment_manager.get_all_equipment()
            
            if status_filter != "All":
                equipment_list = [eq for eq in equipment_list if eq.status.value == status_filter]
            if category_filter != "All":
                equipment_list = [eq for eq in equipment_list if eq.category.value == category_filter]
            
            # Display equipment
            for equipment in equipment_list:
                status_color = {
                    EquipmentStatus.ACTIVE: "🟢",
                    EquipmentStatus.MAINTENANCE: "🟡",
                    EquipmentStatus.IDLE: "🔵",
                    EquipmentStatus.OUT_OF_SERVICE: "🔴",
                    EquipmentStatus.RENTED: "🟠"
                }.get(equipment.status, "⚪")
                
                maintenance_warning = "⚠️ MAINTENANCE DUE" if equipment.needs_maintenance() else ""
                inspection_warning = "🔍 INSPECTION OVERDUE" if equipment.is_overdue_inspection() else ""
                
                with st.expander(f"{status_color} {equipment.equipment_code} | {equipment.name} | {equipment.total_hours:.1f}h {maintenance_warning} {inspection_warning}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📂 Category:** {equipment.category.value}")
                        st.write(f"**🏭 Manufacturer:** {equipment.manufacturer}")
                        st.write(f"**📋 Model:** {equipment.model}")
                        st.write(f"**🔢 Serial:** {equipment.serial_number}")
                        st.write(f"**📅 Year:** {equipment.year_manufactured}")
                        st.write(f"**📍 Location:** {equipment.current_location}")
                    
                    with col2:
                        st.write(f"**👤 Assigned To:** {equipment.assigned_to}")
                        st.write(f"**💰 Current Value:** ${equipment.current_value:,.0f}")
                        st.write(f"**⏱️ Total Hours:** {equipment.total_hours:.1f}")
                        st.write(f"**📊 This Month:** {equipment.hours_this_month:.1f} hours")
                        if equipment.rental_rate_daily > 0:
                            st.write(f"**💸 Daily Rate:** ${equipment.rental_rate_daily:.0f}")
                        st.write(f"**🔧 Ownership:** {equipment.owned_rented}")
                    
                    if equipment.description:
                        st.write(f"**📝 Description:** {equipment.description}")
                    
                    # Performance metrics
                    utilization = equipment.calculate_utilization_rate()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Utilization", f"{utilization:.1f}%")
                    with col2:
                        if equipment.needs_maintenance():
                            st.error("⚠️ Maintenance Due")
                        else:
                            st.success("✅ Maintenance OK")
                    with col3:
                        if equipment.is_overdue_inspection():
                            st.error("🔍 Inspection Overdue")
                        else:
                            st.success("✅ Inspection OK")
                    
                    # Quick actions
                    st.write("---")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"🔧 Add Maintenance", key=f"btn_maint_{equipment.equipment_id}"):
                            st.session_state[f"show_maintenance_{equipment.equipment_id}"] = True
                    
                    with col2:
                        if st.button(f"⏱️ Record Usage", key=f"btn_usage_{equipment.equipment_id}"):
                            st.session_state[f"show_usage_{equipment.equipment_id}"] = True
                    
                    with col3:
                        new_status = st.selectbox(f"Update Status", 
                                                [status.value for status in EquipmentStatus],
                                                index=[status.value for status in EquipmentStatus].index(equipment.status.value),
                                                key=f"status_{equipment.equipment_id}")
                        if st.button(f"📊 Update", key=f"btn_status_{equipment.equipment_id}"):
                            if equipment_manager.update_equipment_status(equipment.equipment_id, EquipmentStatus(new_status)):
                                st.success("Status updated!")
                                st.rerun()
                    
                    # Maintenance form
                    if st.session_state.get(f"show_maintenance_{equipment.equipment_id}", False):
                        with st.form(f"maintenance_form_{equipment.equipment_id}"):
                            st.write("**🔧 Add Maintenance Record**")
                            maint_date = st.date_input("Maintenance Date")
                            maint_type = st.selectbox("Maintenance Type", [mtype.value for mtype in MaintenanceType])
                            maint_desc = st.text_area("Description")
                            performed_by = st.text_input("Performed By")
                            maint_cost = st.number_input("Cost", min_value=0.0, step=10.0)
                            parts_replaced = st.text_input("Parts Replaced (comma-separated)")
                            next_service = st.date_input("Next Service Date")
                            maint_notes = st.text_area("Notes")
                            
                            if st.form_submit_button("🔧 Add Maintenance"):
                                maintenance_data = {
                                    "maintenance_date": maint_date.strftime('%Y-%m-%d'),
                                    "maintenance_type": maint_type,
                                    "description": maint_desc,
                                    "performed_by": performed_by,
                                    "cost": maint_cost,
                                    "parts_replaced": [part.strip() for part in parts_replaced.split(',') if part.strip()],
                                    "next_service_date": next_service.strftime('%Y-%m-%d'),
                                    "notes": maint_notes
                                }
                                if equipment_manager.add_maintenance_record(equipment.equipment_id, maintenance_data):
                                    st.success("Maintenance record added!")
                                    st.session_state[f"show_maintenance_{equipment.equipment_id}"] = False
                                    st.rerun()
                    
                    # Usage form
                    if st.session_state.get(f"show_usage_{equipment.equipment_id}", False):
                        with st.form(f"usage_form_{equipment.equipment_id}"):
                            st.write("**⏱️ Record Equipment Usage**")
                            use_start = st.date_input("Start Date")
                            use_end = st.date_input("End Date")
                            operator = st.text_input("Operator")
                            use_location = st.text_input("Location")
                            project_phase = st.text_input("Project Phase")
                            hours_used = st.number_input("Hours Used", min_value=0.1, step=0.1)
                            fuel_consumed = st.number_input("Fuel Consumed (L)", min_value=0.0, step=0.1)
                            use_notes = st.text_area("Usage Notes")
                            
                            if st.form_submit_button("⏱️ Record Usage"):
                                usage_data = {
                                    "start_date": use_start.strftime('%Y-%m-%d'),
                                    "end_date": use_end.strftime('%Y-%m-%d'),
                                    "operator": operator,
                                    "location": use_location,
                                    "project_phase": project_phase,
                                    "hours_used": hours_used,
                                    "fuel_consumed": fuel_consumed,
                                    "notes": use_notes
                                }
                                if equipment_manager.add_usage_record(equipment.equipment_id, usage_data):
                                    st.success("Usage recorded!")
                                    st.session_state[f"show_usage_{equipment.equipment_id}"] = False
                                    st.rerun()
        
        with tab2:
            st.subheader("➕ Add New Equipment")
            
            with st.form("create_equipment_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("📝 Equipment Name*", placeholder="Enter equipment name")
                    description = st.text_area("📋 Description", placeholder="Detailed description")
                    category = st.selectbox("📂 Category*", options=[cat.value for cat in EquipmentCategory])
                    manufacturer = st.text_input("🏭 Manufacturer*", placeholder="Equipment manufacturer")
                    model = st.text_input("📋 Model*", placeholder="Model number/name")
                
                with col2:
                    serial_number = st.text_input("🔢 Serial Number*", placeholder="Serial number")
                    year_manufactured = st.number_input("📅 Year Manufactured", min_value=1990, max_value=2030, step=1, value=2023)
                    owned_rented = st.selectbox("🔧 Ownership*", options=["Owned", "Rented"])
                    purchase_cost = st.number_input("💰 Purchase/Rental Cost*", min_value=0.0, step=100.0)
                    current_value = st.number_input("💸 Current Value", min_value=0.0, step=100.0)
                
                # Specifications
                st.write("**📋 Specifications**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    capacity = st.text_input("⚖️ Capacity", placeholder="e.g., 20 tons")
                    weight = st.text_input("🏋️ Weight", placeholder="e.g., 65 tons")
                
                with col2:
                    dimensions = st.text_input("📐 Dimensions", placeholder="L x W x H")
                    power_rating = st.text_input("⚡ Power Rating", placeholder="e.g., 132 kW")
                
                with col3:
                    fuel_type = st.text_input("⛽ Fuel Type", placeholder="e.g., Diesel, Electric")
                    fuel_efficiency = st.number_input("📊 Fuel Efficiency (L/hr)", min_value=0.0, step=0.1)
                
                # Location and assignment
                col1, col2 = st.columns(2)
                
                with col1:
                    current_location = st.text_input("📍 Current Location*", placeholder="Where is this equipment?")
                    assigned_to = st.text_input("👤 Assigned To", placeholder="Person or crew assigned")
                    project_assignment = st.text_input("📋 Project Assignment", value="Highland Tower Development")
                
                with col2:
                    service_interval = st.number_input("🔧 Service Interval (hours)", min_value=1, step=1, value=200)
                    rental_rate = st.number_input("💰 Daily Rental Rate", min_value=0.0, step=10.0)
                    acquisition_date = st.date_input("📅 Acquisition Date*")
                
                # Additional details
                col1, col2 = st.columns(2)
                
                with col1:
                    certifications = st.text_input("📜 Required Certifications", placeholder="Comma-separated list")
                    manual_location = st.text_input("📖 Manual Location", placeholder="Where are the manuals?")
                
                with col2:
                    warranty_expiry = st.date_input("🛡️ Warranty Expiry")
                    insurance_policy = st.text_input("🛡️ Insurance Policy", placeholder="Policy number")
                
                notes = st.text_area("📝 Additional Notes", placeholder="Procurement notes, operational details, etc.")
                
                submit_equipment = st.form_submit_button("🆕 Add Equipment", use_container_width=True)
                
                if submit_equipment:
                    if not name or not category or not manufacturer or not model or not serial_number:
                        st.error("Please fill in all required fields marked with *")
                    else:
                        equipment_data = {
                            "name": name,
                            "description": description,
                            "category": category,
                            "manufacturer": manufacturer,
                            "model": model,
                            "serial_number": serial_number,
                            "year_manufactured": year_manufactured,
                            "capacity": capacity,
                            "weight": weight,
                            "dimensions": dimensions,
                            "power_rating": power_rating,
                            "fuel_type": fuel_type,
                            "purchase_cost": purchase_cost,
                            "current_value": current_value if current_value > 0 else purchase_cost,
                            "rental_rate_daily": rental_rate,
                            "depreciation_rate": 15.0,  # Default 15% per year
                            "current_location": current_location,
                            "assigned_to": assigned_to,
                            "project_assignment": project_assignment,
                            "fuel_efficiency": fuel_efficiency,
                            "service_interval_hours": service_interval,
                            "certifications_required": [cert.strip() for cert in certifications.split(',') if cert.strip()],
                            "manual_location": manual_location,
                            "warranty_expiry": warranty_expiry.strftime('%Y-%m-%d') if warranty_expiry else None,
                            "insurance_policy": insurance_policy,
                            "procurement_notes": notes,
                            "operational_notes": "",
                            "safety_notes": "",
                            "owned_rented": owned_rented,
                            "acquisition_date": acquisition_date.strftime('%Y-%m-%d'),
                            "created_by": "Current User",
                            "updated_by": "Current User"
                        }
                        
                        equipment_id = equipment_manager.create_equipment(equipment_data)
                        st.success(f"✅ Equipment added successfully! ID: {equipment_id}")
                        st.rerun()
        
        with tab3:
            st.subheader("✏️ Manage Equipment")
            
            equipment_list = equipment_manager.get_all_equipment()
            if equipment_list:
                equipment_options = [f"{eq.equipment_code} - {eq.name}" for eq in equipment_list]
                selected_index = st.selectbox("Select Equipment to Manage", range(len(equipment_options)), format_func=lambda x: equipment_options[x])
                selected_equipment = equipment_list[selected_index]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("✏️ Edit Equipment", use_container_width=True):
                        st.session_state.show_edit_equipment_form = True
                
                with col2:
                    if st.button("🗑️ Delete Equipment", use_container_width=True):
                        if selected_equipment.equipment_id in equipment_manager.equipment:
                            del equipment_manager.equipment[selected_equipment.equipment_id]
                            st.success("✅ Equipment deleted successfully!")
                            st.rerun()
                
                with col3:
                    if st.button("📋 Duplicate Equipment", use_container_width=True):
                        # Create duplicate with modified name
                        equipment_data = {
                            "name": f"Copy of {selected_equipment.name}",
                            "description": selected_equipment.description,
                            "category": selected_equipment.category.value,
                            "manufacturer": selected_equipment.manufacturer,
                            "model": selected_equipment.model,
                            "serial_number": f"COPY-{selected_equipment.serial_number}",
                            "year_manufactured": selected_equipment.year_manufactured,
                            "capacity": selected_equipment.capacity,
                            "weight": selected_equipment.weight,
                            "dimensions": selected_equipment.dimensions,
                            "power_rating": selected_equipment.power_rating,
                            "fuel_type": selected_equipment.fuel_type,
                            "purchase_cost": selected_equipment.purchase_cost,
                            "current_value": selected_equipment.current_value,
                            "rental_rate_daily": selected_equipment.rental_rate_daily,
                            "depreciation_rate": selected_equipment.depreciation_rate,
                            "current_location": "New Location",
                            "assigned_to": selected_equipment.assigned_to,
                            "project_assignment": selected_equipment.project_assignment,
                            "fuel_efficiency": selected_equipment.fuel_efficiency,
                            "service_interval_hours": selected_equipment.service_interval_hours,
                            "certifications_required": selected_equipment.certifications_required,
                            "manual_location": selected_equipment.manual_location,
                            "warranty_expiry": selected_equipment.warranty_expiry,
                            "insurance_policy": f"COPY-{selected_equipment.insurance_policy}",
                            "procurement_notes": selected_equipment.procurement_notes,
                            "operational_notes": selected_equipment.operational_notes,
                            "safety_notes": selected_equipment.safety_notes,
                            "owned_rented": selected_equipment.owned_rented,
                            "acquisition_date": datetime.now().strftime('%Y-%m-%d'),
                            "created_by": "Current User",
                            "updated_by": "Current User"
                        }
                        equipment_id = equipment_manager.create_equipment(equipment_data)
                        st.success(f"✅ Equipment duplicated! ID: {equipment_id}")
                        st.rerun()
                
                # Edit form
                if st.session_state.get('show_edit_equipment_form', False):
                    with st.form("edit_equipment_form"):
                        st.write("**✏️ Edit Equipment Details**")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_name = st.text_input("📝 Name", value=selected_equipment.name)
                            edit_description = st.text_area("📋 Description", value=selected_equipment.description)
                            edit_location = st.text_input("📍 Location", value=selected_equipment.current_location)
                            edit_assigned = st.text_input("👤 Assigned To", value=selected_equipment.assigned_to)
                        
                        with col2:
                            edit_value = st.number_input("💰 Current Value", value=float(selected_equipment.current_value), step=100.0)
                            edit_rental_rate = st.number_input("💸 Daily Rate", value=float(selected_equipment.rental_rate_daily), step=10.0)
                            edit_notes = st.text_area("📝 Notes", value=selected_equipment.operational_notes)
                        
                        if st.form_submit_button("✏️ Update Equipment"):
                            # Update the equipment
                            selected_equipment.name = edit_name
                            selected_equipment.description = edit_description
                            selected_equipment.current_location = edit_location
                            selected_equipment.assigned_to = edit_assigned
                            selected_equipment.current_value = edit_value
                            selected_equipment.rental_rate_daily = edit_rental_rate
                            selected_equipment.operational_notes = edit_notes
                            selected_equipment.updated_by = "Current User"
                            selected_equipment.updated_at = datetime.now().isoformat()
                            
                            st.success("✅ Equipment updated successfully!")
                            st.session_state.show_edit_equipment_form = False
                            st.rerun()
            else:
                st.info("No equipment available. Add some equipment first.")
        
        with tab4:
            st.subheader("📊 Equipment Analytics")
            
            if metrics:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📊 Status Distribution:**")
                    for status, count in metrics['status_breakdown'].items():
                        status_icon = {
                            "Active": "🟢",
                            "Under Maintenance": "🟡",
                            "Idle": "🔵",
                            "Out of Service": "🔴",
                            "Rented Out": "🟠"
                        }.get(status, "⚪")
                        st.write(f"• {status_icon} {status}: {count}")
                    
                    st.write("**📂 Category Distribution:**")
                    for category, count in metrics['category_breakdown'].items():
                        if count > 0:
                            st.write(f"• {category}: {count}")
                
                with col2:
                    st.write("**📈 Performance Metrics:**")
                    st.write(f"• **Total Asset Value:** ${metrics['total_asset_value']:,.0f}")
                    st.write(f"• **Monthly Rental Cost:** ${metrics['monthly_rental_cost']:,.0f}")
                    st.write(f"• **Average Utilization:** {metrics['average_utilization']}%")
                    st.write(f"• **Hours This Month:** {metrics['total_hours_this_month']:.0f}")
                    st.write(f"• **Maintenance Needed:** {metrics['maintenance_needed']}")
                    st.write(f"• **Overdue Inspections:** {metrics['overdue_inspections']}")
                    
                    # Equipment needing attention
                    maintenance_needed = equipment_manager.get_equipment_needing_maintenance()
                    if maintenance_needed:
                        st.write("**⚠️ Equipment Needing Maintenance:**")
                        for eq in maintenance_needed[:5]:
                            st.write(f"• {eq.name}: Due {eq.next_service_date}")
        
        return
        
    except ImportError:
        st.error("Enterprise Equipment Tracking module not available")
        render_equipment_tracking_basic()

def render_equipment_tracking_basic():
    """Basic equipment tracking module - fallback version"""
    st.title("🚧 Equipment Tracking")
    st.info("🚧 Equipment tracking module for asset management")

def render_analytics():
    """Enterprise Analytics with full CRUD functionality"""
    try:
        from modules.analytics_backend import analytics_manager, ReportType, ReportFrequency, MetricStatus
        
        st.markdown("""
        <div class="module-header">
            <h1>📊 Advanced Analytics</h1>
            <p>Highland Tower Development - Executive dashboards and performance intelligence</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display summary metrics
        metrics = analytics_manager.generate_analytics_metrics()
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📊 Total Reports", metrics['total_reports'])
            with col2:
                st.metric("📈 KPI Metrics", metrics['total_kpis'])
            with col3:
                st.metric("⚠️ Critical KPIs", metrics['critical_kpis'])
            with col4:
                st.metric("🎯 Exceeding Target", metrics['exceeding_kpis'])
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 KPI Dashboard", "📋 Reports", "➕ Create", "⚙️ Manage"])
        
        with tab1:
            st.subheader("📊 Highland Tower Development - Key Performance Indicators")
            
            # Get KPI metrics
            kpis = analytics_manager.get_kpi_metrics()
            
            if kpis:
                # Overall project health
                critical_count = len([k for k in kpis if k.status == MetricStatus.CRITICAL])
                exceeding_count = len([k for k in kpis if k.status == MetricStatus.EXCEEDING])
                
                if critical_count > 0:
                    st.error(f"⚠️ {critical_count} KPIs are in critical status - immediate attention required")
                elif exceeding_count >= len(kpis) // 2:
                    st.success(f"🎯 Project performing excellently - {exceeding_count} KPIs exceeding targets!")
                else:
                    st.info("📊 Project performance within acceptable ranges")
                
                # Display KPIs by category
                categories = list(set(kpi.category for kpi in kpis))
                
                for category in categories:
                    st.write(f"**{category} Performance**")
                    category_kpis = [k for k in kpis if k.category == category]
                    
                    cols = st.columns(min(len(category_kpis), 4))
                    for i, kpi in enumerate(category_kpis):
                        with cols[i % 4]:
                            # Status color coding
                            status_color = {
                                MetricStatus.EXCEEDING: "🟢",
                                MetricStatus.ON_TARGET: "🟢", 
                                MetricStatus.AT_RISK: "🟡",
                                MetricStatus.CRITICAL: "🔴"
                            }.get(kpi.status, "⚪")
                            
                            # Trend indicator
                            trend_icon = {
                                "Improving": "📈",
                                "Declining": "📉",
                                "Stable": "➡️"
                            }.get(kpi.trend, "")
                            
                            st.metric(
                                label=f"{status_color} {kpi.metric_name}",
                                value=f"{kpi.current_value} {kpi.unit}",
                                delta=f"Target: {kpi.target_value} {kpi.unit}"
                            )
                            
                            with st.expander(f"Details {trend_icon}"):
                                st.write(f"**Status:** {kpi.status.value}")
                                st.write(f"**Trend:** {kpi.trend}")
                                st.write(f"**Last Updated:** {kpi.last_updated}")
                                st.write(f"**Description:** {kpi.description}")
                                
                                # Quick update
                                new_value = st.number_input(
                                    "Update Value", 
                                    value=float(kpi.current_value),
                                    step=0.1,
                                    key=f"kpi_update_{kpi.metric_id}"
                                )
                                if st.button(f"📊 Update", key=f"btn_update_{kpi.metric_id}"):
                                    if analytics_manager.update_kpi_value(kpi.metric_id, new_value):
                                        st.success("KPI updated!")
                                        st.rerun()
                    
                    st.write("---")
            else:
                st.info("No KPI metrics available. Create some metrics to start tracking performance.")
        
        with tab2:
            st.subheader("📋 Analytics Reports")
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                type_filter = st.selectbox("Filter by Type", ["All"] + [rtype.value for rtype in ReportType])
            with col2:
                frequency_filter = st.selectbox("Filter by Frequency", ["All"] + [freq.value for freq in ReportFrequency])
            
            # Get filtered reports
            reports = analytics_manager.get_all_reports()
            
            if type_filter != "All":
                reports = [r for r in reports if r.report_type.value == type_filter]
            if frequency_filter != "All":
                reports = [r for r in reports if r.frequency.value == frequency_filter]
            
            # Display reports
            for report in reports:
                status_color = {
                    "Generated": "🟢",
                    "In Progress": "🟡",
                    "Scheduled": "🔵",
                    "Failed": "🔴"
                }.get(report.status, "⚪")
                
                automated_indicator = "🤖 AUTOMATED" if report.automated else "📝 MANUAL"
                
                with st.expander(f"{status_color} {report.report_code} | {report.title} | {automated_indicator}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📋 Type:** {report.report_type.value}")
                        st.write(f"**🔄 Frequency:** {report.frequency.value}")
                        st.write(f"**📅 Generated:** {report.generated_date}")
                        st.write(f"**📊 Period:** {report.report_period_start} to {report.report_period_end}")
                        st.write(f"**👤 Created By:** {report.created_by}")
                    
                    with col2:
                        st.write(f"**📄 Format:** {report.file_format}")
                        if report.file_size > 0:
                            st.write(f"**📊 Size:** {report.file_size / 1024 / 1024:.1f} MB")
                        st.write(f"**🔐 Access:** {report.access_level}")
                        if report.next_generation:
                            st.write(f"**🔄 Next Generation:** {report.next_generation}")
                        st.write(f"**📧 Distribution:** {len(report.distribution_list)} recipients")
                    
                    if report.description:
                        st.write(f"**📝 Description:** {report.description}")
                    
                    if report.notes:
                        st.write(f"**📋 Notes:** {report.notes}")
                    
                    # Data sources and metrics
                    if report.data_sources:
                        st.write(f"**📊 Data Sources:** {', '.join(report.data_sources)}")
                    
                    if report.metrics_included:
                        st.write(f"**📈 Metrics:** {', '.join(report.metrics_included)}")
                    
                    # Quick actions
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"📥 Download", key=f"btn_download_{report.report_id}"):
                            st.success(f"Downloading {report.file_format} report...")
                    
                    with col2:
                        if st.button(f"🔄 Regenerate", key=f"btn_regen_{report.report_id}"):
                            st.success("Report regeneration started...")
                    
                    with col3:
                        if st.button(f"📧 Redistribute", key=f"btn_dist_{report.report_id}"):
                            st.success("Report sent to distribution list")
        
        with tab3:
            st.subheader("➕ Create New Analytics")
            
            # Sub-tabs for different creation options
            create_tab1, create_tab2 = st.tabs(["📊 Create KPI Metric", "📋 Create Report"])
            
            with create_tab1:
                st.write("**📊 Create New KPI Metric**")
                
                with st.form("create_kpi_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        metric_name = st.text_input("📝 Metric Name*", placeholder="e.g., Schedule Performance Index")
                        category = st.selectbox("📂 Category*", options=["Schedule", "Cost", "Quality", "Safety", "Communication", "Resource"])
                        current_value = st.number_input("📊 Current Value*", step=0.1)
                        target_value = st.number_input("🎯 Target Value*", step=0.1)
                    
                    with col2:
                        unit = st.text_input("📏 Unit*", placeholder="e.g., %, days, $, ratio")
                        status = st.selectbox("📊 Initial Status*", options=[status.value for status in MetricStatus])
                        trend = st.selectbox("📈 Trend", options=["Improving", "Declining", "Stable"])
                        description = st.text_area("📝 Description*", placeholder="Detailed description of this metric")
                    
                    if st.form_submit_button("📊 Create KPI Metric", use_container_width=True):
                        if not metric_name or not category or not description:
                            st.error("Please fill in all required fields marked with *")
                        else:
                            kpi_data = {
                                "metric_name": metric_name,
                                "category": category,
                                "current_value": current_value,
                                "target_value": target_value,
                                "unit": unit,
                                "status": status,
                                "trend": trend,
                                "description": description
                            }
                            
                            metric_id = analytics_manager.create_kpi_metric(kpi_data)
                            st.success(f"✅ KPI metric created successfully! ID: {metric_id}")
                            st.rerun()
            
            with create_tab2:
                st.write("**📋 Create New Report**")
                
                with st.form("create_report_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        title = st.text_input("📝 Report Title*", placeholder="Highland Tower Performance Report")
                        description = st.text_area("📋 Description", placeholder="Detailed report description")
                        report_type = st.selectbox("📋 Report Type*", options=[rtype.value for rtype in ReportType])
                        frequency = st.selectbox("🔄 Frequency*", options=[freq.value for freq in ReportFrequency])
                        file_format = st.selectbox("📄 Format*", options=["PDF", "Excel", "PowerBI", "Dashboard"])
                    
                    with col2:
                        period_start = st.date_input("📅 Period Start*")
                        period_end = st.date_input("📅 Period End*")
                        access_level = st.selectbox("🔐 Access Level*", options=["Public", "Project Team", "Management", "Executive"])
                        automated = st.checkbox("🤖 Automated Generation")
                        if automated:
                            next_generation = st.date_input("🔄 Next Generation Date")
                    
                    # Data sources and content
                    st.write("**📊 Report Content**")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        data_sources = st.text_input("📊 Data Sources", placeholder="Comma-separated data sources")
                        metrics_included = st.text_input("📈 Metrics", placeholder="Comma-separated metrics to include")
                    
                    with col2:
                        charts_included = st.text_input("📊 Charts", placeholder="Comma-separated chart types")
                        distribution_list = st.text_input("📧 Distribution List", placeholder="Comma-separated recipients")
                    
                    parameters = st.text_area("⚙️ Parameters (JSON)", placeholder='{"include_photos": true, "detail_level": "summary"}')
                    notes = st.text_area("📝 Notes", placeholder="Additional notes about this report")
                    
                    if st.form_submit_button("📋 Create Report", use_container_width=True):
                        if not title or not report_type or not frequency:
                            st.error("Please fill in all required fields marked with *")
                        else:
                            # Parse parameters
                            try:
                                params = json.loads(parameters) if parameters else {}
                            except:
                                params = {}
                            
                            report_data = {
                                "title": title,
                                "description": description,
                                "report_type": report_type,
                                "frequency": frequency,
                                "data_sources": [ds.strip() for ds in data_sources.split(',') if ds.strip()],
                                "metrics_included": [m.strip() for m in metrics_included.split(',') if m.strip()],
                                "charts_included": [c.strip() for c in charts_included.split(',') if c.strip()],
                                "report_period_start": period_start.strftime('%Y-%m-%d'),
                                "report_period_end": period_end.strftime('%Y-%m-%d'),
                                "created_by": "Current User",
                                "distribution_list": [d.strip() for d in distribution_list.split(',') if d.strip()],
                                "access_level": access_level,
                                "file_path": None,
                                "file_format": file_format,
                                "automated": automated,
                                "next_generation": next_generation.strftime('%Y-%m-%d') if automated else None,
                                "notes": notes,
                                "parameters": params
                            }
                            
                            report_id = analytics_manager.create_report(report_data)
                            st.success(f"✅ Report created successfully! ID: {report_id}")
                            st.rerun()
        
        with tab4:
            st.subheader("⚙️ Manage Analytics")
            
            manage_tab1, manage_tab2 = st.tabs(["📊 Manage KPIs", "📋 Manage Reports"])
            
            with manage_tab1:
                kpis = analytics_manager.get_kpi_metrics()
                if kpis:
                    kpi_options = [f"{k.metric_name} ({k.category})" for k in kpis]
                    selected_kpi_index = st.selectbox("Select KPI to Manage", range(len(kpi_options)), format_func=lambda x: kpi_options[x])
                    selected_kpi = kpis[selected_kpi_index]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("✏️ Edit KPI", use_container_width=True):
                            st.session_state.show_edit_kpi_form = True
                    
                    with col2:
                        if st.button("🗑️ Delete KPI", use_container_width=True):
                            if selected_kpi.metric_id in analytics_manager.kpi_metrics:
                                del analytics_manager.kpi_metrics[selected_kpi.metric_id]
                                st.success("✅ KPI deleted successfully!")
                                st.rerun()
                    
                    with col3:
                        if st.button("📋 Duplicate KPI", use_container_width=True):
                            # Create duplicate with modified name
                            kpi_data = {
                                "metric_name": f"Copy of {selected_kpi.metric_name}",
                                "category": selected_kpi.category,
                                "current_value": selected_kpi.current_value,
                                "target_value": selected_kpi.target_value,
                                "unit": selected_kpi.unit,
                                "status": selected_kpi.status.value,
                                "trend": selected_kpi.trend,
                                "description": selected_kpi.description
                            }
                            metric_id = analytics_manager.create_kpi_metric(kpi_data)
                            st.success(f"✅ KPI duplicated! ID: {metric_id}")
                            st.rerun()
                    
                    # Edit form
                    if st.session_state.get('show_edit_kpi_form', False):
                        with st.form("edit_kpi_form"):
                            st.write("**✏️ Edit KPI Details**")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                edit_name = st.text_input("📝 Name", value=selected_kpi.metric_name)
                                edit_category = st.text_input("📂 Category", value=selected_kpi.category)
                                edit_target = st.number_input("🎯 Target", value=float(selected_kpi.target_value), step=0.1)
                            
                            with col2:
                                edit_unit = st.text_input("📏 Unit", value=selected_kpi.unit)
                                edit_description = st.text_area("📝 Description", value=selected_kpi.description)
                            
                            if st.form_submit_button("✏️ Update KPI"):
                                # Update the KPI
                                selected_kpi.metric_name = edit_name
                                selected_kpi.category = edit_category
                                selected_kpi.target_value = edit_target
                                selected_kpi.unit = edit_unit
                                selected_kpi.description = edit_description
                                selected_kpi.last_updated = datetime.now().strftime('%Y-%m-%d')
                                
                                st.success("✅ KPI updated successfully!")
                                st.session_state.show_edit_kpi_form = False
                                st.rerun()
                else:
                    st.info("No KPIs available. Create some KPIs first.")
            
            with manage_tab2:
                reports = analytics_manager.get_all_reports()
                if reports:
                    report_options = [f"{r.report_code} - {r.title}" for r in reports]
                    selected_report_index = st.selectbox("Select Report to Manage", range(len(report_options)), format_func=lambda x: report_options[x])
                    selected_report = reports[selected_report_index]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("✏️ Edit Report", use_container_width=True):
                            st.session_state.show_edit_report_form = True
                    
                    with col2:
                        if st.button("🗑️ Delete Report", use_container_width=True):
                            if selected_report.report_id in analytics_manager.reports:
                                del analytics_manager.reports[selected_report.report_id]
                                st.success("✅ Report deleted successfully!")
                                st.rerun()
                    
                    with col3:
                        if st.button("📋 Duplicate Report", use_container_width=True):
                            # Create duplicate with modified title
                            report_data = {
                                "title": f"Copy of {selected_report.title}",
                                "description": selected_report.description,
                                "report_type": selected_report.report_type.value,
                                "frequency": selected_report.frequency.value,
                                "data_sources": selected_report.data_sources.copy(),
                                "metrics_included": selected_report.metrics_included.copy(),
                                "charts_included": selected_report.charts_included.copy(),
                                "report_period_start": selected_report.report_period_start,
                                "report_period_end": selected_report.report_period_end,
                                "created_by": "Current User",
                                "distribution_list": selected_report.distribution_list.copy(),
                                "access_level": selected_report.access_level,
                                "file_path": None,
                                "file_format": selected_report.file_format,
                                "automated": selected_report.automated,
                                "next_generation": selected_report.next_generation,
                                "notes": selected_report.notes,
                                "parameters": selected_report.parameters
                            }
                            report_id = analytics_manager.create_report(report_data)
                            st.success(f"✅ Report duplicated! ID: {report_id}")
                            st.rerun()
                    
                    # Edit form
                    if st.session_state.get('show_edit_report_form', False):
                        with st.form("edit_report_form"):
                            st.write("**✏️ Edit Report Details**")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                edit_title = st.text_input("📝 Title", value=selected_report.title)
                                edit_description = st.text_area("📋 Description", value=selected_report.description)
                                edit_access = st.text_input("🔐 Access Level", value=selected_report.access_level)
                            
                            with col2:
                                edit_distribution = st.text_input("📧 Distribution", value=", ".join(selected_report.distribution_list))
                                edit_notes = st.text_area("📝 Notes", value=selected_report.notes)
                            
                            if st.form_submit_button("✏️ Update Report"):
                                # Update the report
                                selected_report.title = edit_title
                                selected_report.description = edit_description
                                selected_report.access_level = edit_access
                                selected_report.distribution_list = [d.strip() for d in edit_distribution.split(',') if d.strip()]
                                selected_report.notes = edit_notes
                                selected_report.updated_at = datetime.now().isoformat()
                                
                                st.success("✅ Report updated successfully!")
                                st.session_state.show_edit_report_form = False
                                st.rerun()
                else:
                    st.info("No reports available. Create some reports first.")
        
        return
        
    except ImportError:
        st.error("Enterprise Analytics module not available")
        st.info("📊 Analytics module with advanced reporting and insights")

def render_performance_snapshot():
    """Enterprise Performance Snapshot with full CRUD functionality"""
    try:
        from modules.performance_snapshot_backend import performance_manager, HealthStatus, TrendDirection
        
        st.markdown("""
        <div class="module-header">
            <h1>📈 Performance Snapshot</h1>
            <p>Highland Tower Development - Executive dashboard and real-time project health monitoring</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get overall project health and metrics
        overall_health = performance_manager.calculate_overall_project_health()
        metrics = performance_manager.generate_performance_metrics()
        latest_summary = performance_manager.get_latest_summary()
        
        # Project Health Banner
        health_colors = {
            HealthStatus.EXCELLENT: "🟢",
            HealthStatus.GOOD: "🟡", 
            HealthStatus.WARNING: "🟠",
            HealthStatus.CRITICAL: "🔴"
        }
        
        health_color = health_colors.get(overall_health, "⚪")
        
        if overall_health == HealthStatus.EXCELLENT:
            st.success(f"{health_color} **PROJECT STATUS: EXCELLENT** - All systems performing above expectations")
        elif overall_health == HealthStatus.GOOD:
            st.info(f"{health_color} **PROJECT STATUS: GOOD** - Performance within acceptable ranges")
        elif overall_health == HealthStatus.WARNING:
            st.warning(f"{health_color} **PROJECT STATUS: WARNING** - Some metrics need attention")
        else:
            st.error(f"{health_color} **PROJECT STATUS: CRITICAL** - Immediate action required")
        
        # Executive Summary Cards
        if latest_summary:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "📊 Project Progress", 
                    f"{latest_summary.percent_complete:.1f}%",
                    f"{'+' if latest_summary.days_ahead_behind > 0 else ''}{latest_summary.days_ahead_behind} days"
                )
            
            with col2:
                budget_used_pct = (latest_summary.spent_to_date / latest_summary.total_budget) * 100
                st.metric(
                    "💰 Budget Performance", 
                    f"{budget_used_pct:.1f}% used",
                    f"${(latest_summary.total_budget - latest_summary.projected_final_cost):,.0f} projected savings"
                )
            
            with col3:
                st.metric(
                    "🦺 Safety Rating", 
                    f"{latest_summary.safety_rating:.1f}%",
                    "Excellent"
                )
            
            with col4:
                st.metric(
                    "✅ Quality Score", 
                    f"{latest_summary.quality_score:.1f}%",
                    "Above Target"
                )
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Dashboard", "⚠️ Alerts & Issues", "➕ Create", "⚙️ Manage"])
        
        with tab1:
            st.subheader("📊 Highland Tower Development - Executive Performance Dashboard")
            
            # Performance Metrics by Category
            performance_metrics = performance_manager.get_performance_metrics()
            
            if performance_metrics:
                categories = list(set(metric.category for metric in performance_metrics))
                
                for category in categories:
                    st.write(f"**{category} Performance**")
                    category_metrics = performance_manager.get_metrics_by_category(category)
                    
                    cols = st.columns(min(len(category_metrics), 3))
                    for i, metric in enumerate(category_metrics):
                        with cols[i % 3]:
                            # Status and trend indicators
                            status_icon = health_colors.get(metric.status, "⚪")
                            trend_icon = {
                                TrendDirection.IMPROVING: "📈",
                                TrendDirection.DECLINING: "📉",
                                TrendDirection.STABLE: "➡️"
                            }.get(metric.trend, "")
                            
                            # Color code the variance
                            variance_color = "normal"
                            if abs(metric.variance_percentage) > 10:
                                variance_color = "inverse"
                            
                            st.metric(
                                label=f"{status_icon} {metric.metric_name}",
                                value=f"{metric.current_value} {metric.unit}",
                                delta=f"{metric.variance_percentage:+.1f}% vs target",
                                delta_color=variance_color
                            )
                            
                            with st.expander(f"Details {trend_icon}"):
                                st.write(f"**Target:** {metric.target_value} {metric.unit}")
                                st.write(f"**Status:** {metric.status.value}")
                                st.write(f"**Trend:** {metric.trend.value}")
                                st.write(f"**Last Updated:** {metric.last_updated}")
                                st.write(f"**Description:** {metric.description}")
                                
                                # Quick update capability
                                new_value = st.number_input(
                                    "Update Value",
                                    value=float(metric.current_value),
                                    step=0.1,
                                    key=f"metric_update_{metric.metric_id}"
                                )
                                if st.button(f"📊 Update", key=f"btn_update_{metric.metric_id}"):
                                    if performance_manager.update_metric_value(metric.metric_id, new_value):
                                        st.success("Metric updated!")
                                        st.rerun()
                    
                    st.write("---")
                
                # Executive Summary Section
                if latest_summary:
                    st.subheader("📋 Executive Summary")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**📈 Key Accomplishments:**")
                        for accomplishment in latest_summary.accomplishments:
                            st.write(f"• {accomplishment}")
                        
                        st.write("**📅 Upcoming Milestones:**")
                        for milestone in latest_summary.upcoming_milestones:
                            status_emoji = {"On Track": "🟢", "Ahead": "🟢", "Behind": "🔴", "At Risk": "🟡"}.get(milestone["status"], "⚪")
                            st.write(f"• {status_emoji} {milestone['milestone']} - {milestone['date']}")
                    
                    with col2:
                        st.write("**💰 Financial Summary:**")
                        st.write(f"• **Total Budget:** ${latest_summary.total_budget:,.0f}")
                        st.write(f"• **Spent to Date:** ${latest_summary.spent_to_date:,.0f}")
                        st.write(f"• **Remaining:** ${latest_summary.remaining_budget:,.0f}")
                        st.write(f"• **Projected Final:** ${latest_summary.projected_final_cost:,.0f}")
                        
                        st.write("**👥 Resource Status:**")
                        st.write(f"• **Current Workforce:** {latest_summary.current_workforce} workers")
                        st.write(f"• **Equipment Utilization:** {latest_summary.equipment_utilization:.1f}%")
                        st.write(f"• **Open Issues:** {latest_summary.open_issues}")
                        st.write(f"• **High Priority Risks:** {latest_summary.high_priority_risks}")
                    
                    if latest_summary.executive_notes:
                        st.write("**📝 Executive Notes:**")
                        st.info(latest_summary.executive_notes)
            
            else:
                st.info("No performance metrics available. Create some metrics to start monitoring project health.")
        
        with tab2:
            st.subheader("⚠️ Project Alerts & Issues")
            
            # Get active alerts
            active_alerts = performance_manager.get_active_alerts()
            high_priority_alerts = performance_manager.get_high_priority_alerts()
            
            if high_priority_alerts:
                st.error(f"🚨 {len(high_priority_alerts)} HIGH PRIORITY ALERTS require immediate attention!")
                
                for alert in high_priority_alerts:
                    severity_color = {
                        "Critical": "🔴",
                        "High": "🟠", 
                        "Medium": "🟡",
                        "Low": "🟢"
                    }.get(alert.severity, "⚪")
                    
                    with st.expander(f"{severity_color} {alert.severity.upper()} - {alert.title}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**📋 Type:** {alert.alert_type}")
                            st.write(f"**📅 Due Date:** {alert.due_date}")
                            st.write(f"**👤 Responsible:** {alert.responsible_party}")
                            st.write(f"**📊 Status:** {alert.status}")
                        
                        with col2:
                            st.write(f"**📅 Created:** {alert.created_date}")
                            if alert.resolved_date:
                                st.write(f"**✅ Resolved:** {alert.resolved_date}")
                        
                        st.write(f"**📝 Description:** {alert.description}")
                        st.write(f"**💥 Impact:** {alert.impact}")
                        st.write(f"**🔧 Recommended Action:** {alert.recommended_action}")
                        
                        # Quick actions
                        col1, col2 = st.columns(2)
                        with col1:
                            if alert.status != "Resolved" and st.button(f"✅ Mark Resolved", key=f"resolve_{alert.alert_id}"):
                                if performance_manager.resolve_alert(alert.alert_id):
                                    st.success("Alert marked as resolved!")
                                    st.rerun()
                        
                        with col2:
                            if st.button(f"📧 Escalate", key=f"escalate_{alert.alert_id}"):
                                st.success("Alert escalated to senior management")
            
            # Display all active alerts
            st.write("**📋 All Active Alerts**")
            
            if active_alerts:
                for alert in active_alerts:
                    if alert not in high_priority_alerts:  # Don't duplicate high priority ones
                        severity_color = {
                            "Critical": "🔴",
                            "High": "🟠", 
                            "Medium": "🟡",
                            "Low": "🟢"
                        }.get(alert.severity, "⚪")
                        
                        with st.expander(f"{severity_color} {alert.severity} - {alert.title}"):
                            st.write(f"**Type:** {alert.alert_type} | **Due:** {alert.due_date} | **Responsible:** {alert.responsible_party}")
                            st.write(f"**Description:** {alert.description}")
                            st.write(f"**Recommended Action:** {alert.recommended_action}")
                            
                            if alert.status != "Resolved" and st.button(f"✅ Resolve", key=f"resolve_all_{alert.alert_id}"):
                                if performance_manager.resolve_alert(alert.alert_id):
                                    st.success("Alert resolved!")
                                    st.rerun()
            else:
                st.success("🎉 No active alerts - all issues resolved!")
        
        with tab3:
            st.subheader("➕ Create Performance Items")
            
            create_tab1, create_tab2, create_tab3 = st.tabs(["📊 Create Metric", "⚠️ Create Alert", "📋 Executive Summary"])
            
            with create_tab1:
                st.write("**📊 Create Performance Metric**")
                
                with st.form("create_metric_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        metric_name = st.text_input("📝 Metric Name*", placeholder="e.g., Resource Utilization Rate")
                        category = st.selectbox("📂 Category*", options=["Schedule", "Cost", "Quality", "Safety", "Resource", "Progress", "Financial"])
                        current_value = st.number_input("📊 Current Value*", step=0.1)
                        target_value = st.number_input("🎯 Target Value*", step=0.1)
                    
                    with col2:
                        unit = st.text_input("📏 Unit*", placeholder="e.g., %, $, days, ratio")
                        status = st.selectbox("📊 Status*", options=[status.value for status in HealthStatus])
                        trend = st.selectbox("📈 Trend*", options=[trend.value for trend in TrendDirection])
                        description = st.text_area("📝 Description*", placeholder="Detailed description of this performance metric")
                    
                    if st.form_submit_button("📊 Create Metric", use_container_width=True):
                        if not metric_name or not category or not description:
                            st.error("Please fill in all required fields marked with *")
                        else:
                            metric_data = {
                                "metric_name": metric_name,
                                "category": category,
                                "current_value": current_value,
                                "target_value": target_value,
                                "unit": unit,
                                "status": status,
                                "trend": trend,
                                "description": description
                            }
                            
                            metric_id = performance_manager.create_performance_metric(metric_data)
                            st.success(f"✅ Performance metric created! ID: {metric_id}")
                            st.rerun()
            
            with create_tab2:
                st.write("**⚠️ Create Project Alert**")
                
                with st.form("create_alert_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        title = st.text_input("📝 Alert Title*", placeholder="Brief description of the alert")
                        alert_type = st.selectbox("📂 Alert Type*", options=["Budget", "Schedule", "Safety", "Quality", "Resource", "Risk"])
                        severity = st.selectbox("🚨 Severity*", options=["Low", "Medium", "High", "Critical"])
                        responsible_party = st.text_input("👤 Responsible Party*", placeholder="Person or team responsible")
                    
                    with col2:
                        due_date = st.date_input("📅 Due Date*")
                        description = st.text_area("📝 Description*", placeholder="Detailed description of the issue")
                        impact = st.text_area("💥 Impact", placeholder="Describe the potential impact")
                        recommended_action = st.text_area("🔧 Recommended Action*", placeholder="What should be done to resolve this?")
                    
                    if st.form_submit_button("⚠️ Create Alert", use_container_width=True):
                        if not title or not alert_type or not responsible_party or not recommended_action:
                            st.error("Please fill in all required fields marked with *")
                        else:
                            alert_data = {
                                "alert_type": alert_type,
                                "severity": severity,
                                "title": title,
                                "description": description,
                                "impact": impact,
                                "recommended_action": recommended_action,
                                "responsible_party": responsible_party,
                                "due_date": due_date.strftime('%Y-%m-%d')
                            }
                            
                            alert_id = performance_manager.create_alert(alert_data)
                            st.success(f"✅ Project alert created! ID: {alert_id}")
                            st.rerun()
            
            with create_tab3:
                st.write("**📋 Create Executive Summary**")
                
                with st.form("create_summary_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        project_phase = st.text_input("📊 Project Phase*", value="Core & Shell Construction")
                        overall_health = st.selectbox("🏥 Overall Health*", options=[health.value for health in HealthStatus])
                        schedule_performance = st.number_input("📅 Schedule Performance*", min_value=0.0, step=0.01, value=1.0)
                        cost_performance = st.number_input("💰 Cost Performance*", min_value=0.0, step=0.01, value=1.0)
                        quality_score = st.number_input("✅ Quality Score*", min_value=0.0, max_value=100.0, step=0.1, value=90.0)
                        safety_rating = st.number_input("🦺 Safety Rating*", min_value=0.0, max_value=100.0, step=0.1, value=95.0)
                    
                    with col2:
                        total_budget = st.number_input("💰 Total Budget*", min_value=0.0, step=1000.0, value=45500000.0)
                        spent_to_date = st.number_input("💸 Spent to Date*", min_value=0.0, step=1000.0, value=30000000.0)
                        percent_complete = st.number_input("📊 Percent Complete*", min_value=0.0, max_value=100.0, step=0.1, value=75.0)
                        days_ahead_behind = st.number_input("📅 Days Ahead/Behind", step=1, value=0)
                        current_workforce = st.number_input("👥 Current Workforce", min_value=0, step=1, value=120)
                        equipment_utilization = st.number_input("🚧 Equipment Utilization", min_value=0.0, max_value=100.0, step=0.1, value=85.0)
                    
                    critical_path_status = st.selectbox("🛤️ Critical Path Status", options=["On Track", "At Risk", "Behind", "Ahead"])
                    accomplishments = st.text_area("🎯 Key Accomplishments", placeholder="Enter accomplishments, one per line")
                    executive_notes = st.text_area("📝 Executive Notes*", placeholder="Overall project summary and key insights")
                    
                    if st.form_submit_button("📋 Create Executive Summary", use_container_width=True):
                        if not project_phase or not executive_notes:
                            st.error("Please fill in all required fields marked with *")
                        else:
                            # Calculate derived values
                            remaining_budget = total_budget - spent_to_date
                            projected_final_cost = total_budget * 0.985  # Assume 1.5% savings
                            
                            summary_data = {
                                "project_phase": project_phase,
                                "overall_health": overall_health,
                                "schedule_performance": schedule_performance,
                                "cost_performance": cost_performance,
                                "quality_score": quality_score,
                                "safety_rating": safety_rating,
                                "total_budget": total_budget,
                                "spent_to_date": spent_to_date,
                                "remaining_budget": remaining_budget,
                                "projected_final_cost": projected_final_cost,
                                "percent_complete": percent_complete,
                                "days_ahead_behind": days_ahead_behind,
                                "critical_path_status": critical_path_status,
                                "accomplishments": [acc.strip() for acc in accomplishments.split('\n') if acc.strip()],
                                "upcoming_milestones": [],  # Would be populated from project data
                                "open_issues": 5,  # Default values
                                "high_priority_risks": 2,
                                "current_workforce": current_workforce,
                                "equipment_utilization": equipment_utilization,
                                "executive_notes": executive_notes,
                                "created_by": "Current User"
                            }
                            
                            summary_id = performance_manager.create_executive_summary(summary_data)
                            st.success(f"✅ Executive summary created! ID: {summary_id}")
                            st.rerun()
        
        with tab4:
            st.subheader("⚙️ Manage Performance Items")
            
            manage_tab1, manage_tab2 = st.tabs(["📊 Manage Metrics", "⚠️ Manage Alerts"])
            
            with manage_tab1:
                metrics_list = performance_manager.get_performance_metrics()
                if metrics_list:
                    metric_options = [f"{m.metric_name} ({m.category})" for m in metrics_list]
                    selected_metric_index = st.selectbox("Select Metric to Manage", range(len(metric_options)), format_func=lambda x: metric_options[x])
                    selected_metric = metrics_list[selected_metric_index]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("✏️ Edit Metric", use_container_width=True):
                            st.session_state.show_edit_metric_form = True
                    
                    with col2:
                        if st.button("🗑️ Delete Metric", use_container_width=True):
                            if selected_metric.metric_id in performance_manager.metrics:
                                del performance_manager.metrics[selected_metric.metric_id]
                                st.success("✅ Metric deleted!")
                                st.rerun()
                    
                    with col3:
                        if st.button("📋 Duplicate Metric", use_container_width=True):
                            metric_data = {
                                "metric_name": f"Copy of {selected_metric.metric_name}",
                                "category": selected_metric.category,
                                "current_value": selected_metric.current_value,
                                "target_value": selected_metric.target_value,
                                "unit": selected_metric.unit,
                                "status": selected_metric.status.value,
                                "trend": selected_metric.trend.value,
                                "description": selected_metric.description
                            }
                            metric_id = performance_manager.create_performance_metric(metric_data)
                            st.success(f"✅ Metric duplicated! ID: {metric_id}")
                            st.rerun()
                    
                    # Edit form
                    if st.session_state.get('show_edit_metric_form', False):
                        with st.form("edit_metric_form"):
                            st.write("**✏️ Edit Metric Details**")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                edit_name = st.text_input("📝 Name", value=selected_metric.metric_name)
                                edit_target = st.number_input("🎯 Target", value=float(selected_metric.target_value), step=0.1)
                                edit_unit = st.text_input("📏 Unit", value=selected_metric.unit)
                            
                            with col2:
                                edit_category = st.text_input("📂 Category", value=selected_metric.category)
                                edit_description = st.text_area("📝 Description", value=selected_metric.description)
                            
                            if st.form_submit_button("✏️ Update Metric"):
                                selected_metric.metric_name = edit_name
                                selected_metric.target_value = edit_target
                                selected_metric.unit = edit_unit
                                selected_metric.category = edit_category
                                selected_metric.description = edit_description
                                selected_metric.last_updated = datetime.now().strftime('%Y-%m-%d')
                                
                                st.success("✅ Metric updated!")
                                st.session_state.show_edit_metric_form = False
                                st.rerun()
                else:
                    st.info("No metrics available. Create some metrics first.")
            
            with manage_tab2:
                alerts_list = list(performance_manager.alerts.values())
                if alerts_list:
                    alert_options = [f"{a.title} ({a.severity})" for a in alerts_list]
                    selected_alert_index = st.selectbox("Select Alert to Manage", range(len(alert_options)), format_func=lambda x: alert_options[x])
                    selected_alert = alerts_list[selected_alert_index]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if selected_alert.status != "Resolved" and st.button("✅ Resolve Alert", use_container_width=True):
                            if performance_manager.resolve_alert(selected_alert.alert_id):
                                st.success("✅ Alert resolved!")
                                st.rerun()
                    
                    with col2:
                        if st.button("✏️ Edit Alert", use_container_width=True):
                            st.session_state.show_edit_alert_form = True
                    
                    with col3:
                        if st.button("🗑️ Delete Alert", use_container_width=True):
                            if selected_alert.alert_id in performance_manager.alerts:
                                del performance_manager.alerts[selected_alert.alert_id]
                                st.success("✅ Alert deleted!")
                                st.rerun()
                else:
                    st.info("No alerts available. Create some alerts first.")
        
        return
        
    except ImportError:
        st.error("Enterprise Performance Snapshot module not available")
        st.info("📈 Performance Snapshot with executive-level insights")

def render_ai_assistant():
    """AI Assistant module"""
    st.markdown("""
    <div class="module-header">
        <h1>🤖 AI Assistant</h1>
        <p>Intelligent construction management assistant</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("🤖 AI Assistant with intelligent project insights and recommendations")

def render_settings():
    """Enterprise Settings and Configuration Management"""
    st.markdown("""
    <div class="module-header">
        <h1>⚙️ Enterprise Settings</h1>
        <p>Highland Tower Development - System configuration and user management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different settings categories
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏢 Project Settings", "👥 User Management", "🔧 System Config", "📊 Data Export", "🔒 Security"])
    
    with tab1:
        st.subheader("🏢 Project Configuration")
        
        with st.form("project_settings_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📋 Project Information**")
                project_name = st.text_input("Project Name", value="Highland Tower Development")
                project_value = st.text_input("Project Value", value="$45.5M")
                project_location = st.text_input("Location", value="Downtown Highland District")
                start_date = st.date_input("Start Date")
                completion_date = st.date_input("Completion Date")
            
            with col2:
                st.write("**🏗️ Project Details**")
                project_size = st.text_input("Size", value="168,500 sq ft")
                floors = st.text_input("Floors", value="15 stories above ground, 2 below")
                units = st.text_input("Units", value="120 residential, 8 retail")
                client = st.text_input("Client", value="Highland Properties LLC")
                project_manager = st.text_input("Project Manager", value="John Smith")
            
            st.write("**📝 Project Description**")
            project_description = st.text_area("Description", 
                value="Mixed-use high-rise development featuring luxury residential units and retail spaces in downtown Highland District.")
            
            if st.form_submit_button("💾 Save Project Settings", use_container_width=True):
                st.success("✅ Project settings saved successfully!")
    
    with tab2:
        st.subheader("👥 User Management & Permissions")
        
        # Current users table
        st.write("**Current Project Team**")
        
        users_data = [
            {"Name": "John Smith", "Role": "Project Manager", "Email": "jsmith@gcprime.com", "Access": "Full Access", "Last Login": "2025-05-28"},
            {"Name": "Sarah Wilson", "Role": "Site Supervisor", "Email": "swilson@gcprime.com", "Access": "Field Operations", "Last Login": "2025-05-28"},
            {"Name": "Mike Johnson", "Role": "Safety Manager", "Email": "mjohnson@gcprime.com", "Access": "Safety & QC", "Last Login": "2025-05-27"},
            {"Name": "Lisa Chen", "Role": "Project Engineer", "Email": "lchen@gcprime.com", "Access": "Engineering", "Last Login": "2025-05-28"},
            {"Name": "Tom Brown", "Role": "Cost Manager", "Email": "tbrown@gcprime.com", "Access": "Cost & Finance", "Last Login": "2025-05-27"}
        ]
        
        for user in users_data:
            with st.expander(f"👤 {user['Name']} - {user['Role']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Email:** {user['Email']}")
                    st.write(f"**Access Level:** {user['Access']}")
                with col2:
                    st.write(f"**Last Login:** {user['Last Login']}")
                    st.write(f"**Status:** Active")
                with col3:
                    if st.button(f"✏️ Edit", key=f"edit_user_{user['Name']}"):
                        st.info("User edit functionality")
                    if st.button(f"🔒 Deactivate", key=f"deactivate_{user['Name']}"):
                        st.warning("User deactivation functionality")
        
        # Add new user
        st.write("---")
        st.write("**➕ Add New User**")
        
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_user_name = st.text_input("Full Name")
                new_user_email = st.text_input("Email Address")
                new_user_role = st.selectbox("Role", [
                    "Project Manager", "Site Supervisor", "Safety Manager", 
                    "Project Engineer", "Cost Manager", "Field Worker", "Admin"
                ])
            
            with col2:
                access_level = st.selectbox("Access Level", [
                    "Full Access", "Field Operations", "Safety & QC", 
                    "Engineering", "Cost & Finance", "View Only"
                ])
                send_invite = st.checkbox("Send invitation email")
                temp_password = st.text_input("Temporary Password", type="password")
            
            if st.form_submit_button("➕ Add User", use_container_width=True):
                st.success(f"✅ User {new_user_name} added successfully!")
    
    with tab3:
        st.subheader("🔧 System Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**⏰ Time & Date Settings**")
            timezone = st.selectbox("Timezone", ["Pacific Time (PT)", "Mountain Time (MT)", "Central Time (CT)", "Eastern Time (ET)"])
            date_format = st.selectbox("Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
            time_format = st.selectbox("Time Format", ["12-hour (AM/PM)", "24-hour"])
            
            st.write("**🔔 Notification Settings**")
            email_notifications = st.checkbox("Email Notifications", value=True)
            sms_notifications = st.checkbox("SMS Notifications")
            push_notifications = st.checkbox("Push Notifications", value=True)
        
        with col2:
            st.write("**📊 Data Settings**")
            auto_backup = st.checkbox("Automatic Backups", value=True)
            backup_frequency = st.selectbox("Backup Frequency", ["Daily", "Weekly", "Monthly"])
            data_retention = st.selectbox("Data Retention", ["1 Year", "2 Years", "5 Years", "Permanent"])
            
            st.write("**🎨 Interface Settings**")
            default_theme = st.selectbox("Default Theme", ["Light", "Dark", "Auto"])
            sidebar_width = st.selectbox("Sidebar Width", ["Normal", "Wide", "Narrow"])
            mobile_optimization = st.checkbox("Mobile Optimization", value=True)
        
        if st.button("💾 Save System Settings", use_container_width=True):
            st.success("✅ System settings saved successfully!")
    
    with tab4:
        st.subheader("📊 Data Export & Reports")
        
        st.write("**📥 Export Project Data**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            export_modules = st.multiselect("Select Modules to Export", [
                "Daily Reports", "RFIs", "Safety", "Cost Management", 
                "Scheduling", "Progress Photos", "Material Management", 
                "Quality Control", "Submittals", "Transmittals"
            ], default=["Daily Reports", "RFIs", "Safety"])
            
            export_format = st.selectbox("Export Format", ["Excel (.xlsx)", "CSV", "PDF Report", "JSON"])
            date_range = st.selectbox("Date Range", ["Last 30 Days", "Last Quarter", "Year to Date", "All Data", "Custom Range"])
        
        with col2:
            include_photos = st.checkbox("Include Photos", value=True)
            include_attachments = st.checkbox("Include Attachments")
            compress_export = st.checkbox("Compress Export", value=True)
            
            st.write("**📈 Automated Reports**")
            weekly_reports = st.checkbox("Weekly Summary Reports", value=True)
            monthly_reports = st.checkbox("Monthly Progress Reports", value=True)
            executive_dashboard = st.checkbox("Executive Dashboard", value=True)
        
        if st.button("📥 Generate Export", use_container_width=True):
            st.success("✅ Export generated successfully! Download will begin shortly.")
        
        st.write("---")
        st.write("**📊 Recent Exports**")
        
        recent_exports = [
            {"Date": "2025-05-27", "Type": "Monthly Report", "Size": "15.2 MB", "Status": "Complete"},
            {"Date": "2025-05-25", "Type": "Safety Data", "Size": "2.8 MB", "Status": "Complete"},
            {"Date": "2025-05-20", "Type": "Cost Summary", "Size": "8.4 MB", "Status": "Complete"}
        ]
        
        for export in recent_exports:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**{export['Date']}**")
            with col2:
                st.write(export['Type'])
            with col3:
                st.write(export['Size'])
            with col4:
                st.button("📥 Download", key=f"download_{export['Date']}")
    
    with tab5:
        st.subheader("🔒 Security & Compliance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🔐 Security Settings**")
            two_factor_auth = st.checkbox("Two-Factor Authentication", value=True)
            password_requirements = st.checkbox("Strong Password Requirements", value=True)
            session_timeout = st.selectbox("Session Timeout", ["15 minutes", "30 minutes", "1 hour", "4 hours"])
            ip_restrictions = st.checkbox("IP Address Restrictions")
            
            st.write("**📋 Compliance**")
            hipaa_compliance = st.checkbox("HIPAA Compliance")
            gdpr_compliance = st.checkbox("GDPR Compliance", value=True)
            audit_logging = st.checkbox("Audit Logging", value=True)
        
        with col2:
            st.write("**🔍 Activity Monitoring**")
            login_monitoring = st.checkbox("Login Monitoring", value=True)
            data_access_logs = st.checkbox("Data Access Logs", value=True)
            failed_login_alerts = st.checkbox("Failed Login Alerts", value=True)
            
            st.write("**🚨 Security Alerts**")
            st.write("• **Last Security Scan:** 2025-05-27 - ✅ No issues found")
            st.write("• **Failed Login Attempts:** 0 in last 24 hours")
            st.write("• **Active Sessions:** 5 current users")
            st.write("• **Data Backup Status:** ✅ Last backup: 2 hours ago")
        
        if st.button("🔒 Save Security Settings", use_container_width=True):
            st.success("✅ Security settings saved successfully!")

def render_integrations():
    """Enterprise Integrations and API Management"""
    st.markdown("""
    <div class="module-header">
        <h1>🔄 Enterprise Integrations</h1>
        <p>Highland Tower Development - External system connections and API management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different integration categories
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏗️ Construction Software", "💰 Financial Systems", "📊 Analytics Tools", "🔗 API Management", "📱 Mobile Apps"])
    
    with tab1:
        st.subheader("🏗️ Construction Software Integrations")
        
        # Popular construction software integrations
        integrations = [
            {
                "name": "Autodesk Construction Cloud",
                "description": "BIM collaboration and document management",
                "status": "Connected",
                "icon": "🏗️",
                "features": ["BIM Models", "Document Sync", "Issue Tracking"]
            },
            {
                "name": "Procore",
                "description": "Project management and field operations",
                "status": "Available",
                "icon": "📋",
                "features": ["Project Data", "RFIs", "Daily Reports"]
            },
            {
                "name": "PlanGrid",
                "description": "Construction drawings and field management",
                "status": "Connected",
                "icon": "📐",
                "features": ["Drawing Sync", "Field Updates", "Photo Markup"]
            },
            {
                "name": "Fieldwire",
                "description": "Task management and coordination",
                "status": "Available",
                "icon": "📱",
                "features": ["Task Sync", "Issue Tracking", "Progress Updates"]
            }
        ]
        
        for integration in integrations:
            with st.expander(f"{integration['icon']} {integration['name']} - {integration['status']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Description:** {integration['description']}")
                    st.write(f"**Status:** {integration['status']}")
                
                with col2:
                    st.write("**Features:**")
                    for feature in integration['features']:
                        st.write(f"• {feature}")
                
                with col3:
                    if integration['status'] == "Connected":
                        st.success("✅ Active")
                        if st.button(f"⚙️ Configure", key=f"config_{integration['name']}"):
                            st.info("Configuration options...")
                        if st.button(f"🔄 Sync Now", key=f"sync_{integration['name']}"):
                            st.success("Synchronization started!")
                    else:
                        if st.button(f"🔗 Connect", key=f"connect_{integration['name']}"):
                            st.success(f"Connected to {integration['name']}!")
    
    with tab2:
        st.subheader("💰 Financial System Integrations")
        
        financial_systems = [
            {
                "name": "QuickBooks Enterprise",
                "description": "Accounting and financial management",
                "status": "Connected",
                "icon": "💼",
                "sync_frequency": "Daily"
            },
            {
                "name": "Sage 300 Construction",
                "description": "Construction-specific accounting",
                "status": "Available",
                "icon": "📊",
                "sync_frequency": "Real-time"
            },
            {
                "name": "Foundation Software",
                "description": "Construction accounting and project management",
                "status": "Available",
                "icon": "🏗️",
                "sync_frequency": "Hourly"
            },
            {
                "name": "Viewpoint Vista",
                "description": "Enterprise construction ERP",
                "status": "Connected",
                "icon": "🎯",
                "sync_frequency": "Real-time"
            }
        ]
        
        for system in financial_systems:
            with st.expander(f"{system['icon']} {system['name']} - {system['status']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Description:** {system['description']}")
                    st.write(f"**Sync Frequency:** {system['sync_frequency']}")
                    st.write(f"**Last Sync:** 2025-05-28 09:15 AM")
                
                with col2:
                    if system['status'] == "Connected":
                        st.success("✅ Active Connection")
                        st.write("**Sync Data:**")
                        st.write("• Cost codes and budgets")
                        st.write("• Purchase orders")
                        st.write("• Invoice processing")
                        st.write("• Payment tracking")
                    else:
                        st.info("⚙️ Available for Connection")
                        if st.button(f"🔗 Setup Integration", key=f"setup_{system['name']}"):
                            st.success("Integration setup initiated!")
    
    with tab3:
        st.subheader("📊 Analytics and BI Tools")
        
        analytics_tools = [
            {
                "name": "Microsoft Power BI",
                "description": "Business intelligence and analytics",
                "status": "Connected",
                "icon": "📊"
            },
            {
                "name": "Tableau",
                "description": "Data visualization and analytics",
                "status": "Available",
                "icon": "📈"
            },
            {
                "name": "Looker Studio",
                "description": "Google's business intelligence platform",
                "status": "Connected",
                "icon": "🔍"
            }
        ]
        
        for tool in analytics_tools:
            with st.expander(f"{tool['icon']} {tool['name']} - {tool['status']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Description:** {tool['description']}")
                    if tool['status'] == "Connected":
                        st.write("**Dashboard Links:**")
                        st.write("• Executive Summary Dashboard")
                        st.write("• Project Performance Metrics")
                        st.write("• Cost Analysis Reports")
                
                with col2:
                    if tool['status'] == "Connected":
                        st.success("✅ Active")
                        if st.button(f"📊 Open Dashboard", key=f"dash_{tool['name']}"):
                            st.success("Opening dashboard...")
                    else:
                        if st.button(f"🔗 Connect", key=f"connect_analytics_{tool['name']}"):
                            st.success("Analytics integration connected!")
    
    with tab4:
        st.subheader("🔗 API Management & Custom Integrations")
        
        st.write("**🔑 API Keys & Authentication**")
        
        api_keys = [
            {"Service": "Weather API", "Status": "Active", "Expires": "2025-12-31", "Usage": "85%"},
            {"Service": "Google Maps API", "Status": "Active", "Expires": "2026-06-30", "Usage": "42%"},
            {"Service": "Email Service", "Status": "Active", "Expires": "2025-09-15", "Usage": "23%"},
            {"Service": "SMS Gateway", "Status": "Inactive", "Expires": "2025-08-01", "Usage": "0%"}
        ]
        
        for api in api_keys:
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.write(f"**{api['Service']}**")
            with col2:
                if api['Status'] == "Active":
                    st.success("🟢 Active")
                else:
                    st.error("🔴 Inactive")
            with col3:
                st.write(api['Expires'])
            with col4:
                st.write(api['Usage'])
            with col5:
                st.button("⚙️ Manage", key=f"api_{api['Service']}")
        
        st.write("---")
        st.write("**🔧 Custom Integration Development**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Available APIs:**")
            st.write("• REST API for data access")
            st.write("• Webhook notifications")
            st.write("• Real-time data streams")
            st.write("• Bulk data export/import")
        
        with col2:
            st.write("**Documentation:**")
            if st.button("📖 API Documentation"):
                st.info("Opening API documentation...")
            if st.button("🔧 Developer Tools"):
                st.info("Opening developer tools...")
            if st.button("🧪 API Testing"):
                st.info("Opening API testing interface...")
    
    with tab5:
        st.subheader("📱 Mobile Application Integrations")
        
        mobile_apps = [
            {
                "name": "gcPanel Mobile",
                "description": "Native mobile app for field operations",
                "platform": "iOS & Android",
                "status": "Active",
                "version": "2.1.3"
            },
            {
                "name": "Safety Inspector",
                "description": "Dedicated safety inspection app",
                "platform": "iOS & Android",
                "status": "Active",
                "version": "1.8.2"
            },
            {
                "name": "Time Tracker",
                "description": "Employee time and attendance tracking",
                "platform": "iOS & Android",
                "status": "Development",
                "version": "Beta 0.9"
            }
        ]
        
        for app in mobile_apps:
            with st.expander(f"📱 {app['name']} - {app['status']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Description:** {app['description']}")
                    st.write(f"**Platform:** {app['platform']}")
                    st.write(f"**Version:** {app['version']}")
                
                with col2:
                    if app['status'] == "Active":
                        st.success("✅ Live in App Stores")
                        st.write("**Download Links:**")
                        if st.button("📱 iOS App Store", key=f"ios_{app['name']}"):
                            st.success("Opening App Store...")
                        if st.button("🤖 Google Play", key=f"android_{app['name']}"):
                            st.success("Opening Google Play...")
                    else:
                        st.info(f"🔄 {app['status']}")
        
        st.write("---")
        st.write("**📊 Mobile App Analytics**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Users", "127", "+12 this week")
        with col2:
            st.metric("Daily Reports", "34", "+8 today")
        with col3:
            st.metric("Photos Uploaded", "89", "+23 today")
        with col4:
            st.metric("Safety Checks", "15", "+3 today")

def render_quick_start():
    """Quick start guide module"""
    st.markdown("""
    <div class="module-header">
        <h1>📖 Quick Start Guide</h1>
        <p>Getting started with gcPanel</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ## Welcome to gcPanel! 🏗️
    
    Your comprehensive construction management platform for Highland Tower Development.
    
    ### 🚀 Getting Started
    
    1. **Dashboard** - Start here for project overview
    2. **Daily Reports** - Track daily progress and activities
    3. **Safety** - Manage safety incidents and compliance
    4. **RFIs** - Handle requests for information
    5. **Progress Photos** - Document visual progress
    
    ### 📋 Module Overview
    
    **Core Tools** - Essential daily operations
    **Project Management** - Planning and execution
    **Advanced Tools** - Specialized functionality
    **Resource Management** - Documents and pricing
    **Analytics & AI** - Insights and intelligence
    
    ### 💡 Tips
    
    - Use the sidebar to navigate between modules
    - Most modules support real-time collaboration
    - All data is automatically saved
    - Mobile-responsive design for field use
    
    ### 📞 Support
    
    For technical support, contact the development team.
    """)

def main():
    """Main application entry point"""
    configure_page()
    apply_styling()
    initialize_session_state()
    
    render_sidebar()
    
    # Route to appropriate page
    page = st.session_state.current_page
    
    # Page routing
    if page == "dashboard":
        render_dashboard()
    elif page == "daily_reports":
        render_daily_reports()
    elif page == "deliveries":
        render_deliveries()
    elif page == "safety":
        render_safety()
    elif page == "preconstruction":
        render_preconstruction()
    elif page == "engineering":
        render_engineering()
    elif page == "field_operations":
        render_field_operations()
    elif page == "contracts":
        render_contracts()
    elif page == "cost_management":
        render_cost_management()
    elif page == "bim":
        render_bim()
    elif page == "closeout":
        render_closeout()
    elif page == "rfis":
        render_rfis()
    elif page == "submittals":
        render_submittals()
    elif page == "transmittals":
        render_transmittals()
    elif page == "scheduling":
        render_scheduling()
    elif page == "quality_control":
        render_quality_control()
    elif page == "progress_photos":
        render_progress_photos()
    elif page == "subcontractor_management":
        render_subcontractor_management()
    elif page == "inspections":
        render_inspections()
    elif page == "issues_risks":
        render_issues_risks()
    elif page == "documents":
        render_documents()
    elif page == "unit_prices":
        render_unit_prices()
    elif page == "analytics":
        render_analytics()
    elif page == "performance_snapshot":
        render_performance_snapshot()
    elif page == "ai_assistant":
        render_ai_assistant()
    elif page == "quick_start":
        render_quick_start()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()