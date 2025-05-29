"""
Submittals Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(
    page_title="Submittals - gcPanel",
    page_icon="📨",
    layout="wide"
)

# Initialize session state
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("📨 Submittals Management")
st.markdown("Highland Tower Development - Document Submittal Tracking")
st.markdown("---")

# Initialize submittals in session state if not exists
if 'submittals' not in st.session_state:
    st.session_state.submittals = [
        {
            "id": "SUB-001",
            "title": "Structural Steel Shop Drawings",
            "specification": "05 12 00",
            "submittal_date": "2024-12-08",
            "discipline": "Structural",
            "status": "Under Review",
            "submitted_by": "Steel Fabricator Inc.",
            "reviewer": "Structural Engineer",
            "due_date": "2024-12-18",
            "revision": "Rev 1"
        },
        {
            "id": "SUB-002",
            "title": "HVAC Equipment Schedules",
            "specification": "23 00 00",
            "submittal_date": "2024-12-10",
            "discipline": "Mechanical",
            "status": "Approved",
            "submitted_by": "HVAC Contractor LLC",
            "reviewer": "MEP Engineer",
            "due_date": "2024-12-20",
            "revision": "Rev 0"
        }
    ]

# Main content
tab1, tab2 = st.tabs(["📊 Submittals Database", "📝 Create New Submittal"])

with tab1:
    st.subheader("📊 Submittals Database")
    
    if st.session_state.submittals:
        df = pd.DataFrame(st.session_state.submittals)
        
        # Search and filter
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search submittals...", placeholder="Search by title, spec, or ID", key="submittals_search_1")
        with col2:
            status_filter = st.selectbox("Status", ["All", "Under Review", "Approved", "Rejected", "Resubmit Required"])
        with col3:
            discipline_filter = st.selectbox("Discipline", ["All", "Architectural", "Structural", "Mechanical", "Electrical"])
        
        # Filter data
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[
                filtered_df.astype(str).apply(
                    lambda x: x.str.contains(search_term, case=False, na=False)
                ).any(axis=1)
            ]
        
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
            
        if discipline_filter != "All":
            filtered_df = filtered_df[filtered_df['discipline'] == discipline_filter]
        
        # Display results
        st.write(f"**Total Submittals:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            # Status color coding
            def get_status_indicator(status):
                indicators = {
                    "Under Review": "🟡",
                    "Approved": "🟢",
                    "Rejected": "🔴",
                    "Resubmit Required": "🟠"
                }
                return indicators.get(status, "⚪")
            
            # Add status indicators
            display_df = filtered_df.copy()
            display_df['Status'] = display_df['status'].apply(lambda x: f"{get_status_indicator(x)} {x}")
            
            # Display with column configuration
            st.dataframe(
                clean_dataframe_for_display(display_df),
                column_config={
                    "id": st.column_config.TextColumn("Submittal ID"),
                    "title": st.column_config.TextColumn("Title"),
                    "specification": st.column_config.TextColumn("Spec Section"),
                    "submittal_date": st.column_config.DateColumn("Submitted"),
                    "due_date": st.column_config.DateColumn("Due Date"),
                    "Status": st.column_config.TextColumn("Status"),
                    "submitted_by": st.column_config.TextColumn("Submitted By"),
                    "reviewer": st.column_config.TextColumn("Reviewer")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No submittals found matching your criteria.")
    else:
        st.info("No submittals available. Create your first submittal in the Create tab!")

with tab2:
    st.subheader("📝 Create New Submittal")
    
    with st.form("submittal_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            submittal_title = st.text_input("Submittal Title*", placeholder="Description of submittal package")
            specification = st.text_input("Specification Section", placeholder="e.g., 05 12 00")
            discipline = st.selectbox("Discipline", 
                ["Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil", "General"])
            submitted_by = st.text_input("Submitted By*", placeholder="Contractor/Vendor name")
        
        with col2:
            reviewer = st.text_input("Reviewer", placeholder="Assigned reviewer")
            due_date = st.date_input("Review Due Date", value=date.today())
            revision = st.text_input("Revision", value="Rev 0", placeholder="e.g., Rev 1")
            submittal_type = st.selectbox("Type", ["Shop Drawings", "Product Data", "Samples", "Mix Designs", "Other"])
        
        description = st.text_area("Description & Notes", height=100,
            placeholder="Additional details about the submittal...")
        
        submitted = st.form_submit_button("📤 Submit for Review", type="primary", use_container_width=True)
        
        if submitted and submittal_title and submitted_by:
            new_submittal = {
                "id": f"SUB-{len(st.session_state.submittals) + 1:03d}",
                "title": submittal_title,
                "specification": specification,
                "submittal_date": str(date.today()),
                "discipline": discipline,
                "status": "Under Review",
                "submitted_by": submitted_by,
                "reviewer": reviewer,
                "due_date": str(due_date),
                "revision": revision,
                "type": submittal_type,
                "description": description
            }
            st.session_state.submittals.insert(0, new_submittal)
            st.success(f"Submittal {new_submittal['id']} created successfully!")
            st.rerun()
        elif submitted:
            st.error("Please fill in all required fields (*)")

with tab2:
    st.subheader("📊 Submittals Database")
    
    if st.session_state.submittals:
        df = pd.DataFrame(st.session_state.submittals)
        
        # Search and filter
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search submittals...", placeholder="Search by title, spec, or ID", key="submittals_search_2")
        with col2:
            status_filter = st.selectbox("Status", ["All", "Under Review", "Approved", "Rejected", "Resubmit Required"])
        with col3:
            discipline_filter = st.selectbox("Discipline", ["All", "Architectural", "Structural", "Mechanical", "Electrical"])
        
        # Filter data
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[
                filtered_df.astype(str).apply(
                    lambda x: x.str.contains(search_term, case=False, na=False)
                ).any(axis=1)
            ]
        
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
            
        if discipline_filter != "All":
            filtered_df = filtered_df[filtered_df['discipline'] == discipline_filter]
        
        # Display results
        st.write(f"**Total Submittals:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            # Status color coding
            def get_status_indicator(status):
                indicators = {
                    "Under Review": "🟡",
                    "Approved": "🟢",
                    "Rejected": "🔴",
                    "Resubmit Required": "🟠"
                }
                return indicators.get(status, "⚪")
            
            # Add status indicators
            display_df = filtered_df.copy()
            display_df['Status'] = display_df['status'].apply(lambda x: f"{get_status_indicator(x)} {x}")
            
            # Display with column configuration
            st.dataframe(
                clean_dataframe_for_display(display_df),
                column_config={
                    "id": st.column_config.TextColumn("Submittal ID"),
                    "title": st.column_config.TextColumn("Title"),
                    "specification": st.column_config.TextColumn("Spec Section"),
                    "submittal_date": st.column_config.DateColumn("Submitted"),
                    "due_date": st.column_config.DateColumn("Due Date"),
                    "Status": st.column_config.TextColumn("Status"),
                    "submitted_by": st.column_config.TextColumn("Submitted By"),
                    "reviewer": st.column_config.TextColumn("Reviewer")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No submittals found matching your criteria.")
    else:
        st.info("No submittals available. Create your first submittal above!")

# Quick stats
col1, col2, col3, col4 = st.columns(4)
if st.session_state.submittals:
    df = pd.DataFrame(st.session_state.submittals)
    
    with col1:
        total_submittals = len(df)
        st.metric("Total Submittals", total_submittals)
    
    with col2:
        under_review = len(df[df['status'] == 'Under Review'])
        st.metric("Under Review", under_review)
    
    with col3:
        approved = len(df[df['status'] == 'Approved'])
        st.metric("Approved", approved)
    
    with col4:
        overdue = len(df[pd.to_datetime(df['due_date']) < pd.Timestamp.now()])
        st.metric("Overdue", overdue, delta_color="inverse")