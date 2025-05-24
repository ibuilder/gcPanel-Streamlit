"""
Clean Modern Styling for Highland Tower Development Dashboard

This module provides a lighter, cleaner, and more modern visual design
with improved readability and professional construction industry aesthetics.
"""

import streamlit as st

def apply_clean_modern_styles():
    """Apply clean, modern styling with lighter colors and better spacing"""
    
    st.markdown("""
    <style>
    /* Import clean modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Clean Layout */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #fafbfc;
        color: #2d3748;
    }
    
    /* Clean Header Styling */
    .header-container {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        border-bottom: 1px solid #e2e8f0;
        padding: 1rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }
    
    /* Light Clean Cards */
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        transition: all 0.2s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        border-color: #cbd5e0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    /* Clean Button Styling */
    .stButton > button {
        background: #4299e1;
        border: none;
        border-radius: 6px;
        color: white;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
        box-shadow: none;
        font-size: 0.875rem;
    }
    
    .stButton > button:hover {
        background: #3182ce;
        transform: none;
        box-shadow: 0 1px 3px rgba(66, 153, 225, 0.2);
    }
    
    /* Clean Primary Button */
    .stButton > button[kind="primary"] {
        background: #48bb78;
        color: white;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #38a169;
    }
    
    /* Light Status Colors */
    .status-active { color: #38a169; font-weight: 500; }
    .status-pending { color: #ed8936; font-weight: 500; }
    .status-critical { color: #e53e3e; font-weight: 500; }
    .status-completed { color: #4299e1; font-weight: 500; }
    
    /* Clean Module Cards */
    .module-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    
    .module-card:hover {
        border-color: #cbd5e0;
    }
    
    /* Clean Navigation */
    .stSelectbox > div > div {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        font-size: 0.875rem;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #4299e1;
        box-shadow: 0 0 0 1px #4299e1;
    }
    
    /* Clean Input Fields */
    .stTextInput > div > div > input {
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 0.5rem 0.75rem;
        font-size: 0.875rem;
        background: #ffffff;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4299e1;
        box-shadow: 0 0 0 1px #4299e1;
    }
    
    /* Clean Data Tables */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        overflow: hidden;
    }
    
    .stDataFrame table {
        font-size: 0.875rem;
    }
    
    /* Light Progress Bars */
    .progress-container {
        background: #f7fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 6px;
        background: #e2e8f0;
        border-radius: 3px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: #48bb78;
        border-radius: 3px;
        transition: width 0.3s ease;
    }
    
    /* Clean Alert Styles */
    .alert-success {
        background: #f0fff4;
        border: 1px solid #9ae6b4;
        border-left: 3px solid #48bb78;
        color: #22543d;
        padding: 0.75rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        font-size: 0.875rem;
    }
    
    .alert-warning {
        background: #fffbf0;
        border: 1px solid #fbd38d;
        border-left: 3px solid #ed8936;
        color: #7b341e;
        padding: 0.75rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        font-size: 0.875rem;
    }
    
    .alert-error {
        background: #fff5f5;
        border: 1px solid #feb2b2;
        border-left: 3px solid #e53e3e;
        color: #742a2a;
        padding: 0.75rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        font-size: 0.875rem;
    }
    
    /* Clean Typography */
    h1, h2, h3 {
        color: #2d3748;
        font-weight: 600;
        line-height: 1.2;
    }
    
    h1 { font-size: 1.875rem; margin-bottom: 1rem; }
    h2 { font-size: 1.5rem; margin-bottom: 0.75rem; }
    h3 { font-size: 1.25rem; margin-bottom: 0.5rem; }
    
    /* Clean Spacing */
    .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Light Construction Colors */
    .construction-orange { color: #ed8936; }
    .construction-blue { color: #4299e1; }
    .construction-green { color: #48bb78; }
    .construction-gray { color: #718096; }
    
    /* Clean Badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-success {
        background: #c6f6d5;
        color: #22543d;
    }
    
    .badge-warning {
        background: #feebc8;
        color: #7b341e;
    }
    
    .badge-info {
        background: #bee3f8;
        color: #2a4365;
    }
    
    /* Clean Header Logo */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .logo-text {
        font-weight: 600;
        font-size: 1.125rem;
        color: #2d3748;
    }
    
    .logo-accent {
        color: #4299e1;
    }
    
    /* Mobile Responsive Clean Design */
    @media (max-width: 768px) {
        .module-card {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        h1 { font-size: 1.5rem; }
        h2 { font-size: 1.25rem; }
        h3 { font-size: 1.125rem; }
    }
    
    /* Clean Minimal Animations */
    * {
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    
    /* Hide Streamlit Branding for Cleaner Look */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Full Width Container */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    .main .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

def create_clean_status_badge(status, text):
    """Create a clean, minimal status badge"""
    
    badge_classes = {
        "success": "badge-success",
        "warning": "badge-warning", 
        "info": "badge-info",
        "active": "badge-success",
        "pending": "badge-warning",
        "completed": "badge-info"
    }
    
    badge_class = badge_classes.get(status, "badge-info")
    
    st.markdown(f"""
    <span class="status-badge {badge_class}">{text}</span>
    """, unsafe_allow_html=True)

def create_clean_metric_card(title, value, change=None, icon="📊"):
    """Create a clean, minimal metric card"""
    
    change_html = ""
    if change:
        change_color = "#48bb78" if change.startswith("+") else "#e53e3e"
        change_html = f'<div style="color: {change_color}; font-size: 0.75rem; margin-top: 0.25rem;">{change}</div>'
    
    st.markdown(f"""
    <div class="metric-card">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span style="margin-right: 0.5rem; font-size: 1.25rem;">{icon}</span>
            <span style="font-size: 0.875rem; color: #718096; font-weight: 500;">{title}</span>
        </div>
        <div style="font-size: 1.5rem; font-weight: 600; color: #2d3748;">{value}</div>
        {change_html}
    </div>
    """, unsafe_allow_html=True)