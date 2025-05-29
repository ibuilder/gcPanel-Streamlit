"""
Theme Management for gcPanel
Centralized styling and theme control for consistent UI
"""

import streamlit as st

class ThemeManager:
    """Manages application themes and styling"""
    
    def __init__(self):
        self.themes = {
            "dark": self._get_dark_theme(),
            "light": self._get_light_theme()
        }
    
    def _get_dark_theme(self) -> str:
        """Professional dark theme with Highland Tower branding"""
        return """
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
            background: linear-gradient(135deg, #0ea5e9, #38bdf8) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            margin: 4px 0 !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }
        
        section[data-testid="stSidebar"] button:hover {
            background: linear-gradient(135deg, #0284c7, #0ea5e9) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3) !important;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #0ea5e9, #38bdf8);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #0284c7, #0ea5e9);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
        }
        
        .project-info {
            background: linear-gradient(135deg, #1e40af, #3b82f6);
            padding: 1rem;
            border-radius: 12px;
            margin: 1rem 0;
            border: 1px solid #60a5fa;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #1e293b, #334155);
            border: 1px solid #475569;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 0.5rem 0;
        }
        
        .status-active {
            color: #10b981;
            font-weight: 600;
        }
        
        .loading-spinner {
            border: 3px solid #1e293b;
            border-top: 3px solid #0ea5e9;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        """
    
    def _get_light_theme(self) -> str:
        """Professional light theme"""
        return """
        <style>
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            color: #1e293b;
        }
        
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%) !important;
            border-right: 2px solid #3b82f6;
        }
        
        section[data-testid="stSidebar"] * {
            color: #1e293b !important;
        }
        
        section[data-testid="stSidebar"] button {
            background: linear-gradient(135deg, #3b82f6, #60a5fa) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            margin: 4px 0 !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }
        
        section[data-testid="stSidebar"] button:hover {
            background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #60a5fa);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #2563eb, #3b82f6);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        .project-info {
            background: linear-gradient(135deg, #3b82f6, #60a5fa);
            color: white;
            padding: 1rem;
            border-radius: 12px;
            margin: 1rem 0;
            border: 1px solid #93c5fd;
        }
        
        .metric-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        .status-active {
            color: #059669;
            font-weight: 600;
        }
        </style>
        """
    
    def apply_current_theme(self):
        """Apply the current theme from session state"""
        current_theme = st.session_state.get("theme", "dark")
        if current_theme in self.themes:
            st.markdown(self.themes[current_theme], unsafe_allow_html=True)
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        current_theme = st.session_state.get("theme", "dark")
        new_theme = "light" if current_theme == "dark" else "dark"
        st.session_state.theme = new_theme
        st.rerun()
    
    def get_theme_button_text(self) -> str:
        """Get appropriate theme toggle button text"""
        current_theme = st.session_state.get("theme", "dark")
        return "☀️ Light Mode" if current_theme == "dark" else "🌙 Dark Mode"