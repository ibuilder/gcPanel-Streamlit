"""
Dashboard module for the gcPanel Construction Management Dashboard.

This module provides the dashboard view with construction project metrics,
activity feeds, and key performance indicators.
"""

import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import random

def render_dashboard():
    """Render the main dashboard with project overview and metrics."""
    st.header("Dashboard")
    
    # Project stats
    st.subheader("Project Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="dashboard-card">'
                   '<div class="counter-value">12</div>'
                   '<div class="counter-label">Active Projects</div>'
                   '</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="dashboard-card">'
                   '<div class="counter-value">36</div>'
                   '<div class="counter-label">Open RFIs</div>'
                   '</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="dashboard-card">'
                   '<div class="counter-value">28</div>'
                   '<div class="counter-label">Pending Submittals</div>'
                   '</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="dashboard-card">'
                   '<div class="counter-value">8</div>'
                   '<div class="counter-label">Overdue Tasks</div>'
                   '</div>', unsafe_allow_html=True)
    
    # Recent activity feed
    st.subheader("Recent Activity")
    
    # Placeholder for recent activity feed
    activities = [
        {"type": "RFI", "project": "Highland Tower", "description": "RFI #123 was answered", "time": "2 hours ago"},
        {"type": "Submittal", "project": "City Center", "description": "Submittal #45 was approved", "time": "Yesterday"},
        {"type": "Project", "project": "Riverside Apartments", "description": "New milestone added", "time": "2 days ago"},
        {"type": "Task", "project": "Highland Tower", "description": "Task assigned to John Smith", "time": "3 days ago"}
    ]
    
    # Use a nicer display for activities
    for activity in activities:
        col1, col2 = st.columns([1, 4])
        with col1:
            if activity["type"] == "RFI":
                icon = "📝"
            elif activity["type"] == "Submittal":
                icon = "📋"
            elif activity["type"] == "Project":
                icon = "🏢"
            else:
                icon = "✅"
            st.markdown(f"<div style='font-size:24px; text-align:center;'>{icon}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 10px;'>
                <div><strong>{activity['description']}</strong> on {activity['project']}</div>
                <div style='color: #666; font-size: 0.9em;'>{activity['time']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Add Project Status chart
    st.subheader("Project Status")
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Project Status Chart data
        chart_data = pd.DataFrame({
            'Status': ['On Track', 'At Risk', 'Behind Schedule', 'Completed'],
            'Count': [7, 3, 2, 5]
        })
        
        # Custom colors for the chart
        colors = ['#1e3a8a', '#3b82f6', '#ef4444', '#10b981']
        
        # Display the chart
        st.bar_chart(chart_data.set_index('Status'), color='#1e3a8a')
    
    with col2:
        # Budget Utilization Chart data
        budget_data = pd.DataFrame({
            'Category': ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'Other'],
            'Percentage': [35, 25, 15, 20, 5]
        })
        
        # Display the chart
        st.bar_chart(budget_data.set_index('Category'), color='#1e3a8a')
    
    # Add Project Timeline
    st.subheader("Project Timeline")
    
    projects = [
        {"name": "Highland Tower", "start": "2025-01-15", "end": "2025-12-30", "progress": 35},
        {"name": "City Center", "start": "2024-11-01", "end": "2025-09-15", "progress": 65},
        {"name": "Riverside Apartments", "start": "2025-03-10", "end": "2026-02-28", "progress": 15},
        {"name": "Metro Office Complex", "start": "2025-02-01", "end": "2025-08-15", "progress": 45}
    ]
    
    for project in projects:
        st.markdown(f"""
        <div style='margin-bottom: 15px;'>
            <div style='display: flex; justify-content: space-between;'>
                <div><strong>{project['name']}</strong></div>
                <div>{project['progress']}% complete</div>
            </div>
            <div style='height: 12px; background-color: #e5e7eb; border-radius: 6px; margin-top: 8px;'>
                <div style='height: 12px; width: {project['progress']}%; background-color: #1e3a8a; border-radius: 6px;'></div>
            </div>
            <div style='display: flex; justify-content: space-between; font-size: 0.8em; color: #666; margin-top: 4px;'>
                <div>Start: {project['start']}</div>
                <div>End: {project['end']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)