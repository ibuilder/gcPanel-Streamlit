"""
Safety Management Page - Highland Tower Development
Refactored using MVC pattern with models, controllers, and helpers
"""

import streamlit as st
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib.utils.helpers import check_authentication
from lib.models.all_models import SafetyModel
from lib.controllers.crud_controller import CRUDController
from lib.helpers.ui_helpers import render_highland_header, apply_highland_tower_styling, render_status_badge

# Page configuration
st.set_page_config(page_title="Safety - gcPanel", page_icon="🦺", layout="wide")

# Check authentication
if not check_authentication():
    st.error("🔒 Please log in to access this page")
    st.stop()

# Apply styling
apply_highland_tower_styling()

# Render header
render_highland_header("🦺 Safety Management", "Highland Tower Development - Safety Incident Tracking")

# Initialize model and controller
safety_model = SafetyModel()

# Display configuration
display_config = {
    'title': 'Safety Incidents',
    'item_name': 'Incident',
    'title_field': 'id',
    'key_fields': ['incident_type', 'severity', 'location', 'date_occurred', 'status'],
    'detail_fields': ['reported_by', 'description'],
    'search_fields': ['description', 'location', 'incident_type', 'reported_by'],
    'primary_filter': {
        'field': 'severity',
        'label': 'Severity'
    },
    'secondary_filter': {
        'field': 'incident_type',
        'label': 'Incident Type'
    },
    'column_config': {
        "id": st.column_config.TextColumn("ID"),
        "incident_type": st.column_config.TextColumn("Type"),
        "severity": st.column_config.TextColumn("Severity"), 
        "location": st.column_config.TextColumn("Location"),
        "date_occurred": st.column_config.DateColumn("Date"),
        "status": st.column_config.TextColumn("Status"),
        "status": st.column_config.TextColumn("Status"),
        "reported_by": st.column_config.TextColumn("Reported By")
    }
}

# Form configuration
form_config = {
    'fields': [
        {'key': 'date', 'type': 'date', 'label': 'Incident Date'},
        {'key': 'type', 'type': 'select', 'label': 'Incident Type',
         'options': ['Near Miss', 'First Aid', 'Medical Treatment', 'Lost Time', 'Equipment Incident']},
        {'key': 'severity', 'type': 'select', 'label': 'Severity',
         'options': ['Low', 'Medium', 'High', 'Critical']},
        {'key': 'location', 'type': 'text', 'label': 'Location', 'placeholder': 'Enter incident location'},
        {'key': 'description', 'type': 'textarea', 'label': 'Description', 'placeholder': 'Detailed incident description'},
        {'key': 'reported_by', 'type': 'text', 'label': 'Reported By', 'placeholder': 'Name and title'},
        {'key': 'status', 'type': 'select', 'label': 'Status',
         'options': ['Open', 'Under Investigation', 'Investigated', 'Closed']},
        {'key': 'investigation_notes', 'type': 'textarea', 'label': 'Investigation Notes'},
        {'key': 'corrective_actions', 'type': 'textarea', 'label': 'Corrective Actions'},
        {'key': 'follow_up_required', 'type': 'select', 'label': 'Follow-up Required',
         'options': [True, False]}
    ]
}

# Initialize controller
crud_controller = CRUDController(safety_model, 'safety', display_config)

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📊 Safety Incidents", "📝 Report Incident", "📈 Safety Metrics"])

with tab1:
    crud_controller.render_data_view('safety')

with tab2:
    crud_controller.render_create_form(form_config)

with tab3:
    st.subheader("📈 Safety Performance Metrics")
    
    # Safety metrics
    total_incidents = len(safety_model.get_all())
    open_incidents = len(safety_model.get_open_incidents())
    followup_required = len(safety_model.get_incidents_requiring_followup())
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Incidents", total_incidents)
    
    with col2:
        st.metric("Open Incidents", open_incidents)
    
    with col3:
        st.metric("Follow-up Required", followup_required)
    
    with col4:
        safety_rate = ((total_incidents - open_incidents) / total_incidents * 100) if total_incidents > 0 else 100
        st.metric("Resolution Rate", f"{safety_rate:.1f}%")
    
    # Incident trends
    st.subheader("Incident Analysis")
    incidents_df = safety_model.to_dataframe()
    if not incidents_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            severity_dist = incidents_df['severity'].value_counts()
            st.bar_chart(severity_dist, use_container_width=True)
            st.caption("Incidents by Severity")
        
        with col2:
            type_dist = incidents_df['incident_type'].value_counts()
            st.bar_chart(type_dist, use_container_width=True)
            st.caption("Incidents by Type")

# Sidebar
with st.sidebar:
    st.header("Safety Dashboard")
    
    incidents = safety_model.get_all()
    if incidents:
        st.metric("Highland Tower Safety", f"{len(incidents)} incidents")
        
        # Recent incidents
        st.subheader("Recent Incidents")
        recent_incidents = sorted(incidents, key=lambda x: x.get('date', ''), reverse=True)[:3]
        
        for incident in recent_incidents:
            with st.expander(f"🦺 {incident['id']} - {incident['incident_type']}"):
                st.write(f"**Severity:** {incident['severity']}")
                st.write(f"**Location:** {incident['location']}")
                st.write(f"**Status:** {incident['status']}")
    
    st.markdown("---")
    st.write("**Safety First**")
    st.write("Highland Tower Development maintains the highest safety standards for all personnel and operations.")