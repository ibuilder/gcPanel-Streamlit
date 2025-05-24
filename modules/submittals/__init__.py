"""
Submittals Module for Highland Tower Development

This standalone module provides comprehensive submittal management functionality including:
- Submittal creation, tracking, and approval workflow
- Multi-revision management and version control
- Trade-specific submittal categories
- Review time tracking and analytics
- Digital approval processes
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

def render():
    """Render the standalone Submittals module"""
    st.title("📦 Submittal Management")
    
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
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ New Submittal", type="primary", use_container_width=True):
            st.session_state['show_submittal_form'] = True
            st.rerun()
    
    with col2:
        if st.button("📊 Submittal Analytics", type="secondary", use_container_width=True):
            st.session_state['show_submittal_analytics'] = True
            st.rerun()
    
    with col3:
        if st.button("📤 Export Submittals", type="secondary", use_container_width=True):
            st.success("Submittal data exported successfully!")
    
    with col4:
        if st.button("🔄 Refresh Data", type="secondary", use_container_width=True):
            st.success("Submittal data refreshed!")
    
    # Submittal List with filters
    st.markdown("#### Active Submittals - Highland Tower Development")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_filter = st.selectbox("Status", ["All", "Submitted", "Under Review", "Revise & Resubmit", "Approved", "Rejected"])
    with col2:
        type_filter = st.selectbox("Type", ["All", "Shop Drawings", "Product Data", "Samples", "Mix Designs", "Test Reports"])
    with col3:
        trade_filter = st.selectbox("Trade", ["All", "Structural Steel", "Concrete", "MEP", "Architectural", "Finishes"])
    with col4:
        search_term = st.text_input("Search Submittals", placeholder="Search by ID or title...")
    
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
        },
        {
            "submittal_id": "SUB-HTD-005",
            "title": "Elevator System Specifications",
            "type": "Product Data",
            "trade": "MEP",
            "status": "Under Review",
            "submitted_date": "2025-05-21",
            "due_date": "2025-05-28",
            "submitted_by": "Vertical Transportation Inc",
            "reviewer": "Jennifer Wilson",
            "days_in_review": 3,
            "revision": "Rev 0"
        }
    ]
    
    # Filter submittals based on selections
    filtered_submittals = submittals
    if status_filter != "All":
        filtered_submittals = [sub for sub in filtered_submittals if sub["status"] == status_filter]
    if type_filter != "All":
        filtered_submittals = [sub for sub in filtered_submittals if sub["type"] == type_filter]
    if trade_filter != "All":
        filtered_submittals = [sub for sub in filtered_submittals if sub["trade"] == trade_filter]
    if search_term:
        filtered_submittals = [sub for sub in filtered_submittals if 
                              search_term.lower() in sub["submittal_id"].lower() or 
                              search_term.lower() in sub["title"].lower()]
    
    # Display filtered count
    st.caption(f"Showing {len(filtered_submittals)} of {len(submittals)} submittals")
    
    # Display Submittals in enhanced format
    for submittal in filtered_submittals:
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
                if st.button("View Details", key=f"view_submittal_standalone_{submittal['submittal_id']}", use_container_width=True):
                    st.session_state[f'show_submittal_detail_{submittal["submittal_id"]}'] = True
                    st.rerun()
    
    # Submittal Analytics section
    if len(filtered_submittals) > 0:
        st.markdown("#### Submittal Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Status distribution
            status_counts = {}
            for submittal in filtered_submittals:
                status = submittal["status"]
                status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                fig_status = px.pie(
                    values=list(status_counts.values()),
                    names=list(status_counts.keys()),
                    title="Submittal Status Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_status.update_layout(height=300)
                st.plotly_chart(fig_status, use_container_width=True)
        
        with col2:
            # Trade distribution
            trade_counts = {}
            for submittal in filtered_submittals:
                trade = submittal["trade"]
                trade_counts[trade] = trade_counts.get(trade, 0) + 1
            
            if trade_counts:
                fig_trade = px.bar(
                    x=list(trade_counts.keys()),
                    y=list(trade_counts.values()),
                    title="Submittals by Trade",
                    labels={"x": "Trade", "y": "Count"},
                    color=list(trade_counts.keys()),
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_trade.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig_trade, use_container_width=True)