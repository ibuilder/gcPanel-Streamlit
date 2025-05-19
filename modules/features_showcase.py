"""
Features Showcase Module for gcPanel.

This module demonstrates all the new features implemented for gcPanel,
including integrations, analytics, mobile view, collaboration, and AI features.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def render_features_showcase():
    """Render the features showcase module."""
    # Import and render the header component
    from components.header_clean import render_header
    render_header()
    
    st.title("gcPanel New Features Showcase")
    
    st.write("""
    This showcase demonstrates the powerful new features of gcPanel Construction Management Dashboard.
    Each feature can be integrated into the appropriate modules in your production environment.
    """)
    
    # Create tabs for different feature categories
    tabs = st.tabs([
        "Integrations", 
        "Analytics", 
        "Mobile Features", 
        "Collaboration Tools", 
        "AI Assistant"
    ])
    
    # Integrations Tab
    with tabs[0]:
        st.header("External Service Integrations")
        st.write("Connect gcPanel with your essential construction management tools.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Project Management")
            st.info("Connect with tools like Procore, PlanGrid, or Microsoft Project.")
            
            st.subheader("Calendar & Scheduling")
            st.info("Sync with Google Calendar, Outlook, or iCalendar.")
        
        with col2:
            st.subheader("Cloud Storage")
            st.info("Link with Dropbox, Google Drive, OneDrive, or Box.")
            
            st.subheader("BIM & Design")
            st.info("Integrate with Autodesk BIM 360, Revit, or SketchUp.")
    
    # Analytics Tab
    with tabs[1]:
        st.header("Advanced Analytics & Reporting")
        
        # Create sample data
        dates = pd.date_range(start=datetime.now() - timedelta(days=90), periods=90, freq='D')
        
        # Project progress data
        progress_data = pd.DataFrame({
            'Date': dates,
            'Planned': np.linspace(0, 100, 90),
            'Actual': np.linspace(0, 85, 90) + np.random.normal(0, 3, 90)
        })
        
        # Cost data
        cost_data = pd.DataFrame({
            'Date': dates,
            'Budget': np.ones(90) * 1000000,
            'Actual': np.linspace(100000, 850000, 90) + np.random.normal(0, 15000, 90)
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Project Progress Tracking")
            st.line_chart(
                progress_data.set_index('Date')[['Planned', 'Actual']]
            )
        
        with col2:
            st.subheader("Budget vs. Actual Cost")
            st.line_chart(
                cost_data.set_index('Date')[['Budget', 'Actual']]
            )
        
        st.subheader("Predictive Analytics")
        st.info("""
        Machine learning models analyze project data to predict:
        - Completion dates
        - Cost overruns
        - Resource bottlenecks
        - Safety incidents
        """)
    
    # Mobile Features Tab
    with tabs[2]:
        st.header("Mobile-First Design & Features")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Key Mobile Features")
            st.markdown("""
            - Responsive UI for all devices
            - PWA support for offline access
            - Touch-optimized controls
            - Mobile image/document capture
            - QR code/barcode scanning
            """)
        
        with col2:
            st.subheader("Mobile Companion Preview")
            # Use a placeholder message instead of loading an external image
            st.info("Mobile companion interface preview would be displayed here.")
    
    # Collaboration Tab
    with tabs[3]:
        st.header("Real-Time Collaboration Tools")
        
        st.subheader("Document Collaboration")
        st.info("""
        Edit documents with multiple team members simultaneously.
        See who's viewing and editing in real-time.
        """)
        
        st.subheader("Real-Time Chat & Comments")
        
        # Mock chat interface
        with st.container():
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                <p><strong>John (Project Manager):</strong> The foundation inspection is scheduled for tomorrow at 9am.</p>
            </div>
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                <p><strong>Sarah (Engineer):</strong> I've uploaded the revised drawings for review.</p>
            </div>
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                <p><strong>Mike (Foreman):</strong> We need the concrete delivery to be pushed to 11am.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.text_input("Type your message...")
            st.button("Send")
    
    # AI Assistant Tab
    with tabs[4]:
        st.header("AI-Powered Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Smart Document Search")
            st.info("""
            Find information across all project documents using natural language questions:
            - "Show me all RFIs about the foundation"
            - "Find drawings with electrical revisions"
            """)
            
            st.text_input("Search documents...", placeholder="E.g., Show inspection reports from last week")
            st.button("Search")
        
        with col2:
            st.subheader("Intelligent Alerts & Insights")
            st.warning("Budget forecast shows potential 5% overrun in electrical work.")
            st.warning("Schedule analysis indicates critical path delays in framing phase.")
            st.info("AI recommends adjusting crew allocation to optimize workflow.")
        
        st.subheader("AI Project Summary")
        st.success("""
        Highland Tower project is currently 3 days behind schedule but within budget constraints.
        Recent weather delays have impacted exterior work, but the team has adjusted interior tasks
        to maintain productivity. The AI recommends shifting resources to focus on completing
        level 5 electrical work to avoid potential cascading delays.
        """)