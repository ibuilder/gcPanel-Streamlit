"""
Enhanced Analytics & Reporting for Highland Tower Development
Executive dashboards with predictive analytics and custom reporting
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

def render_advanced_analytics():
    """Main analytics dashboard interface"""
    st.markdown("""
    <div class="enterprise-header">
        <h1>📊 Advanced Analytics & Intelligence</h1>
        <p>Highland Tower Development - Data-Driven Project Insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Analytics tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Executive Dashboard", 
        "🔮 Predictive Analytics", 
        "📈 Performance Metrics",
        "📋 Custom Reports",
        "📸 Progress Tracking"
    ])
    
    with tab1:
        render_executive_dashboard()
    
    with tab2:
        render_predictive_analytics()
    
    with tab3:
        render_performance_metrics()
    
    with tab4:
        render_custom_reports()
    
    with tab5:
        render_progress_tracking()

def render_executive_dashboard():
    """Executive-level KPI dashboard"""
    st.markdown("### 🎯 Highland Tower Executive Dashboard")
    st.caption("Real-time project health and performance indicators")
    
    # Key Performance Indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Project Completion",
            "67.3%",
            "2.1% this week",
            help="Overall project progress based on schedule milestones"
        )
    
    with col2:
        st.metric(
            "Budget Performance", 
            "94.2%",
            "-1.8% under budget",
            help="Current budget utilization vs planned spending"
        )
    
    with col3:
        st.metric(
            "Schedule Variance",
            "+3 days",
            "Improved 2 days",
            help="Schedule performance against baseline"
        )
    
    with col4:
        st.metric(
            "Safety Score",
            "9.6/10",
            "+0.2 this month",
            help="Composite safety performance rating"
        )
    
    # Executive summary charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Project progress over time
        dates = pd.date_range(start='2024-01-01', end='2025-01-27', freq='W')
        planned_progress = np.cumsum(np.random.normal(2.5, 0.5, len(dates)))
        actual_progress = np.cumsum(np.random.normal(2.3, 0.7, len(dates)))
        
        # Ensure final values are realistic
        planned_progress = planned_progress * (70 / planned_progress[-1])
        actual_progress = actual_progress * (67.3 / actual_progress[-1])
        
        fig_progress = go.Figure()
        fig_progress.add_trace(go.Scatter(
            x=dates, y=planned_progress,
            mode='lines', name='Planned Progress',
            line=dict(color='blue', dash='dash')
        ))
        fig_progress.add_trace(go.Scatter(
            x=dates, y=actual_progress,
            mode='lines+markers', name='Actual Progress',
            line=dict(color='green')
        ))
        
        fig_progress.update_layout(
            title='Project Progress Tracking',
            xaxis_title='Date',
            yaxis_title='Completion %',
            height=400
        )
        st.plotly_chart(fig_progress, use_container_width=True)
    
    with col2:
        # Budget performance
        budget_categories = ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'Other']
        budgeted = [12500000, 18200000, 3800000, 9200000, 1800000]
        actual = [11800000, 17950000, 3650000, 9450000, 1650000]
        
        fig_budget = go.Figure(data=[
            go.Bar(name='Budgeted', x=budget_categories, y=budgeted, marker_color='lightblue'),
            go.Bar(name='Actual', x=budget_categories, y=actual, marker_color='darkblue')
        ])
        
        fig_budget.update_layout(
            title='Budget Performance by Category',
            barmode='group',
            height=400,
            yaxis_title='Amount ($)'
        )
        st.plotly_chart(fig_budget, use_container_width=True)
    
    # Critical issues summary
    st.markdown("#### 🚨 Executive Attention Required")
    
    critical_items = [
        {
            'category': 'Schedule Risk',
            'item': 'Level 9-10 structural steel delivery delayed',
            'impact': 'High',
            'action': 'Expedited shipping arranged, minimal schedule impact expected',
            'owner': 'Jennifer Walsh'
        },
        {
            'category': 'Budget Variance',
            'item': 'MEP materials cost increase due to market conditions',
            'impact': 'Medium',
            'action': 'Value engineering review scheduled, alternative suppliers identified',
            'owner': 'David Kim'
        },
        {
            'category': 'Quality Concern',
            'item': 'Concrete testing results below spec on Level 7',
            'impact': 'High',
            'action': 'Core testing ordered, structural analysis in progress',
            'owner': 'Sarah Chen, PE'
        }
    ]
    
    for item in critical_items:
        with st.expander(f"⚠️ {item['category']}: {item['item'][:50]}..."):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Impact Level:** {item['impact']}")
                st.markdown(f"**Responsible:** {item['owner']}")
            
            with col2:
                st.markdown(f"**Action Plan:** {item['action']}")

def render_predictive_analytics():
    """AI-powered predictive insights"""
    st.markdown("### 🔮 Predictive Analytics Engine")
    st.caption("AI-powered forecasting for proactive project management")
    
    # Predictive models overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📅 Schedule Forecast")
        
        # Completion date prediction
        predicted_completion = datetime(2025, 8, 15)
        baseline_completion = datetime(2025, 8, 12)
        variance_days = (predicted_completion - baseline_completion).days
        
        st.metric(
            "Predicted Completion",
            predicted_completion.strftime("%B %d, %Y"),
            f"+{variance_days} days vs baseline"
        )
        
        # Risk factors
        st.markdown("**Risk Factors:**")
        st.markdown("• Weather delays: 35% probability")
        st.markdown("• Material delivery: 20% probability") 
        st.markdown("• Labor availability: 15% probability")
    
    with col2:
        st.markdown("#### 💰 Cost Forecast")
        
        predicted_cost = 46200000
        baseline_cost = 45500000
        variance_amount = predicted_cost - baseline_cost
        
        st.metric(
            "Predicted Final Cost",
            f"${predicted_cost:,.0f}",
            f"+${variance_amount:,.0f} (+{variance_amount/baseline_cost*100:.1f}%)"
        )
        
        # Cost drivers
        st.markdown("**Key Drivers:**")
        st.markdown("• Material inflation: +$450K")
        st.markdown("• Labor efficiency: -$180K")
        st.markdown("• Change orders: +$430K")
    
    with col3:
        st.markdown("#### ⚡ Performance Trends")
        
        productivity_trend = 102.3
        st.metric(
            "Productivity Index",
            f"{productivity_trend}%",
            "+2.3% vs last period"
        )
        
        # Trend indicators
        st.markdown("**Trend Analysis:**")
        st.markdown("• 📈 Improving: Structural work")
        st.markdown("• 📊 Stable: MEP installation") 
        st.markdown("• 📉 Declining: Finish work pace")
    
    # Predictive charts
    st.markdown("#### 📊 Forecasting Models")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Schedule risk probability
        weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6']
        on_time_prob = [95, 92, 88, 84, 79, 75]
        
        fig_risk = go.Figure()
        fig_risk.add_trace(go.Scatter(
            x=weeks, y=on_time_prob,
            mode='lines+markers',
            name='On-Time Probability',
            line=dict(color='orange', width=3),
            marker=dict(size=8)
        ))
        
        # Add threshold line
        fig_risk.add_hline(y=80, line_dash="dash", line_color="red", 
                          annotation_text="Risk Threshold")
        
        fig_risk.update_layout(
            title='Schedule Risk Forecast',
            xaxis_title='Future Weeks',
            yaxis_title='On-Time Probability (%)',
            height=350
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        # Cost variance prediction
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
        budget_variance = [-50000, -120000, 80000, 200000, 350000, 480000, 650000, 700000]
        
        fig_cost = go.Figure()
        fig_cost.add_trace(go.Bar(
            x=months, y=budget_variance,
            name='Predicted Variance',
            marker_color=['green' if x < 0 else 'red' for x in budget_variance]
        ))
        
        fig_cost.update_layout(
            title='Monthly Budget Variance Forecast',
            xaxis_title='Month',
            yaxis_title='Variance ($)',
            height=350
        )
        st.plotly_chart(fig_cost, use_container_width=True)
    
    # AI insights
    st.markdown("#### 🤖 AI-Generated Insights")
    
    insights = [
        {
            'type': 'Opportunity',
            'insight': 'Steel fabrication is 5% ahead of schedule. Consider accelerating MEP rough-in to capitalize on this lead.',
            'confidence': '87%',
            'impact': 'Medium'
        },
        {
            'type': 'Risk',
            'insight': 'Weather patterns suggest 40% chance of rain delays in next 2 weeks. Prepare indoor work alternatives.',
            'confidence': '73%',
            'impact': 'High'
        },
        {
            'type': 'Optimization',
            'insight': 'Labor productivity peaks between 7-11 AM. Scheduling critical tasks during this window could improve efficiency by 12%.',
            'confidence': '91%',
            'impact': 'Medium'
        }
    ]
    
    for insight in insights:
        insight_color = 'green' if insight['type'] == 'Opportunity' else 'red' if insight['type'] == 'Risk' else 'blue'
        
        with st.expander(f"🤖 {insight['type']}: {insight['insight'][:60]}..."):
            st.markdown(f"**Full Insight:** {insight['insight']}")
            st.markdown(f"**Confidence Level:** {insight['confidence']}")
            st.markdown(f"**Potential Impact:** {insight['impact']}")

def render_performance_metrics():
    """Detailed performance analytics"""
    st.markdown("### 📈 Performance Metrics & KPIs")
    
    # Metric categories
    metric_category = st.selectbox("Select Metric Category", [
        "Overall Project Health",
        "Schedule Performance", 
        "Cost Management",
        "Quality Metrics",
        "Safety Performance",
        "Team Productivity"
    ])
    
    if metric_category == "Overall Project Health":
        render_project_health_metrics()
    elif metric_category == "Schedule Performance":
        render_schedule_metrics()
    elif metric_category == "Cost Management":
        render_cost_metrics()
    elif metric_category == "Quality Metrics":
        render_quality_metrics()
    elif metric_category == "Safety Performance":
        render_safety_metrics()
    elif metric_category == "Team Productivity":
        render_productivity_metrics()

def render_project_health_metrics():
    """Overall project health dashboard"""
    st.markdown("#### 🏗️ Overall Project Health")
    
    # Health score components
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Schedule Health", "85%", "+3%")
    with col2:
        st.metric("Budget Health", "92%", "-1%")
    with col3:
        st.metric("Quality Health", "94%", "+2%")
    with col4:
        st.metric("Safety Health", "96%", "+1%")
    
    # Health trend over time
    dates = pd.date_range(start='2024-12-01', end='2025-01-27', freq='D')
    health_scores = 85 + np.cumsum(np.random.normal(0, 1, len(dates))) * 0.1
    health_scores = np.clip(health_scores, 75, 98)  # Keep realistic bounds
    
    fig_health = go.Figure()
    fig_health.add_trace(go.Scatter(
        x=dates, y=health_scores,
        mode='lines',
        name='Project Health Score',
        line=dict(color='green', width=2),
        fill='tonexty'
    ))
    
    # Add threshold zones
    fig_health.add_hline(y=90, line_dash="dash", line_color="green", 
                        annotation_text="Excellent (90%+)")
    fig_health.add_hline(y=80, line_dash="dash", line_color="orange",
                        annotation_text="Good (80%+)")
    fig_health.add_hline(y=70, line_dash="dash", line_color="red",
                        annotation_text="Needs Attention (70%+)")
    
    fig_health.update_layout(
        title='Project Health Score Trend',
        xaxis_title='Date',
        yaxis_title='Health Score (%)',
        height=400
    )
    st.plotly_chart(fig_health, use_container_width=True)

def render_schedule_metrics():
    """Schedule performance analytics"""
    st.markdown("#### 📅 Schedule Performance Analytics")
    
    # Schedule variance by trade
    trades = ['Structural', 'MEP', 'Architectural', 'Civil', 'Finishes']
    schedule_variance = [2, -1, 3, 0, -2]  # Days ahead/behind
    
    fig_schedule = go.Figure(data=[
        go.Bar(x=trades, y=schedule_variance,
               marker_color=['green' if x >= 0 else 'red' for x in schedule_variance])
    ])
    
    fig_schedule.update_layout(
        title='Schedule Variance by Trade (Days)',
        xaxis_title='Trade',
        yaxis_title='Days Ahead/Behind',
        height=400
    )
    st.plotly_chart(fig_schedule, use_container_width=True)

def render_cost_metrics():
    """Cost management analytics"""
    st.markdown("#### 💰 Cost Management Analytics")
    
    # Cost performance index over time
    weeks = list(range(1, 13))
    cpi_values = [1.0 + np.random.normal(0, 0.05) for _ in weeks]
    
    fig_cpi = go.Figure()
    fig_cpi.add_trace(go.Scatter(
        x=weeks, y=cpi_values,
        mode='lines+markers',
        name='Cost Performance Index',
        line=dict(color='blue', width=3)
    ))
    
    # Add benchmark line
    fig_cpi.add_hline(y=1.0, line_dash="dash", line_color="black",
                     annotation_text="Baseline (CPI = 1.0)")
    
    fig_cpi.update_layout(
        title='Cost Performance Index Trend',
        xaxis_title='Week',
        yaxis_title='CPI Value',
        height=400
    )
    st.plotly_chart(fig_cpi, use_container_width=True)

def render_quality_metrics():
    """Quality performance tracking"""
    st.markdown("#### 🎯 Quality Metrics")
    
    # Quality indicators
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Defect Rate", "0.8%", "-0.2%")
    with col2:
        st.metric("Rework Hours", "142", "-18 hours")
    with col3:
        st.metric("Inspection Pass Rate", "94.2%", "+1.5%")

def render_safety_metrics():
    """Safety performance dashboard"""
    st.markdown("#### 🛡️ Safety Performance")
    
    # Safety KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Days Without Incident", "127", "+1 day")
    with col2:
        st.metric("Near Miss Reports", "3", "This week")
    with col3:
        st.metric("Safety Training %", "98%", "All current")
    with col4:
        st.metric("PPE Compliance", "99.2%", "+0.5%")

def render_productivity_metrics():
    """Team productivity analytics"""
    st.markdown("#### ⚡ Team Productivity")
    
    # Productivity by trade
    trades = ['Structural', 'MEP', 'Architectural', 'Civil', 'Finishes']
    productivity = [112, 98, 105, 103, 94]  # Percentage of baseline
    
    fig_productivity = go.Figure(data=[
        go.Bar(x=trades, y=productivity,
               marker_color=['green' if x >= 100 else 'red' for x in productivity])
    ])
    
    fig_productivity.add_hline(y=100, line_dash="dash", line_color="black",
                              annotation_text="Baseline (100%)")
    
    fig_productivity.update_layout(
        title='Productivity Index by Trade',
        xaxis_title='Trade',
        yaxis_title='Productivity Index (%)',
        height=400
    )
    st.plotly_chart(fig_productivity, use_container_width=True)

def render_custom_reports():
    """Custom report builder"""
    st.markdown("### 📋 Custom Report Builder")
    
    # Report configuration
    with st.form("custom_report"):
        col1, col2 = st.columns(2)
        
        with col1:
            report_name = st.text_input("Report Name", "Highland Tower Weekly Executive Summary")
            
            report_type = st.selectbox("Report Type", [
                "Executive Summary",
                "Schedule Status",
                "Cost Performance", 
                "Safety Review",
                "Quality Assessment",
                "Progress Update"
            ])
            
            date_range = st.date_input("Report Period", 
                value=[datetime.now() - timedelta(days=7), datetime.now()])
        
        with col2:
            include_charts = st.multiselect("Include Charts", [
                "Project Progress",
                "Budget Performance",
                "Schedule Variance",
                "Safety Metrics",
                "Quality Indicators",
                "Productivity Trends"
            ], default=["Project Progress", "Budget Performance"])
            
            recipients = st.multiselect("Report Recipients", [
                "Executive Team",
                "Project Management", 
                "Field Supervision",
                "Engineering Team",
                "Safety Committee"
            ])
            
            delivery_method = st.selectbox("Delivery Method", [
                "Email (PDF)",
                "Dashboard Link",
                "Both Email and Dashboard"
            ])
        
        if st.form_submit_button("📊 Generate Report", type="primary"):
            st.success(f"✅ Custom report '{report_name}' generated successfully!")
            st.info("📧 Report delivered to selected recipients")
            
            # Show sample report preview
            with st.expander("📋 Report Preview"):
                st.markdown(f"**{report_name}**")
                st.markdown(f"**Period:** {date_range[0]} to {date_range[1]}")
                st.markdown("**Executive Summary:** Highland Tower Development continues to progress well with 67.3% completion...")

def render_progress_tracking():
    """Visual progress tracking with photos"""
    st.markdown("### 📸 Visual Progress Tracking")
    
    # Progress comparison interface
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Select Comparison Dates")
        comparison_date1 = st.date_input("From Date", datetime.now() - timedelta(days=30))
        comparison_date2 = st.date_input("To Date", datetime.now())
        
        location_filter = st.selectbox("Location", [
            "Overall Project",
            "Level 8 - Residential",
            "Level 9 - Residential", 
            "Ground Floor - Retail",
            "Basement - Parking",
            "Exterior - Facade"
        ])
    
    with col2:
        st.markdown("#### 📊 Progress Metrics")
        
        # Simulated progress data
        progress_from = 45.2
        progress_to = 67.3
        progress_change = progress_to - progress_from
        
        st.metric(
            "Progress Change",
            f"+{progress_change:.1f}%",
            f"From {progress_from}% to {progress_to}%"
        )
        
        days_diff = (comparison_date2 - comparison_date1).days
        daily_progress = progress_change / days_diff if days_diff > 0 else 0
        
        st.metric(
            "Daily Progress Rate",
            f"{daily_progress:.2f}%/day",
            "Above target" if daily_progress > 0.3 else "Below target"
        )
    
    # Photo comparison (simulated)
    st.markdown("#### 📷 Photo Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{comparison_date1.strftime('%B %d, %Y')}**")
        st.info("📸 Progress photo would be displayed here")
        st.caption(f"Progress: {progress_from}% complete")
    
    with col2:
        st.markdown(f"**{comparison_date2.strftime('%B %d, %Y')}**")
        st.info("📸 Current progress photo would be displayed here")
        st.caption(f"Progress: {progress_to}% complete")
    
    # Progress timeline
    st.markdown("#### 📈 Progress Timeline")
    
    # Generate sample progress data
    timeline_dates = pd.date_range(start=comparison_date1, end=comparison_date2, freq='W')
    timeline_progress = np.linspace(progress_from, progress_to, len(timeline_dates))
    
    fig_timeline = go.Figure()
    fig_timeline.add_trace(go.Scatter(
        x=timeline_dates, y=timeline_progress,
        mode='lines+markers',
        name='Actual Progress',
        line=dict(color='green', width=3),
        marker=dict(size=8)
    ))
    
    fig_timeline.update_layout(
        title=f'Progress Timeline - {location_filter}',
        xaxis_title='Date',
        yaxis_title='Completion %',
        height=400
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

if __name__ == "__main__":
    render_advanced_analytics()