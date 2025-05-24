"""
Meeting Management Module for Highland Tower Development

This module provides comprehensive meeting management functionality including:
- Meeting scheduling and coordination
- Agenda creation and management
- Meeting minutes and action items
- Stakeholder attendance tracking
- Professional meeting templates
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render():
    """Render the Meeting Management module"""
    st.title("🤝 Meeting Management")
    
    # Meeting Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Scheduled Meetings", "8", "+2 this week")
    with col2:
        st.metric("Completed Meetings", "24", "+3 completed")
    with col3:
        st.metric("Action Items", "15", "7 pending")
    with col4:
        st.metric("Attendance Rate", "94%", "+2% improvement")
    
    # Quick actions
    st.markdown("#### Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Schedule Meeting", type="primary", use_container_width=True, key="schedule_meeting_btn"):
            st.success("Meeting scheduling form would open here")
    
    with col2:
        if st.button("📝 Create Agenda", type="secondary", use_container_width=True, key="create_agenda_btn"):
            st.success("Agenda template created!")
    
    with col3:
        if st.button("📋 Meeting Minutes", type="secondary", use_container_width=True, key="meeting_minutes_btn"):
            st.info("Meeting minutes template available")
    
    with col4:
        if st.button("📊 Meeting Reports", type="secondary", use_container_width=True, key="meeting_reports_btn"):
            st.success("Meeting reports generated!")
    
    # Recent Meetings
    st.markdown("#### Recent Meetings - Highland Tower Development")
    
    meetings = [
        {
            "meeting_id": "MTG-HTD-001",
            "title": "Weekly Project Review",
            "date": "2025-05-24",
            "time": "9:00 AM",
            "type": "Project Review",
            "attendees": 8,
            "status": "Scheduled",
            "location": "Site Office"
        },
        {
            "meeting_id": "MTG-HTD-002",
            "title": "Safety Coordination Meeting",
            "date": "2025-05-23",
            "time": "2:00 PM",
            "type": "Safety",
            "attendees": 12,
            "status": "Completed",
            "location": "Conference Room A"
        },
        {
            "meeting_id": "MTG-HTD-003",
            "title": "Design Review - Mechanical Systems",
            "date": "2025-05-22",
            "time": "10:30 AM",
            "type": "Design Review",
            "attendees": 6,
            "status": "Completed",
            "location": "Virtual Meeting"
        }
    ]
    
    for meeting in meetings:
        with st.container():
            st.markdown("---")
            
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                st.markdown(f"**{meeting['meeting_id']}**: {meeting['title']}")
                st.markdown(f"<small>📅 {meeting['date']} at {meeting['time']}</small>", unsafe_allow_html=True)
            
            with col2:
                status_color = "#4CAF50" if meeting['status'] == "Completed" else "#2196F3"
                st.markdown(f"<span style='color: {status_color}; font-weight: bold;'>{meeting['status']}</span>", unsafe_allow_html=True)
                st.markdown(f"📍 {meeting['location']}")
            
            with col3:
                st.markdown(f"👥 **{meeting['attendees']}** attendees")
                st.markdown(f"<small>{meeting['type']}</small>", unsafe_allow_html=True)
            
            with col4:
                if st.button("View Details", key=f"view_meeting_{meeting['meeting_id']}", use_container_width=True):
                    st.success(f"Opening {meeting['meeting_id']} details...")
    
    # Meeting Templates
    st.markdown("#### Meeting Templates")
    
    templates = [
        "Weekly Project Review",
        "Safety Coordination Meeting", 
        "Design Review Meeting",
        "Owner Progress Meeting",
        "Subcontractor Coordination",
        "Quality Control Review"
    ]
    
    col1, col2, col3 = st.columns(3)
    for i, template in enumerate(templates):
        col = [col1, col2, col3][i % 3]
        with col:
            if st.button(f"📋 {template}", key=f"template_{i}", use_container_width=True):
                st.info(f"Using {template} template...")