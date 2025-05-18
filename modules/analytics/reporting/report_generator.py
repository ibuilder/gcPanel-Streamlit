"""
Custom Report Generator for gcPanel.

This module provides customizable report generation functionality with
options to export reports in various formats including PDF and Excel.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import io
import base64
from datetime import datetime, timedelta

# Utility functions for report generation
def get_mock_report_data():
    """
    Get sample data for report templates.
    
    In a production environment, this would fetch real data from the database.
    """
    # Generate dates for last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # Generate budget data
    total_budget = 45500000  # $45.5M total budget
    planned_budget = np.linspace(0, total_budget * 0.85, len(dates))
    actual_budget = planned_budget + np.random.normal(0, 500000, len(dates))
    
    # Generate schedule data (% complete)
    planned_schedule = np.linspace(0, 85, len(dates))
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

def generate_project_summary(df):
    """
    Generate project summary section.
    
    Args:
        df: DataFrame with project data
        
    Returns:
        tuple: (summary_text, summary_metrics)
    """
    # Get latest data
    latest = df.iloc[-1]
    
    # Calculate key metrics
    budget_variance = ((latest['actual_budget'] - latest['planned_budget']) / latest['planned_budget']) * 100
    schedule_variance = latest['actual_schedule'] - latest['planned_schedule']
    
    # Create summary text
    summary_text = f"""
    # Project Summary Report
    
    ## Highland Tower Development
    **Report Date:** {datetime.now().strftime('%Y-%m-%d')}
    
    ### Project Overview
    The Highland Tower Development is a $45.5M mixed-use project featuring 120 residential units 
    and 8 retail spaces. The development spans 168,500 sq ft across 15 stories above ground and 
    2 stories below ground.
    
    ### Current Status
    As of {latest['date'].strftime('%B %d, %Y')}, the project is **{latest['actual_schedule']:.1f}%** 
    complete. The project is currently **{schedule_variance:.1f}%** {"ahead of" if schedule_variance > 0 else "behind"} 
    schedule and **{abs(budget_variance):.1f}%** {"over" if budget_variance > 0 else "under"} budget.
    """
    
    # Create summary metrics
    summary_metrics = {
        "Budget Status": f"${latest['actual_budget']:,.0f} of ${latest['planned_budget']:,.0f} ({budget_variance:.1f}%)",
        "Schedule Status": f"{latest['actual_schedule']:.1f}% of {latest['planned_schedule']:.1f}% ({schedule_variance:.1f}%)",
        "Quality Issues": f"{latest['issues_resolved']} of {latest['issues_found']} resolved",
        "Safety Incidents": f"{latest['safety_incidents']} incidents, {latest['near_misses']} near misses"
    }
    
    return summary_text, summary_metrics

def generate_budget_section(df):
    """
    Generate budget section for report.
    
    Args:
        df: DataFrame with project data
        
    Returns:
        tuple: (section_text, budget_chart)
    """
    # Get latest data
    latest = df.iloc[-1]
    
    # Calculate key metrics
    budget_variance = ((latest['actual_budget'] - latest['planned_budget']) / latest['planned_budget']) * 100
    
    # Create section text
    section_text = f"""
    ## Budget Analysis
    
    The project's total budget is $45,500,000. Current expenditure is 
    ${latest['actual_budget']:,.0f}, which is {budget_variance:.1f}% 
    {"over" if budget_variance > 0 else "under"} the planned amount of 
    ${latest['planned_budget']:,.0f}.
    
    ### Key Financial Metrics
    - **Burn Rate:** ${latest['actual_budget'] / len(df):,.0f} per month
    - **Estimated Final Cost:** ${45500000 * (1 + budget_variance/100):,.0f}
    - **Budget Contingency Remaining:** ${45500000 * 0.08 - (latest['actual_budget'] - latest['planned_budget']):,.0f}
    """
    
    # Create budget chart
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
        height=400
    )
    
    return section_text, fig

def generate_schedule_section(df):
    """
    Generate schedule section for report.
    
    Args:
        df: DataFrame with project data
        
    Returns:
        tuple: (section_text, schedule_chart)
    """
    # Get latest data
    latest = df.iloc[-1]
    
    # Calculate key metrics
    schedule_variance = latest['actual_schedule'] - latest['planned_schedule']
    
    # Create section text
    section_text = f"""
    ## Schedule Analysis
    
    The project is currently {latest['actual_schedule']:.1f}% complete,
    which is {abs(schedule_variance):.1f}% {"ahead of" if schedule_variance > 0 else "behind"} 
    the planned progress of {latest['planned_schedule']:.1f}%.
    
    ### Key Schedule Metrics
    - **Average Weekly Progress:** {latest['actual_schedule'] / (len(df) * 4):.1f}%
    - **Estimated Completion Date:** {(datetime.now() + timedelta(days=(100 - latest['actual_schedule']) / (latest['actual_schedule'] / (len(df) * 30)))).strftime('%Y-%m-%d')}
    - **Critical Path Status:** {"On Track" if schedule_variance >= 0 else "At Risk"}
    """
    
    # Create schedule chart
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
        height=400
    )
    
    return section_text, fig

def generate_quality_safety_section(df):
    """
    Generate quality and safety section for report.
    
    Args:
        df: DataFrame with project data
        
    Returns:
        tuple: (section_text, quality_chart, safety_chart)
    """
    # Get latest data
    latest = df.iloc[-1]
    
    # Calculate quality rate
    issues_rate = latest['issues_found'] / latest['inspections'] if latest['inspections'] > 0 else 0
    resolution_rate = latest['issues_resolved'] / latest['issues_found'] if latest['issues_found'] > 0 else 1
    
    # Create section text
    section_text = f"""
    ## Quality and Safety
    
    ### Quality Metrics
    - **Number of Inspections:** {latest['inspections']}
    - **Issues Found:** {latest['issues_found']} ({issues_rate:.2f} per inspection)
    - **Issues Resolved:** {latest['issues_resolved']} ({resolution_rate:.0%} resolution rate)
    
    ### Safety Metrics
    - **Recordable Incidents:** {latest['safety_incidents']}
    - **Near Misses:** {latest['near_misses']}
    - **Incident Rate:** {sum(df['safety_incidents']) / (len(df) * 30 * 100) * 200000:.2f} (per 200,000 work hours)
    """
    
    # Create quality chart
    quality_fig = go.Figure()
    
    # Add bars for issues found
    quality_fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['issues_found'],
            name="Issues Found",
            marker_color='red'
        )
    )
    
    # Add bars for issues resolved
    quality_fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['issues_resolved'],
            name="Issues Resolved",
            marker_color='green'
        )
    )
    
    # Add line for inspections
    quality_fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['inspections'],
            name="Inspections",
            line=dict(color='blue'),
            yaxis="y2"
        )
    )
    
    # Update layout
    quality_fig.update_layout(
        title="Quality Metrics Over Time",
        xaxis_title="Date",
        yaxis_title="Issues",
        yaxis2=dict(
            title="Inspections",
            overlaying="y",
            side="right"
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        barmode='group',
        height=300
    )
    
    # Create safety chart
    safety_fig = go.Figure()
    
    # Add bars for safety incidents
    safety_fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['safety_incidents'],
            name="Safety Incidents",
            marker_color='red'
        )
    )
    
    # Add bars for near misses
    safety_fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['near_misses'],
            name="Near Misses",
            marker_color='orange'
        )
    )
    
    # Update layout
    safety_fig.update_layout(
        title="Safety Metrics Over Time",
        xaxis_title="Date",
        yaxis_title="Count",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        barmode='stack',
        height=300
    )
    
    return section_text, quality_fig, safety_fig

def generate_issues_risks_section():
    """
    Generate issues and risks section for report.
    
    Returns:
        str: section_text
    """
    # Create section text
    section_text = """
    ## Key Issues and Risks
    
    ### Current Issues
    1. **Material Delivery Delays**: Curtain wall systems delayed by 3 weeks due to supply chain issues
    2. **Subcontractor Performance**: MEP subcontractor behind schedule on 12th and 13th floors
    3. **Design Changes**: Late owner-requested changes to retail spaces impacting finishes schedule
    
    ### Risk Assessment
    | Risk | Probability | Impact | Mitigation |
    |------|------------|--------|------------|
    | Weather delays | Medium | High | Accelerated interior work schedule, temporary weather protection |
    | Labor shortage | High | Medium | Advanced recruiting, overtime authorization, alternative subcontractors |
    | Material cost escalation | Medium | High | Early procurement, alternative material evaluation, contingency allocation |
    | Permit delays | Low | High | Pre-submission meetings with officials, expedited permit applications |
    """
    
    return section_text

def generate_recommendations_section():
    """
    Generate recommendations section for report.
    
    Returns:
        str: section_text
    """
    # Create section text
    section_text = """
    ## Recommendations and Next Steps
    
    ### Recommended Actions
    1. **Schedule Recovery**: Implement weekend work for MEP subcontractor to recover schedule on 12th and 13th floors
    2. **Budget Management**: Review and adjust contingency allocations based on updated risk assessment
    3. **Material Procurement**: Expedite curtain wall delivery and identify alternative suppliers for critical path items
    4. **Quality Assurance**: Increase inspection frequency for high-risk work areas (structural connections, waterproofing)
    
    ### Next Milestone Targets
    - Complete building envelope by June 15, 2025
    - Begin interior finishes on floors 8-15 by July 1, 2025
    - Finalize commissioning plan by July 15, 2025
    - Complete elevator installation by August 1, 2025
    """
    
    return section_text

def create_excel_report(df):
    """
    Create Excel report from dataframe.
    
    Args:
        df: DataFrame with project data
        
    Returns:
        bytes: Excel file as bytes
    """
    # Create a BytesIO object to hold the Excel file
    output = io.BytesIO()
    
    # Create ExcelWriter object
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Write project summary to Excel
        summary_month = df.resample('M', on='date').last()
        summary_month.to_excel(writer, sheet_name='Project Summary', index=True)
        
        # Write detailed data to Excel
        df.to_excel(writer, sheet_name='Detailed Data', index=False)
        
        # Create and write budget analysis
        budget_df = pd.DataFrame({
            'Date': df['date'],
            'Planned Budget': df['planned_budget'],
            'Actual Expenditure': df['actual_budget'],
            'Variance': df['actual_budget'] - df['planned_budget'],
            'Variance %': ((df['actual_budget'] - df['planned_budget']) / df['planned_budget']) * 100
        })
        budget_df.to_excel(writer, sheet_name='Budget Analysis', index=False)
        
        # Create and write schedule analysis
        schedule_df = pd.DataFrame({
            'Date': df['date'],
            'Planned Progress': df['planned_schedule'],
            'Actual Progress': df['actual_schedule'],
            'Variance': df['actual_schedule'] - df['planned_schedule']
        })
        schedule_df.to_excel(writer, sheet_name='Schedule Analysis', index=False)
        
        # Create and write quality analysis
        quality_df = pd.DataFrame({
            'Date': df['date'],
            'Inspections': df['inspections'],
            'Issues Found': df['issues_found'],
            'Issues Resolved': df['issues_resolved'],
            'Issues per Inspection': df['issues_found'] / df['inspections'].replace(0, 1),
            'Resolution Rate': df['issues_resolved'] / df['issues_found'].replace(0, 1)
        })
        quality_df.to_excel(writer, sheet_name='Quality Analysis', index=False)
        
        # Create and write safety analysis
        safety_df = pd.DataFrame({
            'Date': df['date'],
            'Safety Incidents': df['safety_incidents'],
            'Near Misses': df['near_misses'],
            'Total Safety Events': df['safety_incidents'] + df['near_misses']
        })
        safety_df.to_excel(writer, sheet_name='Safety Analysis', index=False)
    
    # Move to the beginning of the BytesIO object
    output.seek(0)
    
    return output.getvalue()

def create_download_link(data, filename, link_text):
    """
    Create a download link for data.
    
    Args:
        data: Data to download
        filename: Name of file
        link_text: Text for download link
        
    Returns:
        str: HTML for download link
    """
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

def render_report_generator():
    """Render the custom report generator interface."""
    st.header("Custom Report Generator")
    
    # Get report data
    df = get_mock_report_data()
    
    # Project selector (in a real app, this would load different project data)
    project = st.selectbox(
        "Select Project",
        ["Highland Tower Development", "Project B", "Project C"],
        index=0
    )
    
    # Report type selector
    report_type = st.selectbox(
        "Report Type",
        ["Executive Summary", "Detailed Progress Report", "Financial Report", "Schedule Analysis", "Custom Report"]
    )
    
    # Date range selector
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=df['date'].min().date(),
            min_value=df['date'].min().date(),
            max_value=df['date'].max().date()
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            value=df['date'].max().date(),
            min_value=df['date'].min().date(),
            max_value=df['date'].max().date()
        )
    
    # Filter data based on date range
    filtered_df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
    
    # Custom report options
    if report_type == "Custom Report":
        st.subheader("Select Report Sections")
        include_summary = st.checkbox("Project Summary", value=True)
        include_budget = st.checkbox("Budget Analysis", value=True)
        include_schedule = st.checkbox("Schedule Analysis", value=True)
        include_quality = st.checkbox("Quality Metrics", value=True)
        include_safety = st.checkbox("Safety Metrics", value=True)
        include_issues = st.checkbox("Issues and Risks", value=True)
        include_recommendations = st.checkbox("Recommendations", value=True)
    else:
        # Set default sections based on report type
        include_summary = True
        include_budget = report_type in ["Executive Summary", "Detailed Progress Report", "Financial Report"]
        include_schedule = report_type in ["Executive Summary", "Detailed Progress Report", "Schedule Analysis"]
        include_quality = report_type in ["Detailed Progress Report"]
        include_safety = report_type in ["Detailed Progress Report"]
        include_issues = report_type in ["Executive Summary", "Detailed Progress Report"]
        include_recommendations = report_type in ["Executive Summary", "Detailed Progress Report"]
    
    # Generate report preview
    st.subheader("Report Preview")
    
    # Project summary section
    if include_summary:
        summary_text, summary_metrics = generate_project_summary(filtered_df)
        st.markdown(summary_text)
        
        # Display metrics
        metrics_cols = st.columns(len(summary_metrics))
        for i, (label, value) in enumerate(summary_metrics.items()):
            with metrics_cols[i]:
                st.metric(label=label, value=value)
        
        st.markdown("---")
    
    # Budget section
    if include_budget:
        budget_text, budget_chart = generate_budget_section(filtered_df)
        st.markdown(budget_text)
        st.plotly_chart(budget_chart, use_container_width=True)
        st.markdown("---")
    
    # Schedule section
    if include_schedule:
        schedule_text, schedule_chart = generate_schedule_section(filtered_df)
        st.markdown(schedule_text)
        st.plotly_chart(schedule_chart, use_container_width=True)
        st.markdown("---")
    
    # Quality and safety section
    if include_quality or include_safety:
        quality_safety_text, quality_chart, safety_chart = generate_quality_safety_section(filtered_df)
        st.markdown(quality_safety_text)
        
        if include_quality:
            st.plotly_chart(quality_chart, use_container_width=True)
        
        if include_safety:
            st.plotly_chart(safety_chart, use_container_width=True)
        
        st.markdown("---")
    
    # Issues and risks section
    if include_issues:
        issues_risks_text = generate_issues_risks_section()
        st.markdown(issues_risks_text)
        st.markdown("---")
    
    # Recommendations section
    if include_recommendations:
        recommendations_text = generate_recommendations_section()
        st.markdown(recommendations_text)
    
    # Export options
    st.subheader("Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export as PDF"):
            st.info("PDF export functionality would be implemented here.")
            st.info("In a production environment, this would generate a PDF report using ReportLab or another PDF generation library.")
    
    with col2:
        if st.button("Export as Excel"):
            # Create Excel report
            excel_data = create_excel_report(filtered_df)
            
            # Create download link
            file_name = f"{project.replace(' ', '_')}_{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx"
            st.markdown(create_download_link(excel_data, file_name, "Download Excel Report"), unsafe_allow_html=True)
    
    with col3:
        if st.button("Export as CSV"):
            # Export as CSV
            csv_data = filtered_df.to_csv(index=False).encode()
            
            # Create download link
            file_name = f"{project.replace(' ', '_')}_{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv"
            st.markdown(create_download_link(csv_data, file_name, "Download CSV Report"), unsafe_allow_html=True)
    
    # Scheduled reports option
    st.subheader("Schedule Recurring Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        frequency = st.selectbox(
            "Report Frequency",
            ["Daily", "Weekly", "Bi-Weekly", "Monthly", "Quarterly"]
        )
    
    with col2:
        recipients = st.text_input("Email Recipients (comma-separated)")
    
    if st.button("Schedule Report"):
        st.success(f"Report scheduled to be sent {frequency.lower()} to: {recipients}")
        st.info("In a production environment, this would schedule recurring reports using a task scheduler.")