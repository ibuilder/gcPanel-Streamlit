"""
RFI Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="RFIs - gcPanel", page_icon="📄", layout="wide")

def clean_dataframe_for_display(df):
    """Clean DataFrame to prevent Arrow serialization errors"""
    if df.empty:
        return df
    cleaned_df = df.copy()
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype == 'object':
            cleaned_df[col] = cleaned_df[col].astype(str)
    return cleaned_df

st.title("📄 Request for Information (RFI)")
st.markdown("Highland Tower Development - Design Clarifications & Information Requests")
st.markdown("---")

if 'rfis' not in st.session_state:
    st.session_state.rfis = [
        {
            "id": "RFI-001",
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
            "id": "RFI-002",
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
            "id": "RFI-003",
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

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📊 RFI Database", "📝 Create RFI", "📈 Analytics"])

with tab1:
    st.subheader("📊 RFI Database")
    
    if st.session_state.rfis:
        df = pd.DataFrame(st.session_state.rfis)
        
        # Search and filter
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search RFIs...", key="rfis_search")
        with col2:
            status_filter = st.selectbox("Status", ["All", "Under Review", "Responded", "Pending Response"])
        with col3:
            priority_filter = st.selectbox("Priority", ["All", "Low", "Medium", "High", "Critical"])
        
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
            
        if priority_filter != "All":
            filtered_df = filtered_df[filtered_df['priority'] == priority_filter]
        
        st.write(f"**Total RFIs:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            # View mode toggle
            view_mode = st.radio("View Mode:", ["📊 Table View", "📋 Card View"], horizontal=True, key="rfis_view_mode")
            
            if view_mode == "📊 Table View":
                st.dataframe(clean_dataframe_for_display(filtered_df), use_container_width=True, hide_index=True)
            else:
                # Card view with actions
                for idx, row in filtered_df.iterrows():
                    with st.container():
                        st.markdown("---")
                        col1, col2, col3 = st.columns([3, 2, 1])
                        
                        with col1:
                            st.subheader(f"📄 {row['title']}")
                            st.write(f"**ID:** {row['id']} | **Priority:** {row['priority']}")
                            st.write(f"**Trade:** {row['trade']}")
                        
                        with col2:
                            st.write(f"**Submitted:** {row['date_submitted']}")
                            st.write(f"**Status:** {row['status']}")
                            st.write(f"**Submitted By:** {row['submitted_by']}")
                        
                        with col3:
                            if st.button("👁️ View", key=f"view_rfi_{row['id']}", help="View details"):
                                with st.expander("RFI Details", expanded=True):
                                    for key, value in row.items():
                                        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
                            if st.button("✏️ Edit", key=f"edit_rfi_{row['id']}", help="Edit RFI"):
                                st.info(f"Edit functionality for RFI {row['id']} - Feature coming soon!")
        else:
            st.info("No RFIs found matching your criteria.")
    else:
        st.info("No RFIs available. Create your first RFI in the Create tab!")

with tab2:
    st.subheader("📝 Create New RFI")
    
    with st.form("rfi_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("RFI Title", placeholder="Brief descriptive title")
            trade = st.selectbox("Trade", ["Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil", "Vertical Transportation"])
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            submitted_by = st.text_input("Submitted By", placeholder="Company name")
        
        with col2:
            date_submitted = st.date_input("Date Submitted", datetime.now().date())
            status = st.selectbox("Status", ["Under Review", "Responded", "Pending Response", "Closed"])
            due_date = st.date_input("Due Date")
            assignee = st.text_input("Assigned To", placeholder="Responsible party")
        
        description = st.text_area("Description", placeholder="Detailed description of the request")
        location = st.text_input("Location", placeholder="Project location reference")
        drawing_reference = st.text_input("Drawing Reference", placeholder="Related drawing numbers")
        
        submitted = st.form_submit_button("Create RFI")
        
        if submitted and title and description:
            new_rfi = {
                "id": f"RFI-{len(st.session_state.rfis) + 1:03d}",
                "title": title,
                "description": description,
                "trade": trade,
                "priority": priority,
                "submitted_by": submitted_by,
                "date_submitted": date_submitted.strftime("%Y-%m-%d"),
                "status": status,
                "assignee": assignee,
                "due_date": due_date.strftime("%Y-%m-%d") if due_date else "",
                "location": location,
                "drawing_reference": drawing_reference
            }
            
            st.session_state.rfis.append(new_rfi)
            st.success(f"RFI {new_rfi['id']} created successfully!")
            st.rerun()

with tab3:
    st.subheader("📈 RFI Analytics")
    
    if st.session_state.rfis:
        df = pd.DataFrame(st.session_state.rfis)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total RFIs", len(df))
        
        with col2:
            under_review = len(df[df['status'] == 'Under Review'])
            st.metric("Under Review", under_review)
        
        with col3:
            high_priority = len(df[df['priority'] == 'High'])
            st.metric("High Priority", high_priority)
        
        with col4:
            responded = len(df[df['status'] == 'Responded'])
            response_rate = (responded / len(df) * 100) if len(df) > 0 else 0
            st.metric("Response Rate", f"{response_rate:.1f}%")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("RFIs by Trade")
            trade_counts = df['trade'].value_counts()
            st.bar_chart(trade_counts)
        
        with col2:
            st.subheader("RFIs by Priority")
            priority_counts = df['priority'].value_counts()
            st.bar_chart(priority_counts)
    else:
        st.info("No RFIs available yet. Create your first RFI to see analytics!")