"""
Submittals Management Page - Highland Tower Development
Refactored using MVC pattern with models, controllers, and helpers
"""

import streamlit as st
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.submittal_model import SubmittalModel
from controllers.crud_controller import CRUDController
from helpers.ui_helpers import render_highland_header, apply_highland_tower_styling

# Page configuration
st.set_page_config(page_title="Submittals - gcPanel", page_icon="📨", layout="wide")

# Apply styling
apply_highland_tower_styling()

# Render header
render_highland_header("📨 Submittals Management", "Highland Tower Development - Construction Submittals")

# Initialize model
submittal_model = SubmittalModel()

# Display configuration
display_config = {
    'title': 'Submittals',
    'item_name': 'Submittal',
    'title_field': 'title',
    'key_fields': ['submittal_number', 'title', 'trade', 'status', 'date_submitted'],
    'detail_fields': ['date_submitted', 'status', 'reviewer'],
    'search_fields': ['title', 'trade', 'submitted_by', 'submittal_number'],
    'primary_filter': {
        'field': 'status',
        'label': 'Status'
    },
    'secondary_filter': {
        'field': 'status',
        'label': 'Discipline'
    },
    'column_config': {
        "id": st.column_config.TextColumn("Submittal ID"),
        "title": st.column_config.TextColumn("Title"),
        "spec_section": st.column_config.TextColumn("Spec Section"),
        "discipline": st.column_config.TextColumn("Discipline"),
        "submitted_by": st.column_config.TextColumn("Submitted By"),
        "date_submitted": st.column_config.DateColumn("Date Submitted"),
        "status": st.column_config.TextColumn("Status"),
        "reviewer": st.column_config.TextColumn("Reviewer")
    }
}

# Form configuration
form_config = {
    'fields': [
        {'key': 'title', 'type': 'text', 'label': 'Submittal Title', 'placeholder': 'Descriptive title'},
        {'key': 'spec_section', 'type': 'text', 'label': 'Spec Section', 'placeholder': 'e.g., 05 12 00'},
        {'key': 'discipline', 'type': 'select', 'label': 'Discipline',
         'options': ['Architectural', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Civil']},
        {'key': 'submitted_by', 'type': 'text', 'label': 'Submitted By', 'placeholder': 'Company name'},
        {'key': 'date_submitted', 'type': 'date', 'label': 'Date Submitted'},
        {'key': 'status', 'type': 'select', 'label': 'Status',
         'options': ['Under Review', 'Approved', 'Rejected', 'Resubmit Required']},
        {'key': 'reviewer', 'type': 'text', 'label': 'Reviewer', 'placeholder': 'Assigned reviewer'},
        {'key': 'review_due_date', 'type': 'date', 'label': 'Review Due Date'},
        {'key': 'description', 'type': 'textarea', 'label': 'Description'},
        {'key': 'manufacturer', 'type': 'text', 'label': 'Manufacturer'},
        {'key': 'model_number', 'type': 'text', 'label': 'Model Number'},
        {'key': 'revision', 'type': 'text', 'label': 'Revision', 'placeholder': 'e.g., Rev A'}
    ]
}

# Initialize controller
crud_controller = CRUDController(submittal_model, 'submittals', display_config)

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📊 Submittals Database", "📝 Create Submittal", "📈 Analytics"])

with tab1:
    crud_controller.render_data_view('submittals')

with tab2:
    crud_controller.render_create_form(form_config)

with tab3:
    st.subheader("📈 Submittal Analytics")
    
    # Metrics
    total_submittals = len(submittal_model.get_all())
    approved_submittals = len(submittal_model.get_submittals_by_status('Approved'))
    overdue_reviews = len(submittal_model.get_overdue_reviews())
    resubmit_required = len(submittal_model.get_resubmit_required())
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Submittals", total_submittals)
    
    with col2:
        st.metric("Approved", approved_submittals)
    
    with col3:
        st.metric("Overdue Reviews", overdue_reviews)
    
    with col4:
        approval_rate = (approved_submittals / total_submittals * 100) if total_submittals > 0 else 0
        st.metric("Approval Rate", f"{approval_rate:.1f}%")
    
    # Charts
    submittals_df = submittal_model.to_dataframe()
    if not submittals_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Submittals by Discipline")
            discipline_dist = submittals_df['discipline'].value_counts()
            st.bar_chart(discipline_dist)
        
        with col2:
            st.subheader("Submittals by Status")
            status_dist = submittals_df['status'].value_counts()
            st.bar_chart(status_dist)

# Sidebar
with st.sidebar:
    st.header("Submittal Summary")
    
    submittals = submittal_model.get_all()
    if submittals:
        st.metric("Highland Tower Submittals", len(submittals))
        
        # Recent submittals
        st.subheader("Recent Submittals")
        recent_submittals = sorted(submittals, key=lambda x: x.get('date_submitted', ''), reverse=True)[:3]
        
        for submittal in recent_submittals:
            with st.expander(f"📨 {submittal['id']}"):
                st.write(f"**Title:** {submittal['title'][:30]}...")
                st.write(f"**Discipline:** {submittal['discipline']}")
                st.write(f"**Status:** {submittal['status']}")
    
    st.markdown("---")
    st.write("**Quality Assurance**")
    st.write("Highland Tower Development maintains rigorous submittal review processes.")