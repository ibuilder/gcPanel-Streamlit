"""
Engineering Module for gcPanel

This module provides engineering management functionality for the construction management dashboard,
with a focus on Submittal Packages and Transmittals using the standardized CRUD styling.
"""

import streamlit as st
from modules.engineering.submittal_packages import render as render_submittal_packages
from modules.engineering.transmittals import render as render_transmittals

def render_rfi_automation_dashboard():
    """Render RFI workflow automation dashboard"""
    st.markdown("### 🤖 RFI Workflow Automation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Active RFIs**")
        rfis = [
            {"id": "RFI-001", "subject": "Foundation Detail Clarification", "status": "Pending Response", "days": 3},
            {"id": "RFI-002", "subject": "HVAC Equipment Specifications", "status": "Under Review", "days": 1},
            {"id": "RFI-003", "subject": "Window Installation Method", "status": "Answered", "days": 0}
        ]
        
        for rfi in rfis:
            status_color = "#ff8800" if rfi["status"] == "Pending Response" else "#4CAF50" if rfi["status"] == "Answered" else "#2196F3"
            st.markdown(f"""
                <div style="border-left: 4px solid {status_color}; padding: 10px; margin: 5px 0; background-color: #f8f9fa;">
                    <strong>{rfi["id"]}</strong>: {rfi["subject"]}<br>
                    <small>Status: {rfi["status"]} | Days Open: {rfi["days"]}</small>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Automated Routing**")
        st.markdown("✅ Auto-assign based on trade")
        st.markdown("✅ Priority escalation after 48hrs")
        st.markdown("✅ Notification to all stakeholders")
        st.markdown("📊 Average response time: 2.3 days")

def render_drawing_revision_control():
    """Render drawing revision control system"""
    st.markdown("### 📐 Drawing Revision Control")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Recent Revisions**")
        revisions = [
            {"drawing": "A-101", "revision": "C", "date": "2025-05-20", "changes": "Updated door schedule"},
            {"drawing": "S-102", "revision": "B", "date": "2025-05-18", "changes": "Beam size revision"},
            {"drawing": "M-201", "revision": "A", "date": "2025-05-15", "changes": "Equipment relocation"}
        ]
        
        for rev in revisions:
            st.markdown(f"""
                <div style="padding: 10px; margin: 5px 0; background-color: #f0f8ff; border-radius: 5px;">
                    <strong>{rev["drawing"]} Rev {rev["revision"]}</strong><br>
                    <small>{rev["date"]}: {rev["changes"]}</small>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Version Control Features**")
        st.markdown("🔄 Automatic version tracking")
        st.markdown("📋 Change log documentation")
        st.markdown("👥 Multi-user collaboration")
        st.markdown("🔍 Side-by-side comparison")

def render_technical_review_system():
    """Render technical review checklist system"""
    st.markdown("### ✅ Technical Review Checklists")
    
    review_items = [
        {"category": "Structural", "completed": 8, "total": 10, "status": "In Progress"},
        {"category": "MEP Coordination", "completed": 12, "total": 12, "status": "Complete"},
        {"category": "Fire Protection", "completed": 5, "total": 8, "status": "In Progress"},
        {"category": "Code Compliance", "completed": 15, "total": 18, "status": "In Progress"}
    ]
    
    for item in review_items:
        progress = item["completed"] / item["total"]
        status_color = "#4CAF50" if item["status"] == "Complete" else "#ff8800"
        
        st.markdown(f"""
            <div style="margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong>{item["category"]}</strong>
                    <span style="color: {status_color};">{item["status"]}</span>
                </div>
                <div style="margin-top: 5px;">
                    Progress: {item["completed"]}/{item["total"]} ({progress:.0%})
                </div>
            </div>
        """, unsafe_allow_html=True)

def render():
    """Render the Engineering Management module."""
    st.title("🔧 Engineering Management")
    
    # Create tabs for different engineering functions
    tab1, tab2, tab3, tab4 = st.tabs(["📋 RFIs", "📦 Submittals", "📄 Transmittals", "📊 Dashboard"])
    
    # RFIs Tab
    with tab1:
        render_rfi_management()
    
    # Submittals Tab
    with tab2:
        render_submittal_management()
    
    # Transmittals Tab
    with tab3:
        render_transmittals()
        
    # Dashboard Tab
    with tab4:
        render_engineering_dashboard()

def render_rfi_management():
    """Render comprehensive RFI management for Highland Tower Development"""
    st.header("📋 Request for Information (RFI) Management")
    
    # RFI Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Open RFIs", "7", "+2 this week")
    with col2:
        st.metric("Avg Response Time", "2.3 days", "-0.5 days")
    with col3:
        st.metric("Critical RFIs", "2", "⚠️ Attention needed")
    with col4:
        st.metric("This Month", "15", "+8 from last month")
    
    # Quick actions
    st.markdown("#### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ New RFI", type="primary", use_container_width=True, key="new_rfi_btn"):
            st.session_state['show_rfi_form'] = True
            st.rerun()
    
    with col2:
        if st.button("📊 RFI Analytics", type="secondary", use_container_width=True, key="rfi_analytics_btn"):
            st.session_state['show_rfi_analytics'] = True
            st.rerun()
    
    with col3:
        if st.button("📤 Export RFIs", type="secondary", use_container_width=True, key="export_rfi_btn"):
            st.success("RFI data exported successfully!")
    
    # RFI List with filters
    st.markdown("#### Active RFIs - Highland Tower Development")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Status", ["All", "Open", "Pending Response", "Under Review", "Answered", "Closed"])
    with col2:
        priority_filter = st.selectbox("Priority", ["All", "Critical", "High", "Medium", "Low"])
    with col3:
        trade_filter = st.selectbox("Trade", ["All", "Structural", "Architectural", "MEP", "Civil", "Other"])
    
    # Highland Tower Development RFI data
    rfis = [
        {
            "rfi_id": "RFI-HTD-001",
            "subject": "Foundation Detail Clarification - Tower Base",
            "trade": "Structural",
            "status": "Pending Response",
            "priority": "High",
            "submitted_date": "2025-05-20",
            "due_date": "2025-05-27",
            "submitted_by": "Mike Johnson",
            "assigned_to": "Jennifer Wilson",
            "days_open": 4,
            "description": "Need clarification on foundation details at grid lines A1-A3 for Highland Tower base connection to existing structure."
        },
        {
            "rfi_id": "RFI-HTD-002",
            "subject": "HVAC Equipment Specifications - Penthouse Level",
            "trade": "MEP",
            "status": "Under Review",
            "priority": "Medium",
            "submitted_date": "2025-05-22",
            "due_date": "2025-05-29",
            "submitted_by": "Sarah Thompson",
            "assigned_to": "David Chen",
            "days_open": 2,
            "description": "Seeking specifications for rooftop HVAC equipment for Highland Tower penthouse level including capacity requirements."
        },
        {
            "rfi_id": "RFI-HTD-003",
            "subject": "Curtain Wall Connection Details - Floors 8-15",
            "trade": "Architectural",
            "status": "Answered",
            "priority": "Critical",
            "submitted_date": "2025-05-18",
            "due_date": "2025-05-25",
            "submitted_by": "Lisa Rodriguez",
            "assigned_to": "Jennifer Wilson",
            "days_open": 0,
            "description": "Critical connection details needed for curtain wall installation on upper floors of Highland Tower."
        },
        {
            "rfi_id": "RFI-HTD-004",
            "subject": "Elevator Shaft Dimensions - Service Elevator",
            "trade": "Structural",
            "status": "Open",
            "priority": "High",
            "submitted_date": "2025-05-23",
            "due_date": "2025-05-30",
            "submitted_by": "Carlos Rivera",
            "assigned_to": "Mike Johnson",
            "days_open": 1,
            "description": "Service elevator shaft dimensions conflict between architectural and structural drawings."
        }
    ]
    
    # Display RFIs in enhanced format
    for rfi in rfis:
        with st.container():
            st.markdown("---")
            
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                priority_color = "#ef4444" if rfi["priority"] == "Critical" else "#ff8800" if rfi["priority"] == "High" else "#4CAF50"
                st.markdown(f"**{rfi['rfi_id']}**: {rfi['subject']}")
                st.markdown(f"<small style='color: {priority_color};'>● {rfi['priority']} Priority | {rfi['trade']}</small>", unsafe_allow_html=True)
            
            with col2:
                status_color = "#ef4444" if rfi["status"] == "Pending Response" else "#ff8800" if rfi["status"] == "Under Review" else "#4CAF50"
                st.markdown(f"<span style='color: {status_color}; font-weight: bold;'>{rfi['status']}</span>", unsafe_allow_html=True)
                st.markdown(f"<small>Due: {rfi['due_date']}</small>", unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"**{rfi['days_open']}** days open")
                st.markdown(f"<small>{rfi['assigned_to']}</small>", unsafe_allow_html=True)
            
            with col4:
                if st.button("View Details", key=f"view_rfi_{rfi['rfi_id']}", use_container_width=True):
                    st.session_state[f'show_rfi_detail_{rfi["rfi_id"]}'] = True
                    st.rerun()

def render_submittal_management():
    """Render comprehensive Submittal management for Highland Tower Development"""
    st.header("📦 Submittal Management")
    
    # Submittal Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Submittals", "23", "+5 this week")
    with col2:
        st.metric("Avg Review Time", "4.2 days", "+0.3 days")
    with col3:
        st.metric("Pending Review", "8", "⏳ Review needed")
    with col4:
        st.metric("Approved This Month", "18", "+12 from last month")
    
    # Quick actions
    st.markdown("#### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ New Submittal", type="primary", use_container_width=True, key="new_submittal_btn"):
            st.session_state['show_submittal_form'] = True
            st.rerun()
    
    with col2:
        if st.button("📊 Submittal Analytics", type="secondary", use_container_width=True, key="submittal_analytics_btn"):
            st.session_state['show_submittal_analytics'] = True
            st.rerun()
    
    with col3:
        if st.button("📤 Export Submittals", type="secondary", use_container_width=True, key="export_submittal_btn"):
            st.success("Submittal data exported successfully!")
    
    # Submittal List with filters
    st.markdown("#### Active Submittals - Highland Tower Development")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Status", ["All", "Submitted", "Under Review", "Revise & Resubmit", "Approved", "Rejected"], key="submittal_status_filter")
    with col2:
        type_filter = st.selectbox("Type", ["All", "Shop Drawings", "Product Data", "Samples", "Mix Designs", "Test Reports"], key="submittal_type_filter")
    with col3:
        trade_filter = st.selectbox("Trade", ["All", "Structural Steel", "Concrete", "MEP", "Architectural", "Finishes"], key="submittal_trade_filter")
    
    # Highland Tower Development Submittal data
    submittals = [
        {
            "submittal_id": "SUB-HTD-001",
            "title": "Structural Steel Shop Drawings - Floors 1-5",
            "type": "Shop Drawings",
            "trade": "Structural Steel",
            "status": "Under Review",
            "submitted_date": "2025-05-20",
            "due_date": "2025-05-27",
            "submitted_by": "Highland Steel Works",
            "reviewer": "Jennifer Wilson",
            "days_in_review": 4,
            "revision": "Rev 0"
        },
        {
            "submittal_id": "SUB-HTD-002",
            "title": "Curtain Wall System Product Data",
            "type": "Product Data",
            "trade": "Architectural",
            "status": "Approved",
            "submitted_date": "2025-05-15",
            "due_date": "2025-05-22",
            "submitted_by": "Facade Systems Inc",
            "reviewer": "Lisa Rodriguez",
            "days_in_review": 0,
            "revision": "Rev 1"
        },
        {
            "submittal_id": "SUB-HTD-003",
            "title": "HVAC Equipment Cut Sheets - Penthouse",
            "type": "Product Data",
            "trade": "MEP",
            "status": "Revise & Resubmit",
            "submitted_date": "2025-05-18",
            "due_date": "2025-05-25",
            "submitted_by": "Climate Control LLC",
            "reviewer": "David Chen",
            "days_in_review": 2,
            "revision": "Rev 0"
        },
        {
            "submittal_id": "SUB-HTD-004",
            "title": "Concrete Mix Design - High Strength",
            "type": "Mix Designs",
            "trade": "Concrete",
            "status": "Submitted",
            "submitted_date": "2025-05-23",
            "due_date": "2025-05-30",
            "submitted_by": "Reliable Concrete LLC",
            "reviewer": "Mike Johnson",
            "days_in_review": 1,
            "revision": "Rev 0"
        }
    ]
    
    # Display Submittals in enhanced format
    for submittal in submittals:
        with st.container():
            st.markdown("---")
            
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                st.markdown(f"**{submittal['submittal_id']}**: {submittal['title']}")
                st.markdown(f"<small>🔧 {submittal['trade']} | 📋 {submittal['type']} | {submittal['revision']}</small>", unsafe_allow_html=True)
            
            with col2:
                status_colors = {
                    "Submitted": "#2196F3",
                    "Under Review": "#ff8800", 
                    "Revise & Resubmit": "#ef4444",
                    "Approved": "#4CAF50",
                    "Rejected": "#ef4444"
                }
                status_color = status_colors.get(submittal["status"], "#666")
                st.markdown(f"<span style='color: {status_color}; font-weight: bold;'>{submittal['status']}</span>", unsafe_allow_html=True)
                st.markdown(f"<small>Due: {submittal['due_date']}</small>", unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"**{submittal['days_in_review']}** days in review")
                st.markdown(f"<small>{submittal['reviewer']}</small>", unsafe_allow_html=True)
            
            with col4:
                if st.button("View Details", key=f"view_submittal_{submittal['submittal_id']}", use_container_width=True):
                    st.session_state[f'show_submittal_detail_{submittal["submittal_id"]}'] = True
                    st.rerun()

def render_engineering_dashboard():
    """Render engineering dashboard with analytics"""
    st.header("📊 Engineering Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_rfi_automation_dashboard()
    
    with col2:
        render_drawing_revision_control()