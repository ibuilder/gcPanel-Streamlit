"""
AI Assistant module for gcPanel.

This module provides AI-powered features for construction professionals,
including document analysis, smart search, predictive insights, and
natural language processing for project data.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json

def render_ai_assistant():
    """Render the AI assistant dashboard with various AI-powered tools."""
    st.title("AI Assistant")
    
    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        st.warning("⚠️ Anthropic API key not found. Some AI features may be limited.")
        st.info("Please add your Anthropic API key in the settings to enable all AI features.")
    
    # Sidebar with AI tool selection
    with st.sidebar:
        st.subheader("AI Tools")
        selected_tool = st.radio(
            "Select Tool",
            ["Document Analysis", "Project Insights", "Risk Assessment", 
             "Schedule Optimization", "Cost Forecasting"]
        )
    
    # Render the selected AI tool
    if selected_tool == "Document Analysis":
        render_document_analysis()
    elif selected_tool == "Project Insights":
        render_project_insights()
    elif selected_tool == "Risk Assessment":
        render_risk_assessment()
    elif selected_tool == "Schedule Optimization":
        render_schedule_optimization()
    elif selected_tool == "Cost Forecasting":
        render_cost_forecasting()

def render_document_analysis():
    """Render document analysis tool for extracting insights from construction documents."""
    st.header("Document Analysis")
    st.markdown("""
    Upload construction documents to extract key information, summarize content,
    and identify important elements like deadlines, requirements, and risks.
    """)
    
    # Document upload section
    uploaded_file = st.file_uploader(
        "Upload a document (PDF, Word, or Text)", 
        type=["pdf", "docx", "txt"]
    )
    
    if uploaded_file:
        # Show analysis options
        st.subheader("Analysis Options")
        
        col1, col2 = st.columns(2)
        with col1:
            extract_dates = st.checkbox("Extract important dates", value=True)
            extract_costs = st.checkbox("Extract cost information", value=True)
            extract_requirements = st.checkbox("Extract requirements", value=True)
        
        with col2:
            extract_contacts = st.checkbox("Extract contact information", value=True)
            extract_risks = st.checkbox("Identify potential risks", value=True)
            generate_summary = st.checkbox("Generate executive summary", value=True)
        
        # Analysis button
        if st.button("Analyze Document"):
            with st.spinner("Analyzing document..."):
                # Simulate analysis (in a real app, this would use the AI API)
                st.success("Document analysis complete!")
                
                # Display results in tabs
                tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Key Elements", "Risks", "Action Items"])
                
                with tab1:
                    st.subheader("Executive Summary")
                    st.markdown("""
                    This document appears to be a **Change Order Request** for the Highland Tower project.
                    The contractor is requesting a schedule extension of 15 working days and additional 
                    compensation of $127,450 due to unforeseen subsurface conditions discovered during 
                    excavation for the foundation work. The document includes supporting evidence from 
                    geotechnical reports and outlines impacts to the critical path schedule.
                    """)
                
                with tab2:
                    st.subheader("Key Elements")
                    
                    st.markdown("##### Important Dates")
                    dates_df = pd.DataFrame({
                        "Description": ["Issue Date", "Response Required By", "Proposed Completion Extension"],
                        "Date": ["May 15, 2025", "May 29, 2025", "June 30, 2025"]
                    })
                    st.table(dates_df)
                    
                    st.markdown("##### Cost Information")
                    costs_df = pd.DataFrame({
                        "Item": ["Additional Labor", "Equipment", "Materials", "Overhead", "Total"],
                        "Amount": ["$52,300", "$35,800", "$28,450", "$10,900", "$127,450"]
                    })
                    st.table(costs_df)
                
                with tab3:
                    st.subheader("Identified Risks")
                    risks = [
                        "Schedule delay may impact subsequent trades",
                        "Additional unforeseen conditions may be discovered",
                        "Cost overrun exceeds contingency budget by approximately 12%",
                        "Potential disputes with owner over responsibility for conditions"
                    ]
                    for risk in risks:
                        st.markdown(f"- {risk}")
                
                with tab4:
                    st.subheader("Recommended Actions")
                    actions = [
                        "Verify geotechnical findings independently",
                        "Review contract clauses regarding unforeseen conditions",
                        "Evaluate impact on critical path schedule",
                        "Prepare negotiation strategy for owner meeting",
                        "Document all related communication for potential claims"
                    ]
                    for action in actions:
                        st.markdown(f"- {action}")

def render_project_insights():
    """Render project insights tool for generating intelligence from project data."""
    st.header("Project Insights")
    st.markdown("""
    Get AI-powered insights about your project performance, trends, and potential issues.
    The system analyzes your project data to identify patterns and make recommendations.
    """)
    
    # Project selection (in a real app, would be actual projects)
    project = st.selectbox(
        "Select Project",
        ["Highland Tower Development", "Riverside Commercial Complex", "Metro Transit Hub"]
    )
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=90))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # Analysis areas
    st.subheader("Analysis Areas")
    
    analysis_areas = {
        "Schedule Performance": st.checkbox("Schedule Performance", value=True),
        "Cost Management": st.checkbox("Cost Management", value=True),
        "Quality Issues": st.checkbox("Quality Issues", value=True),
        "Safety Incidents": st.checkbox("Safety Incidents", value=True),
        "Resource Utilization": st.checkbox("Resource Utilization", value=True),
        "Subcontractor Performance": st.checkbox("Subcontractor Performance", value=True)
    }
    
    # Generate insights button
    if st.button("Generate Insights"):
        with st.spinner("Analyzing project data..."):
            # Simulate insight generation (in a real app, this would use the AI API)
            st.success("Analysis complete!")
            
            # Display insights in an expandable section
            with st.expander("Schedule Performance Insights", expanded=True):
                st.markdown("""
                ### Schedule Performance Insights
                
                **Current Status: 🟠 At Risk**
                
                The project is currently **7 days behind schedule** (4% variance) with the following critical observations:
                
                - Foundation work completed 3 days later than planned due to unexpected soil conditions
                - MEP rough-in on floors 3-5 is progressing 15% slower than planned rate
                - Elevator installation has not started due to pending approvals (5 days delay)
                
                **Recommendations:**
                
                1. Increase MEP crew size by 2-3 workers to accelerate rough-in progress
                2. Expedite elevator installation approval by escalating to senior building inspector
                3. Consider weekend work for curtain wall installation to recover schedule
                
                **Predictive Alert:** If current trends continue, project completion may be delayed by approximately 12-15 working days.
                """)
            
            if analysis_areas["Cost Management"]:
                with st.expander("Cost Management Insights"):
                    st.markdown("""
                    ### Cost Management Insights
                    
                    **Current Status: 🟢 On Target**
                    
                    The project is currently **2% under budget** with the following observations:
                    
                    - Structural steel costs came in 5% below estimates due to favorable pricing
                    - Concrete work exceeded budget by 7% due to additional requirements
                    - Change orders represent 3.2% of total budget (below 5% threshold)
                    
                    **Recommendations:**
                    
                    1. Review upcoming finishes procurement to capture potential savings
                    2. Apply contingency from steel savings to address potential MEP overruns
                    3. Continue weekly cost tracking meetings with subcontractors
                    
                    **Predictive Alert:** Mechanical system costs may exceed estimates by 8-10% based on recent material price increases.
                    """)
        
            # Additional insights sections would follow similar pattern

def render_risk_assessment():
    """Render risk assessment tool for identifying and managing project risks."""
    st.header("Risk Assessment")
    st.markdown("""
    AI-powered risk assessment helps identify potential issues before they occur.
    The system analyzes project data, history, and external factors to predict and quantify risks.
    """)
    
    # Risk assessment setup
    col1, col2 = st.columns(2)
    with col1:
        project_type = st.selectbox(
            "Project Type",
            ["Mixed-Use High-Rise", "Commercial", "Infrastructure", "Healthcare", "Residential"]
        )
    
    with col2:
        project_phase = st.selectbox(
            "Current Phase",
            ["Pre-Construction", "Foundation", "Structural", "Envelope", "MEP", "Finishes"]
        )
    
    # Risk categories
    st.subheader("Risk Categories to Assess")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        schedule_risk = st.checkbox("Schedule Risks", value=True)
        budget_risk = st.checkbox("Budget Risks", value=True)
    
    with col2:
        quality_risk = st.checkbox("Quality Risks", value=True)
        safety_risk = st.checkbox("Safety Risks", value=True)
    
    with col3:
        regulatory_risk = st.checkbox("Regulatory Risks", value=True)
        resource_risk = st.checkbox("Resource Risks", value=True)
    
    # Additional factors
    st.subheader("Additional Risk Factors")
    
    col1, col2 = st.columns(2)
    with col1:
        weather_impact = st.slider("Weather Impact Potential", 0, 10, 5)
        supply_chain = st.slider("Supply Chain Disruption Potential", 0, 10, 4)
    
    with col2:
        labor_market = st.slider("Labor Market Constraints", 0, 10, 6)
        design_changes = st.slider("Design Change Likelihood", 0, 10, 3)
    
    # Historical data toggle
    include_historical = st.checkbox("Include Historical Project Data", value=True)
    
    # Generate risk assessment button
    if st.button("Generate Risk Assessment"):
        with st.spinner("Analyzing risks..."):
            # Simulate risk analysis (in a real app, this would use the AI API)
            st.success("Risk assessment complete!")
            
            # Display risk matrix
            st.subheader("Risk Matrix")
            
            # Create synthetic risk data
            risks = [
                {"category": "Schedule", "risk": "Material delivery delays", "impact": 4, "probability": 3},
                {"category": "Schedule", "risk": "Labor shortages", "impact": 3, "probability": 4},
                {"category": "Budget", "risk": "Steel price escalation", "impact": 4, "probability": 4},
                {"category": "Budget", "risk": "Change order scope creep", "impact": 3, "probability": 3},
                {"category": "Quality", "risk": "Curtain wall water intrusion", "impact": 5, "probability": 2},
                {"category": "Safety", "risk": "Working at heights incidents", "impact": 5, "probability": 2},
                {"category": "Regulatory", "risk": "Inspection delays", "impact": 3, "probability": 3},
                {"category": "Resource", "risk": "Subcontractor bankruptcy", "impact": 5, "probability": 1}
            ]
            
            # Create risk dataframe
            risk_df = pd.DataFrame(risks)
            risk_df["Risk Score"] = risk_df["impact"] * risk_df["probability"]
            risk_df["Priority"] = risk_df["Risk Score"].apply(lambda x: 
                "High" if x >= 12 else "Medium" if x >= 6 else "Low")
            
            # Color-coded risk table
            def highlight_priority(val):
                if val == "High":
                    return 'background-color: #ffcccc'
                elif val == "Medium":
                    return 'background-color: #ffffcc'
                else:
                    return 'background-color: #ccffcc'
            
            styled_risks = risk_df.style.applymap(highlight_priority, subset=["Priority"])
            st.dataframe(styled_risks)
            
            # Risk mitigation recommendations
            st.subheader("Mitigation Recommendations")
            
            for risk in risks:
                if risk["impact"] * risk["probability"] >= 12:  # High priority risks
                    st.markdown(f"**{risk['risk']}** (High Priority)")
                    
                    # Generate recommendations based on risk type
                    if risk["category"] == "Schedule":
                        st.markdown("""
                        - Identify alternative suppliers and establish backup delivery options
                        - Implement expedited procurement process for critical path items
                        - Develop labor resource leveling strategy with incentives for key positions
                        """)
                    elif risk["category"] == "Budget":
                        st.markdown("""
                        - Negotiate price lock agreements with suppliers for extended periods
                        - Implement enhanced change order review process with multiple approval levels
                        - Increase contingency allocation for affected cost codes
                        """)

def render_schedule_optimization():
    """Render schedule optimization tool for improving project timelines."""
    st.header("Schedule Optimization")
    st.markdown("""
    AI-powered schedule optimization helps identify opportunities to improve project timelines,
    reallocate resources, and resolve conflicts to keep projects on track.
    """)
    
    # Upload schedule file option
    schedule_file = st.file_uploader("Upload Project Schedule (optional)", type=["xml", "mpp", "xlsx"])
    
    # Schedule parameters
    st.subheader("Schedule Parameters")
    
    col1, col2 = st.columns(2)
    with col1:
        project_duration = st.number_input("Project Duration (weeks)", min_value=1, value=78)
        resources_available = st.number_input("Available Resource Units", min_value=1, value=25)
    
    with col2:
        critical_milestone = st.date_input("Key Milestone Target", datetime.now() + timedelta(days=180))
        optimization_goal = st.selectbox(
            "Optimization Goal",
            ["Minimize Duration", "Resource Leveling", "Cost Optimization", "Risk Reduction"]
        )
    
    # Constraints
    st.subheader("Constraints")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        max_daily_crews = st.number_input("Max Crews Per Day", min_value=1, value=8)
    
    with col2:
        weather_days = st.number_input("Weather Contingency Days", min_value=0, value=10)
    
    with col3:
        weekend_work = st.checkbox("Allow Weekend Work")
    
    # Activity dependencies toggle
    respect_dependencies = st.checkbox("Respect All Existing Dependencies", value=True)
    
    # Fixed milestones
    fixed_milestones = st.multiselect(
        "Fixed Milestones (Cannot Move)",
        ["Project Start", "Foundation Complete", "Structure Complete", "Building Dry-In", "MEP Complete", "Project Completion"]
    )
    
    # Run optimization button
    if st.button("Run Schedule Optimization"):
        with st.spinner("Optimizing schedule..."):
            # Simulate optimization (in a real app, this would use the AI API)
            st.success("Schedule optimization complete!")
            
            # Display optimization results
            st.subheader("Optimization Results")
            
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Original Duration", "78 weeks", "")
                st.metric("Optimized Duration", "72 weeks", "-6 weeks")
            
            with col2:
                st.metric("Resource Utilization", "68%", "+12%")
                st.metric("Critical Path Activities", "24", "-5")
            
            with col3:
                st.metric("Schedule Efficiency", "82%", "+15%")
                st.metric("Risk Rating", "Medium", "")
            
            # Gantt chart visualization
            st.subheader("Optimized Schedule")
            
            # Create sample schedule data
            tasks = [
                {"Task": "Site Preparation", "Start": "2025-06-01", "End": "2025-07-15", "Type": "Actual"},
                {"Task": "Site Preparation", "Start": "2025-06-01", "End": "2025-07-30", "Type": "Original"},
                {"Task": "Foundation", "Start": "2025-07-16", "End": "2025-09-30", "Type": "Actual"},
                {"Task": "Foundation", "Start": "2025-08-01", "End": "2025-10-15", "Type": "Original"},
                {"Task": "Structural Frame", "Start": "2025-10-01", "End": "2026-01-15", "Type": "Actual"},
                {"Task": "Structural Frame", "Start": "2025-10-16", "End": "2026-02-01", "Type": "Original"},
                {"Task": "MEP Rough-In", "Start": "2025-12-15", "End": "2026-03-30", "Type": "Actual"},
                {"Task": "MEP Rough-In", "Start": "2026-01-15", "End": "2026-04-15", "Type": "Original"},
                {"Task": "Interior Finishes", "Start": "2026-03-01", "End": "2026-06-15", "Type": "Actual"},
                {"Task": "Interior Finishes", "Start": "2026-03-15", "End": "2026-07-01", "Type": "Original"}
            ]
            
            df = pd.DataFrame(tasks)
            df["Start"] = pd.to_datetime(df["Start"])
            df["End"] = pd.to_datetime(df["End"])
            
            # Display as a table for simplicity
            st.dataframe(df)
            
            # Optimization recommendations
            st.subheader("Key Optimization Recommendations")
            
            recommendations = [
                "Overlap site preparation and initial foundation work to save 2 weeks",
                "Increase structural crew from 6 to 8 workers to accelerate frame construction",
                "Start MEP rough-in on lower floors while upper structural work continues",
                "Consolidate material deliveries to reduce logistical downtime",
                "Implement Just-in-Time delivery for finishes to reduce storage requirements",
                "Reschedule non-critical inspections to avoid workforce interruptions"
            ]
            
            for i, rec in enumerate(recommendations):
                st.markdown(f"{i+1}. {rec}")

def render_cost_forecasting():
    """Render cost forecasting tool for predicting and managing project costs."""
    st.header("Cost Forecasting")
    st.markdown("""
    AI-powered cost forecasting helps predict future project costs, identify potential overruns,
    and recommend mitigation strategies based on current trends and historical data.
    """)
    
    # Budget parameters
    st.subheader("Budget Parameters")
    
    col1, col2 = st.columns(2)
    with col1:
        total_budget = st.number_input("Total Project Budget ($)", min_value=0, value=45500000)
        contingency_percent = st.slider("Contingency Percentage", 0.0, 15.0, 7.5)
    
    with col2:
        current_spent = st.number_input("Current Expenditure ($)", min_value=0, value=18200000)
        completion_percent = st.slider("Project Completion Percentage", 0.0, 100.0, 40.0)
    
    # Cost factors
    st.subheader("Cost Influence Factors")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        material_inflation = st.slider("Material Price Inflation (%)", -5.0, 20.0, 4.5)
    with col2:
        labor_inflation = st.slider("Labor Rate Inflation (%)", -5.0, 20.0, 3.2)
    with col3:
        productivity_factor = st.slider("Productivity Factor", 0.8, 1.2, 1.0, 0.05)
    
    # Special considerations
    consider_factors = st.multiselect(
        "Consider Additional Factors",
        ["Supply Chain Disruptions", "Labor Shortages", "Seasonal Weather Impact", "Regulatory Changes"]
    )
    
    # Generate forecast button
    if st.button("Generate Cost Forecast"):
        with st.spinner("Analyzing cost data..."):
            # Simulate cost forecasting (in a real app, this would use the AI API)
            st.success("Cost forecast complete!")
            
            # Display forecast summary
            st.subheader("Forecast Summary")
            
            # Calculate some forecast metrics
            spent_percent = (current_spent / total_budget) * 100
            budget_variance = spent_percent - completion_percent
            
            earned_value = total_budget * (completion_percent / 100)
            cost_performance = earned_value / current_spent
            
            forecast_total = current_spent / (completion_percent / 100)
            forecast_variance = forecast_total - total_budget
            forecast_variance_percent = (forecast_variance / total_budget) * 100
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Budget Performance", f"{budget_variance:.1f}%", 
                          f"{-budget_variance:.1f}%" if budget_variance > 0 else f"{abs(budget_variance):.1f}%")
                st.metric("Cost Performance Index", f"{cost_performance:.2f}", 
                          f"{cost_performance-1:.2f}" if cost_performance >= 1 else f"{cost_performance-1:.2f}")
            
            with col2:
                st.metric("Original Budget", f"${total_budget:,.0f}", "")
                st.metric("Forecast at Completion", f"${forecast_total:,.0f}", 
                          f"${forecast_variance:,.0f}" if forecast_variance >= 0 else f"-${abs(forecast_variance):,.0f}")
            
            with col3:
                st.metric("Contingency Budget", f"${total_budget * (contingency_percent/100):,.0f}", "")
                st.metric("Forecast Variance", f"{forecast_variance_percent:.1f}%", 
                          f"{forecast_variance_percent:.1f}%" if forecast_variance_percent >= 0 else f"{forecast_variance_percent:.1f}%")
            
            # Cost trend chart
            st.subheader("Cost Trend Analysis")
            
            # Create sample cost data
            months = pd.date_range(start='2025-01-01', periods=24, freq='M')
            
            # Planned and actual cumulative costs
            planned_curve = [total_budget * (1 - np.exp(-0.15 * i)) / (1 - np.exp(-0.15 * 24)) for i in range(1, 25)]
            
            # Simulated actuals that deviate slightly
            actuals = []
            for i in range(int(len(months) * (completion_percent / 100))):
                variance_factor = 1 + (np.random.rand() - 0.5) * 0.06  # Random variance
                actuals.append(planned_curve[i] * variance_factor)
            
            # Create forecast based on current performance
            forecast = []
            if actuals:
                current_trend = actuals[-1] / planned_curve[len(actuals)-1]
                for i in range(len(actuals), 24):
                    forecast.append(planned_curve[i] * current_trend)
            
            # Display as a table for simplicity
            data = {
                "Month": months,
                "Planned": planned_curve
            }
            
            df = pd.DataFrame(data)
            df["Actual"] = pd.Series(actuals + [None] * (24 - len(actuals)))
            df["Forecast"] = pd.Series([None] * len(actuals) + forecast)
            
            st.dataframe(df)
            
            # Cost risk factors
            st.subheader("Cost Risk Factors")
            
            risk_factors = [
                {"Category": "Materials", "Risk": "Steel price volatility", "Impact": "Medium", "Trend": "↑ Increasing"},
                {"Category": "Labor", "Risk": "Skilled labor availability", "Impact": "High", "Trend": "→ Stable"},
                {"Category": "Subcontractors", "Risk": "MEP subcontractor performance", "Impact": "Medium", "Trend": "↓ Improving"},
                {"Category": "Schedule", "Risk": "Weather delays impacting costs", "Impact": "Low", "Trend": "→ Stable"},
                {"Category": "Design", "Risk": "Late design changes", "Impact": "Medium", "Trend": "↑ Increasing"}
            ]
            
            risk_df = pd.DataFrame(risk_factors)
            st.dataframe(risk_df)
            
            # Recommendations
            st.subheader("Cost Optimization Recommendations")
            
            recommendations = [
                "Lock in pricing for remaining steel deliveries to mitigate price volatility",
                "Accelerate MEP coordination to reduce potential rework costs",
                "Implement value engineering for upcoming interior packages (potential 4-6% savings)",
                "Review and optimize remaining change order contingencies",
                "Consider prefabrication options for repetitive bathroom and kitchen units"
            ]
            
            for i, rec in enumerate(recommendations):
                st.markdown(f"{i+1}. {rec}")