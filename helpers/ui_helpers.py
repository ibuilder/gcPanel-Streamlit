"""
UI Helpers for gcPanel Construction Management Platform
Common UI components and utilities
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional

def clean_dataframe_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """Clean DataFrame to prevent Arrow serialization errors"""
    if df.empty:
        return df
    
    cleaned_df = df.copy()
    
    # Convert any problematic data types
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype == 'object':
            cleaned_df[col] = cleaned_df[col].astype(str)
    
    return cleaned_df

def render_metric_cards(metrics: List[Dict[str, Any]]):
    """Render metric cards in columns"""
    if not metrics:
        return
    
    cols = st.columns(len(metrics))
    
    for i, metric in enumerate(metrics):
        with cols[i]:
            st.metric(
                label=metric['label'],
                value=metric['value'],
                delta=metric.get('delta'),
                help=metric.get('help')
            )

def render_status_badge(status: str) -> str:
    """Render a colored status badge"""
    status_colors = {
        'Active': '🟢',
        'Completed': '🔵', 
        'In Progress': '🟡',
        'Pending': '🟠',
        'Cancelled': '🔴',
        'Draft': '⚪',
        'Under Review': '🟡',
        'Approved': '🟢',
        'Rejected': '🔴',
        'High': '🔴',
        'Medium': '🟡',
        'Low': '🟢',
        'Critical': '🔴'
    }
    
    color = status_colors.get(status, '⚫')
    return f"{color} {status}"

def format_currency(amount: float) -> str:
    """Format number as currency"""
    return f"${amount:,.2f}"

def format_percentage(value: float) -> str:
    """Format number as percentage"""
    return f"{value:.1f}%"

def render_search_filters(search_config: Dict[str, Any], key_prefix: str) -> Dict[str, Any]:
    """Render search and filter controls"""
    filters = {}
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'search' in search_config:
            filters['search_term'] = st.text_input(
                search_config['search']['label'],
                placeholder=search_config['search'].get('placeholder', ''),
                key=f"{key_prefix}_search"
            )
    
    with col2:
        if 'filter1' in search_config:
            filter_config = search_config['filter1']
            filters['filter1_value'] = st.selectbox(
                filter_config['label'],
                filter_config['options'],
                key=f"{key_prefix}_filter1"
            )
    
    with col3:
        if 'filter2' in search_config:
            filter_config = search_config['filter2']
            filters['filter2_value'] = st.selectbox(
                filter_config['label'],
                filter_config['options'],
                key=f"{key_prefix}_filter2"
            )
    
    return filters

def render_action_buttons(record_id: str, module_name: str, actions: List[str] = None) -> Dict[str, bool]:
    """Render action buttons for CRUD operations"""
    if actions is None:
        actions = ['view', 'edit', 'delete']
    
    button_states = {}
    
    for action in actions:
        if action == 'view':
            button_states['view'] = st.button(
                "👁️ View",
                key=f"view_{module_name}_{record_id}",
                help="View details"
            )
        elif action == 'edit':
            button_states['edit'] = st.button(
                "✏️ Edit",
                key=f"edit_{module_name}_{record_id}",
                help="Edit record"
            )
        elif action == 'delete':
            button_states['delete'] = st.button(
                "🗑️ Delete",
                key=f"delete_{module_name}_{record_id}",
                help="Delete record",
                type="secondary"
            )
    
    return button_states

def show_success_message(message: str):
    """Show success message"""
    st.success(message)

def show_error_message(message: str):
    """Show error message"""
    st.error(message)

def show_info_message(message: str):
    """Show info message"""
    st.info(message)

def show_warning_message(message: str):
    """Show warning message"""
    st.warning(message)

def render_progress_bar(progress: float, label: str = "Progress"):
    """Render progress bar"""
    st.progress(progress / 100.0, text=f"{label}: {progress:.1f}%")

def render_tabs(tab_config: List[Dict[str, str]], key_prefix: str = "tabs"):
    """Render tabs and return selected tab"""
    tab_labels = [tab['label'] for tab in tab_config]
    return st.tabs(tab_labels)

def render_expander_card(title: str, content: Dict[str, Any], expanded: bool = False):
    """Render an expandable card with content"""
    with st.expander(title, expanded=expanded):
        col1, col2 = st.columns(2)
        
        fields = list(content.items())
        mid_point = len(fields) // 2
        
        with col1:
            for key, value in fields[:mid_point]:
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        with col2:
            for key, value in fields[mid_point:]:
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")

def render_data_table(df: pd.DataFrame, column_config: Dict[str, Any] = None):
    """Render a data table with optional column configuration"""
    if df.empty:
        st.info("No data available")
        return
    
    st.dataframe(
        clean_dataframe_for_display(df),
        column_config=column_config or {},
        hide_index=True,
        use_container_width=True
    )

def apply_highland_tower_styling():
    """Apply Highland Tower Development branded styling"""
    st.markdown("""
    <style>
    .highland-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        margin-bottom: 1rem;
    }
    
    .highland-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .highland-metric {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 1rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

def render_highland_header(title: str, subtitle: str = "Highland Tower Development - $45.5M Mixed-Use Project"):
    """Render Highland Tower Development branded header"""
    st.markdown(f"""
    <div class="highland-header">
        <h2 style="margin: 0; color: white;">{title}</h2>
        <p style="margin: 0; opacity: 0.9; color: white;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)