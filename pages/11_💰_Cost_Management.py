"""
Cost Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Cost Management - gcPanel", page_icon="💰", layout="wide")

st.title("💰 Cost Management")
st.markdown("Highland Tower Development - Project Cost Control & Budget Management")
st.markdown("---")

# Initialize session state for cost data
if 'cost_items' not in st.session_state:
    st.session_state.cost_items = [
        {
            "id": "COST-001",
            "category": "Labor",
            "description": "Structural Steel Installation - Floors 20-25",
            "budget": 1250000,
            "actual": 1175000,
            "committed": 1200000,
            "variance": 75000,
            "status": "On Budget",
            "last_updated": "2024-12-15"
        },
        {
            "id": "COST-002", 
            "category": "Materials",
            "description": "Concrete & Rebar - Foundation & Structure",
            "budget": 850000,
            "actual": 875000,
            "committed": 850000,
            "variance": -25000,
            "status": "Over Budget",
            "last_updated": "2024-12-14"
        }
    ]

# Main tabs
tab1, tab2, tab3 = st.tabs(["📊 Cost Overview", "📝 Add Cost Item", "📈 Budget Analysis"])

with tab1:
    st.subheader("📊 Cost Database")
    if st.session_state.cost_items:
        df = pd.DataFrame(st.session_state.cost_items)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No cost data available")

with tab2:
    st.subheader("📝 Add New Cost Item")
    st.info("Cost item creation form coming soon")

with tab3:
    st.subheader("📈 Budget Analysis")
    st.info("Budget analysis charts coming soon")

# Display configuration
display_config = {
    'title': 'Cost Management',
    'item_name': 'Cost Management',
    'title_field': 'title' if 'title' in model.schema.get('fields', {}) else 'id',
    'key_fields': ['id', 'status', 'type'] if 'status' in model.schema.get('fields', {}) else ['id'],
    'detail_fields': ['date', 'location', 'description'] if 'date' in model.schema.get('fields', {}) else [],
    'search_fields': ['title', 'description', 'id'] if 'title' in model.schema.get('fields', {}) else ['id'],
    'primary_filter': {
        'field': 'status',
        'label': 'Status'
    } if 'status' in model.schema.get('fields', {}) else None,
    'secondary_filter': {
        'field': 'type',
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
crud_controller = CRUDController(model, 'cost_management', display_config)

# Main content tabs
tab1, tab2, tab3 = st.tabs(["💰 Cost Management Database", "📝 Create New", "📈 Analytics"])

with tab1:
    crud_controller.render_data_view('cost_management')

with tab2:
    crud_controller.render_create_form(form_config)

with tab3:
    st.subheader("📈 Cost Management Analytics")
    
    # Basic metrics
    total_items = len(model.get_all())
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cost Management", total_items)
    
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
    st.header("Cost Management Summary")
    
    items = model.get_all()
    if items:
        st.metric("Highland Tower Cost Management", len(items))
        
        # Show recent items
        st.subheader("Recent Items")
        recent_items = items[:3]  # Show first 3 items
        
        for item in recent_items:
            with st.expander(f"💰 {item.get('id', 'Item')}"):
                for key, value in list(item.items())[:3]:  # Show first 3 fields
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    st.markdown("---")
    st.write("**Highland Tower Development**")
    st.write("$45.5M Mixed-Use Project")
    st.write("Cost Management powered by gcPanel")
