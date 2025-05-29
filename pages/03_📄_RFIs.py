"""
RFI Management Page - Highland Tower Development
Refactored using MVC pattern with models, controllers, and helpers
"""

import streamlit as st
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.rfi_model import RFIModel
from controllers.crud_controller import CRUDController
from helpers.ui_helpers import render_highland_header, apply_highland_tower_styling

# Page configuration
st.set_page_config(page_title="RFIs - gcPanel", page_icon="📄", layout="wide")

# Apply styling
apply_highland_tower_styling()

# Render header
render_highland_header("📄 Request for Information (RFI)", "Highland Tower Development - Design Clarifications")

# Initialize model
rfi_model = RFIModel()

# Display configuration
display_config = {
    'title': 'RFIs',
    'item_name': 'RFI',
    'title_field': 'title',
    'key_fields': ['id', 'priority', 'trade'],
    'detail_fields': ['date_submitted', 'status', 'assignee'],
    'search_fields': ['title', 'description', 'trade', 'submitted_by'],
    'primary_filter': {
        'field': 'status',
        'label': 'Status'
    },
    'secondary_filter': {
        'field': 'priority',
        'label': 'Priority'
    },
    'column_config': {
        "id": st.column_config.TextColumn("RFI ID"),
        "title": st.column_config.TextColumn("Title"),
        "trade": st.column_config.TextColumn("Trade"),
        "priority": st.column_config.TextColumn("Priority"),
        "submitted_by": st.column_config.TextColumn("Submitted By"),
        "date_submitted": st.column_config.DateColumn("Date Submitted"),
        "status": st.column_config.TextColumn("Status"),
        "due_date": st.column_config.DateColumn("Due Date")
    }
}

# Form configuration
form_config = {
    'fields': [
        {'key': 'title', 'type': 'text', 'label': 'RFI Title', 'placeholder': 'Brief descriptive title'},
        {'key': 'description', 'type': 'textarea', 'label': 'Description', 'placeholder': 'Detailed description of the request'},
        {'key': 'trade', 'type': 'select', 'label': 'Trade',
         'options': ['Architectural', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Civil', 'Vertical Transportation']},
        {'key': 'priority', 'type': 'select', 'label': 'Priority',
         'options': ['Low', 'Medium', 'High', 'Critical']},
        {'key': 'submitted_by', 'type': 'text', 'label': 'Submitted By', 'placeholder': 'Company name'},
        {'key': 'date_submitted', 'type': 'date', 'label': 'Date Submitted'},
        {'key': 'assignee', 'type': 'text', 'label': 'Assigned To', 'placeholder': 'Responsible party'},
        {'key': 'due_date', 'type': 'date', 'label': 'Due Date'},
        {'key': 'location', 'type': 'text', 'label': 'Location', 'placeholder': 'Project location reference'},
        {'key': 'drawing_reference', 'type': 'text', 'label': 'Drawing Reference', 'placeholder': 'Drawing numbers'}
    ]
}

# Initialize controller
crud_controller = CRUDController(rfi_model, 'rfis', display_config)

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📊 RFI Database", "📝 Create RFI", "📈 RFI Analytics"])

with tab1:
    crud_controller.render_data_view('rfis')

with tab2:
    crud_controller.render_create_form(form_config)

with tab3:
    st.subheader("📈 RFI Performance Analytics")
    
    # RFI metrics
    total_rfis = len(rfi_model.get_all())
    pending_rfis = len(rfi_model.get_pending_rfis())
    overdue_rfis = len(rfi_model.get_overdue_rfis())
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total RFIs", total_rfis)
    
    with col2:
        st.metric("Pending Response", pending_rfis)
    
    with col3:
        st.metric("Overdue", overdue_rfis)
    
    with col4:
        response_rate = ((total_rfis - pending_rfis) / total_rfis * 100) if total_rfis > 0 else 100
        st.metric("Response Rate", f"{response_rate:.1f}%")
    
    # RFI analysis charts
    rfis_df = rfi_model.to_dataframe()
    if not rfis_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("RFIs by Trade")
            trade_dist = rfis_df['trade'].value_counts()
            st.bar_chart(trade_dist)
        
        with col2:
            st.subheader("RFIs by Priority")
            priority_dist = rfis_df['priority'].value_counts()
            st.bar_chart(priority_dist)

# Sidebar
with st.sidebar:
    st.header("RFI Summary")
    
    rfis = rfi_model.get_all()
    if rfis:
        st.metric("Highland Tower RFIs", len(rfis))
        
        # High priority RFIs
        high_priority = rfi_model.get_rfis_by_priority('High')
        st.metric("High Priority", len(high_priority))
        
        # Recent RFIs
        st.subheader("Recent RFIs")
        recent_rfis = sorted(rfis, key=lambda x: x.get('date_submitted', ''), reverse=True)[:3]
        
        for rfi in recent_rfis:
            with st.expander(f"📄 {rfi['id']}"):
                st.write(f"**Title:** {rfi['title'][:40]}...")
                st.write(f"**Trade:** {rfi['trade']}")
                st.write(f"**Priority:** {rfi['priority']}")
                st.write(f"**Status:** {rfi['status']}")
    
    st.markdown("---")
    st.write("**Design Coordination**")
    st.write("Ensuring clear communication and timely resolution of design questions for Highland Tower Development.")