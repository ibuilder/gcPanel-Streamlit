"""
RFI Management Page - Highland Tower Development
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
    page_title="RFIs - gcPanel",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("📄 Request for Information (RFI)")
st.markdown("Highland Tower Development - Information Request Management")
st.markdown("---")

# Initialize RFIs in session state if not exists
if 'rfis' not in st.session_state:
    st.session_state.rfis = [
        {
            "id": "RFI-001",
            "title": "Structural Steel Connection Detail",
            "description": "Clarification needed on beam-to-column connection detail at Grid Line B-3",
            "submittal_date": "2024-12-10",
            "discipline": "Structural",
            "priority": "High",
            "status": "Open",
            "submitted_by": "John Smith",
            "assigned_to": "Structural Engineer",
            "due_date": "2024-12-20"
        },
        {
            "id": "RFI-002", 
            "title": "HVAC Duct Routing",
            "description": "Conflict between HVAC ductwork and structural beam at Level 3",
            "submittal_date": "2024-12-12",
            "discipline": "Mechanical",
            "priority": "Medium",
            "status": "In Review",
            "submitted_by": "Mike Johnson",
            "assigned_to": "MEP Coordinator",
            "due_date": "2024-12-22"
        }
    ]

# Main content
tab1, tab2 = st.tabs(["📝 Create New RFI", "📊 View RFIs"])

with tab1:
    st.subheader("📝 Create New RFI")
    
    with st.form("rfi_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            rfi_title = st.text_input("RFI Title*", placeholder="Brief description of the information request")
            discipline = st.selectbox("Discipline", 
                ["Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil", "General"])
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            due_date = st.date_input("Response Due Date", value=date.today())
        
        with col2:
            assigned_to = st.text_input("Assigned To", placeholder="Person/Team responsible for response")
            project_location = st.text_input("Project Location", placeholder="Building area, floor, grid lines")
            drawing_reference = st.text_input("Drawing Reference", placeholder="Drawing numbers, sheet references")
            specification_reference = st.text_input("Specification Reference", placeholder="Spec section references")
        
        description = st.text_area("Detailed Description*", height=150,
            placeholder="Provide detailed description of the information needed...")
        
        submitted = st.form_submit_button("📤 Submit RFI", type="primary", use_container_width=True)
        
        if submitted and rfi_title and description:
            new_rfi = {
                "id": f"RFI-{len(st.session_state.rfis) + 1:03d}",
                "title": rfi_title,
                "description": description,
                "submittal_date": str(date.today()),
                "discipline": discipline,
                "priority": priority,
                "status": "Open",
                "submitted_by": st.session_state.get('user_name', 'User'),
                "assigned_to": assigned_to,
                "due_date": str(due_date),
                "project_location": project_location,
                "drawing_reference": drawing_reference,
                "specification_reference": specification_reference
            }
            st.session_state.rfis.insert(0, new_rfi)
            st.success(f"RFI {new_rfi['id']} submitted successfully!")
            st.rerun()
        elif submitted:
            st.error("Please fill in all required fields (*)")

with tab2:
    st.subheader("📊 RFI Database")
    
    if st.session_state.rfis:
        df = pd.DataFrame(st.session_state.rfis)
        
        # Search and filter
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search RFIs...", placeholder="Search by title, description, or ID")
        with col2:
            status_filter = st.selectbox("Status", ["All", "Open", "In Review", "Answered", "Closed"])
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
        st.write(f"**Total RFIs:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            # Priority color coding
            def get_priority_color(priority):
                colors = {
                    "Critical": "🔴",
                    "High": "🟠", 
                    "Medium": "🟡",
                    "Low": "🟢"
                }
                return colors.get(priority, "⚪")
            
            # Add priority indicators
            display_df = filtered_df.copy()
            display_df['Priority'] = display_df['priority'].apply(lambda x: f"{get_priority_color(x)} {x}")
            
            # Display with column configuration
            st.dataframe(
                clean_dataframe_for_display(display_df),
                column_config={
                    "id": st.column_config.TextColumn("RFI ID"),
                    "title": st.column_config.TextColumn("Title"),
                    "submittal_date": st.column_config.DateColumn("Submitted"),
                    "due_date": st.column_config.DateColumn("Due Date"),
                    "status": st.column_config.SelectboxColumn("Status", 
                        options=["Open", "In Review", "Answered", "Closed"]),
                    "Priority": st.column_config.TextColumn("Priority")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No RFIs found matching your criteria.")
    else:
        st.info("No RFIs available. Create your first RFI above!")

# Quick stats
col1, col2, col3, col4 = st.columns(4)
if st.session_state.rfis:
    df = pd.DataFrame(st.session_state.rfis)
    
    with col1:
        total_rfis = len(df)
        st.metric("Total RFIs", total_rfis)
    
    with col2:
        open_rfis = len(df[df['status'] == 'Open'])
        st.metric("Open RFIs", open_rfis)
    
    with col3:
        in_review = len(df[df['status'] == 'In Review'])
        st.metric("In Review", in_review)
    
    with col4:
        overdue = len(df[pd.to_datetime(df['due_date']) < pd.Timestamp.now()])
        st.metric("Overdue", overdue, delta_color="inverse")