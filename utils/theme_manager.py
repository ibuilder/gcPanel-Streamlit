"""
Theme management for gcPanel.

This module provides a centralized theme management system with
support for light and dark modes, along with customizable colors.
"""

import streamlit as st
import os

# Theme options
THEMES = {
    "light": {
        "primary_color": "#3367D6",
        "secondary_color": "#28a745",
        "background_color": "#FFFFFF",
        "text_color": "#333333",
        "accent_color": "#f9c851",
        "error_color": "#dc3545",
        "success_color": "#28a745",
        "warning_color": "#ffc107",
        "info_color": "#17a2b8",
    },
    "dark": {
        "primary_color": "#3367D6",
        "secondary_color": "#28a745",
        "background_color": "#121212",
        "text_color": "#E1E1E1",
        "accent_color": "#f9c851",
        "error_color": "#ef5350",
        "success_color": "#4caf50",
        "warning_color": "#ffca28",
        "info_color": "#29b6f6",
    },
    "blue": {
        "primary_color": "#1976D2",
        "secondary_color": "#26A69A",
        "background_color": "#F5F7FA",
        "text_color": "#37474F",
        "accent_color": "#FF9800",
        "error_color": "#E53935",
        "success_color": "#43A047",
        "warning_color": "#FDD835",
        "info_color": "#039BE5",
    },
    "dark_blue": {
        "primary_color": "#1976D2",
        "secondary_color": "#26A69A",
        "background_color": "#0A1929",
        "text_color": "#E1E1E1",
        "accent_color": "#FF9800",
        "error_color": "#EF5350",
        "success_color": "#66BB6A",
        "warning_color": "#FFEE58",
        "info_color": "#4FC3F7",
    }
}

def initialize_theme():
    """Initialize theme in session state if not already present."""
    if "theme" not in st.session_state:
        # Try to get system preference
        st.session_state.theme = "light"
        
        # Or use environment variable if set
        env_theme = os.environ.get("GCPANEL_THEME")
        if env_theme and env_theme in THEMES:
            st.session_state.theme = env_theme

def get_current_theme():
    """Get the current theme name."""
    initialize_theme()
    return st.session_state.theme

def get_theme_colors():
    """Get all colors for current theme."""
    theme_name = get_current_theme()
    return THEMES.get(theme_name, THEMES["light"])

def get_color(color_name):
    """Get a specific color from the current theme."""
    colors = get_theme_colors()
    return colors.get(color_name, "#000000")
    
def toggle_theme():
    """Toggle between light and dark themes."""
    initialize_theme()
    if st.session_state.theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"
    return st.session_state.theme

def set_theme(theme_name):
    """Set a specific theme."""
    if theme_name in THEMES:
        st.session_state.theme = theme_name
        return True
    return False

def apply_theme():
    """Apply the current theme using Streamlit custom CSS."""
    colors = get_theme_colors()
    
    # Create theme CSS
    theme_css = f"""
    <style>
        :root {{
            --primary-color: {colors['primary_color']};
            --secondary-color: {colors['secondary_color']};
            --background-color: {colors['background_color']};
            --text-color: {colors['text_color']};
            --accent-color: {colors['accent_color']};
            --error-color: {colors['error_color']};
            --success-color: {colors['success_color']};
            --warning-color: {colors['warning_color']};
            --info-color: {colors['info_color']};
        }}
        
        /* Apply theme variables */
        body {{
            background-color: var(--background-color);
            color: var(--text-color);
        }}
        
        .stApp {{
            background-color: var(--background-color);
        }}
        
        .stButton button {{
            background-color: var(--primary-color);
            color: white;
        }}
        
        .stTextInput input {{
            border-color: var(--primary-color);
        }}
        
        /* Additional theme-specific styling */
        .dashboard-card {{
            background-color: {'rgba(0, 0, 0, 0.1)' if 'dark' in st.session_state.theme else 'rgba(255, 255, 255, 0.8)'};
            box-shadow: 0 4px 6px {'rgba(0, 0, 0, 0.3)' if 'dark' in st.session_state.theme else 'rgba(0, 0, 0, 0.1)'};
        }}
        
        /* Style tweaks for dark mode */
        .stMarkdown {{
            color: var(--text-color);
        }}
    </style>
    """
    
    # Apply CSS
    st.markdown(theme_css, unsafe_allow_html=True)

def render_theme_selector():
    """Render a theme selection widget."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_theme = st.selectbox(
            "Select Theme",
            options=list(THEMES.keys()),
            index=list(THEMES.keys()).index(get_current_theme())
        )
    
    with col2:
        if st.button("Apply Theme"):
            set_theme(selected_theme)
            st.rerun()
    
    # Show theme preview
    st.markdown(f"**Preview of {selected_theme.title()} Theme**")
    
    colors = THEMES[selected_theme]
    preview_html = f"""
    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
    """
    
    for color_name, color_value in colors.items():
        preview_html += f"""
        <div style="text-align: center;">
            <div style="width: 80px; height: 40px; background-color: {color_value}; 
                     border-radius: 4px; margin-bottom: 4px;"></div>
            <div style="font-size: 0.8rem;">{color_name}</div>
        </div>
        """
    
    preview_html += "</div>"
    st.markdown(preview_html, unsafe_allow_html=True)