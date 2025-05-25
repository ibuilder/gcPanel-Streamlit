"""
🏗️ gcPanel Construction Management - Highland Tower Development
Central construction management hub for the $45.5M mixed-use development project
120 Residential + 8 Retail Units • 15 Stories Above + 2 Below Ground
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render():
    """Render the comprehensive Construction Management hub"""
    st.title("🏗️ gcPanel Construction Management")
    st.markdown("**Highland Tower Development • $45.5M Investment**")
    st.markdown("*120 Residential + 8 Retail Units • 15 Stories Above + 2 Below Ground*")
    
    # Project status overview
    render_project_overview()
    
    # Main management tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Executive Dashboard", "👥 Team Management", "📊 Project Control", "🚨 Critical Issues", "📈 Performance", "⚙️ System Admin"
    ])
    
    with tab1:
        render_executive_dashboard()
    
    with tab2:
        render_team_management()
    
    with tab3:
        render_project_control()
    
    with tab4:
        render_critical_issues()
    
    with tab5:
        render_performance_metrics()
    
    with tab6:
        render_system_admin()

def render_project_overview():
    """Highland Tower Development project overview"""
    st.markdown("### 📋 Project Status Overview")
    
    # Real-time project metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Project Progress", "67.3%", "2.1% this week", help="Overall completion vs baseline schedule")
    with col2:
        st.metric("Budget Status", "$30.5M", "-$2.1M under", help="Spent vs $45.5M total budget")
    with col3:
        st.metric("Schedule Health", "5 Days Ahead", "Ahead of schedule", help="Current vs planned timeline")
    with col4:
        st.metric("Safety Rating", "98.5%", "+0.5% improvement", help="OSHA compliance score")
    with col5:
        st.metric("Quality Score", "96.2%", "+1.2% this month", help="QC inspections passed")
    
    # Current phase status
    st.markdown("### 🏗️ Current Construction Phase")
    
    phase_data = [
        {"Phase": "Foundation", "Status": "Complete", "Progress": 100, "Start": "2025-01-15", "End": "2025-03-10"},
        {"Phase": "Structural Steel", "Status": "Active", "Progress": 85, "Start": "2025-03-15", "End": "2025-06-20"},
        {"Phase": "MEP Rough-in", "Status": "Active", "Progress": 65, "Start": "2025-04-01", "End": "2025-08-15"},
        {"Phase": "Building Envelope", "Status": "Starting", "Progress": 15, "Start": "2025-06-01", "End": "2025-09-30"},
        {"Phase": "Interior Finishes", "Status": "Planned", "Progress": 0, "Start": "2025-08-15", "End": "2025-11-30"},
        {"Phase": "Final Inspections", "Status": "Planned", "Progress": 0, "Start": "2025-11-15", "End": "2025-12-20"}
    ]
    
    for phase in phase_data:
        status_colors = {
            "Complete": "#28a745",
            "Active": "#007bff", 
            "Starting": "#fd7e14",
            "Planned": "#6c757d"
        }
        
        color = status_colors.get(phase["Status"], "#6c757d")
        
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div style="border-left: 4px solid {color}; padding-left: 12px; margin: 8px 0;">
                <strong>{phase['Phase']}</strong><br>
                <small>{phase['Start']} → {phase['End']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.progress(phase["Progress"] / 100)
        
        with col3:
            st.markdown(f"**{phase['Progress']}%**")
        
        with col4:
            st.markdown(f"<span style='color: {color}; font-weight: bold;'>{phase['Status']}</span>", unsafe_allow_html=True)

def render_executive_dashboard():
    """Executive-level project dashboard"""
    st.subheader("🎯 Executive Dashboard - Highland Tower Development")
    
    # Quick action buttons for executives
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📊 Weekly Report", use_container_width=True):
            st.success("📄 Generating executive weekly report...")
    
    with col2:
        if st.button("💰 Financial Review", use_container_width=True):
            st.session_state.current_menu = "Cost Management"
            st.rerun()
    
    with col3:
        if st.button("🚨 Risk Dashboard", use_container_width=True):
            st.warning("⚠️ Opening risk management dashboard...")
    
    with col4:
        if st.button("👥 Stakeholder Update", use_container_width=True):
            st.info("📧 Preparing stakeholder communication...")
    
    with col5:
        if st.button("📈 Performance Analytics", use_container_width=True):
            st.session_state.current_menu = "Analytics"
            st.rerun()
    
    # Executive summary cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💼 Executive Summary")
        st.markdown("""
        **Highland Tower Development Status:**
        
        ✅ **On Schedule:** 5 days ahead of baseline  
        ✅ **Under Budget:** $2.1M projected savings  
        ✅ **Safety Excellence:** 98.5% compliance rating  
        ⚠️ **Watch Items:** Steel delivery scheduling  
        
        **Key Achievements This Week:**
        - Level 13 steel erection 85% complete
        - MEP rough-in progressing ahead of schedule
        - Zero safety incidents for 45 consecutive days
        - Budget variance improved by $340K
        
        **Upcoming Milestones:**
        - Structural steel completion: June 15, 2025
        - Building envelope start: June 1, 2025
        - MEP rough-in completion: August 15, 2025
        """)
    
    with col2:
        st.markdown("#### 📊 Financial Performance")
        
        # Financial chart
        financial_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'Planned': [2.1, 4.5, 8.2, 12.8, 18.5],
            'Actual': [2.0, 4.2, 7.9, 12.3, 17.8],
            'Forecast': [2.0, 4.2, 7.9, 12.3, 17.8]
        })
        
        fig = px.line(financial_data, x='Month', y=['Planned', 'Actual'], 
                     title="Cumulative Spending (Millions $)")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Budget status
        st.metric("Budget Utilization", "67.2%", "2.8% under plan")
        st.metric("Cash Flow Status", "Positive", "$1.2M available")

def render_team_management():
    """Team and resource management"""
    st.subheader("👥 Team Management - Highland Tower Development")
    
    # Team overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Workforce", "89 Active", "+5 this week")
    with col2:
        st.metric("Prime Contractor", "34 Workers", "Highland Construction")
    with col3:
        st.metric("Subcontractors", "55 Workers", "12 companies")
    with col4:
        st.metric("Management Staff", "8 Personnel", "On-site daily")
    
    # Current team assignments
    st.markdown("### 🏗️ Current Team Assignments")
    
    team_assignments = pd.DataFrame([
        {
            "Trade": "Structural Steel",
            "Company": "Highland Steel Works",
            "Workers": 12,
            "Location": "Level 13",
            "Supervisor": "Mike Rodriguez",
            "Status": "Active",
            "Progress": "85%"
        },
        {
            "Trade": "MEP - Electrical", 
            "Company": "Elite Electrical",
            "Workers": 8,
            "Location": "Levels 9-11",
            "Supervisor": "Sarah Chen",
            "Status": "Active", 
            "Progress": "70%"
        },
        {
            "Trade": "MEP - Plumbing",
            "Company": "Premium Plumbing",
            "Workers": 6,
            "Location": "Levels 9-11", 
            "Supervisor": "David Kim",
            "Status": "Active",
            "Progress": "65%"
        },
        {
            "Trade": "MEP - HVAC",
            "Company": "Climate Control Pro",
            "Workers": 7,
            "Location": "Levels 8-10",
            "Supervisor": "Jennifer Walsh", 
            "Status": "Active",
            "Progress": "60%"
        },
        {
            "Trade": "Concrete Finishing",
            "Company": "Precision Concrete",
            "Workers": 10,
            "Location": "Level 12",
            "Supervisor": "Antonio Silva",
            "Status": "Standby",
            "Progress": "100%"
        }
    ])
    
    st.dataframe(team_assignments, use_container_width=True)
    
    # Team communication tools
    st.markdown("### 📢 Team Communication")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📱 Send Team Alert", use_container_width=True):
            st.success("📲 Team alert sent to all active crews")
    
    with col2:
        if st.button("📅 Schedule Meeting", use_container_width=True):
            st.info("📅 Opening meeting scheduler...")
    
    with col3:
        if st.button("📋 Daily Briefing", use_container_width=True):
            st.info("📋 Preparing daily briefing materials...")

def render_project_control():
    """Integrated project control center"""
    st.subheader("📊 Project Control Center")
    
    # Control metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Schedule Performance", "SPI: 1.05", "5% ahead")
    with col2:
        st.metric("Cost Performance", "CPI: 1.04", "4% under budget")
    with col3:
        st.metric("Quality Index", "96.2%", "Excellent")
    with col4:
        st.metric("Risk Level", "Low", "Well controlled")
    
    # Integrated module access
    st.markdown("### 🎛️ Project Control Modules")
    
    control_modules = [
        ("📅", "Scheduling", "Master schedule and critical path", "On track"),
        ("💰", "Cost Management", "Budget tracking and forecasting", "Under budget"),
        ("🔍", "Quality Control", "Inspections and compliance", "Excellent"),
        ("🦺", "Safety Management", "Safety compliance and reporting", "98.5% rating"),
        ("📸", "Progress Photos", "Visual documentation and tracking", "2,847 photos"),
        ("📋", "Change Orders", "Design and scope modifications", "12 active COs"),
        ("📄", "Document Control", "Plans, specs, and submittals", "All current"),
        ("🏢", "BIM Coordination", "3D modeling and clash detection", "Zero clashes")
    ]
    
    # Display in 2x4 grid
    for i in range(0, len(control_modules), 2):
        col1, col2 = st.columns(2)
        
        # First module
        if i < len(control_modules):
            icon, name, desc, status = control_modules[i]
            with col1:
                with st.container():
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 8px 0; background: white;">
                        <h4>{icon} {name}</h4>
                        <p style="color: #666; margin: 8px 0;">{desc}</p>
                        <div style="color: #28a745; font-weight: bold;">Status: {status}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Open {name}", key=f"open_{name}"):
                        st.session_state.current_menu = name
                        st.rerun()
        
        # Second module
        if i + 1 < len(control_modules):
            icon, name, desc, status = control_modules[i + 1]
            with col2:
                with st.container():
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 8px 0; background: white;">
                        <h4>{icon} {name}</h4>
                        <p style="color: #666; margin: 8px 0;">{desc}</p>
                        <div style="color: #28a745; font-weight: bold;">Status: {status}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Open {name}", key=f"open_{name}"):
                        st.session_state.current_menu = name
                        st.rerun()

def render_critical_issues():
    """Critical issues and risk management"""
    st.subheader("🚨 Critical Issues & Risk Management")
    
    # Issue priority overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Critical Issues", "2", "Require immediate attention")
    with col2:
        st.metric("High Priority", "5", "Need resolution this week")
    with col3:
        st.metric("Medium Priority", "12", "Monitor closely")
    with col4:
        st.metric("Risk Score", "Low", "Well managed")
    
    # Current critical issues
    st.markdown("### 🚨 Current Critical Issues")
    
    critical_issues = [
        {
            "Issue": "Steel delivery delay risk",
            "Priority": "Critical",
            "Description": "Potential 3-day delay in Level 14-15 steel delivery due to supplier logistics",
            "Impact": "Schedule delay, resource reallocation needed",
            "Action": "Alternative supplier identified, expedited shipping arranged",
            "Owner": "Construction Manager",
            "Due": "2025-05-28"
        },
        {
            "Issue": "MEP coordination conflict", 
            "Priority": "High",
            "Description": "Electrical conduit routing conflicts with HVAC ducts in Level 11 ceiling",
            "Impact": "Rework required, potential 2-day delay",
            "Action": "Coordination meeting scheduled, BIM clash detection updated",
            "Owner": "MEP Coordinator",
            "Due": "2025-05-26"
        }
    ]
    
    for issue in critical_issues:
        priority_colors = {"Critical": "#dc3545", "High": "#fd7e14", "Medium": "#ffc107"}
        color = priority_colors.get(issue["Priority"], "#6c757d")
        
        with st.expander(f"🚨 {issue['Issue']} - {issue['Priority']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div style="border-left: 4px solid {color}; padding-left: 12px;">
                <strong>Description:</strong> {issue['Description']}<br>
                <strong>Impact:</strong> {issue['Impact']}<br>
                <strong>Action Plan:</strong> {issue['Action']}<br>
                <strong>Owner:</strong> {issue['Owner']}<br>
                <strong>Due Date:</strong> {issue['Due']}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("📝 Update", key=f"update_{issue['Issue']}"):
                    st.info("Opening issue update form...")
                
                if st.button("✅ Resolve", key=f"resolve_{issue['Issue']}"):
                    st.success("Issue marked as resolved!")
    
    # Risk mitigation strategies
    st.markdown("### 🛡️ Risk Mitigation Strategies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Active Risk Mitigations:**
        
        ✅ **Weather Contingency:** 10-day buffer built into schedule  
        ✅ **Supplier Backup:** Alternative suppliers identified for critical materials  
        ✅ **Labor Pool:** Cross-trained crews available for flexibility  
        ✅ **Cash Flow:** $1.5M contingency fund maintained  
        """)
    
    with col2:
        st.markdown("""
        **Monitoring & Controls:**
        
        📊 **Daily Risk Assessment:** Morning safety/risk briefings  
        📈 **Trend Analysis:** Weekly risk score trending  
        🔔 **Early Warning System:** Automated alerts for schedule/budget variance  
        📋 **Lessons Learned:** Continuous improvement documentation  
        """)

def render_performance_metrics():
    """Comprehensive performance analytics"""
    st.subheader("📈 Performance Metrics & Analytics")
    
    # Performance dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        # Schedule performance trend
        schedule_data = pd.DataFrame({
            'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
            'Planned': [10, 22, 35, 48, 62],
            'Actual': [11, 24, 37, 50, 67]
        })
        
        fig = px.line(schedule_data, x='Week', y=['Planned', 'Actual'],
                     title="Schedule Performance Index")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cost performance trend
        cost_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'Budget': [2.1, 4.5, 8.2, 12.8, 18.5],
            'Actual': [2.0, 4.2, 7.9, 12.3, 17.8]
        })
        
        fig = px.bar(cost_data, x='Month', y=['Budget', 'Actual'],
                    title="Cost Performance (Millions $)", barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    # Key performance indicators
    st.markdown("### 📊 Key Performance Indicators")
    
    kpi_data = pd.DataFrame([
        {"KPI": "Schedule Performance Index (SPI)", "Current": 1.05, "Target": 1.00, "Status": "Excellent"},
        {"KPI": "Cost Performance Index (CPI)", "Current": 1.04, "Target": 1.00, "Status": "Excellent"},
        {"KPI": "Quality Performance Index", "Current": 0.96, "Target": 0.95, "Status": "Good"},
        {"KPI": "Safety Performance Rating", "Current": 0.985, "Target": 0.95, "Status": "Excellent"},
        {"KPI": "Productivity Rate", "Current": 1.12, "Target": 1.00, "Status": "Excellent"},
        {"KPI": "Resource Utilization", "Current": 0.94, "Target": 0.90, "Status": "Good"}
    ])
    
    st.dataframe(kpi_data, use_container_width=True)

def render_system_admin():
    """System administration and settings"""
    st.subheader("⚙️ System Administration")
    
    # Admin functions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👥 User Management")
        
        if st.button("👤 Add New User", use_container_width=True):
            st.info("Opening user registration form...")
        
        if st.button("🔐 Manage Permissions", use_container_width=True):
            st.info("Opening role-based access control...")
        
        if st.button("📊 User Activity Report", use_container_width=True):
            st.success("Generating user activity analytics...")
        
        st.markdown("#### 🔧 System Configuration")
        
        if st.button("⚙️ Module Settings", use_container_width=True):
            st.info("Opening module configuration panel...")
        
        if st.button("🔔 Notification Setup", use_container_width=True):
            st.info("Configuring alert and notification settings...")
        
        if st.button("💾 Backup Management", use_container_width=True):
            st.success("System backup initiated...")
    
    with col2:
        st.markdown("#### 🏢 Project Configuration")
        
        if st.button("🏗️ Project Settings", use_container_width=True):
            st.info("Highland Tower Development project configuration...")
        
        if st.button("📋 Workflow Templates", use_container_width=True):
            st.info("Managing construction workflow templates...")
        
        if st.button("🔗 Integration Setup", use_container_width=True):
            st.info("External system integration management...")
        
        st.markdown("#### 📊 System Health")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("System Status", "Operational", "All systems green")
        with col_b:
            st.metric("Database Size", "2.4 GB", "Growing normally")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Active Users", "24", "Peak: 31")
        with col_b:
            st.metric("Uptime", "99.8%", "Last 30 days")

if __name__ == "__main__":
    render()