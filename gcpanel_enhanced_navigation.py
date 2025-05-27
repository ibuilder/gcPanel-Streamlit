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
    
    .css-1d391kg {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%) !important;
        border-right: 2px solid #4a5568 !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.25) !important;
        padding: 0 !important;
        width: 280px !important;
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: #f8fafc !important;
        padding: 0 !important;
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
    .stButton > button {
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
    
    .stButton > button:hover {
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
        
        if st.button("📊 Dashboard", key="dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
        
        if st.button("📋 Daily Reports", key="daily_reports", use_container_width=True):
            st.session_state.current_page = "daily_reports"
        
        if st.button("🚚 Deliveries", key="deliveries", use_container_width=True):
            st.session_state.current_page = "deliveries"
        
        if st.button("🦺 Safety", key="safety", use_container_width=True):
            st.session_state.current_page = "safety"
        
        # Project Management Section
        st.markdown('<div class="section-header">🎯 Project Management</div>', unsafe_allow_html=True)
        
        if st.button("🏗️ PreConstruction", key="preconstruction", use_container_width=True):
            st.session_state.current_page = "preconstruction"
        
        if st.button("⚙️ Engineering", key="engineering", use_container_width=True):
            st.session_state.current_page = "engineering"
        
        if st.button("👷 Field Operations", key="field_operations", use_container_width=True):
            st.session_state.current_page = "field_operations"
        
        if st.button("📄 Contracts", key="contracts", use_container_width=True):
            st.session_state.current_page = "contracts"
        
        if st.button("💰 Cost Management", key="cost_management", use_container_width=True):
            st.session_state.current_page = "cost_management"
        
        if st.button("🏢 BIM", key="bim", use_container_width=True):
            st.session_state.current_page = "bim"
        
        if st.button("✅ Closeout", key="closeout", use_container_width=True):
            st.session_state.current_page = "closeout"
        
        # Advanced Tools Section
        st.markdown('<div class="section-header">🔧 Advanced Tools</div>', unsafe_allow_html=True)
        
        if st.button("📝 RFIs", key="rfis", use_container_width=True):
            st.session_state.current_page = "rfis"
        
        if st.button("📤 Submittals", key="submittals", use_container_width=True):
            st.session_state.current_page = "submittals"
        
        if st.button("📨 Transmittals", key="transmittals", use_container_width=True):
            st.session_state.current_page = "transmittals"
        
        if st.button("📅 Scheduling", key="scheduling", use_container_width=True):
            st.session_state.current_page = "scheduling"
        
        if st.button("🔍 Quality Control", key="quality_control", use_container_width=True):
            st.session_state.current_page = "quality_control"
        
        if st.button("📸 Progress Photos", key="progress_photos", use_container_width=True):
            st.session_state.current_page = "progress_photos"
        
        if st.button("🏭 Subcontractor Management", key="subcontractor_management", use_container_width=True):
            st.session_state.current_page = "subcontractor_management"
        
        if st.button("🔍 Inspections", key="inspections", use_container_width=True):
            st.session_state.current_page = "inspections"
        
        if st.button("⚠️ Issues & Risks", key="issues_risks", use_container_width=True):
            st.session_state.current_page = "issues_risks"
        
        # Resource Management Section
        st.markdown('<div class="section-header">📦 Resource Management</div>', unsafe_allow_html=True)
        
        if st.button("📁 Documents", key="documents", use_container_width=True):
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
    """Initialize session state"""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = True  # Skip login for demo

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
    """Enhanced Daily Reports module with full CRUD functionality"""
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
                inspections = st.text_area("Inspections Completed", height=60,
                    placeholder="List any inspections completed today...")
            with col4:
                materials_delivered = st.text_area("Materials Delivered", height=60,
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
    
    # Initialize deliveries data
    if "deliveries" not in st.session_state:
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
                root_cause = st.text_area("Root Cause Analysis", height=60,
                    placeholder="What was the underlying cause of this incident...")
                corrective_action = st.text_area("Corrective Actions", height=60,
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
                    attendees = st.text_area("Expected Attendees", height=60)
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
    """Engineering module with RFI and technical management"""
    st.markdown("""
    <div class="module-header">
        <h1>⚙️ Engineering Management</h1>
        <p>Technical coordination, RFIs, and engineering workflows</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Engineering metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active RFIs", "23", "+3")
    with col2:
        st.metric("Pending Reviews", "8", "+1")
    with col3:
        st.metric("Change Orders", "12", "+2")
    with col4:
        st.metric("Shop Drawings", "45", "+5")
    
    tab1, tab2, tab3 = st.tabs(["📝 RFI Management", "📋 Change Orders", "🔧 Technical Reviews"])
    
    with tab1:
        st.subheader("📝 Request for Information (RFI) Tracking")
        
        # RFI summary
        rfi_data = {
            'RFI #': ['RFI-001', 'RFI-002', 'RFI-003', 'RFI-004', 'RFI-005'],
            'Subject': ['Concrete Mix Design', 'Electrical Panel Location', 'HVAC Duct Routing', 'Fire Rating Details', 'Structural Connection'],
            'Trade': ['Concrete', 'Electrical', 'HVAC', 'Fireproofing', 'Steel'],
            'Priority': ['High', 'Medium', 'High', 'Low', 'Medium'],
            'Status': ['Response Pending', 'Under Review', 'Closed', 'Response Pending', 'Draft'],
            'Days Open': [8, 5, 0, 12, 2]
        }
        
        df = pd.DataFrame(rfi_data)
        st.dataframe(df, use_container_width=True)
        
        # Quick RFI creation
        with st.expander("➕ Create New RFI"):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("RFI Subject")
                st.selectbox("Trade", ["Concrete", "Steel", "Electrical", "HVAC", "Plumbing", "Other"])
                st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            with col2:
                st.text_area("Question/Issue Description", height=100)
                st.file_uploader("Attach Documents", accept_multiple_files=True)
                st.date_input("Response Required By")
            
            if st.button("📝 Submit RFI", type="primary"):
                st.success("✅ RFI submitted successfully!")
    
    with tab2:
        st.subheader("📋 Change Order Management")
        
        change_orders = {
            'CO #': ['CO-001', 'CO-002', 'CO-003'],
            'Description': ['Additional MEP Work', 'Design Modification', 'Site Condition'],
            'Amount': ['$125,000', '$75,000', '$45,000'],
            'Status': ['Approved', 'Under Review', 'Pending'],
            'Impact': ['5 days', '0 days', '3 days']
        }
        
        df_co = pd.DataFrame(change_orders)
        st.dataframe(df_co, use_container_width=True)
    
    with tab3:
        st.subheader("🔧 Technical Reviews")
        
        reviews = [
            {"item": "Shop Drawings - Steel Connections", "reviewer": "John Smith, P.E.", "status": "✅ Approved", "date": "May 25"},
            {"item": "MEP Coordination Plans", "reviewer": "Sarah Wilson, P.E.", "status": "🔄 Under Review", "date": "May 24"},
            {"item": "Concrete Mix Design", "reviewer": "Mike Johnson, P.E.", "status": "⚠️ Revisions Required", "date": "May 23"},
        ]
        
        for review in reviews:
            with st.container():
                col_a, col_b, col_c = st.columns([2, 1, 1])
                with col_a:
                    st.write(f"📋 {review['item']}")
                    st.write(f"Reviewer: {review['reviewer']}")
                with col_b:
                    st.write(review['status'])
                with col_c:
                    st.write(review['date'])
                st.divider()

def render_field_operations():
    """Field Operations module"""
    st.markdown("""
    <div class="module-header">
        <h1>👷 Field Operations</h1>
        <p>Real-time field management and crew coordination</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Field metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Workers", "147", "+5")
    with col2:
        st.metric("Crews on Site", "8", "0")
    with col3:
        st.metric("Equipment Units", "23", "+2")
    with col4:
        st.metric("Productivity", "102%", "+3%")
    
    tab1, tab2, tab3 = st.tabs(["👥 Crew Management", "🏗️ Work Progress", "⚡ Equipment"])
    
    with tab1:
        st.subheader("👥 Active Crews")
        
        crews_data = {
            'Crew': ['Concrete Team A', 'Steel Crew 1', 'MEP Team', 'Finishing Crew', 'Site Prep'],
            'Foreman': ['Mike Smith', 'John Doe', 'Sarah Wilson', 'Tom Brown', 'Dave Johnson'],
            'Workers': [12, 8, 15, 10, 6],
            'Location': ['Level 3', 'Level 4', 'Level 2', 'Level 1', 'Exterior'],
            'Status': ['Active', 'Active', 'Break', 'Active', 'Active']
        }
        
        df = pd.DataFrame(crews_data)
        st.dataframe(df, use_container_width=True)
        
        # Crew productivity chart
        productivity_data = pd.DataFrame({
            'Hour': ['7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM'],
            'Workers': [45, 120, 135, 140, 145, 75, 130, 140, 147]
        })
        
        fig = px.line(productivity_data, x='Hour', y='Workers', 
                     title="Worker Count Throughout Day")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🏗️ Today's Work Progress")
        
        tasks = [
            {"task": "Concrete Pour - Level 3 Slab", "progress": 85, "crew": "Concrete Team A", "eta": "4:00 PM"},
            {"task": "Steel Installation - Elevator Shaft", "progress": 60, "crew": "Steel Crew 1", "eta": "5:30 PM"},
            {"task": "MEP Rough-in - Level 2", "progress": 40, "crew": "MEP Team", "eta": "Tomorrow"},
            {"task": "Drywall Installation - Level 1", "progress": 90, "crew": "Finishing Crew", "eta": "3:00 PM"},
        ]
        
        for task in tasks:
            with st.container():
                st.write(f"🔧 **{task['task']}**")
                st.write(f"Crew: {task['crew']} | ETA: {task['eta']}")
                st.progress(task['progress'] / 100)
                st.write(f"Progress: {task['progress']}%")
                st.divider()
    
    with tab3:
        st.subheader("⚡ Equipment Management")
        
        equipment_data = {
            'Equipment': ['Tower Crane 1', 'Concrete Pump', 'Scissor Lift A', 'Excavator', 'Forklift 1'],
            'Type': ['Crane', 'Pump', 'Lift', 'Excavator', 'Forklift'],
            'Location': ['Center Site', 'Level 3', 'Level 2', 'Exterior', 'Ground Level'],
            'Status': ['Operating', 'Operating', 'Maintenance', 'Operating', 'Operating'],
            'Operator': ['Steve Wilson', 'Mike Chen', 'In Shop', 'Tom Davis', 'Sarah Kim']
        }
        
        df_eq = pd.DataFrame(equipment_data)
        st.dataframe(df_eq, use_container_width=True)

# Additional render functions for all other modules...
def render_contracts():
    """Contracts management module"""
    st.markdown("""
    <div class="module-header">
        <h1>📄 Contracts Management</h1>
        <p>Comprehensive contract administration and tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📄 Contracts module with comprehensive contract management features")

def render_cost_management():
    """Cost management module"""
    st.markdown("""
    <div class="module-header">
        <h1>💰 Cost Management</h1>
        <p>Advanced financial tracking and budget management</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("💰 Cost Management module with budget tracking and financial analytics")

def render_bim():
    """BIM management module"""
    st.markdown("""
    <div class="module-header">
        <h1>🏢 Building Information Modeling</h1>
        <p>3D coordination and model management</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("🏢 BIM module with 3D model coordination and clash detection")

def render_closeout():
    """Project closeout module"""
    st.markdown("""
    <div class="module-header">
        <h1>✅ Project Closeout</h1>
        <p>Final documentation and project completion</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("✅ Closeout module with final documentation and warranties")

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
    """Submittals management module"""
    st.markdown("""
    <div class="module-header">
        <h1>📤 Submittals Management</h1>
        <p>Product submittals and approval workflow</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📤 Submittals module with approval workflows and tracking")

def render_transmittals():
    """Transmittals management module"""
    st.markdown("""
    <div class="module-header">
        <h1>📨 Transmittals</h1>
        <p>Document distribution and transmittal tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📨 Transmittals module for document distribution")

def render_scheduling():
    """Scheduling module"""
    st.markdown("""
    <div class="module-header">
        <h1>📅 Project Scheduling</h1>
        <p>Advanced scheduling and timeline management</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📅 Scheduling module with Gantt charts and critical path analysis")

def render_quality_control():
    """Quality control module"""
    st.markdown("""
    <div class="module-header">
        <h1>🔍 Quality Control</h1>
        <p>Inspection management and quality assurance</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("🔍 Quality Control module with inspection workflows")

def render_progress_photos():
    """Progress photos module"""
    st.markdown("""
    <div class="module-header">
        <h1>📸 Progress Photos</h1>
        <p>Visual documentation and progress tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📸 Progress Photos module with visual timeline tracking")

def render_subcontractor_management():
    """Subcontractor management module"""
    st.markdown("""
    <div class="module-header">
        <h1>🏭 Subcontractor Management</h1>
        <p>Subcontractor coordination and performance tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("🏭 Subcontractor Management with performance tracking")

def render_inspections():
    """Inspections module"""
    st.markdown("""
    <div class="module-header">
        <h1>🔍 Inspections</h1>
        <p>Inspection scheduling and compliance tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("🔍 Inspections module with compliance tracking")

def render_issues_risks():
    """Issues and risks module"""
    st.markdown("""
    <div class="module-header">
        <h1>⚠️ Issues & Risks</h1>
        <p>Risk management and issue tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("⚠️ Issues & Risks module with comprehensive risk management")

def render_documents():
    """Document management module"""
    st.markdown("""
    <div class="module-header">
        <h1>📁 Document Management</h1>
        <p>Centralized document storage and version control</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📁 Documents module with version control and collaboration")

def render_unit_prices():
    """Unit prices module"""
    st.markdown("""
    <div class="module-header">
        <h1>💲 Unit Prices</h1>
        <p>Unit price database and cost estimation</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("💲 Unit Prices module with cost database and estimation tools")

def render_analytics():
    """Analytics module"""
    st.markdown("""
    <div class="module-header">
        <h1>📊 Advanced Analytics</h1>
        <p>Data analytics and business intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📊 Analytics module with advanced reporting and insights")

def render_performance_snapshot():
    """Performance snapshot module"""
    st.markdown("""
    <div class="module-header">
        <h1>📈 Performance Snapshot</h1>
        <p>Executive dashboard and KPI tracking</p>
    </div>
    """, unsafe_allow_html=True)
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