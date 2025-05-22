"""
Pre-Construction Module for gcPanel Construction Management Dashboard

This module provides comprehensive pre-construction planning capabilities including:
- Site Analysis
- Design Development
- Estimating
- Value Engineering
- Preconstruction Scheduling
- Constructability Review
- Bid Management
- Procurement Planning
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import json

# Import sub-modules
from modules.preconstruction.site_analysis import render_site_analysis
from modules.preconstruction.estimating import render_estimating
from modules.preconstruction.value_engineering import render_value_engineering
from modules.preconstruction.constructability import render_constructability
from modules.preconstruction.bid_management import render_bid_management
from modules.preconstruction.procurement import render_procurement

def render():
    """Render the Pre-Construction module"""
    st.title("Pre-Construction")
    
    # Sub-module navigation tabs
    tab_names = [
        "Dashboard", 
        "Site Analysis", 
        "Estimating", 
        "Value Engineering", 
        "Constructability", 
        "Bid Management", 
        "Procurement"
    ]
    
    tabs = st.tabs(tab_names)
    
    # Pre-Construction Dashboard
    with tabs[0]:
        render_dashboard()
    
    # Site Analysis
    with tabs[1]:
        render_site_analysis()
    
    # Estimating
    with tabs[2]:
        render_estimating()
    
    # Value Engineering
    with tabs[3]:
        render_value_engineering()
    
    # Constructability
    with tabs[4]:
        render_constructability()
    
    # Bid Management
    with tabs[5]:
        render_bid_management()
    
    # Procurement
    with tabs[6]:
        render_procurement()

def render_dashboard():
    """Render the Pre-Construction Dashboard"""
    st.header("Pre-Construction Dashboard")
    
    # Create layout columns
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        render_progress_chart()
    
    # Right side columns
    with col2:
        render_metrics()
    
    with col3:
        render_upcoming_tasks()
    
    # Bottom row
    st.subheader("Recent Activity")
    render_activity_feed()

def render_progress_chart():
    """Render the progress chart for preconstruction phases"""
    st.subheader("Pre-Construction Progress")
    
    # Define preconstruction phases and their progress
    phases = {
        "Site Analysis": 100,
        "Design Review": 85,
        "Estimating": 70,
        "Value Engineering": 50,
        "Constructability Review": 30,
        "Bid Management": 20,
        "Procurement Planning": 10
    }
    
    # Create a DataFrame for visualization
    df = pd.DataFrame({
        "Phase": list(phases.keys()),
        "Progress": list(phases.values())
    })
    
    # Plot the horizontal bar chart
    st.bar_chart(df.set_index("Phase"))
    
    # Overall project pre-construction completion
    overall = sum(phases.values()) / len(phases)
    st.progress(overall / 100)
    st.write(f"Overall Pre-Construction Progress: {overall:.1f}%")

def render_metrics():
    """Render key metrics for the pre-construction phase"""
    st.subheader("Key Metrics")
    
    metrics = [
        {"label": "Budget", "value": "$45.5M", "delta": "-2.3%"},
        {"label": "Estimated Duration", "value": "24 months", "delta": "0"},
        {"label": "Trade Packages", "value": "28", "delta": "+3"},
        {"label": "RFIs Issued", "value": "47", "delta": "+5"}
    ]
    
    for metric in metrics:
        st.metric(
            label=metric["label"],
            value=metric["value"],
            delta=metric["delta"]
        )

def render_upcoming_tasks():
    """Render upcoming tasks for the pre-construction phase"""
    st.subheader("Upcoming Tasks")
    
    tasks = [
        {"task": "Finalize Site Logistics Plan", "due": "May 25, 2025", "assigned": "John D."},
        {"task": "Complete 90% Estimate", "due": "May 28, 2025", "assigned": "Sarah T."},
        {"task": "MEP Coordination Meeting", "due": "May 30, 2025", "assigned": "Team"},
        {"task": "Issue Bid Package #3", "due": "Jun 2, 2025", "assigned": "Michael P."}
    ]
    
    for task in tasks:
        st.markdown(
            f"""
            <div style="padding: 10px; border-left: 3px solid #4a90e2; margin-bottom: 8px; background-color: #f8f9fa;">
                <div style="font-weight: 500;">{task["task"]}</div>
                <div style="display: flex; justify-content: space-between; font-size: 12px; color: #6c757d;">
                    <span>Due: {task["due"]}</span>
                    <span>{task["assigned"]}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_activity_feed():
    """Render recent activity feed"""
    activities = [
        {"action": "Updated estimate for foundation package", "user": "Sarah T.", "time": "2 hours ago"},
        {"action": "Uploaded revised site survey", "user": "John D.", "time": "6 hours ago"},
        {"action": "Created bid package for MEP", "user": "Michael P.", "time": "Yesterday"},
        {"action": "Added value engineering proposal #12", "user": "Lisa K.", "time": "Yesterday"},
        {"action": "Completed constructability review for Phase 1", "user": "Robert M.", "time": "2 days ago"}
    ]
    
    for activity in activities:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                <div>{activity["action"]}</div>
                <div style="color: #6c757d; font-size: 13px;">
                    <span>{activity["user"]}</span> • <span>{activity["time"]}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )