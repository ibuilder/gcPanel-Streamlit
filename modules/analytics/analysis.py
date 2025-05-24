"""
Analysis Module for gcPanel Analytics

This module provides chart-based analysis features for the analytics dashboard,
consolidating visualization functionality from across the application.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
import os

def render_project_performance_charts():
    """Render charts related to overall project performance."""
    st.subheader("Project Performance Analysis")
    
    # Create container with white background
    st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
    
    # Project timeline
    st.markdown("### Project Timeline & Progress")
    
    # Generate sample project timeline data
    today = datetime.now()
    project_start = today - timedelta(days=120)
    project_end = today + timedelta(days=240)
    total_duration = (project_end - project_start).days
    elapsed_days = (today - project_start).days
    progress_percent = (elapsed_days / total_duration) * 100
    
    # Create timeline milestones
    milestones = [
        {"name": "Project Start", "date": project_start, "complete": True},
        {"name": "Design Development", "date": project_start + timedelta(days=30), "complete": True},
        {"name": "Construction Documents", "date": project_start + timedelta(days=60), "complete": True},
        {"name": "Foundation Complete", "date": project_start + timedelta(days=90), "complete": True},
        {"name": "Structure to Level 5", "date": today - timedelta(days=10), "complete": True},
        {"name": "Structure Complete", "date": today + timedelta(days=30), "complete": False},
        {"name": "Building Envelope", "date": today + timedelta(days=90), "complete": False},
        {"name": "Interior Finishes", "date": today + timedelta(days=150), "complete": False},
        {"name": "Substantial Completion", "date": today + timedelta(days=210), "complete": False},
        {"name": "Final Completion", "date": project_end, "complete": False}
    ]
    
    # Create dataframe for timeline
    df_milestones = pd.DataFrame(milestones)
    df_milestones['days_from_start'] = df_milestones['date'].apply(lambda x: (x - project_start).days)
    df_milestones['percent_of_project'] = df_milestones['days_from_start'] / total_duration * 100
    
    # Create the timeline chart
    fig = px.timeline(
        df_milestones, 
        x_start='days_from_start', 
        x_end=[x+10 for x in df_milestones['days_from_start']], 
        y='name',
        color='complete',
        labels={"name": "Milestone", "complete": "Completed"},
        color_discrete_map={True: "green", False: "blue"}
    )
    
    # Add vertical line for today
    fig.add_vline(x=elapsed_days, line_width=2, line_dash="dash", line_color="red")
    fig.add_annotation(x=elapsed_days, y=10, text="Today", showarrow=False, yshift=10)
    
    # Update layout
    fig.update_layout(
        xaxis_title="Days from Project Start",
        yaxis_title="",
        height=400,
        xaxis=dict(
            tickvals=[0, 60, 120, 180, 240, 300, 360],
            ticktext=[
                project_start.strftime('%b %Y'),
                (project_start + timedelta(days=60)).strftime('%b %Y'),
                (project_start + timedelta(days=120)).strftime('%b %Y'),
                (project_start + timedelta(days=180)).strftime('%b %Y'),
                (project_start + timedelta(days=240)).strftime('%b %Y'),
                (project_start + timedelta(days=300)).strftime('%b %Y'),
                (project_start + timedelta(days=360)).strftime('%b %Y')
            ]
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show progress metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Project Progress", f"{progress_percent:.1f}%")
    with col2:
        st.metric("Days Elapsed", f"{elapsed_days} days", f"{elapsed_days/total_duration*100:.1f}% of schedule")
    with col3:
        st.metric("Remaining", f"{total_duration - elapsed_days} days")
    with col4:
        try:
            future_milestones = [m for m in milestones if m.get('days_from_start', 0) > elapsed_days]
            if future_milestones:
                days_to_next_milestone = min([m['days_from_start'] - elapsed_days for m in future_milestones])
                next_milestone = next((m['name'] for m in future_milestones if m['days_from_start'] - elapsed_days == days_to_next_milestone), "None")
                st.metric("Next Milestone", next_milestone, f"in {days_to_next_milestone} days")
            else:
                st.metric("Next Milestone", "Project Complete", "0 days")
        except (KeyError, ValueError):
            st.metric("Next Milestone", "Foundation Pour", "in 14 days")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Project Budget Analysis
    st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
    st.markdown("### Budget Analysis")
    
    # Generate budget data
    budget_data = {
        "Division": [
            "Division 01 - General Requirements",
            "Division 02 - Site Construction",
            "Division 03 - Concrete",
            "Division 04 - Masonry",
            "Division 05 - Metals",
            "Division 06 - Wood & Plastics",
            "Division 07 - Thermal & Moisture",
            "Division 08 - Doors & Windows",
            "Division 09 - Finishes",
            "Division 10 - Specialties",
            "Division 11 - Equipment",
            "Division 12 - Furnishings",
            "Division 13 - Special Construction",
            "Division 14 - Conveying Systems",
            "Division 21-23 - Mechanical",
            "Division 26-28 - Electrical",
        ],
        "Budget": [
            3185000, 3640000, 6825000, 4095000, 5460000, 2275000, 3640000, 2730000,
            3185000, 1365000, 1820000, 1365000, 2275000, 1820000, 6825000, 5460000
        ]
    }
    
    # Calculate actual costs (some over, some under budget)
    actuals = []
    for budget in budget_data["Budget"]:
        variance_factor = random.uniform(0.85, 1.15)  # 15% under to 15% over
        actuals.append(budget * variance_factor)
    
    budget_data["Actual"] = actuals
    budget_data["Variance"] = [a - b for a, b in zip(budget_data["Budget"], budget_data["Actual"])]
    budget_data["Variance_Percent"] = [v / b * 100 for v, b in zip(budget_data["Variance"], budget_data["Budget"])]
    
    df_budget = pd.DataFrame(budget_data)
    
    # Create budget vs actual bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_budget["Division"],
        y=df_budget["Budget"],
        name="Budget",
        marker_color='blue'
    ))
    
    fig.add_trace(go.Bar(
        x=df_budget["Division"],
        y=df_budget["Actual"],
        name="Actual",
        marker_color='red'
    ))
    
    fig.update_layout(
        barmode='group',
        xaxis_tickangle=-45,
        height=500,
        xaxis_title="Division",
        yaxis_title="Amount ($)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Budget summary metrics
    total_budget = sum(budget_data["Budget"])
    total_actual = sum(budget_data["Actual"])
    total_variance = total_budget - total_actual
    variance_percent = total_variance / total_budget * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Budget", f"${total_budget:,.2f}")
    with col2:
        st.metric("Total Actual", f"${total_actual:,.2f}")
    with col3:
        st.metric("Variance", f"${total_variance:,.2f}", f"{variance_percent:.1f}%", 
                  delta_color="normal" if total_variance >= 0 else "inverse")
    
    # Create table of divisions with largest variances
    st.markdown("#### Divisions with Largest Variances")
    
    # Sort by absolute variance percent
    df_sorted = df_budget.copy()
    df_sorted["Abs_Variance_Percent"] = df_sorted["Variance_Percent"].abs()
    df_sorted = df_sorted.sort_values("Abs_Variance_Percent", ascending=False).head(5)
    
    # Format the table for display
    df_display = df_sorted[["Division", "Budget", "Actual", "Variance", "Variance_Percent"]].copy()
    df_display["Budget"] = df_display["Budget"].apply(lambda x: f"${x:,.2f}")
    df_display["Actual"] = df_display["Actual"].apply(lambda x: f"${x:,.2f}")
    
    # Format variance with colors
    def format_variance(row):
        variance = row["Variance"]
        variance_pct = row["Variance_Percent"]
        color = "green" if variance >= 0 else "red"
        return f"<span style='color:{color}'>${abs(variance):,.2f} ({variance_pct:.1f}%)</span>"
    
    df_display["Variance"] = df_sorted.apply(format_variance, axis=1)
    df_display = df_display.rename(columns={"Variance_Percent": "% Variance"})
    df_display = df_display.drop(columns=["% Variance"])
    
    # Display the table
    st.markdown(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_safety_analysis():
    """Render charts for safety performance analysis."""
    st.subheader("Safety Performance Analysis")
    
    # Create container with white background
    st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
    
    # Generate sample safety data
    today = datetime.now()
    start_date = today - timedelta(days=180)
    
    # Create date range
    date_range = [start_date + timedelta(days=x) for x in range(180)]
    months = [d.strftime('%b %Y') for d in date_range if d.day == 1]
    month_positions = [i for i, d in enumerate(date_range) if d.day == 1]
    
    # Generate safety incidents
    np.random.seed(42)  # For reproducible results
    incident_dates = sorted(np.random.choice(range(180), size=15, replace=False))
    incidents = []
    
    incident_types = ["Near Miss", "First Aid", "Medical Treatment", "Lost Time", "Property Damage"]
    severity = ["Low", "Medium", "High"]
    
    for i, day in enumerate(incident_dates):
        incident_date = start_date + timedelta(days=day)
        incident_type = np.random.choice(incident_types, p=[0.4, 0.3, 0.15, 0.05, 0.1])
        incident_severity = np.random.choice(severity, p=[0.6, 0.3, 0.1])
        
        incidents.append({
            "date": incident_date,
            "day_number": day,
            "type": incident_type,
            "severity": incident_severity,
            "description": f"Safety incident #{i+1}"
        })
    
    # Calculate safety metrics
    total_work_days = 180
    total_incidents = len(incidents)
    incident_rate = (total_incidents / total_work_days) * 100
    
    # Create metrics by month
    monthly_data = {}
    for incident in incidents:
        month_key = incident["date"].strftime('%b %Y')
        if month_key not in monthly_data:
            monthly_data[month_key] = {"total": 0, "types": {}}
        
        monthly_data[month_key]["total"] += 1
        
        if incident["type"] not in monthly_data[month_key]["types"]:
            monthly_data[month_key]["types"][incident["type"]] = 0
        
        monthly_data[month_key]["types"][incident["type"]] += 1
    
    # Prepare data for charts
    months_list = sorted(monthly_data.keys(), key=lambda x: datetime.strptime(x, '%b %Y'))
    
    incidents_by_month = [monthly_data.get(month, {"total": 0})["total"] for month in months_list]
    
    # Create incident trend chart
    fig = px.bar(
        x=months_list,
        y=incidents_by_month,
        labels={"x": "Month", "y": "Number of Incidents"},
        title="Safety Incidents by Month"
    )
    
    # Add target line
    fig.add_trace(go.Scatter(
        x=months_list,
        y=[2] * len(months_list),  # Target of 2 incidents per month
        mode='lines',
        name='Target',
        line=dict(color='red', dash='dash')
    ))
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Incidents by type
    incident_types_count = {}
    for incident in incidents:
        if incident["type"] not in incident_types_count:
            incident_types_count[incident["type"]] = 0
        incident_types_count[incident["type"]] += 1
    
    fig = px.pie(
        values=list(incident_types_count.values()),
        names=list(incident_types_count.keys()),
        title="Incidents by Type"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Incidents by severity
        severity_count = {}
        for incident in incidents:
            if incident["severity"] not in severity_count:
                severity_count[incident["severity"]] = 0
            severity_count[incident["severity"]] += 1
        
        fig = px.pie(
            values=list(severity_count.values()),
            names=list(severity_count.keys()),
            title="Incidents by Severity",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Safety metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Incidents", total_incidents)
    
    with col2:
        st.metric("Incident Rate", f"{incident_rate:.2f}%")
    
    with col3:
        lost_time_incidents = sum(1 for incident in incidents if incident["type"] == "Lost Time")
        st.metric("Lost Time Incidents", lost_time_incidents)
    
    with col4:
        near_misses = sum(1 for incident in incidents if incident["type"] == "Near Miss")
        st.metric("Near Misses", near_misses)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_quality_analysis():
    """Render charts for quality analysis."""
    st.subheader("Quality Analysis")
    
    # Create container with white background
    st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
    
    # Generate sample quality data
    today = datetime.now()
    
    # Quality issues by trade
    trades = [
        "Concrete", "Steel", "Framing", "Drywall", "Electrical", 
        "Plumbing", "HVAC", "Finishes", "Roofing", "Waterproofing"
    ]
    
    issue_counts = [random.randint(1, 15) for _ in trades]
    resolved_counts = [int(count * random.uniform(0.3, 0.9)) for count in issue_counts]
    
    # Create DataFrame
    df_quality = pd.DataFrame({
        "Trade": trades,
        "Total Issues": issue_counts,
        "Resolved Issues": resolved_counts,
        "Open Issues": [t - r for t, r in zip(issue_counts, resolved_counts)]
    })
    
    # Calculate total issues and resolution rate
    total_issues = sum(issue_counts)
    total_resolved = sum(resolved_counts)
    resolution_rate = (total_resolved / total_issues) * 100 if total_issues > 0 else 0
    
    # Quality issues by trade chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_quality["Trade"],
        y=df_quality["Resolved Issues"],
        name="Resolved Issues",
        marker_color='green'
    ))
    
    fig.add_trace(go.Bar(
        x=df_quality["Trade"],
        y=df_quality["Open Issues"],
        name="Open Issues",
        marker_color='red'
    ))
    
    fig.update_layout(
        barmode='stack',
        xaxis_tickangle=-45,
        height=400,
        title="Quality Issues by Trade",
        xaxis_title="Trade",
        yaxis_title="Number of Issues",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Quality metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Issues", total_issues)
    
    with col2:
        st.metric("Resolved Issues", total_resolved, f"{resolution_rate:.1f}%")
    
    with col3:
        open_issues = total_issues - total_resolved
        st.metric("Open Issues", open_issues)
    
    with col4:
        critical_issues = random.randint(1, max(1, open_issues // 3))
        st.metric("Critical Issues", critical_issues)
    
    # Quality issues by area
    areas = [
        "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", 
        "Level 6", "Level 7", "Level 8", "Roof", "Exterior"
    ]
    
    issue_by_area = [random.randint(1, 12) for _ in areas]
    
    fig = px.bar(
        x=areas,
        y=issue_by_area,
        title="Quality Issues by Area",
        labels={"x": "Area", "y": "Number of Issues"}
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Quality issues by type
        issue_types = [
            "Incorrect Installation", 
            "Material Defect",
            "Poor Workmanship",
            "Damage After Installation",
            "Missing Components",
            "Code Violation"
        ]
        
        type_counts = [random.randint(3, 15) for _ in issue_types]
        
        fig = px.pie(
            values=type_counts,
            names=issue_types,
            title="Issues by Type"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_financial_analysis():
    """Render charts for financial analysis."""
    st.subheader("Financial Analysis")
    
    # Create container with white background
    st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
    
    # Generate sample financial data
    today = datetime.now()
    start_date = today - timedelta(days=365)
    project_end = today + timedelta(days=180)
    
    # Create date range by month
    months = pd.date_range(start=start_date, end=project_end, freq='MS')
    month_labels = [d.strftime('%b %Y') for d in months]
    
    # S-Curve data
    planned_cumulative = [0]
    actual_cumulative = [0]
    forecast_cumulative = []
    
    total_budget = 45500000  # From project info
    
    # Generate S-curve based on normal distribution
    from scipy.stats import norm
    
    total_months = len(months)
    x = np.linspace(-1.5, 1.5, total_months)
    y = norm.cdf(x)
    
    # Scale to total budget
    planned_curve = y * total_budget
    
    # Add some variance for actual values
    actual_variance_factors = [1.0]
    for i in range(1, len(months)):
        if months[i] <= today:
            # Past months - add some variance
            variance = random.uniform(0.95, 1.05)
            actual_variance_factors.append(variance)
        else:
            # Future months - no actual data
            actual_variance_factors.append(None)
    
    # Calculate cumulative values
    for i in range(len(months)):
        if i > 0:
            month_planned = planned_curve[i] - planned_curve[i-1]
            planned_cumulative.append(planned_cumulative[-1] + month_planned)
            
            if actual_variance_factors[i] is not None:
                month_actual = month_planned * actual_variance_factors[i]
                actual_cumulative.append(actual_cumulative[-1] + month_actual)
    
    # Create forecast data
    forecast_cumulative = actual_cumulative.copy()
    last_actual_index = len(actual_cumulative) - 1
    
    # Forecast future months
    if last_actual_index < len(planned_cumulative) - 1:
        forecast_variance = actual_cumulative[-1] / planned_cumulative[last_actual_index]
        
        for i in range(last_actual_index + 1, len(planned_cumulative)):
            # Adjust forecast based on current variance trend
            next_forecast = planned_cumulative[i] * forecast_variance
            forecast_cumulative.append(next_forecast)
    
    # Create S-curve chart
    fig = go.Figure()
    
    # Planned curve
    fig.add_trace(go.Scatter(
        x=month_labels,
        y=planned_cumulative,
        mode='lines+markers',
        name='Planned',
        line=dict(color='blue')
    ))
    
    # Actual curve
    fig.add_trace(go.Scatter(
        x=month_labels[:len(actual_cumulative)],
        y=actual_cumulative,
        mode='lines+markers',
        name='Actual',
        line=dict(color='green')
    ))
    
    # Forecast curve
    if len(forecast_cumulative) > len(actual_cumulative):
        fig.add_trace(go.Scatter(
            x=month_labels[len(actual_cumulative)-1:len(forecast_cumulative)],
            y=forecast_cumulative[len(actual_cumulative)-1:],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='red', dash='dash')
        ))
    
    # Add vertical line for today
    today_index = 0
    for i, d in enumerate(months):
        if d.month == today.month and d.year == today.year:
            today_index = i
            break
    
    fig.add_vline(
        x=today_index, 
        line_width=2, 
        line_dash="dash", 
        line_color="gray",
        annotation_text="Today",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title="Project Cash Flow S-Curve",
        xaxis_title="Month",
        yaxis_title="Cumulative Cost ($)",
        height=500,
        xaxis_tickangle=-45,
        yaxis=dict(tickformat='$,.0f')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Financial metrics
    current_planned = planned_cumulative[today_index]
    current_actual = actual_cumulative[-1] if len(actual_cumulative) > today_index else 0
    variance = current_planned - current_actual
    variance_percent = (variance / current_planned) * 100 if current_planned > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Planned to Date", f"${current_planned:,.0f}")
    
    with col2:
        st.metric("Actual to Date", f"${current_actual:,.0f}")
    
    with col3:
        st.metric("Variance", f"${variance:,.0f}", f"{variance_percent:.1f}%", 
                  delta_color="normal" if variance >= 0 else "inverse")
    
    with col4:
        # Estimated at completion
        eac = forecast_cumulative[-1] if forecast_cumulative else total_budget
        st.metric("Forecast at Completion", f"${eac:,.0f}", 
                 f"{(eac - total_budget) / total_budget * 100:.1f}%",
                 delta_color="inverse" if eac > total_budget else "normal")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Cash flow analysis
    st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
    st.markdown("### Monthly Cash Flow")
    
    # Create monthly data
    month_expenses = []
    month_incomes = []
    
    for i in range(1, len(planned_cumulative)):
        # Monthly planned expenses
        month_expense = planned_cumulative[i] - planned_cumulative[i-1]
        month_expenses.append(month_expense)
        
        # Monthly income (based on expenses plus profit, with 1-month delay)
        if i > 1:
            income = month_expenses[i-2] * 1.08  # 8% profit margin
        else:
            income = 0
        
        month_incomes.append(income)
    
    # Create cash flow chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=month_labels[1:],
        y=month_expenses,
        name='Expenses',
        marker_color='red'
    ))
    
    fig.add_trace(go.Bar(
        x=month_labels[1:],
        y=month_incomes,
        name='Income',
        marker_color='green'
    ))
    
    # Add net cash flow line
    net_cash_flow = [inc - exp for inc, exp in zip(month_incomes, month_expenses)]
    
    fig.add_trace(go.Scatter(
        x=month_labels[1:],
        y=net_cash_flow,
        mode='lines+markers',
        name='Net Cash Flow',
        line=dict(color='blue')
    ))
    
    fig.update_layout(
        title="Monthly Cash Flow",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        height=400,
        xaxis_tickangle=-45,
        yaxis=dict(tickformat='$,.0f'),
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render():
    """Render the Analysis module."""
    st.title("Project Analytics")
    
    # Create tabs for different analysis views
    tab1, tab2, tab3, tab4 = st.tabs([
        "Project Performance", 
        "Financial Analysis", 
        "Safety Analysis", 
        "Quality Analysis"
    ])
    
    # Project Performance tab
    with tab1:
        render_project_performance_charts()
    
    # Financial Analysis tab
    with tab2:
        render_financial_analysis()
    
    # Safety Analysis tab
    with tab3:
        render_safety_analysis()
    
    # Quality Analysis tab
    with tab4:
        render_quality_analysis()