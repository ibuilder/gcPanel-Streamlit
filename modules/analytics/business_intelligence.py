"""
Business Intelligence & Analytics Dashboard for gcPanel Construction Platform

Advanced analytics, reporting, and insights for construction project management
with real-time KPIs, predictive analytics, and executive dashboards.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Optional

def render_business_intelligence():
    """Render the comprehensive business intelligence dashboard."""
    
    st.title("📊 Business Intelligence & Analytics")
    st.markdown("### Executive Construction Management Dashboard")
    
    # Dashboard navigation
    dashboard_tabs = st.tabs([
        "🎯 Executive Overview",
        "📈 Project Performance", 
        "💰 Financial Analytics",
        "🦺 Safety Intelligence",
        "⚡ Productivity Metrics",
        "📋 Custom Reports"
    ])
    
    with dashboard_tabs[0]:
        render_executive_overview()
    
    with dashboard_tabs[1]:
        render_project_performance()
    
    with dashboard_tabs[2]:
        render_financial_analytics()
    
    with dashboard_tabs[3]:
        render_safety_intelligence()
    
    with dashboard_tabs[4]:
        render_productivity_metrics()
    
    with dashboard_tabs[5]:
        render_custom_reports()

def render_executive_overview():
    """Render executive-level KPI dashboard."""
    
    st.markdown("#### 🎯 Key Performance Indicators")
    
    # Top-level KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Portfolio Value",
            "$125.5M",
            delta="$8.2M vs last quarter",
            help="Total value of active construction projects"
        )
    
    with col2:
        st.metric(
            "Projects On Schedule",
            "80%",
            delta="5% improvement",
            help="Percentage of projects meeting timeline targets"
        )
    
    with col3:
        st.metric(
            "Average Profit Margin",
            "12.8%",
            delta="1.2% increase",
            help="Overall profit margin across all projects"
        )
    
    with col4:
        st.metric(
            "Safety Score",
            "94.2",
            delta="2.1 point improvement",
            help="Composite safety performance score"
        )
    
    with col5:
        st.metric(
            "Client Satisfaction",
            "4.6/5.0",
            delta="0.3 improvement",
            help="Average client satisfaction rating"
        )
    
    st.markdown("---")
    
    # Executive summary charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Portfolio performance over time
        portfolio_data = create_portfolio_timeline_data()
        fig_portfolio = px.line(
            portfolio_data,
            x='date',
            y='portfolio_value',
            title='📈 Portfolio Value Trend (Last 12 Months)',
            labels={'portfolio_value': 'Portfolio Value ($M)', 'date': 'Date'}
        )
        fig_portfolio.update_layout(height=400)
        st.plotly_chart(fig_portfolio, use_container_width=True)
    
    with col2:
        # Project status distribution
        project_status_data = {
            'Status': ['On Track', 'Behind Schedule', 'Ahead of Schedule', 'On Hold'],
            'Count': [12, 3, 2, 1],
            'Value': [89.2, 18.7, 12.8, 4.8]
        }
        
        fig_status = px.pie(
            project_status_data,
            values='Count',
            names='Status',
            title='🎯 Project Status Distribution',
            color_discrete_sequence=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
        )
        fig_status.update_layout(height=400)
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Regional performance summary
    st.markdown("#### 🌍 Regional Performance Summary")
    
    regional_data = pd.DataFrame({
        'Region': ['Northeast', 'Southeast', 'Midwest', 'West Coast'],
        'Active Projects': [8, 5, 4, 1],
        'Total Value ($M)': [78.2, 32.1, 12.8, 2.4],
        'Avg Margin (%)': [14.2, 11.8, 13.5, 9.2],
        'Safety Score': [96.1, 92.3, 94.8, 91.2]
    })
    
    st.dataframe(
        regional_data.style.format({
            'Total Value ($M)': '${:.1f}M',
            'Avg Margin (%)': '{:.1f}%',
            'Safety Score': '{:.1f}'
        }),
        use_container_width=True
    )

def render_project_performance():
    """Render detailed project performance analytics."""
    
    st.markdown("#### 📈 Project Performance Analytics")
    
    # Project selector
    projects = [
        "Highland Tower Development", "Maple Commons", "Oak Street Condos", 
        "Pine Valley Homes", "Cedar Heights", "All Projects"
    ]
    selected_project = st.selectbox("Select Project for Analysis", projects, index=5)
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Schedule Performance", "96%", delta="4% vs baseline")
    
    with col2:
        st.metric("Cost Performance", "108%", delta="-8% over budget")
    
    with col3:
        st.metric("Quality Score", "92.5", delta="1.5 improvement")
    
    with col4:
        st.metric("Resource Utilization", "87%", delta="3% increase")
    
    st.markdown("---")
    
    # Project timeline analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Schedule variance chart
        schedule_data = create_schedule_variance_data()
        fig_schedule = px.bar(
            schedule_data,
            x='project',
            y='variance_days',
            color='status',
            title='📅 Schedule Variance by Project',
            labels={'variance_days': 'Days (+ Ahead / - Behind)', 'project': 'Project'},
            color_discrete_map={
                'ahead': '#28A745',
                'on_track': '#17A2B8', 
                'behind': '#DC3545'
            }
        )
        st.plotly_chart(fig_schedule, use_container_width=True)
    
    with col2:
        # Cost performance index trend
        cpi_data = create_cost_performance_data()
        fig_cpi = px.line(
            cpi_data,
            x='month',
            y='cpi',
            title='💰 Cost Performance Index Trend',
            labels={'cpi': 'Cost Performance Index', 'month': 'Month'}
        )
        fig_cpi.add_hline(y=1.0, line_dash="dash", line_color="red", 
                         annotation_text="Budget Baseline")
        st.plotly_chart(fig_cpi, use_container_width=True)
    
    # Detailed project breakdown
    st.markdown("#### 🔍 Detailed Project Analysis")
    
    project_details = create_project_details_data()
    
    # Format the dataframe for better display
    formatted_df = project_details.style.format({
        'Budget ($M)': '${:.1f}M',
        'Spent ($M)': '${:.1f}M',
        'Progress (%)': '{:.1f}%',
        'Schedule Variance': '{:+d} days',
        'Cost Variance (%)': '{:+.1f}%'
    }).background_gradient(subset=['Progress (%)'], cmap='RdYlGn', vmin=0, vmax=100)
    
    st.dataframe(formatted_df, use_container_width=True)

def render_financial_analytics():
    """Render comprehensive financial analytics."""
    
    st.markdown("#### 💰 Financial Performance Analytics")
    
    # Financial overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue YTD", "$89.2M", delta="$12.8M vs last year")
    
    with col2:
        st.metric("Gross Profit Margin", "28.5%", delta="2.3% improvement")
    
    with col3:
        st.metric("Operating Cash Flow", "$8.7M", delta="$1.2M positive")
    
    with col4:
        st.metric("Outstanding AR", "$15.3M", delta="-$2.1M improvement")
    
    st.markdown("---")
    
    # Financial trend analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue and profit trend
        financial_data = create_financial_trend_data()
        
        fig_financial = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Monthly Revenue', 'Monthly Profit'),
            shared_xaxes=True,
            vertical_spacing=0.1
        )
        
        fig_financial.add_trace(
            go.Scatter(x=financial_data['month'], y=financial_data['revenue'],
                      name='Revenue', line=dict(color='#2E86AB')),
            row=1, col=1
        )
        
        fig_financial.add_trace(
            go.Scatter(x=financial_data['month'], y=financial_data['profit'],
                      name='Profit', line=dict(color='#28A745')),
            row=2, col=1
        )
        
        fig_financial.update_layout(
            title='📊 Financial Performance Trend',
            height=500
        )
        
        st.plotly_chart(fig_financial, use_container_width=True)
    
    with col2:
        # Cash flow analysis
        cashflow_data = create_cashflow_data()
        
        fig_cashflow = go.Figure()
        
        fig_cashflow.add_trace(go.Bar(
            x=cashflow_data['month'],
            y=cashflow_data['inflow'],
            name='Cash Inflow',
            marker_color='#28A745'
        ))
        
        fig_cashflow.add_trace(go.Bar(
            x=cashflow_data['month'],
            y=[-x for x in cashflow_data['outflow']],
            name='Cash Outflow',
            marker_color='#DC3545'
        ))
        
        fig_cashflow.update_layout(
            title='💵 Cash Flow Analysis',
            yaxis_title='Cash Flow ($M)',
            barmode='relative',
            height=500
        )
        
        st.plotly_chart(fig_cashflow, use_container_width=True)
    
    # Accounts receivable aging
    st.markdown("#### 📋 Accounts Receivable Aging")
    
    ar_data = pd.DataFrame({
        'Client': ['Highland Properties LLC', 'Maple Development Corp', 'Oak Street Partners', 'Pine Valley Holdings'],
        'Current': [2.5, 1.8, 0.9, 0.3],
        '1-30 Days': [1.2, 0.5, 0.0, 0.8],
        '31-60 Days': [0.8, 0.0, 0.2, 0.0],
        '61-90 Days': [0.0, 0.3, 0.0, 0.0],
        '90+ Days': [0.0, 0.0, 0.1, 0.0],
        'Total Outstanding': [4.5, 2.6, 1.2, 1.1]
    })
    
    st.dataframe(
        ar_data.style.format({
            'Current': '${:.1f}M',
            '1-30 Days': '${:.1f}M',
            '31-60 Days': '${:.1f}M', 
            '61-90 Days': '${:.1f}M',
            '90+ Days': '${:.1f}M',
            'Total Outstanding': '${:.1f}M'
        }),
        use_container_width=True
    )

def render_safety_intelligence():
    """Render safety analytics and intelligence."""
    
    st.markdown("#### 🦺 Safety Performance Intelligence")
    
    # Safety KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Days Without Incident", "47", delta="12 days improvement")
    
    with col2:
        st.metric("OSHA Recordable Rate", "2.1", delta="-0.8 improvement")
    
    with col3:
        st.metric("Training Compliance", "96.8%", delta="1.2% increase")
    
    with col4:
        st.metric("Safety Audit Score", "94.2", delta="2.1 improvement")
    
    st.markdown("---")
    
    # Safety trend analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Incident trend
        incident_data = create_safety_incident_data()
        fig_incidents = px.line(
            incident_data,
            x='month',
            y='incidents',
            title='📉 Safety Incident Trend',
            labels={'incidents': 'Number of Incidents', 'month': 'Month'}
        )
        fig_incidents.update_traces(line_color='#DC3545')
        st.plotly_chart(fig_incidents, use_container_width=True)
    
    with col2:
        # Training completion by category
        training_data = pd.DataFrame({
            'Category': ['Fall Protection', 'Equipment Safety', 'Hazmat', 'First Aid', 'Emergency Response'],
            'Completion Rate': [98.2, 96.5, 94.8, 92.1, 89.3]
        })
        
        fig_training = px.bar(
            training_data,
            x='Category',
            y='Completion Rate',
            title='📚 Training Completion Rates',
            color='Completion Rate',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig_training, use_container_width=True)
    
    # Safety incident breakdown
    st.markdown("#### 🔍 Incident Analysis")
    
    incident_breakdown = pd.DataFrame({
        'Incident Type': ['Near Miss', 'First Aid', 'Medical Treatment', 'Lost Time', 'Property Damage'],
        'This Month': [8, 3, 1, 0, 2],
        'Last Month': [12, 5, 2, 1, 1],
        'YTD Total': [89, 34, 12, 3, 15],
        'Severity Score': [1, 2, 4, 8, 3]
    })
    
    st.dataframe(incident_breakdown, use_container_width=True)

def render_productivity_metrics():
    """Render productivity and efficiency analytics."""
    
    st.markdown("#### ⚡ Productivity & Efficiency Metrics")
    
    # Productivity KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Labor Productivity", "87%", delta="5% improvement")
    
    with col2:
        st.metric("Equipment Utilization", "74%", delta="2% increase")
    
    with col3:
        st.metric("Material Efficiency", "96%", delta="1% improvement")
    
    with col4:
        st.metric("Daily Report Compliance", "94%", delta="3% increase")
    
    st.markdown("---")
    
    # Productivity analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Labor productivity by trade
        labor_data = pd.DataFrame({
            'Trade': ['Concrete', 'Framing', 'Electrical', 'Plumbing', 'HVAC', 'Finishes'],
            'Productivity Index': [92, 88, 85, 82, 79, 87],
            'Target': [90, 85, 85, 80, 80, 85]
        })
        
        fig_labor = px.bar(
            labor_data,
            x='Trade',
            y=['Productivity Index', 'Target'],
            title='👷 Labor Productivity by Trade',
            barmode='group'
        )
        st.plotly_chart(fig_labor, use_container_width=True)
    
    with col2:
        # Equipment utilization
        equipment_data = create_equipment_utilization_data()
        fig_equipment = px.scatter(
            equipment_data,
            x='hours_scheduled',
            y='hours_utilized',
            size='efficiency_score',
            hover_name='equipment_type',
            title='🚛 Equipment Utilization Analysis',
            labels={
                'hours_scheduled': 'Scheduled Hours',
                'hours_utilized': 'Utilized Hours'
            }
        )
        # Add diagonal line for 100% utilization
        fig_equipment.add_shape(
            type="line",
            x0=0, y0=0, x1=200, y1=200,
            line=dict(color="red", dash="dash")
        )
        st.plotly_chart(fig_equipment, use_container_width=True)

def render_custom_reports():
    """Render custom reporting interface."""
    
    st.markdown("#### 📋 Custom Report Builder")
    
    # Report configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Report Parameters")
        
        report_type = st.selectbox(
            "Report Type",
            ["Executive Summary", "Project Performance", "Financial Analysis", 
             "Safety Report", "Productivity Analysis", "Custom Query"]
        )
        
        date_range = st.date_input(
            "Date Range",
            value=[datetime.now() - timedelta(days=30), datetime.now()],
            help="Select start and end dates for the report"
        )
        
        projects_filter = st.multiselect(
            "Projects",
            ["Highland Tower", "Maple Commons", "Oak Street Condos", "Pine Valley Homes"],
            default=["Highland Tower", "Maple Commons"]
        )
    
    with col2:
        st.markdown("##### Output Options")
        
        output_format = st.selectbox(
            "Output Format",
            ["PDF Report", "Excel Workbook", "PowerPoint Presentation", "CSV Data"]
        )
        
        include_charts = st.checkbox("Include Charts and Visualizations", value=True)
        include_raw_data = st.checkbox("Include Raw Data Tables", value=False)
        
        report_frequency = st.selectbox(
            "Schedule (Optional)",
            ["One-time", "Daily", "Weekly", "Monthly", "Quarterly"]
        )
    
    # Generate report button
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("📊 Generate Custom Report", type="primary", use_container_width=True):
            with st.spinner("Generating custom report..."):
                # Simulate report generation
                st.success("✅ Custom report generated successfully!")
                st.download_button(
                    label=f"📥 Download {report_type} Report",
                    data="Sample report data would be generated here",
                    file_name=f"{report_type.lower().replace(' ', '_')}_report.pdf",
                    mime="application/pdf"
                )

# Helper functions to create sample data
def create_portfolio_timeline_data():
    """Create portfolio value timeline data."""
    dates = pd.date_range(start='2024-01-01', end='2025-01-01', freq='M')
    values = [98.2, 102.5, 108.7, 115.2, 118.9, 122.1, 119.8, 123.4, 125.1, 127.8, 124.3, 125.5, 125.5]
    return pd.DataFrame({'date': dates, 'portfolio_value': values[:len(dates)]})

def create_schedule_variance_data():
    """Create schedule variance data."""
    return pd.DataFrame({
        'project': ['Highland Tower', 'Maple Commons', 'Oak Street', 'Pine Valley', 'Cedar Heights'],
        'variance_days': [-5, 12, -2, 3, -8],
        'status': ['ahead', 'behind', 'ahead', 'behind', 'ahead']
    })

def create_cost_performance_data():
    """Create cost performance index data."""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    cpi_values = [1.05, 1.02, 0.98, 1.08, 1.12, 1.06, 1.04, 1.09, 1.03, 1.07, 1.05, 1.08]
    return pd.DataFrame({'month': months, 'cpi': cpi_values})

def create_project_details_data():
    """Create detailed project data."""
    return pd.DataFrame({
        'Project': ['Highland Tower', 'Maple Commons', 'Oak Street Condos', 'Pine Valley Homes', 'Cedar Heights'],
        'Budget ($M)': [45.5, 23.2, 18.7, 12.3, 8.9],
        'Spent ($M)': [29.6, 11.2, 14.8, 2.7, 8.1],
        'Progress (%)': [68, 45, 82, 23, 91],
        'Schedule Variance': [-5, 12, -2, 3, -8],
        'Cost Variance (%)': [-2.3, 5.1, -1.8, 0.8, -0.5]
    })

def create_financial_trend_data():
    """Create financial trend data."""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    revenue = [6.2, 7.1, 8.5, 7.8, 9.2, 8.7, 9.5, 8.9, 7.6, 8.3, 7.9, 8.1]
    profit = [1.8, 2.1, 2.4, 2.2, 2.6, 2.5, 2.7, 2.5, 2.2, 2.4, 2.3, 2.3]
    return pd.DataFrame({'month': months, 'revenue': revenue, 'profit': profit})

def create_cashflow_data():
    """Create cash flow data."""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    inflow = [8.2, 6.5, 9.1, 7.8, 8.9, 7.2]
    outflow = [7.1, 6.8, 8.2, 7.5, 8.1, 6.9]
    return pd.DataFrame({'month': months, 'inflow': inflow, 'outflow': outflow})

def create_safety_incident_data():
    """Create safety incident trend data."""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    incidents = [8, 6, 4, 7, 3, 5, 2, 4, 3, 2, 1, 2]
    return pd.DataFrame({'month': months, 'incidents': incidents})

def create_equipment_utilization_data():
    """Create equipment utilization data."""
    return pd.DataFrame({
        'equipment_type': ['Excavator', 'Crane', 'Concrete Pump', 'Bulldozer', 'Loader', 'Dump Truck'],
        'hours_scheduled': [160, 180, 120, 140, 150, 200],
        'hours_utilized': [142, 167, 108, 125, 138, 185],
        'efficiency_score': [89, 93, 90, 89, 92, 93]
    })

def render():
    """Main render function for business intelligence module."""
    render_business_intelligence()