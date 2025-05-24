"""
RFI (Request for Information) Module for Highland Tower Development

This standalone module provides comprehensive RFI management functionality including:
- RFI creation, tracking, and management
- Status workflow management
- Priority and trade-based filtering
- Response time tracking
- Digital collaboration tools
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

def render():
    """Render the standalone RFI Management module"""
    st.title("❓ Request for Information (RFI) Management")
    
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
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ New RFI", type="primary", use_container_width=True, key="new_rfi_main"):
            st.session_state['show_rfi_form'] = True
            st.rerun()
    
    with col2:
        if st.button("📊 RFI Analytics", type="secondary", use_container_width=True, key="rfi_analytics_main"):
            st.session_state['show_rfi_analytics'] = True
            st.rerun()
    
    with col3:
        if st.button("📤 Export RFIs", type="secondary", use_container_width=True, key="export_rfi_main"):
            st.success("RFI data exported successfully!")
    
    with col4:
        if st.button("🔄 Refresh Data", type="secondary", use_container_width=True, key="refresh_rfi_main"):
            st.success("RFI data refreshed!")
    
    # RFI List with filters
    st.markdown("#### Active RFIs - Highland Tower Development")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_filter = st.selectbox("Status", ["All", "Open", "Pending Response", "Under Review", "Answered", "Closed"])
    with col2:
        priority_filter = st.selectbox("Priority", ["All", "Critical", "High", "Medium", "Low"])
    with col3:
        trade_filter = st.selectbox("Trade", ["All", "Structural", "Architectural", "MEP", "Civil", "Other"])
    with col4:
        search_term = st.text_input("Search RFIs", placeholder="Search by ID or subject...")
    
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
        },
        {
            "rfi_id": "RFI-HTD-005",
            "subject": "Fire Protection System Integration - Retail Spaces",
            "trade": "MEP",
            "status": "Open",
            "priority": "Medium",
            "submitted_date": "2025-05-24",
            "due_date": "2025-05-31",
            "submitted_by": "Fire Safety Inc",
            "assigned_to": "David Chen",
            "days_open": 0,
            "description": "Integration requirements for fire protection systems in retail spaces below Highland Tower."
        }
    ]
    
    # Filter RFIs based on selections
    filtered_rfis = rfis
    if status_filter != "All":
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["status"] == status_filter]
    if priority_filter != "All":
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["priority"] == priority_filter]
    if trade_filter != "All":
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["trade"] == trade_filter]
    if search_term:
        filtered_rfis = [rfi for rfi in filtered_rfis if 
                        search_term.lower() in rfi["rfi_id"].lower() or 
                        search_term.lower() in rfi["subject"].lower()]
    
    # Display filtered count
    st.caption(f"Showing {len(filtered_rfis)} of {len(rfis)} RFIs")
    
    # Display RFIs in enhanced format
    for rfi in filtered_rfis:
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
                if st.button("View Details", key=f"view_rfi_standalone_{rfi['rfi_id']}", use_container_width=True):
                    st.session_state[f'show_rfi_detail_{rfi["rfi_id"]}'] = True
                    st.rerun()
    
    # RFI Analytics section
    if len(filtered_rfis) > 0:
        st.markdown("#### RFI Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Status distribution
            status_counts = {}
            for rfi in filtered_rfis:
                status = rfi["status"]
                status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                fig_status = px.pie(
                    values=list(status_counts.values()),
                    names=list(status_counts.keys()),
                    title="RFI Status Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_status.update_layout(height=300)
                st.plotly_chart(fig_status, use_container_width=True)
        
        with col2:
            # Priority distribution
            priority_counts = {}
            for rfi in filtered_rfis:
                priority = rfi["priority"]
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            if priority_counts:
                fig_priority = px.bar(
                    x=list(priority_counts.keys()),
                    y=list(priority_counts.values()),
                    title="RFI Priority Distribution",
                    labels={"x": "Priority", "y": "Count"},
                    color=list(priority_counts.keys()),
                    color_discrete_map={
                        "Critical": "#ef4444",
                        "High": "#ff8800", 
                        "Medium": "#ffeb3b",
                        "Low": "#4CAF50"
                    }
                )
                fig_priority.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig_priority, use_container_width=True)