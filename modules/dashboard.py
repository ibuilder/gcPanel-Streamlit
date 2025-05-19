"""
Dashboard module for the gcPanel Construction Management Dashboard.

This module provides the dashboard view with construction project metrics,
activity feeds, and key performance indicators.
Includes mobile optimization and intelligent alerts for a responsive user experience.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Import mobile optimizations
from utils.mobile.responsive_layout import add_mobile_styles
from utils.mobile.pwa_support import setup_pwa

# Import AI features
from utils.ai.smart_suggestions import IntelligentAlerts

def render_dashboard():
    """Render the main dashboard with project overview and metrics."""
    
    # Apply mobile optimizations and PWA support
    add_mobile_styles()
    setup_pwa()
    
    # Page title
    st.header("Dashboard")
    
    # Initialize intelligent alerts system
    alerts = IntelligentAlerts()
    
    # Display intelligent alerts at the top of the dashboard
    with st.expander("Intelligent Alerts", expanded=True):
        # Get high priority alerts
        high_priority_alerts = alerts.get_alerts_by_priority("high_priority")
        
        if high_priority_alerts:
            st.warning(f"**{len(high_priority_alerts)} High Priority Alerts Require Attention**")
            
            for alert in high_priority_alerts:
                st.markdown(f"""
                <div style="background-color: #f8d7da; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <div style="font-weight: bold; margin-bottom: 5px;">{alert['title']}</div>
                    <div style="margin-bottom: 10px;">{alert['description']}</div>
                    <div style="font-size: 0.9em; margin-bottom: 5px;"><b>Recommendation:</b> {alert['recommendation']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No high priority alerts at this time.")
    
    # Check if we have a selected project
    project_name = st.session_state.get('current_project', 'Highland Tower Development')
    
    # Project metrics summary
    st.subheader(f"{project_name} Overview")
    
    # Create a row of metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 14px; color: #6c757d; margin-bottom: 8px;">Project Completion</div>
            <div style="font-size: 24px; font-weight: 600; color: #3e79f7; margin-bottom: 5px;">42%</div>
            <div style="font-size: 12px; color: #38d39f;">+2.5% from last week</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 14px; color: #6c757d; margin-bottom: 8px;">Budget Variance</div>
            <div style="font-size: 24px; font-weight: 600; color: #38d39f; margin-bottom: 5px;">+$42K</div>
            <div style="font-size: 12px; color: #38d39f;">Under budget by 1.8%</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 14px; color: #6c757d; margin-bottom: 8px;">Schedule Variance</div>
            <div style="font-size: 24px; font-weight: 600; color: #ff5b5b; margin-bottom: 5px;">-3 days</div>
            <div style="font-size: 12px; color: #ff5b5b;">Critical path delay</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 14px; color: #6c757d; margin-bottom: 8px;">Outstanding RFIs</div>
            <div style="font-size: 24px; font-weight: 600; color: #f9c851; margin-bottom: 5px;">12</div>
            <div style="font-size: 12px; color: #f9c851;">4 require urgent attention</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create two columns for the next row of charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Budget Progress")
        
        # Budget data
        budget_data = pd.DataFrame({
            'Category': ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'Overhead'],
            'Budgeted': [2500000, 1800000, 750000, 1200000, 550000],
            'Actual': [1200000, 850000, 280000, 480000, 240000]
        })
        
        # Calculate percentages for better visualization
        budget_data['Percentage'] = (budget_data['Actual'] / budget_data['Budgeted'] * 100).round(1)
        
        # Create a more visual representation with progress bars
        for i, row in budget_data.iterrows():
            st.markdown(f"**{row['Category']}**")
            
            # Calculate percentage to show
            percent = row['Percentage']
            
            # Determine color based on variance (over/under budget)
            if percent > 100:
                bar_color = "#ff5b5b"  # Red for over budget
                status_text = f"<span style='color: #ff5b5b;'>Over budget by {percent - 100:.1f}%</span>"
            elif percent > 90:
                bar_color = "#f9c851"  # Yellow for close to budget
                status_text = f"<span style='color: #f9c851;'>{percent:.1f}% of budget</span>"
            else:
                bar_color = "#38d39f"  # Green for under budget
                status_text = f"<span style='color: #38d39f;'>{percent:.1f}% of budget</span>"
            
            # Create the progress bar
            st.progress(min(percent / 100, 1.0))
            
            # Show budget details
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.markdown(f"Actual: ${row['Actual']:,.0f}")
            with col2:
                st.markdown(f"Budget: ${row['Budgeted']:,.0f}")
            with col3:
                st.markdown(status_text, unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Schedule Progress")
        
        # Generate milestone data
        milestones = [
            {"name": "Design Development", "planned": "2025-01-15", "actual": "2025-01-20", "status": "Completed"},
            {"name": "Permits & Approvals", "planned": "2025-02-28", "actual": "2025-03-10", "status": "Completed"},
            {"name": "Site Preparation", "planned": "2025-03-15", "actual": "2025-03-15", "status": "Completed"},
            {"name": "Foundation", "planned": "2025-04-15", "actual": "2025-04-20", "status": "Completed"},
            {"name": "Structural Steel", "planned": "2025-05-30", "actual": None, "status": "In Progress"},
            {"name": "Building Envelope", "planned": "2025-07-15", "actual": None, "status": "Not Started"},
            {"name": "MEP Rough-ins", "planned": "2025-08-30", "actual": None, "status": "Not Started"},
            {"name": "Interior Finishes", "planned": "2025-10-15", "actual": None, "status": "Not Started"},
            {"name": "Commissioning", "planned": "2025-11-15", "actual": None, "status": "Not Started"},
            {"name": "Substantial Completion", "planned": "2025-12-01", "actual": None, "status": "Not Started"}
        ]
        
        # Convert to DataFrame
        milestones_df = pd.DataFrame(milestones)
        
        # Create interactive schedule chart
        for i, milestone in enumerate(milestones):
            # Status indicator
            if milestone["status"] == "Completed":
                status_color = "#38d39f"  # Green
                status_icon = "✓"
            elif milestone["status"] == "In Progress":
                status_color = "#3e79f7"  # Blue
                status_icon = "→"
            else:
                status_color = "#6c757d"  # Gray
                status_icon = "○"
            
            # Calculate days variance if completed
            if milestone["actual"]:
                planned_date = datetime.strptime(milestone["planned"], "%Y-%m-%d")
                actual_date = datetime.strptime(milestone["actual"], "%Y-%m-%d")
                variance_days = (actual_date - planned_date).days
                
                if variance_days > 0:
                    variance_text = f"<span style='color: #ff5b5b;'>+{variance_days} days late</span>"
                elif variance_days < 0:
                    variance_text = f"<span style='color: #38d39f;'>{abs(variance_days)} days early</span>"
                else:
                    variance_text = "<span style='color: #6c757d;'>On schedule</span>"
            else:
                variance_text = ""
            
            # Create milestone row with status indication
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="width: 24px; height: 24px; border-radius: 50%; background-color: {status_color}; 
                            color: white; display: flex; align-items: center; justify-content: center; 
                            margin-right: 10px;">{status_icon}</div>
                <div style="flex-grow: 1;">
                    <div style="font-weight: 500;">{milestone['name']}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 12px;">
                        <span>Plan: {milestone['planned']}</span>
                        <span>Actual: {milestone['actual'] if milestone['actual'] else '-'}</span>
                        <span>{variance_text}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Activity Feed and Notifications
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader("Recent Activity")
    
    # Sample activity data
    activities = [
        {"type": "RFI", "project": project_name, "description": "RFI #123 (Floor drainage details) was answered by John Smith", "time": "2 hours ago", "icon": "help_outline", "color": "#3e79f7"},
        {"type": "Submittal", "project": project_name, "description": "Submittal #45 (Glazing samples) was approved with comments", "time": "Yesterday", "icon": "description", "color": "#38d39f"},
        {"type": "Issue", "project": project_name, "description": "Issue #18 (MEP coordination in east wing) was created by Mary Johnson", "time": "Yesterday", "icon": "warning", "color": "#ff5b5b"},
        {"type": "Meeting", "project": project_name, "description": "Weekly coordination meeting minutes uploaded", "time": "2 days ago", "icon": "groups", "color": "#6c757d"},
        {"type": "Change Order", "project": project_name, "description": "Change Order #7 (Add roof garden) was submitted for approval", "time": "3 days ago", "icon": "sync_alt", "color": "#f9c851"}
    ]
    
    # Display activities with better styling
    for activity in activities:
        col1, col2 = st.columns([1, 15])
        
        with col1:
            st.markdown(f"""
            <div style="width: 36px; height: 36px; border-radius: 18px; background-color: {activity['color']}20; 
                        display: flex; align-items: center; justify-content: center; margin-top: 5px;">
                <span class="material-icons" style="color: {activity['color']};">{activity['icon']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 10px;">
                <div style="font-weight: 500;">{activity['description']}</div>
                <div style="color: #6c757d; font-size: 12px;">{activity['time']}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Weather and Site Conditions (for construction projects)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Weather Forecast")
        
        # Sample weather data
        weather_days = ["Today", "Tomorrow", "Wednesday", "Thursday", "Friday"]
        weather_conditions = ["Sunny", "Partly Cloudy", "Sunny", "Rainy", "Thunderstorm"]
        weather_temps = ["72°F", "75°F", "78°F", "68°F", "65°F"]
        weather_icons = ["wb_sunny", "cloud", "wb_sunny", "rainy", "thunderstorm"]
        weather_colors = ["#f9c851", "#6c757d", "#f9c851", "#3e79f7", "#ff5b5b"]
        
        # Display weather forecast
        for i in range(len(weather_days)):
            col_day, col_icon, col_temp = st.columns([2, 1, 1])
            with col_day:
                st.markdown(f"""
                <div>
                    <div style="font-weight: 500;">{weather_days[i]}</div>
                    <div style="font-size: 12px; color: #6c757d;">{weather_conditions[i]}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_icon:
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: center; height: 100%;">
                    <span class="material-icons" style="color: {weather_colors[i]}; font-size: 24px;">{weather_icons[i]}</span>
                </div>
                """, unsafe_allow_html=True)
            with col_temp:
                st.markdown(f"""
                <div style="text-align: right; font-weight: 500;">{weather_temps[i]}</div>
                """, unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Key Dates")
        
        # Sample key dates
        key_dates = [
            {"event": "Structural Steel Delivery", "date": "May 25, 2025", "days_away": 8, "type": "delivery"},
            {"event": "MEP Coordination Meeting", "date": "May 20, 2025", "days_away": 3, "type": "meeting"},
            {"event": "City Inspection", "date": "May 30, 2025", "days_away": 13, "type": "inspection"},
            {"event": "Owner Walkthrough", "date": "June 5, 2025", "days_away": 19, "type": "milestone"},
            {"event": "Elevator Installation Begins", "date": "June 10, 2025", "days_away": 24, "type": "construction"}
        ]
        
        # Display key dates
        for date_item in key_dates:
            # Icons for different event types
            icon_map = {
                "delivery": "local_shipping",
                "meeting": "groups",
                "inspection": "search",
                "milestone": "flag",
                "construction": "construction"
            }
            
            # Color code based on days away
            if date_item["days_away"] <= 7:
                color = "#ff5b5b"  # Red for urgent
            elif date_item["days_away"] <= 14:
                color = "#f9c851"  # Yellow for upcoming
            else:
                color = "#6c757d"  # Gray for further away
            
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="width: 32px; height: 32px; border-radius: 16px; background-color: {color}20; 
                            display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                    <span class="material-icons" style="color: {color}; font-size: 18px;">{icon_map[date_item['type']]}</span>
                </div>
                <div style="flex-grow: 1;">
                    <div style="font-weight: 500;">{date_item['event']}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 12px;">
                        <span>{date_item['date']}</span>
                        <span>{date_item['days_away']} days away</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)