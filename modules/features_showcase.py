"""
Features Showcase Module for gcPanel.

This module demonstrates all the new features implemented for gcPanel,
including integrations, analytics, mobile view, collaboration, and AI features.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import new feature modules
from utils.integration_manager import IntegrationType, IntegrationProvider
from utils.mobile.responsive_layout import add_mobile_styles, create_responsive_card
from utils.mobile.pwa_support import setup_pwa
from utils.collaboration.realtime_collaboration import render_collaboration_chat, render_document_collaboration
from utils.ai.document_search import render_smart_search_interface
from utils.ai.smart_suggestions import PredictiveTyping, IntelligentAlerts

def render_features_showcase():
    """Render the features showcase module."""
    st.title("gcPanel New Features Showcase")
    
    # Apply mobile optimizations
    add_mobile_styles()
    
    # Set up PWA support
    setup_pwa()
    
    # Feature selection
    st.sidebar.title("Feature Categories")
    feature_category = st.sidebar.radio(
        "Select Feature Category",
        ["Overview", "Integration Manager", "Analytics Dashboard", 
         "Mobile Optimization", "Collaboration Tools", "AI-Powered Features"]
    )
    
    # Render selected feature category
    if feature_category == "Overview":
        render_feature_overview()
    elif feature_category == "Integration Manager":
        render_integration_showcase()
    elif feature_category == "Analytics Dashboard":
        render_analytics_showcase()
    elif feature_category == "Mobile Optimization":
        render_mobile_showcase()
    elif feature_category == "Collaboration Tools":
        render_collaboration_showcase()
    elif feature_category == "AI-Powered Features":
        render_ai_showcase()

def render_feature_overview():
    """Render overview of all new features."""
    st.header("New Features Overview")
    
    st.markdown("""
    ### 1. Integration Manager
    Connect gcPanel with external services including:
    - Project management tools (Jira, Asana, MS Project)
    - Calendars (Google Calendar, Microsoft Outlook)
    - Cloud storage (Google Drive, Dropbox, OneDrive)
    - Construction management platforms (Procore)
    
    ### 2. Advanced Analytics Dashboard
    Gain insights from your project data with:
    - Interactive data visualizations with Plotly charts
    - Predictive analytics for project timelines and budgets
    - Custom reporting with exportable formats
    
    ### 3. Mobile Optimization
    Access gcPanel on any device with:
    - Responsive layout for mobile devices
    - Progressive Web App (PWA) capabilities for offline access
    - Dedicated field companion app for construction personnel
    
    ### 4. Collaboration Tools
    Work together more effectively with:
    - Real-time collaboration via WebSockets
    - Document comments and discussion threads
    - @mentions and task assignments
    
    ### 5. AI-Powered Features
    Enhance productivity with:
    - Smart document search using natural language
    - Predictive typing and form field suggestions
    - Intelligent alerts based on project patterns
    
    Select a feature category from the sidebar to see it in action.
    """)
    
    # Show feature showcase images
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("attached_assets/image_1747581248447.png", caption="Analytics Dashboard", use_column_width=True)
        st.image("attached_assets/image_1747582086074.png", caption="Mobile Interface", use_column_width=True)
    
    with col2:
        st.image("attached_assets/image_1747577298348.png", caption="Project Management", use_column_width=True)
        st.image("attached_assets/image_1747581883336.png", caption="Collaboration Tools", use_column_width=True)

def render_integration_showcase():
    """Render integration manager showcase."""
    st.header("Integration Manager")
    
    st.markdown("""
    The Integration Manager allows gcPanel to connect with external services, 
    enabling seamless workflows between different platforms used in construction management.
    """)
    
    # Integration types tabs
    tabs = st.tabs([
        "Project Management", 
        "Calendar", 
        "Cloud Storage",
        "Construction Management"
    ])
    
    # Project Management tab
    with tabs[0]:
        st.subheader("Project Management Integrations")
        
        st.markdown("""
        Connect gcPanel with project management tools to sync tasks, issues, and timelines.
        """)
        
        # Available integrations
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                """
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; text-align: center;">
                    <h3>Jira</h3>
                    <p>Sync issues, epics and sprints with Jira project management</p>
                    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                        Status: Not Connected
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if st.button("Connect Jira", key="connect_jira"):
                st.info("This would launch the Jira authentication flow in a real implementation.")
        
        with col2:
            st.markdown(
                """
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; text-align: center;">
                    <h3>Asana</h3>
                    <p>Sync tasks, projects and milestones with Asana</p>
                    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                        Status: Not Connected
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if st.button("Connect Asana", key="connect_asana"):
                st.info("This would launch the Asana authentication flow in a real implementation.")
        
        with col3:
            st.markdown(
                """
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; text-align: center;">
                    <h3>MS Project</h3>
                    <p>Sync tasks, timelines and resources with Microsoft Project</p>
                    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                        Status: Not Connected
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if st.button("Connect MS Project", key="connect_ms_project"):
                st.info("This would launch the Microsoft authentication flow in a real implementation.")
    
    # Calendar tab
    with tabs[1]:
        st.subheader("Calendar Integrations")
        
        st.markdown("""
        Connect gcPanel with calendar services to sync project events, meetings, and deadlines.
        """)
        
        # Available integrations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(
                """
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; text-align: center;">
                    <h3>Google Calendar</h3>
                    <p>Sync project events with Google Calendar</p>
                    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                        Status: Not Connected
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if st.button("Connect Google Calendar", key="connect_google_calendar"):
                st.info("This would launch the Google authentication flow in a real implementation.")
        
        with col2:
            st.markdown(
                """
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; text-align: center;">
                    <h3>Microsoft Outlook</h3>
                    <p>Sync project events with Microsoft Outlook</p>
                    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                        Status: Not Connected
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if st.button("Connect Outlook", key="connect_outlook"):
                st.info("This would launch the Microsoft authentication flow in a real implementation.")
    
    # Cloud Storage tab
    with tabs[2]:
        st.subheader("Cloud Storage Integrations")
        
        st.markdown("""
        Connect gcPanel with cloud storage services to sync project documents and files.
        """)
        
        # Available integrations
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                """
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; text-align: center;">
                    <h3>Google Drive</h3>
                    <p>Sync project files with Google Drive</p>
                    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                        Status: Not Connected
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if st.button("Connect Google Drive", key="connect_google_drive"):
                st.info("This would launch the Google authentication flow in a real implementation.")
        
        with col2:
            st.markdown(
                """
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; text-align: center;">
                    <h3>Dropbox</h3>
                    <p>Sync project files with Dropbox</p>
                    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                        Status: Not Connected
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if st.button("Connect Dropbox", key="connect_dropbox"):
                st.info("This would launch the Dropbox authentication flow in a real implementation.")
        
        with col3:
            st.markdown(
                """
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; text-align: center;">
                    <h3>OneDrive</h3>
                    <p>Sync project files with Microsoft OneDrive</p>
                    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                        Status: Not Connected
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if st.button("Connect OneDrive", key="connect_onedrive"):
                st.info("This would launch the Microsoft authentication flow in a real implementation.")
    
    # Construction Management tab
    with tabs[3]:
        st.subheader("Construction Management Integrations")
        
        st.markdown("""
        Connect gcPanel with construction management platforms for advanced interoperability.
        """)
        
        # Available integrations
        col1, = st.columns(1)
        
        with col1:
            st.markdown(
                """
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; text-align: center;">
                    <h3>Procore</h3>
                    <p>Connect with Procore construction management platform</p>
                    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                        Status: Not Connected
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if st.button("Connect Procore", key="connect_procore"):
                st.info("This would launch the Procore authentication flow in a real implementation.")
    
    # Integration settings
    with st.expander("Integration Settings"):
        st.markdown("### Global Settings")
        
        st.checkbox("Enable automatic syncing", value=True)
        st.selectbox("Sync frequency", ["Every 15 minutes", "Every hour", "Every 4 hours", "Daily"])
        st.checkbox("Notify on sync errors", value=True)
        
        st.markdown("### Connection Management")
        
        if st.button("Test All Connections"):
            st.info("This would test all connected integrations in a real implementation.")
        
        if st.button("Reset All Connections"):
            st.warning("This would reset all integration connections in a real implementation.")

def render_analytics_showcase():
    """Render analytics dashboard showcase."""
    st.header("Advanced Analytics Dashboard")
    
    st.markdown("""
    The Analytics Dashboard provides powerful visualization and analysis tools
    to gain insights from your project data, including predictive analytics
    and custom reporting capabilities.
    """)
    
    # Analytics types tabs
    tabs = st.tabs([
        "Data Visualization", 
        "Predictive Analytics", 
        "Custom Reporting"
    ])
    
    # Data Visualization tab
    with tabs[0]:
        st.subheader("Interactive Data Visualization")
        
        st.markdown("""
        Explore project data with interactive Plotly charts and visualizations.
        """)
        
        # Sample visualization
        import plotly.express as px
        
        # Generate sample data
        dates = pd.date_range(start='2024-06-01', end='2025-06-01', freq='M')
        planned_progress = np.linspace(0, 100, len(dates))
        actual_progress = planned_progress + np.random.normal(0, 5, len(dates))
        actual_progress = np.clip(actual_progress, 0, 100)
        
        df = pd.DataFrame({
            'Date': dates,
            'Planned': planned_progress,
            'Actual': actual_progress
        })
        
        # Create visualization
        fig = px.line(
            df, 
            x='Date', 
            y=['Planned', 'Actual'],
            title='Project Progress Over Time',
            labels={'value': 'Completion (%)', 'variable': 'Series'}
        )
        
        # Add today marker
        fig.add_vline(
            x=datetime.now(),
            line_dash="dash",
            line_color="green",
            annotation_text="Today"
        )
        
        # Show visualization
        st.plotly_chart(fig, use_container_width=True)
        
        # Visualization options
        st.markdown("### Visualization Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Chart Type", ["Line Chart", "Bar Chart", "Area Chart", "Scatter Plot"])
            st.selectbox("Time Period", ["Last Month", "Last Quarter", "Last Year", "Project to Date"])
        
        with col2:
            st.multiselect("Data Series", ["Planned Progress", "Actual Progress", "Budget", "Labor Hours"], 
                         default=["Planned Progress", "Actual Progress"])
            st.checkbox("Show Forecast", value=True)
    
    # Predictive Analytics tab
    with tabs[1]:
        st.subheader("Predictive Analytics")
        
        st.markdown("""
        Use machine learning to forecast project timelines and budgets based on current data.
        """)
        
        # Sample prediction visualization
        # Generate sample data
        dates = pd.date_range(start='2024-06-01', end=datetime.now(), freq='W')
        progress = np.linspace(0, 60, len(dates)) + np.random.normal(0, 2, len(dates))
        progress = np.clip(progress, 0, 100)
        
        # Create prediction
        current_progress = progress[-1]
        progress_per_week = np.mean(np.diff(progress))
        weeks_remaining = (100 - current_progress) / progress_per_week
        predicted_completion = dates[-1] + timedelta(weeks=weeks_remaining)
        
        # Create confidence interval
        lower_bound = predicted_completion - timedelta(weeks=2)
        upper_bound = predicted_completion + timedelta(weeks=2)
        
        # Create future dates
        future_dates = pd.date_range(start=dates[-1], end=predicted_completion + timedelta(weeks=4), freq='W')
        future_progress = np.linspace(current_progress, 100, len(future_dates))
        
        # Create visualization
        import plotly.graph_objects as go
        
        fig = go.Figure()
        
        # Add historical data
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=progress,
                name="Actual Progress",
                line=dict(color='blue')
            )
        )
        
        # Add forecast
        fig.add_trace(
            go.Scatter(
                x=future_dates,
                y=future_progress,
                name="Forecast",
                line=dict(color='red', dash='dash')
            )
        )
        
        # Add predicted completion
        fig.add_trace(
            go.Scatter(
                x=[predicted_completion],
                y=[100],
                name="Predicted Completion",
                mode="markers",
                marker=dict(color="red", size=12, symbol="star")
            )
        )
        
        # Add confidence interval
        fig.add_trace(
            go.Scatter(
                x=[lower_bound, upper_bound],
                y=[100, 100],
                name="Confidence Interval",
                mode="markers",
                marker=dict(color="orange", size=10, symbol="diamond")
            )
        )
        
        # Add today marker
        fig.add_vline(
            x=datetime.now(),
            line_dash="dash",
            line_color="green",
            annotation_text="Today"
        )
        
        # Update layout
        fig.update_layout(
            title="Project Timeline Prediction",
            xaxis_title="Date",
            yaxis_title="Progress (%)",
            height=400
        )
        
        # Show visualization
        st.plotly_chart(fig, use_container_width=True)
        
        # Prediction details
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Current Progress",
                value=f"{current_progress:.1f}%"
            )
        
        with col2:
            st.metric(
                label="Predicted Completion",
                value=predicted_completion.strftime("%Y-%m-%d")
            )
        
        with col3:
            # Calculate if ahead or behind schedule
            planned_date = datetime(2025, 7, 1)
            days_diff = (predicted_completion - planned_date).days
            
            status = "On Schedule"
            delta_color = "off"
            
            if days_diff > 0:
                status = f"{days_diff} days behind"
                delta_color = "inverse"
            elif days_diff < 0:
                status = f"{abs(days_diff)} days ahead"
                delta_color = "normal"
            
            st.metric(
                label="Schedule Status",
                value=status,
                delta=status,
                delta_color=delta_color
            )
        
        # Prediction options
        st.markdown("### Prediction Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Prediction Type", ["Timeline", "Budget", "Resource Utilization"])
            st.selectbox("Model Type", ["Linear Regression", "ARIMA", "Random Forest"])
        
        with col2:
            st.number_input("Confidence Level (%)", min_value=80, max_value=99, value=95)
            st.checkbox("Show Confidence Interval", value=True)
    
    # Custom Reporting tab
    with tabs[2]:
        st.subheader("Custom Reporting")
        
        st.markdown("""
        Generate custom reports with the exact data you need, in the format you prefer.
        """)
        
        # Report builder
        st.markdown("### Report Builder")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.multiselect(
                "Report Sections",
                ["Project Summary", "Schedule Analysis", "Budget Analysis", 
                 "Quality Metrics", "Safety Metrics", "Risk Analysis"],
                default=["Project Summary", "Schedule Analysis", "Budget Analysis"]
            )
            
            st.multiselect(
                "Data Fields",
                ["Project Name", "Project Status", "Start Date", "End Date", 
                 "Budget", "Actual Cost", "Planned Progress", "Actual Progress",
                 "Quality Issues", "Safety Incidents", "Risk Level"],
                default=["Project Name", "Project Status", "Planned Progress", "Actual Progress"]
            )
        
        with col2:
            st.selectbox("Report Type", ["Executive Summary", "Detailed Report", "Custom"])
            st.selectbox("Time Period", ["Last Month", "Last Quarter", "Last Year", "Custom"])
            st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
            st.date_input("End Date", value=datetime.now())
        
        # Export options
        st.markdown("### Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Export as PDF"):
                st.info("This would generate a PDF report in a real implementation.")
        
        with col2:
            if st.button("Export as Excel"):
                st.info("This would generate an Excel report in a real implementation.")
        
        with col3:
            if st.button("Export as CSV"):
                st.info("This would generate CSV files in a real implementation.")
        
        # Report preview
        st.markdown("### Report Preview")
        
        st.markdown("""
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 5px;">
            <h2 style="text-align: center;">Executive Summary Report</h2>
            <h3 style="text-align: center;">Highland Tower Development</h3>
            <p style="text-align: center;">Report Period: Last 30 Days</p>
            
            <h4>Project Status</h4>
            <p>The project is currently <b>85%</b> complete, which is <b>2%</b> ahead of schedule.
            The budget is currently <b>3%</b> over the planned amount.</p>
            
            <h4>Key Metrics</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background-color: #f0f0f0;">
                    <th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Metric</th>
                    <th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Planned</th>
                    <th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Actual</th>
                    <th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Variance</th>
                </tr>
                <tr>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">Progress</td>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">83%</td>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">85%</td>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd; color: green;">+2%</td>
                </tr>
                <tr>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">Budget</td>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">$38,675,000</td>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">$39,835,250</td>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd; color: red;">+3%</td>
                </tr>
                <tr>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">Quality Issues</td>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">0</td>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">3</td>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd; color: red;">+3</td>
                </tr>
                <tr>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">Safety Incidents</td>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">0</td>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">0</td>
                    <td style="padding: 8px; text-align: left; border: 1px solid #ddd; color: green;">0</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

def render_mobile_showcase():
    """Render mobile optimization showcase."""
    st.header("Mobile Optimization")
    
    st.markdown("""
    gcPanel now features comprehensive mobile optimization to ensure the application
    works well on any device, with special features for field personnel.
    """)
    
    # Mobile features tabs
    tabs = st.tabs([
        "Responsive Layout", 
        "Progressive Web App", 
        "Field Companion"
    ])
    
    # Responsive Layout tab
    with tabs[0]:
        st.subheader("Responsive Layout")
        
        st.markdown("""
        The application now features a responsive layout that adapts to any screen size,
        from desktop monitors to mobile phones.
        """)
        
        # Demonstration
        col1, col2 = st.columns(2)
        
        with col1:
            st.image("attached_assets/image_1747602131443.png", caption="Desktop View", use_column_width=True)
        
        with col2:
            st.image("attached_assets/image_1747603031794.png", caption="Mobile View", use_column_width=True)
        
        # Responsive features
        st.markdown("""
        ### Key Responsive Features
        
        - **Adaptive Layout**: Content automatically adjusts to screen width
        - **Touch-Friendly Controls**: Larger buttons and inputs for touch screens
        - **Optimized Typography**: Readable text sizes on all devices
        - **Mobile Navigation**: Compact menus for smaller screens
        - **Flexible Grids**: Column stacking on narrow screens
        """)
        
        # Demo responsive card
        st.markdown("### Responsive Card Demo")
        
        create_responsive_card(
            title="Highland Tower Development",
            content="This is a responsive card component that adapts to different screen sizes. It will display properly on both desktop and mobile devices."
        )
    
    # Progressive Web App tab
    with tabs[1]:
        st.subheader("Progressive Web App (PWA)")
        
        st.markdown("""
        gcPanel can now function as a Progressive Web App, allowing users to install
        it on their devices and use it offline.
        """)
        
        # PWA features
        st.markdown("""
        ### Key PWA Features
        
        - **Offline Capability**: Access previously loaded data without an internet connection
        - **Install on Home Screen**: Add the app to your device's home screen for quick access
        - **Native-Like Experience**: Full-screen interface without browser chrome
        - **Automatic Updates**: Get the latest features when connected to the internet
        - **Push Notifications**: Receive important project alerts
        """)
        
        # PWA demo
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Install Prompt
            
            Users will see a prompt to install the app on supported devices:
            
            <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-top: 10px;">
                <div style="font-weight: bold;">Add gcPanel to Home Screen</div>
                <div style="margin: 10px 0;">Install this app on your device for quick access.</div>
                <button style="background-color: #3B82F6; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Install</button>
                <button style="background-color: transparent; border: none; padding: 8px 16px; cursor: pointer;">Not Now</button>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            ### Offline Mode
            
            When offline, users will still have access to critical data:
            
            <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; background-color: #fff3cd; margin-top: 10px;">
                <div style="font-weight: bold; margin-bottom: 5px;">You're Offline</div>
                <div>You can still access previously loaded data and some features.</div>
            </div>
            
            <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-top: 10px;">
                <div style="font-weight: bold; margin-bottom: 5px;">Available Offline:</div>
                <ul>
                    <li>Project dashboard (last synced)</li>
                    <li>Document viewer (cached documents)</li>
                    <li>Field notes and checklists</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Field Companion tab
    with tabs[2]:
        st.subheader("Field Companion")
        
        st.markdown("""
        The Field Companion provides specialized mobile-friendly views and functionality
        for construction personnel working on-site.
        """)
        
        # Field Companion features
        st.markdown("""
        ### Key Field Companion Features
        
        - **Quick Actions**: Capture photos, submit daily logs, and complete checklists with one tap
        - **Offline Capabilities**: Continue working without internet connection
        - **Location Awareness**: Tag photos and issues with precise locations
        - **Mobile-First Design**: Optimized for use with gloves and in bright sunlight
        - **Simplified Interface**: Focus on the most needed features in the field
        """)
        
        # Field Companion demo
        col1, col2 = st.columns(2)
        
        with col1:
            st.image("attached_assets/image_1747603048426.png", caption="Field Companion Dashboard", use_column_width=True)
            
            st.markdown("""
            ### Daily Field Log
            
            Quickly document daily activities:
            
            - Weather conditions
            - Workforce present
            - Work completed
            - Materials delivered
            - Equipment used
            - Issues encountered
            - Photo documentation
            """)
        
        with col2:
            st.markdown("""
            ### Quick Actions
            
            Common field tasks accessible with one tap:
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                <div style="background-color: #3B82F6; color: white; padding: 15px; border-radius: 5px; text-align: center;">
                    <div style="font-size: 24px;">📸</div>
                    <div>Capture Photo</div>
                </div>
                <div style="background-color: #3B82F6; color: white; padding: 15px; border-radius: 5px; text-align: center;">
                    <div style="font-size: 24px;">📝</div>
                    <div>Daily Log</div>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div style="background-color: #3B82F6; color: white; padding: 15px; border-radius: 5px; text-align: center;">
                    <div style="font-size: 24px;">✓</div>
                    <div>Checklist</div>
                </div>
                <div style="background-color: #3B82F6; color: white; padding: 15px; border-radius: 5px; text-align: center;">
                    <div style="font-size: 24px;">⚠️</div>
                    <div>Report Issue</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            ### Field Checklist
            
            Complete quality control and safety checklists:
            
            - Pre-pour concrete inspections
            - Safety compliance checks
            - Quality control verification
            - Close-out punch lists
            - Equipment inspections
            """)

def render_collaboration_showcase():
    """Render collaboration tools showcase."""
    st.header("Collaboration Tools")
    
    st.markdown("""
    The new collaboration tools enable real-time teamwork and communication
    directly within gcPanel, improving coordination and productivity.
    """)
    
    # Collaboration features tabs
    tabs = st.tabs([
        "Real-time Chat", 
        "Document Collaboration", 
        "@Mentions & Assignments"
    ])
    
    # Real-time Chat tab
    with tabs[0]:
        st.subheader("Real-time Chat")
        
        st.markdown("""
        Team members can communicate in real-time through the integrated chat system,
        with dedicated channels for different project aspects.
        """)
        
        # Demo chat interface
        # For this showcase, we'll use a simplified version of the actual chat implementation
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 5px; margin-bottom: 15px;">
            <div style="background-color: #f0f0f0; padding: 8px 15px; border-bottom: 1px solid #ddd; font-weight: bold;">
                Project Team Chat
            </div>
            <div style="height: 300px; overflow-y: auto; padding: 10px; background-color: #fff;">
                <div style="margin-bottom: 10px;">
                    <div style="display: inline-block; max-width: 80%; background-color: #f1f1f1; border-radius: 10px; padding: 8px 12px;">
                        <div style="font-size: 0.8em; color: #666; margin-bottom: 3px;">
                            John Smith • Today at 9:30 AM
                        </div>
                        <div>Good morning team! The concrete truck will arrive at 10:30 AM. Please make sure the forms are ready for inspection by 10:00 AM.</div>
                    </div>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <div style="display: inline-block; max-width: 80%; background-color: #f1f1f1; border-radius: 10px; padding: 8px 12px;">
                        <div style="font-size: 0.8em; color: #666; margin-bottom: 3px;">
                            Sarah Johnson • Today at 9:32 AM
                        </div>
                        <div>Got it. The inspection team is on-site and will be ready.</div>
                    </div>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <div style="display: inline-block; max-width: 80%; background-color: #f1f1f1; border-radius: 10px; padding: 8px 12px;">
                        <div style="font-size: 0.8em; color: #666; margin-bottom: 3px;">
                            Mike Chen • Today at 9:45 AM
                        </div>
                        <div>We need to discuss the revised drawings for the 14th floor. The client requested some changes to the layout. <span style="color: #3B82F6; font-weight: bold;">@Sarah Johnson</span> can you review them before our 2:00 PM meeting?</div>
                    </div>
                </div>
                
                <div style="margin-bottom: 10px; text-align: right;">
                    <div style="display: inline-block; max-width: 80%; background-color: #e2f0fd; border-radius: 10px; padding: 8px 12px;">
                        <div style="font-size: 0.8em; color: #666; margin-bottom: 3px;">
                            You • Just now
                        </div>
                        <div>I'll be on-site in 15 minutes. Let me know if there's anything else we need to prepare for the concrete pour.</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Message input
        st.text_input("Type a message", placeholder="Type your message here...")
        
        col1, col2 = st.columns([4, 1])
        
        with col2:
            st.button("Send")
        
        # Chat features
        st.markdown("""
        ### Key Chat Features
        
        - **Real-time Messaging**: Instant communication between team members
        - **Chat Channels**: Dedicated channels for different topics and teams
        - **File Sharing**: Share documents and photos directly in the chat
        - **Message History**: Searchable history of all conversations
        - **Presence Indicators**: See who's online and available
        - **Mobile Notifications**: Receive alerts on your mobile device
        """)
    
    # Document Collaboration tab
    with tabs[1]:
        st.subheader("Document Collaboration")
        
        st.markdown("""
        Team members can collaborate on documents with comments, suggestions,
        and real-time editing capabilities.
        """)
        
        # Document collaboration demo
        # For this showcase, we'll use a simplified version of the actual implementation
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px;">
            <h3>Highland Tower Foundation Specifications</h3>
            <div style="display: flex; margin-bottom: 10px;">
                <div style="margin-right: 15px; display: flex; align-items: center;">
                    <div style="width: 10px; height: 10px; border-radius: 50%; background-color: green; margin-right: 5px;"></div>
                    <div style="font-size: 0.9em;">3 viewers</div>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 10px; height: 10px; border-radius: 50%; background-color: orange; margin-right: 5px;"></div>
                    <div style="font-size: 0.9em;">Last edit: 5m ago</div>
                </div>
            </div>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
                <p><strong>Foundation Specifications for Highland Tower</strong></p>
                <p>The foundation consists of a reinforced concrete mat slab with a thickness of 1.2m.</p>
                <p>Concrete strength: 45 MPa at 28 days.</p>
                <p>Reinforcement: #11 bars at 25cm on center each way.</p>
                <p>Waterproofing: <span style="background-color: #ffeb3b; padding: 0 2px;">Bentonite waterproofing system</span> with drainage layer.</p>
                <p>Foundation depth: 12m below street level.</p>
            </div>
            
            <h4>Comments</h4>
            
            <div style="margin-bottom: 15px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <div style="width: 30px; height: 30px; border-radius: 50%; background-color: #3B82F6; color: white; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                        MC
                    </div>
                    <div>
                        <div style="font-weight: bold;">Mike Chen</div>
                        <div style="font-size: 0.8em; color: #666;">Yesterday at 2:30 PM</div>
                    </div>
                </div>
                <div style="margin-bottom: 10px;">We need to verify if bentonite waterproofing is appropriate given the high water table in this area. <span style="color: #3B82F6; font-weight: bold;">@Sarah Johnson</span> can you confirm with the geotechnical engineer?</div>
                
                <div style="margin-left: 40px; margin-bottom: 15px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #f0f0f0;">
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <div style="width: 30px; height: 30px; border-radius: 50%; background-color: #3B82F6; color: white; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                            SJ
                        </div>
                        <div>
                            <div style="font-weight: bold;">Sarah Johnson</div>
                            <div style="font-size: 0.8em; color: #666;">Today at 9:15 AM</div>
                        </div>
                    </div>
                    <div>I've confirmed with the geotechnical engineer. They recommend adding a secondary membrane waterproofing system in addition to the bentonite. I'll update the specs accordingly.</div>
                </div>
            </div>
            
            <div style="margin-bottom: 15px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <div style="width: 30px; height: 30px; border-radius: 50%; background-color: #3B82F6; color: white; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                        JS
                    </div>
                    <div>
                        <div style="font-weight: bold;">John Smith</div>
                        <div style="font-size: 0.8em; color: #666;">Today at 10:30 AM</div>
                    </div>
                </div>
                <div>Please update the concrete strength specification to include the early strength requirement of 20 MPa at 7 days as well.</div>
            </div>
            
            <h4>Add Comment</h4>
            <textarea style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; margin-bottom: 10px;" placeholder="Write a comment..."></textarea>
            <button style="background-color: #3B82F6; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Post Comment</button>
        </div>
        """, unsafe_allow_html=True)
        
        # Document collaboration features
        st.markdown("""
        ### Key Document Collaboration Features
        
        - **Commenting**: Add comments to specific sections of documents
        - **Threaded Discussions**: Organize discussions with nested replies
        - **Tracked Changes**: See who changed what and when
        - **Version History**: Access previous versions of documents
        - **Real-time Co-editing**: Multiple users can edit simultaneously
        - **Approval Workflows**: Request and track document approvals
        """)
    
    # @Mentions & Assignments tab
    with tabs[2]:
        st.subheader("@Mentions & Assignments")
        
        st.markdown("""
        Tag team members in comments and discussions, and assign tasks directly
        within the context of project documents and conversations.
        """)
        
        # @Mentions demo
        st.markdown("""
        ### @Mentions
        
        Tag team members to get their attention:
        
        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px; background-color: #f9f9f9;">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="width: 30px; height: 30px; border-radius: 50%; background-color: #3B82F6; color: white; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                    MC
                </div>
                <div>
                    <div style="font-weight: bold;">Mike Chen</div>
                    <div style="font-size: 0.8em; color: #666;">Today at 11:15 AM</div>
                </div>
            </div>
            <div>
                I've updated the structural drawings for the 12th floor based on the architect's revisions. 
                <span style="color: #3B82F6; font-weight: bold;">@John Smith</span> please review the changes to make sure they align with the MEP requirements. 
                <span style="color: #3B82F6; font-weight: bold;">@Sarah Johnson</span> we'll need to update the schedule to accommodate these changes.
            </div>
        </div>
        
        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 15px; background-color: #e2f0fd;">
            <div style="display: flex; align-items: center;">
                <div style="width: 30px; height: 30px; border-radius: 50%; background-color: #3B82F6; color: white; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                    🔔
                </div>
                <div>
                    <div><strong>Mention Notification</strong></div>
                    <div>Mike Chen mentioned you in a comment on "Structural Drawings - Floor 12"</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Task assignments demo
        st.markdown("""
        ### Task Assignments
        
        Assign tasks directly within context:
        
        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px;">
            <h4>Task Assignment</h4>
            
            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                <div style="font-weight: bold; margin-bottom: 5px;">Review Structural Changes - Floor 12</div>
                <div style="margin-bottom: 5px;">Review the updated structural drawings for the 12th floor to ensure they align with MEP requirements.</div>
                <div style="display: flex; margin-top: 10px;">
                    <div style="margin-right: 15px;">
                        <div style="font-size: 0.8em; color: #666;">Assigned To</div>
                        <div>John Smith</div>
                    </div>
                    <div style="margin-right: 15px;">
                        <div style="font-size: 0.8em; color: #666;">Due Date</div>
                        <div>May 20, 2025</div>
                    </div>
                    <div>
                        <div style="font-size: 0.8em; color: #666;">Priority</div>
                        <div>High</div>
                    </div>
                </div>
            </div>
            
            <h4>Assignment Actions</h4>
            <div style="display: flex; gap: 10px;">
                <button style="background-color: #3B82F6; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Accept</button>
                <button style="background-color: transparent; border: 1px solid #3B82F6; color: #3B82F6; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Request Changes</button>
                <button style="background-color: transparent; border: 1px solid #ddd; color: #666; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Reassign</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Features list
        st.markdown("""
        ### Key @Mentions & Assignment Features
        
        - **@Mentions**: Tag specific team members in comments and discussions
        - **Notifications**: Receive alerts when mentioned or assigned a task
        - **Contextual Assignments**: Create tasks directly within relevant content
        - **Task Tracking**: Monitor assignment status and progress
        - **Due Dates & Priorities**: Set task importance and deadlines
        - **Integration**: Connect with project schedule and task lists
        """)

def render_ai_showcase():
    """Render AI-powered features showcase."""
    st.header("AI-Powered Features")
    
    st.markdown("""
    gcPanel now incorporates artificial intelligence to enhance productivity,
    improve data access, and provide intelligent insights.
    """)
    
    # AI features tabs
    tabs = st.tabs([
        "Smart Document Search", 
        "Predictive Typing", 
        "Intelligent Alerts"
    ])
    
    # Smart Document Search tab
    with tabs[0]:
        st.subheader("Smart Document Search")
        
        st.markdown("""
        The smart document search uses natural language processing to help you
        find the exact documents you need, even if you don't know the precise keywords.
        """)
        
        # Document search demo
        st.text_input(
            "Search documents in natural language",
            placeholder="e.g., 'Find foundation specs for Highland Tower'"
        )
        
        st.radio("Search method", ["Basic", "Semantic (AI-powered)"], horizontal=True)
        
        # Sample search results
        st.markdown("### Search Results")
        
        with st.expander("Highland Tower Foundation Specifications (Specification)"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("**Author:** John Smith")
                st.markdown("**Last Updated:** 2025-01-10")
                st.markdown("**Status:** Approved (v2.1)")
            
            with col2:
                st.markdown("**Tags:**")
                st.markdown("""
                <span style="background-color: #e1e1e1; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em;">foundation</span>
                <span style="background-color: #e1e1e1; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em;">structural</span>
                <span style="background-color: #e1e1e1; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em;">specifications</span>
                """, unsafe_allow_html=True)
            
            st.markdown("**Content:**")
            st.text("""
This document details the foundation specifications for the Highland Tower project.
The foundation consists of a reinforced concrete mat slab with a thickness of 1.2m.
Concrete strength: 45 MPa at 28 days.
Reinforcement: #11 bars at 25cm on center each way.
Waterproofing: Bentonite waterproofing system with drainage layer.
Foundation depth: 12m below street level.
            """)
            
            st.button("Extract Key Information", key="extract_doc1")
        
        with st.expander("Highland Tower Structural Analysis Report (Report)"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("**Author:** Mike Chen")
                st.markdown("**Last Updated:** 2025-03-15")
                st.markdown("**Status:** Final (v3.0)")
            
            with col2:
                st.markdown("**Tags:**")
                st.markdown("""
                <span style="background-color: #e1e1e1; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em;">structural</span>
                <span style="background-color: #e1e1e1; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em;">analysis</span>
                <span style="background-color: #e1e1e1; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em;">engineering</span>
                """, unsafe_allow_html=True)
            
            st.markdown("**Content:**")
            st.text("""
Structural analysis report for Highland Tower:
The building has been analyzed for wind loads up to 150 mph and seismic loads per local code.
Lateral force resisting system: Concrete shear walls with coupling beams.
Floor system: 8" post-tensioned concrete slabs with 5ksi concrete.
Column layout: 30'x30' typical bay size with 24"x24" columns at lower levels.
Drift ratio: Maximum of 1/500 under service wind loads.
The analysis confirms that the structural system meets all code requirements with adequate safety factors.
            """)
        
        # Search features
        st.markdown("""
        ### Key Search Features
        
        - **Natural Language Queries**: Search using plain English questions
        - **Semantic Understanding**: Find documents based on concepts, not just keywords
        - **Content Analysis**: Extract key information from documents
        - **Advanced Filters**: Refine search by document type, author, date, etc.
        - **Search History**: Quick access to previous searches
        - **Relevance Ranking**: Most relevant documents appear first
        """)
    
    # Predictive Typing tab
    with tabs[1]:
        st.subheader("Predictive Typing")
        
        st.markdown("""
        The predictive typing feature suggests completions as you type,
        saving time and ensuring consistency across project documentation.
        """)
        
        # Predictive typing demo
        predictive_typing = PredictiveTyping()
        
        st.markdown("### Form Field Suggestions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = predictive_typing.render_predictive_input(
                "Name",
                "person_name",
                placeholder="Start typing a name..."
            )
        
        with col2:
            company = predictive_typing.render_predictive_input(
                "Company",
                "company",
                placeholder="Start typing a company name..."
            )
        
        location = predictive_typing.render_predictive_input(
            "Location",
            "location",
            placeholder="Start typing a location..."
        )
        
        st.markdown("### Document Text Suggestions")
        
        description = predictive_typing.render_predictive_textarea(
            "Description",
            "description",
            placeholder="Start typing a description...",
            height=150
        )
        
        # Predictive typing features
        st.markdown("""
        ### Key Predictive Typing Features
        
        - **Contextual Suggestions**: Suggestions based on the current field
        - **Learning System**: Improves suggestions based on usage patterns
        - **Common Phrases**: Quick insertion of frequently used text
        - **Consistency**: Ensures standardized terminology across the project
        - **Time Saving**: Reduces typing effort and errors
        - **Mobile Support**: Works on mobile devices for field personnel
        """)
    
    # Intelligent Alerts tab
    with tabs[2]:
        st.subheader("Intelligent Alerts")
        
        st.markdown("""
        The intelligent alerts system analyzes project data to identify potential issues
        and opportunities, providing proactive notifications to the team.
        """)
        
        # Intelligent alerts demo
        intelligent_alerts = IntelligentAlerts()
        
        # Get counts by priority
        high_count = len(intelligent_alerts.alerts.get("high_priority", []))
        medium_count = len(intelligent_alerts.alerts.get("medium_priority", []))
        low_count = len(intelligent_alerts.alerts.get("low_priority", []))
        total_count = high_count + medium_count + low_count
        
        # Display summary
        st.markdown("### Alert Summary")
        
        # Create metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Alerts", total_count)
        
        with col2:
            st.metric(
                "High Priority", 
                high_count, 
                delta=f"{high_count} active", 
                delta_color="inverse" if high_count > 0 else "normal"
            )
        
        with col3:
            st.metric("Medium Priority", medium_count)
        
        with col4:
            st.metric("Low Priority", low_count)
        
        # Display sample alerts
        st.markdown("### Current Alerts")
        
        with st.expander("Critical Path Delay Risk (High Impact)"):
            st.markdown("""
            <div style="background-color: #f8d7da; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                <div style="font-weight: bold; margin-bottom: 5px;">Critical Path Delay Risk</div>
                <div style="margin-bottom: 10px;">The curtain wall installation is 3 days behind schedule, which may impact the building envelope completion milestone.</div>
                <div style="font-size: 0.9em; margin-bottom: 5px;"><b>Affected Areas:</b> Floors 8-12, Building Envelope</div>
                <div style="font-size: 0.9em; margin-bottom: 5px;"><b>Recommendation:</b> Authorize overtime work for the glazing contractor to accelerate installation.</div>
                <div style="font-size: 0.8em; color: #666;">Generated: 2025-05-16</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.button("Dismiss", key="dismiss_alert1")
            
            with col2:
                st.button("Assign", key="assign_alert1")
            
            with col3:
                st.button("View Details", key="details_alert1")
        
        with st.expander("MEP Budget Risk (High Impact)"):
            st.markdown("""
            <div style="background-color: #f8d7da; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                <div style="font-weight: bold; margin-bottom: 5px;">MEP Budget Risk</div>
                <div style="margin-bottom: 10px;">The MEP package is trending 7.5% over budget due to material price increases and additional scope.</div>
                <div style="font-size: 0.9em; margin-bottom: 5px;"><b>Affected Areas:</b> MEP Systems, Budget</div>
                <div style="font-size: 0.9em; margin-bottom: 5px;"><b>Recommendation:</b> Review value engineering options for the mechanical systems on floors 10-15.</div>
                <div style="font-size: 0.8em; color: #666;">Generated: 2025-05-15</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Intelligent alerts features
        st.markdown("""
        ### Key Intelligent Alert Features
        
        - **Proactive Monitoring**: Continuous analysis of project data
        - **Risk Identification**: Early detection of potential issues
        - **Prioritization**: Alerts categorized by impact and urgency
        - **Actionable Recommendations**: Specific suggestions for addressing issues
        - **Assignment**: Delegate alert resolution to team members
        - **Tracking**: Monitor alert status and resolution
        """)

        # Pattern detection explanation
        with st.expander("How Alert Patterns Are Detected"):
            st.markdown("""
            The system analyzes patterns in project data to identify potential issues:
            
            1. **Schedule Analysis**: Compares planned vs. actual progress to detect delays
            2. **Budget Monitoring**: Tracks spending rates and forecasts potential overruns
            3. **Quality Metrics**: Identifies recurring issues in specific areas or trades
            4. **Weather Impact**: Correlates weather forecasts with scheduled activities
            5. **Resource Allocation**: Detects potential resource conflicts or shortages
            6. **Safety Indicators**: Recognizes patterns that may lead to safety incidents
            """)
        
        # AI model details
        with st.expander("AI Model Information"):
            st.markdown("""
            The intelligent alerts system uses several AI techniques:
            
            - **Regression Models**: For budget and schedule forecasting
            - **Pattern Recognition**: To identify recurring issues
            - **Anomaly Detection**: To spot unusual project behavior
            - **Natural Language Processing**: To extract insights from text reports
            - **Classification Algorithms**: To categorize and prioritize alerts
            
            The models are trained on historical project data and continuously improve
            as they process more information from current projects.
            """)