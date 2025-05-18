"""
Analytics Module for gcPanel.

This module provides advanced data visualization, predictive analytics,
and custom reporting capabilities for construction project management.
"""

import streamlit as st
from modules.analytics.visualizations import dashboard
from modules.analytics.predictive import timeline_predictor, budget_predictor
from modules.analytics.reporting import report_generator

def render_analytics():
    """Render the analytics module interface."""
    st.title("Project Analytics")
    
    # Create tabs for different analytics sections
    tabs = st.tabs([
        "Dashboard", 
        "Predictive Analytics", 
        "Custom Reports"
    ])
    
    # Dashboard tab
    with tabs[0]:
        dashboard.render_analytics_dashboard()
    
    # Predictive Analytics tab
    with tabs[1]:
        render_predictive_analytics()
    
    # Custom Reports tab
    with tabs[2]:
        report_generator.render_report_generator()

def render_predictive_analytics():
    """Render the predictive analytics section."""
    st.header("Predictive Analytics")
    
    # Add subheader with description
    st.subheader("Project Timeline and Budget Predictions")
    st.markdown("""
    Predictive analytics uses historical project data and statistical models to forecast:
    * Project completion dates
    * Budget overruns or savings
    * Risk factors and potential delays
    
    Select a prediction type below to generate forecasts for your project.
    """)
    
    # Create columns for timeline and budget predictions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Timeline Prediction")
        st.markdown("Forecast project completion dates and milestone timelines")
        if st.button("Analyze Timeline", key="analyze_timeline"):
            timeline_predictor.render_timeline_prediction()
    
    with col2:
        st.markdown("### Budget Prediction")
        st.markdown("Forecast project costs and identify budget risk areas")
        if st.button("Analyze Budget", key="analyze_budget"):
            budget_predictor.render_budget_prediction()