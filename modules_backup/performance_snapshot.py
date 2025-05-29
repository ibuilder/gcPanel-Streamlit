"""
Performance Snapshot Module for Highland Tower Development
Executive-level performance dashboard and KPI tracking
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render():
    """Render comprehensive performance snapshot dashboard"""
    
    st.title("📊 Performance Snapshot - Highland Tower Development")
    st.markdown("**Executive dashboard for $45.5M mixed-use construction project**")
    
    # Key Performance Indicators Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;">
        <h2 style="color: white; margin: 0; font-size: 1.8rem;">
            Highland Tower Development - Real-Time Performance Dashboard
        </h2>
        <p style="color: #e8f4fd; margin: 0.5rem 0 0 0;">
            120 Residential Units + 8 Retail Spaces | 15 Stories | Live Project Metrics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top-level KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="🏗️ Project Progress",
            value="67.3%",
            delta="↗️ 2.1% this week",
            help="Overall project completion percentage"
        )
    
    with col2:
        st.metric(
            label="📅 Schedule Status",
            value="5 days ahead",
            delta="↗️ Accelerated",
            help="Current schedule performance vs baseline"
        )
    
    with col3:
        st.metric(
            label="💰 Budget Status",
            value="$2.1M under",
            delta="↗️ 4.6% savings",
            help="Current cost performance vs approved budget"
        )
    
    with col4:
        st.metric(
            label="🛡️ Safety Score",
            value="98.5%",
            delta="↗️ 0.3% improved",
            help="OSHA compliance and safety performance"
        )
    
    with col5:
        st.metric(
            label="⭐ Quality Rating",
            value="4.8/5.0",
            delta="↗️ 0.2 improved",
            help="Overall quality control and inspection scores"
        )
    
    st.markdown("---")
    
    # Navigation tabs for different performance views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Executive Summary", "🏗️ Construction Metrics", "💰 Financial Performance", 
        "👥 Team Performance", "📊 Detailed Analytics"
    ])
    
    with tab1:
        render_executive_summary()
    
    with tab2:
        render_construction_metrics()
    
    with tab3:
        render_financial_performance()
    
    with tab4:
        render_team_performance()
    
    with tab5:
        render_detailed_analytics()

def render_executive_summary():
    """Executive summary dashboard"""
    st.markdown("### 📈 Executive Performance Summary")
    
    # Project timeline visualization
    st.markdown("#### 📅 Project Timeline & Milestones")
    
    # Create timeline chart
    timeline_data = {
        'Phase': ['Design', 'Permits', 'Foundation', 'Structure', 'MEP', 'Finishes', 'Closeout'],
        'Planned_Start': ['2024-01-01', '2024-03-01', '2024-05-01', '2024-08-01', '2024-11-01', '2025-02-01', '2025-05-01'],
        'Planned_End': ['2024-04-30', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-07-31'],
        'Actual_Progress': [100, 100, 100, 87, 68, 25, 0],
        'Status': ['Complete', 'Complete', 'Complete', 'Active', 'Active', 'Planned', 'Planned']
    }
    
    df_timeline = pd.DataFrame(timeline_data)
    
    fig_timeline = go.Figure()
    
    # Add planned vs actual progress bars
    for i, row in df_timeline.iterrows():
        # Planned timeline (background)
        fig_timeline.add_trace(go.Scatter(
            x=[row['Planned_Start'], row['Planned_End']],
            y=[i, i],
            mode='lines',
            line=dict(color='lightgray', width=20),
            name=f"{row['Phase']} - Planned",
            showlegend=False
        ))
        
        # Actual progress
        progress_color = 'green' if row['Status'] == 'Complete' else 'blue' if row['Status'] == 'Active' else 'orange'
        fig_timeline.add_trace(go.Scatter(
            x=[row['Planned_Start'], row['Planned_End']],
            y=[i, i],
            mode='lines',
            line=dict(color=progress_color, width=row['Actual_Progress']/5),
            name=f"{row['Phase']} - {row['Actual_Progress']}%",
            showlegend=False
        ))
    
    fig_timeline.update_layout(
        title="🏗️ Highland Tower Construction Timeline",
        yaxis=dict(tickvals=list(range(len(df_timeline))), ticktext=df_timeline['Phase']),
        height=400
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Critical success factors
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Critical Success Factors")
        
        success_factors = [
            {"factor": "Schedule Performance", "score": 95, "status": "Excellent"},
            {"factor": "Budget Control", "score": 92, "status": "Excellent"}, 
            {"factor": "Quality Standards", "score": 96, "status": "Excellent"},
            {"factor": "Safety Compliance", "score": 98, "status": "Excellent"},
            {"factor": "Stakeholder Satisfaction", "score": 88, "status": "Good"},
            {"factor": "Resource Utilization", "score": 91, "status": "Excellent"}
        ]
        
        for factor in success_factors:
            st.markdown(f"**{factor['factor']}:** {factor['score']}% - {factor['status']}")
            st.progress(factor['score'] / 100)
    
    with col2:
        st.markdown("#### 🚨 Key Risk Indicators")
        
        # Risk gauge chart
        fig_risk = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = 23,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Overall Risk Score"},
            delta = {'reference': 30, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [None, 50]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 15], 'color': "lightgreen"},
                    {'range': [15, 30], 'color': "yellow"},
                    {'range': [30, 50], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 35
                }
            }
        ))
        
        fig_risk.update_layout(height=300)
        st.plotly_chart(fig_risk, use_container_width=True)
    
    # Weekly highlights
    st.markdown("#### 📝 This Week's Highlights")
    
    highlights = [
        "✅ Level 13 structural steel installation completed ahead of schedule",
        "✅ MEP rough-in Level 12 passed inspection with zero deficiencies", 
        "✅ South facade curtain wall installation 70% complete",
        "⚠️ Minor electrical conduit spacing issue resolved in Level 12",
        "📈 Overall project efficiency improved to 94.2% this week"
    ]
    
    for highlight in highlights:
        st.markdown(highlight)

def render_construction_metrics():
    """Construction-specific performance metrics"""
    st.markdown("### 🏗️ Construction Performance Metrics")
    
    # Construction KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Productivity Rate", "94.2%", "↗️ +2.1%")
    
    with col2:
        st.metric("Work Hours/Week", "3,560 hrs", "↗️ +120 hrs")
    
    with col3:
        st.metric("Equipment Utilization", "87.5%", "↗️ +3.2%")
    
    with col4:
        st.metric("Inspection Pass Rate", "96.8%", "↗️ +1.5%")
    
    # Progress by building system
    st.markdown("#### 🏗️ Progress by Building System")
    
    systems_data = {
        'System': ['Foundation', 'Structural Steel', 'MEP Rough-in', 'Exterior Envelope', 'Interior Finishes'],
        'Planned': [100, 90, 75, 60, 30],
        'Actual': [100, 87, 78, 65, 25],
        'Variance': [0, -3, +3, +5, -5]
    }
    
    df_systems = pd.DataFrame(systems_data)
    
    fig_systems = go.Figure()
    
    fig_systems.add_trace(go.Bar(
        name='Planned',
        x=df_systems['System'],
        y=df_systems['Planned'],
        marker_color='lightblue'
    ))
    
    fig_systems.add_trace(go.Bar(
        name='Actual',
        x=df_systems['System'],
        y=df_systems['Actual'],
        marker_color='darkblue'
    ))
    
    fig_systems.update_layout(
        title="📊 Construction Progress by System",
        barmode='group',
        yaxis_title="Completion %"
    )
    
    st.plotly_chart(fig_systems, use_container_width=True)
    
    # Quality metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔍 Quality Control Metrics")
        
        quality_data = {
            'Inspection Type': ['Structural', 'MEP', 'Envelope', 'Fire Safety', 'Finishes'],
            'Inspections': [24, 18, 12, 8, 6],
            'Pass Rate': [100, 89, 100, 100, 83]
        }
        
        df_quality = pd.DataFrame(quality_data)
        
        fig_quality = px.bar(
            df_quality,
            x='Inspection Type',
            y='Pass Rate',
            title="🔍 Inspection Pass Rates by Type",
            color='Pass Rate',
            color_continuous_scale='RdYlGn'
        )
        
        st.plotly_chart(fig_quality, use_container_width=True)
    
    with col2:
        st.markdown("#### 🛡️ Safety Performance")
        
        safety_metrics = [
            {"metric": "Days Without Incident", "value": "147", "trend": "↗️"},
            {"metric": "Safety Training Hours", "value": "1,240", "trend": "↗️"},
            {"metric": "PPE Compliance", "value": "99.2%", "trend": "→"},
            {"metric": "Safety Inspections", "value": "52", "trend": "↗️"}
        ]
        
        for metric in safety_metrics:
            st.markdown(f"**{metric['metric']}:** {metric['value']} {metric['trend']}")

def render_financial_performance():
    """Financial performance dashboard"""
    st.markdown("### 💰 Financial Performance Dashboard")
    
    # Financial KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Budget", "$45.5M", "Approved")
    
    with col2:
        st.metric("Spent to Date", "$30.7M", "67.5% of budget")
    
    with col3:
        st.metric("Budget Variance", "-$2.1M", "↗️ 4.6% under")
    
    with col4:
        st.metric("Forecasted Total", "$43.4M", "↗️ $2.1M savings")
    
    # Cost breakdown
    st.markdown("#### 💰 Cost Breakdown by Category")
    
    cost_data = {
        'Category': ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'Overhead'],
        'Budgeted': [18.2, 15.4, 4.8, 5.6, 1.5],
        'Actual': [17.8, 14.9, 4.2, 5.4, 1.4],
        'Variance': [-0.4, -0.5, -0.6, -0.2, -0.1]
    }
    
    df_costs = pd.DataFrame(cost_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_budget = px.pie(
            df_costs,
            values='Budgeted',
            names='Category',
            title="💰 Original Budget Allocation ($M)"
        )
        st.plotly_chart(fig_budget, use_container_width=True)
    
    with col2:
        fig_actual = px.pie(
            df_costs,
            values='Actual',
            names='Category', 
            title="💸 Actual Spending to Date ($M)"
        )
        st.plotly_chart(fig_actual, use_container_width=True)
    
    # Cash flow projection
    st.markdown("#### 📈 Cash Flow Projection")
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    planned_cash = [2.1, 3.8, 4.2, 4.8, 5.1, 4.9, 4.6, 4.2, 3.8, 3.4, 2.9, 2.0]
    actual_cash = [1.9, 3.6, 3.9, 4.5, 4.8, None, None, None, None, None, None, None]
    
    fig_cashflow = go.Figure()
    
    fig_cashflow.add_trace(go.Scatter(
        x=months,
        y=planned_cash,
        mode='lines+markers',
        name='Planned Cash Flow',
        line=dict(color='blue', dash='dash')
    ))
    
    fig_cashflow.add_trace(go.Scatter(
        x=months[:5],
        y=actual_cash[:5],
        mode='lines+markers', 
        name='Actual Cash Flow',
        line=dict(color='green')
    ))
    
    fig_cashflow.update_layout(
        title="💰 Monthly Cash Flow - Highland Tower ($M)",
        yaxis_title="Cash Flow ($M)",
        xaxis_title="Month (2025)"
    )
    
    st.plotly_chart(fig_cashflow, use_container_width=True)

def render_team_performance():
    """Team and resource performance metrics"""
    st.markdown("### 👥 Team Performance Dashboard")
    
    # Team metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Team Size", "89", "Active workers")
    
    with col2:
        st.metric("Productivity Index", "94.2%", "↗️ +2.1%")
    
    with col3:
        st.metric("Training Hours", "1,240", "This month")
    
    with col4:
        st.metric("Retention Rate", "96.8%", "↗️ Excellent")
    
    # Subcontractor performance
    st.markdown("#### 🏗️ Subcontractor Performance Summary")
    
    subcontractor_data = {
        'Subcontractor': ['Apex Steel', 'Premier MEP', 'Elite Glass', 'Precision Concrete', 'Highland Interior'],
        'Performance': [4.8, 4.6, 4.9, 4.9, 4.7],
        'Safety': [4.9, 4.8, 4.7, 4.8, 4.6],
        'Schedule': [95, 92, 98, 99, 85],
        'Status': ['Active', 'Active', 'Active', 'Complete', 'Starting Soon']
    }
    
    df_subs = pd.DataFrame(subcontractor_data)
    
    fig_subs = go.Figure()
    
    fig_subs.add_trace(go.Scatter(
        x=df_subs['Performance'],
        y=df_subs['Safety'],
        mode='markers+text',
        text=df_subs['Subcontractor'],
        textposition="top center",
        marker=dict(
            size=df_subs['Schedule'],
            sizemode='diameter',
            sizeref=2,
            color=df_subs['Schedule'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Schedule Compliance %")
        )
    ))
    
    fig_subs.update_layout(
        title="👥 Subcontractor Performance Matrix",
        xaxis_title="Performance Rating (1-5)",
        yaxis_title="Safety Rating (1-5)",
        height=500
    )
    
    st.plotly_chart(fig_subs, use_container_width=True)
    
    # Workforce distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👷 Workforce by Trade")
        
        workforce_data = {
            'Trade': ['Steel Workers', 'MEP Technicians', 'Glaziers', 'Concrete Crew', 'General Labor'],
            'Count': [18, 24, 12, 16, 19]
        }
        
        fig_workforce = px.bar(
            workforce_data,
            x='Trade',
            y='Count',
            title="👷 Current Workforce Distribution"
        )
        
        st.plotly_chart(fig_workforce, use_container_width=True)
    
    with col2:
        st.markdown("#### 📚 Training & Certifications")
        
        training_stats = [
            {"program": "OSHA 30-Hour", "completion": "100%", "status": "✅"},
            {"program": "Fall Protection", "completion": "98%", "status": "✅"},
            {"program": "Crane Safety", "completion": "95%", "status": "✅"},
            {"program": "Confined Space", "completion": "92%", "status": "✅"},
            {"program": "First Aid/CPR", "completion": "89%", "status": "⚠️"}
        ]
        
        for program in training_stats:
            st.markdown(f"**{program['program']}:** {program['completion']} {program['status']}")

def render_detailed_analytics():
    """Detailed analytics and trends"""
    st.markdown("### 📊 Detailed Performance Analytics")
    
    # Performance trends over time
    st.markdown("#### 📈 Performance Trends (Last 12 Weeks)")
    
    weeks = list(range(1, 13))
    schedule_performance = [88, 89, 91, 92, 90, 93, 94, 92, 95, 96, 97, 95]
    budget_performance = [92, 91, 93, 94, 92, 95, 96, 94, 96, 97, 95, 92] 
    quality_performance = [94, 95, 93, 96, 97, 95, 98, 96, 97, 98, 96, 98]
    safety_performance = [96, 97, 98, 97, 98, 99, 98, 97, 99, 98, 99, 98]
    
    fig_trends = go.Figure()
    
    fig_trends.add_trace(go.Scatter(
        x=weeks, y=schedule_performance,
        mode='lines+markers', name='Schedule Performance',
        line=dict(color='blue')
    ))
    
    fig_trends.add_trace(go.Scatter(
        x=weeks, y=budget_performance,
        mode='lines+markers', name='Budget Performance',
        line=dict(color='green')
    ))
    
    fig_trends.add_trace(go.Scatter(
        x=weeks, y=quality_performance,
        mode='lines+markers', name='Quality Performance',
        line=dict(color='purple')
    ))
    
    fig_trends.add_trace(go.Scatter(
        x=weeks, y=safety_performance,
        mode='lines+markers', name='Safety Performance',
        line=dict(color='orange')
    ))
    
    fig_trends.update_layout(
        title="📈 Highland Tower Performance Trends",
        xaxis_title="Week",
        yaxis_title="Performance Score (%)",
        yaxis=dict(range=[80, 100])
    )
    
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # Predictive analytics
    st.markdown("#### 🔮 Predictive Analytics & Forecasting")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📅 Schedule Forecast:**")
        st.success("✅ On track for completion 5 days ahead of schedule")
        st.markdown("**💰 Budget Forecast:**")
        st.success("✅ Projected to finish $2.1M under budget") 
        st.markdown("**🎯 Quality Forecast:**")
        st.success("✅ Maintaining 4.8/5.0 quality rating")
    
    with col2:
        st.markdown("**⚠️ Risk Indicators:**")
        st.warning("⚠️ MEP coordination may need additional resources")
        st.info("ℹ️ Winter weather preparations recommended")
        st.success("✅ All other metrics within acceptable ranges")
    
    # Performance benchmarking
    st.markdown("#### 🏆 Industry Benchmarking")
    
    benchmark_data = {
        'Metric': ['Schedule Performance', 'Budget Control', 'Safety Score', 'Quality Rating'],
        'Highland Tower': [95, 92, 98.5, 4.8],
        'Industry Average': [85, 88, 94.2, 4.2],
        'Best in Class': [98, 95, 99.1, 4.9]
    }
    
    df_benchmark = pd.DataFrame(benchmark_data)
    
    fig_benchmark = go.Figure()
    
    fig_benchmark.add_trace(go.Bar(
        name='Highland Tower',
        x=df_benchmark['Metric'],
        y=df_benchmark['Highland Tower'],
        marker_color='darkblue'
    ))
    
    fig_benchmark.add_trace(go.Bar(
        name='Industry Average',
        x=df_benchmark['Metric'],
        y=df_benchmark['Industry Average'],
        marker_color='gray'
    ))
    
    fig_benchmark.add_trace(go.Bar(
        name='Best in Class',
        x=df_benchmark['Metric'],
        y=df_benchmark['Best in Class'],
        marker_color='gold'
    ))
    
    fig_benchmark.update_layout(
        title="🏆 Highland Tower vs Industry Benchmarks",
        barmode='group',
        yaxis_title="Performance Score"
    )
    
    st.plotly_chart(fig_benchmark, use_container_width=True)

if __name__ == "__main__":
    render()