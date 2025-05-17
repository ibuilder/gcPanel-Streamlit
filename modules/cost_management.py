"""
Cost Management module for the gcPanel Construction Management Dashboard.

This module provides cost management functionality including budgets, expenses,
forecasting, and financial reporting.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

def render_cost_management():
    """Render the cost management interface."""
    st.header("Cost Management")
    
    # Create tabs for different cost management functions
    tabs = st.tabs(["Overview", "Budget vs. Actual", "Forecasting", "Reporting"])
    
    # Cost Overview Tab
    with tabs[0]:
        render_cost_overview()
    
    # Budget vs. Actual Tab
    with tabs[1]:
        render_budget_vs_actual()
    
    # Forecasting Tab
    with tabs[2]:
        render_forecasting()
        
    # Reporting Tab
    with tabs[3]:
        render_reporting()

def render_cost_overview():
    """Render the cost overview dashboard."""
    st.subheader("Cost Overview")
    
    # Cost metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Budget", "$42.5M", "All Projects")
    with col2:
        st.metric("Spent to Date", "$18.3M", "43% of budget")
    with col3:
        st.metric("Forecast at Completion", "$43.2M", "+$0.7M over budget")
    
    # Cost performance by project
    st.subheader("Cost Performance by Project")
    
    cost_performance = [
        {"project": "Highland Tower", "budget": "$15,500,000", "actual": "$6,750,000", "forecast": "$15,900,000", "variance": "-$400,000", "variance_pct": "-2.6%"},
        {"project": "City Center", "budget": "$12,200,000", "actual": "$8,200,000", "forecast": "$12,100,000", "variance": "+$100,000", "variance_pct": "+0.8%"},
        {"project": "Riverside Apartments", "budget": "$8,800,000", "actual": "$2,100,000", "forecast": "$9,200,000", "variance": "-$400,000", "variance_pct": "-4.5%"},
        {"project": "Metro Office Complex", "budget": "$6,000,000", "actual": "$1,250,000", "forecast": "$6,000,000", "variance": "$0", "variance_pct": "0.0%"}
    ]
    
    cost_df = pd.DataFrame(cost_performance)
    
    # Apply styling based on variance
    def variance_color(val):
        if '-' in val:
            return 'background-color: #fee2e2; color: #7f1d1d'
        elif '+' in val:
            return 'background-color: #d1fae5; color: #064e3b'
        else:
            return 'background-color: #f5f5f4; color: #44403c'
    
    # Apply styling
    styled_cost_df = cost_df.style.applymap(variance_color, subset=['variance_pct'])
    
    # Display the dataframe
    st.dataframe(styled_cost_df, use_container_width=True)
    
    # Cost distribution chart
    st.subheader("Cost Distribution by Category")
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost distribution data
        cost_categories = {
            'Category': ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'General Conditions', 'Overhead'],
            'Percentage': [30, 25, 10, 20, 10, 5]
        }
        
        cost_cat_df = pd.DataFrame(cost_categories)
        st.bar_chart(cost_cat_df.set_index('Category'), color='#1e3a8a')
    
    with col2:
        # Cost trend data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        cost_trend = pd.DataFrame({
            'Month': months,
            'Budget': [1.2, 2.4, 3.6, 4.8, 6.0, 7.2, 8.4, 9.6, 10.8, 12.0, 13.2, 14.4],
            'Actual': [1.1, 2.3, 3.5, 4.9, 6.2, 7.4, 8.6, 9.8, 11.0, 12.2, 13.4, 14.6]
        })
        
        # Plot the trend
        st.line_chart(cost_trend.set_index('Month'))
    
    # Recent cost activities
    st.subheader("Recent Cost Activities")
    
    activities = [
        {"date": "2025-05-15", "project": "Highland Tower", "description": "Concrete subcontractor payment", "amount": "$245,000"},
        {"date": "2025-05-14", "project": "City Center", "description": "Steel materials delivery", "amount": "$180,000"},
        {"date": "2025-05-12", "project": "Riverside Apartments", "description": "Equipment rental - tower crane", "amount": "$35,000"},
        {"date": "2025-05-10", "project": "Metro Office", "description": "Labor - site preparation", "amount": "$48,000"},
        {"date": "2025-05-08", "project": "Highland Tower", "description": "Change order - foundation work", "amount": "$45,000"}
    ]
    
    activities_df = pd.DataFrame(activities)
    st.dataframe(activities_df, use_container_width=True)

def render_budget_vs_actual():
    """Render the budget vs. actual cost comparison."""
    st.subheader("Budget vs. Actual")
    
    # Project selector
    project = st.selectbox(
        "Select Project",
        ["All Projects", "Highland Tower", "City Center", "Riverside Apartments", "Metro Office Complex"]
    )
    
    # Cost breakdown structure selector
    if project != "All Projects":
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("From Date", datetime.now() - timedelta(days=180))
        with col2:
            st.date_input("To Date", datetime.now())
        
        # Cost breakdown view toggle
        view_type = st.radio("View By", ["Cost Codes", "Time", "Work Packages"])
        
        if view_type == "Cost Codes":
            render_cost_codes_view(project)
        elif view_type == "Time":
            render_time_view(project)
        else:
            render_work_packages_view(project)
    else:
        # Summary table for all projects
        st.subheader("All Projects Budget Summary")
        
        budget_summary = [
            {"category": "Labor", "budget": "$12,750,000", "actual": "$5,490,000", "variance": "$7,260,000", "percent_spent": "43.1%"},
            {"category": "Materials", "budget": "$10,625,000", "actual": "$4,575,000", "variance": "$6,050,000", "percent_spent": "43.1%"},
            {"category": "Equipment", "budget": "$4,250,000", "actual": "$1,830,000", "variance": "$2,420,000", "percent_spent": "43.1%"},
            {"category": "Subcontractors", "budget": "$8,500,000", "actual": "$3,660,000", "variance": "$4,840,000", "percent_spent": "43.1%"},
            {"category": "General Conditions", "budget": "$4,250,000", "actual": "$1,830,000", "variance": "$2,420,000", "percent_spent": "43.1%"},
            {"category": "Overhead", "budget": "$2,125,000", "actual": "$915,000", "variance": "$1,210,000", "percent_spent": "43.1%"},
            {"category": "TOTAL", "budget": "$42,500,000", "actual": "$18,300,000", "variance": "$24,200,000", "percent_spent": "43.1%"}
        ]
        
        budget_df = pd.DataFrame(budget_summary)
        st.dataframe(budget_df, use_container_width=True)
        
        # Project comparison chart
        st.subheader("Project Budget Performance")
        
        project_performance = {
            'Project': ['Highland Tower', 'City Center', 'Riverside Apartments', 'Metro Office'],
            'Budget %': [100, 100, 100, 100],
            'Actual %': [43.5, 67.2, 23.9, 20.8]
        }
        
        project_df = pd.DataFrame(project_performance)
        st.bar_chart(project_df.set_index('Project'))

def render_cost_codes_view(project):
    """Render cost breakdown by cost codes."""
    st.subheader(f"{project} - Cost Codes")
    
    # Sample cost code data
    if project == "Highland Tower":
        cost_codes = [
            {"code": "01-1000", "description": "General Requirements", "budget": "$775,000", "actual": "$310,000", "forecast": "$775,000", "variance": "$0", "percent_spent": "40.0%"},
            {"code": "02-2000", "description": "Site Work", "budget": "$930,000", "actual": "$930,000", "forecast": "$930,000", "variance": "$0", "percent_spent": "100.0%"},
            {"code": "03-3000", "description": "Concrete", "budget": "$1,850,000", "actual": "$1,110,000", "forecast": "$1,900,000", "variance": "-$50,000", "percent_spent": "60.0%"},
            {"code": "05-1000", "description": "Structural Steel", "budget": "$2,100,000", "actual": "$1,260,000", "forecast": "$2,100,000", "variance": "$0", "percent_spent": "60.0%"},
            {"code": "07-1000", "description": "Thermal & Moisture Protection", "budget": "$1,240,000", "actual": "$310,000", "forecast": "$1,240,000", "variance": "$0", "percent_spent": "25.0%"},
            {"code": "08-1000", "description": "Doors & Windows", "budget": "$930,000", "actual": "$140,000", "forecast": "$980,000", "variance": "-$50,000", "percent_spent": "15.1%"},
            {"code": "09-1000", "description": "Finishes", "budget": "$1,550,000", "actual": "$155,000", "forecast": "$1,550,000", "variance": "$0", "percent_spent": "10.0%"},
            {"code": "15-1000", "description": "Mechanical", "budget": "$2,325,000", "actual": "$930,000", "forecast": "$2,375,000", "variance": "-$50,000", "percent_spent": "40.0%"},
            {"code": "16-1000", "description": "Electrical", "budget": "$1,860,000", "actual": "$744,000", "forecast": "$1,910,000", "variance": "-$50,000", "percent_spent": "40.0%"},
        ]
    else:
        # Generate some placeholder data for other projects
        cost_codes = [
            {"code": "01-1000", "description": "General Requirements", "budget": "$500,000", "actual": "$200,000", "forecast": "$500,000", "variance": "$0", "percent_spent": "40.0%"},
            {"code": "02-2000", "description": "Site Work", "budget": "$600,000", "actual": "$600,000", "forecast": "$600,000", "variance": "$0", "percent_spent": "100.0%"},
            {"code": "03-3000", "description": "Concrete", "budget": "$1,200,000", "actual": "$720,000", "forecast": "$1,200,000", "variance": "$0", "percent_spent": "60.0%"},
            {"code": "05-1000", "description": "Structural Steel", "budget": "$1,400,000", "actual": "$840,000", "forecast": "$1,400,000", "variance": "$0", "percent_spent": "60.0%"},
            {"code": "07-1000", "description": "Thermal & Moisture Protection", "budget": "$800,000", "actual": "$200,000", "forecast": "$800,000", "variance": "$0", "percent_spent": "25.0%"},
        ]
    
    # Convert to DataFrame
    cost_codes_df = pd.DataFrame(cost_codes)
    
    # Apply styling based on variance
    def variance_color(val):
        if '-' in val:
            return 'background-color: #fee2e2; color: #7f1d1d'
        elif '+' in val:
            return 'background-color: #d1fae5; color: #064e3b'
        else:
            return 'background-color: #f5f5f4; color: #44403c'
    
    # Apply styling
    styled_df = cost_codes_df.style.applymap(variance_color, subset=['variance'])
    
    # Display the dataframe
    st.dataframe(styled_df, use_container_width=True)
    
    # Chart showing budget vs actual
    st.subheader("Budget vs. Actual by Cost Code")
    
    # Prepare data for chart
    chart_data = cost_codes_df[['description', 'budget', 'actual']].copy()
    chart_data['budget'] = chart_data['budget'].str.replace('$', '').str.replace(',', '').astype(float)
    chart_data['actual'] = chart_data['actual'].str.replace('$', '').str.replace(',', '').astype(float)
    
    # Create a temporary pivoted dataframe for the chart
    chart_pivot = pd.DataFrame({
        'Cost Code': chart_data['description'],
        'Budget': chart_data['budget'],
        'Actual': chart_data['actual']
    })
    
    chart_pivot = chart_pivot.set_index('Cost Code')
    st.bar_chart(chart_pivot)

def render_time_view(project):
    """Render cost breakdown by time."""
    st.subheader(f"{project} - Monthly Costs")
    
    # Sample monthly cost data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    if project == "Highland Tower":
        monthly_data = pd.DataFrame({
            'Month': months,
            'Budget': [450, 520, 680, 650, 700, 750, 800, 850, 900, 950, 1000, 1100],
            'Actual': [460, 510, 690, 660, 710],
            'Forecast': [460, 510, 690, 660, 710, 760, 820, 870, 930, 980, 1050, 1150]
        })
    else:
        # Generate some placeholder data for other projects
        monthly_data = pd.DataFrame({
            'Month': months,
            'Budget': [250, 320, 380, 350, 400, 450, 500, 550, 600, 650, 700, 750],
            'Actual': [260, 310, 390, 360, 410],
            'Forecast': [260, 310, 390, 360, 410, 460, 520, 570, 630, 680, 730, 780]
        })
    
    # Set month as index for the chart
    chart_data = monthly_data.set_index('Month')
    
    # Display the line chart
    st.line_chart(chart_data)
    
    # Show the data in tabular form
    st.subheader("Monthly Cost Data")
    
    # Add variance columns
    monthly_table = monthly_data.copy()
    monthly_table['Monthly Variance'] = monthly_table.apply(
        lambda row: f"${(row['Actual'] - row['Budget']) * 1000:,.0f}" if pd.notnull(row['Actual']) else "N/A", 
        axis=1
    )
    
    monthly_table['Cumulative Variance'] = [
        "$10,000", "-$0", "$10,000", "$20,000", "$30,000", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"
    ]
    
    # Format the budget, actual, and forecast columns
    monthly_table['Budget'] = monthly_table['Budget'].apply(lambda x: f"${x * 1000:,.0f}")
    monthly_table['Actual'] = monthly_table['Actual'].apply(lambda x: f"${x * 1000:,.0f}" if pd.notnull(x) else "N/A")
    monthly_table['Forecast'] = monthly_table['Forecast'].apply(lambda x: f"${x * 1000:,.0f}" if pd.notnull(x) else "N/A")
    
    st.dataframe(monthly_table, use_container_width=True)

def render_work_packages_view(project):
    """Render cost breakdown by work packages."""
    st.subheader(f"{project} - Work Packages")
    
    # Sample work package data
    if project == "Highland Tower":
        work_packages = [
            {"id": "WP-001", "description": "Foundation Package", "budget": "$1,240,000", "actual": "$1,240,000", "forecast": "$1,240,000", "variance": "$0", "percent_complete": "100%"},
            {"id": "WP-002", "description": "Structural Frame Floors 1-10", "budget": "$2,480,000", "actual": "$2,480,000", "forecast": "$2,480,000", "variance": "$0", "percent_complete": "100%"},
            {"id": "WP-003", "description": "Structural Frame Floors 11-20", "budget": "$2,480,000", "actual": "$1,240,000", "forecast": "$2,530,000", "variance": "-$50,000", "percent_complete": "50%"},
            {"id": "WP-004", "description": "Exterior Envelope Floors 1-10", "budget": "$1,550,000", "actual": "$1,085,000", "forecast": "$1,550,000", "variance": "$0", "percent_complete": "70%"},
            {"id": "WP-005", "description": "Exterior Envelope Floors 11-20", "budget": "$1,550,000", "actual": "$0", "forecast": "$1,550,000", "variance": "$0", "percent_complete": "0%"},
            {"id": "WP-006", "description": "MEP Rough-in Floors 1-10", "budget": "$1,860,000", "actual": "$1,302,000", "forecast": "$1,900,000", "variance": "-$40,000", "percent_complete": "70%"},
            {"id": "WP-007", "description": "MEP Rough-in Floors 11-20", "budget": "$1,860,000", "actual": "$0", "forecast": "$1,900,000", "variance": "-$40,000", "percent_complete": "0%"},
            {"id": "WP-008", "description": "Interior Finishes Floors 1-10", "budget": "$1,240,000", "actual": "$372,000", "forecast": "$1,240,000", "variance": "$0", "percent_complete": "30%"},
        ]
    else:
        # Generate some placeholder data for other projects
        work_packages = [
            {"id": "WP-001", "description": "Foundation Package", "budget": "$800,000", "actual": "$800,000", "forecast": "$800,000", "variance": "$0", "percent_complete": "100%"},
            {"id": "WP-002", "description": "Structural Frame", "budget": "$1,600,000", "actual": "$1,120,000", "forecast": "$1,600,000", "variance": "$0", "percent_complete": "70%"},
            {"id": "WP-003", "description": "Exterior Envelope", "budget": "$1,200,000", "actual": "$600,000", "forecast": "$1,200,000", "variance": "$0", "percent_complete": "50%"},
            {"id": "WP-004", "description": "MEP Systems", "budget": "$1,800,000", "actual": "$720,000", "forecast": "$1,800,000", "variance": "$0", "percent_complete": "40%"},
            {"id": "WP-005", "description": "Interior Finishes", "budget": "$1,000,000", "actual": "$200,000", "forecast": "$1,000,000", "variance": "$0", "percent_complete": "20%"},
        ]
    
    # Convert to DataFrame
    work_packages_df = pd.DataFrame(work_packages)
    
    # Apply styling based on variance
    def variance_color(val):
        if '-' in val:
            return 'background-color: #fee2e2; color: #7f1d1d'
        elif '+' in val:
            return 'background-color: #d1fae5; color: #064e3b'
        else:
            return 'background-color: #f5f5f4; color: #44403c'
    
    # Apply styling
    styled_df = work_packages_df.style.applymap(variance_color, subset=['variance'])
    
    # Display the dataframe
    st.dataframe(styled_df, use_container_width=True)
    
    # Progress visualization
    st.subheader("Work Package Progress")
    
    # Display progress bars
    for package in work_packages:
        if package['percent_complete'] == "0%":
            continue
        
        # Extract percentage value
        percent = int(package['percent_complete'].replace('%', ''))
        
        # Display a progress bar
        st.markdown(f"**{package['id']}: {package['description']}**")
        st.progress(percent / 100)

def render_forecasting():
    """Render cost forecasting tools."""
    st.subheader("Cost Forecasting")
    
    # Project selector
    project = st.selectbox(
        "Select Project",
        ["All Projects", "Highland Tower", "City Center", "Riverside Apartments", "Metro Office Complex"],
        key="forecast_project"
    )
    
    # Forecasting method selector
    method = st.radio(
        "Forecasting Method",
        ["Estimate at Completion (EAC)", "Trend Analysis", "S-Curve Analysis"]
    )
    
    if method == "Estimate at Completion (EAC)":
        render_eac_forecast(project)
    elif method == "Trend Analysis":
        render_trend_forecast(project)
    else:
        render_scurve_forecast(project)

def render_eac_forecast(project):
    """Render EAC forecasting view."""
    st.subheader("Estimate at Completion (EAC)")
    
    # EAC metrics
    col1, col2, col3 = st.columns(3)
    
    if project == "All Projects":
        with col1:
            st.metric("Original Budget", "$42.5M")
        with col2:
            st.metric("EAC", "$43.2M")
        with col3:
            st.metric("Variance", "-$0.7M (-1.6%)")
        
        # EAC Table for all projects
        eac_data = [
            {"project": "Highland Tower", "budget": "$15,500,000", "spent": "$6,750,000", "etc": "$9,150,000", "eac": "$15,900,000", "variance": "-$400,000", "variance_pct": "-2.6%"},
            {"project": "City Center", "budget": "$12,200,000", "spent": "$8,200,000", "etc": "$3,900,000", "eac": "$12,100,000", "variance": "+$100,000", "variance_pct": "+0.8%"},
            {"project": "Riverside Apartments", "budget": "$8,800,000", "spent": "$2,100,000", "etc": "$7,100,000", "eac": "$9,200,000", "variance": "-$400,000", "variance_pct": "-4.5%"},
            {"project": "Metro Office Complex", "budget": "$6,000,000", "spent": "$1,250,000", "etc": "$4,750,000", "eac": "$6,000,000", "variance": "$0", "variance_pct": "0.0%"}
        ]
    else:
        # Show detailed information for a single project
        if project == "Highland Tower":
            with col1:
                st.metric("Original Budget", "$15.5M")
            with col2:
                st.metric("EAC", "$15.9M")
            with col3:
                st.metric("Variance", "-$0.4M (-2.6%)")
            
            # EAC Table for Highland Tower by cost category
            eac_data = [
                {"category": "General Requirements", "budget": "$775,000", "spent": "$310,000", "etc": "$465,000", "eac": "$775,000", "variance": "$0", "variance_pct": "0.0%"},
                {"category": "Site Work", "budget": "$930,000", "spent": "$930,000", "etc": "$0", "eac": "$930,000", "variance": "$0", "variance_pct": "0.0%"},
                {"category": "Concrete", "budget": "$1,850,000", "spent": "$1,110,000", "etc": "$790,000", "eac": "$1,900,000", "variance": "-$50,000", "variance_pct": "-2.7%"},
                {"category": "Structural Steel", "budget": "$2,100,000", "spent": "$1,260,000", "etc": "$840,000", "eac": "$2,100,000", "variance": "$0", "variance_pct": "0.0%"},
                {"category": "Thermal & Moisture", "budget": "$1,240,000", "spent": "$310,000", "etc": "$930,000", "eac": "$1,240,000", "variance": "$0", "variance_pct": "0.0%"},
                {"category": "MEP Systems", "budget": "$4,185,000", "spent": "$1,674,000", "etc": "$2,611,000", "eac": "$4,285,000", "variance": "-$100,000", "variance_pct": "-2.4%"},
                {"category": "Finishes", "budget": "$1,550,000", "spent": "$155,000", "etc": "$1,395,000", "eac": "$1,550,000", "variance": "$0", "variance_pct": "0.0%"},
                {"category": "General Conditions", "budget": "$1,550,000", "spent": "$620,000", "etc": "$930,000", "eac": "$1,550,000", "variance": "$0", "variance_pct": "0.0%"},
                {"category": "Fee & Contingency", "budget": "$1,320,000", "spent": "$391,000", "etc": "$1,179,000", "eac": "$1,570,000", "variance": "-$250,000", "variance_pct": "-18.9%"},
            ]
        else:
            # Placeholder for other projects
            with col1:
                st.metric("Original Budget", "$10.0M")
            with col2:
                st.metric("EAC", "$10.2M")
            with col3:
                st.metric("Variance", "-$0.2M (-2.0%)")
            
            eac_data = [
                {"category": "General Requirements", "budget": "$500,000", "spent": "$200,000", "etc": "$300,000", "eac": "$500,000", "variance": "$0", "variance_pct": "0.0%"},
                {"category": "Site Work", "budget": "$600,000", "spent": "$540,000", "etc": "$60,000", "eac": "$600,000", "variance": "$0", "variance_pct": "0.0%"},
                {"category": "Concrete & Steel", "budget": "$2,600,000", "spent": "$1,560,000", "etc": "$1,040,000", "eac": "$2,600,000", "variance": "$0", "variance_pct": "0.0%"},
                {"category": "Thermal & Moisture", "budget": "$800,000", "spent": "$240,000", "etc": "$560,000", "eac": "$800,000", "variance": "$0", "variance_pct": "0.0%"},
                {"category": "MEP Systems", "budget": "$2,700,000", "spent": "$810,000", "etc": "$1,890,000", "eac": "$2,700,000", "variance": "$0", "variance_pct": "0.0%"},
            ]
    
    # Convert to DataFrame
    eac_df = pd.DataFrame(eac_data)
    
    # Apply styling based on variance
    def variance_color(val):
        if '-' in val:
            return 'background-color: #fee2e2; color: #7f1d1d'
        elif '+' in val:
            return 'background-color: #d1fae5; color: #064e3b'
        else:
            return 'background-color: #f5f5f4; color: #44403c'
    
    # Apply styling
    styled_df = eac_df.style.applymap(variance_color, subset=['variance_pct'])
    
    # Display the dataframe
    st.dataframe(styled_df, use_container_width=True)
    
    # EAC Analysis
    st.subheader("EAC Formula Options")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**EAC = AC + (BAC - EV) / CPI**")
        st.write("This formula assumes future cost performance will be the same as past performance.")
    with col2:
        st.write("**EAC = AC + ETC**")
        st.write("This formula uses a bottom-up estimate for remaining work.")
    
    st.write("**Where:**")
    st.write("- AC = Actual Cost to date")
    st.write("- BAC = Budget at Completion")
    st.write("- EV = Earned Value")
    st.write("- CPI = Cost Performance Index")
    st.write("- ETC = Estimate to Complete")

def render_trend_forecast(project):
    """Render trend-based forecasting view."""
    st.subheader("Cost Trend Analysis")
    
    # Create sample trend data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    if project == "All Projects" or project == "Highland Tower":
        trend_data = pd.DataFrame({
            'Month': months,
            'Planned': [1.2, 2.4, 3.6, 4.8, 6.0, 7.2, 8.4, 9.6, 10.8, 12.0, 13.2, 14.4],
            'Actual': [1.3, 2.5, 3.8, 5.1, 6.4, None, None, None, None, None, None, None],
            'Forecast (Base)': [1.3, 2.5, 3.8, 5.1, 6.4, 7.7, 9.0, 10.3, 11.6, 12.9, 14.2, 15.5],
            'Forecast (Optimistic)': [1.3, 2.5, 3.8, 5.1, 6.4, 7.6, 8.8, 10.0, 11.2, 12.4, 13.6, 14.8],
            'Forecast (Pessimistic)': [1.3, 2.5, 3.8, 5.1, 6.4, 7.8, 9.2, 10.6, 12.0, 13.4, 14.8, 16.2]
        })
    else:
        # Generate placeholder trend data for other projects
        trend_data = pd.DataFrame({
            'Month': months,
            'Planned': [0.8, 1.6, 2.4, 3.2, 4.0, 4.8, 5.6, 6.4, 7.2, 8.0, 8.8, 9.6],
            'Actual': [0.7, 1.5, 2.2, 3.0, 3.8, None, None, None, None, None, None, None],
            'Forecast (Base)': [0.7, 1.5, 2.2, 3.0, 3.8, 4.6, 5.4, 6.2, 7.0, 7.8, 8.6, 9.4],
            'Forecast (Optimistic)': [0.7, 1.5, 2.2, 3.0, 3.8, 4.5, 5.2, 5.9, 6.6, 7.3, 8.0, 8.7],
            'Forecast (Pessimistic)': [0.7, 1.5, 2.2, 3.0, 3.8, 4.7, 5.6, 6.5, 7.4, 8.3, 9.2, 10.1]
        })
    
    # Select which forecast to show
    forecast_option = st.radio(
        "Forecast Scenario",
        ["Base Case", "Optimistic", "Pessimistic", "All Scenarios"]
    )
    
    # Prepare chart data based on selection
    if forecast_option == "Base Case":
        chart_data = trend_data[['Month', 'Planned', 'Actual', 'Forecast (Base)']].copy()
    elif forecast_option == "Optimistic":
        chart_data = trend_data[['Month', 'Planned', 'Actual', 'Forecast (Optimistic)']].copy()
    elif forecast_option == "Pessimistic":
        chart_data = trend_data[['Month', 'Planned', 'Actual', 'Forecast (Pessimistic)']].copy()
    else:
        chart_data = trend_data.copy()
    
    # Set month as index for the chart
    chart_pivot = chart_data.set_index('Month')
    
    # Display the line chart
    st.line_chart(chart_pivot)
    
    # Trend analysis explanation
    st.subheader("Trend Analysis Methodology")
    
    st.write("""
    Cost trend analysis extrapolates future performance based on historical data. The forecasts shown consider:
    
    - **Base Case**: Continues the current cost performance trend
    - **Optimistic**: Assumes 5% improvement in cost efficiency for remaining work
    - **Pessimistic**: Assumes 5% decrease in cost efficiency for remaining work
    
    This analysis helps identify potential budget risks early and informs mitigation strategies.
    """)

def render_scurve_forecast(project):
    """Render S-curve forecasting view."""
    st.subheader("S-Curve Analysis")
    
    # Generate sample S-curve data
    months = list(range(1, 25))  # 24 month project
    
    if project == "All Projects" or project == "Highland Tower":
        # Generate S-curve for a 24-month project
        planned_curve = [0]
        for i in range(1, 25):
            if i <= 6:  # Slow start
                increment = i * 0.5
            elif i <= 18:  # Rapid middle
                increment = 6
            else:  # Slow finish
                increment = (24 - i) * 0.5
            planned_curve.append(planned_curve[-1] + increment)
        
        # Normalize to budget
        total_budget = 15500000
        planned_curve = [round(x / planned_curve[-1] * total_budget, 0) for x in planned_curve][1:]
        
        # Generate actual curve (follows planned with some variance)
        actual_curve = []
        for i in range(len(planned_curve)):
            if i < 5:  # We have 5 months of actual data
                variance = random.uniform(0.95, 1.05)
                actual_curve.append(round(planned_curve[i] * variance, 0))
            else:
                actual_curve.append(None)
        
        # Create forecast curves
        forecast_base = actual_curve.copy()
        forecast_optimistic = actual_curve.copy()
        forecast_pessimistic = actual_curve.copy()
        
        # Fill in forecasts
        last_actual_index = 4  # 0-based index for month 5
        last_actual_value = actual_curve[last_actual_index]
        remaining_planned = [planned_curve[i] - planned_curve[last_actual_index] for i in range(last_actual_index + 1, len(planned_curve))]
        
        for i in range(last_actual_index + 1, len(planned_curve)):
            forecast_base[i] = round(last_actual_value + remaining_planned[i - last_actual_index - 1] * 1.02, 0)
            forecast_optimistic[i] = round(last_actual_value + remaining_planned[i - last_actual_index - 1] * 0.98, 0)
            forecast_pessimistic[i] = round(last_actual_value + remaining_planned[i - last_actual_index - 1] * 1.05, 0)
    else:
        # Generate placeholder S-curve data for other projects
        # Similar logic but with different values
        planned_curve = [i**2 * 30000 for i in range(1, 25)]
        
        # Generate actual curve (follows planned with some variance)
        actual_curve = []
        for i in range(len(planned_curve)):
            if i < 5:  # We have 5 months of actual data
                variance = random.uniform(0.95, 1.05)
                actual_curve.append(round(planned_curve[i] * variance, 0))
            else:
                actual_curve.append(None)
        
        # Create forecast curves
        forecast_base = actual_curve.copy()
        forecast_optimistic = actual_curve.copy()
        forecast_pessimistic = actual_curve.copy()
        
        # Fill in forecasts
        last_actual_index = 4  # 0-based index for month 5
        last_actual_value = actual_curve[last_actual_index]
        remaining_planned = [planned_curve[i] - planned_curve[last_actual_index] for i in range(last_actual_index + 1, len(planned_curve))]
        
        for i in range(last_actual_index + 1, len(planned_curve)):
            forecast_base[i] = round(last_actual_value + remaining_planned[i - last_actual_index - 1] * 1.0, 0)
            forecast_optimistic[i] = round(last_actual_value + remaining_planned[i - last_actual_index - 1] * 0.95, 0)
            forecast_pessimistic[i] = round(last_actual_value + remaining_planned[i - last_actual_index - 1] * 1.05, 0)
    
    # Create dataframe for S-curve
    scurve_data = pd.DataFrame({
        'Month': months,
        'Planned': planned_curve,
        'Actual': actual_curve,
        'Forecast (Base)': forecast_base,
        'Forecast (Optimistic)': forecast_optimistic,
        'Forecast (Pessimistic)': forecast_pessimistic
    })
    
    # Select which forecast to show
    forecast_option = st.radio(
        "Forecast Scenario",
        ["Base Case", "Optimistic", "Pessimistic", "All Scenarios"],
        key="scurve_forecast"
    )
    
    # Prepare chart data based on selection
    if forecast_option == "Base Case":
        chart_data = scurve_data[['Month', 'Planned', 'Actual', 'Forecast (Base)']].copy()
    elif forecast_option == "Optimistic":
        chart_data = scurve_data[['Month', 'Planned', 'Actual', 'Forecast (Optimistic)']].copy()
    elif forecast_option == "Pessimistic":
        chart_data = scurve_data[['Month', 'Planned', 'Actual', 'Forecast (Pessimistic)']].copy()
    else:
        chart_data = scurve_data.copy()
    
    # Set month as index for the chart
    chart_pivot = chart_data.set_index('Month')
    
    # Format data for better display (divide by 1,000,000 for millions)
    chart_pivot_formatted = chart_pivot / 1000000
    
    # Display the line chart
    st.line_chart(chart_pivot_formatted)
    
    # Add y-axis label
    st.write("*Y-axis shows values in millions ($)*")
    
    # S-curve explanation
    st.subheader("S-Curve Analysis Methodology")
    
    st.write("""
    S-curves visualize the cumulative cost over the project duration. They typically follow an S-shape because:
    
    1. **Initial Phase**: Slow expenditure as the project mobilizes
    2. **Middle Phase**: Rapid expenditure during peak construction
    3. **Final Phase**: Tapering expenditure as the project nears completion
    
    Comparing actual expenditure to the planned S-curve provides early warnings of cost overruns or schedule delays.
    """)

def render_reporting():
    """Render cost reporting tools."""
    st.subheader("Cost Reporting")
    
    # Report type selector
    report_type = st.selectbox(
        "Report Type",
        ["Monthly Cost Report", "Cost Performance Index (CPI)", "Cash Flow Forecast", "Cost Distribution"]
    )
    
    # Project selector
    project = st.selectbox(
        "Select Project",
        ["All Projects", "Highland Tower", "City Center", "Riverside Apartments", "Metro Office Complex"],
        key="report_project"
    )
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("From Date", datetime.now() - timedelta(days=90), key="report_from")
    with col2:
        st.date_input("To Date", datetime.now(), key="report_to")
    
    # Report format options
    format_options = st.multiselect(
        "Export Format",
        ["PDF", "Excel", "CSV"],
        default=["PDF"]
    )
    
    # Generate Report button
    if st.button("Generate Report"):
        st.success(f"{report_type} for {project} has been generated successfully!")
        
        # Show sample report preview
        st.subheader("Report Preview")
        
        if report_type == "Monthly Cost Report":
            render_monthly_cost_report(project)
        elif report_type == "Cost Performance Index (CPI)":
            render_cpi_report(project)
        elif report_type == "Cash Flow Forecast":
            render_cash_flow_report(project)
        else:
            render_cost_distribution_report(project)

def render_monthly_cost_report(project):
    """Render a sample monthly cost report."""
    st.write(f"**{project} - Monthly Cost Report - May 2025**")
    
    # Executive summary
    st.write("### Executive Summary")
    st.write("""
    This report summarizes the cost performance for the project as of May 15, 2025. 
    The project is currently tracking within 2.6% of the overall budget. Key concerns include:
    
    - Concrete costs are trending 2.7% over budget due to material price increases
    - MEP systems showing potential cost overruns of approximately $100,000
    - Change orders have been submitted that may impact the final cost
    
    Overall, the cost performance remains satisfactory with proper controls in place.
    """)
    
    # Cost summary table
    st.write("### Cost Summary")
    
    cost_summary = [
        {"Category": "Original Contract", "Amount": "$15,500,000"},
        {"Category": "Approved Change Orders", "Amount": "$320,000"},
        {"Category": "Current Contract", "Amount": "$15,820,000"},
        {"Category": "Costs to Date", "Amount": "$6,750,000"},
        {"Category": "Committed Costs", "Amount": "$8,450,000"},
        {"Category": "Forecasted Uncommitted", "Amount": "$700,000"},
        {"Category": "Total Projected Costs", "Amount": "$15,900,000"},
        {"Category": "Variance", "Amount": "-$80,000 (-0.5%)"}
    ]
    
    st.table(pd.DataFrame(cost_summary))
    
    # Monthly cost charts
    st.write("### Monthly Cost Performance")
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Monthly Cost Distribution**")
        monthly_costs = {
            'Category': ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'General Conditions'],
            'Amount': [310000, 425000, 150000, 510000, 95000]
        }
        monthly_df = pd.DataFrame(monthly_costs)
        st.bar_chart(monthly_df.set_index('Category'))
    
    with col2:
        st.write("**Budget vs. Actual (Cumulative)**")
        cumulative = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'Budget': [1550000, 3100000, 4650000, 6200000, 7750000],
            'Actual': [1590000, 3200000, 4820000, 6400000, 6750000]
        })
        st.line_chart(cumulative.set_index('Month'))

def render_cpi_report(project):
    """Render a sample CPI report."""
    st.write(f"**{project} - Cost Performance Index (CPI) Report - May 2025**")
    
    # CPI explanation
    st.write("### Cost Performance Index (CPI)")
    st.write("""
    The Cost Performance Index (CPI) is a measure of cost efficiency. It is calculated as:
    
    **CPI = Earned Value (EV) / Actual Cost (AC)**
    
    - CPI > 1.0: Project is under budget (good)
    - CPI = 1.0: Project is on budget
    - CPI < 1.0: Project is over budget (concerning)
    """)
    
    # CPI table
    cpi_data = [
        {"Work Package": "Foundation Package", "Budget": "$1,240,000", "Earned Value": "$1,240,000", "Actual Cost": "$1,260,000", "CPI": "0.98"},
        {"Work Package": "Structural Frame (Lower)", "Budget": "$2,480,000", "Earned Value": "$2,480,000", "Actual Cost": "$2,450,000", "CPI": "1.01"},
        {"Work Package": "Structural Frame (Upper)", "Budget": "$2,480,000", "Earned Value": "$1,240,000", "Actual Cost": "$1,280,000", "CPI": "0.97"},
        {"Work Package": "Exterior Envelope (Lower)", "Budget": "$1,550,000", "Earned Value": "$1,085,000", "Actual Cost": "$1,060,000", "CPI": "1.02"},
        {"Work Package": "MEP Rough-in (Lower)", "Budget": "$1,860,000", "Earned Value": "$1,302,000", "Actual Cost": "$1,350,000", "CPI": "0.96"},
        {"Work Package": "Interior Finishes (Lower)", "Budget": "$1,240,000", "Earned Value": "$372,000", "Actual Cost": "$380,000", "CPI": "0.98"},
        {"Work Package": "Overall Project", "Budget": "$15,500,000", "Earned Value": "$7,719,000", "Actual Cost": "$7,780,000", "CPI": "0.99"}
    ]
    
    # Convert to DataFrame
    cpi_df = pd.DataFrame(cpi_data)
    
    # Add CPI styling
    def cpi_color(val):
        try:
            cpi_val = float(val)
            if cpi_val >= 1.0:
                return 'background-color: #d1fae5; color: #064e3b'
            elif cpi_val >= 0.95:
                return 'background-color: #fef3c7; color: #78350f'
            else:
                return 'background-color: #fee2e2; color: #7f1d1d'
        except:
            return ''
    
    # Apply styling
    styled_cpi_df = cpi_df.style.applymap(cpi_color, subset=['CPI'])
    
    # Display the dataframe
    st.dataframe(styled_cpi_df, use_container_width=True)
    
    # CPI trend chart
    st.write("### CPI Trend (Last 6 Months)")
    
    cpi_trend = pd.DataFrame({
        'Month': ['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'CPI': [1.02, 1.01, 1.00, 0.99, 0.98, 0.99]
    })
    
    st.line_chart(cpi_trend.set_index('Month'))
    
    # CPI analysis
    st.write("### CPI Analysis")
    st.write("""
    The overall project CPI of 0.99 indicates that the project is performing at 99% cost efficiency - slightly over budget but within acceptable ranges.
    
    Key trends:
    
    - CPI has been gradually declining over the past 6 months, suggesting increasing cost pressures
    - MEP Rough-in work package has the lowest CPI (0.96) and should be monitored closely
    - Exterior Envelope work is performing well with a CPI of 1.02
    
    Recommended actions:
    
    1. Conduct detailed review of MEP costs and subcontractor performance
    2. Implement additional cost controls for the upper structural frame package
    3. Continue monitoring material cost escalation and potential impacts
    """)

def render_cash_flow_report(project):
    """Render a sample cash flow report."""
    st.write(f"**{project} - Cash Flow Forecast Report - May 2025**")
    
    # Cash flow explanation
    st.write("### Cash Flow Forecast")
    st.write("""
    This report presents the projected cash flow for the project through completion. The forecast is based on:
    
    - Actual costs incurred to date
    - Current commitments and procurement schedules
    - Project schedule and planned activities
    - Anticipated change orders and contingencies
    
    Cash flow projections help ensure adequate funding is available throughout the project lifecycle.
    """)
    
    # Cash flow chart
    st.write("### Cash Flow Projection")
    
    # Generate sample cash flow data for 24 months
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
              'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    if project == "Highland Tower" or project == "All Projects":
        # Monthly cash flow (in thousands)
        monthly_flow = [550, 600, 620, 650, 680, 720, 780, 850, 900, 950, 980, 1000,
                        950, 880, 820, 750, 680, 620, 580, 520, 450, 350, 250, 120]
        
        # Cumulative cash flow
        cumulative_flow = []
        running_total = 0
        for monthly in monthly_flow:
            running_total += monthly
            cumulative_flow.append(running_total)
    else:
        # Placeholder data for other projects
        monthly_flow = [300, 320, 350, 380, 420, 450, 480, 510, 540, 570, 600, 620,
                        580, 540, 500, 460, 420, 380, 340, 300, 260, 220, 180, 100]
        
        # Cumulative cash flow
        cumulative_flow = []
        running_total = 0
        for monthly in monthly_flow:
            running_total += monthly
            cumulative_flow.append(running_total)
    
    # Create dataframe
    cash_flow_data = pd.DataFrame({
        'Month': months,
        'Monthly ($K)': monthly_flow,
        'Cumulative ($M)': [round(c / 1000, 2) for c in cumulative_flow]
    })
    
    # Mark actual vs projected
    cash_flow_data['Type'] = ['Actual' if i < 5 else 'Projected' for i in range(len(months))]
    
    # Display table
    st.dataframe(cash_flow_data, use_container_width=True)
    
    # Display chart
    st.line_chart(cash_flow_data.set_index('Month')['Cumulative ($M)'])
    
    # Monthly burn rate chart
    st.write("### Monthly Expenditure")
    st.bar_chart(cash_flow_data.set_index('Month')['Monthly ($K)'])
    
    # Cash flow analysis
    st.write("### Cash Flow Analysis")
    st.write("""
    Key observations:
    
    - The project is expected to reach peak monthly expenditure of $1,000K in December 2025
    - Total forecasted project cost is $15.9M
    - Current funding drawdown is on track with projections
    - Q3 2025 will see the highest overall expenditure and should be planned for accordingly
    
    Funding recommendations:
    
    1. Ensure capital reserves of at least $4M are available for Q3-Q4 2025
    2. Consider accelerating progress payments to subcontractors in Q2 to better manage Q3 cash flow
    3. Verify that contingency funds remain adequate for potential cost escalations in later project phases
    """)

def render_cost_distribution_report(project):
    """Render a sample cost distribution report."""
    st.write(f"**{project} - Cost Distribution Report - May 2025**")
    
    # Cost distribution explanation
    st.write("### Cost Distribution Analysis")
    st.write("""
    This report analyzes how project costs are distributed across various categories, work packages, 
    and subcontractors. Understanding cost distribution helps identify areas of financial risk and 
    opportunities for cost optimization.
    """)
    
    # Distribution by cost category
    st.write("### Distribution by Cost Category")
    
    if project == "Highland Tower" or project == "All Projects":
        categories = {
            'Category': ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'General Conditions', 'Overhead & Profit'],
            'Amount ($M)': [4.65, 3.88, 1.55, 3.10, 1.55, 1.17],
            'Percentage': ['30%', '25%', '10%', '20%', '10%', '7.5%']
        }
    else:
        # Placeholder data for other projects
        categories = {
            'Category': ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'General Conditions', 'Overhead & Profit'],
            'Amount ($M)': [3.0, 2.5, 1.0, 2.0, 1.0, 0.75],
            'Percentage': ['30%', '25%', '10%', '20%', '10%', '7.5%']
        }
    
    categories_df = pd.DataFrame(categories)
    st.dataframe(categories_df, use_container_width=True)
    
    # Create pie chart data
    chart_data = pd.DataFrame({
        'Category': categories['Category'],
        'Amount': [float(amt) for amt in categories['Amount ($M)']]
    })
    
    # Column layout for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Cost Category Distribution**")
        st.bar_chart(chart_data.set_index('Category')['Amount'])
    
    with col2:
        st.write("**Distribution by CSI Division**")
        if project == "Highland Tower" or project == "All Projects":
            csi_data = {
                'Division': ['Div 01-09 (Architectural)', 'Div 10-14 (Finishes)', 'Div 21-23 (Mechanical)', 
                            'Div 26-28 (Electrical)', 'Div 31-33 (Sitework)'],
                'Amount': [6.2, 2.3, 3.1, 2.3, 1.6]
            }
        else:
            csi_data = {
                'Division': ['Div 01-09 (Architectural)', 'Div 10-14 (Finishes)', 'Div 21-23 (Mechanical)', 
                            'Div 26-28 (Electrical)', 'Div 31-33 (Sitework)'],
                'Amount': [4.0, 1.5, 2.0, 1.5, 1.0]
            }
        
        csi_df = pd.DataFrame(csi_data)
        st.bar_chart(csi_df.set_index('Division')['Amount'])
    
    # Top subcontractors
    st.write("### Top Subcontractors by Contract Value")
    
    if project == "Highland Tower" or project == "All Projects":
        subcontractors = [
            {"Subcontractor": "ABC Concrete, Inc.", "Trade": "Concrete", "Contract": "$1,850,000", "Percent": "11.9%"},
            {"Subcontractor": "Steel Experts LLC", "Trade": "Steel", "Contract": "$2,100,000", "Percent": "13.5%"},
            {"Subcontractor": "Modern Electrical Co.", "Trade": "Electrical", "Contract": "$1,750,000", "Percent": "11.3%"},
            {"Subcontractor": "Quality Plumbing Services", "Trade": "Plumbing", "Contract": "$980,000", "Percent": "6.3%"},
            {"Subcontractor": "Premier HVAC Systems", "Trade": "HVAC", "Contract": "$1,240,000", "Percent": "8.0%"}
        ]
    else:
        # Placeholder data for other projects
        subcontractors = [
            {"Subcontractor": "General Contracting Inc.", "Trade": "General", "Contract": "$1,200,000", "Percent": "12.0%"},
            {"Subcontractor": "Steel City LLC", "Trade": "Steel", "Contract": "$950,000", "Percent": "9.5%"},
            {"Subcontractor": "Electrical Pros Co.", "Trade": "Electrical", "Contract": "$850,000", "Percent": "8.5%"},
            {"Subcontractor": "Plumbing Masters", "Trade": "Plumbing", "Contract": "$700,000", "Percent": "7.0%"},
            {"Subcontractor": "HVAC Experts", "Trade": "HVAC", "Contract": "$600,000", "Percent": "6.0%"}
        ]
    
    st.dataframe(pd.DataFrame(subcontractors), use_container_width=True)
    
    # Cost distribution analysis
    st.write("### Cost Distribution Analysis")
    st.write("""
    Key observations:
    
    - Labor and materials account for 55% of total project costs
    - MEP trades (mechanical, electrical, plumbing) collectively represent 25.6% of the budget
    - The top 5 subcontractors account for 51.0% of total project costs
    - General conditions are tracking at 10% of overall costs, as planned
    
    Recommendations:
    
    1. Monitor concrete and structural steel costs closely as they represent 25.4% of the budget
    2. Evaluate potential for bulk purchasing of materials across similar upcoming projects
    3. Consider value engineering options for mechanical systems which are trending higher than expected
    4. Review subcontractor performance monthly with focus on the top 5 contracts
    """)