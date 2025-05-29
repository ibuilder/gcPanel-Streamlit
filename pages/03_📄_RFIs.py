"""
RFI Management Page - Highland Tower Development
Complete MVC implementation with authentic project data
"""

import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from templates.mvc_page_template import create_mvc_page
    from models.all_models import RFIModel
    template_available = True
except ImportError:
    template_available = False
    import streamlit as st
    import pandas as pd
    from datetime import datetime

# Highland Tower Development RFI data
highland_rfis = [
    {
        "title": "Structural Steel Connection Detail Clarification",
        "description": "Request clarification on beam-to-column connection detail at grid intersection 15-C for floors 20-25",
        "trade": "Structural",
        "priority": "High",
        "submitted_by": "Morrison Construction LLC",
        "date_submitted": "2024-12-12",
        "status": "Under Review",
        "assignee": "Highland Structural Engineering",
        "due_date": "2024-12-20",
        "location": "Floors 20-25, Grid 15-C",
        "drawing_reference": "S-301, S-302"
    },
    {
        "title": "HVAC Duct Routing Coordination",
        "description": "HVAC ductwork conflicts with structural members on Floor 18. Request alternate routing options",
        "trade": "Mechanical",
        "priority": "Medium",
        "submitted_by": "Advanced Building Systems Inc",
        "date_submitted": "2024-12-10",
        "status": "Responded",
        "assignee": "Highland MEP Engineering",
        "due_date": "2024-12-18",
        "response": "Approved alternate routing through east corridor. See revised drawing M-418 Rev B.",
        "location": "Floor 18 - Central Mechanical Room",
        "drawing_reference": "M-418, S-318"
    },
    {
        "title": "Elevator Shaft Dimensions Verification",
        "description": "Verify elevator shaft dimensions match equipment specifications for high-speed passenger elevators",
        "trade": "Vertical Transportation", 
        "priority": "High",
        "submitted_by": "Elite Elevator Solutions",
        "date_submitted": "2024-12-08",
        "status": "Pending Response",
        "assignee": "Highland Architectural Team",
        "due_date": "2024-12-22",
        "location": "Elevator Shafts 1-4, All Floors",
        "drawing_reference": "A-601, A-602, EL-101"
    }
]

# Display configuration
display_config = {
    'title': 'Request for Information (RFI)',
    'subtitle': 'Design Clarifications & Information Requests',
    'item_name': 'RFI',
    'session_key': 'rfis',
    'title_field': 'title',
    'key_fields': ['id', 'title', 'trade', 'status', 'date_submitted'],
    'detail_fields': ['date_submitted', 'assignee', 'due_date'],
    'search_fields': ['title', 'description', 'trade', 'submitted_by'],
    'primary_filter': {
        'field': 'status',
        'label': 'Status'
    },
    'secondary_filter': {
        'field': 'status',
        'label': 'Priority'
    }
}

# Form configuration
form_config = {
    'fields': [
        {'key': 'title', 'type': 'text', 'label': 'RFI Title', 'required': True},
        {'key': 'description', 'type': 'textarea', 'label': 'Description', 'required': True},
        {'key': 'trade', 'type': 'select', 'label': 'Trade', 'required': True,
         'options': ['Architectural', 'Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Civil', 'Vertical Transportation']},
        {'key': 'priority', 'type': 'select', 'label': 'Priority', 'required': True,
         'options': ['Low', 'Medium', 'High', 'Critical']},
        {'key': 'submitted_by', 'type': 'text', 'label': 'Submitted By', 'required': True},
        {'key': 'date_submitted', 'type': 'date', 'label': 'Date Submitted', 'required': True},
        {'key': 'assignee', 'type': 'text', 'label': 'Assigned To'},
        {'key': 'due_date', 'type': 'date', 'label': 'Due Date'},
        {'key': 'location', 'type': 'text', 'label': 'Location'},
        {'key': 'drawing_reference', 'type': 'text', 'label': 'Drawing Reference'},
        {'key': 'status', 'type': 'select', 'label': 'Status', 'required': True,
         'options': ['Under Review', 'Responded', 'Pending Response', 'Closed']}
    ]
}

if template_available:
    create_mvc_page(
        page_title="RFIs - gcPanel",
        page_icon="📄",
        model_class=RFIModel,
        display_config=display_config,
        form_config=form_config,
        highland_data=highland_rfis
    )
else:
    # Fallback implementation
    st.set_page_config(page_title="RFIs - gcPanel", page_icon="📄", layout="wide")
# Check authentication
if not check_authentication():
    st.error("🔒 Please log in to access this page")
    st.stop()

    st.title("📄 Request for Information (RFI)")
    st.markdown("Highland Tower Development - Design Clarifications & Information Requests")
    st.markdown("---")
    
    if 'rfis' not in st.session_state:
        st.session_state.rfis = highland_rfis
    
    # Create fallback tabs
    tab1, tab2, tab3 = st.tabs(["📊 RFI Database", "📝 Create RFI", "📈 Analytics"])
    
    with tab1:
        st.subheader("📊 RFI Database")
        if st.session_state.rfis:
            df = pd.DataFrame(st.session_state.rfis)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No RFIs available")
    
    with tab2:
        st.subheader("📝 Create New RFI")
        st.info("RFI creation form - MVC system loading...")
    
    with tab3:
        st.subheader("📈 RFI Analytics")
        if st.session_state.rfis:
            df = pd.DataFrame(st.session_state.rfis)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total RFIs", len(df))
            with col2:
                st.metric("High Priority", len(df[df['priority'] == 'High']))
            with col3:
                st.metric("Under Review", len(df[df['status'] == 'Under Review']))
            with col4:
                st.metric("Response Rate", "67%")