"""
Project Information module for the gcPanel Construction Management Dashboard.

This module provides project information display and editing functionality
for the single-project focused platform.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import random
from components.project_forms import project_edit_form

def render_project_information():
    """Render the project information interface for the selected project."""
    st.header("Project Information")
    
    # Get the current project (in a real app, this would be loaded from database)
    project_name = st.session_state.get('current_project', 'Highland Tower Development')
    
    # Tabs for different project information sections
    tabs = st.tabs(["Overview", "Team", "Schedule", "Documents", "Photos", "Settings"])
    
    with tabs[0]:
        render_project_overview()
    
    with tabs[1]:
        render_project_team()
    
    with tabs[2]:
        render_project_schedule()
    
    with tabs[3]:
        render_project_documents()
    
    with tabs[4]:
        render_project_photos()
    
    with tabs[5]:
        render_project_settings()

def render_project_overview():
    """Render project overview information."""
    # Get the current project data (in a real app, this would be loaded from database)
    project_data = get_sample_project_data()
    
    # Project header with title and status
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(project_data["name"])
        st.caption(f"Project Code: {project_data['code']}")
    
    with col2:
        status_colors = {
            "Planning": "#f59e0b",
            "Preconstruction": "#3e79f7",
            "Active": "#38d39f",
            "On Hold": "#ff5b5b",
            "Closed": "#6c757d"
        }
        
        status_color = status_colors.get(project_data["status"], "#6c757d")
        
        st.markdown(f"""
        <div style="text-align: right;">
            <div style="display: inline-block; background-color: {status_color}20; color: {status_color}; 
                        padding: 4px 12px; border-radius: 16px; font-size: 14px; font-weight: 500;">
                {project_data["status"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Project main information card
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    
    # Project image/map
    st.image("https://placehold.co/800x300/e9ecef/495057?text=Project+Image", use_column_width=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate days elapsed and remaining
    start_date = project_data["start_date"]
    end_date = project_data["end_date"]
    today = date.today()
    
    total_days = (end_date - start_date).days
    days_elapsed = (today - start_date).days
    days_remaining = (end_date - today).days
    
    # Calculate completion percentage
    completion_pct = min(100, max(0, (days_elapsed / total_days * 100))) if total_days > 0 else 0
    time_progress_pct = min(100, max(0, (days_elapsed / total_days * 100))) if total_days > 0 else 0
    
    # Budget progress
    budget_spent = 3650000  # Sample data
    budget_total = project_data["total_budget"]
    budget_progress_pct = (budget_spent / budget_total * 100) if budget_total > 0 else 0
    
    # Cost Performance Index (CPI) - sample data
    cpi = 1.05  # >1 means under budget, <1 means over budget
    
    with col1:
        st.metric(label="Project Completion", value="42%")
    
    with col2:
        st.metric(label="Time Progress", value=f"{time_progress_pct:.1f}%")
    
    with col3:
        # We can't directly set colors with st.metric, but we can use delta to indicate positive/negative
        delta = "On budget" if cpi >= 1.0 else "Over budget"
        delta_color = "normal" if cpi >= 1.0 else "inverse"
        st.metric(label="Cost Performance", value=f"{cpi:.2f}", delta=delta, delta_color=delta_color)
    
    with col4:
        # For days remaining, use appropriate delta indicators
        if days_remaining > 30:
            delta = "On schedule"
            delta_color = "normal"
        elif days_remaining > 0:
            delta = "Approaching deadline"
            delta_color = "off"
        else:
            delta = "Past deadline"
            delta_color = "inverse"
        
        st.metric(label="Days Remaining", value=days_remaining, delta=delta, delta_color=delta_color)
    
    # Project details in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Project Details")
        
        details = [
            {"label": "Client", "value": project_data["client"]},
            {"label": "Type", "value": project_data["type"]},
            {"label": "Location", "value": f"{project_data['address']}, {project_data['location']}"},
            {"label": "Start Date", "value": project_data["start_date"].strftime("%B %d, %Y")},
            {"label": "End Date", "value": project_data["end_date"].strftime("%B %d, %Y")},
            {"label": "Duration", "value": f"{project_data['duration']} days"}
        ]
        
        # Display details with subtle styling
        for detail in details:
            col_label, col_value = st.columns([1, 2])
            with col_label:
                st.markdown(f"**{detail['label']}:**")
            with col_value:
                st.markdown(f"{detail['value']}")
    
    with col2:
        st.markdown("### Budget Information")
        
        # Budget progress bar
        st.markdown("**Budget Progress**")
        st.progress(budget_progress_pct / 100)
        st.markdown(f"**${budget_spent:,.0f}** of **${budget_total:,.0f}** ({budget_progress_pct:.1f}%)")
        
        # Budget details
        budget_details = [
            {"label": "Base Budget", "value": f"${project_data['base_budget']:,.0f}"},
            {"label": "Contingency", "value": f"${project_data['contingency_amount']:,.0f} ({project_data['contingency_percent']}%)"},
            {"label": "Total Budget", "value": f"${project_data['total_budget']:,.0f}"},
            {"label": "Contract Type", "value": project_data["contract_type"]},
            {"label": "Payment Terms", "value": project_data["payment_terms"]}
        ]
        
        # Display budget details
        for detail in budget_details:
            col_label, col_value = st.columns([1, 2])
            with col_label:
                st.markdown(f"**{detail['label']}:**")
            with col_value:
                st.markdown(f"{detail['value']}")
    
    # Project description
    st.markdown("### Description")
    st.markdown(project_data["description"])
    
    # Edit project button
    if st.button("Edit Project Information", key="edit_project_btn", type="primary"):
        st.session_state.edit_project = True
    
    # Show edit form if requested
    if st.session_state.get("edit_project", False):
        with st.form("edit_project_modal"):
            st.subheader("Edit Project Information")
            
            # Basic project fields to edit
            st.text_input("Project Name", value=project_data["name"], key="edit_name")
            st.text_input("Client", value=project_data["client"], key="edit_client")
            st.text_area("Description", value=project_data["description"], key="edit_description")
            st.selectbox("Status", options=["Planning", "Preconstruction", "Active", "On Hold", "Closed"], 
                          index=["Planning", "Preconstruction", "Active", "On Hold", "Closed"].index(project_data["status"]),
                          key="edit_status")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Save Changes", type="primary")
            with col2:
                cancelled = st.form_submit_button("Cancel")
            
            if submitted:
                st.success("Project information updated successfully!")
                st.session_state.edit_project = False
                # Here you would update the project in the database
            
            if cancelled:
                st.session_state.edit_project = False
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Project stats and charts
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    
    st.subheader("Project Analytics")
    
    # Create a row of charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Budget Distribution")
        
        # Sample budget distribution data
        budget_categories = {
            "General Requirements": 275000,
            "Site Work": 425000,
            "Concrete": 625000,
            "Masonry": 350000,
            "Metals": 550000,
            "Woodwork": 275000,
            "Thermal & Moisture": 450000,
            "Doors & Windows": 325000,
            "Finishes": 575000,
            "Specialties": 125000,
            "Equipment": 175000,
            "Furnishings": 125000,
            "MEP": 825000,
            "Overhead & Profit": 500000
        }
        
        # Convert to DataFrame for visualization
        budget_df = pd.DataFrame({
            "Category": budget_categories.keys(),
            "Amount": budget_categories.values()
        })
        
        # Generate color gradient for the chart
        color_scale = ["#3e79f7", "#5584f7", "#6c90f8", "#849bf8", "#9ba7f9", "#b3b3f9", "#cabffa", "#e1cafa", "#f9d6fb", "#fce2ec", "#ffeddc", "#fff9cc", "#e6ffcc", "#ccffcc"]
        
        # Create horizontal bar chart with colors
        budget_df = budget_df.sort_values("Amount", ascending=True)
        st.bar_chart(budget_df.set_index("Category"))
    
    with col2:
        st.markdown("#### Schedule Performance")
        
        # Sample schedule data for an S-curve
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        planned_progress = [5, 12, 20, 29, 39, 50, 62, 73, 84, 92, 97, 100]
        actual_progress = [4, 10, 18, 27, 38, 42, None, None, None, None, None, None]  # Only up to current month
        
        # Convert to DataFrame
        schedule_df = pd.DataFrame({
            "Month": months,
            "Planned": planned_progress,
            "Actual": actual_progress
        })
        
        # Convert to format suitable for Streamlit's line chart
        chart_data = pd.DataFrame({
            "Planned": schedule_df["Planned"],
            "Actual": schedule_df["Actual"]
        }, index=schedule_df["Month"])
        
        # Draw the line chart
        st.line_chart(chart_data)
    
    # Add a risk matrix visualization with colors
    st.markdown("#### Project Risk Matrix")
    
    # Sample risk data
    risks = [
        {"id": 1, "name": "Weather Delays", "probability": "Medium", "impact": "Medium", "status": "Monitored"},
        {"id": 2, "name": "Material Shortages", "probability": "High", "impact": "High", "status": "Mitigating"},
        {"id": 3, "name": "Labor Availability", "probability": "Medium", "impact": "High", "status": "Mitigating"},
        {"id": 4, "name": "Permit Delays", "probability": "Low", "impact": "High", "status": "Resolved"},
        {"id": 5, "name": "Design Changes", "probability": "Medium", "impact": "Medium", "status": "Monitored"},
        {"id": 6, "name": "Site Access Issues", "probability": "Low", "impact": "Medium", "status": "Monitored"},
        {"id": 7, "name": "Subcontractor Default", "probability": "Low", "impact": "High", "status": "Monitored"},
        {"id": 8, "name": "Budget Overruns", "probability": "Medium", "impact": "High", "status": "Mitigating"}
    ]
    
    # Create a matrix visualization
    st.markdown("##### Risk Level")
    
    # Create the risk matrix
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Risk matrix grid
        grid_html = """
        <div style="display: grid; grid-template-columns: 50px repeat(3, 1fr); grid-template-rows: 50px repeat(3, 1fr); gap: 2px; margin-bottom: 20px;">
            <!-- Header row -->
            <div style="grid-column: 1; grid-row: 1; display: flex; align-items: center; justify-content: center;"></div>
            <div style="grid-column: 2; grid-row: 1; display: flex; align-items: center; justify-content: center; font-weight: 500;">Low</div>
            <div style="grid-column: 3; grid-row: 1; display: flex; align-items: center; justify-content: center; font-weight: 500;">Medium</div>
            <div style="grid-column: 4; grid-row: 1; display: flex; align-items: center; justify-content: center; font-weight: 500;">High</div>
            
            <!-- Left column -->
            <div style="grid-column: 1; grid-row: 2; display: flex; align-items: center; justify-content: center; writing-mode: vertical-rl; transform: rotate(180deg); font-weight: 500;">High</div>
            <div style="grid-column: 1; grid-row: 3; display: flex; align-items: center; justify-content: center; writing-mode: vertical-rl; transform: rotate(180deg); font-weight: 500;">Medium</div>
            <div style="grid-column: 1; grid-row: 4; display: flex; align-items: center; justify-content: center; writing-mode: vertical-rl; transform: rotate(180deg); font-weight: 500;">Low</div>
            
            <!-- Matrix cells -->
            <div style="grid-column: 2; grid-row: 4; background-color: #38d39f40; height: 100px; display: flex; align-items: center; justify-content: center; border-radius: 4px; padding: 5px; color: #0f5132;">Low Risk</div>
            <div style="grid-column: 3; grid-row: 4; background-color: #38d39f40; height: 100px; display: flex; align-items: center; justify-content: center; border-radius: 4px; padding: 5px; color: #0f5132;">Low Risk</div>
            <div style="grid-column: 4; grid-row: 4; background-color: #f9c85140; height: 100px; display: flex; align-items: center; justify-content: center; border-radius: 4px; padding: 5px; color: #664d03;">Medium Risk</div>
            
            <div style="grid-column: 2; grid-row: 3; background-color: #38d39f40; height: 100px; display: flex; align-items: center; justify-content: center; border-radius: 4px; padding: 5px; color: #0f5132;">Low Risk</div>
            <div style="grid-column: 3; grid-row: 3; background-color: #f9c85140; height: 100px; display: flex; align-items: center; justify-content: center; border-radius: 4px; padding: 5px; color: #664d03;">Medium Risk</div>
            <div style="grid-column: 4; grid-row: 3; background-color: #ff5b5b40; height: 100px; display: flex; align-items: center; justify-content: center; border-radius: 4px; padding: 5px; color: #842029;">High Risk</div>
            
            <div style="grid-column: 2; grid-row: 2; background-color: #f9c85140; height: 100px; display: flex; align-items: center; justify-content: center; border-radius: 4px; padding: 5px; color: #664d03;">Medium Risk</div>
            <div style="grid-column: 3; grid-row: 2; background-color: #ff5b5b40; height: 100px; display: flex; align-items: center; justify-content: center; border-radius: 4px; padding: 5px; color: #842029;">High Risk</div>
            <div style="grid-column: 4; grid-row: 2; background-color: #ff5b5b40; height: 100px; display: flex; align-items: center; justify-content: center; border-radius: 4px; padding: 5px; color: #842029;">High Risk</div>
        </div>
        
        <div style="display: flex; justify-content: center; margin-bottom: 10px; font-weight: 500;">Impact</div>
        <div style="position: absolute; left: 0; top: 50%; transform: rotate(-90deg) translateY(-50%); transform-origin: left center; font-weight: 500; margin-left: -35px;">Probability</div>
        """
        
        st.markdown(grid_html, unsafe_allow_html=True)
    
    # Risk list with colored indicators
    st.markdown("##### Risk Register")
    
    # Create a colored risk table
    risk_df = pd.DataFrame(risks)
    
    # Add color coding
    def get_risk_level(probability, impact):
        if probability == "High" and impact == "High":
            return "High Risk"
        elif probability == "High" and impact == "Medium":
            return "High Risk"
        elif probability == "Medium" and impact == "High":
            return "High Risk"
        elif probability == "Medium" and impact == "Medium":
            return "Medium Risk"
        elif probability == "Low" and impact == "High":
            return "Medium Risk"
        elif probability == "High" and impact == "Low":
            return "Medium Risk"
        elif probability == "Medium" and impact == "Low":
            return "Low Risk"
        elif probability == "Low" and impact == "Medium":
            return "Low Risk"
        else:
            return "Low Risk"
    
    # Calculate risk level and color
    risk_df["Risk Level"] = risk_df.apply(lambda row: get_risk_level(row["probability"], row["impact"]), axis=1)
    
    # Create styled table
    risk_table_html = """
    <table style="width:100%; border-collapse: collapse; margin-bottom: 20px;">
        <thead>
            <tr style="background-color: #f8f9fa; border-bottom: 2px solid #dee2e6;">
                <th style="padding: 10px; text-align: left;">ID</th>
                <th style="padding: 10px; text-align: left;">Risk</th>
                <th style="padding: 10px; text-align: left;">Probability</th>
                <th style="padding: 10px; text-align: left;">Impact</th>
                <th style="padding: 10px; text-align: left;">Risk Level</th>
                <th style="padding: 10px; text-align: left;">Status</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for _, risk in risk_df.iterrows():
        # Determine colors based on risk level
        if risk["Risk Level"] == "High Risk":
            level_color = "#ff5b5b"
            level_bg = "#ff5b5b20"
        elif risk["Risk Level"] == "Medium Risk":
            level_color = "#f9c851"
            level_bg = "#f9c85120"
        else:
            level_color = "#38d39f"
            level_bg = "#38d39f20"
        
        # Determine status color
        if risk["status"] == "Mitigating":
            status_color = "#3e79f7"
            status_bg = "#3e79f720"
        elif risk["status"] == "Resolved":
            status_color = "#38d39f"
            status_bg = "#38d39f20"
        else:
            status_color = "#f9c851"
            status_bg = "#f9c85120"
        
        risk_table_html += f"""
        <tr style="border-bottom: 1px solid #dee2e6;">
            <td style="padding: 10px;">{risk['id']}</td>
            <td style="padding: 10px;">{risk['name']}</td>
            <td style="padding: 10px;">{risk['probability']}</td>
            <td style="padding: 10px;">{risk['impact']}</td>
            <td style="padding: 10px;">
                <span style="background-color: {level_bg}; color: {level_color}; padding: 3px 8px; border-radius: 12px; font-size: 12px;">
                    {risk['Risk Level']}
                </span>
            </td>
            <td style="padding: 10px;">
                <span style="background-color: {status_bg}; color: {status_color}; padding: 3px 8px; border-radius: 12px; font-size: 12px;">
                    {risk['status']}
                </span>
            </td>
        </tr>
        """
    
    risk_table_html += """
        </tbody>
    </table>
    """
    
    st.markdown(risk_table_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_project_team():
    """Render project team information."""
    st.subheader("Project Team")
    
    # Team organization card
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    
    # Project team chart
    st.markdown("### Project Organization")
    
    # Team structure visualization - could be replaced with a more advanced org chart
    org_chart_html = """
    <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 30px;">
        <!-- Project Manager Level -->
        <div style="margin-bottom: 20px;">
            <div style="width: 180px; padding: 15px; background-color: #3e79f720; border: 2px solid #3e79f7; border-radius: 8px; text-align: center;">
                <div style="font-weight: 500; color: #3e79f7;">Project Manager</div>
                <div>John Smith</div>
            </div>
        </div>
        
        <!-- Level 2 -->
        <div style="position: relative; width: 100%; height: 20px;">
            <div style="position: absolute; left: 50%; top: 0; width: 2px; height: 20px; background-color: #3e79f7;"></div>
        </div>
        
        <div style="display: flex; justify-content: space-around; width: 100%; margin-bottom: 20px;">
            <div style="width: 160px; padding: 10px; background-color: #38d39f20; border: 2px solid #38d39f; border-radius: 8px; text-align: center;">
                <div style="font-weight: 500; color: #38d39f;">Superintendent</div>
                <div>Mike Johnson</div>
            </div>
            
            <div style="width: 160px; padding: 10px; background-color: #f9c85120; border: 2px solid #f9c851; border-radius: 8px; text-align: center;">
                <div style="font-weight: 500; color: #f9c851;">Project Engineer</div>
                <div>Sarah Williams</div>
            </div>
            
            <div style="width: 160px; padding: 10px; background-color: #ff5b5b20; border: 2px solid #ff5b5b; border-radius: 8px; text-align: center;">
                <div style="font-weight: 500; color: #ff5b5b;">Project Controls</div>
                <div>David Chen</div>
            </div>
        </div>
        
        <!-- Level 3 -->
        <div style="position: relative; width: 100%; height: 20px;">
            <div style="position: absolute; left: 20%; top: 0; width: 2px; height: 20px; background-color: #38d39f;"></div>
            <div style="position: absolute; left: 50%; top: 0; width: 2px; height: 20px; background-color: #f9c851;"></div>
            <div style="position: absolute; left: 80%; top: 0; width: 2px; height: 20px; background-color: #ff5b5b;"></div>
        </div>
        
        <div style="display: flex; justify-content: space-around; width: 100%;">
            <div style="width: 140px; padding: 8px; background-color: #38d39f15; border: 1px solid #38d39f; border-radius: 8px; text-align: center;">
                <div style="font-weight: 500; color: #38d39f;">Asst. Super</div>
                <div>Tom Rodriguez</div>
            </div>
            
            <div style="width: 140px; padding: 8px; background-color: #f9c85115; border: 1px solid #f9c851; border-radius: 8px; text-align: center;">
                <div style="font-weight: 500; color: #f9c851;">Field Engineer</div>
                <div>Emily Taylor</div>
            </div>
            
            <div style="width: 140px; padding: 8px; background-color: #f9c85115; border: 1px solid #f9c851; border-radius: 8px; text-align: center;">
                <div style="font-weight: 500; color: #f9c851;">MEP Coordinator</div>
                <div>Robert Lee</div>
            </div>
            
            <div style="width: 140px; padding: 8px; background-color: #ff5b5b15; border: 1px solid #ff5b5b; border-radius: 8px; text-align: center;">
                <div style="font-weight: 500; color: #ff5b5b;">Cost Engineer</div>
                <div>Lisa Martinez</div>
            </div>
        </div>
    </div>
    """
    
    st.markdown(org_chart_html, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.15;'>", unsafe_allow_html=True)
    
    # Team members table with colorful role indicators
    st.markdown("### Team Directory")
    
    # Sample team data
    team_members = [
        {"name": "John Smith", "role": "Project Manager", "company": "Highland Construction", "email": "john.smith@highland.com", "phone": "(555) 123-4567"},
        {"name": "Mike Johnson", "role": "Superintendent", "company": "Highland Construction", "email": "mike.johnson@highland.com", "phone": "(555) 234-5678"},
        {"name": "Sarah Williams", "role": "Project Engineer", "company": "Highland Construction", "email": "sarah.williams@highland.com", "phone": "(555) 345-6789"},
        {"name": "David Chen", "role": "Project Controls", "company": "Highland Construction", "email": "david.chen@highland.com", "phone": "(555) 456-7890"},
        {"name": "Emily Taylor", "role": "Field Engineer", "company": "Highland Construction", "email": "emily.taylor@highland.com", "phone": "(555) 567-8901"},
        {"name": "Robert Lee", "role": "MEP Coordinator", "company": "Highland Construction", "email": "robert.lee@highland.com", "phone": "(555) 678-9012"},
        {"name": "Lisa Martinez", "role": "Cost Engineer", "company": "Highland Construction", "email": "lisa.martinez@highland.com", "phone": "(555) 789-0123"},
        {"name": "Michael Brown", "role": "Safety Manager", "company": "Highland Construction", "email": "michael.brown@highland.com", "phone": "(555) 890-1234"},
        {"name": "Jennifer Wilson", "role": "Architect", "company": "Modern Design Associates", "email": "jwilson@moderndesign.com", "phone": "(555) 901-2345"},
        {"name": "Steven Thompson", "role": "Structural Engineer", "company": "Thompson Engineering", "email": "steven@thompsoneng.com", "phone": "(555) 012-3456"},
        {"name": "Karen Davis", "role": "MEP Engineer", "company": "Davis MEP Consultants", "email": "karen@davismep.com", "phone": "(555) 123-4568"},
        {"name": "James Wilson", "role": "Civil Engineer", "company": "Wilson & Associates", "email": "james@wilsonassoc.com", "phone": "(555) 234-5679"},
        {"name": "Patricia Miller", "role": "Owner's Representative", "company": "Highland Tower LLC", "email": "patricia@highlandtower.com", "phone": "(555) 345-6780"}
    ]
    
    # Define role colors
    role_colors = {
        "Project Manager": "#3e79f7",
        "Superintendent": "#38d39f",
        "Project Engineer": "#f9c851",
        "Field Engineer": "#f9c851",
        "Project Controls": "#ff5b5b",
        "Cost Engineer": "#ff5b5b",
        "MEP Coordinator": "#f9c851",
        "Safety Manager": "#f76e3e",
        "Architect": "#a05eff",
        "Structural Engineer": "#a05eff",
        "MEP Engineer": "#a05eff",
        "Civil Engineer": "#a05eff",
        "Owner's Representative": "#6c757d"
    }
    
    # Create styled team table
    team_table_html = """
    <table style="width:100%; border-collapse: collapse; margin-bottom: 20px;">
        <thead>
            <tr style="background-color: #f8f9fa; border-bottom: 2px solid #dee2e6;">
                <th style="padding: 10px; text-align: left;">Name</th>
                <th style="padding: 10px; text-align: left;">Role</th>
                <th style="padding: 10px; text-align: left;">Company</th>
                <th style="padding: 10px; text-align: left;">Email</th>
                <th style="padding: 10px; text-align: left;">Phone</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for member in team_members:
        role_color = role_colors.get(member["role"], "#6c757d")
        
        team_table_html += f"""
        <tr style="border-bottom: 1px solid #dee2e6;">
            <td style="padding: 10px;">{member['name']}</td>
            <td style="padding: 10px;">
                <span style="background-color: {role_color}20; color: {role_color}; padding: 3px 8px; border-radius: 12px; font-size: 12px;">
                    {member['role']}
                </span>
            </td>
            <td style="padding: 10px;">{member['company']}</td>
            <td style="padding: 10px;"><a href="mailto:{member['email']}" style="color: #3e79f7; text-decoration: none;">{member['email']}</a></td>
            <td style="padding: 10px;">{member['phone']}</td>
        </tr>
        """
    
    team_table_html += """
        </tbody>
    </table>
    """
    
    st.markdown(team_table_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_project_schedule():
    """Render project schedule information."""
    st.subheader("Project Schedule")
    
    # Schedule overview card
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    
    # Schedule controls
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Schedule Overview")
        view_mode = st.radio("View", ["Gantt Chart", "Milestones", "Calendar"], horizontal=True)
    
    with col2:
        st.markdown("&nbsp;")  # Spacing
        if st.button("Download Schedule", type="secondary"):
            st.success("Schedule downloaded!")
    
    # Schedule visualization - simple Gantt chart
    if view_mode == "Gantt Chart":
        # Sample schedule data
        schedule_items = [
            {"id": 1, "name": "Design Development", "start": "2025-01-05", "end": "2025-02-15", "progress": 100, "dep": None},
            {"id": 2, "name": "Permits & Approvals", "start": "2025-02-01", "end": "2025-03-10", "progress": 100, "dep": 1},
            {"id": 3, "name": "Site Preparation", "start": "2025-03-01", "end": "2025-03-25", "progress": 100, "dep": 2},
            {"id": 4, "name": "Foundation", "start": "2025-03-20", "end": "2025-04-25", "progress": 100, "dep": 3},
            {"id": 5, "name": "Structural Steel", "start": "2025-04-20", "end": "2025-06-15", "progress": 30, "dep": 4},
            {"id": 6, "name": "Building Envelope", "start": "2025-06-01", "end": "2025-07-30", "progress": 0, "dep": 5},
            {"id": 7, "name": "MEP Rough-ins", "start": "2025-06-15", "end": "2025-08-30", "progress": 0, "dep": 5},
            {"id": 8, "name": "Interior Finishes", "start": "2025-08-01", "end": "2025-10-30", "progress": 0, "dep": [6, 7]},
            {"id": 9, "name": "Commissioning", "start": "2025-10-15", "end": "2025-11-15", "progress": 0, "dep": 8},
            {"id": 10, "name": "Substantial Completion", "start": "2025-11-15", "end": "2025-12-01", "progress": 0, "dep": 9}
        ]
        
        # Convert to dataframe for processing
        df = pd.DataFrame(schedule_items)
        
        # Add color coding based on progress
        def get_progress_color(progress):
            if progress == 100:
                return "#38d39f"  # Green for completed
            elif progress > 0:
                return "#3e79f7"  # Blue for in progress
            else:
                return "#6c757d"  # Gray for not started
        
        df["color"] = df["progress"].apply(get_progress_color)
        
        # Create a simplified Gantt chart
        # First parse dates
        df["start_date"] = pd.to_datetime(df["start"])
        df["end_date"] = pd.to_datetime(df["end"])
        
        # Sort by start date
        df = df.sort_values("start_date")
        
        # Get min and max dates
        min_date = df["start_date"].min()
        max_date = df["end_date"].max()
        total_days = (max_date - min_date).days
        
        # Generate Gantt chart HTML
        gantt_html = """
        <div style="margin-top: 20px; overflow-x: auto;">
            <div style="min-width: 800px;">
                <div style="display: flex; margin-bottom: 5px;">
                    <div style="width: 200px; font-weight: 500; padding: 5px;">Task</div>
                    <div style="flex-grow: 1; display: flex; font-weight: 500; padding: 5px;">Timeline</div>
                </div>
        """
        
        today = pd.Timestamp.today()
        
        for _, item in df.iterrows():
            # Calculate position and width for gantt bar
            start_offset = (item["start_date"] - min_date).days / total_days * 100
            duration = (item["end_date"] - item["start_date"]).days / total_days * 100
            
            # Calculate progress bar width
            progress_width = duration * item["progress"] / 100
            
            # Determine if this task is current
            is_current = (item["start_date"] <= today) and (item["end_date"] >= today)
            task_border = "2px solid #3e79f7" if is_current else "none"
            
            gantt_html += f"""
            <div style="display: flex; margin-bottom: 8px; align-items: center;">
                <div style="width: 200px; padding: 5px; font-size: 14px; border-left: {task_border}; padding-left: 8px;">{item["name"]}</div>
                <div style="flex-grow: 1; position: relative; height: 30px; background-color: #f8f9fa; border-radius: 4px;">
                    <div style="position: absolute; left: {start_offset}%; width: {duration}%; height: 100%; background-color: {item["color"]}30; border-radius: 4px;"></div>
                    <div style="position: absolute; left: {start_offset}%; width: {progress_width}%; height: 100%; background-color: {item["color"]}; border-radius: 4px 0 0 4px;"></div>
                    <div style="position: absolute; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 12px;">
                        {item["start"]} to {item["end"]}
                    </div>
                </div>
            </div>
            """
        
        # Add today marker
        today_offset = (today - min_date).days / total_days * 100
        if 0 <= today_offset <= 100:
            gantt_html += f"""
            <div style="position: relative; height: 10px; margin-top: 5px;">
                <div style="position: absolute; left: {today_offset}%; top: -35px; bottom: 0; width: 2px; background-color: #ff5b5b;"></div>
                <div style="position: absolute; left: {today_offset}%; transform: translateX(-50%); background-color: #ff5b5b; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px;">Today</div>
            </div>
            """
        
        gantt_html += """
            </div>
        </div>
        """
        
        st.markdown(gantt_html, unsafe_allow_html=True)
        
    # Milestones view
    elif view_mode == "Milestones":
        # Sample milestone data
        milestones = [
            {"name": "Design Development Complete", "date": "2025-02-15", "status": "Completed"},
            {"name": "All Permits Obtained", "date": "2025-03-10", "status": "Completed"},
            {"name": "Site Preparation Complete", "date": "2025-03-25", "status": "Completed"},
            {"name": "Foundation Complete", "date": "2025-04-25", "status": "Completed"},
            {"name": "Structural Steel Topped Out", "date": "2025-06-15", "status": "In Progress"},
            {"name": "Building Dry-In", "date": "2025-07-30", "status": "Not Started"},
            {"name": "MEP Rough-ins Complete", "date": "2025-08-30", "status": "Not Started"},
            {"name": "Interior Finishes Complete", "date": "2025-10-30", "status": "Not Started"},
            {"name": "Commissioning Complete", "date": "2025-11-15", "status": "Not Started"},
            {"name": "Substantial Completion", "date": "2025-12-01", "status": "Not Started"},
            {"name": "Final Completion", "date": "2025-12-15", "status": "Not Started"}
        ]
        
        # Display milestones with timeline visualization
        st.markdown("#### Project Milestones")
        
        milestone_html = """
        <div style="position: relative; padding-left: 30px; margin-top: 30px; margin-bottom: 30px;">
            <!-- Timeline line -->
            <div style="position: absolute; left: 15px; top: 0; bottom: 0; width: 2px; background-color: #e9ecef;"></div>
        """
        
        for i, milestone in enumerate(milestones):
            # Determine status and colors
            if milestone["status"] == "Completed":
                status_color = "#38d39f"  # Green
                dot_color = "#38d39f"
                date_color = "#6c757d"
            elif milestone["status"] == "In Progress":
                status_color = "#3e79f7"  # Blue
                dot_color = "#3e79f7"
                date_color = "#3e79f7"
            else:
                status_color = "#6c757d"  # Gray
                dot_color = "#dee2e6"
                date_color = "#6c757d"
            
            milestone_html += f"""
            <div style="position: relative; margin-bottom: 20px;">
                <!-- Timeline dot -->
                <div style="position: absolute; left: -15px; width: 16px; height: 16px; background-color: {dot_color}; border-radius: 50%; transform: translateX(-50%);"></div>
                
                <!-- Content box -->
                <div style="background-color: #ffffff; border-radius: 8px; padding: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-left: 10px;">
                    <div style="font-weight: 500;">{milestone['name']}</div>
                    <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 14px;">
                        <div style="color: {date_color};">{milestone['date']}</div>
                        <div style="background-color: {status_color}20; color: {status_color}; padding: 2px 8px; border-radius: 12px; font-size: 12px;">
                            {milestone['status']}
                        </div>
                    </div>
                </div>
            </div>
            """
        
        milestone_html += """
        </div>
        """
        
        st.markdown(milestone_html, unsafe_allow_html=True)
        
    # Calendar view
    else:
        st.markdown("#### Project Calendar")
        
        # Create a month calendar view
        month_names = ["January", "February", "March", "April", "May", "June", 
                       "July", "August", "September", "October", "November", "December"]
        current_month = datetime.now().month - 1  # 0-based index
        
        # Month selector
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            if st.button("◀ Previous"):
                current_month = (current_month - 1) % 12
        with col2:
            st.markdown(f"<h4 style='text-align: center;'>{month_names[current_month]} 2025</h4>", unsafe_allow_html=True)
        with col3:
            if st.button("Next ▶"):
                current_month = (current_month + 1) % 12
        
        # Sample events for different months
        events = {
            0: [  # January
                {"day": 5, "title": "Design Kickoff", "type": "meeting"},
                {"day": 15, "title": "Client Review", "type": "meeting"},
                {"day": 25, "title": "Design Development", "type": "milestone"}
            ],
            1: [  # February
                {"day": 10, "title": "Submit Permits", "type": "milestone"},
                {"day": 15, "title": "Design Complete", "type": "milestone"},
                {"day": 28, "title": "Pre-construction Meeting", "type": "meeting"}
            ],
            2: [  # March
                {"day": 5, "title": "Site Mobilization", "type": "milestone"},
                {"day": 10, "title": "Permits Approved", "type": "milestone"},
                {"day": 15, "title": "Excavation Begins", "type": "task"},
                {"day": 25, "title": "Site Preparation Complete", "type": "milestone"}
            ],
            3: [  # April
                {"day": 1, "title": "Foundation Pour", "type": "task"},
                {"day": 15, "title": "Owner Meeting", "type": "meeting"},
                {"day": 25, "title": "Foundation Complete", "type": "milestone"}
            ],
            4: [  # May
                {"day": 1, "title": "Steel Delivery", "type": "delivery"},
                {"day": 5, "title": "Steel Erection Begins", "type": "task"},
                {"day": 15, "title": "Progress Meeting", "type": "meeting"},
                {"day": 17, "title": "TODAY", "type": "today"}
            ],
            5: [  # June
                {"day": 1, "title": "Roof Start", "type": "task"},
                {"day": 15, "title": "Steel Top Out", "type": "milestone"}
            ],
            6: [  # July
                {"day": 1, "title": "MEP Rough-in Start", "type": "task"},
                {"day": 15, "title": "Progress Meeting", "type": "meeting"},
                {"day": 30, "title": "Building Dry-in", "type": "milestone"}
            ],
            7: [  # August
                {"day": 15, "title": "Interior Framing", "type": "task"},
                {"day": 30, "title": "MEP Rough Complete", "type": "milestone"}
            ],
            8: [  # September
                {"day": 1, "title": "Drywall Start", "type": "task"},
                {"day": 15, "title": "Progress Meeting", "type": "meeting"}
            ],
            9: [  # October
                {"day": 15, "title": "Finishes Begin", "type": "task"},
                {"day": 30, "title": "Finishes Complete", "type": "milestone"}
            ],
            10: [  # November
                {"day": 15, "title": "Commissioning", "type": "milestone"}
            ],
            11: [  # December
                {"day": 1, "title": "Substantial Completion", "type": "milestone"},
                {"day": 15, "title": "Final Completion", "type": "milestone"}
            ]
        }
        
        # Days of the week
        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        
        # Event type colors
        event_colors = {
            "meeting": "#3e79f7",
            "milestone": "#38d39f",
            "task": "#f9c851",
            "delivery": "#ff5b5b",
            "today": "#ff5b5b"
        }
        
        # Create the calendar grid
        calendar_html = """
        <div style="margin-top: 20px;">
            <div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px;">
        """
        
        # Add day headers
        for day in days_of_week:
            calendar_html += f"""
            <div style="padding: 10px; text-align: center; font-weight: 500; background-color: #f8f9fa; border-radius: 4px;">
                {day}
            </div>
            """
        
        # Simple mock calendar - just show 35 days (5 weeks)
        month_events = events.get(current_month, [])
        event_days = {event["day"]: event for event in month_events}
        
        for day in range(1, 36):
            if day <= 31:  # Most months have 31 or fewer days
                event = event_days.get(day)
                has_event = event is not None
                event_type = event["type"] if has_event else None
                event_color = event_colors.get(event_type, "#6c757d") if has_event else "#ffffff"
                event_bg = f"{event_color}20" if has_event else "#ffffff"
                
                calendar_html += f"""
                <div style="min-height: 100px; padding: 10px; background-color: {event_bg}; border: 1px solid #dee2e6; border-radius: 4px; position: relative;">
                    <div style="font-weight: 500;">{day}</div>
                    {f'<div style="margin-top: 5px; padding: 5px; background-color: {event_color}40; border-radius: 4px; font-size: 12px; color: {event_color};">{event["title"]}</div>' if has_event else ''}
                </div>
                """
            else:
                # Empty cells for days beyond the month
                calendar_html += """
                <div style="min-height: 100px; padding: 10px; background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px; opacity: 0.5;"></div>
                """
        
        calendar_html += """
            </div>
        </div>
        """
        
        st.markdown(calendar_html, unsafe_allow_html=True)
    
    # Schedule stats with color indicators
    st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.15;'>", unsafe_allow_html=True)
    
    st.markdown("### Schedule Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""<div style="text-align: center;">
            <div style="font-size: 14px; color: #6c757d;">% Complete</div>
            <div style="font-size: 24px; font-weight: 600; color: #3e79f7;">42%</div>
            <div style="font-size: 12px; color: #38d39f;">On track</div>
        </div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""<div style="text-align: center;">
            <div style="font-size: 14px; color: #6c757d;">SPI</div>
            <div style="font-size: 24px; font-weight: 600; color: #f9c851;">0.98</div>
            <div style="font-size: 12px; color: #f9c851;">Slightly behind</div>
        </div>""", unsafe_allow_html=True)
    
    with col3:
        st.markdown("""<div style="text-align: center;">
            <div style="font-size: 14px; color: #6c757d;">Critical Path</div>
            <div style="font-size: 24px; font-weight: 600; color: #ff5b5b;">-3 days</div>
            <div style="font-size: 12px; color: #ff5b5b;">Behind schedule</div>
        </div>""", unsafe_allow_html=True)
    
    with col4:
        st.markdown("""<div style="text-align: center;">
            <div style="font-size: 14px; color: #6c757d;">Milestones</div>
            <div style="font-size: 24px; font-weight: 600; color: #38d39f;">4/11</div>
            <div style="font-size: 12px; color: #38d39f;">Completed</div>
        </div>""", unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

def render_project_documents():
    """Render project documents section."""
    st.subheader("Project Documents")
    
    # Documents card
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    
    # Document explorer
    st.markdown("### Document Explorer")
    
    # Filter controls
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        doc_type = st.selectbox("Document Type", ["All Documents", "Drawings", "Specifications", "Submittals", "RFIs", "Contracts", "Reports", "Photos"])
    
    with col2:
        doc_search = st.text_input("Search", placeholder="Search documents...")
    
    with col3:
        st.markdown("&nbsp;")  # Spacing
        st.button("Upload Document", type="primary")
    
    # Create a folder/file explorer
    st.markdown("#### Project Files")
    
    # Folder structure
    folders = [
        {
            "name": "01 - Contract Documents",
            "files": [
                {"name": "Owner-Contractor Agreement.pdf", "type": "pdf", "size": "2.4 MB", "date": "2025-01-10"},
                {"name": "General Conditions.pdf", "type": "pdf", "size": "3.7 MB", "date": "2025-01-10"},
                {"name": "Payment Bond.pdf", "type": "pdf", "size": "1.2 MB", "date": "2025-01-15"},
                {"name": "Performance Bond.pdf", "type": "pdf", "size": "1.1 MB", "date": "2025-01-15"}
            ]
        },
        {
            "name": "02 - Design Documents",
            "files": [
                {"name": "Architectural Drawings.pdf", "type": "pdf", "size": "25.8 MB", "date": "2025-02-05"},
                {"name": "Structural Drawings.pdf", "type": "pdf", "size": "18.2 MB", "date": "2025-02-05"},
                {"name": "MEP Drawings.pdf", "type": "pdf", "size": "22.5 MB", "date": "2025-02-05"},
                {"name": "Civil Drawings.pdf", "type": "pdf", "size": "15.3 MB", "date": "2025-02-05"},
                {"name": "Specifications.pdf", "type": "pdf", "size": "8.7 MB", "date": "2025-02-10"}
            ]
        },
        {
            "name": "03 - Submittals",
            "files": [
                {"name": "Concrete Mix Design.pdf", "type": "pdf", "size": "3.2 MB", "date": "2025-03-01"},
                {"name": "Rebar Shop Drawings.pdf", "type": "pdf", "size": "8.5 MB", "date": "2025-03-05"},
                {"name": "Structural Steel Shop Drawings.pdf", "type": "pdf", "size": "12.8 MB", "date": "2025-03-15"},
                {"name": "Glazing Samples.pdf", "type": "pdf", "size": "5.4 MB", "date": "2025-03-20"}
            ]
        },
        {
            "name": "04 - RFIs",
            "files": [
                {"name": "RFI Log.xlsx", "type": "excel", "size": "1.8 MB", "date": "2025-05-15"},
                {"name": "RFI-001 Foundation Details.pdf", "type": "pdf", "size": "2.2 MB", "date": "2025-03-10"},
                {"name": "RFI-002 Steel Connections.pdf", "type": "pdf", "size": "3.5 MB", "date": "2025-04-05"},
                {"name": "RFI-003 MEP Coordination.pdf", "type": "pdf", "size": "4.2 MB", "date": "2025-04-20"}
            ]
        },
        {
            "name": "05 - Meeting Minutes",
            "files": [
                {"name": "Kickoff Meeting Minutes.pdf", "type": "pdf", "size": "1.2 MB", "date": "2025-01-05"},
                {"name": "Weekly Progress Meeting 01.pdf", "type": "pdf", "size": "1.5 MB", "date": "2025-01-15"},
                {"name": "Weekly Progress Meeting 02.pdf", "type": "pdf", "size": "1.4 MB", "date": "2025-01-22"},
                {"name": "OAC Meeting 01.pdf", "type": "pdf", "size": "1.8 MB", "date": "2025-02-01"}
            ]
        },
        {
            "name": "06 - Reports",
            "files": [
                {"name": "Geotechnical Report.pdf", "type": "pdf", "size": "8.4 MB", "date": "2024-12-15"},
                {"name": "Environmental Assessment.pdf", "type": "pdf", "size": "5.6 MB", "date": "2024-12-20"},
                {"name": "Monthly Progress Report - March.pdf", "type": "pdf", "size": "4.2 MB", "date": "2025-04-01"},
                {"name": "Monthly Progress Report - April.pdf", "type": "pdf", "size": "4.5 MB", "date": "2025-05-01"}
            ]
        },
        {
            "name": "07 - Photos",
            "files": [
                {"name": "Site Photos - March.zip", "type": "zip", "size": "45.2 MB", "date": "2025-03-30"},
                {"name": "Site Photos - April.zip", "type": "zip", "size": "52.8 MB", "date": "2025-04-30"},
                {"name": "Foundation Progress.jpg", "type": "image", "size": "2.8 MB", "date": "2025-04-15"},
                {"name": "Steel Erection.jpg", "type": "image", "size": "3.2 MB", "date": "2025-05-10"}
            ]
        }
    ]
    
    # Document explorer with expandable folders and colored file icons
    for folder in folders:
        with st.expander(folder["name"], expanded=False):
            # Create file table with icons
            file_html = """
            <table style="width:100%; border-collapse: collapse; margin-bottom: 10px;">
                <thead>
                    <tr style="background-color: #f8f9fa; border-bottom: 1px solid #dee2e6;">
                        <th style="padding: 8px; text-align: left; width: 50%;">File Name</th>
                        <th style="padding: 8px; text-align: left; width: 15%;">Type</th>
                        <th style="padding: 8px; text-align: left; width: 15%;">Size</th>
                        <th style="padding: 8px; text-align: left; width: 20%;">Date</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for file in folder["files"]:
                # Set icon and color based on file type
                if file["type"] == "pdf":
                    icon = "picture_as_pdf"
                    color = "#ff5b5b"
                elif file["type"] == "excel":
                    icon = "table_chart"
                    color = "#38d39f"
                elif file["type"] == "image":
                    icon = "image"
                    color = "#3e79f7"
                elif file["type"] == "zip":
                    icon = "folder_zip"
                    color = "#f9c851"
                else:
                    icon = "description"
                    color = "#6c757d"
                
                file_html += f"""
                <tr style="border-bottom: 1px solid #dee2e6;">
                    <td style="padding: 8px;">
                        <div style="display: flex; align-items: center;">
                            <span class="material-icons" style="color: {color}; margin-right: 8px;">{icon}</span>
                            <span>{file['name']}</span>
                        </div>
                    </td>
                    <td style="padding: 8px; text-transform: uppercase; font-size: 12px;">{file['type']}</td>
                    <td style="padding: 8px;">{file['size']}</td>
                    <td style="padding: 8px;">{file['date']}</td>
                </tr>
                """
            
            file_html += """
                </tbody>
            </table>
            """
            
            st.markdown(file_html, unsafe_allow_html=True)
    
    # Document stats with colorful indicators
    st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.15;'>", unsafe_allow_html=True)
    
    st.markdown("### Document Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""<div style="text-align: center;">
            <div style="font-size: 14px; color: #6c757d;">Total Documents</div>
            <div style="font-size: 24px; font-weight: 600; color: #3e79f7;">57</div>
            <div style="height: 5px; background-color: #f8f9fa; border-radius: 3px; margin-top: 10px;">
                <div style="width: 100%; height: 100%; background-color: #3e79f7; border-radius: 3px;"></div>
            </div>
        </div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""<div style="text-align: center;">
            <div style="font-size: 14px; color: #6c757d;">Recent Uploads</div>
            <div style="font-size: 24px; font-weight: 600; color: #38d39f;">12</div>
            <div style="height: 5px; background-color: #f8f9fa; border-radius: 3px; margin-top: 10px;">
                <div style="width: 75%; height: 100%; background-color: #38d39f; border-radius: 3px;"></div>
            </div>
        </div>""", unsafe_allow_html=True)
    
    with col3:
        st.markdown("""<div style="text-align: center;">
            <div style="font-size: 14px; color: #6c757d;">Pending Review</div>
            <div style="font-size: 24px; font-weight: 600; color: #f9c851;">8</div>
            <div style="height: 5px; background-color: #f8f9fa; border-radius: 3px; margin-top: 10px;">
                <div style="width: 50%; height: 100%; background-color: #f9c851; border-radius: 3px;"></div>
            </div>
        </div>""", unsafe_allow_html=True)
    
    with col4:
        st.markdown("""<div style="text-align: center;">
            <div style="font-size: 14px; color: #6c757d;">Storage Used</div>
            <div style="font-size: 24px; font-weight: 600; color: #ff5b5b;">2.8 GB</div>
            <div style="height: 5px; background-color: #f8f9fa; border-radius: 3px; margin-top: 10px;">
                <div style="width: 35%; height: 100%; background-color: #ff5b5b; border-radius: 3px;"></div>
            </div>
        </div>""", unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

def render_project_photos():
    """Render project photos section."""
    st.subheader("Project Photos")
    
    # Photos card
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    
    # Photo gallery
    st.markdown("### Project Gallery")
    
    # Filter controls
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        photo_date = st.selectbox("Date Range", ["All Photos", "Last 7 Days", "Last 30 Days", "March 2025", "April 2025", "May 2025"])
    
    with col2:
        photo_category = st.selectbox("Category", ["All Categories", "Aerial", "Progress", "Site Conditions", "Safety", "Quality Control", "Issues"])
    
    with col3:
        st.markdown("&nbsp;")  # Spacing
        st.button("Upload Photos", type="primary")
    
    # Create a photo gallery grid
    st.markdown("#### Recent Photos")
    
    # Sample photo data - Would be loaded from database in real app
    photos = [
        {"url": "https://placehold.co/600x400/3e79f7/ffffff?text=Steel+Erection", "date": "May 10, 2025", "category": "Progress"},
        {"url": "https://placehold.co/600x400/38d39f/ffffff?text=Concrete+Pour", "date": "April 25, 2025", "category": "Progress"},
        {"url": "https://placehold.co/600x400/f9c851/ffffff?text=Site+Overview", "date": "April 20, 2025", "category": "Aerial"},
        {"url": "https://placehold.co/600x400/ff5b5b/ffffff?text=Safety+Inspection", "date": "April 15, 2025", "category": "Safety"},
        {"url": "https://placehold.co/600x400/6c757d/ffffff?text=Foundation+Work", "date": "April 10, 2025", "category": "Progress"},
        {"url": "https://placehold.co/600x400/a05eff/ffffff?text=Site+Preparation", "date": "March 20, 2025", "category": "Progress"},
        {"url": "https://placehold.co/600x400/f76e3e/ffffff?text=Excavation", "date": "March 15, 2025", "category": "Progress"},
        {"url": "https://placehold.co/600x400/3e79f7/ffffff?text=Pre-Construction", "date": "March 5, 2025", "category": "Site Conditions"}
    ]
    
    # Create a grid of photos with information overlay
    gallery_html = """
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-top: 20px;">
    """
    
    for photo in photos:
        gallery_html += f"""
        <div style="position: relative; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <img src="{photo['url']}" style="width: 100%; height: 180px; object-fit: cover;">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(0deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0) 100%); color: white; padding: 15px 10px 10px;">
                <div style="font-size: 14px; margin-bottom: 3px;">{photo['date']}</div>
                <div style="font-size: 12px; background-color: #ffffff40; display: inline-block; padding: 2px 8px; border-radius: 12px;">{photo['category']}</div>
            </div>
        </div>
        """
    
    gallery_html += """
    </div>
    """
    
    st.markdown(gallery_html, unsafe_allow_html=True)
    
    # Load more button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("Load More Photos", use_container_width=True)
    
    # Photo map view
    st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.15;'>", unsafe_allow_html=True)
    
    st.markdown("### Photo Locations")
    st.image("https://placehold.co/1200x400/e9ecef/495057?text=Photo+Location+Map", use_column_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

def render_project_settings():
    """Render project settings."""
    st.subheader("Project Settings")
    
    # Settings card
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    
    # Project settings with colorful sections
    st.markdown("### Project Configuration")
    
    # General settings
    st.markdown('<div style="background-color: #3e79f710; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 3px solid #3e79f7;">', unsafe_allow_html=True)
    st.markdown("#### General Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox("Default View", ["Dashboard", "Schedule", "Budget", "Team"])
    
    with col2:
        st.selectbox("Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
    
    st.toggle("Enable Notifications", value=True)
    st.toggle("Show Project in Public Directory", value=False)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Access control
    st.markdown('<div style="background-color: #f9c85110; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 3px solid #f9c851;">', unsafe_allow_html=True)
    st.markdown("#### Access Control")
    
    st.selectbox("Project Visibility", ["Team Members Only", "Organization Only", "Public"])
    
    # Role permissions table
    roles_html = """
    <table style="width:100%; border-collapse: collapse; margin: 15px 0;">
        <thead>
            <tr style="background-color: #f8f9fa; border-bottom: 2px solid #dee2e6;">
                <th style="padding: 8px; text-align: left;">Role</th>
                <th style="padding: 8px; text-align: center;">View</th>
                <th style="padding: 8px; text-align: center;">Edit</th>
                <th style="padding: 8px; text-align: center;">Create</th>
                <th style="padding: 8px; text-align: center;">Delete</th>
                <th style="padding: 8px; text-align: center;">Admin</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom: 1px solid #dee2e6;">
                <td style="padding: 8px;">Project Manager</td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #38d39f; font-size: 18px;">check_circle</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #38d39f; font-size: 18px;">check_circle</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #38d39f; font-size: 18px;">check_circle</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #38d39f; font-size: 18px;">check_circle</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #38d39f; font-size: 18px;">check_circle</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #dee2e6;">
                <td style="padding: 8px;">Team Member</td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #38d39f; font-size: 18px;">check_circle</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #38d39f; font-size: 18px;">check_circle</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #38d39f; font-size: 18px;">check_circle</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #ff5b5b; font-size: 18px;">cancel</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #ff5b5b; font-size: 18px;">cancel</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #dee2e6;">
                <td style="padding: 8px;">Viewer</td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #38d39f; font-size: 18px;">check_circle</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #ff5b5b; font-size: 18px;">cancel</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #ff5b5b; font-size: 18px;">cancel</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #ff5b5b; font-size: 18px;">cancel</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #ff5b5b; font-size: 18px;">cancel</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #dee2e6;">
                <td style="padding: 8px;">Client</td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #38d39f; font-size: 18px;">check_circle</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #ff5b5b; font-size: 18px;">cancel</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #ff5b5b; font-size: 18px;">cancel</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #ff5b5b; font-size: 18px;">cancel</span></td>
                <td style="padding: 8px; text-align: center;"><span class="material-icons" style="color: #ff5b5b; font-size: 18px;">cancel</span></td>
            </tr>
        </tbody>
    </table>
    """
    
    st.markdown(roles_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Integrations
    st.markdown('<div style="background-color: #38d39f10; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 3px solid #38d39f;">', unsafe_allow_html=True)
    st.markdown("#### Integrations")
    
    integrations = [
        {"name": "Microsoft Project", "status": "Connected", "color": "#38d39f"},
        {"name": "BIM 360", "status": "Not Connected", "color": "#6c757d"},
        {"name": "Procore", "status": "Connected", "color": "#38d39f"},
        {"name": "QuickBooks", "status": "Not Connected", "color": "#6c757d"}
    ]
    
    # Create integration cards
    col1, col2 = st.columns(2)
    
    for i, integration in enumerate(integrations):
        with col1 if i % 2 == 0 else col2:
            if integration["status"] == "Connected":
                button_text = "Disconnect"
                button_type = "secondary"
            else:
                button_text = "Connect"
                button_type = "primary"
                
            st.markdown(f"""
            <div style="padding: 15px; border: 1px solid #dee2e6; border-radius: 8px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div style="font-weight: 500;">{integration["name"]}</div>
                    <div style="background-color: {integration["color"]}20; color: {integration["color"]}; padding: 3px 8px; border-radius: 12px; font-size: 12px;">
                        {integration["status"]}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.button(button_text, key=f"integration_{i}", type=button_type if button_type == "primary" else None)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Advanced settings
    st.markdown('<div style="background-color: #ff5b5b10; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 3px solid #ff5b5b;">', unsafe_allow_html=True)
    st.markdown("#### Advanced Settings")
    
    st.number_input("Cache Expiration (minutes)", min_value=5, max_value=60, value=15)
    st.selectbox("Log Level", ["Error", "Warning", "Info", "Debug"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("Reset Project Settings", key="reset_settings", type="secondary")
    
    with col2:
        st.button("Archive Project", key="archive_project", type="secondary")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Save settings button
    st.button("Save All Settings", key="save_all_settings", type="primary")
        
    st.markdown('</div>', unsafe_allow_html=True)

def get_sample_project_data():
    """Get sample project data for demonstration."""
    return {
        "name": "Highland Tower Development",
        "code": "HTD-2025-001",
        "client": "Highland Properties LLC",
        "type": "Commercial",
        "address": "1250 Highland Avenue",
        "location": "Metro City, State",
        "start_date": date(2025, 1, 5),
        "end_date": date(2025, 12, 15),
        "duration": 345,
        "base_budget": 6800000,
        "contingency_percent": 10.0,
        "contingency_amount": 680000,
        "total_budget": 7480000,
        "contract_type": "Guaranteed Maximum Price",
        "payment_terms": "Monthly",
        "project_manager": "John Smith",
        "superintendent": "Mike Johnson",
        "architect": "Modern Design Associates",
        "engineer": "Thompson Engineering",
        "description": """
        The Highland Tower Development is a 15-story mixed-use commercial building located in the downtown area. 
        The project includes office spaces, retail areas on the ground floor, and underground parking.
        
        Key features include a modern glass curtain wall system, rooftop garden, and energy-efficient HVAC systems.
        The building is targeting LEED Gold certification and includes various sustainable design elements.
        """,
        "status": "Active",
        "priority": "High",
        "created_at": datetime(2024, 12, 1),
        "created_by": "admin"
    }