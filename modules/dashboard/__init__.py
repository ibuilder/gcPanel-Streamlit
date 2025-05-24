"""
Dashboard module for gcPanel Construction Management Dashboard.

This module renders the main dashboard with project overview, KPIs, and activity feed.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render_enhanced_project_status_section(current_project):
    """Render enhanced project status with real-time data integration"""
    st.markdown("### 🏗️ Enhanced Project Status")
    
    # Real-time project metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Overall Progress", "72%", "+3% this week", delta_color="normal")
    
    with col2:
        st.metric("Budget Status", "$32.8M", "-2.3% under budget", delta_color="inverse")
    
    with col3:
        st.metric("Schedule Status", "On Track", "+2 days ahead", delta_color="normal")
    
    with col4:
        st.metric("Quality Score", "94%", "+2% improvement", delta_color="normal")
    
    with col5:
        st.metric("Safety Score", "98%", "0 incidents this week", delta_color="normal")

def render_critical_path_alerts_section():
    """Render critical path alerts and schedule dependencies"""
    st.markdown("### ⚠️ Critical Path Alerts")
    
    alerts = [
        {
            "severity": "high",
            "task": "Foundation Inspection",
            "impact": "2-day delay risk",
            "action": "Schedule inspector for tomorrow",
            "responsible": "John Smith"
        },
        {
            "severity": "medium", 
            "task": "Steel Delivery",
            "impact": "Potential 1-week delay",
            "action": "Confirm delivery schedule",
            "responsible": "Sarah Johnson"
        }
    ]
    
    for alert in alerts:
        severity_color = "#ff4444" if alert["severity"] == "high" else "#ff8800"
        st.markdown(
            f"""
            <div style="border-left: 4px solid {severity_color}; padding: 12px; margin: 8px 0; background-color: #f8f9fa;">
                <strong>🚨 {alert["task"]}</strong><br>
                <span style="color: {severity_color};">Impact: {alert["impact"]}</span><br>
                Action: {alert["action"]} (Assigned: {alert["responsible"]})
            </div>
            """,
            unsafe_allow_html=True
        )

def render_weather_impact_section():
    """Render weather conditions affecting construction"""
    st.markdown("### 🌤️ Weather Impact Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Current Conditions**")
        st.markdown("🌤️ Partly Cloudy")
        st.markdown("🌡️ 72°F")
        st.markdown("💨 Wind: 8 mph")
        st.markdown("💧 Humidity: 45%")
    
    with col2:
        st.markdown("**Today's Impact**")
        st.markdown("✅ Concrete work: Favorable")
        st.markdown("✅ Exterior work: Good conditions")
        st.markdown("⚠️ High work: Monitor wind")
        st.markdown("✅ Material delivery: Clear")
    
    with col3:
        st.markdown("**3-Day Forecast**")
        st.markdown("🌤️ Tomorrow: Partly cloudy, 75°F")
        st.markdown("☀️ Friday: Sunny, 78°F")
        st.markdown("🌧️ Saturday: Rain expected")

def render_customizable_widgets_section():
    """Render customizable dashboard widgets"""
    st.markdown("### 🎛️ Customizable Widgets")
    
    # Widget customization options
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("**Widget Options**")
        widget_options = st.multiselect(
            "Select widgets to display:",
            ["Project Timeline", "Budget Trend", "Team Activity", "Recent Photos", "Equipment Status"],
            default=["Project Timeline", "Budget Trend", "Team Activity"]
        )
    
    with col2:
        # Render selected widgets
        if "Project Timeline" in widget_options:
            st.markdown("**📅 Project Timeline**")
            timeline_data = pd.DataFrame({
                'Phase': ['Foundation', 'Structure', 'Envelope', 'MEP', 'Finishes'],
                'Progress': [100, 85, 60, 30, 10]
            })
            st.bar_chart(timeline_data.set_index('Phase'))
        
        if "Budget Trend" in widget_options:
            st.markdown("**💰 Budget Trend**")
            budget_data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                'Planned': [2000000, 4500000, 7200000, 10800000, 15200000],
                'Actual': [1950000, 4350000, 7050000, 10500000, 14800000]
            })
            st.line_chart(budget_data.set_index('Month'))
        
        if "Team Activity" in widget_options:
            st.markdown("**👥 Team Activity**")
            st.markdown("- 🟢 12 team members active")
            st.markdown("- 📋 8 tasks completed today")
            st.markdown("- 💬 15 new messages")
            st.markdown("- 📊 3 reports submitted")

def render_dashboard():
    """Render the clean Highland Tower Development dashboard."""
    
    # Apply zero spacing CSS for dashboard
    st.markdown("""
    <style>
    /* Bring dashboard content to top with zero spacing */
    .main .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Remove spacing between elements */
    .element-container {
        margin-bottom: 0.5rem !important;
    }
    
    h1, h2, h3 {
        margin-top: 0 !important;
        margin-bottom: 0.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🏗️ Highland Tower Development Dashboard")
    
    # Current project info
    current_project = st.session_state.get("current_project", "Highland Tower Development")
    
    # Clean project metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Progress", "68%", "+3% this week")
    with col2:
        st.metric("Budget Status", "$30.2M", "-$1.3M under budget")
    with col3:
        st.metric("Schedule", "On Track", "2 days ahead")
    with col4:
        st.metric("Safety Score", "98%", "+2% this month")
    

    
    # Project Header Card
    st.markdown(
        f"""
        <div class="dashboard-card" style="padding: 1.5rem; margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="margin-bottom: 0.3rem; font-size: 1.5rem;">{current_project}</h2>
                    <div style="color: #6c757d; font-size: 0.9rem;">
                        <span style="margin-right: 1rem;">
                            <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.2rem;">
                                calendar_today
                            </span>
                            Start: Jan 15, 2025
                        </span>
                        <span style="margin-right: 1rem;">
                            <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.2rem;">
                                event
                            </span>
                            End: Dec 20, 2025
                        </span>
                        <span>
                            <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.2rem;">
                                person
                            </span>
                            PM: John Smith
                        </span>
                    </div>
                </div>
                <div>
                    <span class="status-pill status-active">Active</span>
                </div>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="counter-value">72%</div>
                <div class="counter-label">Overall Progress</div>
                <div style="width: 100%; background-color: #eee; height: 4px; margin-top: 0.7rem; border-radius: 2px;">
                    <div style="width: 72%; background-color: #3e79f7; height: 4px; border-radius: 2px;"></div>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="counter-value">45</div>
                <div class="counter-label">Open RFIs</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="counter-value">28</div>
                <div class="counter-label">Pending Submittals</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="counter-value">8</div>
                <div class="counter-label">Overdue Tasks</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Two column layout for charts and activity
    col_charts, col_activity = st.columns([2, 1])
    
    with col_charts:
        st.subheader("Project Performance")
        
        # Create tabs for different charts
        tab1, tab2, tab3 = st.tabs(["Schedule", "Budget", "Quality"])
        
        with tab1:
            # Schedule chart - improved with Plotly
            schedule_data = {
                'Task': ['Foundation', 'Structure', 'Envelope', 'MEP', 'Finishes', 'Commissioning'],
                'Planned': [100, 80, 60, 40, 20, 5],
                'Actual': [100, 85, 55, 30, 10, 0]
            }
            
            df_schedule = pd.DataFrame(schedule_data)
            
            # Using Plotly for better visualization and no warnings
            fig = px.bar(
                df_schedule, 
                x='Task', 
                y=['Planned', 'Actual'],
                title='Schedule Progress by Task',
                barmode='group',
                labels={'value': 'Completion (%)', 'variable': 'Type'},
                color_discrete_map={'Planned': '#3367D6', 'Actual': '#28a745'}
            )
            
            # Improve layout and styling
            fig.update_layout(
                height=300,
                margin=dict(l=10, r=10, t=40, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis=dict(ticksuffix="%")
            )
            
            # Use Streamlit container for clean display
            with st.container():
                st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            # Budget chart - improved with Plotly
            budget_data = {
                'Category': ['Labor', 'Materials', 'Equipment', 'Subcontracts', 'General Conditions'],
                'Budget': [2500000, 3200000, 1200000, 4500000, 800000],
                'Actual': [2300000, 3000000, 1150000, 4200000, 750000]
            }
            
            df_budget = pd.DataFrame(budget_data)
            
            # Using Plotly for better visualization
            fig = px.bar(
                df_budget, 
                x='Category', 
                y=['Budget', 'Actual'],
                title='Budget vs. Actual by Category',
                barmode='group',
                labels={'value': 'Amount ($)', 'variable': 'Type'},
                color_discrete_map={'Budget': '#3367D6', 'Actual': '#28a745'}
            )
            
            # Format the Y-axis to show currency
            fig.update_layout(
                height=300,
                margin=dict(l=10, r=10, t=40, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis=dict(tickprefix="$", tickformat=",.0f")
            )
            
            # Use Streamlit container for clean display
            with st.container():
                st.plotly_chart(fig, use_container_width=True)
            
        with tab3:
            # Quality chart - improved version using Plotly for better rendering
            quality_data = {
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                'NCRs': [12, 8, 10, 7, 3],
                'Inspections': [45, 50, 48, 52, 55]
            }
            
            df_quality = pd.DataFrame(quality_data)
            
            # Using Plotly Express for better control and no warnings
            fig = px.line(
                df_quality, 
                x='Month', 
                y=['NCRs', 'Inspections'],
                title='Quality Metrics by Month',
                markers=True,
                labels={'value': 'Count', 'variable': 'Metric'}
            )
            
            # Improve layout for better display
            fig.update_layout(
                height=300,
                margin=dict(l=10, r=10, t=40, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            # Container styling without raw HTML
            with st.container():
                st.plotly_chart(fig, use_container_width=True)
    
    with col_activity:
        st.subheader("Recent Activity")
        
        # Recent activity feed
        activities = [
            {"type": "RFI", "project": "Highland Tower", "description": "RFI #123 was answered", "time": "2 hours ago", "icon": "question_answer", "color": "#3e79f7"},
            {"type": "Submittal", "project": "Highland Tower", "description": "Submittal #45 was approved", "time": "Yesterday", "icon": "assignment_turned_in", "color": "#38d39f"},
            {"type": "Project", "project": "Highland Tower", "description": "New milestone added", "time": "2 days ago", "icon": "flag", "color": "#f9c851"},
            {"type": "Task", "project": "Highland Tower", "description": "Task assigned to John Smith", "time": "3 days ago", "icon": "assignment", "color": "#6c757d"},
            {"type": "Document", "project": "Highland Tower", "description": "New document uploaded", "time": "4 days ago", "icon": "description", "color": "#6c757d"},
            {"type": "Safety", "project": "Highland Tower", "description": "Safety meeting scheduled", "time": "5 days ago", "icon": "health_and_safety", "color": "#ff5b5b"}
        ]
        
        st.markdown("<div class='dashboard-card' style='padding: 0;'>", unsafe_allow_html=True)
        
        for activity in activities:
            st.markdown(
                f"""
                <div style="display: flex; padding: 0.8rem 1rem; border-bottom: 1px solid #eee;">
                    <div style="width: 32px; height: 32px; border-radius: 50%; 
                               background-color: {activity['color']}20; color: {activity['color']}; 
                               display: flex; justify-content: center; align-items: center; 
                               margin-right: 0.8rem;">
                        <span class="material-icons" style="font-size: 1rem;">
                            {activity['icon']}
                        </span>
                    </div>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 500;">{activity['type']}: {activity['description']}</div>
                        <div style="font-size: 0.8rem; color: #6c757d;">{activity['time']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_enhanced_project_status_section(current_project):
    """Render enhanced project status with real-time data integration"""
    st.markdown("### 🏗️ Enhanced Project Status")
    
    # Real-time project metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Overall Progress", "72%", "+3% this week", delta_color="normal")
    
    with col2:
        st.metric("Budget Status", "$32.8M", "-2.3% under budget", delta_color="inverse")
    
    with col3:
        st.metric("Schedule Status", "On Track", "+2 days ahead", delta_color="normal")
    
    with col4:
        st.metric("Quality Score", "94%", "+2% improvement", delta_color="normal")
    
    with col5:
        st.metric("Safety Score", "98%", "0 incidents this week", delta_color="normal")

def render_critical_path_alerts_section():
    """Render critical path alerts and schedule dependencies"""
    st.markdown("### ⚠️ Critical Path Alerts")
    
    alerts = [
        {
            "severity": "high",
            "task": "Foundation Inspection",
            "impact": "2-day delay risk",
            "action": "Schedule inspector for tomorrow",
            "responsible": "John Smith"
        },
        {
            "severity": "medium", 
            "task": "Steel Delivery",
            "impact": "Potential 1-week delay",
            "action": "Confirm delivery schedule",
            "responsible": "Sarah Johnson"
        }
    ]
    
    for alert in alerts:
        severity_color = "#ff4444" if alert["severity"] == "high" else "#ff8800"
        st.markdown(
            f"""
            <div style="border-left: 4px solid {severity_color}; padding: 12px; margin: 8px 0; background-color: #f8f9fa;">
                <strong>🚨 {alert["task"]}</strong><br>
                <span style="color: {severity_color};">Impact: {alert["impact"]}</span><br>
                Action: {alert["action"]} (Assigned: {alert["responsible"]})
            </div>
            """,
            unsafe_allow_html=True
        )

def render_weather_impact_section():
    """Render weather conditions affecting construction"""
    st.markdown("### 🌤️ Weather Impact Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Current Conditions**")
        st.markdown("🌤️ Partly Cloudy")
        st.markdown("🌡️ 72°F")
        st.markdown("💨 Wind: 8 mph")
        st.markdown("💧 Humidity: 45%")
    
    with col2:
        st.markdown("**Today's Impact**")
        st.markdown("✅ Concrete work: Favorable")
        st.markdown("✅ Exterior work: Good conditions")
        st.markdown("⚠️ High work: Monitor wind")
        st.markdown("✅ Material delivery: Clear")
    
    with col3:
        st.markdown("**3-Day Forecast**")
        st.markdown("🌤️ Tomorrow: Partly cloudy, 75°F")
        st.markdown("☀️ Friday: Sunny, 78°F")
        st.markdown("🌧️ Saturday: Rain expected")

def render_customizable_widgets_section():
    """Render customizable dashboard widgets"""
    st.markdown("### 🎛️ Customizable Widgets")
    
    # Widget customization options
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("**Widget Options**")
        widget_options = st.multiselect(
            "Select widgets to display:",
            ["Project Timeline", "Budget Trend", "Team Activity", "Recent Photos", "Equipment Status"],
            default=["Project Timeline", "Budget Trend", "Team Activity"]
        )
    
    with col2:
        # Render selected widgets
        if "Project Timeline" in widget_options:
            st.markdown("**📅 Project Timeline**")
            timeline_data = pd.DataFrame({
                'Phase': ['Foundation', 'Structure', 'Envelope', 'MEP', 'Finishes'],
                'Progress': [100, 85, 60, 30, 10]
            })
            st.bar_chart(timeline_data.set_index('Phase'))
        
        if "Budget Trend" in widget_options:
            st.markdown("**💰 Budget Trend**")
            budget_data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                'Planned': [2000000, 4500000, 7200000, 10800000, 15200000],
                'Actual': [1950000, 4350000, 7050000, 10500000, 14800000]
            })
            st.line_chart(budget_data.set_index('Month'))
        
        if "Team Activity" in widget_options:
            st.markdown("**👥 Team Activity**")
            st.markdown("- 🟢 12 team members active")
            st.markdown("- 📋 8 tasks completed today")
            st.markdown("- 💬 15 new messages")
            st.markdown("- 📊 3 reports submitted")
    
    # Upcoming deadlines section
    st.subheader("Upcoming Deadlines")
    
    # Upcoming deadlines data
    deadlines = [
        {"task": "Submit Foundation Inspection", "date": "May 20, 2025", "assigned": "John Smith", "status": "Pending", "type": "Inspection"},
        {"task": "MEP Coordination Meeting", "date": "May 22, 2025", "assigned": "Sarah Johnson", "status": "Scheduled", "type": "Meeting"},
        {"task": "Structural Steel Submittal Review", "date": "May 25, 2025", "assigned": "Robert Chen", "status": "In Progress", "type": "Submittal"},
        {"task": "Update Project Schedule", "date": "May 27, 2025", "assigned": "John Smith", "status": "Not Started", "type": "Task"}
    ]
    
    col1, col2, col3, col4 = st.columns(4)
    
    for idx, deadline in enumerate(deadlines):
        # Determine status color
        status_color = "#6c757d"  # Default gray
        if deadline["status"] == "Completed":
            status_color = "#38d39f"  # Green
        elif deadline["status"] == "Pending" or deadline["status"] == "In Progress":
            status_color = "#f9c851"  # Yellow
        elif deadline["status"] == "Overdue":
            status_color = "#ff5b5b"  # Red
        
        # Determine type icon
        type_icon = "task"
        if deadline["type"] == "Meeting":
            type_icon = "groups"
        elif deadline["type"] == "Inspection":
            type_icon = "check_circle"
        elif deadline["type"] == "Submittal":
            type_icon = "description"
        
        if idx == 0:
            with col1:
                st.markdown(
                    f"""
                    <div class="dashboard-card" style="height: 100%;">
                        <div style="display: flex; margin-bottom: 0.5rem;">
                            <span class="material-icons" style="color: {status_color}; margin-right: 0.5rem;">
                                {type_icon}
                            </span>
                            <span style="font-size: 0.8rem; color: #6c757d; text-transform: uppercase;">{deadline["type"]}</span>
                        </div>
                        <div style="font-weight: 500; margin-bottom: 0.5rem;">{deadline["task"]}</div>
                        <div style="font-size: 0.9rem; color: #6c757d;">
                            <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.2rem;">
                                calendar_today
                            </span>
                            {deadline["date"]}
                        </div>
                        <div style="font-size: 0.9rem; color: #6c757d;">
                            <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.2rem;">
                                person
                            </span>
                            {deadline["assigned"]}
                        </div>
                        <div style="margin-top: 0.5rem;">
                            <span style="display: inline-block; padding: 0.2rem 0.5rem; border-radius: 4px; 
                                      font-size: 0.8rem; background-color: {status_color}20; color: {status_color};">
                                {deadline["status"]}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        elif idx == 1:
            with col2:
                st.markdown(
                    f"""
                    <div class="dashboard-card" style="height: 100%;">
                        <div style="display: flex; margin-bottom: 0.5rem;">
                            <span class="material-icons" style="color: {status_color}; margin-right: 0.5rem;">
                                {type_icon}
                            </span>
                            <span style="font-size: 0.8rem; color: #6c757d; text-transform: uppercase;">{deadline["type"]}</span>
                        </div>
                        <div style="font-weight: 500; margin-bottom: 0.5rem;">{deadline["task"]}</div>
                        <div style="font-size: 0.9rem; color: #6c757d;">
                            <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.2rem;">
                                calendar_today
                            </span>
                            {deadline["date"]}
                        </div>
                        <div style="font-size: 0.9rem; color: #6c757d;">
                            <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.2rem;">
                                person
                            </span>
                            {deadline["assigned"]}
                        </div>
                        <div style="margin-top: 0.5rem;">
                            <span style="display: inline-block; padding: 0.2rem 0.5rem; border-radius: 4px; 
                                      font-size: 0.8rem; background-color: {status_color}20; color: {status_color};">
                                {deadline["status"]}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        elif idx == 2:
            with col3:
                st.markdown(
                    f"""
                    <div class="dashboard-card" style="height: 100%;">
                        <div style="display: flex; margin-bottom: 0.5rem;">
                            <span class="material-icons" style="color: {status_color}; margin-right: 0.5rem;">
                                {type_icon}
                            </span>
                            <span style="font-size: 0.8rem; color: #6c757d; text-transform: uppercase;">{deadline["type"]}</span>
                        </div>
                        <div style="font-weight: 500; margin-bottom: 0.5rem;">{deadline["task"]}</div>
                        <div style="font-size: 0.9rem; color: #6c757d;">
                            <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.2rem;">
                                calendar_today
                            </span>
                            {deadline["date"]}
                        </div>
                        <div style="font-size: 0.9rem; color: #6c757d;">
                            <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.2rem;">
                                person
                            </span>
                            {deadline["assigned"]}
                        </div>
                        <div style="margin-top: 0.5rem;">
                            <span style="display: inline-block; padding: 0.2rem 0.5rem; border-radius: 4px; 
                                      font-size: 0.8rem; background-color: {status_color}20; color: {status_color};">
                                {deadline["status"]}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        elif idx == 3:
            with col4:
                st.markdown(
                    f"""
                    <div class="dashboard-card" style="height: 100%;">
                        <div style="display: flex; margin-bottom: 0.5rem;">
                            <span class="material-icons" style="color: {status_color}; margin-right: 0.5rem;">
                                {type_icon}
                            </span>
                            <span style="font-size: 0.8rem; color: #6c757d; text-transform: uppercase;">{deadline["type"]}</span>
                        </div>
                        <div style="font-weight: 500; margin-bottom: 0.5rem;">{deadline["task"]}</div>
                        <div style="font-size: 0.9rem; color: #6c757d;">
                            <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.2rem;">
                                calendar_today
                            </span>
                            {deadline["date"]}
                        </div>
                        <div style="font-size: 0.9rem; color: #6c757d;">
                            <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.2rem;">
                                person
                            </span>
                            {deadline["assigned"]}
                        </div>
                        <div style="margin-top: 0.5rem;">
                            <span style="display: inline-block; padding: 0.2rem 0.5rem; border-radius: 4px; 
                                      font-size: 0.8rem; background-color: {status_color}20; color: {status_color};">
                                {deadline["status"]}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )