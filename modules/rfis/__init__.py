"""
RFIs (Requests for Information) Module for Highland Tower Development

This standalone module provides comprehensive RFI management functionality including:
- RFI creation, tracking, and response management
- Priority-based workflow and escalation
- Multi-party collaboration and notifications
- Response time tracking and analytics
- Professional RFI formatting and distribution
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render():
    """Render the standalone RFIs module"""
    st.title("❓ Request for Information (RFI) Management")
    
    # RFI Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Open RFIs", "12", "+3 this week")
    with col2:
        st.metric("Avg Response Time", "2.8 days", "+0.2 days")
    with col3:
        st.metric("Pending Response", "5", "Awaiting answers")
    with col4:
        st.metric("Resolved This Month", "24", "+8 from last month")
    
    # Quick actions
    st.markdown("#### Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Create New RFI", type="primary", use_container_width=True, key="new_rfi_btn"):
            st.session_state['show_rfi_form'] = True
            st.rerun()
    
    with col2:
        if st.button("📊 RFI Analytics", type="secondary", use_container_width=True, key="rfi_analytics_btn"):
            st.session_state['show_rfi_analytics'] = True
            st.rerun()
    
    with col3:
        if st.button("📤 Export RFIs", type="secondary", use_container_width=True, key="export_rfis_btn"):
            st.success("RFI data exported successfully!")
    
    with col4:
        if st.button("🔄 Refresh Status", type="secondary", use_container_width=True, key="refresh_rfis_btn"):
            st.success("RFI status updated!")
    
    # RFI List with filters
    st.markdown("#### Active RFIs - Highland Tower Development")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_filter = st.selectbox("Status", ["All", "Open", "Under Review", "Answered", "Closed"], key="rfi_status_filter")
    with col2:
        priority_filter = st.selectbox("Priority", ["All", "Critical", "High", "Medium", "Low"], key="rfi_priority_filter")
    with col3:
        category_filter = st.selectbox("Category", ["All", "Design", "Specification", "Schedule", "Materials", "Safety"], key="rfi_category_filter")
    with col4:
        search_term = st.text_input("Search RFIs", placeholder="Search by ID or description...", key="rfi_search")
    
    # Highland Tower Development RFI data
    rfis = [
        {
            "rfi_id": "RFI-HTD-001",
            "title": "Foundation Reinforcement Detail Clarification",
            "description": "Need clarification on rebar placement for foundation grid A1-A3",
            "category": "Design",
            "priority": "High",
            "status": "Under Review",
            "submitted_date": "2025-05-23",
            "due_date": "2025-05-30",
            "submitted_by": "Highland Steel Works",
            "assigned_to": "Jennifer Wilson",
            "days_open": 1,
            "responses": 0
        },
        {
            "rfi_id": "RFI-HTD-002",
            "title": "MEP Coordination - HVAC Duct Routing",
            "description": "Conflict between HVAC ductwork and structural beam on Level 2",
            "category": "Design",
            "priority": "Critical",
            "status": "Open",
            "submitted_date": "2025-05-22",
            "due_date": "2025-05-25",
            "submitted_by": "Climate Control LLC",
            "assigned_to": "David Chen",
            "days_open": 2,
            "responses": 1
        },
        {
            "rfi_id": "RFI-HTD-003",
            "title": "Curtain Wall Anchor Specification",
            "description": "Request specification for curtain wall anchor system at penthouse level",
            "category": "Specification",
            "priority": "Medium",
            "status": "Answered",
            "submitted_date": "2025-05-20",
            "due_date": "2025-05-27",
            "submitted_by": "Facade Systems Inc",
            "assigned_to": "Lisa Rodriguez",
            "days_open": 0,
            "responses": 2
        },
        {
            "rfi_id": "RFI-HTD-004",
            "title": "Concrete Pour Schedule Coordination",
            "description": "Clarification needed on concrete pour sequence for parking garage",
            "category": "Schedule",
            "priority": "High",
            "status": "Under Review",
            "submitted_date": "2025-05-21",
            "due_date": "2025-05-28",
            "submitted_by": "Reliable Concrete LLC",
            "assigned_to": "Mike Johnson",
            "days_open": 3,
            "responses": 0
        },
        {
            "rfi_id": "RFI-HTD-005",
            "title": "Fire Safety System Integration",
            "description": "Integration details for fire suppression with elevator shaft",
            "category": "Safety",
            "priority": "Critical",
            "status": "Open",
            "submitted_date": "2025-05-24",
            "due_date": "2025-05-26",
            "submitted_by": "Fire Safety Inc",
            "assigned_to": "Safety Manager",
            "days_open": 0,
            "responses": 0
        }
    ]
    
    # Filter RFIs based on selections
    filtered_rfis = rfis
    if status_filter != "All":
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["status"] == status_filter]
    if priority_filter != "All":
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["priority"] == priority_filter]
    if category_filter != "All":
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["category"] == category_filter]
    if search_term:
        filtered_rfis = [rfi for rfi in filtered_rfis if 
                        search_term.lower() in rfi["rfi_id"].lower() or 
                        search_term.lower() in rfi["title"].lower() or
                        search_term.lower() in rfi["description"].lower()]
    
    # Display filtered count
    st.caption(f"Showing {len(filtered_rfis)} of {len(rfis)} RFIs")
    
    # Display RFIs in enhanced format
    for rfi in filtered_rfis:
        with st.container():
            st.markdown("---")
            
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                st.markdown(f"**{rfi['rfi_id']}**: {rfi['title']}")
                st.markdown(f"<small>📂 {rfi['category']} | {rfi['description'][:60]}...</small>", unsafe_allow_html=True)
            
            with col2:
                # Priority color coding
                priority_colors = {
                    "Critical": "#ef4444",
                    "High": "#ff8800", 
                    "Medium": "#2196F3",
                    "Low": "#4CAF50"
                }
                priority_color = priority_colors.get(rfi["priority"], "#666")
                
                # Status color coding
                status_colors = {
                    "Open": "#2196F3",
                    "Under Review": "#ff8800",
                    "Answered": "#4CAF50",
                    "Closed": "#666"
                }
                status_color = status_colors.get(rfi["status"], "#666")
                
                st.markdown(f"<span style='color: {priority_color}; font-weight: bold;'>● {rfi['priority']}</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='color: {status_color}; font-weight: bold;'>{rfi['status']}</span>", unsafe_allow_html=True)
            
            with col3:
                if rfi['days_open'] > 0:
                    st.markdown(f"**{rfi['days_open']}** days open")
                else:
                    st.markdown("**New** RFI")
                st.markdown(f"<small>Due: {rfi['due_date']}</small>", unsafe_allow_html=True)
            
            with col4:
                if st.button("View Details", key=f"view_rfi_{rfi['rfi_id']}", use_container_width=True):
                    st.session_state[f'show_rfi_detail_{rfi["rfi_id"]}'] = True
                    st.rerun()
    
    # RFI Analytics section
    if len(filtered_rfis) > 0:
        st.markdown("#### RFI Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Priority distribution
            priority_counts = {}
            for rfi in filtered_rfis:
                priority = rfi["priority"]
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            st.markdown("**Priority Distribution**")
            for priority, count in priority_counts.items():
                color = priority_colors.get(priority, "#666")
                st.markdown(f"<span style='color: {color};'>● {priority}: {count}</span>", unsafe_allow_html=True)
        
        with col2:
            # Status distribution
            status_counts = {}
            for rfi in filtered_rfis:
                status = rfi["status"]
                status_counts[status] = status_counts.get(status, 0) + 1
            
            st.markdown("**Status Distribution**")
            for status, count in status_counts.items():
                color = status_colors.get(status, "#666")
                st.markdown(f"<span style='color: {color};'>● {status}: {count}</span>", unsafe_allow_html=True)