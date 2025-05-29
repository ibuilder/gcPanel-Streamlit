"""
Highland Tower Development - Chart Functionality Fix
Fixes plotting issues in the Highland Tower platform
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

def create_safe_chart(chart_type, data, **kwargs):
    """Safely create charts with error handling"""
    try:
        if chart_type == "line":
            fig = px.line(data, **kwargs)
        elif chart_type == "bar":
            fig = px.bar(data, **kwargs)
        elif chart_type == "scatter":
            fig = px.scatter(data, **kwargs)
        elif chart_type == "pie":
            fig = px.pie(data, **kwargs)
        else:
            # Fallback to simple bar chart
            fig = px.bar(data, x=data.columns[0], y=data.columns[1] if len(data.columns) > 1 else data.columns[0])
        
        # Apply Highland Tower styling
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", size=12),
            title_font_size=16,
            showlegend=True
        )
        
        return fig
    
    except Exception as e:
        st.error(f"Chart creation error: {e}")
        return None

def render_highland_tower_metrics():
    """Render Highland Tower project metrics with working charts"""
    
    # Highland Tower progress data
    progress_data = pd.DataFrame({
        'Phase': ['Foundation', 'Structure', 'MEP', 'Finishes', 'Closeout'],
        'Planned': [100, 100, 85, 60, 20],
        'Actual': [100, 95, 78, 45, 5],
        'Budget': [5.2, 18.5, 12.3, 8.7, 0.8]  # millions
    })
    
    # Cost tracking data
    cost_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'Budgeted': [3.2, 6.8, 12.5, 18.9, 25.4],
        'Actual': [3.1, 6.9, 12.8, 19.2, 26.1],
        'Forecast': [3.1, 6.9, 12.8, 19.2, 26.1]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Project Progress by Phase")
        chart = create_safe_chart(
            "bar", 
            progress_data,
            x='Phase',
            y=['Planned', 'Actual'],
            title="Highland Tower Progress (%)",
            barmode='group'
        )
        if chart:
            st.plotly_chart(chart, use_container_width=True)
    
    with col2:
        st.subheader("Cost Performance")
        chart = create_safe_chart(
            "line",
            cost_data,
            x='Month',
            y=['Budgeted', 'Actual', 'Forecast'],
            title="Highland Tower Cost Tracking ($M)"
        )
        if chart:
            st.plotly_chart(chart, use_container_width=True)

def render_rfi_analytics():
    """Render RFI analytics with working charts"""
    
    # RFI status data
    rfi_status = pd.DataFrame({
        'Status': ['Open', 'In Review', 'Closed', 'Overdue'],
        'Count': [5, 8, 78, 2],
        'Color': ['#ef4444', '#f59e0b', '#10b981', '#8b5cf6']
    })
    
    # RFI trend data
    rfi_trend = pd.DataFrame({
        'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'Created': [12, 8, 15, 6],
        'Resolved': [10, 12, 11, 9]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("RFI Status Distribution")
        chart = create_safe_chart(
            "pie",
            rfi_status,
            values='Count',
            names='Status',
            title="Current RFI Status"
        )
        if chart:
            st.plotly_chart(chart, use_container_width=True)
    
    with col2:
        st.subheader("RFI Trend Analysis")
        chart = create_safe_chart(
            "line",
            rfi_trend,
            x='Week',
            y=['Created', 'Resolved'],
            title="RFI Creation vs Resolution"
        )
        if chart:
            st.plotly_chart(chart, use_container_width=True)

def render_safety_dashboard():
    """Render safety metrics with working charts"""
    
    # Safety metrics
    safety_data = pd.DataFrame({
        'Metric': ['Near Misses', 'Safety Training', 'Inspections', 'Incidents'],
        'This Month': [12, 45, 23, 0],
        'Last Month': [8, 42, 20, 1]
    })
    
    # Safety score trend
    safety_trend = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=5, freq='M'),
        'Safety Score': [95.2, 96.8, 98.1, 97.5, 98.2]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Safety Metrics Comparison")
        chart = create_safe_chart(
            "bar",
            safety_data,
            x='Metric',
            y=['This Month', 'Last Month'],
            title="Safety Performance Comparison",
            barmode='group'
        )
        if chart:
            st.plotly_chart(chart, use_container_width=True)
    
    with col2:
        st.subheader("Safety Score Trend")
        chart = create_safe_chart(
            "line",
            safety_trend,
            x='Date',
            y='Safety Score',
            title="Highland Tower Safety Performance"
        )
        if chart:
            st.plotly_chart(chart, use_container_width=True)

def render_cost_analytics():
    """Render cost management analytics"""
    
    # Budget vs actual by category
    cost_breakdown = pd.DataFrame({
        'Category': ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'Other'],
        'Budget': [12.5, 18.2, 4.8, 8.9, 1.1],
        'Actual': [12.8, 17.9, 5.1, 8.7, 1.2],
        'Variance': [0.3, -0.3, 0.3, -0.2, 0.1]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Budget vs Actual by Category")
        chart = create_safe_chart(
            "bar",
            cost_breakdown,
            x='Category',
            y=['Budget', 'Actual'],
            title="Cost Performance by Category ($M)",
            barmode='group'
        )
        if chart:
            st.plotly_chart(chart, use_container_width=True)
    
    with col2:
        st.subheader("Cost Variance Analysis")
        chart = create_safe_chart(
            "bar",
            cost_breakdown,
            x='Category',
            y='Variance',
            title="Budget Variance by Category ($M)",
            color='Variance',
            color_continuous_scale=['red', 'white', 'green']
        )
        if chart:
            st.plotly_chart(chart, use_container_width=True)

def test_chart_functionality():
    """Test if charts are working properly"""
    st.subheader("Chart Functionality Test")
    
    try:
        # Simple test chart
        test_data = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 3, 5, 6]
        })
        
        fig = px.line(test_data, x='x', y='y', title="Chart Test - If you see this, charts are working")
        st.plotly_chart(fig, use_container_width=True)
        st.success("Charts are working correctly!")
        
    except Exception as e:
        st.error(f"Chart error: {e}")
        st.info("Charts may need configuration or dependency updates")