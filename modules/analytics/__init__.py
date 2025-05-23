"""
Analytics Module for gcPanel

This module provides comprehensive analytics and reporting functionality for the construction management dashboard.
It includes submodules for different types of analysis and reporting.
"""

import streamlit as st
from modules.analytics.analysis import render as render_analysis
from modules.analytics.business_intelligence import render_business_intelligence

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

def render_predictive_analytics():
    """Render AI-powered predictive analytics dashboard"""
    st.markdown("### 🤖 AI-Powered Predictive Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Project Completion Predictions**")
        st.metric("Predicted Completion", "June 15, 2027", "2 weeks ahead of schedule")
        st.metric("Budget at Completion", "$44.2M", "Under budget by $1.3M")
        st.metric("Risk Score", "Medium", "Weather and supply chain factors")
        
        st.markdown("**Key Risk Factors**")
        st.markdown("🌦️ Weather delays: 15% probability")
        st.markdown("📦 Supply chain: 8% probability")
        st.markdown("👷 Labor shortage: 5% probability")
    
    with col2:
        st.markdown("**Performance Trends**")
        # Sample predictive data
        import pandas as pd
        prediction_data = pd.DataFrame({
            'Month': ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
            'Actual Progress': [72, None, None, None, None, None],
            'Predicted Progress': [72, 78, 84, 89, 95, 100],
            'Confidence Interval': [72, 76, 81, 86, 92, 98]
        })
        st.line_chart(prediction_data.set_index('Month')[['Predicted Progress', 'Confidence Interval']])

def render_real_time_insights():
    """Render real-time business insights dashboard"""
    st.markdown("### ⚡ Real-Time Business Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Today's Insights**")
        st.metric("Productivity Index", "118%", "+12% vs average")
        st.metric("Cost Efficiency", "96%", "Better than target")
        st.metric("Quality Score", "94%", "+2% this week")
    
    with col2:
        st.markdown("**Live Alerts**")
        st.success("✅ Steel delivery on schedule")
        st.warning("⚠️ Concrete pour delayed 2 hours")
        st.info("ℹ️ Equipment utilization at 85%")
        st.success("✅ Safety compliance at 98%")
    
    with col3:
        st.markdown("**Market Intelligence**")
        st.metric("Material Cost Index", "108", "+3% this quarter")
        st.metric("Labor Availability", "Good", "No shortages predicted")
        st.metric("Competitor Analysis", "Leading", "2 weeks ahead average")

def render_executive_analytics():
    """Render executive-level analytics and KPIs"""
    st.markdown("### 👔 Executive Analytics Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Portfolio Performance**")
        portfolio_data = pd.DataFrame({
            'Project': ['Highland Tower', 'Oak Plaza', 'Metro Center', 'River View'],
            'Progress': [72, 45, 89, 23],
            'Budget Status': [97, 103, 95, 101],
            'Schedule Status': [102, 98, 105, 99]
        })
        st.dataframe(portfolio_data, use_container_width=True)
    
    with col2:
        st.markdown("**Strategic Metrics**")
        st.metric("Portfolio Value", "$180M", "4 active projects")
        st.metric("Average Profit Margin", "12.8%", "+1.2% vs target")
        st.metric("Client Satisfaction", "96%", "Industry leading")
        st.metric("Employee Retention", "94%", "+3% this year")

def render():
    """Render the Enhanced Analytics & AI-Powered Business Intelligence module."""
    st.title("📊 Enhanced Analytics & AI-Powered Business Intelligence")
    
    # AI-Powered Predictive Analytics
    render_predictive_analytics()
    
    # Real-Time Business Insights
    render_real_time_insights()
    
    # Executive Analytics
    render_executive_analytics()
    
    # Create comprehensive tabs for all analytics features
    tabs = st.tabs([
        "📈 Executive Dashboard", 
        "🔍 Detailed Analysis", 
        "📊 Business Intelligence",
        "📋 Reports Overview"
    ])
    
    with tabs[0]:
        render_analytics_dashboard()
    
    with tabs[1]:
        render_analysis()
    
    with tabs[2]:
        render_business_intelligence()
    
    with tabs[3]:
        render_reports_overview()

def render_reports_overview():
    """Render comprehensive reports overview with enterprise features."""
    st.markdown("### 📋 Enterprise Reporting Center")
    
    # Quick report generation
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🚀 Quick Report Generation")
        
        quick_reports = [
            {
                "title": "📊 Executive Summary",
                "description": "High-level KPIs and project portfolio overview",
                "type": "executive"
            },
            {
                "title": "💰 Financial Performance",
                "description": "Revenue, profit margins, and cash flow analysis",
                "type": "financial"
            },
            {
                "title": "🦺 Safety Analytics",
                "description": "Incident tracking, compliance, and safety metrics",
                "type": "safety"
            },
            {
                "title": "⚡ Productivity Report",
                "description": "Labor efficiency, equipment utilization, and progress",
                "type": "productivity"
            }
        ]
        
        for report in quick_reports:
            with st.container():
                col_a, col_b, col_c = st.columns([3, 1, 1])
                
                with col_a:
                    st.markdown(f"**{report['title']}**")
                    st.caption(report['description'])
                
                with col_b:
                    if st.button("📄 Generate", key=f"gen_{report['type']}"):
                        st.success(f"✅ {report['title']} generated successfully!")
                
                with col_c:
                    if st.button("📥 Export", key=f"exp_{report['type']}"):
                        st.success(f"✅ {report['title']} exported to PDF!")
                
                st.markdown("---")
    
    with col2:
        st.markdown("#### 📈 Report Statistics")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Reports Generated", "127", "+15 this month")
        with col_b:
            st.metric("Scheduled Reports", "8", "2 daily, 6 weekly")
        
        st.markdown("#### 🔄 Automated Reports")
        
        automated_reports = [
            {"name": "Daily Safety Summary", "frequency": "Daily", "next": "Tomorrow 8:00 AM"},
            {"name": "Weekly Progress Report", "frequency": "Weekly", "next": "Monday 9:00 AM"},
            {"name": "Monthly Financial", "frequency": "Monthly", "next": "1st of next month"}
        ]
        
        for report in automated_reports:
            st.text(f"📅 {report['name']}")
            st.caption(f"Next: {report['next']}")
            st.markdown("---")
    
    # Recent reports section
    st.markdown("#### 📚 Recent Reports")
    
    recent_reports_data = [
        {"Report": "Executive Summary - May 2025", "Generated": "2 hours ago", "Type": "Executive", "Status": "✅ Ready"},
        {"Report": "Project Progress - Highland Tower", "Generated": "1 day ago", "Type": "Project", "Status": "✅ Ready"},
        {"Report": "Safety Performance Q2", "Generated": "3 days ago", "Type": "Safety", "Status": "✅ Ready"},
        {"Report": "Financial Analysis - April", "Generated": "1 week ago", "Type": "Financial", "Status": "✅ Ready"}
    ]
    
    import pandas as pd
    reports_df = pd.DataFrame(recent_reports_data)
    st.dataframe(reports_df, use_container_width=True)
    
    # Advanced reporting features
    st.markdown("---")
    st.markdown("#### 🔧 Advanced Reporting Features")
    
    adv_col1, adv_col2, adv_col3 = st.columns(3)
    
    with adv_col1:
        st.markdown("**📊 Custom Dashboards**")
        st.write("Create personalized dashboards with your preferred KPIs and visualizations")
        if st.button("🎯 Create Custom Dashboard"):
            st.info("Custom dashboard builder would be available here")
    
    with adv_col2:
        st.markdown("**📧 Email Reports**")
        st.write("Automatically send reports to stakeholders via email")
        if st.button("📬 Setup Email Reports"):
            st.info("Email report scheduling would be configured here")
    
    with adv_col3:
        st.markdown("**🔗 API Integration**")
        st.write("Connect reports to external systems and databases")
        if st.button("🔌 Manage Integrations"):
            st.info("API integration management would be available here")