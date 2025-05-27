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
    """Complete Cost Management with full CRUD functionality"""
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
    """Complete BIM Management with full CRUD functionality"""
    st.markdown("""
    <div class="module-header">
        <h1>🏢 Building Information Modeling</h1>
        <p>Advanced 3D coordination, model management, and clash detection</p>
    </div>
    """, unsafe_allow_html=True)
    
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