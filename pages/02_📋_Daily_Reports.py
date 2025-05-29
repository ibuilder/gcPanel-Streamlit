"""
Daily Reports Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Daily Reports - gcPanel", page_icon="📋", layout="wide")

st.title("📋 Daily Reports")
st.markdown("Highland Tower Development - Daily Progress & Activity Reports")
st.markdown("---")

# Initialize session state for daily reports
if 'daily_reports' not in st.session_state:
    st.session_state.daily_reports = [
        {
            "id": "DR-001",
            "date": "2024-12-15",
            "weather": "Clear, 45°F",
            "crew_count": 45,
            "hours_worked": 360,
            "activities": "Structural steel installation - Floor 22",
            "progress": "85% complete on Floor 22 framing",
            "issues": "None reported",
            "safety_incidents": 0
        }
    ]

# Main tabs
tab1, tab2, tab3 = st.tabs(["📊 Reports Database", "📝 Create Report", "📈 Progress Summary"])

with tab1:
    st.subheader("📊 Daily Reports Database")
    if st.session_state.daily_reports:
        df = pd.DataFrame(st.session_state.daily_reports)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No daily reports available")

with tab2:
    st.subheader("📝 Create Daily Report")
    st.info("Daily report creation form coming soon")

with tab3:
    st.subheader("📈 Progress Summary")
    st.info("Progress analytics coming soon")

# Display configuration
display_config = {
    'title': 'Daily Reports',
    'item_name': 'Daily Reports',
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
crud_controller = CRUDController(model, 'daily_reports', display_config)

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📋 Daily Reports Database", "📝 Create New", "📈 Analytics"])

with tab1:
    crud_controller.render_data_view('daily_reports')

with tab2:
    crud_controller.render_create_form(form_config)

with tab3:
    st.subheader("📈 Daily Reports Analytics")
    
    # Basic metrics
    total_items = len(model.get_all())
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Daily Reports", total_items)
    
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
    st.header("Daily Reports Summary")
    
    items = model.get_all()
    if items:
        st.metric("Highland Tower Daily Reports", len(items))
        
        # Show recent items
        st.subheader("Recent Items")
        recent_items = items[:3]  # Show first 3 items
        
        for item in recent_items:
            with st.expander(f"📋 {item.get('id', 'Item')}"):
                for key, value in list(item.items())[:3]:  # Show first 3 fields
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    st.markdown("---")
    st.write("**Highland Tower Development**")
    st.write("$45.5M Mixed-Use Project")
    st.write("Daily Reports powered by gcPanel")
