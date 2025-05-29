"""
Deliveries Page - Highland Tower Development
Refactored using MVC pattern with models, controllers, and helpers
"""

import streamlit as st
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import check_authentication

from models.all_models import DeliveryModel
from controllers.crud_controller import CRUDController
from helpers.ui_helpers import render_highland_header, apply_highland_tower_styling, format_currency

# Page configuration
st.set_page_config(page_title="Deliveries - gcPanel", page_icon="🚚", layout="wide")
# Check authentication
if not check_authentication():
    st.error("🔒 Please log in to access this page")
    st.stop()


# Apply styling
apply_highland_tower_styling()

# Render header
render_highland_header("🚚 Deliveries", "Highland Tower Development - Material Delivery Tracking")

# Initialize model
model = DeliveryModel()

# Display configuration
display_config = {
    'title': 'Deliveries',
    'item_name': 'Deliveries',
    'title_field': 'title' if 'title' in model.schema.get('fields', {}) else 'id',
    'key_fields': ['delivery_date', 'supplier', 'material_description', 'quantity', 'status'] if 'status' in model.schema.get('fields', {}) else ['id'],
    'detail_fields': ['date', 'location', 'description'] if 'date' in model.schema.get('fields', {}) else [],
    'search_fields': ['supplier', 'material_description', 'delivery_ticket_number'] if 'title' in model.schema.get('fields', {}) else ['id'],
    'primary_filter': {
        'field': 'status',
        'label': 'Status'
    } if 'status' in model.schema.get('fields', {}) else None,
    'secondary_filter': {
        'field': 'status',
        'label': 'Type'  
    } if 'type' in model.schema.get('fields', {}) else None
}

# Form configuration - dynamically generate from schema
form_fields = []
for field_name, field_config in model.schema.get('fields', {}).items():
    if field_name == 'id':
        continue  # Skip ID field in forms
    
    field_type = field_config.get('type', 'text')
    if field_type == 'date':
        form_fields.append({'key': field_name, 'type': 'date', 'label': field_name.replace('_', ' ').title()})
    elif field_type == 'number':
        form_fields.append({'key': field_name, 'type': 'number', 'label': field_name.replace('_', ' ').title(), 'min_value': 0.0})
    elif field_type == 'boolean':
        form_fields.append({'key': field_name, 'type': 'select', 'label': field_name.replace('_', ' ').title(), 'options': [True, False]})
    else:
        form_fields.append({'key': field_name, 'type': 'text', 'label': field_name.replace('_', ' ').title()})

form_config = {'fields': form_fields}

# Initialize controller
crud_controller = CRUDController(model, 'deliveries', display_config)

# Main content tabs
tab1, tab2, tab3 = st.tabs(["🚚 Deliveries Database", "📝 Create New", "📈 Analytics"])

with tab1:
    crud_controller.render_data_view('deliveries')

with tab2:
    crud_controller.render_create_form(form_config)

with tab3:
    st.subheader("📈 Deliveries Analytics")
    
    # Basic metrics
    total_items = len(model.get_all())
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Deliveries", total_items)
    
    with col2:
        if 'status' in model.schema.get('fields', {}):
            active_items = len([item for item in model.get_all() if item.get('status') in ['Active', 'In Progress', 'Open']])
            st.metric("Active Items", active_items)
        else:
            st.metric("Recent Items", min(total_items, 10))
    
    with col3:
        if 'date' in model.schema.get('fields', {}):
            from datetime import datetime, timedelta
            recent_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            recent_items = len([item for item in model.get_all() if item.get('date', '') >= recent_date])
            st.metric("Recent (30 days)", recent_items)
        else:
            st.metric("Total Records", total_items)
    
    with col4:
        completion_rate = 100 if total_items == 0 else min(100, (total_items / max(1, total_items)) * 100)
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    # Data visualization
    if total_items > 0:
        items_df = model.to_dataframe()
        if not items_df.empty:
            st.subheader("Data Analysis")
            
            # Show distribution by status if available
            if 'status' in items_df.columns:
                status_dist = items_df['status'].value_counts()
                st.bar_chart(status_dist)
                st.caption("Distribution by Status")
            
            # Show distribution by type if available  
            elif 'type' in items_df.columns:
                type_dist = items_df['type'].value_counts()
                st.bar_chart(type_dist)
                st.caption("Distribution by Type")

# Sidebar
with st.sidebar:
    st.header("Deliveries Summary")
    
    items = model.get_all()
    if items:
        st.metric("Highland Tower Deliveries", len(items))
        
        # Show recent items
        st.subheader("Recent Items")
        recent_items = items[:3]  # Show first 3 items
        
        for item in recent_items:
            with st.expander(f"🚚 {item.get('id', 'Item')}"):
                for key, value in list(item.items())[:3]:  # Show first 3 fields
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    st.markdown("---")
    st.write("**Highland Tower Development**")
    st.write("$45.5M Mixed-Use Project")
    st.write("Deliveries powered by gcPanel")
