"""
Analytics Module for gcPanel

This module provides comprehensive analytics and reporting functionality for the construction management dashboard.
It includes submodules for different types of analysis and reporting.
"""

import streamlit as st
from modules.analytics.analysis import render as render_analysis

def render_analytics_dashboard():
    """Render the analytics dashboard overview."""
    st.subheader("Analytics Dashboard")
    
    # Create container with white background
    st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
    
    # Key Performance Indicators
    st.markdown("### Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Schedule",
            "On Track",
            "+2 days",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "Budget",
            "$45.5M",
            "-3.2%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Safety",
            "2 Incidents",
            "-1",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            "Quality",
            "87%",
            "+2%",
            delta_color="normal"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Recent Reports
    st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
    
    st.markdown("### Recent Reports")
    
    recent_reports = [
        {
            "title": "Monthly Progress Report - April 2025",
            "date": "May 5, 2025",
            "type": "Progress",
            "status": "Approved"
        },
        {
            "title": "Financial Forecast Q2 2025",
            "date": "May 2, 2025",
            "type": "Financial",
            "status": "Draft"
        },
        {
            "title": "Safety Performance Review",
            "date": "April 30, 2025",
            "type": "Safety",
            "status": "Approved"
        },
        {
            "title": "Quality Assurance Audit",
            "date": "April 28, 2025",
            "type": "Quality",
            "status": "Under Review"
        }
    ]
    
    for report in recent_reports:
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
        
        with col1:
            st.markdown(f"**{report['title']}**")
        
        with col2:
            st.markdown(f"{report['date']}")
        
        with col3:
            st.markdown(f"{report['type']}")
        
        with col4:
            status_color = {
                "Approved": "green",
                "Draft": "blue",
                "Under Review": "orange"
            }.get(report['status'], "gray")
            
            st.markdown(f"<span style='color: {status_color};'>{report['status']}</span>", unsafe_allow_html=True)
        
        with col5:
            st.button("View", key=f"view_report_{report['title']}")
        
        st.markdown("---")
    
    # Create a new report button
    if st.button("+ Create New Report", type="primary"):
        st.session_state.create_new_report = True
    
    if st.session_state.get("create_new_report", False):
        with st.form("new_report_form"):
            st.subheader("Create New Report")
            
            report_title = st.text_input("Report Title")
            report_type = st.selectbox("Report Type", ["Progress", "Financial", "Safety", "Quality", "Custom"])
            
            col1, col2 = st.columns(2)
            with col1:
                report_date = st.date_input("Report Date")
            with col2:
                report_period = st.selectbox("Reporting Period", ["Weekly", "Monthly", "Quarterly", "Annual", "Custom"])
            
            report_description = st.text_area("Description")
            
            col1, col2 = st.columns(2)
            with col1:
                submit_button = st.form_submit_button("Create Report")
            with col2:
                cancel_button = st.form_submit_button("Cancel")
            
            if submit_button and report_title:
                st.success(f"Report '{report_title}' created successfully")
                st.session_state.create_new_report = False
                st.rerun()
            
            if cancel_button:
                st.session_state.create_new_report = False
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def render():
    """Render the Analytics module."""
    st.title("Analytics & Reporting")
    
    # Create tabs for different analytics views
    tab1, tab2 = st.tabs(["Dashboard", "Analysis"])
    
    with tab1:
        render_analytics_dashboard()
    
    with tab2:
        render_analysis()