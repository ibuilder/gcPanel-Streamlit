"""
Analytics Dashboard Visualizations for gcPanel.

This module provides interactive data visualizations for the analytics dashboard
using Plotly charts to display project performance metrics.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Utility function to generate mock data for demonstration
def get_mock_project_data():
    """
    Generate mock project data for demonstration.
    
    In a production environment, this would fetch real data from the database.
    """
    # Generate dates for last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # Generate budget data
    planned_budget = np.linspace(0, 45500000, len(dates))  # $45.5M total budget
    actual_budget = planned_budget + np.random.normal(0, 500000, len(dates))
    actual_budget = np.cumsum(np.clip(np.random.normal(0, 1000000, len(dates)), 0, None))
    actual_budget = np.minimum(actual_budget, planned_budget * 1.1)  # Max 10% over budget
    
    # Generate schedule data (% complete)
    planned_schedule = np.linspace(0, 85, len(dates))  # Project is 85% complete
    actual_schedule = planned_schedule + np.random.normal(0, 3, len(dates))
    actual_schedule = np.clip(actual_schedule, 0, 100)
    
    # Generate quality metrics
    inspections = np.random.randint(5, 20, len(dates))
    issues_found = np.random.randint(0, 10, len(dates))
    issues_resolved = np.random.binomial(issues_found, 0.7, len(dates))
    
    # Generate safety metrics
    safety_incidents = np.random.binomial(1, 0.2, len(dates))
    near_misses = np.random.randint(0, 5, len(dates))
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'planned_budget': planned_budget,
        'actual_budget': actual_budget,
        'planned_schedule': planned_schedule,
        'actual_schedule': actual_schedule,
        'inspections': inspections,
        'issues_found': issues_found,
        'issues_resolved': issues_resolved,
        'safety_incidents': safety_incidents,
        'near_misses': near_misses
    })
    
    return df

def create_project_overview_cards():
    """Create project overview metric cards."""
    data = get_mock_project_data().iloc[-1]
    
    # Calculate key metrics
    budget_variance = ((data['actual_budget'] - data['planned_budget']) / data['planned_budget']) * 100
    schedule_variance = data['actual_schedule'] - data['planned_schedule']
    quality_rate = (1 - (data['issues_found'] / data['inspections'])) * 100 if data['inspections'] > 0 else 100
    
    # Create columns for metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Budget Variance",
            value=f"{budget_variance:.1f}%",
            delta=None if abs(budget_variance) < 1 else f"{budget_variance:.1f}%"
        )
    
    with col2:
        st.metric(
            label="Schedule Progress",
            value=f"{data['actual_schedule']:.1f}%",
            delta=f"{schedule_variance:.1f}%" if schedule_variance > 0 else f"{schedule_variance:.1f}%"
        )
    
    with col3:
        st.metric(
            label="Quality Rate",
            value=f"{quality_rate:.1f}%",
            delta="On Target" if quality_rate > 90 else "Below Target"
        )
    
    with col4:
        incident_free_days = random.randint(30, 120)
        st.metric(
            label="Incident-Free Days",
            value=incident_free_days,
            delta=f"{incident_free_days} days"
        )

def create_budget_performance_chart():
    """Create budget performance chart."""
    df = get_mock_project_data()
    
    # Create figure
    fig = go.Figure()
    
    # Add traces
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['planned_budget'],
            name="Planned Budget",
            line=dict(color='blue', dash='dash')
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['actual_budget'],
            name="Actual Expenditure",
            line=dict(color='red')
        )
    )
    
    # Update layout
    fig.update_layout(
        title="Budget Performance Over Time",
        xaxis_title="Date",
        yaxis_title="Cumulative Budget ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        hovermode="x unified",
        height=500
    )
    
    # Format y-axis as currency
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    
    # Add current date line
    fig.add_vline(
        x=datetime.now(),
        line_width=2,
        line_dash="dash",
        line_color="green",
        annotation_text="Today",
        annotation_position="top right"
    )
    
    return fig

def create_schedule_performance_chart():
    """Create schedule performance chart."""
    df = get_mock_project_data()
    
    # Create figure
    fig = go.Figure()
    
    # Add traces
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['planned_schedule'],
            name="Planned Progress",
            line=dict(color='blue', dash='dash')
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['actual_schedule'],
            name="Actual Progress",
            line=dict(color='green')
        )
    )
    
    # Update layout
    fig.update_layout(
        title="Schedule Performance Over Time",
        xaxis_title="Date",
        yaxis_title="Completion (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        hovermode="x unified",
        height=500
    )
    
    # Add current date line
    fig.add_vline(
        x=datetime.now(),
        line_width=2,
        line_dash="dash",
        line_color="green",
        annotation_text="Today",
        annotation_position="top right"
    )
    
    return fig

def create_quality_metrics_chart():
    """Create quality metrics chart."""
    df = get_mock_project_data()
    
    # Create figure
    fig = go.Figure()
    
    # Add bars for issues found
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['issues_found'],
            name="Issues Found",
            marker_color='red'
        )
    )
    
    # Add bars for issues resolved
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['issues_resolved'],
            name="Issues Resolved",
            marker_color='green'
        )
    )
    
    # Add line for inspections
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['inspections'],
            name="Inspections",
            line=dict(color='blue'),
            yaxis="y2"
        )
    )
    
    # Update layout
    fig.update_layout(
        title="Quality Metrics Over Time",
        xaxis_title="Date",
        yaxis_title="Issues",
        yaxis2=dict(
            title="Inspections",
            overlaying="y",
            side="right"
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        hovermode="x unified",
        barmode='group',
        height=500
    )
    
    return fig

def create_safety_metrics_chart():
    """Create safety metrics chart."""
    df = get_mock_project_data()
    
    # Create figure
    fig = go.Figure()
    
    # Add bars for safety incidents
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['safety_incidents'],
            name="Safety Incidents",
            marker_color='red'
        )
    )
    
    # Add bars for near misses
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['near_misses'],
            name="Near Misses",
            marker_color='orange'
        )
    )
    
    # Update layout
    fig.update_layout(
        title="Safety Metrics Over Time",
        xaxis_title="Date",
        yaxis_title="Count",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        hovermode="x unified",
        barmode='stack',
        height=500
    )
    
    return fig

def create_cost_breakdown_chart():
    """Create cost breakdown chart."""
    # Generate mock cost breakdown data
    categories = ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'Overhead', 'Other']
    planned_values = [15000000, 12000000, 6000000, 8000000, 3000000, 1500000]
    actual_values = [15500000, 12800000, 5800000, 8200000, 3100000, 1600000]
    
    # Create figure
    fig = go.Figure()
    
    # Add bars for planned costs
    fig.add_trace(
        go.Bar(
            x=categories,
            y=planned_values,
            name="Planned",
            marker_color='blue'
        )
    )
    
    # Add bars for actual costs
    fig.add_trace(
        go.Bar(
            x=categories,
            y=actual_values,
            name="Actual",
            marker_color='red'
        )
    )
    
    # Update layout
    fig.update_layout(
        title="Cost Breakdown by Category",
        xaxis_title="Category",
        yaxis_title="Cost ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        hovermode="x unified",
        barmode='group',
        height=500
    )
    
    # Format y-axis as currency
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    
    return fig

def create_risk_matrix():
    """Create risk matrix visualization."""
    # Generate mock risk data
    risks = [
        {"name": "Material Delay", "impact": 4, "probability": 3},
        {"name": "Weather Event", "impact": 5, "probability": 2},
        {"name": "Labor Shortage", "impact": 3, "probability": 4},
        {"name": "Permit Issues", "impact": 4, "probability": 2},
        {"name": "Design Changes", "impact": 3, "probability": 3},
        {"name": "Subcontractor Default", "impact": 5, "probability": 1},
        {"name": "Budget Overrun", "impact": 4, "probability": 4},
        {"name": "Quality Issues", "impact": 3, "probability": 2}
    ]
    
    # Create dataframe
    df = pd.DataFrame(risks)
    
    # Calculate risk score
    df['risk_score'] = df['impact'] * df['probability']
    
    # Create bubble chart
    fig = px.scatter(
        df,
        x="probability",
        y="impact",
        size="risk_score",
        color="risk_score",
        text="name",
        size_max=30,
        color_continuous_scale=px.colors.sequential.Reds,
        range_x=[0.5, 5.5],
        range_y=[0.5, 5.5]
    )
    
    # Update layout
    fig.update_layout(
        title="Project Risk Matrix",
        xaxis_title="Probability",
        yaxis_title="Impact",
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Very Low', 'Low', 'Medium', 'High', 'Very High']
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Very Low', 'Low', 'Medium', 'High', 'Very High']
        ),
        height=600
    )
    
    # Add risk zones
    fig.add_shape(
        type="rect",
        x0=0.5, y0=0.5, x1=3.5, y1=2.5,
        line=dict(color="Green"),
        fillcolor="Green",
        opacity=0.1
    )
    
    fig.add_shape(
        type="rect",
        x0=0.5, y0=2.5, x1=2.5, y1=5.5,
        line=dict(color="Orange"),
        fillcolor="Orange",
        opacity=0.1
    )
    
    fig.add_shape(
        type="rect",
        x0=2.5, y0=3.5, x1=5.5, y1=5.5,
        line=dict(color="Red"),
        fillcolor="Red",
        opacity=0.1
    )
    
    fig.add_shape(
        type="rect",
        x0=3.5, y0=0.5, x1=5.5, y1=3.5,
        line=dict(color="Orange"),
        fillcolor="Orange",
        opacity=0.1
    )
    
    fig.add_shape(
        type="rect",
        x0=2.5, y0=2.5, x1=3.5, y1=3.5,
        line=dict(color="Orange"),
        fillcolor="Orange",
        opacity=0.1
    )
    
    # Update traces
    fig.update_traces(
        textposition='top center',
        marker=dict(line=dict(width=1, color='black')),
        mode='markers+text'
    )
    
    return fig

def render_analytics_dashboard():
    """Render the analytics dashboard with interactive visualizations."""
    st.header("Project Analytics Dashboard")
    
    # Project selector (in a real app, this would load different project data)
    st.selectbox(
        "Select Project",
        ["Highland Tower Development", "Project B", "Project C"],
        index=0
    )
    
    # Time period filter
    time_period = st.selectbox(
        "Time Period",
        ["Last Month", "Last Quarter", "Last 6 Months", "Last Year", "All Time"],
        index=3
    )
    
    # Display project overview metrics
    st.subheader("Project Overview")
    create_project_overview_cards()
    
    # Create tabs for different chart categories
    tabs = st.tabs(["Budget & Schedule", "Quality & Safety", "Risk Analysis"])
    
    # Budget & Schedule tab
    with tabs[0]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_budget_performance_chart(), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_schedule_performance_chart(), use_container_width=True)
        
        st.plotly_chart(create_cost_breakdown_chart(), use_container_width=True)
    
    # Quality & Safety tab
    with tabs[1]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_quality_metrics_chart(), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_safety_metrics_chart(), use_container_width=True)
    
    # Risk Analysis tab
    with tabs[2]:
        st.plotly_chart(create_risk_matrix(), use_container_width=True)
    
    # Interactive filters and controls
    st.sidebar.header("Dashboard Controls")
    
    st.sidebar.subheader("Data Filters")
    st.sidebar.checkbox("Show Budget Data", value=True)
    st.sidebar.checkbox("Show Schedule Data", value=True)
    st.sidebar.checkbox("Show Quality Data", value=True)
    st.sidebar.checkbox("Show Safety Data", value=True)
    
    st.sidebar.subheader("Visualization Options")
    st.sidebar.checkbox("Show Trendlines", value=False)
    st.sidebar.checkbox("Show Forecasts", value=True)
    st.sidebar.checkbox("Show Annotations", value=True)
    
    st.sidebar.button("Refresh Data")
    
    # Add export options
    st.sidebar.subheader("Export Options")
    export_format = st.sidebar.selectbox(
        "Export Format",
        ["PDF", "Excel", "CSV", "Image"]
    )
    
    st.sidebar.button("Export Dashboard", key="export_dashboard")