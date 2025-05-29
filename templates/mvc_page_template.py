"""
MVC Page Template for gcPanel Construction Management Platform
Standard template for all construction module pages
"""

import streamlit as st
import sys
import os
from typing import Dict, Any

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def create_mvc_page(
    page_title: str,
    page_icon: str, 
    model_class,
    display_config: Dict[str, Any],
    form_config: Dict[str, Any] = None,
    highland_data: list = None
):
    """
    Create a standardized MVC page for construction modules
    
    Args:
        page_title: Page title for browser tab
        page_icon: Emoji icon for the page
        model_class: Model class for data operations
        display_config: Configuration for data display
        form_config: Configuration for forms (optional)
        highland_data: Highland Tower project data to initialize if empty (optional)
    """
    
    # Page configuration
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")
    
    # Import with error handling
    try:
        from controllers.crud_controller import CRUDController
        from helpers.ui_helpers import apply_highland_tower_styling, render_highland_header
        mvc_available = True
    except ImportError:
        mvc_available = False
    
    # Apply styling if available
    if mvc_available:
        apply_highland_tower_styling()
        render_highland_header(
            display_config.get('title', 'Module'),
            f"Highland Tower Development - {display_config.get('subtitle', 'Construction Management')}"
        )
    else:
        st.title(f"{page_icon} {display_config.get('title', 'Module')}")
        st.markdown(f"Highland Tower Development - {display_config.get('subtitle', 'Construction Management')}")
        st.markdown("---")
    
    # Initialize model and controller
    if mvc_available:
        try:
            model = model_class()
            session_key = model.session_key
            controller = CRUDController(model, session_key, display_config)
            
            # Initialize with Highland Tower data if provided and empty
            if highland_data and not model.get_all():
                for item in highland_data:
                    model.create(item)
            
        except Exception as e:
            st.error(f"Failed to initialize MVC components: {e}")
            mvc_available = False
    
    # Fallback session state initialization
    if not mvc_available:
        session_key = display_config.get('session_key', 'module_data')
        if session_key not in st.session_state:
            st.session_state[session_key] = highland_data or []
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs([
        f"📊 {display_config.get('item_name', 'Records')} Database",
        f"📝 Create {display_config.get('item_name', 'Record')}",
        "📈 Analytics"
    ])
    
    with tab1:
        if mvc_available:
            controller.render_data_view(session_key)
        else:
            render_fallback_data_view(session_key, display_config)
    
    with tab2:
        if mvc_available:
            controller.render_create_form(form_config or {}, session_key)
        else:
            render_fallback_create_form(session_key, display_config, form_config)
    
    with tab3:
        if mvc_available:
            controller.render_analytics(session_key)
        else:
            render_fallback_analytics(session_key, display_config)

def render_fallback_data_view(session_key: str, display_config: Dict[str, Any]):
    """Fallback data view when MVC is not available"""
    import pandas as pd
    
    data = st.session_state.get(session_key, [])
    
    if not data:
        st.info(f"No {display_config.get('item_name', 'records')} found. Create your first record in the Create tab.")
        return
    
    df = pd.DataFrame(data)
    
    # Search functionality
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔍 Search...", key=f"{session_key}_search")
    
    with col2:
        # Primary filter
        primary_filter = display_config.get('primary_filter')
        if primary_filter and primary_filter['field'] in df.columns:
            options = ["All"] + sorted(df[primary_filter['field']].unique().tolist())
            primary_value = st.selectbox(primary_filter['label'], options, key=f"{session_key}_primary")
        else:
            primary_value = "All"
    
    with col3:
        # Secondary filter
        secondary_filter = display_config.get('secondary_filter')
        if secondary_filter and secondary_filter['field'] in df.columns:
            options = ["All"] + sorted(df[secondary_filter['field']].unique().tolist())
            secondary_value = st.selectbox(secondary_filter['label'], options, key=f"{session_key}_secondary")
        else:
            secondary_value = "All"
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_term:
        search_fields = display_config.get('search_fields', list(df.columns))
        mask = filtered_df[search_fields].astype(str).apply(
            lambda x: x.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        filtered_df = filtered_df[mask]
    
    if primary_filter and primary_value != "All":
        filtered_df = filtered_df[filtered_df[primary_filter['field']] == primary_value]
    
    if secondary_filter and secondary_value != "All":
        filtered_df = filtered_df[filtered_df[secondary_filter['field']] == secondary_value]
    
    st.write(f"**Total {display_config.get('item_name', 'Records')}:** {len(filtered_df)}")
    
    # View mode
    view_mode = st.radio("View Mode:", ["📊 Table View", "📋 Card View"], horizontal=True, key=f"{session_key}_view")
    
    if view_mode == "📊 Table View":
        if not filtered_df.empty:
            # Clean dataframe for display
            display_df = filtered_df.copy()
            for col in display_df.columns:
                if display_df[col].dtype == 'object':
                    display_df[col] = display_df[col].astype(str)
            display_df = display_df.fillna('')
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No records match your filters.")
    else:
        # Card view
        if not filtered_df.empty:
            title_field = display_config.get('title_field', 'id')
            key_fields = display_config.get('key_fields', ['id'])
            
            for idx, row in filtered_df.iterrows():
                with st.container():
                    st.markdown("---")
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        title = row.get(title_field, f"Record {row.get('id', idx)}")
                        st.subheader(f"📄 {title}")
                        
                        key_info = []
                        for field in key_fields:
                            if field in row:
                                key_info.append(f"**{field.replace('_', ' ').title()}:** {row[field]}")
                        if key_info:
                            st.write(" | ".join(key_info))
                    
                    with col2:
                        detail_fields = display_config.get('detail_fields', [])
                        for field in detail_fields:
                            if field in row and row[field] is not None:
                                st.write(f"**{field.replace('_', ' ').title()}:** {row[field]}")
                    
                    with col3:
                        if st.button("👁️ View", key=f"view_{session_key}_{idx}"):
                            with st.expander("Record Details", expanded=True):
                                for field, value in row.items():
                                    if value is not None:
                                        st.write(f"**{field.replace('_', ' ').title()}:** {value}")
        else:
            st.info("No records match your filters.")

def render_fallback_create_form(session_key: str, display_config: Dict[str, Any], form_config: Dict[str, Any]):
    """Fallback create form when MVC is not available"""
    from datetime import datetime, date
    
    st.subheader(f"📝 Create New {display_config.get('item_name', 'Record')}")
    
    with st.form(f"create_form_{session_key}"):
        form_data = {}
        
        # Get fields from form config
        fields = form_config.get('fields', []) if form_config else []
        
        # Render form fields
        col1, col2 = st.columns(2)
        
        for i, field in enumerate(fields):
            column = col1 if i % 2 == 0 else col2
            
            with column:
                field_key = field['key']
                field_type = field.get('type', 'text')
                label = field.get('label', field_key.replace('_', ' ').title())
                required = field.get('required', False)
                
                if required:
                    label += " *"
                
                if field_type == 'text':
                    form_data[field_key] = st.text_input(label, key=f"create_{session_key}_{field_key}")
                elif field_type == 'textarea':
                    form_data[field_key] = st.text_area(label, key=f"create_{session_key}_{field_key}")
                elif field_type == 'select':
                    options = field.get('options', [])
                    form_data[field_key] = st.selectbox(label, options, key=f"create_{session_key}_{field_key}")
                elif field_type == 'number':
                    min_val = field.get('min_value', 0.0)
                    form_data[field_key] = st.number_input(label, min_value=min_val, key=f"create_{session_key}_{field_key}")
                elif field_type == 'date':
                    form_data[field_key] = st.date_input(label, value=date.today(), key=f"create_{session_key}_{field_key}")
                elif field_type == 'checkbox':
                    form_data[field_key] = st.checkbox(label, key=f"create_{session_key}_{field_key}")
                elif field_type == 'currency':
                    form_data[field_key] = st.number_input(label, min_value=0.0, step=0.01, format="%.2f", key=f"create_{session_key}_{field_key}")
                else:
                    form_data[field_key] = st.text_input(label, key=f"create_{session_key}_{field_key}")
        
        submitted = st.form_submit_button(f"➕ Create {display_config.get('item_name', 'Record')}")
        
        if submitted and fields:
            # Basic validation
            valid = True
            for field in fields:
                if field.get('required', False) and not form_data.get(field['key']):
                    st.error(f"{field['label']} is required")
                    valid = False
            
            if valid:
                # Add metadata
                current_data = st.session_state.get(session_key, [])
                new_id = max([item.get('id', 0) for item in current_data], default=0) + 1
                
                form_data['id'] = new_id
                form_data['created_at'] = datetime.now().isoformat()
                
                # Convert date objects to strings
                for key, value in form_data.items():
                    if isinstance(value, date):
                        form_data[key] = value.strftime('%Y-%m-%d')
                
                current_data.append(form_data)
                st.session_state[session_key] = current_data
                st.success(f"{display_config.get('item_name', 'Record')} created successfully!")
                st.rerun()

def render_fallback_analytics(session_key: str, display_config: Dict[str, Any]):
    """Fallback analytics when MVC is not available"""
    import pandas as pd
    
    st.subheader(f"📈 {display_config.get('title', 'Analytics')}")
    
    data = st.session_state.get(session_key, [])
    
    if not data:
        st.info("No data available for analytics. Create some records first.")
        return
    
    df = pd.DataFrame(data)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(f"Total {display_config.get('item_name', 'Records')}", len(data))
    
    with col2:
        # Status-based count
        primary_filter = display_config.get('primary_filter')
        if primary_filter and primary_filter['field'] in df.columns:
            active_count = len(df[df[primary_filter['field']].isin(['Active', 'Open', 'In Progress'])])
            st.metric("Active", active_count)
        else:
            st.metric("Total Records", len(data))
    
    with col3:
        # Recent count
        recent_count = min(len(data), 10)
        st.metric("Recent", recent_count)
    
    with col4:
        # Completion rate
        if primary_filter and primary_filter['field'] in df.columns:
            completed = len(df[df[primary_filter['field']].isin(['Completed', 'Closed', 'Done'])])
            completion_rate = (completed / len(data) * 100) if len(data) > 0 else 0
            st.metric("Completion Rate", f"{completion_rate:.1f}%")
        else:
            st.metric("Efficiency", "100%")
    
    # Charts
    if len(df) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            primary_filter = display_config.get('primary_filter')
            if primary_filter and primary_filter['field'] in df.columns:
                st.subheader(f"Distribution by {primary_filter['label']}")
                field_counts = df[primary_filter['field']].value_counts()
                st.bar_chart(field_counts)
        
        with col2:
            secondary_filter = display_config.get('secondary_filter')
            if secondary_filter and secondary_filter['field'] in df.columns:
                st.subheader(f"Distribution by {secondary_filter['label']}")
                field_counts = df[secondary_filter['field']].value_counts()
                st.bar_chart(field_counts)