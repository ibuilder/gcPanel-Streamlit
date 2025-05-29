"""
AI Assistant Module for gcPanel.

This module provides AI-powered features for the gcPanel Construction Management 
Dashboard, including document analysis, project insights, and predictive suggestions.
"""

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Import AI helpers (to be implemented as needed)
# from utils.ai.document_search import render_document_search
# from utils.ai.smart_suggestions import render_smart_suggestions
# from utils.ai.project_insights import render_project_insights

def render_ai_assistant():
    """Render the AI Assistant interface."""
    st.title("AI Assistant")
    
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="margin-top: 0;">AI-Powered Construction Management</h3>
        <p>Use the AI Assistant to analyze project data, gain insights, and receive intelligent recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different AI features
    tabs = st.tabs([
        "Document Search", 
        "Project Insights", 
        "Smart Suggestions",
        "Risk Analysis"
    ])
    
    # Document Search Tab
    with tabs[0]:
        render_document_search()
    
    # Project Insights Tab
    with tabs[1]:
        render_project_insights()
    
    # Smart Suggestions Tab
    with tabs[2]:
        render_smart_suggestions()
    
    # Risk Analysis Tab
    with tabs[3]:
        render_risk_analysis()

def render_document_search():
    """Render the document search interface."""
    st.header("Smart Document Search")
    
    st.markdown("""
    Ask questions about your project documents using natural language.
    The AI will search across all documents and extract relevant information.
    """)
    
    # Search input
    query = st.text_input(
        "Ask about your documents", 
        placeholder="E.g., 'Show me all RFIs related to electrical work'"
    )
    
    # Sample dropdown for document sources to search
    document_sources = st.multiselect(
        "Search in",
        ["RFIs", "Submittals", "Change Orders", "Drawings", "Specifications", "Meeting Minutes", "Daily Reports"],
        default=["RFIs", "Submittals", "Change Orders"]
    )
    
    # Search button
    if st.button("Search Documents", type="primary"):
        if query:
            with st.spinner("Searching documents..."):
                # This would connect to an actual AI document search in production
                st.info("Connecting to Anthropic API for document search...")
                
                # Add delay to simulate processing
                import time
                time.sleep(1)
                
                # Show example results
                st.subheader("Search Results")
                
                # Example results card
                st.markdown("""
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px;">
                    <h4 style="margin-top: 0;">RFI #103: Electrical Panel Location</h4>
                    <p style="color: #666; font-size: 0.9em;">Submitted: April 12, 2025 | Status: Closed</p>
                    <p><strong>Relevant excerpt:</strong> The electrical subcontractor has requested clarification on the location of the main electrical panels on level 2. The current drawings show potential conflict with HVAC ductwork.</p>
                    <p><a href="#" style="text-decoration: none;">View Full Document →</a></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px;">
                    <h4 style="margin-top: 0;">Submittal #87: Electrical Fixtures</h4>
                    <p style="color: #666; font-size: 0.9em;">Submitted: March 28, 2025 | Status: Approved with Comments</p>
                    <p><strong>Relevant excerpt:</strong> The proposed LED fixtures for the common areas meet the energy efficiency requirements but architect has requested sample installations before final approval.</p>
                    <p><a href="#" style="text-decoration: none;">View Full Document →</a></p>
                </div>
                """, unsafe_allow_html=True)
                
                # AI summary of findings
                st.subheader("AI Summary")
                st.success("""
                There are 7 documents related to electrical work. The main topics include:
                
                1. Panel location conflicts with HVAC on level 2
                2. LED fixture approvals for common areas
                3. Power requirements for elevator equipment
                4. Emergency backup generator specifications
                
                The most critical issue appears to be the panel location conflict which needs resolution before wall framing begins next week.
                """)
        else:
            st.warning("Please enter a search query.")

def render_project_insights():
    """Render the project insights interface."""
    st.header("Project Insights")
    
    st.markdown("""
    Get AI-generated insights about your project status, trends, and potential issues.
    """)
    
    # Example project overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Schedule", value="3 days behind", delta="-3 days")
    
    with col2:
        st.metric(label="Budget", value="$23.4M", delta="$120K under")
    
    with col3:
        st.metric(label="Open RFIs", value="12", delta="-4")
    
    with col4:
        st.metric(label="Safety Score", value="94%", delta="+2%")
    
    # Project insights visualization
    st.subheader("Schedule Trend Analysis")
    
    # Create sample data for visualization
    dates = pd.date_range(start=datetime.now() - timedelta(days=180), periods=180, freq='D')
    
    # Sample data for planned vs actual progress
    schedule_data = pd.DataFrame({
        'Date': dates,
        'Planned': np.linspace(0, 65, 180),
        'Actual': np.concatenate([
            np.linspace(0, 20, 60) + np.random.normal(0, 0.5, 60),
            np.linspace(20, 35, 60) + np.random.normal(-1, 0.5, 60),
            np.linspace(35, 62, 60) + np.random.normal(-3, 0.5, 60)
        ])
    })
    
    # Plot the data
    st.line_chart(schedule_data.set_index('Date')[['Planned', 'Actual']])
    
    # AI insights
    st.subheader("AI Analysis")
    st.info("""
    Project analysis indicates a gradual schedule slippage that began approximately 2 months ago. 
    The divergence coincides with several factors:
    
    1. Weather delays during foundation work (7 days total)
    2. Material delivery delays for steel (5 days)
    3. Labor shortages in electrical teams (ongoing)
    
    Recommendation: The current 3-day delay could extend to 5-7 days if the electrical labor issue 
    is not addressed. Consider reallocating resources from the finishing team to support electrical 
    installation on levels 3-5.
    """)
    
    # Additional insights
    st.subheader("Critical Path Impact")
    
    # Mock critical path tasks
    st.markdown("""
    <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px;">
        <h4 style="margin-top: 0; color: #e63946;">At Risk: Level 5-8 Electrical Rough-In</h4>
        <p><strong>Impact:</strong> This task is currently 2 days behind and is on the critical path. Each day of delay here will directly impact project completion.</p>
        <p><strong>AI Recommendation:</strong> Increase electrical crew size by 2-3 workers for the next 2 weeks to recover schedule.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px;">
        <h4 style="margin-top: 0; color: #e9c46a;">Caution: Elevator Installation</h4>
        <p><strong>Impact:</strong> Currently on schedule but highly dependent on timely delivery of equipment scheduled for next week.</p>
        <p><strong>AI Recommendation:</strong> Confirm delivery dates with vendor and prepare contingency plan for installation crews.</p>
    </div>
    """, unsafe_allow_html=True)

def render_smart_suggestions():
    """Render the smart suggestions interface."""
    st.header("Smart Suggestions")
    
    st.markdown("""
    Receive intelligent recommendations based on your project data and construction best practices.
    """)
    
    # Types of suggestions
    suggestion_types = st.multiselect(
        "Show suggestions for",
        ["Schedule Optimization", "Cost Savings", "Risk Mitigation", "Quality Improvements", "Safety Enhancements"],
        default=["Schedule Optimization", "Cost Savings", "Risk Mitigation"]
    )
    
    # Mock suggestions
    st.subheader("Today's Recommendations")
    
    if "Schedule Optimization" in suggestion_types:
        st.markdown("""
        <div style="border-left: 4px solid #457b9d; padding-left: 15px; margin-bottom: 20px;">
            <h4 style="margin-top: 0;">Optimize Concrete Pour Schedule</h4>
            <p>Based on the 10-day weather forecast, Thursday and Friday of next week provide the optimal conditions for the level 10 concrete pour. Rescheduling from the planned Monday date would avoid potential rain delays and cold temperature issues.</p>
            <p><strong>Potential Impact:</strong> Avoid 3-day cure time extension and $8,500 in additional heating costs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    if "Cost Savings" in suggestion_types:
        st.markdown("""
        <div style="border-left: 4px solid #2a9d8f; padding-left: 15px; margin-bottom: 20px;">
            <h4 style="margin-top: 0;">Consolidate Material Orders</h4>
            <p>The system has identified multiple small orders for similar electrical components scheduled over the next 3 weeks. Consolidating these into a single order could save on delivery fees and potentially qualify for bulk pricing discounts.</p>
            <p><strong>Potential Impact:</strong> Estimated savings of $12,300 in material and delivery costs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    if "Risk Mitigation" in suggestion_types:
        st.markdown("""
        <div style="border-left: 4px solid #e63946; padding-left: 15px; margin-bottom: 20px;">
            <h4 style="margin-top: 0;">Preemptive RFI Recommendation</h4>
            <p>Analysis of the mechanical and plumbing drawings has identified a potential conflict between HVAC ducting and plumbing lines in the southeast corner of level 3. Similar issues have caused delays in previous projects.</p>
            <p><strong>Recommended Action:</strong> Submit an RFI to the design team for clarification before work begins in this area next month.</p>
        </div>
        """, unsafe_allow_html=True)
    
    if "Quality Improvements" in suggestion_types:
        st.markdown("""
        <div style="border-left: 4px solid #f4a261; padding-left: 15px; margin-bottom: 20px;">
            <h4 style="margin-top: 0;">Enhanced Inspection Protocol</h4>
            <p>Based on quality issues identified in similar projects, implementing additional inspection points for the curtain wall installation could prevent water infiltration issues commonly found after project completion.</p>
            <p><strong>Potential Impact:</strong> Reduce post-completion issues by approximately 40% based on historical data.</p>
        </div>
        """, unsafe_allow_html=True)
    
    if "Safety Enhancements" in suggestion_types:
        st.markdown("""
        <div style="border-left: 4px solid #ff9f1c; padding-left: 15px; margin-bottom: 20px;">
            <h4 style="margin-top: 0;">Crane Operation Safety Alert</h4>
            <p>Weather forecast indicates high wind conditions (25+ mph) for Tuesday afternoon. Based on the crane manufacturer specifications and project safety plan, this would exceed safe operating parameters.</p>
            <p><strong>Recommended Action:</strong> Adjust the lifting schedule to morning hours when wind speeds are predicted to be lower.</p>
        </div>
        """, unsafe_allow_html=True)

def render_risk_analysis():
    """Render the risk analysis interface."""
    st.header("Project Risk Analysis")
    
    st.markdown("""
    AI-powered analysis of project risks and potential mitigation strategies.
    """)
    
    # Risk analysis options
    analysis_period = st.radio(
        "Analysis Period",
        ["Next 30 Days", "Next 90 Days", "Project Completion"],
        horizontal=True
    )
    
    # Show risk matrix
    st.subheader("Risk Matrix")
    
    # Create sample data for a risk matrix visualization
    risk_data = pd.DataFrame({
        'Risk': [
            'Weather Delays', 
            'Material Availability', 
            'Labor Shortages',
            'Subcontractor Default',
            'Design Changes',
            'Permit Delays',
            'Budget Overruns',
            'Quality Issues'
        ],
        'Likelihood': [0.7, 0.5, 0.6, 0.2, 0.4, 0.3, 0.5, 0.4],
        'Impact': [3, 4, 3, 5, 4, 4, 4, 3],
        'Category': [
            'Environmental', 
            'Supply Chain', 
            'Resource',
            'Financial',
            'Design',
            'Regulatory',
            'Financial',
            'Quality'
        ]
    })
    
    # Adjust data based on selected period
    if analysis_period == "Next 30 Days":
        multiplier = 1.0
    elif analysis_period == "Next 90 Days":
        multiplier = 0.85
        # Add additional risks that might emerge later
        new_risk = pd.DataFrame({
            'Risk': ['Site Security', 'Commissioning Delays'],
            'Likelihood': [0.3, 0.6],
            'Impact': [2, 4],
            'Category': ['Security', 'Schedule']
        })
        risk_data = pd.concat([risk_data, new_risk])
    else:  # Project Completion
        multiplier = 0.7
        # Add additional risks for project completion
        new_risk = pd.DataFrame({
            'Risk': ['Site Security', 'Commissioning Delays', 'Final Inspection Issues', 'Owner Acceptance Delays'],
            'Likelihood': [0.3, 0.6, 0.5, 0.4],
            'Impact': [2, 4, 4, 3],
            'Category': ['Security', 'Schedule', 'Quality', 'Administrative']
        })
        risk_data = pd.concat([risk_data, new_risk])
    
    # Apply multiplier for likelihood changes over time
    risk_data['Likelihood'] = risk_data['Likelihood'] * multiplier
    
    # Calculate risk score
    risk_data['Risk Score'] = risk_data['Likelihood'] * risk_data['Impact']
    
    # Sort by risk score
    risk_data = risk_data.sort_values('Risk Score', ascending=False)
    
    # Display top risks
    st.markdown("### Highest Risk Items")
    for i, row in risk_data.head(3).iterrows():
        severity = "High" if row['Risk Score'] > 2.0 else "Medium"
        color = "#e63946" if severity == "High" else "#f4a261"
        
        st.markdown(f"""
        <div style="border-left: 4px solid {color}; padding-left: 15px; margin-bottom: 20px;">
            <h4 style="margin-top: 0;">{row['Risk']} ({severity} Risk)</h4>
            <p><strong>Category:</strong> {row['Category']}<br>
            <strong>Likelihood:</strong> {int(row['Likelihood']*100)}%<br>
            <strong>Impact:</strong> {row['Impact']}/5<br>
            <strong>Risk Score:</strong> {row['Risk Score']:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display risk mitigation recommendations
    st.subheader("AI Mitigation Recommendations")
    
    top_risk = risk_data.iloc[0]['Risk']
    
    if top_risk == "Weather Delays":
        st.info("""
        For Weather Delays (highest current risk):
        
        1. Review critical path activities scheduled for next 30 days and identify those susceptible to weather impacts
        2. Implement temporary weather protection measures for sensitive work areas
        3. Update the float in the schedule for weather-sensitive activities
        4. Prepare contingency plans for crew reallocation during weather events
        5. Consider temporary heating/cooling equipment rental for maintaining optimal curing conditions
        """)
    elif top_risk == "Material Availability":
        st.info("""
        For Material Availability (highest current risk):
        
        1. Identify all long-lead items and verify current delivery schedules
        2. Establish secondary suppliers for critical materials
        3. Consider pre-purchasing and storing critical items ahead of scheduled installation
        4. Implement weekly supplier check-ins for at-risk materials
        5. Update the schedule to reflect current material delivery timelines
        """)
    else:
        st.info(f"""
        For {top_risk} (highest current risk):
        
        1. Establish a dedicated risk monitoring protocol for this specific risk
        2. Develop contingency plans with specific trigger points
        3. Allocate additional resources to mitigation efforts
        4. Schedule weekly review meetings to track mitigation progress
        5. Update risk assessment as new information becomes available
        """)
    
    # Show trend analysis
    st.subheader("Risk Trend Analysis")
    
    # Create sample data for risk trends over time
    dates = pd.date_range(start=datetime.now() - timedelta(days=90), periods=90, freq='D')
    
    # Overall risk score trend (weighted average of all risks)
    risk_trend = pd.DataFrame({
        'Date': dates,
        'Overall Risk Score': np.concatenate([
            np.linspace(3.2, 2.8, 30) + np.random.normal(0, 0.1, 30),
            np.linspace(2.8, 3.5, 30) + np.random.normal(0, 0.1, 30),
            np.linspace(3.5, 3.0, 30) + np.random.normal(0, 0.1, 30)
        ])
    })
    
    # Plot the risk trend
    st.line_chart(risk_trend.set_index('Date')[['Overall Risk Score']])