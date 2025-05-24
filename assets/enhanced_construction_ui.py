"""
Enhanced Construction Industry UI/UX Improvements for Highland Tower Development

This module provides professional construction industry styling with smooth animations,
modern card layouts, and improved visual hierarchy specifically designed for
construction project management applications.
"""

import streamlit as st

def apply_enhanced_construction_styles():
    """Apply enhanced construction industry styling with animations and modern UI"""
    
    st.markdown("""
    <style>
    /* Import Google Fonts for professional typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Typography and Layout */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Enhanced Header Styling */
    .header-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1rem 2rem;
        border-radius: 0 0 1rem 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border-bottom: 3px solid #f59e0b;
    }
    
    /* Professional Card Styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #3b82f6;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* Construction Industry Color Palette */
    .status-active { color: #10b981; font-weight: 600; }
    .status-pending { color: #f59e0b; font-weight: 600; }
    .status-critical { color: #ef4444; font-weight: 600; }
    .status-completed { color: #6366f1; font-weight: 600; }
    
    /* Enhanced Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    }
    
    /* Construction Progress Indicators */
    .progress-container {
        background: #f1f5f9;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #f59e0b;
    }
    
    .progress-bar {
        height: 8px;
        background: #e2e8f0;
        border-radius: 4px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        border-radius: 4px;
        transition: width 0.8s ease;
    }
    
    /* Module Card Layout */
    .module-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .module-card:hover {
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.1);
        border-color: #3b82f6;
    }
    
    /* Data Table Enhancements */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    /* Navigation Enhancements */
    .stSelectbox > div > div {
        background: white;
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Alert and Notification Styling */
    .alert-success {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-error {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Construction Industry Icons */
    .icon-construction { color: #f59e0b; }
    .icon-safety { color: #ef4444; }
    .icon-progress { color: #10b981; }
    .icon-schedule { color: #3b82f6; }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .module-card {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
    }
    
    /* Smooth Animations */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-slide-in {
        animation: slideIn 0.6s ease-out;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .animate-pulse {
        animation: pulse 2s infinite;
    }
    
    /* Loading States */
    .loading-spinner {
        border: 3px solid #e2e8f0;
        border-top: 3px solid #3b82f6;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Professional Form Styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Construction Dashboard Specific */
    .dashboard-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .project-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    /* Enhanced Hover Effects */
    .hover-lift {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .hover-lift:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    </style>
    """, unsafe_allow_html=True)

def create_construction_card(title, content, icon="🏗️", status="active"):
    """Create a professional construction industry card component"""
    
    status_class = f"status-{status}"
    
    st.markdown(f"""
    <div class="module-card hover-lift animate-slide-in">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 1.5rem; margin-right: 0.75rem;">{icon}</span>
            <h3 style="margin: 0; color: #1e293b; font-weight: 600;">{title}</h3>
            <span class="{status_class}" style="margin-left: auto; font-size: 0.875rem;">
                ● {status.upper()}
            </span>
        </div>
        <div style="color: #64748b; line-height: 1.6;">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_progress_indicator(label, percentage, color="#10b981"):
    """Create an animated progress indicator"""
    
    st.markdown(f"""
    <div class="progress-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-weight: 600; color: #1e293b;">{label}</span>
            <span style="font-weight: 600; color: {color};">{percentage}%</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {percentage}%; background: {color};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_status_badge(status, text):
    """Create a professional status badge"""
    
    status_colors = {
        "success": "#10b981",
        "warning": "#f59e0b", 
        "error": "#ef4444",
        "info": "#3b82f6"
    }
    
    color = status_colors.get(status, "#64748b")
    
    st.markdown(f"""
    <span style="
        background: {color}15;
        color: {color};
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 600;
        border: 1px solid {color}25;
    ">{text}</span>
    """, unsafe_allow_html=True)

def add_construction_animations():
    """Add subtle animations for construction dashboard elements"""
    
    st.markdown("""
    <script>
    // Add smooth scrolling
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Add intersection observer for animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-slide-in');
            }
        });
    });
    
    // Observe all cards
    setTimeout(() => {
        document.querySelectorAll('.module-card').forEach(card => {
            observer.observe(card);
        });
    }, 100);
    
    // Add click animations to buttons
    document.addEventListener('click', (e) => {
        if (e.target.tagName === 'BUTTON') {
            e.target.style.transform = 'scale(0.98)';
            setTimeout(() => {
                e.target.style.transform = '';
            }, 150);
        }
    });
    </script>
    """, unsafe_allow_html=True)