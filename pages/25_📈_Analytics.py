"""
Analytics Dashboard Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from lib.utils.helpers import check_authentication, initialize_session_state

st.set_page_config(page_title="Analytics - gcPanel", page_icon="📈", layout="wide")
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("📈 Project Analytics")
st.markdown("Highland Tower Development - Performance Analytics & Insights")
st.markdown("---")

# Key Performance Indicators
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Project Progress", "78.5%", "2.3%")

with col2:
    st.metric("Schedule Performance Index", "1.05", "0.02")

with col3:
    st.metric("Cost Performance Index", "0.98", "-0.01")

with col4:
    st.metric("Quality Score", "96%", "1%")

st.markdown("---")

# Charts and Analytics
tab1, tab2, tab3, tab4 = st.tabs(["📊 Project Overview", "💰 Cost Analytics", "📅 Schedule Analytics", "🎯 Performance Metrics"])

with tab1:
    st.subheader("📊 Project Overview Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Progress by Phase
        progress_data = pd.DataFrame({
            'Phase': ['Foundation', 'Structure', 'MEP', 'Finishes', 'Landscaping'],
            'Progress': [98, 85, 65, 25, 5],
            'Target': [100, 90, 70, 30, 10]
        })
        
        fig = px.bar(progress_data, x='Phase', y=['Progress', 'Target'],
                    title="Progress vs Target by Phase", barmode='group',
                    color_discrete_map={'Progress': '#2E86AB', 'Target': '#A23B72'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Resource Allocation
        resource_data = pd.DataFrame({
            'Resource Type': ['Labor', 'Materials', 'Equipment', 'Overhead'],
            'Allocated': [35, 40, 15, 10]
        })
        
        fig = px.pie(resource_data, values='Allocated', names='Resource Type',
                    title="Resource Allocation Distribution")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("💰 Cost Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost Trend Analysis
        cost_trend_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            'Budgeted': [2000000, 4200000, 6800000, 9500000, 12800000, 16200000, 20100000, 24300000, 28800000, 33500000, 38400000, 43500000],
            'Actual': [1950000, 4150000, 6750000, 9400000, 12650000, 16000000, 19850000, 24100000, 28500000, 33200000, 38000000, 43200000]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=cost_trend_data['Month'], y=cost_trend_data['Budgeted'],
                                mode='lines+markers', name='Budgeted', line=dict(color='#2E86AB')))
        fig.add_trace(go.Scatter(x=cost_trend_data['Month'], y=cost_trend_data['Actual'],
                                mode='lines+markers', name='Actual', line=dict(color='#A23B72')))
        fig.update_layout(title="Budget vs Actual Cost Trend", xaxis_title="Month", yaxis_title="Cost ($)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cost Variance by Category
        variance_data = pd.DataFrame({
            'Category': ['Labor', 'Materials', 'Equipment', 'Subcontractors'],
            'Variance': [-150000, 85000, -25000, 45000]
        })
        
        colors = ['red' if x < 0 else 'green' for x in variance_data['Variance']]
        fig = px.bar(variance_data, x='Category', y='Variance',
                    title="Cost Variance by Category", color=colors)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("📅 Schedule Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Schedule Performance Index Trend
        spi_data = pd.DataFrame({
            'Week': list(range(1, 13)),
            'SPI': [1.02, 1.01, 0.98, 1.05, 1.08, 1.06, 1.04, 1.07, 1.05, 1.03, 1.05, 1.05]
        })
        
        fig = px.line(spi_data, x='Week', y='SPI',
                     title="Schedule Performance Index Trend",
                     markers=True)
        fig.add_hline(y=1.0, line_dash="dash", line_color="red", 
                     annotation_text="Target SPI = 1.0")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Critical Path Activities
        critical_activities = pd.DataFrame({
            'Activity': ['Foundation Pour', 'Steel Erection', 'MEP Rough-in', 'Drywall', 'Final Inspection'],
            'Days Behind/Ahead': [2, -1, 0, 3, -2],
            'Impact': ['Low', 'Medium', 'High', 'Medium', 'Low']
        })
        
        colors = ['red' if x > 0 else 'green' if x < 0 else 'yellow' for x in critical_activities['Days Behind/Ahead']]
        fig = px.bar(critical_activities, x='Activity', y='Days Behind/Ahead',
                    title="Critical Path Activities Status", color=colors)
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("🎯 Performance Metrics Dashboard")
    
    # Performance scorecard
    performance_metrics = {
        'Safety': {'Score': 98, 'Target': 95, 'Trend': 'up'},
        'Quality': {'Score': 96, 'Target': 95, 'Trend': 'up'},
        'Schedule': {'Score': 105, 'Target': 100, 'Trend': 'up'},
        'Cost': {'Score': 98, 'Target': 100, 'Trend': 'down'},
        'Client Satisfaction': {'Score': 94, 'Target': 90, 'Trend': 'up'}
    }
    
    cols = st.columns(len(performance_metrics))
    for i, (metric, data) in enumerate(performance_metrics.items()):
        with cols[i]:
            delta = data['Score'] - data['Target']
            delta_str = f"+{delta}" if delta > 0 else str(delta)
            st.metric(metric, f"{data['Score']}%", delta_str)
    
    # Detailed performance chart
    perf_df = pd.DataFrame.from_dict(performance_metrics, orient='index').reset_index()
    perf_df.columns = ['Metric', 'Score', 'Target', 'Trend']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=perf_df['Metric'], y=perf_df['Score'],
                            mode='markers+lines', name='Actual Score',
                            marker=dict(size=10, color='#2E86AB')))
    fig.add_trace(go.Scatter(x=perf_df['Metric'], y=perf_df['Target'],
                            mode='markers+lines', name='Target',
                            marker=dict(size=8, color='#A23B72'), line=dict(dash='dash')))
    fig.update_layout(title="Performance Metrics vs Targets", 
                     xaxis_title="Metrics", yaxis_title="Score (%)")
    st.plotly_chart(fig, use_container_width=True)