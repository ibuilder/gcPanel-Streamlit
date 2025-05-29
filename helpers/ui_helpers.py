"""
UI Helpers for gcPanel MVC Architecture
Provides reusable UI components and styling functions
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def apply_highland_tower_styling():
    """Apply Highland Tower Development styling to the page"""
    st.markdown("""
    <style>
    /* Highland Tower Professional Styling */
    .main > div {
        padding-top: 2rem;
    }
    
    .stSidebar > div:first-child {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
        color: white;
    }
    
    .stSidebar .element-container {
        color: white;
    }
    
    .stButton > button {
        background-color: #1e40af;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #1d4ed8;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #1e40af;
        margin-bottom: 1rem;
    }
    
    .highland-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
        display: inline-block;
    }
    
    .status-active {
        background-color: #dcfce7;
        color: #166534;
    }
    
    .status-pending {
        background-color: #fef3c7;
        color: #92400e;
    }
    
    .status-completed {
        background-color: #dbeafe;
        color: #1e40af;
    }
    
    .data-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .data-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .section-divider {
        border-top: 2px solid #e5e7eb;
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def render_highland_header(title: str, subtitle: str = ""):
    """Render Highland Tower Development header"""
    st.markdown(f"""
    <div class="highland-header">
        <h1>{title}</h1>
        <p style="margin: 0; opacity: 0.9; font-size: 1.1rem;">{subtitle}</p>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.8; font-size: 0.9rem;">Highland Tower Development - $45.5M Mixed-Use Project</p>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, delta: str = "", delta_color: str = "normal"):
    """Render a professional metric card"""
    delta_html = ""
    if delta:
        delta_class = f"delta-{delta_color}"
        delta_html = f'<div class="{delta_class}" style="font-size: 0.875rem; margin-top: 0.5rem;">{delta}</div>'
    
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin: 0; color: #374151; font-size: 0.875rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;">{title}</h3>
        <div style="font-size: 2rem; font-weight: 700; color: #1f2937; margin: 0.5rem 0;">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def render_status_badge(status: str):
    """Render a status badge with appropriate styling"""
    status_lower = status.lower()
    
    if status_lower in ['active', 'open', 'in progress', 'ongoing']:
        badge_class = "status-active"
    elif status_lower in ['pending', 'under review', 'waiting']:
        badge_class = "status-pending"
    elif status_lower in ['completed', 'closed', 'done', 'finished']:
        badge_class = "status-completed"
    else:
        badge_class = "status-pending"
    
    return f'<span class="status-badge {badge_class}">{status}</span>'

def render_data_card(data: Dict[str, Any], title_field: str = "title", key_fields: List[str] = None, actions: List[Dict] = None):
    """Render a data card with actions"""
    if key_fields is None:
        key_fields = ['id', 'status']
    
    title = data.get(title_field, f"Record {data.get('id', 'Unknown')}")
    
    card_html = f'<div class="data-card">'
    card_html += f'<h4 style="margin: 0 0 0.5rem 0; color: #1f2937;">{title}</h4>'
    
    # Key fields
    key_info = []
    for field in key_fields:
        if field in data and data[field] is not None:
            value = data[field]
            if field == 'status':
                value = render_status_badge(str(value))
            key_info.append(f"<strong>{field.replace('_', ' ').title()}:</strong> {value}")
    
    if key_info:
        card_html += f'<p style="margin: 0.5rem 0; color: #6b7280;">{" | ".join(key_info)}</p>'
    
    card_html += '</div>'
    
    st.markdown(card_html, unsafe_allow_html=True)

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency with proper symbols and thousands separators"""
    if currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "EUR":
        return f"€{amount:,.2f}"
    elif currency == "GBP":
        return f"£{amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"

def format_date(date_value: Any) -> str:
    """Format date consistently across the application"""
    if date_value is None:
        return "N/A"
    
    if isinstance(date_value, str):
        try:
            date_obj = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
            return date_obj.strftime("%B %d, %Y")
        except:
            return date_value
    elif isinstance(date_value, datetime):
        return date_value.strftime("%B %d, %Y")
    else:
        return str(date_value)

def format_percentage(value: float, decimals: int = 1) -> str:
    """Format percentage values consistently"""
    return f"{value:.{decimals}f}%"

def clean_dataframe_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """Clean DataFrame to prevent Arrow serialization errors"""
    if df.empty:
        return df
    
    cleaned_df = df.copy()
    
    # Convert all object columns to string
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype == 'object':
            cleaned_df[col] = cleaned_df[col].astype(str)
    
    # Handle NaN values
    cleaned_df = cleaned_df.fillna('')
    
    return cleaned_df

def render_progress_bar(current: float, total: float, label: str = "", color: str = "#1e40af"):
    """Render a custom progress bar"""
    percentage = (current / total * 100) if total > 0 else 0
    
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: 500; color: #374151;">{label}</span>
            <span style="color: #6b7280;">{current:,.0f} / {total:,.0f} ({percentage:.1f}%)</span>
        </div>
        <div style="background-color: #f3f4f6; border-radius: 9999px; height: 8px; overflow: hidden;">
            <div style="background-color: {color}; height: 100%; width: {percentage}%; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_dashboard(kpis: List[Dict[str, Any]]):
    """Render a KPI dashboard with multiple metrics"""
    cols = st.columns(len(kpis))
    
    for i, kpi in enumerate(kpis):
        with cols[i]:
            title = kpi.get('title', 'Metric')
            value = kpi.get('value', '0')
            delta = kpi.get('delta', '')
            delta_color = kpi.get('delta_color', 'normal')
            
            render_metric_card(title, value, delta, delta_color)

def render_alert(message: str, alert_type: str = "info", dismissible: bool = False):
    """Render custom alert messages"""
    color_map = {
        "info": "#3b82f6",
        "success": "#10b981", 
        "warning": "#f59e0b",
        "error": "#ef4444"
    }
    
    bg_color_map = {
        "info": "#eff6ff",
        "success": "#f0fdf4",
        "warning": "#fffbeb", 
        "error": "#fef2f2"
    }
    
    color = color_map.get(alert_type, color_map["info"])
    bg_color = bg_color_map.get(alert_type, bg_color_map["info"])
    
    dismiss_button = ""
    if dismissible:
        dismiss_button = '<button onclick="this.parentElement.style.display=\'none\'" style="background: none; border: none; float: right; cursor: pointer; font-size: 1.2rem; color: #6b7280;">&times;</button>'
    
    st.markdown(f"""
    <div style="background-color: {bg_color}; border-left: 4px solid {color}; padding: 1rem; border-radius: 4px; margin: 1rem 0;">
        {dismiss_button}
        <div style="color: #1f2937; font-weight: 500;">{message}</div>
    </div>
    """, unsafe_allow_html=True)

def render_timeline_item(date: str, title: str, description: str, status: str = "completed"):
    """Render a timeline item for project milestones"""
    status_colors = {
        "completed": "#10b981",
        "in_progress": "#3b82f6", 
        "pending": "#f59e0b",
        "cancelled": "#ef4444"
    }
    
    color = status_colors.get(status, status_colors["pending"])
    
    st.markdown(f"""
    <div style="display: flex; margin-bottom: 1.5rem;">
        <div style="flex-shrink: 0; width: 12px; height: 12px; background-color: {color}; border-radius: 50%; margin-right: 1rem; margin-top: 0.25rem;"></div>
        <div style="flex-grow: 1;">
            <div style="font-weight: 600; color: #1f2937; margin-bottom: 0.25rem;">{title}</div>
            <div style="font-size: 0.875rem; color: #6b7280; margin-bottom: 0.25rem;">{date}</div>
            <div style="color: #4b5563;">{description}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_breadcrumbs(items: List[Dict[str, str]], current: str):
    """Render breadcrumb navigation"""
    breadcrumb_html = '<nav style="margin-bottom: 2rem;">'
    
    for i, item in enumerate(items):
        if i > 0:
            breadcrumb_html += ' <span style="color: #6b7280; margin: 0 0.5rem;">></span> '
        
        if i == len(items) - 1:
            breadcrumb_html += f'<span style="color: #1f2937; font-weight: 500;">{current}</span>'
        else:
            breadcrumb_html += f'<a href="{item.get("url", "#")}" style="color: #3b82f6; text-decoration: none;">{item.get("label", "")}</a>'
    
    breadcrumb_html += '</nav>'
    
    st.markdown(breadcrumb_html, unsafe_allow_html=True)

def render_stats_grid(stats: List[Dict[str, Any]], columns: int = 4):
    """Render a grid of statistics"""
    cols = st.columns(columns)
    
    for i, stat in enumerate(stats):
        col_index = i % columns
        with cols[col_index]:
            icon = stat.get('icon', '📊')
            title = stat.get('title', 'Statistic')
            value = stat.get('value', '0')
            change = stat.get('change', '')
            
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 8px; border: 1px solid #e5e7eb; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-size: 2rem; font-weight: 700; color: #1f2937; margin-bottom: 0.25rem;">{value}</div>
                <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.25rem;">{title}</div>
                {f'<div style="color: #10b981; font-size: 0.75rem; font-weight: 500;">{change}</div>' if change else ''}
            </div>
            """, unsafe_allow_html=True)

def initialize_session_state(key: str, default_value: Any):
    """Initialize session state with default value if not exists"""
    if key not in st.session_state:
        st.session_state[key] = default_value
    return st.session_state[key]

def clear_session_cache():
    """Clear all cached session data"""
    for key in list(st.session_state.keys()):
        if key.endswith('_data') or key.startswith('cache_'):
            del st.session_state[key]

def export_dataframe_to_csv(df: pd.DataFrame, filename: str = "export.csv"):
    """Export DataFrame to CSV for download"""
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )

def render_loading_spinner(message: str = "Loading..."):
    """Render a loading spinner with message"""
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <div style="display: inline-block; width: 40px; height: 40px; border: 4px solid #f3f4f6; border-top: 4px solid #3b82f6; border-radius: 50%; animation: spin 1s linear infinite;"></div>
        <div style="margin-top: 1rem; color: #6b7280;">{message}</div>
    </div>
    <style>
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """, unsafe_allow_html=True)