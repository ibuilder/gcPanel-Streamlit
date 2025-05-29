"""
Adaptive Theme Manager for gcPanel.

This module provides role-based theming capabilities that automatically
adapt the application's visual appearance based on the user's role and
permissions. Each role gets a unique color scheme and visual emphasis.
"""

import streamlit as st


# Role-based theme configurations
ROLE_THEMES = {
    "Project Manager": {
        "primary_color": "#2E86AB",  # Professional blue
        "secondary_color": "#A23B72", # Accent purple
        "background_gradient": "linear-gradient(135deg, #2E86AB 0%, #A23B72 100%)",
        "accent_color": "#F18F01",  # Orange highlights
        "text_primary": "#2C3E50",
        "text_secondary": "#6C757D",
        "sidebar_bg": "#E8F4F8",
        "card_bg": "#FFFFFF",
        "border_color": "#2E86AB",
        "success_color": "#28A745",
        "warning_color": "#FFC107",
        "danger_color": "#DC3545",
        "theme_name": "Executive Blue"
    },
    "Superintendent": {
        "primary_color": "#FF6B35",  # Construction orange
        "secondary_color": "#F7931E", # Safety orange
        "background_gradient": "linear-gradient(135deg, #FF6B35 0%, #F7931E 100%)",
        "accent_color": "#004E89",  # Navy blue
        "text_primary": "#2C3E50",
        "text_secondary": "#6C757D",
        "sidebar_bg": "#FFF3E0",
        "card_bg": "#FFFFFF",
        "border_color": "#FF6B35",
        "success_color": "#28A745",
        "warning_color": "#FFC107",
        "danger_color": "#DC3545",
        "theme_name": "Field Operations"
    },
    "Safety Manager": {
        "primary_color": "#28A745",  # Safety green
        "secondary_color": "#20C997", # Teal
        "background_gradient": "linear-gradient(135deg, #28A745 0%, #20C997 100%)",
        "accent_color": "#FFC107",  # Warning yellow
        "text_primary": "#2C3E50",
        "text_secondary": "#6C757D",
        "sidebar_bg": "#E8F5E8",
        "card_bg": "#FFFFFF",
        "border_color": "#28A745",
        "success_color": "#28A745",
        "warning_color": "#FFC107",
        "danger_color": "#DC3545",
        "theme_name": "Safety First"
    },
    "Cost Manager": {
        "primary_color": "#6F42C1",  # Financial purple
        "secondary_color": "#E83E8C", # Analytics pink
        "background_gradient": "linear-gradient(135deg, #6F42C1 0%, #E83E8C 100%)",
        "accent_color": "#FD7E14",  # Data orange
        "text_primary": "#2C3E50",
        "text_secondary": "#6C757D",
        "sidebar_bg": "#F4F0FF",
        "card_bg": "#FFFFFF",
        "border_color": "#6F42C1",
        "success_color": "#28A745",
        "warning_color": "#FFC107",
        "danger_color": "#DC3545",
        "theme_name": "Financial Focus"
    },
    "Quality Manager": {
        "primary_color": "#17A2B8",  # Quality teal
        "secondary_color": "#6610F2", # Inspection purple
        "background_gradient": "linear-gradient(135deg, #17A2B8 0%, #6610F2 100%)",
        "accent_color": "#FD7E14",  # Quality orange
        "text_primary": "#2C3E50",
        "text_secondary": "#6C757D",
        "sidebar_bg": "#E0F7FA",
        "card_bg": "#FFFFFF",
        "border_color": "#17A2B8",
        "success_color": "#28A745",
        "warning_color": "#FFC107",
        "danger_color": "#DC3545",
        "theme_name": "Quality Assurance"
    },
    "Engineer": {
        "primary_color": "#495057",  # Engineering gray
        "secondary_color": "#6C757D", # Technical silver
        "background_gradient": "linear-gradient(135deg, #495057 0%, #6C757D 100%)",
        "accent_color": "#007BFF",  # Technical blue
        "text_primary": "#2C3E50",
        "text_secondary": "#6C757D",
        "sidebar_bg": "#F8F9FA",
        "card_bg": "#FFFFFF",
        "border_color": "#495057",
        "success_color": "#28A745",
        "warning_color": "#FFC107",
        "danger_color": "#DC3545",
        "theme_name": "Engineering Precision"
    },
    "Admin": {
        "primary_color": "#343A40",  # Admin dark
        "secondary_color": "#6C757D", # System gray
        "background_gradient": "linear-gradient(135deg, #343A40 0%, #6C757D 100%)",
        "accent_color": "#DC3545",  # Admin red
        "text_primary": "#2C3E50",
        "text_secondary": "#6C757D",
        "sidebar_bg": "#F8F9FA",
        "card_bg": "#FFFFFF",
        "border_color": "#343A40",
        "success_color": "#28A745",
        "warning_color": "#FFC107",
        "danger_color": "#DC3545",
        "theme_name": "System Admin"
    }
}

# Default theme for unknown roles
DEFAULT_THEME = {
    "primary_color": "#667eea",
    "secondary_color": "#764ba2",
    "background_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "accent_color": "#F18F01",
    "text_primary": "#2C3E50",
    "text_secondary": "#6C757D",
    "sidebar_bg": "#F8F9FA",
    "card_bg": "#FFFFFF",
    "border_color": "#667eea",
    "success_color": "#28A745",
    "warning_color": "#FFC107",
    "danger_color": "#DC3545",
    "theme_name": "Default"
}


def get_user_theme():
    """
    Get the theme configuration for the current user based on their role.
    
    Returns:
        dict: Theme configuration dictionary
    """
    user_role = st.session_state.get('user_role', 'Guest')
    return ROLE_THEMES.get(user_role, DEFAULT_THEME)


def apply_role_based_theme():
    """
    Apply the role-based theme to the application.
    
    This function injects CSS that adapts the application's appearance
    based on the user's role and permissions.
    """
    theme = get_user_theme()
    
    # Enhanced CSS with role-based theming
    theme_css = f"""
    <style>
    /* Root variables for consistent theming */
    :root {{
        --primary-color: {theme['primary_color']};
        --secondary-color: {theme['secondary_color']};
        --accent-color: {theme['accent_color']};
        --text-primary: {theme['text_primary']};
        --text-secondary: {theme['text_secondary']};
        --sidebar-bg: {theme['sidebar_bg']};
        --card-bg: {theme['card_bg']};
        --border-color: {theme['border_color']};
        --success-color: {theme['success_color']};
        --warning-color: {theme['warning_color']};
        --danger-color: {theme['danger_color']};
    }}
    
    /* Main container theming */
    .main .block-container {{
        background: {theme['background_gradient']};
        border-radius: 15px;
        margin-top: 1rem;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}
    
    /* Header theming */
    .stApp > header {{
        background: transparent;
    }}
    
    /* Sidebar theming */
    .css-1d391kg {{
        background: {theme['sidebar_bg']} !important;
        border-right: 3px solid {theme['primary_color']} !important;
    }}
    
    .css-1d391kg .css-6qob1r {{
        background: {theme['sidebar_bg']} !important;
    }}
    
    /* Navigation menu theming */
    .css-1d391kg .css-6qob1r .stSelectbox > div > div {{
        background: {theme['card_bg']} !important;
        border: 2px solid {theme['primary_color']} !important;
        border-radius: 8px !important;
    }}
    
    /* Button theming */
    .stButton > button {{
        background: {theme['primary_color']} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover {{
        background: {theme['secondary_color']} !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }}
    
    /* Secondary button styling */
    .stButton > button[kind="secondary"] {{
        background: transparent !important;
        color: {theme['primary_color']} !important;
        border: 2px solid {theme['primary_color']} !important;
    }}
    
    .stButton > button[kind="secondary"]:hover {{
        background: {theme['primary_color']} !important;
        color: white !important;
    }}
    
    /* Metric cards theming */
    .css-1r6slb0 {{
        background: {theme['card_bg']} !important;
        border: 2px solid {theme['primary_color']} !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1) !important;
    }}
    
    /* Input field theming */
    .stTextInput > div > div > input {{
        border: 2px solid {theme['primary_color']} !important;
        border-radius: 8px !important;
        background: {theme['card_bg']} !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {theme['accent_color']} !important;
        box-shadow: 0 0 0 3px rgba(241, 143, 1, 0.2) !important;
    }}
    
    /* Selectbox theming */
    .stSelectbox > div > div {{
        border: 2px solid {theme['primary_color']} !important;
        border-radius: 8px !important;
        background: {theme['card_bg']} !important;
    }}
    
    /* Tab theming */
    .stTabs [data-baseweb="tab-list"] {{
        background: {theme['card_bg']} !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: {theme['text_secondary']} !important;
        background: transparent !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {theme['primary_color']} !important;
        color: white !important;
    }}
    
    /* Alert theming */
    .stAlert {{
        border-radius: 8px !important;
        border-left: 4px solid {theme['primary_color']} !important;
    }}
    
    /* Success alerts */
    .stSuccess {{
        border-left-color: {theme['success_color']} !important;
        background: rgba(40, 167, 69, 0.1) !important;
    }}
    
    /* Warning alerts */
    .stWarning {{
        border-left-color: {theme['warning_color']} !important;
        background: rgba(255, 193, 7, 0.1) !important;
    }}
    
    /* Error alerts */
    .stError {{
        border-left-color: {theme['danger_color']} !important;
        background: rgba(220, 53, 69, 0.1) !important;
    }}
    
    /* Info alerts */
    .stInfo {{
        border-left-color: {theme['primary_color']} !important;
        background: rgba(46, 134, 171, 0.1) !important;
    }}
    
    /* Expander theming */
    .streamlit-expanderHeader {{
        background: {theme['card_bg']} !important;
        border: 2px solid {theme['primary_color']} !important;
        border-radius: 8px !important;
        color: {theme['text_primary']} !important;
        font-weight: 600 !important;
    }}
    
    /* Table theming */
    .stDataFrame {{
        border: 2px solid {theme['primary_color']} !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }}
    
    /* Progress bar theming */
    .stProgress > div > div > div {{
        background: {theme['primary_color']} !important;
    }}
    
    /* Checkbox theming */
    .stCheckbox > label > div:first-child {{
        border: 2px solid {theme['primary_color']} !important;
        border-radius: 4px !important;
    }}
    
    /* Radio button theming */
    .stRadio > div > label > div:first-child {{
        border: 2px solid {theme['primary_color']} !important;
    }}
    
    /* Custom role indicator */
    .role-theme-indicator {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        background: {theme['primary_color']};
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        z-index: 1000;
    }}
    
    /* Animated gradient background for role cards */
    .role-card {{
        background: {theme['background_gradient']};
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }}
    
    .role-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.2);
    }}
    
    /* Custom scrollbar theming */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {theme['sidebar_bg']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {theme['primary_color']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {theme['secondary_color']};
    }}
    </style>
    """
    
    st.markdown(theme_css, unsafe_allow_html=True)


def show_theme_indicator():
    """
    Display a theme indicator showing the current user's role and theme.
    """
    theme = get_user_theme()
    user_role = st.session_state.get('user_role', 'Guest')
    
    st.markdown(f"""
    <div class="role-theme-indicator">
        🎨 {theme['theme_name']} Theme • {user_role}
    </div>
    """, unsafe_allow_html=True)


def create_role_themed_card(title, content, icon="📋"):
    """
    Create a card with role-based theming.
    
    Args:
        title (str): Card title
        content (str): Card content
        icon (str): Card icon
    """
    theme = get_user_theme()
    
    st.markdown(f"""
    <div class="role-card">
        <h3 style="margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.5rem;">{icon}</span>
            {title}
        </h3>
        <p style="margin: 0; opacity: 0.9;">
            {content}
        </p>
    </div>
    """, unsafe_allow_html=True)


def get_role_icon(role):
    """
    Get the appropriate icon for a user role.
    
    Args:
        role (str): User role
        
    Returns:
        str: Unicode icon for the role
    """
    role_icons = {
        "Project Manager": "👔",
        "Superintendent": "🏗️",
        "Safety Manager": "🦺",
        "Cost Manager": "💰",
        "Quality Manager": "✅",
        "Engineer": "⚙️",
        "Admin": "🔧"
    }
    return role_icons.get(role, "👤")


def apply_role_specific_layout_adjustments():
    """
    Apply role-specific layout adjustments and emphasis.
    """
    user_role = st.session_state.get('user_role', 'Guest')
    
    # Role-specific layout modifications
    role_layouts = {
        "Safety Manager": {
            "emphasis": "safety",
            "highlight_color": "#FFC107",
            "priority_modules": ["Safety", "Incidents", "Training"]
        },
        "Cost Manager": {
            "emphasis": "financial",
            "highlight_color": "#28A745",
            "priority_modules": ["Cost Management", "Budget", "Invoicing"]
        },
        "Superintendent": {
            "emphasis": "operations",
            "highlight_color": "#FF6B35",
            "priority_modules": ["Field Operations", "Daily Reports", "Schedule"]
        }
    }
    
    layout = role_layouts.get(user_role, {})
    
    if layout:
        highlight_css = f"""
        <style>
        /* Priority module highlighting for {user_role} */
        .priority-module {{
            border-left: 4px solid {layout['highlight_color']} !important;
            background: linear-gradient(90deg, rgba(255,255,255,0.1) 0%, transparent 100%) !important;
        }}
        </style>
        """
        st.markdown(highlight_css, unsafe_allow_html=True)