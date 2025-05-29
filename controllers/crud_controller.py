"""
CRUD Controller for gcPanel Construction Management Platform
Handles common CRUD operations and UI rendering
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional

class CRUDController:
    """Controller for handling CRUD operations and UI rendering"""
    
    def __init__(self, model, module_name: str, display_config: Dict[str, Any]):
        self.model = model
        self.module_name = module_name
        self.display_config = display_config
    
    def render_data_view(self, search_key: str):
        """Render the data view with search, filters, and records"""
        st.subheader(f"📊 {self.display_config['title']} Database")
        
        records = self.model.get_all()
        if not records:
            st.info(f"No {self.display_config['item_name'].lower()} available. Create your first {self.display_config['item_name'].lower()} in the Create tab!")
            return
        
        df = self.model.to_dataframe()
        
        # Search and filter section
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input(
                f"🔍 Search {self.display_config['item_name'].lower()}...",
                key=f"{search_key}_search"
            )
        
        with col2:
            filter_field = self.display_config.get('primary_filter')
            if filter_field:
                filter_options = ["All"] + list(df[filter_field['field']].unique()) if not df.empty else ["All"]
                filter_value = st.selectbox(
                    filter_field['label'],
                    filter_options,
                    key=f"{search_key}_filter1"
                )
        
        with col3:
            secondary_filter = self.display_config.get('secondary_filter')
            if secondary_filter:
                secondary_options = ["All"] + list(df[secondary_filter['field']].unique()) if not df.empty else ["All"]
                secondary_value = st.selectbox(
                    secondary_filter['label'],
                    secondary_options,
                    key=f"{search_key}_filter2"
                )
        
        # Apply filters
        filtered_records = records
        
        # Apply search
        if search_term:
            search_fields = self.display_config.get('search_fields', ['id', 'title', 'name'])
            filtered_records = self.model.search_records(search_term, search_fields)
        
        # Apply primary filter
        if filter_field and 'filter_value' in locals() and filter_value != "All":
            filtered_records = [r for r in filtered_records if r.get(filter_field['field']) == filter_value]
        
        # Apply secondary filter
        if secondary_filter and 'secondary_value' in locals() and secondary_value != "All":
            filtered_records = [r for r in filtered_records if r.get(secondary_filter['field']) == secondary_value]
        
        st.write(f"**Total {self.display_config['item_name']}:** {len(filtered_records)}")
        
        if filtered_records:
            # Convert to DataFrame for display
            display_df = pd.DataFrame(filtered_records)
            
            # Apply any formatting
            if 'formatters' in self.display_config:
                for field, formatter in self.display_config['formatters'].items():
                    if field in display_df.columns:
                        display_df[field] = display_df[field].apply(formatter)
            
            # Display view mode toggle
            view_mode = st.radio(
                "View Mode:", 
                ["📊 Table View", "📋 Card View"], 
                horizontal=True, 
                key=f"{search_key}_view_mode"
            )
            
            if view_mode == "📊 Table View":
                self._render_table_view(display_df)
            else:
                self._render_card_view(filtered_records, search_key)
        else:
            st.info(f"No {self.display_config['item_name'].lower()} found matching your criteria.")
    
    def _render_table_view(self, df: pd.DataFrame):
        """Render records in table format"""
        # Configure columns if specified
        column_config = self.display_config.get('column_config', {})
        
        st.dataframe(
            df,
            column_config=column_config,
            hide_index=True,
            use_container_width=True
        )
    
    def _render_card_view(self, records: List[Dict[str, Any]], search_key: str):
        """Render records in card format with action buttons"""
        st.markdown("---")
        st.subheader(f"📋 {self.display_config['item_name']} Cards with Actions")
        
        for idx, record in enumerate(records):
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                # Primary information column
                with col1:
                    title_field = self.display_config.get('title_field', 'title')
                    title = record.get(title_field, record.get('id', f"Record {idx+1}"))
                    st.write(f"**📋 {title}**")
                    
                    # Display key fields
                    key_fields = self.display_config.get('key_fields', ['id', 'status', 'type'])
                    for field in key_fields[:3]:
                        if field in record and field != title_field:
                            value = record[field]
                            st.write(f"**{field.replace('_', ' ').title()}:** {value}")
                
                # Secondary information column  
                with col2:
                    detail_fields = self.display_config.get('detail_fields', [])
                    for field in detail_fields[:3]:
                        if field in record:
                            value = record[field]
                            # Apply formatter if available
                            if 'formatters' in self.display_config and field in self.display_config['formatters']:
                                value = self.display_config['formatters'][field](value)
                            st.write(f"**{field.replace('_', ' ').title()}:** {value}")
                
                # Action buttons column
                with col3:
                    record_id = record.get('id', idx)
                    
                    if st.button("👁️ View", key=f"view_{search_key}_{record_id}", help="View details"):
                        self._show_record_details(record)
                    
                    if st.button("✏️ Edit", key=f"edit_{search_key}_{record_id}", help="Edit record"):
                        st.session_state[f'edit_{self.module_name}'] = record
                        st.session_state[f'show_{self.module_name}_edit'] = True
                        st.experimental_rerun()
                
                st.markdown("---")
    
    def _show_record_details(self, record: Dict[str, Any]):
        """Show detailed view of a record"""
        with st.expander(f"{self.display_config['item_name']} Details", expanded=True):
            # Create a nice formatted display
            col1, col2 = st.columns(2)
            
            fields = list(record.keys())
            mid_point = len(fields) // 2
            
            with col1:
                for field in fields[:mid_point]:
                    value = record[field]
                    # Apply formatter if available
                    if 'formatters' in self.display_config and field in self.display_config['formatters']:
                        value = self.display_config['formatters'][field](value)
                    st.write(f"**{field.replace('_', ' ').title()}:** {value}")
            
            with col2:
                for field in fields[mid_point:]:
                    value = record[field]
                    # Apply formatter if available
                    if 'formatters' in self.display_config and field in self.display_config['formatters']:
                        value = self.display_config['formatters'][field](value)
                    st.write(f"**{field.replace('_', ' ').title()}:** {value}")
    
    def render_create_form(self, form_config: Dict[str, Any]):
        """Render the create form"""
        st.subheader(f"📝 Create New {self.display_config['item_name']}")
        
        with st.form(f"{self.module_name}_form"):
            form_data = {}
            
            # Render form fields
            col1, col2 = st.columns(2)
            
            fields = form_config.get('fields', [])
            mid_point = len(fields) // 2
            
            # Left column fields
            with col1:
                for field in fields[:mid_point]:
                    form_data[field['key']] = self._render_form_field(field)
            
            # Right column fields
            with col2:
                for field in fields[mid_point:]:
                    form_data[field['key']] = self._render_form_field(field)
            
            # Submit button
            submitted = st.form_submit_button(f"Create {self.display_config['item_name']}")
            
            if submitted:
                try:
                    # Create the record
                    new_record = self.model.create(form_data)
                    st.success(f"{self.display_config['item_name']} created successfully!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error creating {self.display_config['item_name'].lower()}: {str(e)}")
    
    def _render_form_field(self, field_config: Dict[str, Any]):
        """Render a single form field"""
        field_type = field_config.get('type', 'text')
        key = field_config['key']
        label = field_config.get('label', key.replace('_', ' ').title())
        
        if field_type == 'text':
            return st.text_input(label, placeholder=field_config.get('placeholder', ''))
        elif field_type == 'textarea':
            return st.text_area(label, placeholder=field_config.get('placeholder', ''))
        elif field_type == 'number':
            return st.number_input(label, min_value=field_config.get('min_value', 0.0))
        elif field_type == 'date':
            return st.date_input(label)
        elif field_type == 'select':
            options = field_config.get('options', [])
            return st.selectbox(label, options)
        elif field_type == 'multiselect':
            options = field_config.get('options', [])
            return st.multiselect(label, options)
        else:
            return st.text_input(label)