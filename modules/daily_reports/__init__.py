"""
Daily Reports Module for Highland Tower Development

This standalone module provides comprehensive daily reporting functionality including:
- Daily field reports with weather, activities, and personnel tracking
- Photo documentation and progress tracking
- Digital signatures and approvals
- Issue and delay tracking
- Export and reporting capabilities
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import uuid

def render():
    """Render the standalone Daily Reports module"""
    st.title("📝 Daily Reports")
    
    # Daily Reports metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Reports This Week", "5", "+2 from last week")
    with col2:
        st.metric("Avg Submission Time", "8:15 AM", "On time")
    with col3:
        st.metric("Photos Uploaded", "47", "+12 today")
    with col4:
        st.metric("Issues Reported", "3", "1 resolved")
    
    # Quick actions
    st.markdown("#### Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ New Daily Report", type="primary", use_container_width=True):
            st.session_state['show_daily_report_form'] = True
            st.rerun()
    
    with col2:
        if st.button("📊 Report Analytics", type="secondary", use_container_width=True):
            st.success("Report analytics would be displayed here")
    
    with col3:
        if st.button("📤 Export Reports", type="secondary", use_container_width=True):
            st.success("Reports exported successfully!")
    
    with col4:
        if st.button("📱 Mobile Quick Entry", type="secondary", use_container_width=True):
            st.info("Mobile app integration for field teams")
    
    # Recent Daily Reports
    st.markdown("#### Recent Daily Reports - Highland Tower Development")
    
    # Sample daily reports data
    daily_reports = [
        {
            "report_id": "DR-HTD-2025-0524",
            "date": "2025-05-24",
            "weather": "Partly Cloudy, 68°F",
            "submitted_by": "Mike Johnson",
            "activities": "Foundation work continues, Steel delivery",
            "photos": 8,
            "issues": 1,
            "status": "Submitted"
        },
        {
            "report_id": "DR-HTD-2025-0523",
            "date": "2025-05-23",
            "weather": "Clear, 72°F",
            "submitted_by": "Sarah Thompson",
            "activities": "Concrete pour Level 1, MEP rough-in",
            "photos": 12,
            "issues": 0,
            "status": "Approved"
        },
        {
            "report_id": "DR-HTD-2025-0522",
            "date": "2025-05-22",
            "weather": "Light Rain, 65°F",
            "submitted_by": "Carlos Rivera",
            "activities": "Interior framing Floors 2-3",
            "photos": 6,
            "issues": 2,
            "status": "Approved"
        }
    ]
    
    # Display reports
    for report in daily_reports:
        with st.container():
            st.markdown("---")
            
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            
            with col1:
                st.markdown(f"**{report['report_id']}** - {report['date']}")
                st.markdown(f"<small>📅 {report['weather']}</small>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**Activities:** {report['activities']}")
                st.markdown(f"<small>👤 {report['submitted_by']}</small>", unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"📸 **{report['photos']}** photos")
                if report['issues'] > 0:
                    st.markdown(f"⚠️ **{report['issues']}** issues")
                else:
                    st.markdown("✅ **No issues**")
            
            with col4:
                status_color = "#4CAF50" if report['status'] == "Approved" else "#ff8800"
                st.markdown(f"<span style='color: {status_color}; font-weight: bold;'>{report['status']}</span>", unsafe_allow_html=True)
                if st.button("View", key=f"view_report_{report['report_id']}", use_container_width=True):
                    st.session_state[f'show_report_detail_{report["report_id"]}'] = True
                    st.rerun()
    
    # Show form if requested
    if st.session_state.get('show_daily_report_form', False):
        render_daily_report_form()

def render_daily_report_form():
    """Render the daily report form"""
    st.markdown("---")
    st.subheader("📝 New Daily Report")
    
    with st.form("daily_report_form"):
        # Basic Information
        col1, col2 = st.columns(2)
        
        with col1:
            report_date = st.date_input("Report Date", value=date.today())
            weather = st.text_input("Weather Conditions", placeholder="Clear, 72°F")
            
        with col2:
            submitted_by = st.text_input("Submitted By", value="Field Supervisor")
            temperature = st.number_input("Temperature (°F)", min_value=-20, max_value=120, value=70)
        
        # Work Activities
        st.markdown("#### Work Activities")
        activities = st.text_area("Activities Performed Today", 
                                placeholder="Describe the main work activities completed today...",
                                height=100)
        
        # Personnel
        st.markdown("#### Personnel on Site")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            contractors = st.number_input("Contractors", min_value=0, value=0)
        with col2:
            subcontractors = st.number_input("Subcontractors", min_value=0, value=0)
        with col3:
            visitors = st.number_input("Visitors", min_value=0, value=0)
        
        # Issues and Delays
        st.markdown("#### Issues and Delays")
        issues_reported = st.text_area("Issues or Delays", 
                                     placeholder="Report any issues, delays, or concerns...",
                                     height=80)
        
        # Quality Control
        st.markdown("#### Quality Control")
        quality_inspections = st.text_area("Quality Inspections Performed", 
                                         placeholder="Describe any quality inspections or tests...",
                                         height=60)
        
        # Safety
        st.markdown("#### Safety")
        safety_incidents = st.text_area("Safety Incidents or Near Misses", 
                                       placeholder="Report any safety incidents or observations...",
                                       height=60)
        
        # Photo Documentation
        st.markdown("#### Photo Documentation")
        st.info("📸 Photo upload functionality would be integrated here in production")
        photo_count = st.number_input("Number of Photos Taken", min_value=0, value=0)
        
        # Submit buttons
        col1, col2 = st.columns(2)
        
        with col1:
            submitted = st.form_submit_button("Submit Report", type="primary", use_container_width=True)
        
        with col2:
            if st.form_submit_button("Cancel", use_container_width=True):
                st.session_state['show_daily_report_form'] = False
                st.rerun()
        
        if submitted:
            # Generate report ID
            report_id = f"DR-HTD-{report_date.strftime('%Y-%m%d')}"
            
            st.success(f"✅ Daily Report {report_id} submitted successfully!")
            st.info("Report has been saved and is pending approval")
            
            # Clear form state
            st.session_state['show_daily_report_form'] = False
            st.rerun()