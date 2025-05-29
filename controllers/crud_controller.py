"""
CRUD Controller for gcPanel MVC Architecture
Handles all user interface operations and data management
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, date
import logging
from data.highland_tower_data import HIGHLAND_TOWER_DATA

logger = logging.getLogger(__name__)

class CRUDController:
    """Complete CRUD controller with advanced UI capabilities"""
    
    def __init__(self, model, session_key: str, display_config: Dict[str, Any]):
        self.model = model
        self.session_key = session_key
        self.display_config = display_config
        
    def render_data_view(self, key_prefix: str = ""):
        """Render the main data view with search, filtering, and actions"""
        data = self.model.get_all()
        
        if not data:
            st.info(f"No {self.display_config.get('item_name', 'records')} found. Create your first record in the Create tab.")
            return
        
        df = pd.DataFrame(data)
        
        # Search and filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input(
                "🔍 Search...", 
                key=f"{key_prefix}_search",
                help="Search across all fields"
            )
        
        with col2:
            # Primary filter (status, type, etc.)
            primary_filter = self.display_config.get('primary_filter')
            primary_value = "All"
            if primary_filter and primary_filter['field'] in df.columns:
                options = ["All"] + sorted(df[primary_filter['field']].unique().tolist())
                primary_value = st.selectbox(
                    primary_filter['label'], 
                    options,
                    key=f"{key_prefix}_primary_filter"
                )
        
        with col3:
            # Secondary filter
            secondary_filter = self.display_config.get('secondary_filter')
            secondary_value = "All"
            if secondary_filter and secondary_filter['field'] in df.columns:
                options = ["All"] + sorted(df[secondary_filter['field']].unique().tolist())
                secondary_value = st.selectbox(
                    secondary_filter['label'], 
                    options,
                    key=f"{key_prefix}_secondary_filter"
                )
        
        # Apply filters
        filtered_df = df.copy()
        
        if search_term:
            search_fields = self.display_config.get('search_fields', list(df.columns))
            mask = filtered_df[search_fields].astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)
            ).any(axis=1)
            filtered_df = filtered_df[mask]
        
        if primary_filter and primary_value != "All":
            filtered_df = filtered_df[filtered_df[primary_filter['field']] == primary_value]
            
        if secondary_filter and secondary_value != "All":
            filtered_df = filtered_df[filtered_df[secondary_filter['field']] == secondary_value]
        
        # Display count
        st.write(f"**Total {self.display_config.get('item_name', 'Records')}:** {len(filtered_df)}")
        
        # View mode toggle
        view_mode = st.radio(
            "View Mode:", 
            ["📊 Table View", "📋 Card View"], 
            horizontal=True,
            key=f"{key_prefix}_view_mode"
        )
        
        if view_mode == "📊 Table View":
            self._render_table_view(filtered_df, key_prefix)
        else:
            self._render_card_view(filtered_df, key_prefix)
    
    def _render_table_view(self, df: pd.DataFrame, key_prefix: str):
        """Render table view with standard Streamlit record selection"""
        if df.empty:
            st.info("No records match your filters.")
            return
        
        # Configure columns
        column_config = self.display_config.get('column_config', {})
        
        # Select key columns for display
        key_fields = self.display_config.get('key_fields', list(df.columns)[:5])
        display_columns = [col for col in key_fields if col in df.columns]
        
        # If no key fields specified or found, use first 5 columns
        if not display_columns:
            display_columns = list(df.columns)[:5]
        
        # Create table header
        header_cols = st.columns(len(display_columns) + 1)  # +1 for actions column
        for i, col in enumerate(display_columns):
            with header_cols[i]:
                st.write(f"**{col.replace('_', ' ').title()}**")
        with header_cols[-1]:
            st.write("**Actions**")
        
        st.divider()
        
        # Display table rows with inline action buttons
        for index, row in df.iterrows():
            row_cols = st.columns(len(display_columns) + 1)
            
            # Display data columns
            for i, col in enumerate(display_columns):
                with row_cols[i]:
                    value = row[col]
                    if pd.isna(value):
                        value = ""
                    st.write(str(value))
            
            # Action buttons column
            with row_cols[-1]:
                action_cols = st.columns(2)
                with action_cols[0]:
                    if st.button("👁️", key=f"{key_prefix}_view_{index}", help="View"):
                        st.session_state[f"{key_prefix}_view_record"] = row.to_dict()
                        st.rerun()
                with action_cols[1]:
                    if st.button("✏️", key=f"{key_prefix}_edit_{index}", help="Edit"):
                        st.session_state[f"{key_prefix}_edit_record"] = row.to_dict()
                        st.rerun()
        
        st.divider()
        
        # Record selection and actions
        st.subheader("Record Actions")
        
        if len(df) > 0:
            # Create record options for selection
            record_options = []
            for index, row in df.iterrows():
                # Create a display label for each record
                key_fields = self.display_config.get('key_fields', ['id'])
                if key_fields and len(key_fields) > 0:
                    first_field = key_fields[0]
                    if first_field in row.index:
                        label = f"{row[first_field]}"
                        if len(key_fields) > 1 and key_fields[1] in row.index:
                            label += f" - {row[key_fields[1]]}"
                    else:
                        label = f"Record {index + 1}"
                else:
                    label = f"Record {index + 1}"
                
                record_options.append((label, index))
            
            # Record selector
            col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
            
            with col1:
                selected_option = st.selectbox(
                    "Select a record:",
                    options=record_options,
                    format_func=lambda x: x[0],
                    key=f"{key_prefix}_record_selector"
                )
            
            if selected_option:
                selected_index = selected_option[1]
                selected_record = df.iloc[selected_index].to_dict()
                
                with col2:
                    if st.button("👁️ View Details", key=f"{key_prefix}_view_action"):
                        st.session_state[f"{key_prefix}_view_record"] = selected_record
                
                with col3:
                    if st.button("✏️ Edit Record", key=f"{key_prefix}_edit_action"):
                        st.session_state[f"{key_prefix}_edit_record"] = selected_record
        
        # Display view details
        if f"{key_prefix}_view_record" in st.session_state:
            st.divider()
            record = st.session_state[f"{key_prefix}_view_record"]
            self._show_record_details(record)
            if st.button("Close View", key=f"{key_prefix}_close_view"):
                del st.session_state[f"{key_prefix}_view_record"]
                st.rerun()
        
        # Display edit form
        if f"{key_prefix}_edit_record" in st.session_state:
            st.divider()
            record = st.session_state[f"{key_prefix}_edit_record"]
            self._show_edit_form(record, key_prefix)
            if st.button("Cancel Edit", key=f"{key_prefix}_cancel_edit"):
                del st.session_state[f"{key_prefix}_edit_record"]
                st.rerun()
    
    def _render_card_view(self, df: pd.DataFrame, key_prefix: str):
        """Render card view with actions"""
        if df.empty:
            st.info("No records match your filters.")
            return
        
        title_field = self.display_config.get('title_field', 'id')
        key_fields = self.display_config.get('key_fields', ['id'])
        detail_fields = self.display_config.get('detail_fields', [])
        
        for idx, row in df.iterrows():
            with st.container():
                st.markdown("---")
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    # Main title
                    title = row.get(title_field, f"Record {row.get('id', idx)}")
                    st.subheader(f"📄 {title}")
                    
                    # Key fields
                    key_info = []
                    for field in key_fields:
                        if field in row:
                            key_info.append(f"**{field.replace('_', ' ').title()}:** {row[field]}")
                    if key_info:
                        st.write(" | ".join(key_info))
                
                with col2:
                    # Detail fields
                    for field in detail_fields:
                        if field in row and row[field] is not None:
                            st.write(f"**{field.replace('_', ' ').title()}:** {row[field]}")
                
                with col3:
                    # Action buttons
                    record_id = row.get('id', idx)
                    
                    if st.button("👁️ View", key=f"view_{key_prefix}_{record_id}", help="View details"):
                        self._show_record_details(row, key_prefix)
                    
                    if st.button("✏️ Edit", key=f"edit_{key_prefix}_{record_id}", help="Edit record"):
                        self._show_edit_form(row, key_prefix)
                    
                    if st.button("🗑️ Delete", key=f"delete_{key_prefix}_{record_id}", help="Delete record", type="secondary"):
                        if st.session_state.get(f"confirm_delete_{key_prefix}_{record_id}"):
                            if self.model.delete(record_id):
                                st.success(f"Record {record_id} deleted successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to delete record")
                        else:
                            st.session_state[f"confirm_delete_{key_prefix}_{record_id}"] = True
                            st.warning("Click Delete again to confirm")
    
    def _show_record_details(self, record: Dict, key_prefix: str):
        """Show detailed view of a record"""
        with st.expander("📋 Record Details", expanded=True):
            col1, col2 = st.columns(2)
            
            fields = list(record.keys())
            mid_point = len(fields) // 2
            
            with col1:
                for field in fields[:mid_point]:
                    if record[field] is not None:
                        label = field.replace('_', ' ').title()
                        st.write(f"**{label}:** {record[field]}")
            
            with col2:
                for field in fields[mid_point:]:
                    if record[field] is not None:
                        label = field.replace('_', ' ').title()
                        st.write(f"**{label}:** {record[field]}")
    
    def _show_edit_form(self, record: Dict, key_prefix: str):
        """Show edit form for a record"""
        with st.expander("✏️ Edit Record", expanded=True):
            with st.form(f"edit_form_{key_prefix}_{record.get('id')}"):
                updated_data = {}
                
                # Generate form fields based on schema
                schema_fields = self.model.schema.get('fields', {})
                
                col1, col2 = st.columns(2)
                fields = list(schema_fields.keys())
                mid_point = len(fields) // 2
                
                for i, field_name in enumerate(fields):
                    if field_name == 'id':  # Skip ID field
                        continue
                    
                    field_config = schema_fields[field_name]
                    current_value = record.get(field_name, '')
                    
                    column = col1 if i < mid_point else col2
                    
                    with column:
                        updated_data[field_name] = self._render_form_field(
                            field_name, 
                            field_config, 
                            current_value,
                            f"edit_{key_prefix}_{field_name}_{record.get('id')}"
                        )
                
                submitted = st.form_submit_button("💾 Update Record")
                
                if submitted:
                    # Validate data
                    errors = self.model.validate_data(updated_data)
                    
                    if errors:
                        for field, field_errors in errors.items():
                            for error in field_errors:
                                st.error(error)
                    else:
                        if self.model.update(record['id'], updated_data):
                            st.success(f"Record {record['id']} updated successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to update record")
    
    def render_create_form(self, form_config: Dict[str, Any], key_prefix: str = ""):
        """Render create form with validation"""
        st.subheader(f"📝 Create New {self.display_config.get('item_name', 'Record')}")
        
        with st.form(f"create_form_{key_prefix}"):
            form_data = {}
            
            # Get form fields from config or generate from schema
            fields = form_config.get('fields', [])
            if not fields:
                # Generate from schema
                schema_fields = self.model.schema.get('fields', {})
                for field_name, field_config in schema_fields.items():
                    if field_name != 'id':  # Skip ID field
                        fields.append({
                            'key': field_name,
                            'type': field_config.get('type', 'text'),
                            'label': field_name.replace('_', ' ').title(),
                            'required': field_config.get('required', False)
                        })
            
            # Render form fields in columns
            col1, col2 = st.columns(2)
            
            for i, field in enumerate(fields):
                column = col1 if i % 2 == 0 else col2
                
                with column:
                    form_data[field['key']] = self._render_form_field(
                        field['key'],
                        field,
                        field.get('default', ''),
                        f"create_{key_prefix}_{field['key']}"
                    )
            
            submitted = st.form_submit_button(f"➕ Create {self.display_config.get('item_name', 'Record')}")
            
            if submitted:
                # Validate data
                errors = self.model.validate_data(form_data)
                
                if errors:
                    for field, field_errors in errors.items():
                        for error in field_errors:
                            st.error(error)
                else:
                    if self.model.create(form_data):
                        st.success(f"{self.display_config.get('item_name', 'Record')} created successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to create record")
    
    def _render_form_field(self, field_name: str, field_config: Dict, current_value: Any, key: str) -> Any:
        """Render individual form field based on type"""
        field_type = field_config.get('type', 'text')
        label = field_config.get('label', field_name.replace('_', ' ').title())
        placeholder = field_config.get('placeholder', '')
        required = field_config.get('required', False)
        
        # Add required indicator to label
        if required:
            label += " *"
        
        if field_type == 'text':
            return st.text_input(label, value=current_value, placeholder=placeholder, key=key)
        
        elif field_type == 'textarea':
            return st.text_area(label, value=current_value, placeholder=placeholder, key=key)
        
        elif field_type == 'number':
            min_value = field_config.get('min_value', 0.0)
            max_value = field_config.get('max_value', None)
            step = field_config.get('step', 1.0)
            return st.number_input(label, value=float(current_value) if current_value else 0.0, 
                                 min_value=min_value, max_value=max_value, step=step, key=key)
        
        elif field_type == 'select':
            options = field_config.get('options', [])
            index = 0
            if current_value and current_value in options:
                index = options.index(current_value)
            return st.selectbox(label, options, index=index, key=key)
        
        elif field_type == 'multiselect':
            options = field_config.get('options', [])
            default = current_value if isinstance(current_value, list) else []
            return st.multiselect(label, options, default=default, key=key)
        
        elif field_type == 'date':
            if current_value:
                if isinstance(current_value, str):
                    try:
                        current_value = datetime.strptime(current_value, '%Y-%m-%d').date()
                    except:
                        current_value = date.today()
                elif isinstance(current_value, datetime):
                    current_value = current_value.date()
            else:
                current_value = date.today()
            return st.date_input(label, value=current_value, key=key)
        
        elif field_type == 'datetime':
            if current_value:
                if isinstance(current_value, str):
                    try:
                        current_value = datetime.fromisoformat(current_value)
                    except:
                        current_value = datetime.now()
            else:
                current_value = datetime.now()
            return st.datetime_input(label, value=current_value, key=key)
        
        elif field_type == 'checkbox':
            return st.checkbox(label, value=bool(current_value), key=key)
        
        elif field_type == 'email':
            return st.text_input(label, value=current_value, placeholder=placeholder or "email@example.com", key=key)
        
        elif field_type == 'url':
            return st.text_input(label, value=current_value, placeholder=placeholder or "https://example.com", key=key)
        
        elif field_type == 'phone':
            return st.text_input(label, value=current_value, placeholder=placeholder or "+1 (555) 123-4567", key=key)
        
        elif field_type == 'currency':
            return st.number_input(label, value=float(current_value) if current_value else 0.0, 
                                 min_value=0.0, step=0.01, format="%.2f", key=key)
        
        else:
            return st.text_input(label, value=current_value, placeholder=placeholder, key=key)
    
    def render_analytics(self, key_prefix: str = ""):
        """Render analytics view with metrics and charts"""
        st.subheader(f"📈 {self.display_config.get('title', 'Analytics')}")
        
        data = self.model.get_all()
        total_records = len(data)
        
        if total_records == 0:
            st.info("No data available for analytics. Create some records first.")
            return
        
        df = pd.DataFrame(data)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(f"Total {self.display_config.get('item_name', 'Records')}", total_records)
        
        with col2:
            # Recent records (last 30 days)
            if 'created_at' in df.columns:
                recent_count = len(df[df['created_at'] >= (datetime.now() - pd.Timedelta(days=30)).isoformat()])
                st.metric("Recent (30 days)", recent_count)
            else:
                st.metric("Active Records", total_records)
        
        with col3:
            # Status-based metric
            primary_filter = self.display_config.get('primary_filter')
            if primary_filter and primary_filter['field'] in df.columns:
                active_count = len(df[df[primary_filter['field']].isin(['Active', 'Open', 'In Progress'])])
                st.metric("Active", active_count)
            else:
                st.metric("Available", total_records)
        
        with col4:
            # Completion rate or similar
            if primary_filter and primary_filter['field'] in df.columns:
                completed = len(df[df[primary_filter['field']].isin(['Completed', 'Closed', 'Done'])])
                completion_rate = (completed / total_records * 100) if total_records > 0 else 0
                st.metric("Completion Rate", f"{completion_rate:.1f}%")
            else:
                st.metric("Growth Rate", "📈 100%")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Primary field distribution
            primary_filter = self.display_config.get('primary_filter')
            if primary_filter and primary_filter['field'] in df.columns:
                st.subheader(f"Distribution by {primary_filter['label']}")
                field_counts = df[primary_filter['field']].value_counts()
                st.bar_chart(field_counts)
        
        with col2:
            # Secondary field distribution or trends
            secondary_filter = self.display_config.get('secondary_filter')
            if secondary_filter and secondary_filter['field'] in df.columns:
                st.subheader(f"Distribution by {secondary_filter['label']}")
                field_counts = df[secondary_filter['field']].value_counts()
                st.bar_chart(field_counts)
            elif 'created_at' in df.columns:
                st.subheader("Creation Trends")
                df['created_date'] = pd.to_datetime(df['created_at']).dt.date
                daily_counts = df['created_date'].value_counts().sort_index()
                st.line_chart(daily_counts)
        
        # Data table with key insights
        st.subheader("📊 Data Summary")
        
        # Show recent records
        recent_data = df.head(10)
        if not recent_data.empty:
            st.write("**Recent Records:**")
            st.dataframe(recent_data, use_container_width=True, hide_index=True)