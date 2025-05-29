"""
Highland Tower Development - Mobile Companion (Fixed)
Clean, working mobile interface for field operations
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def render_mobile_companion():
    """Render clean mobile companion interface"""
    
    st.title("📱 Mobile Companion")
    st.markdown("**Field operations optimized for mobile devices**")
    
    # Quick Actions Section
    st.subheader("⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Quick Report", key="mobile_quick_report", use_container_width=True):
            st.success("✅ Quick report started - ready for field input")
            
        if st.button("📷 Photo Capture", key="mobile_photo", use_container_width=True):
            st.info("📸 Camera interface would open for progress documentation")
    
    with col2:
        if st.button("🦺 Safety Check", key="mobile_safety", use_container_width=True):
            st.warning("🦺 Safety inspection checklist opened")
            
        if st.button("📞 Contact Team", key="mobile_contact", use_container_width=True):
            st.info("📞 Team directory and communication tools")
    
    # Current Status Dashboard
    st.subheader("📊 Current Status")
    
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        st.metric("Active Workers", "89", "+3 today")
    with status_col2:
        st.metric("Weather", "72°F", "Clear skies")
    with status_col3:
        st.metric("Progress", "87%", "+2% this week")
    
    # Today's Schedule
    st.subheader("📅 Today's Schedule")
    
    schedule_data = [
        {"Time": "8:00 AM", "Activity": "Steel beam installation - Level 14", "Status": "In Progress"},
        {"Time": "10:30 AM", "Activity": "Concrete delivery coordination", "Status": "Scheduled"},
        {"Time": "2:00 PM", "Activity": "Safety inspection - MEP areas", "Status": "Pending"},
        {"Time": "4:00 PM", "Activity": "Daily report submission", "Status": "Upcoming"}
    ]
    
    for item in schedule_data:
        status_icon = "🟢" if item["Status"] == "In Progress" else "🔵" if item["Status"] == "Scheduled" else "🟡"
        st.markdown(f"**{item['Time']}** {status_icon} {item['Activity']}")
    
    # Quick Weather & Site Conditions
    st.subheader("🌤️ Site Conditions")
    
    weather_col1, weather_col2 = st.columns(2)
    
    with weather_col1:
        st.info("**Weather:** 72°F, Clear\n**Wind:** 5 mph NW\n**Visibility:** Excellent")
    
    with weather_col2:
        st.info("**Site Access:** Open\n**Crane Operations:** Active\n**Deliveries:** On Schedule")
    
    # Emergency Contacts
    with st.expander("🚨 Emergency Contacts"):
        emergency_contacts = [
            {"Role": "Site Supervisor", "Name": "Mike Rodriguez", "Phone": "(555) 123-4567"},
            {"Role": "Safety Manager", "Name": "Sarah Chen", "Phone": "(555) 234-5678"},
            {"Role": "Security", "Name": "Highland Security", "Phone": "(555) 345-6789"},
            {"Role": "Emergency Services", "Name": "911", "Phone": "911"}
        ]
        
        for contact in emergency_contacts:
            st.markdown(f"**{contact['Role']}:** {contact['Name']} - {contact['Phone']}")

if __name__ == "__main__":
    render_mobile_companion()